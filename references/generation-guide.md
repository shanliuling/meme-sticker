# 2x6 Sticker Sheet Generation Contract

This skill uses **two** sheets, not one 12-grid sheet.
Each sheet must contain exactly **6 stickers**.

## Sheet layout
Every generated sheet must follow:
- exactly 6 stickers
- exactly 3 columns × 2 rows
- landscape composition
- visually regular arrangement
- no visible grid lines

Think of the sheet as 6 invisible territories:

```text
+-------------+-------------+-------------+
|      1      |      2      |      3      |
+-------------+-------------+-------------+
|      4      |      5      |      6      |
+-------------+-------------+-------------+
```

## Visual style target
Default style:
- cute, expressive chat-sticker style
- recognizable subject identity
- white die-cut sticker outline around the sticker content when appropriate
- subtle shadow only if it helps the silhouette
- short chat-friendly captions
- cohesive art direction

## Critical extraction rule
The final pack is extracted automatically, so the sheet must be extraction-friendly.

### Required constraints
- every sticker must stay fully inside its own territory
- subject, caption, white outline, and all decorative marks must belong to the same territory
- no meaningful pixels should touch or cross into the gutter
- keep visible empty space between all neighboring stickers
- it is better to make the sticker slightly smaller than to let it touch a neighbor

## Background rule
Use a single **flat, solid, contrasting key background color** across the entire sheet.
This background is temporary and will be removed by the packaging tool.

### Key background selection
Choose ONE flat key color per sheet, and choose it based on the subject so it does not appear in the sticker artwork.

Preferred choices:
- saturated cyan
- saturated green
- saturated magenta
- another saturated flat color with strong contrast to both the subject and the white outline

Important:
- the key color must be visually uniform from edge to edge
- do not use the chosen key color in captions, clothing, props, stars, bubbles, shadows, or other sticker decorations
- if the subject itself is strongly blue/cyan, prefer green or magenta instead
- if the subject itself is strongly green, prefer magenta or cyan instead
- if the subject itself is strongly magenta/red, prefer cyan or green instead

### Edge-quality rules
To prevent dirty halos after background removal:
- use a crisp white die-cut outline, not a translucent glow
- do not add cyan/green/magenta outer glow around the sticker
- do not cast colored shadows onto the key background
- keep drop shadows extremely subtle and close to the sticker, or omit them
- avoid fuzzy atmospheric effects at the outer silhouette
- keep the outermost contour clean and high-contrast

### Avoid
- white key background when stickers have white outlines
- textured backgrounds
- per-cell backgrounds
- gradients
- scenery / props unrelated to the sticker
- shadows cast far into the gutter
- checkerboards

## Caption rule
Let the image model choose the captions.
Keep them short and readable.
Avoid long phrases.
Use the same language as the user or the current conversation unless the user explicitly requests another language.
Keep the full 12-sticker pack in one language unless the user asks otherwise.

## Output exclusions
Output ONLY the sticker sheet artwork.
Do not include:
- chat UI
- app UI
- headers
- download panels
- poster layouts
- promotional copy
- labels outside the six stickers
