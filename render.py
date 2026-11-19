#!/usr/bin/env python3
"""The Meridian Gazette - one-page world news sheet, Thursday 19 November 2026.

Renders entry.png (1024x1024) with Pillow: masthead, red date band, a lead
story beside a dot-grid world map and a day-in-numbers box, then a three
column river of 41 further stories grouped by region, a ticker and a
sources line. All layout is measured with real text metrics so nothing
overlaps: stories flow down column one, then two, then three.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (253, 252, 247)
INK = (20, 20, 20)
RED = (179, 0, 27)
GREY = (92, 92, 92)
FAINT = (201, 196, 184)
DARK = (22, 22, 22)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
HEAD_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, width):
    """Greedy word wrap returning a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- stories
# (number, headline, body) - grouped in reading order.
LEAD = (
    1,
    "Anthropic's $81.3bn float is the biggest IPO in history",
    "The AI lab priced its debut at $83 a share, above guidance, selling 980 "
    "million shares and valuing the company above $1.5 trillion fully diluted. "
    "It tops the record set by SpaceX in June. Revenue hit $17.0bn in the third "
    "quarter, up twelvefold in a year, and trading starts today on Nasdaq "
    "under the ticker ANT.",
)

GROUPS = [
    ("EUROPE", [
        (2, "Estonia to shut every Russian border crossing",
         "Narva, Luhamaa and Koidula shut from 1 December after a foiled "
         "GRU arson attack; eight men detained."),
        (3, "Huge Prague rally defends public media",
         "Hundreds of thousands marched Sunday against state funding of "
         "media, fearing political control of broadcasters."),
        (4, "EU plans \u20ac45bn loan to keep Ukraine funded",
         "The 2027 loan covers two-thirds of Kyiv's \u20ac70bn gap, repaid "
         "only when Russia pays reparations."),
        (5, "EU clears trade pact with Indonesia",
         "It frees 98.5% of tariff lines, scraps most Indonesian duties in "
         "five years and saves \u20ac600m a year."),
        (6, "Crimean Bridge hit for third time in a week",
         "Traffic halted again as damage is assessed on the bridge linking "
         "occupied Crimea to mainland Russia."),
        (7, "UK inflation climbs to 3.6% on fuel costs",
         "Fuel jumped 33.2% in a year, diesel hit a record 199.5p a litre "
         "and bills may rise \u00a3443 from January."),
        (8, "Ukraine's drones halve Russian oil refining",
         "Long-range strikes cut Russian refining output by nearly half in "
         "20 days, squeezing winter fuel supplies."),
    ]),
    ("ASIA-PACIFIC", [
        (9, "Trump, Xi and Putin meet at APEC in Shenzhen",
         "Their first joint meeting came at the APEC summit, where Xi "
         "hosts leaders of 21 Pacific economies."),
        (10, "North Korea expands uranium plant, IAEA says",
         "The Yongbyon enrichment hall grew from September, satellites "
         "show. Inspectors are barred since 2009."),
        (11, "World court to rule on Rohingya genocide case",
         "The Gambia accuses Myanmar over the 2017 crackdown that drove "
         "700,000 Rohingya into Bangladesh."),
        (12, "India and Japan deepen defence ties in Tokyo",
         "Rajnath Singh and S. Jaishankar held 2+2 defence and security "
         "talks with Japan in Tokyo."),
        (13, "Cyclone Akvan bears down on India's east coast",
         "Landfall is due Friday noon near Visakhapatnam; winds 120-130 "
         "km/h, gusts 145. Odisha is on orange alert."),
        (14, "US lines up $2bn military loan for Philippines",
         "The package includes $400m for long-range fires, command systems "
         "and drones for the South China Sea."),
        (15, "Philippine Airlines in $12bn Boeing deal",
         "Up to 20 Boeing 787s with GE engines anchor the $17bn of deals "
         "unveiled during Trump's Manila state visit."),
        (16, "North Korea fires missiles after allied drill",
         "Ballistic missiles splashed into the sea hours after a "
         "US-South Korea-Japan drill ended."),
        (17, "Delhi schools reopen as smog curbs are lifted",
         "Stage III smog curbs were revoked as the air index eased to "
         "204, ending hybrid lessons in Delhi-NCR."),
        (18, "Trump wraps Asia tour with $17bn in deals",
         "Packages with Manila, Bangkok and Jakarta span jets, energy "
         "and tech, plus a US trade-deficit pledge."),
    ]),
    ("MIDDLE EAST", [
        (19, "Israeli armour pushes past Gaza's Yellow Line",
         "Tanks razed a Hamas tunnel in central Gaza, the first ground "
         "move since the 2025 truce. Hamas protests."),
        (20, "Israel says two Hamas commanders killed",
         "The IDF named platoon commanders Tabasi and Nabhan; three more "
         "Palestinians died in drone strikes."),
        (21, "Peace board: both sides failing Gaza deal",
         "A 12-page UN report warns the truce may collapse; Gaza's new "
         "administration has not yet taken office."),
        (22, "Saudi Arabia: danger passed after Riyadh alerts",
         "Civil Defence warned residents, then said the danger had "
         "passed. Alerts also sounded in the south."),
        (23, "Houthi drones target Saudi oil pipeline",
         "Five drones flew at two pumping stations on the East-West "
         "pipeline, the kingdom's Hormuz bypass artery."),
    ]),
    ("NORTH AMERICA", [
        (24, "Jeffries nominated to lead the House",
         "Democrats picked Hakeem Jeffries, set to become the first "
         "African-American Speaker of the House."),
        (25, "Outage knocks out NSA's secret network",
         "A classified systems failure disrupted intelligence work, "
         "including links tied to the Middle East."),
        (26, "Nvidia halts H200 chip sales to China",
         "Interim chief Colette Kress ends the export deal struck under "
         "ousted CEO Jensen Huang, levy and all."),
        (27, "GTA VI finally lands after 13-year wait",
         "Queues formed from Sydney to Los Angeles for the crime saga, "
         "billed at over $1 billion to produce."),
        (28, "Dollar hovers near a 19-month high",
         "Hawkish Fed minutes lifted the greenback, with one governor "
         "urging a 50-point December rate hike."),
        (29, "Van Gogh canvas sets $190.4m auction record",
         "Blossoming Chestnut Trees sold at Sotheby's after a Nazi-era "
         "claim by a publisher's heirs was settled."),
    ]),
    ("SOUTH AMERICA", [
        (30, "US signs military pact with Venezuela",
         "Hegseth agreed joint training and intelligence sharing in "
         "Caracas, ten months after Maduro fell."),
        (31, "Hegseth hands Colombia a C-130 Hercules",
         "The transport plane anchors new US support against armed "
         "groups, on the second leg of his regional tour."),
    ]),
    ("AFRICA", [
        (32, "Ethiopian and Eritrean forces mass at Badme",
         "Artillery fire and drone strikes have flared for a week around "
         "the town that sparked the 1998-2000 border war."),
        (33, "50,000 flee Moyale fighting into Kenya",
         "Four weeks of Oromo-Somali clashes emptied the border town; "
         "truck drivers are stranded at the crossing."),
        (34, "EU sends \u20ac550,000 for Moyale displaced",
         "Emergency funds flow via UNHCR Kenya and the Red Cross to "
         "families who fled across the border in October."),
        (35, "Drought tightens its grip on the Horn",
         "Somalia has declared a drought emergency; five million people "
         "there and 3.5 million in Kenya need food aid."),
    ]),
    ("OCEANIA", [
        (36, "General Pants collapses, 500 jobs at risk",
         "The Sydney fashion chain, founded in 1972, is in administration. "
         "Its 35 stores keep trading for now."),
        (37, "Aussie dollar sinks to a 10-month low",
         "Soft jobs data pushed it to US$0.6692, the weakest since "
         "January, as the greenback dominated markets."),
    ]),
    ("SCIENCE & WORLD", [
        (38, "Voyager 1 reaches one light-day from Earth",
         "The 1977 probe is 25.9 billion km out, so its signals take a "
         "full day to reach home. NASA marks it today."),
        (39, "Islam set to be largest faith by 2035 - Pew",
         "Pew's study of India's changing faiths projects Islam passing "
         "Christianity as the largest religion."),
        (40, "Cyber attacks on UK finance near record",
         "Firms reported 38 incidents to the FCA in October, the "
         "second-worst month in five years."),
    ]),
    ("SPORT", [
        (41, "Sindhu storms back into world top five",
         "No. 5 with 74,421 points, her first top-five ranking since "
         "2022, and bound for the World Tour Finals."),
        (42, "Dhoni retires from the IPL after 19 seasons",
         "Chennai Super Kings announced their captain's farewell; he "
         "stays on as a mentor for the 2027 season."),
    ]),
]

