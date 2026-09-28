# Separation Principles — resolving physical contradictions

A **physical contradiction** demands that one property take two opposite values: the object must be hot *and* cold, present *and* absent, rigid *and* flexible, open *and* closed. You can't trade the two off against each other — instead, TRIZ resolves them by **separating the opposite requirements** so they no longer collide.

Ask the four separation questions in order; usually one of them unlocks the problem.

## 1. Separation in time
Does the property need both values *at the same moment*? If not, let it switch.

- Landing gear: needed for landing, drag in flight → retractable.
- Software: strict validation needed at write time, not at read time → validate on ingest, serve raw.
- Shape-memory alloy stent: small during insertion, expands at body temperature.

## 2. Separation in space
Does the *whole* object need both values, or different parts/locations?

- Pencil with eraser: writing end and erasing end.
- Bicycle helmet: hard shell outside, soft foam inside.
- Network: strict security at the perimeter, fast unchecked traffic inside a trusted zone.

## 3. Separation upon condition
Can the property flip depending on who/what interacts with it, or under what condition?

- Sieve: wall for large particles, opening for small ones.
- Sunglasses that darken only in bright light (photochromic).
- Rate limiter that engages only for anonymous clients; authenticated traffic passes.

## 4. Separation between parts and the whole (scale / system level)
Can the property have one value at the component level and the opposite at the system level?

- Bicycle chain: rigid links, flexible chain.
- Microservices: each service simple, the system capable.
- Rope: weak fibers, strong braid.

## Connecting back to the Inventive Principles

Each separation route is typically implemented with a cluster of the 40 Inventive Principles (see `references/inventive-principles.md`):

- **Time** → 10 Preliminary action, 11 Beforehand cushioning, 15 Dynamics, 19 Periodic action, 34 Discarding & recovering
- **Space** → 1 Segmentation, 2 Taking out, 3 Local quality, 4 Asymmetry, 17 Another dimension
- **Condition** → 32 Color changes, 35 Parameter changes, 36 Phase transitions, 28 Mechanics substitution
- **Scale** → 1 Segmentation, 5 Merging, 33 Homogeneity, 40 Composite materials

Present the separation route first ("the wing can be large *in flight* and small *on deck* — separation in time"), then use the associated principles to generate the concrete mechanisms.
