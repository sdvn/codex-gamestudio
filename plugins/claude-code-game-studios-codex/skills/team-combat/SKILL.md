---
name: team-combat
description: Orchestrate the combat team: coordinates game-designer, gameplay-programmer, ai-programmer, technical-artist, sound-designer, and qa-tester to design, implement, and validate a combat feature end-to-end.
---

## Codex Compatibility

This is a Codex-native port of the upstream Claude Code Game Studios workflow.

- Ask the user directly in plain text when a decision or approval is needed.
- Work locally by default instead of assuming Claude-specific custom subagents exist.
- Use Codex `worker` or `explorer` agents only when the user explicitly asks for delegation or parallel work.
- Keep the studio conventions in `docs/CODEX-STUDIO.md`, `docs/studio/technical-preferences.md`, and the plugin references under `plugins/claude-code-game-studios-codex/references/` in mind while executing this workflow.

## Team Workflow In Codex

Treat the listed specialties as role briefs, not native Codex agent types.

- Default mode: synthesize the perspectives in one session and stop at each phase boundary for user approval.
- Delegated mode: only if the user explicitly requests delegation or parallel work. In that case, use generic Codex `worker` or `explorer` agents and give each one the matching brief from `plugins/claude-code-game-studios-codex/references/roles/<role>.md`.
- Keep write scopes disjoint when delegating implementation work.

When this skill is invoked, orchestrate the combat team through a structured pipeline.

**Decision Points:** At each phase transition, use a concise plain-text question to the user to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase.

## Team Composition
- **game-designer** — Design the mechanic, define formulas and edge cases
- **gameplay-programmer** — Implement the core gameplay code
- **ai-programmer** — Implement NPC/enemy AI behavior for the feature
- **technical-artist** — Create VFX, shader effects, and visual feedback
- **sound-designer** — Define audio events, impact sounds, and ambient combat audio
- **qa-tester** — Write test cases and validate the implementation

## How to Delegate

If the user explicitly asks for delegation, use Codex generic subagents with these role briefs:
- `role brief: game-designer` — Design the mechanic, define formulas and edge cases
- `role brief: gameplay-programmer` — Implement the core gameplay code
- `role brief: ai-programmer` — Implement NPC/enemy AI behavior
- `role brief: technical-artist` — Create VFX, shader effects, visual feedback
- `role brief: sound-designer` — Define audio events, impact sounds, ambient audio
- `role brief: qa-tester` — Write test cases and validate implementation

When delegating, provide full context in each agent's prompt (design doc path, relevant code files, constraints). Only launch parallel agents when the user explicitly asks for delegation; otherwise execute the phases locally (e.g., Phase 3 agents can run simultaneously).

## Pipeline

### Phase 1: Design
Delegate to **game-designer**:
- Create or update the design document in `design/gdd/` covering: mechanic overview, player fantasy, detailed rules, formulas with variable definitions, edge cases, dependencies, tuning knobs with safe ranges, and acceptance criteria
- Output: completed design document

### Phase 2: Architecture
Delegate to **gameplay-programmer** (with **ai-programmer** if AI is involved):
- Review the design document
- Design the code architecture: class structure, interfaces, data flow
- Identify integration points with existing systems
- Output: architecture sketch with file list and interface definitions

### Phase 3: Implementation (parallel where possible)
Delegate in parallel:
- **gameplay-programmer**: Implement core combat mechanic code
- **ai-programmer**: Implement AI behaviors (if the feature involves NPC reactions)
- **technical-artist**: Create VFX and shader effects
- **sound-designer**: Define audio event list and mixing notes

### Phase 4: Integration
- Wire together gameplay code, AI, VFX, and audio
- Ensure all tuning knobs are exposed and data-driven
- Verify the feature works with existing combat systems

### Phase 5: Validation
Delegate to **qa-tester**:
- Write test cases from the acceptance criteria
- Test all edge cases documented in the design
- Verify performance impact is within budget
- File bug reports for any issues found

### Phase 6: Sign-off
- Collect results from all team members
- Report feature status: COMPLETE / NEEDS WORK / BLOCKED
- List any outstanding issues and their assigned owners

## Output
A summary report covering: design completion status, implementation status per team member, test results, and any open issues.