NUMBERS = [
    ("$81.3bn", "raised by Anthropic, the largest IPO ever"),
    ("\u20ac45bn", "EU loan proposed to fund Ukraine in 2027"),
    ("50,000", "people fled Moyale fighting into Kenya"),
    ("25.9bn km", "Voyager 1's distance: one light-day"),
    ("$190.4m", "record auction price for a Van Gogh"),
    ("3.6%", "UK inflation, a one-year high"),
    ("98.5%", "of EU-Indonesia tariff lines freed"),
    ("145 km/h", "peak gusts of Cyclone Akvan"),
]

TICKER = ("GTA VI queues snake around blocks  +++  Prague marches for public "
          "media  +++  Voyager 1 phones home from one light-day away  +++  "
          "Dhoni bows out of the IPL")

SOURCES = ("Two sources per story, in story order: Al Jazeera & Reuters \u00b7 France 24 & Moscow Times \u00b7 "
           "France 24 & Munich Eye \u00b7 FT & EU Commission \u00b7 Reuters & EU Council \u00b7 BBC & Kyiv reports \u00b7 "
           "BBC & ONS \u00b7 Ukrainska Pravda & Munich Eye \u00b7 Reuters & BBC \u00b7 Reuters & France 24 \u00b7 "
           "Reuters & HRW \u00b7 Times of India & Careerindia \u00b7 IMD & Odisha reports \u00b7 White House & PNA \u00b7 "
           "White House & TradingView \u00b7 Munich Eye & Jagran \u00b7 Tribune & Times of India \u00b7 White House & KuCoin \u00b7 "
           "NBC & BBC \u00b7 IDF & AFP \u00b7 Reuters & The National \u00b7 Reuters & Saudi Civil Defence \u00b7 "
           "Reuters & AppiSToS \u00b7 BBC & Reuters \u00b7 CNN & NewsMediaHouse \u00b7 Reuters & BBC \u00b7 Reuters & BBC \u00b7 "
           "Reuters & Global Banking \u00b7 BBC & Artnet \u00b7 Reuters & TBS \u00b7 Reuters & Particle \u00b7 Reuters & ACLED \u00b7 "
           "Al Jazeera & People Daily \u00b7 EU Commission & People Daily \u00b7 FEWS NET & UN OCHA \u00b7 AAP & The Guardian \u00b7 "
           "Reuters & Global Banking \u00b7 NASA & Nature \u00b7 BBC & NDTV \u00b7 Reuters & FCA \u00b7 The Hindu & MyKhel \u00b7 "
           "CSK & Careerindia. Full citations in sources.txt.")

