# Technical Preferences

<!-- Populated by /setup-engine. Updated as the user makes decisions throughout development. -->
<!-- All agents reference this file for project-specific standards and conventions. -->

This file starts as a clean Codex template. Run `setup-engine` to pin the
engine-specific defaults, then keep it updated as technical decisions become
explicit.

## Engine & Language

- **Engine**: Not configured yet. Run `setup-engine` to choose the engine and version.
- **Language**: Set during engine setup.
- **Rendering**: Record the active render pipeline after engine setup.
- **Physics**: Record the active physics stack after engine setup.

## Naming Conventions

- **Classes**: Pin the project-wide type naming convention during engine setup.
- **Variables**: Follow the primary language convention chosen for the project.
- **Signals/Events**: Record the event naming format once the engine is pinned.
- **Files**: Match the engine and language file naming convention.
- **Scenes/Prefabs**: Record the scene or prefab naming rule after engine setup.
- **Constants**: Keep constants visually distinct from regular variables.

## Performance Budgets

- **Target Framerate**: 60 FPS baseline unless the project chooses a different target.
- **Frame Budget**: 16.6 ms at the current baseline.
- **Draw Calls**: Set once target hardware and content scale are pinned.
- **Memory Ceiling**: Set once target hardware and platform constraints are pinned.

## Testing

- **Framework**: Choose during engine setup based on the selected runtime.
- **Minimum Coverage**: Cover gameplay formulas, save/load, and core loop regressions before production.
- **Required Tests**: Balance formulas, gameplay systems, networking (if applicable)

## Forbidden Patterns

<!-- Add patterns that should never appear in this project's codebase -->
- [None configured yet — add as architectural decisions are made]

## Allowed Libraries / Addons

<!-- Add approved third-party dependencies here -->
- [None configured yet — add as dependencies are approved]

## Architecture Decisions Log

<!-- Quick reference linking to full ADRs in docs/architecture/ -->
- [No ADRs yet — use /architecture-decision to create one]
