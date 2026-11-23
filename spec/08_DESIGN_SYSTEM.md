# 08 · Design System: Frida Kahlo, as on the US Economy Monitor

These tokens are copied from the live Economy Monitor page (`us-economy-monitor/site/index.html`, read 22 November 2026). Use them exactly so the two products read as one family. If the monitor's tokens change, the monitor wins; re-read its page before building.

## The idea behind the palette

Kahlo's palette is Mexican folk color on a plaster wall: cobalt from the Casa Azul, cochineal red, rosa mexicano, marigold, leaf green, ochre earth. On this app the colors carry meaning, not decoration. The wall stays calm and warm; color appears only where money moves.

## Tokens

```css
:root {
  --wall: #FBFAF6;         /* page ground, warm plaster */
  --panel: #FFFFFF;        /* cards, panels */
  --line: #E4E1D8;         /* hairlines */
  --ink: #1B1D26;          /* text, 16.1:1 on wall */
  --ink-2: #555A6B;        /* secondary text, 6.6:1 */
  --ink-3: #8A8E9C;        /* tertiary, 3.1:1: large text and non-text only */
  --cobalt: #1F4FA8;       /* 7.3:1 */
  --cobalt-deep: #173C82;  /* 10.0:1 */
  --cobalt-wash: #EAF0FA;
  --cochineal: #B5263A;    /* 6.1:1 */
  --rosa: #C9357A;         /* 4.7:1 */
  --leaf: #2F7A52;         /* 5.0:1 */
  --ochre: #C27F0A;        /* 3.2:1: marks and large text only */
  --marigold: #F0B429;     /* 1.8:1: fills and highlights only, never text */
  --serif: var(--font-anthropic-serif, Georgia, "Times New Roman", serif);
  --sans: var(--font-anthropic-sans, system-ui, -apple-system, "Segoe UI", sans-serif);
}
```

Contrast ratios above were computed against `--wall`. Rule carried over from the monitor's video review: highlight rings use ochre, not marigold, on the light page.

## Meaning map

| Meaning | Color | Line style (so color is never the only signal) |
|---|---|---|
| Nvidia (center) | `--ink` fill, marigold ring | Double ring |
| Equity (EQ, EQ-SPV) | `--cobalt` | Solid |
| Conditional equity (EQ-C) | `--cobalt` at 40% | Solid, hollow core |
| Backstop, guarantee (BK, GU) | `--cochineal` | Dashed |
| Leaseback, capacity rental (LB) | `--rosa` | Dotted |
| Financing commitment (FC) | `--cobalt-deep` | Solid with arrowhead |
| Supply prepayment (PP) | `--ochre` | Double line |
| Residual value or repurchase (RV) | `--cochineal` | Dash-dot |
| Fund commitment (LP) | `--cobalt` at 60% | Solid with cross ticks |
| License (LI) | `--leaf` | Thin solid |
| Context (CX) | `--ink-3` | Hairline |
| Headline-only portion | Same hue at 20% | Wide faint halo behind the committed stroke |
| Specific wrong-way risk | Small `--cochineal` notch on the node | Notch shape plus "Specific wrong-way risk" in the hover and panel |
| Counterparty grade (only if grades are turned on) | Node outline: Strong `--leaf`, Adequate `--cobalt`, Watch `--ochre`, Weak `--rosa`, Distressed `--cochineal`, Insufficient information `--ink-3` | Outline thickness rises with weakness, plus a text label in the panel |
| Analysis label | `--ink-2` text on `--cobalt-wash` chip | The word "Analysis" |

## Type

- Serif (`--serif`) for the title, section headings and every insight sentence. This is the voice of the page.
- Sans (`--sans`) for interface, tables and numbers. Numbers use tabular figures (`font-variant-numeric: tabular-nums`) so columns align.
- Scale to match the monitor: title about 2.4rem serif; section headings 1.4rem serif; body 1rem; table and chip text 0.8125rem. Key figures in tiles 2rem sans, below the heading's visual weight (lesson from the Economic Index dashboard critique).

## Components to reuse from the monitor

Chips (`em-chip` pattern with `aria-pressed`), tiles, drawers, history charts and the "Built By" header. Copy their markup and class names where possible so a future shared stylesheet is easy.

## Motion

Panel slides in over 180 ms, ease-out. Constellation nodes fade into place on first load over 400 ms, then never animate again unless the user changes a filter. Respect `prefers-reduced-motion`: no movement, instant state changes.

## What not to do

No gradients, no glow, no drop shadows beyond a 1px hairline, no folk-art illustration or Kahlo imagery (the palette is the reference, not her paintings), no logos of counterparties (names in text only).
