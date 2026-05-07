#!/usr/bin/env python3
"""Generate a Markdown datasheet for a hardware feature.

Usage:
    python3 generate-datasheet.py --feature <name> --repo-root <path>

Always exits 0 — never crashes CI.
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Markdown datasheet for a hardware feature."
    )
    parser.add_argument("--feature", required=True, help="Feature name")
    parser.add_argument("--repo-root", required=True, help="Repository root path")
    args = parser.parse_args()

    feature = args.feature
    repo_root = args.repo_root

    feature_dir = os.path.join(repo_root, "features", feature)
    datasheet_dir = os.path.join(feature_dir, "datasheet")
    os.makedirs(datasheet_dir, exist_ok=True)

    today = datetime.date.today().strftime("%Y-%m-%d")
    version = _get_version(repo_root, feature)

    specs, specs_warning = _read_specs(os.path.join(datasheet_dir, "specs.yaml"))
    status = _get_status(specs)
    description = _extract_readme_description(os.path.join(feature_dir, "README.md"))
    app_notes = _read_application_notes(
        os.path.join(datasheet_dir, "application-notes.md")
    )
    errata = _read_errata(os.path.join(datasheet_dir, "errata.md"))
    changelog = _read_changelog(os.path.join(feature_dir, "CHANGELOG.md"))
    gate_history = _get_gate_history(repo_root, feature)

    md = _generate_markdown(
        feature=feature,
        version=version,
        status=status,
        today=today,
        description=description,
        specs=specs,
        specs_warning=specs_warning,
        app_notes=app_notes,
        errata=errata,
        changelog=changelog,
        gate_history=gate_history,
    )

    output_path = os.path.join(datasheet_dir, f"{feature}-datasheet.md")
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(md)
    print(f"✅ Datasheet written to {output_path}")


# ---------------------------------------------------------------------------
# Data readers
# ---------------------------------------------------------------------------

def _get_version(repo_root: str, feature: str) -> str:
    """Return current version from release-please manifest, fallback to 1.0.0."""
    manifest_path = os.path.join(repo_root, ".github", "release-please-manifest.json")
    try:
        with open(manifest_path, encoding="utf-8") as fh:
            manifest = json.load(fh)
        # Try exact key first
        for key in (f"features/{feature}", feature):
            if key in manifest:
                return str(manifest[key])
        # Fallback: any key containing the feature name
        for key, val in manifest.items():
            if feature in key and val:
                return str(val)
    except Exception:
        pass
    return "1.0.0"


def _get_status(specs) -> str:
    """Extract status from specs, defaulting to placeholder."""
    if isinstance(specs, dict):
        return str(specs.get("status", "[COMPLETE BEFORE TRR]"))
    return "[COMPLETE BEFORE TRR]"


def _read_specs(specs_path: str):
    """Read and parse specs.yaml. Returns (data_or_None, warning_or_None)."""
    if not HAS_YAML:
        return None, (
            "> ⚠️ specs.yaml not found or invalid — "
            "complete datasheet/specs.yaml and regenerate."
        )
    if not os.path.exists(specs_path):
        return None, (
            "> ⚠️ specs.yaml not found or invalid — "
            "complete datasheet/specs.yaml and regenerate."
        )
    try:
        with open(specs_path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        if not isinstance(data, dict):
            return None, (
                "> ⚠️ specs.yaml not found or invalid — "
                "complete datasheet/specs.yaml and regenerate."
            )
        return data, None
    except Exception:
        return None, (
            "> ⚠️ specs.yaml not found or invalid — "
            "complete datasheet/specs.yaml and regenerate."
        )


def _extract_readme_description(readme_path: str):
    """Extract text between '## What is this feature?' and next --- or ## heading."""
    if not os.path.exists(readme_path):
        return None
    try:
        with open(readme_path, encoding="utf-8") as fh:
            content = fh.read()
        lines = content.split("\n")
        in_section = False
        result = []
        for line in lines:
            if line.strip() == "## What is this feature?":
                in_section = True
                continue
            if in_section:
                if line.startswith("---") or (
                    line.startswith("## ")
                    and line.strip() != "## What is this feature?"
                ):
                    break
                result.append(line)
        text = "\n".join(result).strip()
        return text if text else None
    except Exception:
        return None


