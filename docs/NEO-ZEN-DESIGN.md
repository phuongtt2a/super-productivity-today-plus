# NEO-Zen Design System · v1

Shared visual contract for Today+, Five and Deadline Watch.

## Principles

- **Shared shell:** centered maximum desktop width **1220px**; matching 41px brand mark, title/byline proportions, aligned main content.
- **Use the application's font:** `var(--font-primary-stack)`, with system fallbacks supporting Vietnamese. Never bundle new display fonts.
- **Preserve wallpaper transparency:** keep `html`, `body`, iframe and primary root canvases transparent in the host. Use the app's supplied theme colors and opacity for individual soft tinted surfaces.
- **NEO accents:** crisp 2px contrast-aware outlines, near-square corners, sturdy readable type hierarchy, hard zero-blur shadows (2–5px), selected green / gold / blue / coral / lilac panels.
- **Zen restraint:** distinct content priorities and generous but efficient whitespace. Avoid decorative hero bloat, unnecessary animation and arbitrary reflow of controls.
- **UX and accessibility:** preserve touch target sizes, keyboard focus outlines, hover/disabled states and semantic ARIA labels.

## Per-plugin layout contracts

- **Today+:** paired task/habit workspace, subtasks and all task/habit actions untouched; small viewports stack columns rather than compress cards.
- **Five:** full-height, five visible priorities without vertical scrolling; a separate independently scrollable Arrange view. Outer shell aligns at 1220px, focus typography still progressive.
- **Deadline Watch:** one chronological list with strongest type on earliest dates and inline repeating end dates.

## Verification before release

Capture browser screenshots using synthetic Vietnamese titles and host-simulated wallpaper in desktop, 390px and 320px dimensions. Test root/body transparency and host font; ensure zero horizontal overflow and no interaction regressions. Review screenshots in PR. Keep minor design releases on the existing plugin version and use the automatic release workflow on merge.
