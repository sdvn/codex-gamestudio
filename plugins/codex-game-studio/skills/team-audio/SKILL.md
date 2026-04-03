---
name: team-audio
description: Orchestrate audio team: audio-director + sound-designer + technical-artist + gameplay-programmer for full audio pipeline from direction to implementation.
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

When this skill is invoked, orchestrate the audio team through a structured pipeline.

**Decision Points:** At each step transition, use a concise plain-text question to the user to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next step.

1. **Read the argument** for the target feature or area (e.g., `combat`,
   `main menu`, `forest biome`, `boss encounter`).

2. **Gather context**:
   - Read relevant design docs in `design/gdd/` for the feature
   - Read the sound bible at `design/gdd/sound-bible.md` if it exists
   - Read existing audio asset lists in `assets/audio/`
   - Read any existing sound design docs for this area

## How to Delegate

If the user explicitly asks for delegation, use Codex generic subagents with these role briefs:
- `role brief: audio-director` — Sonic identity, emotional tone, audio palette
- `role brief: sound-designer` — SFX specifications, audio events, mixing groups
- `role brief: technical-artist` — Audio middleware, bus structure, memory budgets
- `role brief: gameplay-programmer` — Audio manager, gameplay triggers, adaptive music

When delegating, provide full context in each agent's prompt (feature description, existing audio assets, design doc references).

3. **Orchestrate the audio team** in sequence:

### Step 1: Audio Direction (audio-director)
Spawn the `audio-director` agent to:
- Define the sonic identity for this feature/area
- Specify the emotional tone and audio palette
- Set music direction (adaptive layers, stems, transitions)
- Define audio priorities and mix targets
- Establish any adaptive audio rules (combat intensity, exploration, tension)

### Step 2: Sound Design (sound-designer)
Spawn the `sound-designer` agent to:
- Create detailed SFX specifications for every audio event
- Define sound categories (ambient, UI, gameplay, music, dialogue)
- Specify per-sound parameters (volume range, pitch variation, attenuation)
- Plan audio event list with trigger conditions
- Define mixing groups and ducking rules

### Step 3: Technical Implementation (technical-artist)
Spawn the `technical-artist` agent to:
- Design the audio middleware integration (Wwise/FMOD/native)
- Define audio bus structure and routing
- Specify memory budgets for audio assets per platform
- Plan streaming vs preloaded asset strategy
- Design any audio-reactive visual effects

### Step 4: Code Integration (gameplay-programmer)
Spawn the `gameplay-programmer` agent to:
- Implement audio manager system or review existing
- Wire up audio events to gameplay triggers
- Implement adaptive music system (if specified)
- Set up audio occlusion/reverb zones
- Write unit tests for audio event triggers

4. **Compile the audio design document** combining all team outputs.

5. **Save to** `design/gdd/audio-[feature].md`.

6. **Output a summary** with: audio event count, estimated asset count,
   implementation tasks, and any open questions between team members.
