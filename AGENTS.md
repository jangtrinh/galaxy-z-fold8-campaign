# Galaxy Z Fold8 Campaign

Build an independent, premium, scroll-driven campaign study as one self-contained `index.html` plus relative files under `assets/`.

## Source of truth

Read before editing:
1. `README.md`
2. `design-brief.json`
3. `ASSET-CONTRACT.md`
4. `CODEX-BUILD-BRIEF.md`

## Hard rules

- Use only product facts already listed in `README.md`; do not invent claims, awards, testimonials, availability, or performance.
- Keep essential text in HTML, never baked into imagery.
- No runtime dependencies or build step. Inline CSS and JavaScript in `index.html`.
- Provide desktop, tablet, phone, short-screen, touch, and `prefers-reduced-motion` behavior.
- Prevent horizontal document overflow. Content must remain readable if JavaScript fails.
- Use semantic HTML, keyboard focus, alt text, and a complete real footer.
- Use existing approved assets. Do not generate images or modify source imagery.
- Avoid `assets/ratio-motion.png` for primary display because its generated geometry failed visual review.
- Do not claim completion until local HTTP serving and deterministic verification pass.

## Quality bar

Original Awwwards-level composition, not a generic centered hero/equal-card template. The physical fold is the page’s spatial grammar: transitions should change aspect ratio, reading direction, or layer depth.

## Silent bounded execution

- When the user says they are sleeping, away, wants one report, or asks for silent execution: send no progress commentary after the initial acknowledgment.
- Batch work into one implementation pass, one deterministic QA pass, and one deploy pass.
- Maximum one retry per failure mode. After one browser-vision failure, use DOM assertions or deterministic checks.
- Never surface process IDs, tool interruptions, predictions, or internal retry notes to Telegram while another path exists.
- Do not expand scope before the requested change is complete.
- Prefer the shortest reversible fix for specific feedback; layout feedback stays a CSS task.
- Stage explicit production paths. Never include unrelated working-tree changes.
- Report once after the live URL and production assets are verified.
