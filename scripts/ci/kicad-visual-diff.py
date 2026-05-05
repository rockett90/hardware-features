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

try:
    import sexpdata  # type: ignore
    SEXPDATA_AVAILABLE = True
except ImportError:
    SEXPDATA_AVAILABLE = False

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

# SVG files smaller than this are considered empty board layers and are skipped.
# kicad-cli may export a near-empty SVG (just a bounding box) for layers with no
# copper or other content; 500 bytes is well above metadata but below any real content.
_MIN_SVG_SIZE_BYTES = 500

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
    if svg_path.stat().st_size < _MIN_SVG_SIZE_BYTES:
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
# Semantic diff (sexpdata)
# ---------------------------------------------------------------------------

def _sym_type(item: object) -> Optional[str]:
    """Return the type name of an S-expression list element, or None."""
    if not isinstance(item, list) or not item:
        return None
    first = item[0]
    if hasattr(first, "value"):
        return str(first.value())
    return None


def _sexp_find_all(tree: list, type_name: str) -> List[list]:
    """Return all direct children of *tree* whose type matches *type_name*."""
    if not isinstance(tree, list):
        return []
    return [item for item in tree if _sym_type(item) == type_name]


def _get_property(element: list, key: str) -> Optional[str]:
    """Extract value for a named property inside a KiCad element.

    Handles both KiCad 6+ ``(property "Key" "Value" …)`` format and the
    older flat ``(reference "R7")`` / ``(value "10k")`` style.
    """
    for item in element:
        if _sym_type(item) == "property":
            if len(item) >= 3 and item[1] == key:
                val = item[2]
                return str(val) if isinstance(val, str) else None
    # Older flat style — map standard property names
    legacy_map = {
        "Reference": "reference",
        "Value": "value",
        "Footprint": "footprint",
    }
    legacy_tag = legacy_map.get(key)
    if legacy_tag:
        for item in element:
            if _sym_type(item) == legacy_tag and len(item) >= 2:
                val = item[1]
                return str(val) if isinstance(val, str) else None
    return None


def _extract_placed_symbols(tree: list) -> Dict[str, Dict[str, str]]:
    """Return {reference: {value, footprint}} for placed symbol instances."""
    syms: Dict[str, Dict[str, str]] = {}
    for item in tree:
        if _sym_type(item) != "symbol":
            continue
        ref = _get_property(item, "Reference")
        if ref is None:
            continue  # skip lib_symbols entries and unresolved instances
        val = _get_property(item, "Value") or ""
        fp  = _get_property(item, "Footprint") or ""
        syms[ref] = {"value": val, "footprint": fp}
    return syms


def _count_wires(tree: list) -> int:
    """Count wire elements at the top level of the schematic tree."""
    if not isinstance(tree, list):
        return 0
    return sum(1 for item in tree if _sym_type(item) == "wire")


def _extract_label_texts(tree: list) -> "Set[str]":
    """Return the set of all net/global label texts in the schematic tree."""
    texts: Set[str] = set()
    for item in tree:
        if _sym_type(item) not in ("net_label", "global_label", "label"):
            continue
        # KiCad 7+: (net_label "TEXT" ...) or (label "TEXT" ...)
        if len(item) >= 2 and isinstance(item[1], str):
            texts.add(item[1])
            continue
        # KiCad 6+: (net_label ... (property "Value" "TEXT") ...)
        val = _get_property(item, "Value")
        if val:
            texts.add(val)
    return texts


def _extract_sheet_filenames(tree: list) -> "Set[str]":
    """Return the set of hierarchical sheet filenames referenced in the schematic."""
    filenames: Set[str] = set()
    for item in tree:
        if _sym_type(item) != "sheet":
            continue
        fn = _get_property(item, "Sheet file")
        if fn:
            filenames.add(fn)
    return filenames


