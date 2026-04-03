# Codex Port Notes

This repo started from the upstream Claude Code Game Studios template, then was
trimmed into a Codex-focused layout.

## Current Model

- Codex skills live in
  `plugins/claude-code-game-studios-codex/skills/`
- Role briefs live in
  `plugins/claude-code-game-studios-codex/references/roles/`
- Templates live in
  `plugins/claude-code-game-studios-codex/references/templates/`
- Studio docs that skills may consult live in
  `plugins/claude-code-game-studios-codex/references/studio/`
- Project-level working config lives in `docs/CODEX-STUDIO.md`
- Project-level technical preferences live in
  `docs/studio/technical-preferences.md`

## Important Compatibility Choices

- Claude `AskUserQuestion` behavior is handled as normal Codex conversation.
- Claude custom subagent types are treated as role briefs only.
- Codex delegation is optional and should only happen when the user explicitly
  asks for delegated or parallel work.
- Engine reference docs remain project data in `docs/engine-reference/`.

## Why The Repo Is Smaller

The following were intentionally removed once the Codex port was stable:

- the repo-level `.claude/` runtime tree
- the upstream vendor clone
- Claude-specific hooks, settings, and workspace files
- duplicate skill definitions that only existed for Claude

The goal is to keep only the files that Codex needs at runtime or that the
project workflows actively read and write.
