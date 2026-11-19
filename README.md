# The Meridian Gazette

**The World on One Page, Thursday 19 November 2026**

One front page, the whole planet: 42 fully written stories from six
continents, every one confirmed by two independent outlets before it
earned its place on the page.

The lead: Anthropic's $81.3 billion float — priced at $83 a share, the
largest initial public offering in history — alongside a dot-grid world
map with a numbered marker for every story, a day-in-numbers box, and a
three-column river of news grouped by region: Europe, Asia-Pacific, the
Middle East, North America, South America, Africa, Oceania, science and
sport.

## Competition

This is an entry to the make.fun bounty
[news-image-20261119](https://make.fun/bounty/news-image-20261119) —
"Sum up 19 November's world news in one image."

![status](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fmake.fun%2Fapi%2Fcompetitions%2Fnews-image-20261119&query=%24.status&label=competition)
![prize](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fmake.fun%2Fapi%2Fcompetitions%2Fnews-image-20261119&query=%24.prize&label=prize)
![deadline](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fmake.fun%2Fapi%2Fcompetitions%2Fnews-image-20261119&query=%24.deadline&label=deadline)

## What's on the page

- **Lead** — Anthropic's record-breaking IPO (story 1)
- **Europe** — Estonia's border shutdown, Prague's media rally, the EU's
  €45bn Ukraine loan and Indonesia trade pact, the Crimean Bridge, UK
  inflation, Ukraine's drone campaign (2–8)
- **Asia-Pacific** — the Shenzhen trilateral, Yongbyon, the Rohingya
  judgment, Cyclone Akvan, Manila's deals (9–18)
- **Middle East** — Gaza, the peace board's warning, Riyadh alerts (19–23)
- **North America** — Speaker Jeffries, the NSA outage, Nvidia, GTA VI,
  the dollar, a record Van Gogh (24–29)
- **South America** — the Venezuela pact and Colombia's C-130 (30–31)
- **Africa** — Badme, Moyale, drought (32–35)
- **Oceania** — General Pants and the Aussie dollar (36–37)
- **Science & World** — Voyager 1, Pew's faith projection, UK cyber
  incidents (38–40)
- **Sport** — Sindhu and Dhoni (41–42)

## How it is built

- `render.py` — the page renderer (Pillow). It measures every headline
  and paragraph with real font metrics and flows the stories down three
  columns, so nothing overlaps and nothing is cut off.
- `entry.png` — the rendered front page, 1024 × 1024.
- `main.py` — the submission entry point. Standard library only: it
  copies the shipped `entry.png` into `$MAKEFUN_OUTPUT_DIR`.
- `sources.txt` — the two outlets behind each of the 42 stories, in
  story order.