# Dot map: rows of land cells on a rough equirectangular grid,
# 62 columns (longitude -180..180) by 22 rows (latitude ~80..-63).
LAND = [
    "            xxxxx       xxx       x      xxxx     xxxxx       ",
    "  xxxxxxxxxxxxxx       xxxx        xxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "  xxxxxxxxxxxxxxxx      xxx       xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "   xxxxxxxxxxxxxxx                x xxxxxxxxxxxxxxxxxxxxxxxxxx",
    "    xxxxxxxxxxxxx            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx ",
    "     xxxxxxxxxxx                   xxxxxxxxxxxxxxxxxxxxxxxxx  ",
    "     xxxxxxxxxxx                    xxxxxxxxxxxxxxxxxxxxxxxx  ",
    "      xxxxxxxxx                      xxxxxxxxxxxxxxxxxxxxxxx  ",
    "       xxxxxxx                      xxxxxxxxxxxxxxxxxxxxxxx   ",
    "        xxxxx                        xxxxxxxxxxxxxxxxxx       ",
    "         xxx                          xxxxxxxxxxxxxxxxx       ",
    "         xxxx                          xxxxxxxxxxxxxxx        ",
    "         xxxxxx                         xxxxxxxxxxxxx         ",
    "          xxxxxx                         xxxxxxxxxxx          ",
    "          xxxxx                           xxxxxxx  xxxxxx     ",
    "           xxxx                           xxxxxx  x xxxxx     ",
    "           xxx                            xxxxx        xxxxx  ",
    "           xxx                             xxx         xxxx  x",
    "           xx                                                x",
    "           xx                                                 ",
    "           x                                                  ",
    "                                                              ",
]

