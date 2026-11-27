# Making vBook reader skins — guide for AI agents

You are making a **skin** for the text reader of vBook (Android / iOS / desktop). A skin is a
folder with a `skin.json` and pictures; the app draws it around and under the book's text. This
file is the complete contract: what the app reads, how it draws it, the limits, the workflow,
and the design rules learnt from the skins already here. Read it all before writing a skin.

- Human guide (Vietnamese): `README.md`. Machine-checkable schema: `skin.schema.json`.
- A minimal starting point: `template/`. Full examples: `src/*/skin.json` (20 skins).
- The renderer lives in the app repo (vBook): `modules/data/.../reader/text/skin/ReaderSkin.kt`
  (model, parser), `SkinExpression.kt` (expressions), `shared/.../reader/text/core/skin/SkinLayers.kt`
  (drawing), `SkinColors.kt` (colours). When this file and the code disagree, the code wins.

---

## 1. What a skin can and cannot do

**Can:** colours (text, page background, any named token), colours changing through the day,
a day/night palette, pictures (whole page, bands, corners), picture sets picked by an expression
(per chapter / page / hour), text from templates (book name, chapter title, page n/m,
percentages, roman numerals…), rectangles / lines / circles with fill, gradient, stroke, radius,
progress bars, built-in paper textures, per-layer conditions (first page of a chapter, dark mode,
time range).

**Cannot (don't try):** custom fonts (only `serif`, `sans`, `mono` or the reader's font),
animation, rotation, blur/shadows as properties, per-paragraph decoration, vertical text,
changing the text's font/size/line spacing, nine-slice frames (`type: "frame"` is parsed but not
drawn), JavaScript/HTML, network access. Pictures are drawn as given: bake effects into them.

The reading text itself is the app's: the skin only sets its **box** (`body`) and its **colour**
(`text` token).

## 2. Package layout

```
src/<id>/
  skin.json        required
  preview.jpg      required in the store: 480×640 (3:4) JPEG, a real-looking page in the skin
  SOURCES.md       required in the store: where every picture comes from + licence
  images/…         pictures (PNG with alpha, WebP for big ones, JPEG for photos)
```

- `<id>`: `[A-Za-z0-9_-]{1,64}`, equal to the folder name and to `"id"` in `skin.json`.
- Paths in `skin.json` are relative to the folder. Absolute paths, `..`, `:` are rejected (the
  layer draws nothing).
- Package (zip) ≤ 32 MB, unpacked ≤ 128 MB. **Aim for < 150 KB** (the 20 store skins are 50–150 KB;
  the tarot one with 22 card photos is 730 KB).
- A zip may hold the files at its root or inside one folder.

## 3. skin.json — top level

```json
{
  "schema": 1,
  "minApp": 1,
  "id": "my_skin",
  "version": 1,
  "name": { "en": "My Skin", "vi": "Skin của tôi" },
  "description": { "en": "One sentence.", "vi": "Một câu." },
  "author": "vBook",
  "preview": "preview.jpg",
  "tokens": { "background": "#f4efe4", "text": "#2a2420" },
  "timeline": [],
  "palettes": [],
  "body": { "top": 110, "bottom": 72, "left": 30, "right": 30 },
  "imageSets": {},
  "layers": []
}
```

| Key | Type / default | Meaning |
|---|---|---|
| `schema` | int, 1 | Always 1. |
| `minApp` | int, 1 | Feature level needed. The app is at **1**; higher → hidden in the store, refused on import. |
| `id` | string | See §2. |
| `version` | int, 1 | **Bump on every published change** — installed copies get an Update, and preview URLs carry `?v=version` (image caches key on the URL). |
| `name`, `description` | `{lang: string}` | `en` is the fallback. Give `en` and `vi`. Name ≤ ~20 chars (shown under a 58 dp tile). |
| `author` | string | Shown as "by …". |
| `preview` | path | Picture in the package; the store catalog points at a copy. |
| `tokens` | `{name: colour}` | §5. |
| `timeline` | `[{at, tokens}]` | §5. |
| `palettes` | `[{when, tokens}]` | §5. |
| `body` | `{top,bottom,left,right}` dp, defaults 48/40/24/24 | The text box, in from the page's safe edges. Replaces the user's margins while the skin is worn; the app's own header/footer is hidden — yours go in the `top` / `bottom` bands. |
| `imageSets` | `{name: {pattern, count}}` | §6.3. |
| `layers` | array | §6. |

