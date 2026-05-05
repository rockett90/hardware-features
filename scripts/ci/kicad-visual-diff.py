#!/usr/bin/env python3
"""kicad-visual-diff.py — Generate a visual diff of KiCad schematic and PCB layers.

Usage:
    python3 kicad-visual-diff.py \
        --base-dir /tmp/base \
        --head-dir /tmp/head \
        --feature buck-converter-5v \
        --output-dir /tmp/diff-output [--pcb]

Always exits 0. Errors are recorded as warnings, never crashes.
"""

import argparse
import base64
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Optional dependency detection
# ---------------------------------------------------------------------------

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

try:
    import cairosvg  # type: ignore
    CAIROSVG_AVAILABLE = True
except ImportError:
    CAIROSVG_AVAILABLE = False

try:
    import numpy as np  # type: ignore
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

# ---------------------------------------------------------------------------
# PCB layer constants
# ---------------------------------------------------------------------------

PRIORITY_LAYERS = [
    "F.Cu", "B.Cu", "In1.Cu", "In2.Cu",
    "F.Silkscreen", "B.Silkscreen",
    "F.Courtyard", "B.Courtyard",
    "F.Fab", "B.Fab",
    "Edge.Cuts",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_KICAD_CLI_CHECKED = False
_KICAD_CLI_AVAILABLE = False


def _warn(warnings_list: List[str], msg: str) -> None:
    print(f"WARNING: {msg}", file=sys.stderr)
    warnings_list.append(msg)


def _check_kicad_cli(warnings_list: List[str]) -> bool:
    global _KICAD_CLI_CHECKED, _KICAD_CLI_AVAILABLE
    if _KICAD_CLI_CHECKED:
        return _KICAD_CLI_AVAILABLE
    _KICAD_CLI_CHECKED = True
    result = subprocess.run(["which", "kicad-cli"], capture_output=True)
    _KICAD_CLI_AVAILABLE = result.returncode == 0
    if not _KICAD_CLI_AVAILABLE:
        _warn(warnings_list, "kicad-cli not found on PATH — SVG export skipped for all sheets")
    return _KICAD_CLI_AVAILABLE


# ---------------------------------------------------------------------------
# Step 1 — Discover schematics
# ---------------------------------------------------------------------------

def _collect_sheets(root: Path, feature: str) -> Dict[str, Path]:
    """Return {sheet_filename: absolute_path} for a given root dir."""
    sheets: Dict[str, Path] = {}

    # Primary location: features/<feature>/schematics/*.kicad_sch
    sch_dir = root / "features" / feature / "schematics"
    if sch_dir.is_dir():
        for f in sorted(sch_dir.glob("*.kicad_sch")):
            sheets[f.name] = f

    # Fallback: features/<feature>/<feature>.kicad_sch
    fallback = root / "features" / feature / f"{feature}.kicad_sch"
    if fallback.is_file() and fallback.name not in sheets:
        sheets[fallback.name] = fallback

    return sheets


def find_sheets(
    base_dir: Path, head_dir: Path, feature: str
) -> Dict[str, Tuple[Optional[Path], Optional[Path]]]:
    """Return {sheet_name: (base_path_or_None, head_path_or_None)}."""
    base_sheets = _collect_sheets(base_dir, feature)
    head_sheets = _collect_sheets(head_dir, feature)
    all_names = sorted(set(base_sheets) | set(head_sheets))
    return {
        name: (base_sheets.get(name), head_sheets.get(name))
        for name in all_names
    }


# ---------------------------------------------------------------------------
# PCB discovery
# ---------------------------------------------------------------------------

def find_pcb(
    base_dir: Path, head_dir: Path, feature: str
) -> Tuple[Optional[Path], Optional[Path]]:
    """Return (base_pcb_or_None, head_pcb_or_None) for features/<feature>/<feature>.kicad_pcb."""
    def _pcb(root: Path) -> Optional[Path]:
        p = root / "features" / feature / f"{feature}.kicad_pcb"
        return p if p.is_file() else None

    return _pcb(base_dir), _pcb(head_dir)


# ---------------------------------------------------------------------------
# Step 2 — Export SVG
# ---------------------------------------------------------------------------

def export_svg(
    sch_path: Path, svg_out_dir: Path, warnings_list: List[str]
) -> Optional[Path]:
    """Run kicad-cli and return path of exported SVG, or None on failure."""
    svg_out_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["kicad-cli", "sch", "export", "svg",
         "--output", str(svg_out_dir),
         str(sch_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        _warn(
            warnings_list,
            f"kicad-cli failed for {sch_path.name}: "
            f"{(result.stderr or result.stdout or '').strip()[:300]}",
        )
        return None

    # kicad-cli typically names the output <stem>.svg in the output directory
    expected = svg_out_dir / (sch_path.stem + ".svg")
    if expected.is_file():
        return expected

    # Fallback: pick any SVG that appeared in the output dir
    svgs = sorted(svg_out_dir.glob("*.svg"))
    if svgs:
        return svgs[0]

    _warn(warnings_list, f"kicad-cli ran but no SVG found for {sch_path.name}")
    return None


# ---------------------------------------------------------------------------
# Step 2b — Export PCB layer SVG
# ---------------------------------------------------------------------------

def export_pcb_layer_svg(
    pcb_path: Path, layer: str, svg_out_dir: Path, warnings_list: List[str]
) -> Optional[Path]:
    """Export a single PCB layer as SVG. Returns SVG path or None (including empty layers)."""
    svg_out_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["kicad-cli", "pcb", "export", "svg",
         "--layers", layer,
         "--output", str(svg_out_dir),
         str(pcb_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        _warn(
            warnings_list,
            f"kicad-cli pcb export svg failed for {pcb_path.name} layer {layer}: "
            f"{(result.stderr or result.stdout or '').strip()[:300]}",
        )
        return None

    svgs = sorted(svg_out_dir.glob("*.svg"))
    if not svgs:
        _warn(warnings_list, f"kicad-cli ran but no SVG found for {pcb_path.name} layer {layer}")
        return None

    svg_path = svgs[0]
    # Skip layers that produced an effectively empty SVG
    if svg_path.stat().st_size < 500:
        return None

    return svg_path


# ---------------------------------------------------------------------------
# PCB layer diffing
# ---------------------------------------------------------------------------

def diff_pcb_layers(
    base_pcb: Optional[Path],
    head_pcb: Optional[Path],
    feature: str,
    out_dir: Path,
    warnings_list: List[str],
) -> List[dict]:
    """Return a list of layer result dicts, one per priority layer that is non-empty."""
    layer_results: List[dict] = []

    svg_dir  = out_dir / "pcb_svgs"
    png_dir  = out_dir / "pcb_pngs"
    diff_dir = out_dir / "pcb_diffs"
    for d in (svg_dir, png_dir, diff_dir):
        d.mkdir(parents=True, exist_ok=True)

    for layer in PRIORITY_LAYERS:
        layer_safe = layer.replace(".", "_")

        base_svg: Optional[Path] = None
        head_svg: Optional[Path] = None

        if base_pcb is not None:
            base_svg = export_pcb_layer_svg(
                base_pcb, layer, svg_dir / "base" / layer_safe, warnings_list
            )
        if head_pcb is not None:
            head_svg = export_pcb_layer_svg(
                head_pcb, layer, svg_dir / "head" / layer_safe, warnings_list
            )

        # Skip layer if both sides are empty/missing
        if base_svg is None and head_svg is None:
            continue

        r: dict = {"layer": layer}

        # Classify
        if base_pcb is None:
            r["status"] = "new_pcb"
        elif head_pcb is None:
            r["status"] = "deleted_pcb"
        else:
            r["status"] = "compared"

        # Rasterise base side
        base_png: Optional[Path] = None
        if base_svg is not None:
            base_png_path = png_dir / "base" / f"{layer_safe}.png"
            if rasterize_svg(base_svg, base_png_path, warnings_list):
                base_png = base_png_path
        if base_png:
            r["base_png"] = base_png

        # Rasterise head side
        head_png: Optional[Path] = None
        if head_svg is not None:
            head_png_path = png_dir / "head" / f"{layer_safe}.png"
            if rasterize_svg(head_svg, head_png_path, warnings_list):
                head_png = head_png_path
        if head_png:
            r["head_png"] = head_png

        # Compute pixel diff when both sides are present
        if r["status"] == "compared":
            if base_png is None or head_png is None:
                r["status"] = "unrenderable"
                _warn(
                    warnings_list,
                    f"Cannot diff PCB layer {layer}: "
                    f"{'base' if base_png is None else 'head'} side could not be rendered",
                )
            else:
                diff_path = diff_dir / f"{layer_safe}-diff.png"
                if compute_diff(base_png, head_png, diff_path, warnings_list):
                    r["diff_png"] = diff_path
                else:
                    r["status"] = "unrenderable"

        layer_results.append(r)

    return layer_results


# ---------------------------------------------------------------------------
# Step 3 — Rasterise SVG → PNG
# ---------------------------------------------------------------------------

def rasterize_svg(
    svg_path: Path, png_path: Path, warnings_list: List[str]
) -> bool:
    """Convert SVG to PNG. Returns True on success."""
    png_path.parent.mkdir(parents=True, exist_ok=True)

    # Try cairosvg first
    if CAIROSVG_AVAILABLE:
        try:
            cairosvg.svg2png(  # type: ignore[misc]
                url=str(svg_path), write_to=str(png_path), scale=2.0
            )
            if png_path.is_file():
                return True
        except Exception as exc:
            _warn(warnings_list, f"cairosvg failed for {svg_path.name}: {exc}")

    # Try inkscape fallback
    try:
        result = subprocess.run(
            [
                "inkscape",
                "--export-type=png",
                f"--export-filename={png_path}",
                "--export-dpi=150",
                str(svg_path),
            ],
            capture_output=True,
        )
        if result.returncode == 0 and png_path.is_file():
            return True
    except FileNotFoundError:
        pass  # inkscape not installed

    _warn(
        warnings_list,
        f"Neither cairosvg nor inkscape could rasterize {svg_path.name} "
        f"— sheet marked as unrenderable",
    )
    return False


# ---------------------------------------------------------------------------
# Step 4 — Compute pixel diff
# ---------------------------------------------------------------------------

_TOLERANCE = 10
_WHITE_THRESHOLD = 255 - _TOLERANCE  # 245


def _pad_to_same_size(
    img1: "Image.Image", img2: "Image.Image"
) -> Tuple["Image.Image", "Image.Image"]:
    w = max(img1.width, img2.width)
    h = max(img1.height, img2.height)

    def _pad(img: "Image.Image") -> "Image.Image":
        if img.size == (w, h):
            return img
        canvas = Image.new("RGB", (w, h), (255, 255, 255))
        canvas.paste(img, (0, 0))
        return canvas

    return _pad(img1), _pad(img2)


def _compute_diff_numpy(
    img_base: "Image.Image",
    img_head: "Image.Image",
    diff_path: Path,
    warnings_list: List[str],
) -> bool:
    """Pixel diff using numpy arrays (fast)."""
    try:
        arr_b = np.array(img_base, dtype=np.int16)
        arr_h = np.array(img_head, dtype=np.int16)

        diff = np.abs(arr_b - arr_h)
        changed = diff.max(axis=2) > _TOLERANCE

        base_white = arr_b.min(axis=2) >= _WHITE_THRESHOLD
        head_white = arr_h.min(axis=2) >= _WHITE_THRESHOLD

        removed = changed & ~base_white & head_white   # magenta
        added   = changed & base_white & ~head_white   # cyan
        altered = changed & ~base_white & ~head_white  # amber

        out = np.full((arr_b.shape[0], arr_b.shape[1], 3), 220, dtype=np.uint8)
        out[removed] = [255,   0, 255]
        out[added]   = [  0, 220, 220]
        out[altered] = [255, 180,   0]

        Image.fromarray(out, "RGB").save(diff_path)
        return True
    except Exception as exc:
        _warn(warnings_list, f"numpy diff failed: {exc}")
        return False


def _compute_diff_pillow(
    img_base: "Image.Image",
    img_head: "Image.Image",
    diff_path: Path,
    warnings_list: List[str],
) -> bool:
    """Pixel diff using pure Pillow (slower, no numpy required)."""
    try:
        w, h = img_base.width, img_base.height
        out = Image.new("RGB", (w, h), (220, 220, 220))

        base_pixels = img_base.load()
        head_pixels = img_head.load()
        out_pixels  = out.load()

        for y in range(h):
            for x in range(w):
                rb, gb, bb = base_pixels[x, y][:3]  # type: ignore[index]
                rh, gh, bh = head_pixels[x, y][:3]  # type: ignore[index]

                diff_r = abs(rb - rh)
                diff_g = abs(gb - gh)
                diff_b = abs(bb - bh)

                if max(diff_r, diff_g, diff_b) <= _TOLERANCE:
                    # identical
                    out_pixels[x, y] = (220, 220, 220)
                    continue

                base_is_white = rb >= _WHITE_THRESHOLD and gb >= _WHITE_THRESHOLD and bb >= _WHITE_THRESHOLD
                head_is_white = rh >= _WHITE_THRESHOLD and gh >= _WHITE_THRESHOLD and bh >= _WHITE_THRESHOLD

                if not base_is_white and head_is_white:
                    out_pixels[x, y] = (255, 0, 255)    # removed — magenta
                elif base_is_white and not head_is_white:
                    out_pixels[x, y] = (0, 220, 220)    # added — cyan
                else:
                    out_pixels[x, y] = (255, 180, 0)    # changed — amber

        out.save(diff_path)
        return True
    except Exception as exc:
        _warn(warnings_list, f"Pillow diff failed: {exc}")
        return False


def compute_diff(
    base_png: Path, head_png: Path, diff_path: Path, warnings_list: List[str]
) -> bool:
    """Generate diff image between two PNG files. Returns True on success."""
    if not PILLOW_AVAILABLE:
        _warn(warnings_list, "Pillow not available — cannot compute pixel diff")
        return False

    try:
        img_base = Image.open(base_png).convert("RGB")
        img_head = Image.open(head_png).convert("RGB")
        img_base, img_head = _pad_to_same_size(img_base, img_head)
    except Exception as exc:
        _warn(warnings_list, f"Failed to open images for diff: {exc}")
        return False

    if NUMPY_AVAILABLE:
        return _compute_diff_numpy(img_base, img_head, diff_path, warnings_list)
    return _compute_diff_pillow(img_base, img_head, diff_path, warnings_list)


# ---------------------------------------------------------------------------
# Step 5 — Generate outputs
# ---------------------------------------------------------------------------

def _img_tag(path: Optional[Path]) -> str:
    """Return an <img> HTML tag with base64-embedded PNG, or em dash."""
    if path is None or not path.is_file():
        return "&mdash;"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    uri = f"data:image/png;base64,{data}"
    return f'<img src="{uri}" style="max-width:400px;height:auto;" alt="">'


def generate_html(
    feature: str,
    sheets: Dict[str, Tuple[Optional[Path], Optional[Path]]],
    results: Dict[str, dict],
    base_sha: str,
    head_sha: str,
    ts: str,
    pcb_results: Optional[List[dict]] = None,
) -> str:
    if pcb_results is None:
        pcb_results = []
    rows_html_parts = []
    for name in sheets:
        r = results.get(name, {})
        status = r.get("status", "unrenderable")

        if status == "unrenderable":
            cell = (
                '<td colspan="3" class="warn">'
                "&#9888;&#xFE0F; Could not render this sheet &mdash; check workflow logs"
                "</td>"
            )
            rows_html_parts.append(
                f"<tr><td><code>{name}</code></td>{cell}</tr>"
            )
        elif status == "new":
            head_img = _img_tag(r.get("head_png"))
            rows_html_parts.append(
                f"<tr><td><code>{name}</code></td>"
                f"<td>&mdash;</td>"
                f"<td><span class='badge badge-new'>&#x1F195; New sheet</span></td>"
                f"<td>{head_img}</td></tr>"
            )
        elif status == "deleted":
            base_img = _img_tag(r.get("base_png"))
            rows_html_parts.append(
                f"<tr><td><code>{name}</code></td>"
                f"<td>{base_img}</td>"
                f"<td><span class='badge badge-deleted'>&#x1F5D1;&#xFE0F; Deleted</span></td>"
                f"<td>&mdash;</td></tr>"
            )
        else:  # compared
            base_img = _img_tag(r.get("base_png"))
            diff_img = _img_tag(r.get("diff_png"))
            head_img = _img_tag(r.get("head_png"))
            rows_html_parts.append(
                f"<tr><td><code>{name}</code></td>"
                f"<td>{base_img}</td>"
                f"<td>{diff_img}</td>"
                f"<td>{head_img}</td></tr>"
            )

    rows_html = "\n".join(rows_html_parts)

    # Build PCB layers section if there are results
    pcb_section = ""
    if pcb_results:
        pcb_rows_parts = []
        for pr in pcb_results:
            layer = pr.get("layer", "")
            status = pr.get("status", "unrenderable")
            if status == "unrenderable":
                cell = (
                    '<td colspan="3" class="warn">'
                    "&#9888;&#xFE0F; Could not render this layer &mdash; check workflow logs"
                    "</td>"
                )
                pcb_rows_parts.append(f"<tr><td><code>{layer}</code></td>{cell}</tr>")
            elif status == "new_pcb":
                head_img = _img_tag(pr.get("head_png"))
                pcb_rows_parts.append(
                    f"<tr><td><code>{layer}</code></td>"
                    f"<td>&mdash;</td>"
                    f"<td><span class='badge badge-new'>&#x1F195; New PCB</span></td>"
                    f"<td>{head_img}</td></tr>"
                )
            elif status == "deleted_pcb":
                base_img = _img_tag(pr.get("base_png"))
                pcb_rows_parts.append(
                    f"<tr><td><code>{layer}</code></td>"
                    f"<td>{base_img}</td>"
                    f"<td><span class='badge badge-deleted'>&#x1F5D1;&#xFE0F; Deleted</span></td>"
                    f"<td>&mdash;</td></tr>"
                )
            else:  # compared
                base_img = _img_tag(pr.get("base_png"))
                diff_img = _img_tag(pr.get("diff_png"))
                head_img = _img_tag(pr.get("head_png"))
                pcb_rows_parts.append(
                    f"<tr><td><code>{layer}</code></td>"
                    f"<td>{base_img}</td>"
                    f"<td>{diff_img}</td>"
                    f"<td>{head_img}</td></tr>"
                )
        pcb_rows_html = "\n".join(pcb_rows_parts)
        pcb_section = f"""
<h2>PCB Layers</h2>
<table>
  <thead><tr><th>Layer</th><th>Old (base)</th><th>Diff</th><th>New (head)</th></tr></thead>
  <tbody>
{pcb_rows_html}
  </tbody>
</table>
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Visual Diff &mdash; {feature}</title>
<style>
  body {{ font-family: sans-serif; margin: 1em 2em; color: #222; }}
  h1   {{ font-size: 1.4em; }}
  .legend {{ display: flex; flex-wrap: wrap; gap: 1.5em; margin: 1em 0 2em; align-items: center; }}
  .swatch {{ display: inline-block; width: 20px; height: 20px;
             border: 1px solid #999; vertical-align: middle; margin-right: 4px; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #ccc; padding: 0.5em; vertical-align: top; }}
  th {{ background: #f5f5f5; text-align: left; }}
  .warn {{ background: #fff8dc; color: #8a6d00; }}
  .badge {{ padding: 0.2em 0.6em; border-radius: 4px; font-size: 0.9em;
            display: inline-block; }}
  .badge-new {{ background: #00DCDC; color: #000; }}
  .badge-deleted {{ background: #FF00FF; color: #fff; }}
  footer {{ margin-top: 2em; font-size: 0.85em; color: #666;
            border-top: 1px solid #eee; padding-top: 0.5em; }}
</style>
</head>
<body>
<h1>Visual Diff &mdash; <code>{feature}</code></h1>

<div class="legend">
  <span><span class="swatch" style="background:#00DCDC"></span> Added (cyan)</span>
  <span><span class="swatch" style="background:#FF00FF"></span> Removed (magenta)</span>
  <span><span class="swatch" style="background:#FFB400"></span> Changed (amber)</span>
  <span><span class="swatch" style="background:#DCDCDC"></span> Unchanged (grey)</span>
</div>

<table>
  <thead>
    <tr><th>Sheet</th><th>Old (base)</th><th>Diff</th><th>New (head)</th></tr>
  </thead>
  <tbody>
{rows_html}
  </tbody>
</table>
{pcb_section}
<footer>
  Feature: <code>{feature}</code> &nbsp;|&nbsp;
  BASE_SHA: <code>{base_sha}</code> &nbsp;|&nbsp;
  HEAD_SHA: <code>{head_sha}</code> &nbsp;|&nbsp;
  Generated: {ts}
</footer>
</body>
</html>
"""


def generate_comment_md(
    feature: str,
    sheets: Dict[str, Tuple[Optional[Path], Optional[Path]]],
    results: Dict[str, dict],
    warnings_list: List[str],
    pcb_results: Optional[List[dict]] = None,
) -> str:
    if pcb_results is None:
        pcb_results = []
    lines: List[str] = [
        f"### \U0001f5bc\ufe0f Visual Diff \u2014 `{feature}`",
        "",
        "| Sheet | Result |",
        "|---|---|",
    ]
    for name in sheets:
        r = results.get(name, {})
        status = r.get("status", "unrenderable")
        if status == "new":
            result_str = "\U0001f195 New sheet"
        elif status == "deleted":
            result_str = "\U0001f5d1\ufe0f Deleted"
        elif status == "unrenderable":
            result_str = "\u26a0\ufe0f Could not render"
        else:
            result_str = "\u2705 Diff generated"
        lines.append(f"| `{name}` | {result_str} |")

    lines.append("")
    lines.append(
        "\U0001f4e5 Full HTML diff report available in workflow artifacts (90-day retention)."
    )

    if warnings_list:
        lines.append("")
        lines.append(f"<details><summary>\u26a0\ufe0f Warnings ({len(warnings_list)})</summary>")
        lines.append("")
        for w in warnings_list:
            lines.append(f"- {w}")
        lines.append("")
        lines.append("</details>")

    if pcb_results:
        lines.append("")
        lines.append("**PCB Layers**")
        lines.append("")
        lines.append("| Layer | Result |")
        lines.append("|---|---|")
        for pr in pcb_results:
            layer = pr.get("layer", "")
            status = pr.get("status", "unrenderable")
            if status == "new_pcb":
                result_str = "\U0001f195 New PCB"
            elif status == "deleted_pcb":
                result_str = "\U0001f5d1\ufe0f Deleted"
            elif status == "unrenderable":
                result_str = "\u26a0\ufe0f Could not render"
            else:
                result_str = "\u2705 Diff generated"
            lines.append(f"| {layer} | {result_str} |")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Per-sheet processing helpers
# ---------------------------------------------------------------------------

def _process_side(
    sch_path: Optional[Path],
    side: str,
    svg_dir: Path,
    png_dir: Path,
    kicad_available: bool,
    warnings_list: List[str],
) -> Optional[Path]:
    """Export SVG and rasterise to PNG for one side (base or head)."""
    if sch_path is None:
        return None
    if not kicad_available:
        return None

    svg_out = svg_dir / side
    svg_path = export_svg(sch_path, svg_out, warnings_list)
    if svg_path is None:
        return None

    png_path = png_dir / side / (sch_path.stem + ".png")
    if rasterize_svg(svg_path, png_path, warnings_list):
        return png_path
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a visual diff of KiCad schematic sheets."
    )
    parser.add_argument("--base-dir",   required=True, type=Path,
                        help="Directory containing the base (old) files")
    parser.add_argument("--head-dir",   required=True, type=Path,
                        help="Directory containing the head (new) files")
    parser.add_argument("--feature",    required=True,
                        help="Feature name (e.g. buck-converter-5v)")
    parser.add_argument("--output-dir", required=True, type=Path,
                        help="Directory where outputs will be written")
    parser.add_argument("--pcb", action="store_true", default=False,
                        help="Also diff PCB layers when .kicad_pcb files are present")
    args = parser.parse_args()

    base_dir: Path  = args.base_dir
    head_dir: Path  = args.head_dir
    feature: str    = args.feature
    out_dir: Path   = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    warnings_list: List[str] = []
    base_sha = os.environ.get("BASE_SHA", "unknown")
    head_sha = os.environ.get("HEAD_SHA", "unknown")
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # ---- Step 1: Discover schematics ----------------------------------------
    sheets = find_sheets(base_dir, head_dir, feature)
    if not sheets:
        _warn(
            warnings_list,
            f"No .kicad_sch files found for feature '{feature}' "
            f"in either base-dir or head-dir",
        )

    # ---- Step 2: Check kicad-cli availability --------------------------------
    kicad_available = _check_kicad_cli(warnings_list)

    # Working subdirectories
    svg_dir  = out_dir / "svgs"
    png_dir  = out_dir / "pngs"
    diff_dir = out_dir / "diffs"
    for d in (svg_dir, png_dir, diff_dir):
        d.mkdir(parents=True, exist_ok=True)

    results: Dict[str, dict] = {}
    sheets_compared: List[str] = []
    sheets_new:      List[str] = []
    sheets_deleted:  List[str] = []

    for name, (base_sch, head_sch) in sheets.items():
        r: dict = {}

        # Classify sheet
        if base_sch is None:
            status = "new"
            sheets_new.append(name)
        elif head_sch is None:
            status = "deleted"
            sheets_deleted.append(name)
        else:
            status = "compared"
            sheets_compared.append(name)

        r["status"] = status

        # ---- Steps 2 + 3: Export and rasterise --------------------------------
        base_png = _process_side(
            base_sch, "base", svg_dir, png_dir, kicad_available, warnings_list
        )
        head_png = _process_side(
            head_sch, "head", svg_dir, png_dir, kicad_available, warnings_list
        )

        if base_png:
            r["base_png"] = base_png
        if head_png:
            r["head_png"] = head_png

        # ---- Step 4: Compute pixel diff (compared sheets only) ----------------
        if status == "compared":
            if base_png is None or head_png is None:
                r["status"] = "unrenderable"
                _warn(
                    warnings_list,
                    f"Cannot diff {name}: "
                    f"{'base' if base_png is None else 'head'} side could not be rendered",
                )
            else:
                diff_path = diff_dir / (Path(name).stem + "-diff.png")
                if compute_diff(base_png, head_png, diff_path, warnings_list):
                    r["diff_png"] = diff_path
                else:
                    r["status"] = "unrenderable"

        elif status in ("new", "deleted"):
            # Mark unrenderable only if kicad-cli is available but rendering failed
            side_png = head_png if status == "new" else base_png
            if side_png is None and kicad_available:
                r["status"] = "unrenderable"

        results[name] = r

    # ---- PCB layer diff (when --pcb flag is set) ----------------------------
    pcb_results: List[dict] = []
    layers_compared: List[str] = []
    layers_skipped:  List[str] = []

    if args.pcb:
        base_pcb, head_pcb = find_pcb(base_dir, head_dir, feature)
        if base_pcb is None and head_pcb is None:
            _warn(
                warnings_list,
                f"--pcb specified but no .kicad_pcb file found for feature '{feature}' "
                f"in either base-dir or head-dir",
            )
        else:
            pcb_results = diff_pcb_layers(
                base_pcb, head_pcb, feature, out_dir, warnings_list
            )
            for pr in pcb_results:
                if pr.get("status") == "unrenderable":
                    layers_skipped.append(pr["layer"])
                else:
                    layers_compared.append(pr["layer"])

        # Also track layers present in PRIORITY_LAYERS but not in pcb_results
        processed_layers = {pr["layer"] for pr in pcb_results}
        for layer in PRIORITY_LAYERS:
            if layer not in processed_layers:
                layers_skipped.append(layer)

    # ---- Step 5: Generate outputs -------------------------------------------

    # diff-report.html
    html_content = generate_html(
        feature, sheets, results, base_sha, head_sha, ts,
        pcb_results=pcb_results,
    )
    (out_dir / "diff-report.html").write_text(html_content, encoding="utf-8")

    # metadata.json
    metadata = {
        "feature":          feature,
        "base_sha":         base_sha,
        "head_sha":         head_sha,
        "sheets_compared":  sheets_compared,
        "sheets_new":       sheets_new,
        "sheets_deleted":   sheets_deleted,
        "layers_compared":  layers_compared,
        "layers_skipped":   layers_skipped,
        "warnings":         warnings_list,
    }
    (out_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # comment.md
    comment_md = generate_comment_md(
        feature, sheets, results, warnings_list,
        pcb_results=pcb_results,
    )
    (out_dir / "comment.md").write_text(comment_md, encoding="utf-8")

    print(f"kicad-visual-diff complete. Outputs in {out_dir}")
    print(f"  Sheets compared: {len(sheets_compared)}, "
          f"new: {len(sheets_new)}, deleted: {len(sheets_deleted)}")
    if args.pcb:
        print(f"  PCB layers compared: {len(layers_compared)}, "
              f"skipped: {len(layers_skipped)}")
    if warnings_list:
        print(f"  {len(warnings_list)} warning(s):")
        for w in warnings_list:
            print(f"    - {w}")

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"FATAL: {exc}", file=sys.stderr)
        sys.exit(0)  # always exit 0
