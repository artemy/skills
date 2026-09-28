---
name: triz
description: >
  Generates inventive solution ideas for design/engineering problems where improving one
  property degrades another, using TRIZ contradiction analysis, the Altshuller matrix, and
  separation principles. Use when the user has a concrete artifact (hardware, software,
  material, formulation, packaging) and a trade-off they want to escape, not just analyze —
  even without the words "trade-off" or "TRIZ": battery capacity vs. portability, strength
  vs. bulk, security vs. latency, efficacy vs. UX. Also use when they describe a stubborn
  limitation ("every fix for X breaks Y", "we've hit a wall") without naming the opposing
  property yet. Skip for vendor/technology selection, open-ended ideation with no concrete
  artifact, career decisions, or questions about what TRIZ is.
---

# TRIZ Contradiction-Based Brainstorming

TRIZ turns a stubborn trade-off into a named contradiction, then maps it to proven solution strategies. Assume the user doesn't know TRIZ: explain each concept in a sentence or two when it comes up, not upfront. Act as a collaborative thinking partner, not a lecturer.

## Interaction mode

First decide how much back-and-forth is available:

- **Live conversation**: pause only at genuine decision points — confirming a contradiction you had to infer, choosing between candidate parameter mappings, picking which solution direction to deepen.
- **Single response expected** (the user asked for a full brainstorm, or you're running non-interactively): do the complete pass in one message. Where you would have asked, state your assumption inline ("I'm reading this as X vs Y; if the real tension is X vs Z, the same method applies with...") and continue.

## The method

### Step 1. Pin down the contradiction

Most users arrive with the trade-off already stated ("more power makes it too heavy"). In that case **do not run an intake interview** or ask anything their message already answers — restate the conflict in TRIZ form and move on:

> **"When we improve [A], [B] gets worse."**

Only if the problem is genuinely vague — no clear improving goal, or no named downside — ask what they're trying to improve and what's blocking them, until you can fill in that sentence. A problem statement you had to assemble yourself deserves a one-line confirmation before you build on it.

Then classify the contradiction, because the two kinds are solved with different tools:

- **Technical contradiction**: improving parameter A degrades a *different* parameter B (power vs. weight). Solve with parameter mapping and the matrix (Steps 3–4).
- **Physical contradiction**: one and the same property must take two opposite values (the wing must be large for lift and small for storage; the connection must be open for throughput and closed for security). Read `references/separation-principles.md` and resolve by separation in time, space, condition, or scale instead of the matrix.

Route through the method accordingly:

- Technical: Step 1 → 2 → 3 → 4 → 5 → 6
- Physical: Step 1 → 2 → separation principles → 5 → 6

Many real problems can be phrased both ways. If the physical phrasing is natural, work both routes — separation principles often give the more elegant ideas.

### Step 2. Reframe before solving

Offer 2–3 restatements of the problem to surface hidden assumptions — a functional framing ("the system must deliver [function] but [constraint] blocks it"), a user-outcome framing, and always the **Ideal Final Result (IFR)**: describe the ideal system in which the benefit appears *without* the cost ("the stove delivers full heat and weighs nothing extra — what would have to be true?"). The IFR sounds naive but points at resources already present in the system that could do the job for free.

This step exists to avoid solving the wrong problem. In a live session, ask which framing rings true.

### Step 3. Map to TRIZ parameters

Read `references/engineering-parameters.md`. Pick the 2–3 best-matching parameters for the improving side (A) and for the worsening side (B), with one line of reasoning each — the user knows their domain and should be able to veto a mapping. For software problems use the software mapping table in that file (e.g., latency → 9 Speed, code complexity → 36 Device complexity, security threats → 30 Object-affected harmful factors).

### Step 4. Look up the matrix

Run the bundled script with one or more `IMPROVING WORSENING` pairs. Your working directory is usually the user's project, not this skill, so call the script by its full path under the skill's base directory:

```bash
# Power vs Weight of moving object, Power vs Duration of action
python3 <skill-base-dir>/scripts/lookup.py 21 1 21 15
```

It prints the recommended Inventive Principles for each pair from `references/contradiction-matrix.json`. If a cell has no recommendation, the script says so — try your alternate parameter mappings from Step 3, or the transposed pair (B improving, A worsening), and say which cell the suggestions actually came from. Never invent a matrix cell.

### Step 5. Turn principles into ideas

Read `references/inventive-principles.md` for the suggested principles. Several matrix cells often recommend overlapping principles — merge them and pick the 3–4 most promising for this problem rather than covering every one; a long list of thin ideas is harder to act on than a few developed ones. For each chosen principle:

1. Name it and explain it in plain language in one sentence.
2. Give 1–2 concrete ideas **in the user's domain** — a specific mechanism, material, architecture, or process change, not a restatement of the principle. The stock examples in the reference file are for your understanding; the ideas you present must be about *their* stove/app/drone/pipeline, so they never have to translate an abstract principle themselves.

A useful test: an idea is concrete enough when the user could sketch it or prototype it next week.

### Step 6. Iterate

Close by offering real next moves: deepen the most promising direction, work a second contradiction hiding in the problem (there is usually more than one), or re-run from a different reframing. In a single-response setting, note which direction you'd pursue first and why. If the session drifts, re-anchor on the contradiction sentence from Step 1.

## Output shape

Spend most of the response on the solution ideas — that's what the user came for. Keep the method steps to a few lines each:

- Contradiction + reframes: one short paragraph
- Parameter mapping + matrix cells: a compact list
- Ideas: the bulk of the response (Step 5)
- Recommendation: one line on which direction to pursue first

## Reference files

- `references/engineering-parameters.md` — Step 3
- `references/contradiction-matrix.json` — read by `scripts/lookup.py`, Step 4
- `references/inventive-principles.md` — Step 5
- `references/separation-principles.md` — physical contradictions
