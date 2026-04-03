---
name: team-release
description: Orchestrate the release team: coordinates release-manager, qa-lead, devops-engineer, and producer to execute a release from candidate to deployment.
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

When this skill is invoked, orchestrate the release team through a structured pipeline.

**Decision Points:** At each phase transition, use a concise plain-text question to the user to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase.

## Team Composition
- **release-manager** — Release branch, versioning, changelog, deployment
- **qa-lead** — Test sign-off, regression suite, release quality gate
- **devops-engineer** — Build pipeline, artifacts, deployment automation
- **producer** — Go/no-go decision, stakeholder communication, scheduling

## How to Delegate

If the user explicitly asks for delegation, use Codex generic subagents with these role briefs:
- `role brief: release-manager` — Release branch, versioning, changelog, deployment
- `role brief: qa-lead` — Test sign-off, regression suite, release quality gate
- `role brief: devops-engineer` — Build pipeline, artifacts, deployment automation
- `role brief: producer` — Go/no-go decision, stakeholder communication

When delegating, provide full context in each agent's prompt (version number, milestone status, known issues). Only launch parallel agents when the user explicitly asks for delegation; otherwise execute the phases locally (e.g., Phase 3 agents can run simultaneously).

## Pipeline

### Phase 1: Release Planning
Delegate to **producer**:
- Confirm all milestone acceptance criteria are met
- Identify any scope items deferred from this release
- Set the target release date and communicate to team
- Output: release authorization with scope confirmation

### Phase 2: Release Candidate
Delegate to **release-manager**:
- Cut release branch from the agreed commit
- Bump version numbers in all relevant files
- Generate the release checklist using `/release-checklist`
- Freeze the branch — no feature changes, bug fixes only
- Output: release branch name and checklist

### Phase 3: Quality Gate (parallel)
Delegate in parallel:
- **qa-lead**: Execute full regression test suite. Test all critical paths. Verify no S1/S2 bugs. Sign off on quality.
- **devops-engineer**: Build release artifacts for all target platforms. Verify builds are clean and reproducible. Run automated tests in CI.

### Phase 4: Localization and Performance
Delegate (can run in parallel with Phase 3 if resources available):
- Verify all strings are translated (delegate to localization-lead if available)
- Run performance benchmarks against targets (delegate to performance-analyst if available)
- Output: localization and performance sign-off

### Phase 5: Go/No-Go
Delegate to **producer**:
- Collect sign-off from: qa-lead, release-manager, devops-engineer, technical-director
- Evaluate any open issues — are they blocking or can they ship?
- Make the go/no-go call
- Output: release decision with rationale

### Phase 6: Deployment (if GO)
Delegate to **release-manager** + **devops-engineer**:
- Tag the release in version control
- Generate changelog using `/changelog`
- Deploy to staging for final smoke test
- Deploy to production
- Monitor for 48 hours post-release

### Phase 7: Post-Release
- **release-manager**: Generate release report (what shipped, what was deferred, metrics)
- **producer**: Update milestone tracking, communicate to stakeholders
- **qa-lead**: Monitor incoming bug reports for regressions
- Schedule post-release retrospective if issues occurred

## Output
A summary report covering: release version, scope, quality gate results, go/no-go decision, deployment status, and monitoring plan.
