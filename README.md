# Game Studios for Codex

Codex-native port of
[`Donchitos/Claude-Code-Game-Studios`](https://github.com/Donchitos/Claude-Code-Game-Studios),
cleaned to keep only the parts needed for Codex.

## What Stays

- Local plugin:
  `plugins/claude-code-game-studios-codex/`
- Plugin marketplace entry:
  `.agents/plugins/marketplace.json`
- Codex project configuration:
  `docs/CODEX-STUDIO.md`
- Technical preferences working file:
  `docs/studio/technical-preferences.md`
- Engine reference docs:
  `docs/engine-reference/`
- Production session state:
  `production/session-state/`

## Plugin Contents

- 38 Codex skills
  - 37 ported from the upstream Claude template
  - 1 Codex-only router skill: `game-studio`
- Role briefs copied into:
  `plugins/claude-code-game-studios-codex/references/roles/`
- Document templates copied into:
  `plugins/claude-code-game-studios-codex/references/templates/`
- Studio reference docs copied into:
  `plugins/claude-code-game-studios-codex/references/studio/`

## Main Entry Points

- `game-studio`
- `start`
- `setup-engine`
- `project-stage-detect`
- `team-combat`
- `team-ui`
- `code-review`

## Notes

- This repo is intentionally Codex-first. The old `.claude/` runtime layout is
  removed after migration.
- Upstream authorship and license are preserved in `LICENSE`.
- Cleanup and compatibility notes are in `docs/CODEX-PORT.md`.
