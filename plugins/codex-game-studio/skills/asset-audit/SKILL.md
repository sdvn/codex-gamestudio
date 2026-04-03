---
name: asset-audit
description: Audits game assets for compliance with naming conventions, file size budgets, format standards, and pipeline requirements. Identifies orphaned assets, missing references, and standard violations.
---

## Codex Compatibility

This is a Codex-native game production workflow.

- Ask the user directly in plain text when a decision or approval is needed.
- Work locally by default instead of assuming custom subagents exist.
- Use Codex `worker` or `explorer` agents only when the user explicitly asks for delegation or parallel work.
- Keep the studio conventions in `docs/CODEX-STUDIO.md`, `docs/studio/technical-preferences.md`, and the plugin references under `plugins/codex-game-studio/references/` in mind while executing this workflow.

When this skill is invoked:

1. **Read the art bible or asset standards** from the relevant design docs and
   the docs/CODEX-STUDIO.md naming conventions.

2. **Scan the target asset directory** using Glob:
   - `assets/art/**/*` for art assets
   - `assets/audio/**/*` for audio assets
   - `assets/vfx/**/*` for VFX assets
   - `assets/shaders/**/*` for shaders
   - `assets/data/**/*` for data files

3. **Check naming conventions**:
   - Art: `[category]_[name]_[variant]_[size].[ext]`
   - Audio: `[category]_[context]_[name]_[variant].[ext]`
   - All files must be lowercase with underscores

4. **Check file standards**:
   - Textures: Power-of-two dimensions, correct format (PNG for UI, compressed
     for 3D), within size budget
   - Audio: Correct sample rate, format (OGG for SFX, OGG/MP3 for music),
     within duration limits
   - Data: Valid JSON/YAML, schema-compliant

5. **Check for orphaned assets** by searching code for references to each
   asset file.

6. **Check for missing assets** by searching code for asset references and
   verifying the files exist.

7. **Output the audit**:

```markdown
# Asset Audit Report -- [Category] -- [Date]

## Summary
- **Total assets scanned**: [N]
- **Naming violations**: [N]
- **Size violations**: [N]
- **Format violations**: [N]
- **Orphaned assets**: [N]
- **Missing assets**: [N]
- **Overall health**: [CLEAN / MINOR ISSUES / NEEDS ATTENTION]

## Naming Violations
| File | Expected Pattern | Issue |
|------|-----------------|-------|

## Size Violations
| File | Budget | Actual | Overage |
|------|--------|--------|---------|

## Format Violations
| File | Expected Format | Actual Format |
|------|----------------|---------------|

## Orphaned Assets (no code references found)
| File | Last Modified | Size | Recommendation |
|------|-------------|------|---------------|

## Missing Assets (referenced but not found)
| Reference Location | Expected Path |
|-------------------|---------------|

## Recommendations
[Prioritized list of fixes]
```
