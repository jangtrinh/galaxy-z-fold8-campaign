# Galaxy Z Fold8 — The Frame Unfolds

An independent, scroll-driven campaign study for Samsung Galaxy Z Fold8, built as one self-contained HTML file plus a relative `assets/` folder.

## Direction

**Surface:** Decide / Learn.

**Composition thesis:** the physical fold is the page's spatial grammar. Every major transition changes aspect ratio, reading direction, or layer depth rather than repeating a standard marketing section.

**Signature move:** a central titanium hinge line opens the page from 10:16 to 4:3 while the device crosses foreground and background type.

**Visual system:** museum black, warm paper, titanium lavender, Samsung blue, coral signal; precise 1px rules; tightly tracked grotesk display type; monospaced technical labels.

**Avoided template:** centered hero plus equal feature cards. Each section carries one specific product truth in a distinct composition.

## Evidence boundary

Product claims are sourced from Samsung's US Galaxy Z Fold8 product page and Samsung Global Newsroom, accessed 2026-07-24:

- Official name: Galaxy Z Fold8
- 5.5-inch cover screen / 7.6-inch main screen
- Approximate aspect ratios: 10:16 folded / 4:3 unfolded
- 4.5mm thickness
- 201g weight
- 4,800mAh typical battery
- Up to 26 hours video playback under Samsung test conditions
- Snapdragon 8 Elite Gen 5 for Galaxy
- 50MP wide and ultra-wide rear cameras
- 256GB, 512GB, and 1TB storage options
- US starting price: $1,899.99 before trade-in at access time
- Colors: Pistachio, Lavender, Graphite, Cream

No invented awards, reviews, testimonials, availability, durability guarantees, or performance metrics.

## Artifact contract

- `index.html`: complete inline CSS and JavaScript
- `assets/`: relative campaign assets
- Desktop, tablet, phone, short-screen, touch, and reduced-motion behavior
- No runtime dependency
- No horizontal document overflow
- Content remains visible if JavaScript fails
- Generated imagery must contain no baked-in marketing copy
- Page footer discloses this as an independent design study and links product claims to Samsung

## Verification target

1. Open through a local HTTP server.
2. Test 1440px, 768px, and 390px widths.
3. Exercise scroll boundaries, view switcher, pointer parallax, index previews, keyboard focus, and reduced motion.
4. Confirm no console errors or failed relative assets.
5. Confirm `document.documentElement.scrollWidth - innerWidth === 0`.
6. Run DESIGN:OS layout, accessibility, taste, content, and design-system usage checks where supported.