Unknown keys are ignored (so `"$schema"`, comments-as-keys etc. are harmless). A layer with an
unknown or bad `type` is skipped, the rest of the skin still works.

## 4. Geometry

All lengths are **dp** (≈ 1/160 inch). A phone page is ~360–430 dp wide, 700–900 dp tall; a
tablet / unfolded foldable shows **two pages side by side**, each drawn with the full skin;
landscape makes pages short and wide. Design for any size.

Four anchor boxes per page:

```
┌──────────── page (whole page, inside display cutouts) ────────────┐
│  top band  = page top … body top          (height = body.top)     │
│  ┌──────────────────── body (the text) ───────────────────────┐   │
│  │ left/right = body.left / body.right in from the page edges │   │
│  └────────────────────────────────────────────────────────────┘   │
│  bottom band = body bottom … page bottom  (height = body.bottom)  │
└────────────────────────────────────────────────────────────────────┘
```

`rect` places a layer inside its anchor, CSS-absolute style (dp, may be negative = outside):

| Given on an axis | Result |
|---|---|
| `left` + `right` | pinned both sides; `width` ignored |
| `left` (+ `width`) | from the left; no width → stretches to the right edge |
| `right` (+ `width`) | from the right; no width → stretches to the left edge |
| `width` only | centred |
| nothing | fills the axis |

Same for `top` / `bottom` / `height`. `rect: {}` = the whole anchor box.
Idiom: paper behind the text = `"anchor":"body", "rect":{"left":-14,"right":-14,"top":-12,"bottom":-12}`.

Status bar: the page box excludes display cutouts only. Readers usually hide the status bar, but
when it shows it overlaps the first ~24 dp of the top band on phones without a cutout — keep
important header text below `top: 14`, and give `body.top` ≥ ~90 when the top band holds a header.

## 5. Colours

A colour value is one of:
- `#rrggbb` or `#rrggbbaa` (alpha last, CSS order);
- a token name (`"muted": "glow"`), followed up to 4 levels;
- either with an opacity suffix: `"ink@55%"`, `"#ffffff@16%"`.

Tokens the **app** reads: `text` (the book's text colour) and `background` (page colour under all
layers). Also: `paper` is the base colour of `texture` layers (fallback `background`); `accent`
outlines the highlighted picture of a `set`. Every other name is yours (`gold`, `ink`, `faint`…).

Resolution order, later wins: `tokens` → `timeline` (at the current time) → each `palettes` entry
whose `when` holds, in order.

**timeline**: stops `{ "at": "HH:mm", "tokens": {…} }`. Between two stops every colour is blended
(Oklab), wrapping round midnight; the clock moves in 15-minute steps. Each stop should list every
token that changes. To **switch** rather than blend (day → night with light text on dark), put two
stops ≤ 15 min apart:

```json
"timeline": [
  { "at": "00:00", "tokens": NIGHT }, { "at": "05:15", "tokens": NIGHT },
  { "at": "05:30", "tokens": DAWN },  { "at": "09:00", "tokens": DAY },
  { "at": "17:00", "tokens": DAY },   { "at": "18:30", "tokens": DUSK },
  { "at": "19:45", "tokens": DUSK },  { "at": "20:00", "tokens": NIGHT }
]
```

Never blend `text` from dark to light across an hour: mid-way the text and the page are the same
grey. Colours that don't affect legibility (sky, fog, accents) may blend freely.

**palettes**: `{ "when": {"dark": true}, "tokens": NIGHT }` — the app's dark mode. Add one whenever
the day colours are light.

E-ink devices: every colour becomes black or white and pictures, sets and textures are not drawn.
The skin must still read as text + lines.

## 6. Layers

Common keys:

