<p align="center">
  <h1 align="center">Codex Game Studio</h1>
  <p align="center">
    Turn one Codex session into a structured game development studio.
    <br />
    38 workflows. 48 role briefs. One Codex-first production kit.
  </p>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="plugins/codex-game-studio/skills"><img src="https://img.shields.io/badge/workflows-38-1f7a1f" alt="38 workflows"></a>
  <a href="plugins/codex-game-studio/references/roles"><img src="https://img.shields.io/badge/roles-48-0f766e" alt="48 roles"></a>
  <a href="plugins/codex-game-studio/references/templates"><img src="https://img.shields.io/badge/templates-26-9a3412" alt="26 templates"></a>
  <a href="docs/engine-reference"><img src="https://img.shields.io/badge/engine%20refs-46-334155" alt="46 engine references"></a>
  <a href="plugins/codex-game-studio/.codex-plugin/plugin.json"><img src="https://img.shields.io/badge/runtime-Codex-111827" alt="Codex runtime"></a>
</p>

> This repository is a Codex-native port of the original
> [`Donchitos/Claude-Code-Game-Studios`](https://github.com/Donchitos/Claude-Code-Game-Studios),
> cleaned and reorganized to feel native in Codex.

## Why This Exists

Game projects benefit from structure, but a plain chat session rarely gives you
clear lanes for design, implementation, review, production planning, and
release work. This repo turns that loose interaction into a more disciplined
studio model for Codex.

You still make the decisions. The repo gives Codex a stronger operating shape:
named workflows, reusable role briefs, document templates, and engine-specific
reference notes.

## What's Included

| Category | Count | Description |
|----------|-------|-------------|
| **Workflows** | 38 | Codex skill entrypoints for planning, reviews, production, implementation, and release |
| **Role Briefs** | 48 | Domain-specific specialist briefs for design, programming, art, QA, production, and engine work |
| **Templates** | 26 | Reusable docs for GDDs, ADRs, milestones, retrospectives, release work, and reverse-documentation |
| **Engine References** | 46 | Version-aware notes for Godot, Unity, and Unreal |

## Studio Shape

The role library keeps the same three-level studio structure:

| Tier | Focus | Examples |
|------|-------|----------|
| **Leadership** | Direction and conflict resolution | `creative-director`, `technical-director`, `producer` |
| **Department Leads** | Domain ownership | `game-designer`, `lead-programmer`, `art-director`, `qa-lead` |
| **Specialists** | Hands-on execution | `gameplay-programmer`, `ui-programmer`, `writer`, `technical-artist`, `qa-tester` |

These roles live in `plugins/codex-game-studio/references/roles/` and are used
as Codex role briefs rather than product-native subagent types.

## Main Workflows

**Project setup**

`game-studio` `start` `setup-engine` `project-stage-detect`

**Design and planning**

`brainstorm` `map-systems` `design-system` `design-review` `architecture-decision` `estimate`

**Implementation teams**

`team-combat` `team-ui` `team-level` `team-narrative` `team-audio` `team-polish` `team-release`

**Reviews and operations**

`code-review` `perf-profile` `balance-check` `asset-audit` `scope-check` `tech-debt` `release-checklist` `launch-checklist` `hotfix`

## Repository Layout

```text
.
├── .agents/plugins/marketplace.json
├── docs/
│   ├── CODEX-STUDIO.md
│   ├── studio/technical-preferences.md
│   └── engine-reference/
├── plugins/
│   └── codex-game-studio/
│       ├── .codex-plugin/plugin.json
│       ├── skills/
│       ├── references/roles/
│       ├── references/templates/
│       └── references/studio/
└── production/session-state/
```

## How To Use

1. Open the repo in Codex.
2. Let Codex use the local plugin from `plugins/codex-game-studio/`.
3. Start with `game-studio` if you want routing, or jump directly into a named workflow.
4. Keep project-level choices in `docs/CODEX-STUDIO.md`.
5. Keep engine-specific decisions in `docs/studio/technical-preferences.md` and `docs/engine-reference/`.

## Core Files

- `plugins/codex-game-studio/.codex-plugin/plugin.json`
- `.agents/plugins/marketplace.json`
- `docs/CODEX-STUDIO.md`
- `docs/studio/technical-preferences.md`
- `plugins/codex-game-studio/references/roles/`
- `plugins/codex-game-studio/references/templates/`
