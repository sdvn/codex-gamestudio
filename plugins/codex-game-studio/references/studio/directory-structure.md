# Directory Structure

```text
/
├── .agents/                     # Codex plugin marketplace registration
├── plugins/                     # Local Codex plugins
│   └── codex-game-studio/
│       └── references/          # Role briefs, templates, and studio guidance
├── docs/
│   ├── CODEX-STUDIO.md          # Project configuration for Codex workflows
│   ├── studio/                  # Working technical preferences
│   └── engine-reference/        # Version-pinned engine notes
├── src/                         # Godot-oriented runtime code and scenes when the project uses Godot
├── assets/                      # Shared asset source files for non-Unity pipelines
├── Assets/                      # Unity runtime assets, scenes, scripts, and tests (if using Unity)
├── Source/                      # Unreal C++ modules and tests (if using Unreal)
├── Content/                     # Unreal content root for maps, materials, and Blueprint assets
├── design/                      # Game design documents (gdd, narrative, levels, balance)
├── tests/                       # Test suites (unit, integration, performance, playtest)
├── tools/                       # Build and pipeline tools (ci, build, asset-pipeline)
├── prototypes/                  # Throwaway prototypes (isolated from src/)
└── production/                  # Production management (sprints, milestones, releases)
    ├── session-state/           # Ephemeral session state (active.md — gitignored)
    └── session-logs/            # Session audit trail (gitignored)
```