| Key | Default | Meaning |
|---|---|---|
| `type` | — | `image`, `set`, `text`, `shape`, `texture` |
| `anchor` | `page` (`texture`: `body`) | `page`, `body`, `top`, `bottom` (§4) |
| `rect` | `{}` | §4 |
| `z` | `-1` image/shape/texture, `1` set/text | `< 0` under the text, `≥ 0` over it. Same side: drawn in array order (later on top). |
| `opacity` | `1` | 0..1; `0` = never drawn. |
| `when` | always | `{pages, dark, time}`, all given must hold: `pages` `"first"` (a chapter's opening page) / `"other"`; `dark` bool (app dark mode); `time` `"HH:mm-HH:mm"` (wraps midnight if end < start). With no clock a time condition is false. |

Layers over the text (`z ≥ 0`) must not cover the body except as a faint overlay (the Terminal
scanlines at 22 % are the limit).

### 6.1 image
`{"type":"image","src":"images/x.png","fit":"crop"}` — `fit`: `crop` (cover, cut the overflow;
default), `contain` (whole picture, letterboxed), `fill` (stretch). No tiling: draw a big enough
picture.

### 6.2 shape
`shape`: `rect` (default) | `line` (horizontal through the box's middle; needs `stroke`) | `circle`.
`fill`, `fillEnd` (vertical gradient fill → fillEnd), `stroke`, `strokeWidth` (dp, 1),
`radius` (dp corner), `progress` (expression 0..1: drawn to that share of its width — progress
bars). Typical: track `fill:"faint"` + bar `fill:"accent", progress:"chapter.progress"` with the
same rect.

### 6.3 set — a picture picked by an expression
```json
"imageSets": { "moon": { "pattern": "moon/moon-{i}.png", "count": 8 } },
{ "type":"set", "set":"moon", "pick":"chapterSeed % 8", "count":1, "anchor":"top",
  "rect":{"right":22,"top":14,"width":56,"height":56} }
```
- `pattern`: `{i}` → index, `{i:2}` → zero-padded to 2. `count` ≤ 128 pictures.
- `pick`: expression for the first index (wraps modulo the set size).
- `count` (row length, ≤ 32), `gap` (dp, 4), `radius` (dp, 2), `highlight` (0-based slot drawn
  whole with an `accent` outline; others at `dim`, 0.45; null = all whole). Each slot is
  `(width − gap·(count−1)) / count` wide, full height, pictures cropped to it.
- Uses: a card per chapter (`chapterSeed % N`), a frame per page (`page.index - 1`), per hour
  (`time.hour`, 24 frames — sun/moon crossing the sky).

### 6.4 text
```json
{ "type":"text", "value":"{chapter.title}", "anchor":"top",
  "rect":{"left":28,"right":110,"top":40,"height":26}, "size":17, "color":"ink", "weight":600 }
```
`value` (template: literal text with `{expression}` parts), `size` (sp, 4–96, default 12),
`color` (default `text`), `font` (`serif`/`sans`/`mono`; omitted = the reader's font), `weight`
(100–900), `italic`, `align` (`start`/`center`/`end`; mirrored for RTL), `letterSpacing` (sp),
`maxLines` (1–8; overflow ends in "…"). Text is vertically centred in its box — give `height`
≈ size × 1.5. `\n` breaks a line (needs `maxLines` ≥ 2).

### 6.5 texture
`{"type":"texture","texture":"aged","anchor":"page","rect":{},"opacity":0.4,"z":-2}` —
`texture`: `paper`, `do` (mulberry paper), `linen`, `aged`; `radius`. It paints the `paper`
token **opaquely** then the grain: put it right after the page colour, under the pictures, and
use `opacity` to dose it. Night: lower it (0.1–0.2) with a second layer under a `time` condition.

## 7. Expressions

Used in `{…}` of text values, `set.pick`, `shape.progress`. Numbers, `'strings'`, `true/false`,
`+ - * / %`, `== != < <= > >=`, `&& || !`, `a ? b : c`, parentheses, the functions below. No
assignment, loops, member access. Max 512 chars. Errors give `""` (or the fallback), never crash.

| Variable | Value |
|---|---|
| `book.name`, `chapter.title` | strings |
| `chapter.index`, `chapter.count` | 1-based / total |
| `page.index`, `page.count` | 1-based page in the chapter / pages in it |
| `chapter.progress`, `book.progress` | 0..1 |
| `chapterSeed` | stable 32-bit hash of (book, chapter) — "random but fixed" per chapter |
| `first`, `dark` | booleans |
| `time.hour` (0–23), `time.minute` (minutes since midnight), `dayProgress` (0..1) | 15-minute steps |
| `phase` | `'dawn'` 05–08, `'day'` 08–17, `'dusk'` 17–20, `'night'` |

| Function | Result |
|---|---|
| `percent(x)` | `42.5%` |
| `roman(n)` | `XII` (1–3999) |
| `pad(n, w)` | `007` |
| `upper(s)` | upper case |
| `pick(i, a, b, …)` | the i-th (wrapping) of the choices |
| `if(c, a, b)` | a or b |
| `min max clamp(x,lo,hi) lerp(a,b,t) floor round abs sin` | maths |

Examples: `"{page.index} / {page.count}"`, `"{roman(chapter.index)} · {upper(book.name)}"`,
`"{pick(chapterSeed % 4, 'Xuân', 'Hạ', 'Thu', 'Đông')}"`,
`"{phase == 'night' ? 'NIGHT WATCH' : 'DAY WATCH'}"`.

## 8. Pictures

- **Own work or public domain / CC0 only.** No game textures, film stills, characters, logos,
  fonts you don't hold rights to. Port a design idea, redraw everything. Record sources in
  `SOURCES.md`.
- Draw as SVG and rasterise with **Chrome headless** — `tools/chrome_render.py`
  (`chrome_render(svg_text, Path("src/<id>/images/x.png"))`). ImageMagick's own SVG renderer drops
  strokes on unfilled shapes; don't use it for SVG. Generators: `tools/gen_assets*.py`.
- Size for the place it's drawn: a top-band strip should be about as wide as the band is tall ×7
  (e.g. 1820×260) so `crop` cuts the sides, not the sky; whole-page overlays 720×1280.
- PNG with alpha for line art; WebP (quality ~85) for large or photographic pictures. Check
  alpha survived (`magick identify -format "%[channels]"` → `srgba`).
- Pixel art: draw each art pixel as a 4–8 px square so scaling up stays crisp.

## 9. Design rules (learnt the hard way)

1. **One surface.** Header, footer and page share one tone. A dark band around a light sheet of
   paper reads as two things stuck together. If the day page is light, the header is light too.
2. **Text never over busy art.** Leave clear sky behind header text; put scenery under or beside
   it. Over a picture, use a solid/opaque pill behind the text.
3. **Contrast ≥ 4.5 : 1** for `text` on its background at **every** timeline stop and in the
   dark palette. Labels on light skies use `ink`/`muted`, not white.
4. **Switch, don't blend, day ↔ night** (§5). Provide a dark palette.
5. **Restraint.** One focal picture (corner branch, moon, cameo), small labels (8–10 sp,
   letter-spaced caps), one accent colour. Whole-page overlays (petals, snow, stars) at 30–90 %
   under the paper card, not over the text.
6. **Body card.** A card (`shape` with `fill`, `radius`) behind the body, `frame(14,12)`, gives
   text a calm ground on top of scenery.
7. **Readable header hierarchy:** kicker (tiny caps) → chapter title (15–17, weight 600–700) →
   book name (9–10, muted).
8. **Footer:** page `n / m` or a folio, a progress line, book percent — 8.5–12 sp.

## 10. Workflow

1. Copy `template/` to `src/<id>/`, set `id`, names, description.
2. Write pictures with a generator script (keep it in `tools/` if new), render with Chrome.
3. Fill `skin.json` (start it with `"$schema": "../../skin.schema.json"` for editor checks).
   Validate every skin against the schema:
   `(cd /tmp && npm i ajv@8) && NODE_PATH=/tmp/node_modules node skins/tools/validate_schema.js skins`,
   then parse it with the app's own reader:
   `VBOOK_SETTINGS=<this repo> ./gradlew :modules:data:jvmTest --tests '*ReaderSkinTest*'`
   (in the vBook repo; checks every `src/*/skin.json` parses, ids match, preview exists).
4. Try it on a device/emulator: zip the folder, push it, Reader → Settings → Skin → Skin store →
   import (upload icon). Look at: phone portrait, two-page spread, day **and** night (dark mode).
5. Preview: screenshot a page of a real-looking book (not "test" text) in portrait 3:4, crop the
   status bar, 480×640 JPEG q≈84 → `src/<id>/preview.jpg`.
6. `python3 skins/build.py` → `<id>.zip`, `previews/<id>.jpg`, `catalog.json`. Commit sources and
   outputs together. Bump `version` for any change to a published skin.

## 11. Checklist before publishing

- [ ] `id` = folder name; `version` bumped if it changed; `en` + `vi` name/description.
- [ ] No layer of text over scenery without a pill/card; header text ≥ `top: 14`.
- [ ] Day, dusk and night (and dark palette) all legible; day ↔ night switches, not blends.
- [ ] Spread (two pages) and short landscape pages look right.
- [ ] Pictures own/PD/CC0, listed in `SOURCES.md`; transparent where they should be.
- [ ] Package small (< 150 KB unless photos justify more).
- [ ] `preview.jpg` 480×640 from a real-looking page; `build.py` run.
