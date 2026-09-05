---
tokens:
  color:
    canvas: "oklch(0.985 0.006 310)"
    surface: "oklch(0.965 0.010 310)"
    surface_strong: "oklch(0.930 0.018 310)"
    text: "oklch(0.240 0.025 310)"
    muted: "oklch(0.520 0.025 310)"
    border: "oklch(0.880 0.015 310)"
    accent: "oklch(0.420 0.140 305)"
    accent_dark: "oklch(0.340 0.130 305)"
    malignant: "oklch(0.580 0.160 32)"
    malignant_soft: "oklch(0.940 0.035 32)"
    benign: "oklch(0.540 0.100 140)"
    benign_soft: "oklch(0.940 0.030 140)"
    warning: "oklch(0.360 0.080 60)"
    warning_soft: "oklch(0.950 0.045 75)"
    error: "oklch(0.550 0.190 25)"
    error_soft: "oklch(0.960 0.025 25)"
    focus: "oklch(0.700 0.140 305)"
  typography:
    family: '"Segoe UI", system-ui, sans-serif'
    prose_measure: "70ch"
    numeric: "tabular-nums"
  spacing:
    xs: "4px"
    sm: "8px"
    md: "12px"
    lg: "16px"
    xl: "24px"
    2xl: "32px"
    3xl: "48px"
    4xl: "64px"
  radii:
    control: "5px"
    button: "6px"
    compact: "7px"
    panel: "9px"
  layout:
    container: "1180px"
    sidebar: "252px"
    mobile_breakpoint: "900px"
    narrow_breakpoint: "640px"
  interaction:
    target_min: "44px"
    focus_width: "3px"
    focus_offset: "2px"
---

# Design system

## 1. Visual Theme & Atmosphere

This is an index-style analytical dashboard: restrained, light, evidence-first, and comfortable on a large monitor in a bright office. The aubergine navigation and accent family gives the product identity; open canvas, dividers, compact panels, and readable data give it analytical focus. The interface communicates model behavior and provenance, not clinical authority.

Use whitespace and hierarchy before decoration. Avoid the look of a healthcare landing page, generic AI product, or dashboard template.

## 2. Color Palette & Roles

The YAML tokens above are the source values. Runtime CSS custom properties mirror them in `frontend/src/styles.css`.

- Canvas and surface provide restrained contrast; text and muted text establish hierarchy.
- Accent and accent-dark are aubergine navigation, action, link, and focus-family colors.
- `malignant` is coral and `benign` is sage. Both roles require text labels, table structure, or icon/shape support; color is never the only meaning.
- Warning and error use warm semantic treatments with explicit text and roles. A disclaimer uses the accent family and a clear educational title.
- Focus uses a 3px visible ring with a 2px offset. It must remain visible on light and dark surfaces.

Do not add gradients, neon colors, pure red/green-only semantics, or colors that imply clinical urgency beyond the educational warning.

## 3. Typography Rules

Use `"Segoe UI", system-ui, sans-serif`. Headings are compact and editorial, with restrained negative tracking at display sizes. Body copy uses a maximum readable measure of 70 characters and a line-height near 1.65. Labels are concise and uppercase only for small section labels. Metrics, scores, thresholds, counts, and table values use tabular numerals. Do not display unsupported precision.

## 4. Component Stylings

- Buttons use native `<button>`, a minimum 44px height, clear text, visible hover/focus/active/disabled states, and primary/secondary/text variants. Loading buttons retain their label and communicate progress.
- Surfaces and panels mark distinct interactive or evidence regions. Prefer dividers and open sections over nested cards; use the panel radius token and no unnecessary shadow.
- Metrics show label, value, and detail in a stable hierarchy. Values are not presented as clinical confidence or probability.
- Status badges and callouts include a text label and semantic role. Malignant/benign, warning, error, and disclaimer states are not color-only.
- Tables use semantic `<table>`, `<caption>`, `<thead>`, row headers, explicit numeric alignment, and a bounded overflow wrapper on narrow screens.
- Charts have a visible title/caption or heading, accessible name/description, disabled animation, and a nearby textual summary or semantic table/fallback.
- Loading uses quiet skeleton blocks and a visually hidden status label. Empty states explain what is missing and what the user can do next. Error states use `role="alert"` and actionable, non-clinical copy.

## 5. Layout Principles

The desktop shell uses a compact fixed left rail of 252px and a centered analytical canvas capped at 1180px. Use grid and flex for relationships, `min-width: 0` for data regions, and dividers for grouping. Keep the evidence canvas open; avoid a giant rounded-card grid for every section. The primary workflow is evidence first, then local sample-based inference.

## 6. Depth & Elevation

Depth comes from canvas/surface contrast, borders, spacing, and document order. Shadows are unnecessary by default and may not be used to make ordinary evidence sections look like floating products. Navigation can use a solid aubergine field; content surfaces stay light and calm.

## 7. Interaction & Motion

Use native controls and keyboard order. Every interactive control has a visible focus state and a minimum 44px target. Preserve skip navigation, `aria-live` model-output announcements, mobile navigation, loading/error/empty behavior, and lazy page loading. Motion is brief and functional; skeleton pulse and transitions must be disabled or minimized under `prefers-reduced-motion: reduce`. Do not animate charts in a way that hides evidence.

## 8. Responsive Behavior

- At 900px and below, the rail becomes a sticky horizontal navigation bar and the main margin is removed.
- At 640px and below, hide nonessential brand detail, stack page headings/forms/layouts, and reduce panel padding while retaining 44px controls.
- Tables use bounded horizontal scrolling rather than breaking the page. Charts and figures remain within their parent width.
- Verify desktop, tablet/mobile, keyboard focus, and zoom/reflow without horizontal overflow. Do not use hover as the only way to access information.

## 9. Agent Prompt Guide

When changing UI, preserve the educational model-evidence identity, the aubergine/coral/sage roles, and the evidence-first report canvas. Read `PRODUCT.md` and `CONTEXT.md` before editing copy. Reuse a primitive before creating one; use a token before adding a literal. Keep hosted mode read-only and local inference explicit. For every chart, add a text/table alternative. Treat generated metrics and reports as authoritative artifacts, never as design filler.

Anti-patterns: generic AI gradients; glassmorphism; excessive pills; giant rounded-card grids; unnecessary shadows; DNA/cancer/hospital decoration; red/green-only communication; color-only chart meaning; fake precision; and clinical certainty language.
