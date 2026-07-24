# Codex implementation brief — Galaxy Z Fold8 · The Frame Unfolds

## Mission

Implement the complete campaign page now. Deliver a working `index.html` with inline CSS and JavaScript, using relative assets from `assets/`. Do not stop at a plan or stub. Exercise the result through a local HTTP server and deterministic checks before reporting.

## Locked direction

- Surface: Decide / Learn.
- Thesis: the physical fold is the page’s spatial grammar.
- Signature move: a central titanium hinge line opens the composition from folded 10:16 to unfolded 4:3 while the device crosses foreground and background type.
- Visual system: museum black, warm paper, titanium lavender, Samsung blue, coral signal; precise 1px rules; tightly tracked grotesk display type; monospace technical labels.
- Avoid generic centered hero + equal feature-card grids.

## Required page structure

1. Fixed slim left rail and fixed top bar.
2. Pinned hero with normalized 0..1 scroll progress and three phases: intro, build, release. Use `overflow: clip`, never a sticky-breaking ancestor with `overflow: hidden`.
3. Three-view product switcher. Preload before swapping; preserve scroll state; meaningful alt text.
4. Horizontal narrative: tall outer section + sticky viewport + translated track; active label and real progress meter derived from the same normalized progress.
5. Commerce section with price, storage, colors, CTA, and verified metadata from README. Stack deliberately on mobile.
6. Full-width system laboratory using `assets/system-lab.jpg`, visually distinct from commerce.
7. Typographic product index with cursor-following image previews on pointer devices and an accessible non-hover fallback.
8. Finale using `assets/finale-macro.png`, oversized campaign wordmark, CTA, and complete footer with independent-study disclosure and Samsung source links.

## Motion and interaction

- First-load entrance with distinct origins for hero layers; remove entrance state when done so scroll transforms own the scene.
- Shared section-reveal engine with multiple variants, not one repeated fade-up.
- Pointer parallax uses current/target follower interpolation; reset target on leave; disable on touch and reduced motion.
- Use robust clamped scroll math and guard zero-length ranges.
- JS failure must not leave content invisible.

## Responsive requirements

Recompose for desktop, tablet, phone, short desktop screens, touch, and reduced motion. Simplify rail/header on narrow widths. Keep device imagery large while preserving text readability. Footer must join normal flow on mobile. No horizontal document overflow.

## Asset policy

Preferred approved assets:
- `assets/hero-open.png`
- `assets/view-folded.png`
- `assets/commerce-ghost.png`
- `assets/system-lab.jpg`
- `assets/finale-macro.png`

Secondary/use cautiously:
- `assets/view-hinge-chroma.png` still has a generated background; only use if composition intentionally contains it and it does not look like an unfinished chroma asset.
- `assets/ratio-motion.png` failed geometry review; do not use as a prominent product truth image.
- `assets/contact-sheet.jpg` and `assets/cutout-check.jpg` are QA artifacts, not campaign artwork.

## Verification to implement and run

- Add a stdlib-only `scripts/verify-page.py` that verifies: required files/assets exist; no absolute local paths; no missing relative asset references; one H1; semantic main/nav/footer; viewport meta; reduced-motion CSS; no obvious placeholder text.
- Serve over localhost and confirm `index.html` and referenced assets return HTTP 200.
- Run `git diff --check`.
- Keep code maintainable despite single-file requirement: clear section comments and small named JS functions.

## Boundaries

Do not modify `README.md`, `design-brief.json`, `ASSET-CONTRACT.md`, existing imagery, or this brief. Do not commit; Hermes will review and commit after QA.
