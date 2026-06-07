# Design System

## Direction

Restrained light product interface. A reviewer uses it on a large monitor in a bright office, focused on evidence and workflow rather than decoration.

## Color

- Canvas: `oklch(0.985 0.006 310)`
- Surface: `oklch(0.965 0.010 310)`
- Text: `oklch(0.24 0.025 310)`
- Muted: `oklch(0.52 0.025 310)`
- Border: `oklch(0.88 0.015 310)`
- Accent: `oklch(0.42 0.14 305)`
- Malignant: `oklch(0.66 0.16 32)`
- Benign: `oklch(0.67 0.10 140)`
- Error: `oklch(0.58 0.19 25)`

## Typography

Use `"Segoe UI", system-ui, sans-serif`. Fixed product scale, tabular numerals for metrics, maximum prose measure of 70 characters.

## Layout

Desktop uses a compact left navigation and open analytical canvas with dividers. Mobile replaces the rail with horizontal navigation. Avoid nested cards; use panels only for distinct interactive regions.

## Interaction

All controls provide visible hover, focus, active, disabled, loading, error, and success states where applicable. Minimum touch target is 44 pixels. Prediction results are announced with `aria-live`.