def _read_application_notes(path: str):
    """Read application-notes.md; return None if it is just a stub."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        # Strip HTML comments to check for real content
        clean = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL).strip()
        # Strip lines that are only the TRR placeholder
        real_lines = [
            ln
            for ln in clean.split("\n")
            if ln.strip() and "[COMPLETE BEFORE TRR]" not in ln
        ]
        if not real_lines:
            return None
        return content.strip()
    except Exception:
        return None


def _read_errata(path: str):
    """Read errata.md; return None if empty or only comment placeholders."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        # Remove HTML comment blocks
        clean = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL).strip()
        if not clean:
            return None
        return clean
    except Exception:
        return None


def _read_changelog(path: str):
    """Return last 10 section entries from CHANGELOG.md, or None if absent."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            content = fh.read().strip()
        if not content:
            return None
        # Split into ## sections
        entries = []
        current: list = []
        for line in content.split("\n"):
            if line.startswith("## ") and current:
                entries.append("\n".join(current))
                current = [line]
            elif line.startswith("## "):
                current = [line]
            elif current:
                current.append(line)
        if current:
            entries.append("\n".join(current))
        last_10 = entries[-10:]
        result = "\n\n".join(last_10).strip()
        return result if result else None
    except Exception:
        return None


def _get_gate_history(repo_root: str, feature: str) -> dict:
    """Read gate tags via git tag -l."""
    default = {
        "pdr": False,
        "pdr_tag": f"pdr/{feature}/approved",
        "cdr": False,
        "cdr_tag": f"cdr/{feature}/approved",
        "trr": False,
        "trr_tag": f"{feature}-vX.Y.Z-rc.N",
        "release": False,
        "release_tag": f"release/{feature}/approved",
    }
    try:
        result = subprocess.run(
            ["git", "tag", "-l"],
            capture_output=True,
            text=True,
            cwd=repo_root,
            timeout=30,
        )
        tags = set(result.stdout.strip().split("\n"))

        pdr_tag = f"pdr/{feature}/approved"
        cdr_tag = f"cdr/{feature}/approved"
        release_tag = f"release/{feature}/approved"

        # Latest rc tag for TRR
        rc_tags = sorted(
            t for t in tags if t.startswith(f"{feature}-v") and "-rc." in t
        )
        rc_tag = rc_tags[-1] if rc_tags else None

        return {
            "pdr": pdr_tag in tags,
            "pdr_tag": pdr_tag,
            "cdr": cdr_tag in tags,
            "cdr_tag": cdr_tag,
            "trr": rc_tag is not None,
            "trr_tag": rc_tag if rc_tag else f"{feature}-vX.Y.Z-rc.N",
            "release": release_tag in tags,
            "release_tag": release_tag,
        }
    except Exception:
        return default


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------

def _render_table(headers: list, rows: list) -> str:
    """Render a Markdown table."""
    if not rows:
        return "*No entries defined in specs.yaml*\n"
    header_row = "| " + " | ".join(str(h) for h in headers) + " |"
    sep_row = "|" + "|".join("---" for _ in headers) + "|"
    lines = [header_row, sep_row]
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(lines) + "\n"


def _generate_markdown(
    feature: str,
    version: str,
    status: str,
    today: str,
    description,
    specs,
    specs_warning,
    app_notes,
    errata,
    changelog,
    gate_history: dict,
) -> str:
    parts: list = []

    title = feature.upper().replace("-", " ").replace("_", " ").strip()
    parts.append(f"# {title} — Feature Datasheet\n")
    parts.append(f"**Version:** {version}  **Status:** {status}  **Date:** {today}\n")
    parts.append("\n---\n")

    if specs_warning:
        parts.append(f"{specs_warning}\n\n---\n")

    # Description
    parts.append("\n## Description\n")
    if description:
        parts.append(f"\n{description}\n")
    else:
        parts.append("\n[Description not yet written — see README.md]\n")
    parts.append("\n---\n")

    # Absolute Maximum Ratings
    parts.append("\n## Absolute Maximum Ratings\n")
    parts.append(
        "\n> ⚠️ Stresses beyond these values may cause permanent damage."
        " Do not operate at these limits.\n\n"
    )
    if specs and "absolute-maximums" in specs:
        headers = ["Parameter", "Value", "Unit", "Notes"]
        rows = [
            [
                item.get("parameter", ""),
                item.get("value", ""),
                item.get("unit", ""),
                item.get("notes", ""),
            ]
            for item in (specs["absolute-maximums"] or [])
        ]
        parts.append(_render_table(headers, rows))
    else:
        parts.append("*No absolute maximum ratings defined in specs.yaml*\n")
    parts.append("\n---\n")

    # Interface Specifications
    parts.append("\n## Interface Specifications\n\n")
    if specs and "interfaces" in specs:
        headers = [
            "Interface", "Type", "Connector", "Pin",
            "Min", "Nom", "Max", "Unit", "Notes",
        ]
        rows = [
            [
                # specs.yaml uses 'name' as the key — fall back to 'interface' for
                # any legacy specs files that may use the old key name.
                item.get("name", item.get("interface", "")),
                item.get("type", ""),
                item.get("connector", ""),
                item.get("pin", ""),
                item.get("min", ""),
                item.get("nom", ""),
                item.get("max", ""),
                item.get("unit", ""),
                item.get("notes", ""),
            ]
            for item in (specs["interfaces"] or [])
        ]
        parts.append(_render_table(headers, rows))
    else:
        parts.append("*No interface specifications defined in specs.yaml*\n")
    parts.append("\n---\n")

    # Electrical Characteristics
    parts.append("\n## Electrical Characteristics\n\n")
    if specs and "performance" in specs:
        headers = ["Parameter", "Min", "Nom", "Max", "Unit", "Conditions"]
        rows = [
            [
                item.get("parameter", ""),
                item.get("min", ""),
                item.get("nom", ""),
                item.get("max", ""),
                item.get("unit", ""),
                item.get("conditions", ""),
            ]
            for item in (specs["performance"] or [])
        ]
        parts.append(_render_table(headers, rows))
    else:
        parts.append("*No electrical characteristics defined in specs.yaml*\n")
    parts.append("\n---\n")

    # Application Notes
    parts.append("\n## Application Notes\n")
    if app_notes:
        parts.append(f"\n{app_notes}\n")
    else:
        parts.append("\n> ⚠️ COMPLETE BEFORE TRR\n")
    parts.append("\n---\n")

    # Errata (omit section entirely if empty)
    if errata:
        parts.append("\n## Errata\n")
        parts.append(f"\n{errata}\n")
        parts.append("\n---\n")

    # Document Changelog
    parts.append("\n## Document Changelog\n")
    if changelog:
        parts.append(f"\n{changelog}\n")
    else:
        parts.append("\n> No changelog entries yet.\n")
    parts.append("\n---\n")

    # Gate History
    parts.append("\n## Gate History\n\n")
    gh = gate_history
    rows = [
        ["PDR", f"`{gh['pdr_tag']}`", "✅ Cleared" if gh["pdr"] else "⏳ Pending"],
        ["CDR", f"`{gh['cdr_tag']}`", "✅ Cleared" if gh["cdr"] else "⏳ Pending"],
        ["TRR", f"`{gh['trr_tag']}`", "✅ Cleared" if gh["trr"] else "⏳ Pending"],
        [
            "Release",
            f"`{gh['release_tag']}`",
            "✅ Cleared" if gh["release"] else "⏳ Pending",
        ],
    ]
    parts.append(_render_table(["Gate", "Tag", "Status"], rows))
    parts.append("\n---\n")

    parts.append(
        "\n*Generated by `/datasheet` — do not edit this file directly."
        " Edit `datasheet/specs.yaml`, `datasheet/application-notes.md`,"
        " and `datasheet/errata.md`, then regenerate.*\n"
    )

    return "".join(parts)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pylint: disable=broad-except
        print(f"❌ Unexpected error generating datasheet: {exc}", file=sys.stderr)
        sys.exit(0)  # Always exit 0 — never crash CI