# Marker positions as fractions of the map box (story number: (fx, fy)),
# projected from each story's longitude/latitude, nudged apart in clusters.
MARKERS = {
    1: (0.150, 0.282), 2: (0.566, 0.144), 3: (0.540, 0.228), 4: (0.512, 0.212),
    5: (0.794, 0.598), 6: (0.602, 0.250), 7: (0.490, 0.184), 8: (0.586, 0.216),
    9: (0.814, 0.398), 10: (0.842, 0.268), 11: (0.764, 0.402), 12: (0.890, 0.308),
    13: (0.752, 0.456), 14: (0.834, 0.454), 15: (0.858, 0.470), 16: (0.864, 0.294),
    17: (0.710, 0.356), 18: (0.818, 0.486), 19: (0.586, 0.326), 20: (0.608, 0.348),
    21: (0.630, 0.384), 22: (0.630, 0.444), 23: (0.308, 0.266), 24: (0.280, 0.298),
    25: (0.264, 0.270), 26: (0.168, 0.312), 27: (0.180, 0.330), 28: (0.318, 0.290),
    29: (0.292, 0.240), 30: (0.314, 0.486), 31: (0.294, 0.527), 32: (0.594, 0.476),
    33: (0.606, 0.534), 34: (0.598, 0.566), 35: (0.634, 0.508), 36: (0.926, 0.788),
    37: (0.908, 0.812), 38: (0.975, 0.045), 39: (0.700, 0.416), 40: (0.472, 0.226),
    41: (0.720, 0.440), 42: (0.718, 0.472),
}


def draw_map(draw, x0, y0, w, h):
    rows, cols = len(LAND), max(len(r) for r in LAND)
    cw, ch = w / cols, h / rows
    r = max(1.1, min(cw, ch) * 0.40)
    for ri, row in enumerate(LAND):
        for ci, cell in enumerate(row):
            if cell == "x":
                cx, cy = x0 + (ci + 0.5) * cw, y0 + (ri + 0.5) * ch
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 178, 190))
    mf = F(SANS_B, 7)
    for num, (fx, fy) in MARKERS.items():
        cx, cy = x0 + fx * w, y0 + fy * h
        rad = 6 if num < 10 else 7
        draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=RED)
        t = str(num)
        tw = draw.textlength(t, font=mf)
        draw.text((cx - tw / 2, cy - 4.5), t, font=mf, fill=(255, 255, 255))