def parse_schematic_changes(
    base_sch: Path,
    head_sch: Path,
    sheet_name: str,
    warnings_list: List[str],
) -> List[dict]:
    """Parse two .kicad_sch S-expression files and return a list of change dicts.

    Returns an empty list when sexpdata is unavailable or parsing fails.
    High-confidence changes are reported precisely; uncertain situations
    are recorded as ``unknown_change`` with ``confidence: low``.
    """
    if not SEXPDATA_AVAILABLE:
        return []

    changes: List[dict] = []

    def _load(path: Path) -> Optional[list]:
        try:
            return sexpdata.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            _warn(warnings_list, f"sexpdata: failed to parse {path.name}: {exc}")
            return None

    base_tree = _load(base_sch)
    head_tree = _load(head_sch)

    if base_tree is None or head_tree is None:
        return []

    # ---- Symbols -----------------------------------------------------------
    try:
        base_syms = _extract_placed_symbols(base_tree)
        head_syms = _extract_placed_symbols(head_tree)
        all_refs = set(base_syms) | set(head_syms)
        for ref in sorted(all_refs):
            if ref in head_syms and ref not in base_syms:
                changes.append({
                    "type": "symbol_added",
                    "reference": ref,
                    "value": head_syms[ref]["value"],
                    "sheet": sheet_name,
                    "confidence": "high",
                })
            elif ref in base_syms and ref not in head_syms:
                changes.append({
                    "type": "symbol_removed",
                    "reference": ref,
                    "value": base_syms[ref]["value"],
                    "sheet": sheet_name,
                    "confidence": "high",
                })
            else:
                b = base_syms[ref]
                h = head_syms[ref]
                if b["value"] != h["value"]:
                    changes.append({
                        "type": "symbol_value_changed",
                        "reference": ref,
                        "old": b["value"],
                        "new": h["value"],
                        "sheet": sheet_name,
                        "confidence": "high",
                    })
                if b["footprint"] != h["footprint"]:
                    changes.append({
                        "type": "symbol_footprint_changed",
                        "reference": ref,
                        "old": b["footprint"],
                        "new": h["footprint"],
                        "sheet": sheet_name,
                        "confidence": "high",
                    })
    except Exception as exc:
        _warn(warnings_list, f"sexpdata: symbol extraction failed for {sheet_name}: {exc}")
        changes.append({
            "type": "unknown_change",
            "sheet": sheet_name,
            "confidence": "low",
            "description": f"Symbol extraction error: {exc}",
        })

    # ---- Wires -------------------------------------------------------------
    try:
        base_wires = _count_wires(base_tree)
        head_wires = _count_wires(head_tree)
        if base_wires != head_wires:
            changes.append({
                "type": "wire_count_changed",
                "base_count": base_wires,
                "head_count": head_wires,
                "sheet": sheet_name,
                "confidence": "medium",
            })
    except Exception as exc:
        _warn(warnings_list, f"sexpdata: wire count failed for {sheet_name}: {exc}")

    # ---- Net labels --------------------------------------------------------
    try:
        base_labels = _extract_label_texts(base_tree)
        head_labels = _extract_label_texts(head_tree)
        for lbl in sorted(head_labels - base_labels):
            changes.append({
                "type": "net_label_added",
                "label": lbl,
                "sheet": sheet_name,
                "confidence": "high",
            })
        for lbl in sorted(base_labels - head_labels):
            changes.append({
                "type": "net_label_removed",
                "label": lbl,
                "sheet": sheet_name,
                "confidence": "high",
            })
    except Exception as exc:
        _warn(warnings_list, f"sexpdata: label extraction failed for {sheet_name}: {exc}")

    # ---- Hierarchical sheets -----------------------------------------------
    try:
        base_hsheets = _extract_sheet_filenames(base_tree)
        head_hsheets = _extract_sheet_filenames(head_tree)
        for fn in sorted(head_hsheets - base_hsheets):
            changes.append({
                "type": "hierarchical_sheet_added",
                "filename": fn,
                "sheet": sheet_name,
                "confidence": "high",
            })
        for fn in sorted(base_hsheets - head_hsheets):
            changes.append({
                "type": "hierarchical_sheet_removed",
                "filename": fn,
                "sheet": sheet_name,
                "confidence": "high",
            })
    except Exception as exc:
        _warn(warnings_list, f"sexpdata: sheet extraction failed for {sheet_name}: {exc}")

    return changes


# ---------------------------------------------------------------------------
# Step 5 — Generate outputs
# ---------------------------------------------------------------------------

