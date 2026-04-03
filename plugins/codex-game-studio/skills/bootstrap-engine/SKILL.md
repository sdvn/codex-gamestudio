---
name: bootstrap-engine
description: Create a real engine-ready project skeleton after setup-engine. Use when the repo has an engine chosen but still needs initial Godot, Unity, or Unreal project files, directories, starter runtime code, and test scaffolding.
---

## Codex Compatibility

This is a Codex-native game production workflow.

- Ask the user directly in plain text when a decision or approval is needed.
- Work locally by default instead of assuming custom subagents exist.
- Use Codex `worker` or `explorer` agents only when the user explicitly asks for delegation or parallel work.
- Keep the studio conventions in `docs/CODEX-STUDIO.md`, `docs/studio/technical-preferences.md`, and the plugin references under `plugins/codex-game-studio/references/` in mind while executing this workflow.

# Bootstrap Engine

Use this workflow after `setup-engine` when the project needs actual runtime
files, not just pinned docs.

## What It Creates

`bootstrap-engine` writes a deterministic starter scaffold through:

`python3 scripts/bootstrap_engine_project.py`

Supported targets:

- **Godot**: `project.godot`, starter scene, GDScript bootstrap files, test notes
- **Unity**: `Assets/`, `Packages/`, `ProjectSettings/`, starter runtime script, test stub
- **Unreal**: `.uproject`, `Config/`, `Source/`, starter C++ module, game mode stub

It also creates shared repo structure for design, architecture, production,
tests, tools, and prototypes so the rest of the studio workflows have a real
place to write into.

## Workflow

1. Read `docs/CODEX-STUDIO.md` and `docs/studio/technical-preferences.md`.
2. Infer the engine from those files unless the user explicitly passed one.
3. Check whether engine markers already exist:
   - `project.godot`
   - `Packages/manifest.json`
   - `*.uproject`
4. If the engine is not pinned yet, stop and route the user to `setup-engine`.
5. If engine markers already exist, summarize what is present and ask whether
   the user wants to patch the existing scaffold or leave it alone.
6. Gather or confirm:
   - project display name
   - 2D or 3D mode for Godot/Unity
   - whether overwrite is allowed if generated files already exist
7. Preview the intended write set first with:

```bash
python3 scripts/bootstrap_engine_project.py \
  --engine <godot|unity|unreal> \
  --project-name "<Project Name>" \
  --engine-version "<Pinned Version>" \
  --mode <2d|3d> \
  --dry-run
```

8. Show the user the planned files in a concise summary and ask for approval.
9. After approval, run the real command:

```bash
python3 scripts/bootstrap_engine_project.py \
  --engine <godot|unity|unreal> \
  --project-name "<Project Name>" \
  --engine-version "<Pinned Version>" \
  --mode <2d|3d>
```

Add `--force` only if the user explicitly approved overwriting generated files.

## Output Expectations

After writing the scaffold:

- summarize the engine-specific root files created
- call out any engine-specific follow-up the user must do in-editor
- recommend the next exact workflow

Typical next steps:

1. `architecture-decision`
2. `map-systems`
3. `prototype` for the core loop
4. a `team-*` workflow for the first real slice

## Guardrails

- Never bootstrap an engine before `setup-engine` pins the stack.
- Never overwrite existing engine entry files without explicit approval.
- For Unreal, prefer a C++-capable scaffold even if the project expects heavy Blueprint work later.
- For Unity, treat the generated runtime script and tests as starter files; the first scene still needs to be created or wired inside the editor.
- For Godot, keep scenes and scripts under `src/` so the repo-level structure remains aligned with the studio docs.