def story_block(draw, x, y, width, num, headline, body, fonts):
    """Draw one numbered story; return its height."""
    hf, bf, nf = fonts
    nlabel = f"{num:02d}"
    nw = draw.textlength(nlabel, font=nf) + 5
    draw.text((x, y + 1), nlabel, font=nf, fill=RED)
    hsize = 12
    while hsize > 10 and draw.textlength(headline, font=F(HEAD_B, hsize)) > width - nw:
        hsize -= 1
    hfont = F(HEAD_B, hsize)
    hlines = wrap(draw, headline, hfont, width - nw)
    cy = y
    for i, line in enumerate(hlines):
        draw.text((x + nw, cy), line, font=hfont, fill=INK)
        cy += 13.5
    blines = wrap(draw, body, bf, width)
    for line in blines:
        draw.text((x, cy + 1), line, font=bf, fill=(45, 45, 45))
        cy += 11.2
    return cy - y + 3.5


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 22                      # page margin
    CW = W - 2 * M              # content width

    # ---- masthead ------------------------------------------------------
    d.line([M, 10, W - M, 10], fill=INK, width=2)
    d.text((M, 14), "Vol. I - No. 323", font=F(SANS, 9), fill=GREY)
    right = "Price: one minute of your day"
    d.text((W - M - d.textlength(right, font=F(SANS, 9)), 14), right,
           font=F(SANS, 9), fill=GREY)
    name = "THE MERIDIAN GAZETTE"
    nf = F(SERIF_B, 41)
    d.text(((W - d.textlength(name, font=nf)) / 2, 24), name, font=nf, fill=INK)
    tag = "ONE PAGE - THE WHOLE WORLD - EVERY MORNING"
    tf = F(SANS_B, 10)
    d.text(((W - d.textlength(tag, font=tf)) / 2, 68), tag, font=tf, fill=RED)
    d.line([M, 82, W - M, 82], fill=INK, width=2)

    # ---- red date band --------------------------------------------------
    by = 88
    d.rectangle([M, by, W - M, by + 25], fill=RED)
    bf = F(SANS_B, 13)
    d.text((M + 10, by + 5), "THURSDAY 19 NOVEMBER 2026", font=bf, fill=(255, 255, 255))
    right = "42 STORIES \u00b7 6 CONTINENTS"
    d.text((W - M - 10 - d.textlength(right, font=bf), by + 5), right,
           font=bf, fill=(255, 255, 255))

    # ---- lead band -------------------------------------------------------
    ly = by + 34
    lead_w = 566
    d.text((M, ly), "THE LEAD \u00b7 ARTIFICIAL INTELLIGENCE", font=F(SANS_B, 11), fill=RED)
    num, head, body = LEAD
    lhf = F(HEAD_B, 25)
    cy = ly + 17
    for line in wrap(d, head, lhf, lead_w):
        d.text((M, cy), line, font=lhf, fill=INK)
        cy += 29
    lbf = F(SANS, 12)
    cy += 3
    for line in wrap(d, body, lbf, lead_w):
        d.text((M, cy), line, font=lbf, fill=(40, 40, 40))
        cy += 15.5
    lead_bottom = cy

    # right column: map then numbers
    rx, rw = M + lead_w + 26, CW - lead_w - 26
    d.text((rx, ly), "THE WORLD TODAY - STORY MARKERS", font=F(SANS_B, 11), fill=RED)
    map_y, map_h = ly + 15, 94
    draw_map(d, rx, map_y, rw, map_h)
    ny = map_y + map_h + 6
    d.text((rx, ny), "THE DAY IN NUMBERS", font=F(SANS_B, 11), fill=RED)
    ny += 14
    colw = (rw - 10) / 2
    fig_f, lab_f = F(SANS_B, 14), F(SANS, 8)
    for i, (fig, lab) in enumerate(NUMBERS):
        cx = rx + (i % 2) * (colw + 10)
        cyy = ny + (i // 2) * 21.5
        d.text((cx, cyy), fig, font=fig_f, fill=RED)
        fw = d.textlength(fig, font=fig_f) + 5
        for j, line in enumerate(wrap(d, lab, lab_f, colw - fw)):
            d.text((cx + fw, cyy + 1 + j * 9), line, font=lab_f, fill=(50, 50, 50))
    right_bottom = ny + 4 * 21.5

    band_bottom = max(lead_bottom, right_bottom) + 8
    d.line([M, band_bottom, W - M, band_bottom], fill=FAINT, width=1)

    # ---- story river ------------------------------------------------------
    # Flatten groups into items, measure everything, then flow the items
    # down three columns against an even share of the total height, so the
    # columns balance instead of the last one overflowing.
    river_top = band_bottom + 8
    river_bottom = H - 54
    col_w = (CW - 2 * 16) / 3
    fonts = (F(HEAD_B, 12), F(SANS, 10), F(SANS_B, 10))
    scratch = ImageDraw.Draw(img)
    items = []  # (kind, payload, height)
    for gname, stories in GROUPS:
        items.append(("header", gname, 17))
        for story in stories:
            items.append(("story", story,
                          story_height(scratch, col_w, *story, fonts)))
    total = sum(h for _, _, h in items)
    share = total / 3
    hf = F(SANS_B, 10)
    col = 0
    x = M
    y = river_top
    limit = river_top + share
    for i, (kind, payload, hh) in enumerate(items):
        need = hh
        if kind == "header" and i + 1 < len(items):
            need += items[i + 1][2]  # a header travels with its first story
        if col < 2 and y + need > min(limit, river_bottom):
            col += 1
            x = M + col * (col_w + 16)
            y = river_top
            limit += share
        if kind == "header":
            tw = d.textlength(payload, font=hf)
            d.rectangle([x, y, x + tw + 12, y + 14], fill=RED)
            d.text((x + 6, y + 2), payload, font=hf, fill=(255, 255, 255))
            d.line([x + tw + 12, y + 6.5, x + col_w, y + 6.5], fill=FAINT, width=1)
            y += hh
        else:
            y += story_block(d, x, y, col_w, *payload, fonts)
    print("river finished: col", col, "y", round(y), "of", river_bottom,
          "| total", round(total), "share", round(share))

    # ---- footer ------------------------------------------------------------
    sy = H - 54
    sf = F(SANS, 7)
    for i, line in enumerate(wrap(d, SOURCES, sf, CW)):
        d.text((M, sy + i * 8.5), line, font=sf, fill=GREY)
    ty = H - 24
    d.rectangle([0, ty, W, H], fill=DARK)
    tick_f = F(SANS_B, 10.5)
    while d.textlength(TICKER, font=tick_f) > CW and tick_f.size > 8:
        tick_f = F(SANS_B, tick_f.size - 0.5)
    d.text((M, ty + 5), TICKER, font=tick_f, fill=(255, 255, 255))

    img.save("entry.png", optimize=True)
    print("saved entry.png")


def story_height(draw, width, num, headline, body, fonts):
    hf, bf, nf = fonts
    nw = draw.textlength(f"{num:02d}", font=nf) + 5
    hsize = 12
    while hsize > 10 and draw.textlength(headline, font=F(HEAD_B, hsize)) > width - nw:
        hsize -= 1
    hfont = F(HEAD_B, hsize)
    h = 13.5 * len(wrap(draw, headline, hfont, width - nw))
    h += 11.2 * len(wrap(draw, body, bf, width))
    return h + 3.5


if __name__ == "__main__":
    main()
