CLAUDE.md — Universal
Global directives for every session, every machine, every project. Machine- and project-specific rules live in specifics.md.

Git
Never add Claude as a co-author, contributor, or collaborator. No Co-Authored-By: Claude ..., no 🤖 Generated with Claude Code, no self-attribution of any kind — in commit messages, PR/MR descriptions, or anywhere else. Every repo, every branch, every session. No exceptions.
Never commit to main directly. Pull main, then create a new branch. Follow the repo's existing branch-naming convention (look at recent branches and match them).
Never push without an explicit instruction. Commit when asked; push only when told to push. "Hold off on pushing" / "I'll push myself" means do not push, including at end of session. Never open the PR/MR yourself unless asked.
Commit messages: minimal and descriptive. No AI preamble, no bullet lists. Prefer conventional commits — type(scope): short message (feat:, fix:, misc:). When a verbatim message is dictated, use it exactly as given.
How to work
Make the smallest diff that solves the problem. Don't touch files you weren't asked to touch. Don't refactor surrounding code, don't add dependencies, boilerplate, or abstractions when a minimal change works. If a change breaks existing behavior, revert the offending parts while keeping the new functionality.
Plan before non-trivial work. For anything substantial, briefly explore/audit first and present a short plan (and why it'll work) before writing code. Skip the plan for one-liners and obvious fixes.
Then execute autonomously. Once the approach is clear, act. Don't ask permission step-by-step and don't ask clarifying questions for things you can reasonably infer. Treat "do it", "fix it", "handle it", "do whatever's best" as full authorization to run commands and make the calls yourself. Report what you did afterward.
Verify before claiming done. Don't announce a fix as working until you've actually checked the live result — re-screenshot, re-run, re-measure. This is critical for visual / desktop / system changes where "it should work" is not evidence. If you can't verify, say so rather than implying success.
Run things yourself. "Spin up" / "launch" / "run the project" means find how (package.json, Makefile, README, docker-compose, etc.) and do it — don't ask for the command.
Strip your own scaffolding when done. Remove explanatory/tutorial comments you added while working. Don't leave tutorial-style commentary in the code.
Re-read before re-answering. If the user asks the same thing two or three times, you missed something — actually open and read the file/thing before responding, don't repeat a guess.
Preserve other people's code when porting. When importing or porting code authored by someone else, keep it exactly as written — including their comments — unless explicitly asked to change it. Confirm what was changed vs. preserved.
Check current docs, don't rely on memory for library/framework/API questions (Context7 when available).
Output style
Be terse. Skip preamble and trailing summaries; report concisely on what you did.
Spoken/presentation content → one dense, ready-to-read block the user can read aloud, not a bulleted outline. Written deliverables → concise.
Context
Put a short profile of the user here so the agent doesn't have to re-learn it each session — role, stack, and any working preferences. Keep it factual and minimal. For example:

The user is a developer who works across web and systems projects.
Works bilingually (e.g. French + English), sometimes mixed mid-message. Reply in the language of the most recent message; default to French.

## Agent skills

### Issue tracker

Issues are tracked as local markdown files under `.scratch/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five canonical triage labels, label string equal to role name. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context — one root `CONTEXT.md` + `docs/adr/`. See `docs/agents/domain.md`.
