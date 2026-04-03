---
name: team-level
description: Orchestrate level design team: level-designer + narrative-director + world-builder + art-director + systems-designer + qa-tester for complete area/level creation.
---

## Codex Compatibility

This is a Codex-native game production workflow.

- Ask the user directly in plain text when a decision or approval is needed.
- Work locally by default instead of assuming custom subagents exist.
- Use Codex `worker` or `explorer` agents only when the user explicitly asks for delegation or parallel work.
- Keep the studio conventions in `docs/CODEX-STUDIO.md`, `docs/studio/technical-preferences.md`, and the plugin references under `plugins/codex-game-studio/references/` in mind while executing this workflow.

## Team Workflow In Codex

Treat the listed specialties as role briefs, not native Codex agent types.

- Default mode: synthesize the perspectives in one session and stop at each phase boundary for user approval.
- Delegated mode: only if the user explicitly requests delegation or parallel work. In that case, use generic Codex `worker` or `explorer` agents and give each one the matching brief from `plugins/codex-game-studio/references/roles/<role>.md`.
- Keep write scopes disjoint when delegating implementation work.

When this skill is invoked:

**Decision Points:** At each step transition, use a concise plain-text question to the user to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next step.

1. **Read the argument** for the target level or area (e.g., `tutorial`,
   `forest dungeon`, `hub town`, `final boss arena`).

2. **Gather context**:
   - Read the game concept at `design/gdd/game-concept.md`
   - Read game pillars at `design/gdd/game-pillars.md`
   - Read existing level docs in `design/levels/`
   - Read relevant narrative docs in `design/narrative/`
   - Read world-building docs for the area's region/faction

## How to Delegate

If the user explicitly asks for delegation, use Codex generic subagents with these role briefs:
- `role brief: narrative-director` — Narrative purpose, characters, emotional arc
- `role brief: world-builder` — Lore context, environmental storytelling, world rules
- `role brief: level-designer` — Spatial layout, pacing, encounters, navigation
- `role brief: systems-designer` — Enemy compositions, loot tables, difficulty balance
- `role brief: art-director` — Visual theme, color palette, lighting, asset requirements
- `role brief: qa-tester` — Test cases, boundary testing, playtest checklist

When delegating, provide full context in each agent's prompt (game concept, pillars, existing level docs, narrative docs).

3. **Orchestrate the level design team** in sequence:

### Step 1: Narrative Context (narrative-director + world-builder)
Spawn the `narrative-director` agent to:
- Define the narrative purpose of this area (what story beats happen here?)
- Identify key characters, dialogue triggers, and lore elements
- Specify emotional arc (how should the player feel entering, during, leaving?)

Spawn the `world-builder` agent to:
- Provide lore context for the area (history, faction presence, ecology)
- Define environmental storytelling opportunities
- Specify any world rules that affect gameplay in this area

### Step 2: Layout and Encounter Design (level-designer)
Spawn the `level-designer` agent to:
- Design the spatial layout (critical path, optional paths, secrets)
- Define pacing curve (tension peaks, rest areas, exploration zones)
- Place encounters with difficulty progression
- Design environmental puzzles or navigation challenges
- Define points of interest and landmarks for wayfinding
- Specify entry/exit points and connections to adjacent areas

### Step 3: Systems Integration (systems-designer)
Spawn the `systems-designer` agent to:
- Specify enemy compositions and encounter formulas
- Define loot tables and reward placement
- Balance difficulty relative to expected player level/gear
- Design any area-specific mechanics or environmental hazards
- Specify resource distribution (health pickups, save points, shops)

### Step 4: Visual Direction (art-director)
Spawn the `art-director` agent to:
- Define the visual theme and color palette for the area
- Specify lighting mood and time-of-day settings
- List required art assets (environment props, unique assets)
- Define visual landmarks and sight lines
- Specify any special VFX needs (weather, particles, fog)

### Step 5: QA Planning (qa-tester)
Spawn the `qa-tester` agent to:
- Write test cases for the critical path
- Identify boundary and edge cases (sequence breaks, softlocks)
- Create a playtest checklist for the area
- Define acceptance criteria for level completion

4. **Compile the level design document** combining all team outputs into the
   level design template format.

5. **Save to** `design/levels/[level-name].md`.

6. **Output a summary** with: area overview, encounter count, estimated asset
   list, narrative beats, and any cross-team dependencies or open questions.
