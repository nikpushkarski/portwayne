# gamedev_n_learn

Project-local teaching mode for game programming. Pi's portable skill-name format uses hyphens, so the registered name is `gamedev-n-learn`. The requested underscore spelling remains its display name and natural-language tuning name.

## Enable

Run `/reload` in Pi after installing these files. Check startup/reload diagnostics and command discovery. If prompted, review and grant the relevant project trust. No package, extension, API key, or installation command is required.

The root `AGENTS.md` instructs the assistant to load this skill for game-programming work. The skill description also supports automatic selection. This is instruction-based routing, not a hard runtime switch; model compliance is not guaranteed.

To invoke explicitly:

```text
/skill:gamedev-n-learn help me implement crate landing
```

It works across Pi-supported models, including GPT; no model training occurs.

## Simplest tuning API

Just send an ordinary message:

```text
tune gamedev_n_learn: no teasing, explain with diagrams sooner
```

The assistant edits `preferences.md` and applies the update. This is a natural-language convention, not a new registered Pi command.

Other examples:

```text
show gamedev_n_learn preferences
tune gamedev_n_learn: assume I know Python but am new to Godot
tune gamedev_n_learn: first responses may be up to 15 lines
tune gamedev_n_learn: direct mode until I change it back
reset gamedev_n_learn preferences
```

Alternatively, edit **`.agents/skills/gamedev-n-learn/preferences.md`** yourself, then run `/reload`. Advanced workflow changes belong in `SKILL.md`; routing changes belong in the root `AGENTS.md`.

For a one-off escape, say **“just show me the solution”** or **“implement it directly.”** That does not permanently disable teaching. “Implement stacking” alone still uses the guided project default.

## Default preferences / reset source

On an explicit reset, restore these values and remove additional tuning rules:

- **Mode:** guided; direct answers and implementation on explicit request.
- **Brevity:** first response normally 3–8 short lines; expand when clarity requires it.
- **Teasing:** light and occasional; joke about the bug or situation, never the learner.
- **First step:** one concrete hint and one small action or prediction.
- **Diagrams:** ASCII in chat at the first sign of struggle; add repository SVGs for complex or reusable explanations.
- **Rescue threshold:** after two unsuccessful guided attempts, offer a worked solution or a smaller step; offer sooner if frustrated.
- **Code assistance:** inspect freely; leave the central solution to the learner initially. Provide partial snippets or scaffolding as needed. Edit gameplay source when the learner accepts a scaffold or explicitly requests direct implementation.
- **Learning level:** infer cautiously from the current task; explain unfamiliar terms briefly; do not assume an absolute beginner or expert.
- **Verification:** help test each attempt and briefly explain the transferable principle.
- **Additional tuning rules:** None.

## Quick behavior checks

Try these after `/reload`, ideally as separate tasks:

| Request | Expected behavior |
|---|---|
| “Implement crate landing.” | Inspect relevant context, then give a useful hint and a small next step; no complete patch yet. |
| “I don't understand which edge matters.” | Explanation plus an ASCII diagram; narrower next action. |
| “Still stuck.” | Stronger scaffold; offer a worked solution when the rescue threshold is reached. |
| “Just write the full landing function.” | Give or implement the solution directly; no compulsory quiz. |
| “Tune gamedev_n_learn: no jokes.” | Edit only the relevant preference and acknowledge briefly. |
| “Generate a decorative warehouse poster.” | Do the artwork task normally; no mandatory programming lesson. |

File structure and routing can be checked statically; actual teaching behavior needs a live Pi conversation test. No such live reload or behavioral test is claimed by the installation itself.
