# Galaxy Z Fold8 Campaign — Retrospective

## Outcome

The campaign shipped as a static, scroll-driven GitHub Pages site with a consistent nine-image V3 family, local typography, an image-backed horizontal narrative, and a layered transparent hero with pointer and scroll depth.

## What went well

- The user-approved V3 image became the style anchor for the complete family.
- Human approval remained the authority for image aesthetics.
- One model context handled both page implementation and campaign-image generation.
- Product, material, lighting, palette, and screen-art invariants became explicit.
- The final hero separates background, transparent product, frame, and live copy.
- Horizontal panels, progress, pointer reset, reduced motion, calm commerce, hover previews, and finale CTA follow the intended interaction rhythm.
- Deterministic checks finished with zero structure, asset, taste, or static accessibility errors.

## Mistakes and root causes

### 1. Automated taste judgment overruled the user

**Mistake:** Early asset review treated model-based aesthetic criticism as a rejection gate, even after the user liked an image.

**Root cause:** Correctness QA and subjective art direction were mixed into one authority.

**Impact:** Unnecessary retries, token usage, and slower convergence.

**Correction:** The user owns aesthetic approval. Automation checks only technical failures unless explicitly asked to critique.

### 2. Image generation began before the full placement matrix was locked

**Mistake:** Images were produced incrementally without first mapping every section to a required composition.

**Root cause:** The workflow optimized individual prompts instead of the complete page system.

**Impact:** One section remained visually empty; other images required replacement or reframing.

**Correction:** Define placement, aspect ratio, subject position, copy-safe area, and invariant role before generation.

### 3. Composition fit was treated as an image problem

**Mistake:** The folded image placed visual weight behind left-aligned copy.

**Root cause:** Selection focused on visual quality, not the image's role in the layout.

**Impact:** Text and product competed.

**Correction:** Select imagery by whitespace geometry. Use reversible CSS transforms when a simple horizontal flip solves the placement without regeneration.

### 4. Typography lacked a contract

**Mistake:** Arial, Helvetica, Courier New, and ad-hoc sizes were mixed directly in CSS.

**Root cause:** Typography was styled locally instead of defined as a system.

**Impact:** Inconsistent voice and sub-16px body text.

**Correction:** Use two explicit families only: Space Grotesk for display/body and IBM Plex Mono for technical labels, both self-hosted and tokenized.

### 5. The hero was initially a single flattened image

**Mistake:** The first hero could only fake depth because background and product were baked together.

**Root cause:** Asset generation was not planned around interaction layers.

**Impact:** Pointer and scroll parallax lacked real separation.

**Correction:** Generate a background plate and a high-contrast chroma product plate, remove the matte deterministically, verify four transparent corners, then animate layers independently.

### 6. Generated dimensions were assumed exact

**Mistake:** The backend returned 1671×941 and 1670×941 despite a 1672×941 request.

**Root cause:** Prompt constraints were treated as guaranteed output contracts.

**Impact:** The production pipeline initially failed its dimension check.

**Correction:** Preserve one-shot generation, then normalize the canvas technically without aesthetic retries. Verify PNG mode, dimensions, alpha range, and transparent corners.

### 7. Deployment was left too late

**Mistake:** GitHub Pages was enabled near the end, then remained queued upstream.

**Root cause:** Deployment was treated as handoff rather than an early integration surface.

**Impact:** The review URL was temporarily 404 despite a valid repository and configuration.

**Correction:** Create the review deployment after the first stable vertical slice; keep later work as incremental pushes.

### 8. Progress communication became noisy

**Mistake:** Tool interruptions and background completions caused too many intermediate updates.

**Root cause:** Operational events were surfaced individually instead of being consolidated around decisions.

**Impact:** User distraction and concern about token burn.

**Correction:** For autonomous finishing work, report once at completion. Use bounded checks, no polling loops, and no aesthetic retry loops.

## New operating rules

1. Lock direction, section plan, motion plan, and asset-placement matrix first.
2. Record image invariants before any generation call.
3. Generate once per requested asset unless the user requests another attempt.
4. Separate technical QA from human aesthetic approval.
5. Choose images by composition fit and copy-safe space.
6. Prefer reversible CSS transforms over regeneration.
7. Build interaction assets as layers, not flattened scenes.
8. Use a two-family typography contract before layout polish.
9. Run deterministic checks before one bounded browser render.
10. Deploy a review URL early.
11. Stop after one implementation pass and one QA pass unless a blocking defect is proven.
12. Consolidate progress into one completion report when the user is away.

## Verification evidence

- Hero production layers: 1672×941 PNG.
- Product cutout: RGBA with transparent and opaque pixels; all four corners alpha 0.
- `scripts/verify-page.py`: passed.
- DESIGN:OS taste lint: zero violations.
- Static accessibility lint: zero findings; not a WCAG conformance claim.
- Browser render: hero background, isolated product, live text, and downstream sections loaded without visible green matte or broken assets.

## Not verified

- Manual screen-reader testing.
- Physical iOS/Android device testing.
- GitHub's external Pages queue completion time.

## Growth target

The next campaign should reach a reviewable deployed vertical slice before generating the full image family, while preserving the same invariants and one-shot approval workflow.