_CHANGE_TYPE_LABELS: Dict[str, str] = {
    "symbol_added":               "Symbol added",
    "symbol_removed":             "Symbol removed",
    "symbol_value_changed":       "Value changed",
    "symbol_footprint_changed":   "Footprint changed",
    "wire_count_changed":         "Wire count changed",
    "net_label_added":            "Net label added",
    "net_label_removed":          "Net label removed",
    "hierarchical_sheet_added":   "Sheet added",
    "hierarchical_sheet_removed": "Sheet removed",
    "unknown_change":             "Unknown change",
}


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
    changes: Optional[List[dict]] = None,
    pcb_results: Optional[List[dict]] = None,
) -> str:
    if changes is None:
        changes = []
    if pcb_results is None:
        pcb_results = []

    # ---- Change summary section --------------------------------------------

    def _change_row_html(ch: dict) -> str:
        ctype  = ch.get("type", "unknown")
        sheet  = ch.get("sheet", "")
        conf   = ch.get("confidence", "")
        ref    = ch.get("reference", "&mdash;")
        label  = _CHANGE_TYPE_LABELS.get(ctype, ctype.replace("_", " "))
        if ctype in ("symbol_value_changed", "symbol_footprint_changed"):
            detail = f"{ch.get('old', '')} &rarr; {ch.get('new', '')}"
        elif ctype in ("symbol_added", "symbol_removed"):
            detail = ch.get("value", "")
        elif ctype == "wire_count_changed":
            detail = f"{ch.get('base_count', 0)} &rarr; {ch.get('head_count', 0)}"
            ref = "&mdash;"
        elif ctype in ("net_label_added", "net_label_removed"):
            detail = ch.get("label", "")
            ref = "&mdash;"
        elif ctype in ("hierarchical_sheet_added", "hierarchical_sheet_removed"):
            detail = ch.get("filename", "")
            ref = "&mdash;"
        elif ctype == "unknown_change":
            detail = ch.get("description", "")
            ref = "&mdash;"
        else:
            detail = ""
        return (
            f"<tr><td>{label}</td><td>{ref}</td><td>{detail}</td>"
            f"<td>{sheet}</td><td>{conf}</td></tr>"
        )

    if changes:
        change_rows = "\n".join(_change_row_html(ch) for ch in changes)
        changes_section = f"""<details>
  <summary>&#x1F4CB; Change summary ({len(changes)} changes)</summary>
  <table class="changes-table">
    <thead><tr><th>Type</th><th>Reference</th><th>Detail</th><th>Sheet</th><th>Confidence</th></tr></thead>
    <tbody>
{change_rows}
    </tbody>
  </table>
</details>"""
    else:
        changes_section = (
            "<p><em>Semantic diff unavailable &mdash; "
            "sexpdata not installed or no changes detected.</em></p>"
        )

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
  details {{ margin: 1em 0 1.5em; }}
  .changes-table {{ border-collapse: collapse; width: 100%; font-size: 0.9em; }}
  .changes-table th, .changes-table td {{ border: 1px solid #ccc; padding: 0.3em 0.5em; }}
  .changes-table th {{ background: #f5f5f5; text-align: left; }}
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

{changes_section}

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
    changes: Optional[List[dict]] = None,
    pcb_results: Optional[List[dict]] = None,
) -> str:
    if changes is None:
        changes = []
    if pcb_results is None:
        pcb_results = []

    lines: List[str] = [
        f"### \U0001f5bc\ufe0f Visual Diff \u2014 `{feature}`",
        "",
    ]

    # ---- Change summary (high-confidence only, max 10 items) ---------------
    high_conf = [ch for ch in changes if ch.get("confidence") == "high"]
    if high_conf:
        n_total = len(high_conf)
        count_label = f"{n_total}" if n_total <= 10 else f"{n_total} (showing 10)"
        lines.append(f"**Changes detected:** {count_label}")
        lines.append("")
        lines.append("| Type | Reference | Detail |")
        lines.append("|---|---|---|")
        for ch in high_conf[:10]:
            ctype  = ch.get("type", "unknown")
            ref    = ch.get("reference", "\u2014")
            label  = _CHANGE_TYPE_LABELS.get(ctype, ctype.replace("_", " "))
            if ctype in ("symbol_value_changed", "symbol_footprint_changed"):
                detail = f"{ch.get('old', '')} \u2192 {ch.get('new', '')}"
            elif ctype in ("symbol_added", "symbol_removed"):
                detail = ch.get("value", "")
            elif ctype in ("net_label_added", "net_label_removed"):
                detail = ch.get("label", "")
                ref = "\u2014"
            elif ctype in ("hierarchical_sheet_added", "hierarchical_sheet_removed"):
                detail = ch.get("filename", "")
                ref = "\u2014"
            else:
                detail = ""
            lines.append(f"| {label} | {ref} | {detail} |")
        lines.append("")

    # ---- Sheet result table ------------------------------------------------
    lines += [
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

        # Also record layers that were absent on both sides (empty on both base and
        # head) as skipped, so metadata.json gives a complete picture of all
        # PRIORITY_LAYERS that were considered but not compared.
        processed_layers = {pr["layer"] for pr in pcb_results}
        for layer in PRIORITY_LAYERS:
            if layer not in processed_layers:
                layers_skipped.append(layer)

    # ---- Step 5: Generate outputs -------------------------------------------

    # Semantic diff — parse compared sheets and aggregate changes
    all_changes: List[dict] = []
    if sheets_compared and SEXPDATA_AVAILABLE:
        for name in sheets_compared:
            base_sch, head_sch = sheets[name]
            if base_sch is not None and head_sch is not None:
                sheet_changes = parse_schematic_changes(
                    base_sch, head_sch, name, warnings_list
                )
                all_changes.extend(sheet_changes)

    # changes.json — written when compared sheets exist or sexpdata unavailable
    if sheets_compared or not SEXPDATA_AVAILABLE:
        if SEXPDATA_AVAILABLE:
            changes_json: dict = {
                "feature":       feature,
                "total_changes": len(all_changes),
                "changes":       all_changes,
            }
        else:
            changes_json = {
                "feature":       feature,
                "total_changes": 0,
                "changes":       [],
                "warning":       "sexpdata not available",
            }
        (out_dir / "changes.json").write_text(
            json.dumps(changes_json, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    # diff-report.html
    html_content = generate_html(
        feature, sheets, results, base_sha, head_sha, ts,
        all_changes, pcb_results=pcb_results,
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
        feature, sheets, results, warnings_list, all_changes,
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
