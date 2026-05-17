# Style

How specialists write. Read by every agent that produces written output (especially Spec Writer, Rule Lister, and any later docs-shaped agent).

## What's in here

- **`voice-profile.md`** — Generic voice profile template. Fill in for your own voice before porting. See `voice-profile-laksh.md` for a worked example.
- **`anti-ai-pm-writing.md`** — Field guide on patterns that signal AI-generated text. Final-pass filter for every specialist's output.
- **`voice-profile-laksh.md`** — Original worked example (reference only; don't use directly when porting to a new org).
- **`anti-ai-pm-writing-style.md`** — Original version (reference only; superseded by `anti-ai-pm-writing.md`).

## How specialists use these

Each specialist's contract names voice profile + anti-AI style as required reading. The output must pass two tests before sign-off:

1. **Voice match.** Does it sound like Laksh writing it? Direct, peer-level, outcome-first, trade-offs explicit.
2. **No AI tells.** No "delve into", "robust", "leverage", "underscore", "in conclusion". No three-adjective lists. No comprehensive emptiness. No challenges-and-future-outlook closers.

If output fails either test, push it back to the specialist with a specific note. Don't accept and edit — that defeats the point of the agent producing usable drafts.

## Why these live in the framework folder

The framework is meant to be portable. Voice and writing standards are part of what makes the output work — without them, every specialist drifts toward generic AI prose. Duplicating them here keeps the framework self-contained.

The originals in `/Laksh-MD Files/` are archived. These are the live versions.
