#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLUGIN_DIR = ROOT / "plugins" / "codex-game-studio"
PLUGIN_MANIFEST = PLUGIN_DIR / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
README = ROOT / "README.md"
ENGINE_REFS_DIR = ROOT / "docs" / "engine-reference"

EXPECTED_COUNTS = {
    "workflows": 38,
    "roles": 48,
    "templates": 26,
    "engine_refs": 46,
}

EXPECTED_REPO_URL = "https://github.com/sdvn/codex-gamestudio"
EXPECTED_SCREENSHOTS = [
    "./assets/preview-studio-overview.png",
    "./assets/preview-workflow-router.png",
    "./assets/preview-reference-stack.png",
]
FORBIDDEN_TOKENS = (
    "[TO BE CONFIGURED]",
    "[CHOOSE:",
    "[SPECIFY after choosing engine]",
    "noreply@example.com",
)


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def count_entries() -> dict[str, int]:
    workflows = sum(
        1 for path in (PLUGIN_DIR / "skills").iterdir() if path.is_dir() and (path / "SKILL.md").is_file()
    )
    roles = sum(1 for _ in (PLUGIN_DIR / "references" / "roles").glob("*.md"))
    templates = sum(1 for _ in (PLUGIN_DIR / "references" / "templates").glob("*.md"))
    engine_refs = sum(1 for path in ENGINE_REFS_DIR.rglob("*") if path.is_file())
    return {
        "workflows": workflows,
        "roles": roles,
        "templates": templates,
        "engine_refs": engine_refs,
    }


def validate_counts(errors: list[str]) -> None:
    actual = count_entries()
    for label, expected in EXPECTED_COUNTS.items():
        if actual[label] != expected:
            errors.append(
                f"{label} count is {actual[label]}, expected {expected}. "
                "Update README copy and validator expectations if this change is intentional."
            )

    readme = read_text(README)
    required_strings = [
        "38 workflows. 48 role briefs. One Codex-first production kit.",
        "workflows-38",
        "roles-48",
        "templates-26",
        "engine%20refs-46",
    ]
    for item in required_strings:
        if item not in readme:
            errors.append(f"README is missing required presentation string: {item}")


def validate_manifest(errors: list[str]) -> None:
    manifest = load_json(PLUGIN_MANIFEST)
    marketplace = load_json(MARKETPLACE)

    if manifest.get("name") != "codex-game-studio":
        errors.append("Plugin manifest name must be codex-game-studio.")

    author = manifest.get("author", {})
    if author.get("email") == "noreply@example.com":
        errors.append("Plugin manifest still contains placeholder author email.")

    for key in ("homepage", "repository"):
        if manifest.get(key) != EXPECTED_REPO_URL:
            errors.append(f"Plugin manifest {key} must point to {EXPECTED_REPO_URL}.")

    interface = manifest.get("interface", {})
    if interface.get("websiteURL") != EXPECTED_REPO_URL:
        errors.append(f"Plugin interface websiteURL must point to {EXPECTED_REPO_URL}.")
    screenshots = interface.get("screenshots", [])
    if screenshots != EXPECTED_SCREENSHOTS:
        errors.append(
            "Plugin screenshots must match the expected preview assets in plugin.json."
        )
    for relative_path in EXPECTED_SCREENSHOTS:
        screenshot_path = PLUGIN_DIR / relative_path.removeprefix("./")
        if not screenshot_path.is_file():
            errors.append(f"Screenshot asset is missing: {screenshot_path.relative_to(ROOT)}")

    plugins = marketplace.get("plugins", [])
    if len(plugins) != 1:
        errors.append("Marketplace should expose exactly one local plugin entry.")
        return

    plugin_entry = plugins[0]
    if plugin_entry.get("name") != manifest.get("name"):
        errors.append("Marketplace plugin name does not match plugin manifest.")

    source = plugin_entry.get("source", {})
    if source.get("path") != "./plugins/codex-game-studio":
        errors.append("Marketplace source path must remain ./plugins/codex-game-studio.")


def validate_no_legacy_tokens(errors: list[str]) -> None:
    for path in [README, *ROOT.joinpath("docs").rglob("*"), *PLUGIN_DIR.rglob("*"), *ROOT.joinpath(".agents").rglob("*")]:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for token in FORBIDDEN_TOKENS:
            if token in text:
                errors.append(f"{path.relative_to(ROOT)} still contains forbidden token: {token}")

    claude_hits: list[str] = []
    for path in [README, *ROOT.joinpath("docs").rglob("*"), *PLUGIN_DIR.rglob("*"), *ROOT.joinpath(".agents").rglob("*")]:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "Claude" in text and path != README:
            claude_hits.append(str(path.relative_to(ROOT)))
    if claude_hits:
        errors.append("Claude references remain outside README: " + ", ".join(sorted(claude_hits)))

    readme = read_text(README)
    if "Donchitos/Claude-Code-Game-Studios" not in readme:
        errors.append("README should keep the upstream attribution for the Codex-native port.")


def validate_required_files(errors: list[str]) -> None:
    required_files = [
        ROOT / "docs" / "CODEX-STUDIO.md",
        ROOT / "docs" / "studio" / "technical-preferences.md",
        ROOT / "README.vi.md",
        PLUGIN_DIR / "skills" / "game-studio" / "SKILL.md",
        PLUGIN_DIR / "skills" / "start" / "SKILL.md",
        PLUGIN_DIR / "skills" / "setup-engine" / "SKILL.md",
        ROOT / "docs" / "engine-reference" / "README.md",
    ]
    for path in required_files:
        if not path.is_file():
            errors.append(f"Required file is missing: {path.relative_to(ROOT)}")

    studio_doc = read_text(ROOT / "docs" / "CODEX-STUDIO.md")
    if "`docs/engine-reference/README.md`" not in studio_doc and "Not configured yet" in studio_doc:
        errors.append(
            "docs/CODEX-STUDIO.md should point at docs/engine-reference/README.md until an engine is pinned."
        )

    readme = read_text(README)
    readme_vi = read_text(ROOT / "README.vi.md")
    if 'href="README.vi.md"' not in readme:
        errors.append("README.md should link to README.vi.md in the language switch.")
    if 'href="README.md"' not in readme_vi:
        errors.append("README.vi.md should link back to README.md in the language switch.")
    for relative_path in EXPECTED_SCREENSHOTS:
        asset_ref = relative_path.removeprefix("./")
        if asset_ref not in readme:
            errors.append(f"README.md should reference preview asset {asset_ref}.")
        if asset_ref not in readme_vi:
            errors.append(f"README.vi.md should reference preview asset {asset_ref}.")


def main() -> int:
    errors: list[str] = []
    validate_counts(errors)
    validate_manifest(errors)
    validate_no_legacy_tokens(errors)
    validate_required_files(errors)

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
