# Directory Structure

```text
/
├── .agents/                     # Codex plugin marketplace registration
├── plugins/                     # Local Codex plugins
│   └── claude-code-game-studios-codex/
│       └── references/          # Role briefs, templates, and studio guidance
├── docs/
│   ├── CODEX-STUDIO.md          # Project configuration for Codex workflows
│   ├── studio/                  # Working technical preferences
│   └── engine-reference/        # Version-pinned engine notes
├── src/                         # Game source code (core, gameplay, ai, networking, ui, tools)
├── assets/                      # Game assets (art, audio, vfx, shaders, data)
├── design/                      # Game design documents (gdd, narrative, levels, balance)
├── tests/                       # Test suites (unit, integration, performance, playtest)
├── tools/                       # Build and pipeline tools (ci, build, asset-pipeline)
├── prototypes/                  # Throwaway prototypes (isolated from src/)
└── production/                  # Production management (sprints, milestones, releases)
    ├── session-state/           # Ephemeral session state (active.md — gitignored)
    └── session-logs/            # Session audit trail (gitignored)
```
