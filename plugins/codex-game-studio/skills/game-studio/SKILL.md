---
name: game-studio
description: Route requests to the right game-studio workflow in this toolkit. Use when the user needs one entrypoint for planning, setup, implementation teams, reviews, or continuing an existing game project.
---

## Codex Compatibility

This is a Codex-native game production workflow.

- Ask the user directly in plain text when a decision or approval is needed.
- Work locally by default instead of assuming custom subagents exist.
- Use Codex `worker` or `explorer` agents only when the user explicitly asks for delegation or parallel work.
- Keep the studio conventions in `docs/CODEX-STUDIO.md`, `docs/studio/technical-preferences.md`, and the plugin references under `plugins/codex-game-studio/references/` in mind while executing this workflow.

# Game Studio

## Overview

Use this skill as the umbrella entrypoint for Codex Game Studio.

Start here when the user says things like:

- "help me build this game"
- "what should I do next in this repo?"
- "set this project up properly"
- "I need the right workflow, but I do not know which one"

Do not stay here longer than needed. Classify the request, recommend the exact next workflow, explain why, and then continue through that route.

## Routing Rules

1. Read enough project context to avoid blind routing:
   - check whether an engine is configured in `docs/studio/technical-preferences.md`
   - check whether concept and GDD files exist in `design/gdd/`
   - check whether code exists in `src/`
   - check whether production artifacts exist in `production/`
2. Classify the request into one primary lane:
   - `new idea`: use `start` or `brainstorm`
   - `existing project triage`: use `project-stage-detect`, then `gate-check` if phase readiness matters
   - `engine choice or setup`: use `setup-engine`
   - `system planning`: use `map-systems` or `design-system`
   - `feature implementation`: use the relevant `team-*` workflow
   - `review or analysis`: use `code-review`, `design-review`, `perf-profile`, `balance-check`, `asset-audit`, `scope-check`, or `tech-debt`
   - `release or emergency work`: use `team-release`, `release-checklist`, `launch-checklist`, `patch-notes`, or `hotfix`
3. Prefer one clear next workflow over a long menu unless the user explicitly asks for options.

## Team Workflow Routing

Route implementation-heavy requests to the most specific team workflow:

- combat, abilities, enemies, encounter logic: `team-combat`
- narrative, dialogue, lore, story integration: `team-narrative`
- HUD, menus, UX, front-end game screens: `team-ui`
- levels, areas, encounters, world spaces: `team-level`
- sound direction and implementation: `team-audio`
- optimization, feel, final quality pass: `team-polish`
- release readiness and cross-discipline shipping: `team-release`

If no `team-*` workflow fits, route to the single-discipline skill that best matches the work.

## Default Interaction Pattern

1. Summarize the current project state in 2-4 concrete bullets.
2. State the primary workflow you recommend next.
3. Mention one or two alternative workflows only when they are genuinely plausible.
4. Ask the user whether to continue with the recommended route.

## Output Expectations

- Return a short routing decision, not a giant taxonomy.
- Name the exact next skill or workflow.
- Keep the studio structure coherent across design, implementation, QA, and release.
- If the user already named a specific workflow, honor it instead of re-routing unnecessarily.

## Examples

- "Help me start this game project from scratch."
- "Figure out what this repo needs next."
- "Route me to the right workflow for a combat feature."
- "I need the proper game-studio path for release prep."
