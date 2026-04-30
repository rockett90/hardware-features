#!/usr/bin/env python3
"""Validate that a PR touches only one feature and only allowed top-level dirs."""
import sys

ALLOWED_TOP_LEVEL = {
    '.github', 'assets', 'bench', 'checklists', 'config',
    'guidelines', 'library', 'templates', 'scripts', 'features',
    'tests', 'docs', 'pyproject.toml', '.shellcheckrc', '.gitignore',
    '.gitmodules', 'CONTRIBUTING.md', 'README.md',
}

paths = [line.strip() for line in sys.stdin if line.strip()]
if not paths:
    print("✅ No changed files")
    sys.exit(0)

errors = []
features = set()
for p in paths:
    parts = p.split('/')
    top = parts[0]
    if top not in ALLOWED_TOP_LEVEL:
        errors.append(f"❌ Unexpected top-level directory or file: {top}")
    if top == 'features' and len(parts) > 1:
        features.add(parts[1])

if len(features) > 1:
    errors.append(f"❌ PR touches multiple features: {', '.join(sorted(features))}")

if errors:
    for e in errors: print(e)
    sys.exit(1)

print("✅ Directory structure valid")
