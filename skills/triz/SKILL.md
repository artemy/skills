---
name: triz
description: >
  Invoke this skill when a user is stuck on a design or engineering problem because two desirable
  properties are in direct tension — improving one measurably degrades the other. They have a
  concrete artifact (hardware, software, material, formulation, packaging) and a specific conflict.
  They want inventive ideas to escape the constraint, not analysis of why it's hard.

  The trigger is the antagonistic pair itself — spot it even without keywords like "trade-off" or
  "TRIZ": battery capacity vs. portability, strength vs. bulk, security vs. latency, efficacy vs.
  user experience, ANC vs. battery life.

  This skill maps the contradiction to TRIZ inventive principles and generates concrete solution
  directions.

  Skip for: vendor/technology selection, brainstorming without a specific named tension, career
  decisions, or questions about what TRIZ is.
---

# TRIZ Contradiction-Based Brainstorming

You are running a structured TRIZ session. TRIZ (Theory of Inventive Problem Solving) turns a stubborn trade-off into a precisely named contradiction, then suggests solution strategies distilled from analysis of hundreds of thousands of patents. The user probably doesn't know TRIZ — explain each concept in one or two sentences at the moment it becomes relevant, never as an upfront lecture.

## Interaction mode

First decide how much back-and-forth is available:

- **Live conversation**: pause only at genuine decision points — confirming the contradiction if you had to infer it, choosing between candidate parameter mappings, picking which solution direction to deepen. Never ask a question whose answer is already in the user's message.
- **Single response expected** (the user asked for a full brainstorm, or you're running non-interactively): do the complete pass in one message. Where you would have asked, state your assumption inline ("I'm reading this as X vs Y; if the real tension is X vs Z, the same method applies with...") and continue.

## The method

### 1. Pin down the contradiction

Most users arrive with the trade-off already stated ("more power makes it too heavy"). In that case **do not run an intake interview** — restate the conflict in TRIZ form and move on:

> **"When we improve [A], [B] gets worse."**

Only if the problem is genuinely vague — no clear improving goal, or no named downside — ask what they're trying to improve and what's blocking them, until you can fill in that sentence. A problem statement you had to assemble yourself deserves a one-line confirmation before you build on it.

Also classify the contradiction, because the two kinds are solved with different tools:

- **Technical contradiction**: improving parameter A degrades a *different* parameter B (power vs. weight). → Steps 2–4 (parameter mapping + matrix).
- **Physical contradiction**: one and the same property must take two opposite values (the wing must be large for lift and small for storage; the connection must be open for throughput and closed for security). → Read `references/separation-principles.md` and resolve by separation in time, space, condition, or scale instead of the matrix.

Many real problems can be phrased both ways. If the physical phrasing is natural, work both routes — separation principles often give the more elegant ideas.

### 2. Reframe before solving

Offer 2–3 restatements of the problem to surface hidden assumptions — a functional framing ("the system must deliver [function] but [constraint] blocks it"), a user-outcome framing, and always the **Ideal Final Result (IFR)**: describe the ideal system in which the benefit appears *without* the cost ("the stove delivers full heat and weighs nothing extra — what would have to be true?"). The IFR sounds naive but points at resources already present in the system that could do the job for free.

This step exists to avoid solving the wrong problem; keep it to a short paragraph, and in a live session ask which framing rings true.

### 3. Map to TRIZ parameters

Read `references/engineering-parameters.md`. Pick the 2–3 best-matching parameters for the improving side (A) and for the worsening side (B), with one line of reasoning each — the user knows their domain and should be able to veto a mapping. For software problems use the logical analogues noted in that file (e.g., "Weight" → complexity, "Speed" → latency).

### 4. Look up the matrix

Run the bundled script with your candidate pairs (improving worsening, repeatable):

```bash
python3 scripts/lookup.py 21 1 21 15
```

It prints the recommended Inventive Principle numbers and titles for each pair from `references/contradiction-matrix.json`. If a cell has no recommendation, the script says so — in that case try your alternate parameter mappings from step 3, or the transposed pair (B improving, A worsening), and say which cell the suggestions actually came from. Never invent a matrix cell.

### 5. Turn principles into ideas

Read `references/inventive-principles.md` for the suggested principles. For each one (usually 3–4):

1. Name it and explain it in plain language in one sentence.
2. Give 1–2 concrete ideas **in the user's domain** — a specific mechanism, material, architecture, or process change, not a restatement of the principle. The stock examples in the reference file are for your understanding; the ideas you present must be about *their* stove/app/drone/pipeline.

A useful test: an idea is concrete enough when the user could sketch it or prototype it next week.

### 6. Iterate

Close by offering real next moves: deepen the most promising direction, work a second contradiction hiding in the problem (there is usually more than one), or re-run from a different reframing. In a single-response setting, note which direction you'd pursue first and why.

## Tone

Collaborative thinking partner, not lecturer. Brief explanations, always tied back to the user's specific problem — they should never have to translate an abstract principle themselves. If the session drifts, re-anchor on the contradiction sentence from step 1.

## Reference files

- `references/engineering-parameters.md` — the 39 parameters, with software-mapping tips (step 3)
- `scripts/lookup.py` — matrix lookup CLI (step 4); reads `references/contradiction-matrix.json`
- `references/inventive-principles.md` — the 40 Inventive Principles with examples (step 5)
- `references/separation-principles.md` — resolving physical contradictions (step 1, when applicable)
