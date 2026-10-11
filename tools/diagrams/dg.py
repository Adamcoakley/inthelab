"""inthelab diagram library, v2.

One SVG per diagram. Every colour is a CSS class backed by a CSS variable
(--dg-*), so the same file follows the site's light/dark theme when it is
inlined into the page. Each file also carries light-mode fallbacks, so it
still looks right opened on its own.
"""
import math
import os
import re

ICONS = os.environ.get("AWS_ICONS", os.path.join(os.path.dirname(__file__), "aws-icons"))

# ---------------------------------------------------------------- tokens
# name: (meaning, light, dark)
TOKENS = {
    # neutrals
    "ink":       ("strong text, outlines",          "#1F2A37", "#E6EBF5"),
    "ink2":      ("labels",                         "#3E4C5E", "#8FA0BD"),
    "sub":       ("secondary text, captions",       "#5F6B7A", "#9AA7BD"),
    "mute":      ("quiet captions",                 "#6B7A8F", "#5B7290"),
    "faint":     ("inactive, not built yet",        "#A7B1BE", "#44526B"),
    "line":      ("arrows and connectors",          "#475569", "#8FA0BD"),
    "edge":      ("structure: casings, frames",     "#A3B1C2", "#3D5170"),
    "edge2":     ("fine detail inside casings",     "#D3DBE5", "#2D3D52"),
    "surface":   ("neutral cards",                  "#F5F7FA", "#141E2C"),
    "panel":     ("diagram background",             "#FFFFFF", "#0C1220"),
    "well":      ("screens and slots, sunk in",     "#FFFFFF", "#0C1220"),
    "body":      ("front of a 3D object",           "#F5F8FB", "#141E2C"),
    "bodytop":   ("top of a 3D object",             "#E9EEF4", "#1B2738"),
    "bodyside":  ("side of a 3D object",            "#DCE3EB", "#161F2D"),
    # accents. Dark: the original neon palette. Light: re-derived in OKLCH at an
    # even lightness, so no hue shouts or fades; orange is pushed towards red,
    # because a darkened yellow-orange turns brown.
    "net":       ("networking; violet",             "#735ED1", "#8B7BF0"),
    "cmp":       ("compute; orange",                "#D16100", "#F5A524"),
    "priv":      ("private, Region; teal",          "#0A847F", "#22C7B8"),
    "pub":       ("public subnet; green",           "#51850E", "#A3CF4A"),
    "sec":       ("IAM, security services; red",    "#C43E45", "#F25A6E"),
    "db":        ("databases; magenta",             "#A14DA7", "#E05BE6"),
    "you":       ("yours; blue",                    "#396ED6", "#7AA2F7"),
    "ok":        ("allowed, working; green",        "#178950", "#34D399"),
    "bad":       ("blocked, failing; rose",         "#C03D69", "#F2739D"),
    # tints: card fills. In light mode the colour lives in the fill (thin lines
    # on white barely register), so these are clearly tinted, not near-white.
    "nettint":   ("violet fill",                    "#E4E3FF", "#1A1D3A"),
    "cmptint":   ("orange fill",                    "#FFDFC9", "#27211D"),
    "privtint":  ("teal fill",                      "#C4F0EB", "#0F2B35"),
    "pubtint":   ("green fill",                     "#D9EFC5", "#1A2A1E"),
    "sectint":   ("red fill",                       "#FFDDDB", "#2E1A24"),
    "dbtint":    ("magenta fill",                   "#FCD9FD", "#2A1730"),
    "youtint":   ("blue fill",                      "#DAE7FE", "#172446"),
    "oktint":    ("green fill",                     "#CDF0D7", "#122D31"),
    "pubarea":   ("public subnet area",             "#EAF8E0", "#1A2A1E"),
    "privarea":  ("private subnet area",            "#DBF7F4", "#0F2B35"),
    "badtint":   ("rose fill",                      "#FFDCE3", "#2E1A26"),
}

# Phase 0 originals fill their cards with the dark background. In light mode
# that would be plain white, so a card takes its accent's tint instead.
for _acc in ("net", "cmp", "priv", "pub", "sec", "db", "you", "ok", "bad"):
    TOKENS[_acc + "card"] = ("card fill (well)", TOKENS[_acc + "tint"][1], "#0C1220")
    TOKENS[_acc + "cardb"] = ("card fill (body)", TOKENS[_acc + "tint"][1], "#141E2C")

# Light mode only: what a thing *is* decides its colour, so hardware looks like
# hardware. Dark mode keeps the neon schematic look and ignores these roles.
# Each role re-points the --dg-* variables for the shapes that carry it.
_HW = {"body": "#4B5563", "bodytop": "#6B7280", "bodyside": "#374151", "well": "#2F3742",
       "edge": "#1F2937", "edge2": "#59616C", "ink2": "#E5E7EB", "mute": "#D1D5DB"}
ROLES = {
    # servers and racks: solid dark grey, coloured lights and highlights kept
    "srv": {**_HW, "priv": "#1F2937", "priv-text": "#E5E7EB", "privcard": "#2F3742", "privcardb": "#4B5563",
            "privtint": "#2F3742", "cmpcard": "#2F3742", "cmpcardb": "#4B5563", "badcard": "#2F3742",
            "badcardb": "#4B5563", "okcard": "#2F3742"},
    # laptops, phones, printers, TVs: dark grey with a lit screen
    "dev": {**_HW, "bodytop": "#9CA3AF", "well": "#D9E4F2", "edge2": "#6B7280", "cmp": "#1F2937", "bad": "#1F2937",
            "priv": "#1F2937", "cmpcardb": "#4B5563", "badcardb": "#4B5563", "privcardb": "#4B5563",
            "cmpcard": "#D9E4F2", "badcard": "#D9E4F2"},
    # browser windows: a white window in a grey frame
    "win": {"cmp": "#6B7280", "bad": "#6B7280", "priv": "#6B7280", "you": "#6B7280", "cmptint": "#FFFFFF",
            "privtint": "#FFFFFF", "youtint": "#FFFFFF", "cmpcardb": "#FFFFFF", "badcardb": "#FFFFFF", "cmpcard": "#F3F4F6",
            "cmp-text": "#4B5563", "bodytop": "#E5E7EB", "edge": "#9CA3AF", "well": "#F3F4F6"},
    # buildings: concrete, with dark racks inside
    "bld": {"body": "#E7E3DD", "bodytop": "#D3CEC6", "edge": "#8B8378", "priv": "#8B8378", "privcardb": "#E7E3DD",
            "privcard": "#4B5563", "well": "#4B5563", "edge2": "#374151"},
    # a terminal: dark screen, light text
    "term": {"priv": "#1F2937", "privtint": "#1F2937", "priv-text": "#E5E7EB", "faint": "#6B7280"},
    # the internet: blue
    "globe": {"priv": "#2F6FD1", "privcard": "#E3EEFD", "well": "#E3EEFD", "priv-text": "#1E4FA3"},
    # markers that belong to hardware: neutral, not green
    "ntr": {"priv": "#4B5563", "privcard": "#F3F4F6", "priv-text": "#374151", "ok": "#4B5563", "okcard": "#F3F4F6", "ok-text": "#374151"},
}

# In light mode an accent needs a deeper shade for text than for lines,
# or it fails contrast on white. In dark mode one shade does both.
TEXT = {
    "net": ("#5C4AAC", "#8B7BF0"), "cmp": ("#A34202", "#F5A524"), "priv": ("#02736E", "#22C7B8"),
    "pub": ("#456B02", "#A3CF4A"), "sec": ("#A12F35", "#F25A6E"), "db": ("#86398B", "#E05BE6"),
    "you": ("#2B58B1", "#7AA2F7"), "ok": ("#02703F", "#34D399"), "bad": ("#9E2D54", "#F2739D"),
}

FONT = "Inter,'Amazon Ember',Arial,Helvetica,sans-serif"
MONO = "'JetBrains Mono',ui-monospace,Menlo,Consolas,monospace"


def _style():
    rules = [f".dg text{{font-family:{FONT}}}", f".dg .mono{{font-family:{MONO}}}"]
    for name, (_, light, _dark) in TOKENS.items():
        rules.append(f".dg .f-{name}{{fill:var(--dg-{name},{light})}}")
        rules.append(f".dg .s-{name}{{stroke:var(--dg-{name},{light})}}")
    for name, (light, _dark) in TEXT.items():
        rules.append(f".dg text.f-{name}{{fill:var(--dg-{name}-text,{light})}}")
    return "<style>" + "".join(rules) + "</style>"


def site_css():
    """CSS variables for the site: light under :root, dark under [data-theme=dark]."""
    light = ";".join([f"--dg-{k}:{v[1]}" for k, v in TOKENS.items()] + [f"--dg-{k}-text:{v[0]}" for k, v in TEXT.items()])
    dark = ";".join([f"--dg-{k}:{v[2]}" for k, v in TOKENS.items()] + [f"--dg-{k}-text:{v[1]}" for k, v in TEXT.items()])
    roles = "".join(f':root:not([data-theme="dark"]) .dg .r-{r}{{' + ";".join(f"--dg-{k}:{v}" for k, v in m.items()) + "}"
                    for r, m in ROLES.items())
    return (f":root,[data-theme=\"light\"]{{{light};--dg-grid:#EEF2F6;--dg-border:#E3E7EC}}\n"
            f"[data-theme=\"dark\"]{{{dark};--dg-grid:#17233A;--dg-border:#1B2740}}\n"
            f"{roles}\n")


# AWS icon colours -> our classes, so icons follow the theme too
RECOLOR = {
    "#ed7100": "cmp", "#8c4fff": "net", "#7aa116": "pub", "#dd344c": "sec",
    "#c925d1": "db", "#01a88d": "priv", "#00a4a6": "priv",
    "#232f3e": "ink", "#242f3e": "ink", "#232f3d": "ink",
}


TINT = {"net": "nettint", "cmp": "cmptint", "priv": "privtint", "pub": "pubtint", "sec": "sectint",
        "db": "dbtint", "you": "youtint", "ok": "oktint", "bad": "badtint"}

# resource outline icons that read as dated; drawn as the service tile instead
TILES = {
    "resource/AmazonEC2Instance": ("architecture-service/AmazonEC2", 0.8),
    "resource/AmazonEC2Instances": ("architecture-service/AmazonEC2", 0.8),
    "resource/AmazonSimpleStorageServiceBucketWithObjects": ("architecture-service/AmazonSimpleStorageService", 0.8),
}


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class D:
    def __init__(self, w, h):
        self.w, self.h, self.p = w, h, []

    # ------------------------------------------------------------ basics
    def raw(self, s):
        self.p.append(s)

    def text(self, x, y, s, c="ink", size=12, anchor="start", weight=400, mono=False, halo=False):
        # every label is monospace now (the Phase 0 look); former sans labels
        # are drawn a touch smaller because mono runs wider
        if weight >= 600 and size < 12:
            weight = 500   # small labels: medium, not bold; bold is for headings
        if not mono:
            size = round(size * 0.9, 1)
            weight = min(weight, 600)
        cls = f"f-{c} mono"
        h = (' style="paint-order:stroke;stroke:var(--dg-panel,#FFFFFF);stroke-width:4px;stroke-linejoin:round"'
             if halo else "")
        self.raw(f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" font-weight="{weight}" '
                 f'text-anchor="{anchor}"{h}>{esc(s)}</text>')

    def rect(self, x, y, w, h, stroke="line", fill=None, rx=0, sw=1.5, dash=None, glow=False):
        f = f'class="s-{stroke}' + (f' f-{fill}"' if fill else '"')
        d = f' stroke-dasharray="{dash}"' if dash else ""
        nofill = "" if fill else ' fill="none"'
        if stroke is None:
            f = f'class="f-{fill}"'
        g = ' filter="url(#__GLOW__)"' if glow else ""
        self.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" {f}{nofill} stroke-width="{sw}"{d}{g}/>')

    def path(self, d, stroke="line", sw=1.6, dash=None, fill=None):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        cls = f"s-{stroke}" + (f" f-{fill}" if fill else "")
        nofill = "" if fill else ' fill="none"'
        self.raw(f'<path d="{d}" class="{cls}"{nofill} stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"{dd}/>')

    # ------------------------------------------------------------ arrows & marks
    def arrow(self, pts, c="line", dash=None, head=True, sw=1.6):
        d = " ".join(("M" if i == 0 else "L") + f"{a} {b}" for i, (a, b) in enumerate(pts))
        if head:
            (x1, y1), (x2, y2) = pts[-2], pts[-1]
            ang = math.atan2(y2 - y1, x2 - x1)
            # shorten the line so it ends under the head
            sx, sy = x2 - 6 * math.cos(ang), y2 - 6 * math.sin(ang)
            pts2 = pts[:-1] + [(round(sx, 1), round(sy, 1))]
            d = " ".join(("M" if i == 0 else "L") + f"{a} {b}" for i, (a, b) in enumerate(pts2))
        self.path(d, c, sw, dash)
        if head:
            hx, hy = x2 - 10 * math.cos(ang), y2 - 10 * math.sin(ang)
            p = [(x2, y2), (hx + 5 * math.sin(ang), hy - 5 * math.cos(ang)), (hx - 5 * math.sin(ang), hy + 5 * math.cos(ang))]
            self.raw(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in p)}" class="f-{c}"/>')

    def step(self, cx, cy, n):
        self.raw(f'<circle cx="{cx}" cy="{cy}" r="11" class="f-ink"/>')
        self.text(cx, cy + 4.5, n, "panel", 12, "middle", 700)

    def ok(self, cx, cy, r=9):
        self.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" class="f-panel s-ok" stroke-width="1.8"/>')
        self.path(f"M{cx - r * .42} {cy} L{cx - r * .1} {cy + r * .34} L{cx + r * .46} {cy - r * .38}", "ok", 1.9)

    def bad(self, cx, cy, r=9):
        self.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" class="f-panel s-bad" stroke-width="1.8"/>')
        o = r * .58
        self.path(f"M{cx - o} {cy - o} L{cx + o} {cy + o}", "bad", 1.9)

    # ------------------------------------------------------------ icons
    def icon(self, name, x, y, size, keep_colour=False, tint=None):
        if name in TILES:          # use AWS's current service tile instead
            name, k = TILES[name]
            x, y, size = x + size * (1 - k) / 2, y + size * (1 - k) / 2, size * k
        if name.startswith("architecture-service/"):
            keep_colour = True     # service tiles keep AWS's colours in both themes
        src = open(f"{ICONS}/{name}.svg").read()
        vb = re.search(r'viewBox="([^"]+)"', src).group(1)
        inner = re.sub(r"^.*?<svg[^>]*>", "", src, flags=re.S)
        inner = re.sub(r"</svg>\s*$", "", inner)
        inner = re.sub(r"<title>.*?</title>", "", inner)
        if not keep_colour:
            def swap(m):
                cls = RECOLOR.get(m.group(1).lower())
                return f'class="f-{cls}"' if cls else m.group(0)
            inner = re.sub(r'fill="(#[0-9a-fA-F]{6})"', swap, inner)
            if name.startswith("architecture-service/"):   # tile glyph: cut out of the tile
                inner = inner.replace('fill="#fff"', 'class="f-panel"')
        if tint:
            inner = inner.replace('class="f-ink"', f'class="f-{tint}"')
        mx, my, vw, vh = (float(v) for v in vb.split())
        k = size / vw
        self.raw(f'<g transform="translate({x - mx * k:.2f} {y - my * k:.2f}) scale({k:.4f})">{inner}</g>')

    def labelled(self, name, cx, y, size, label, sub=None, sub_mono=True, tint=None, label_c="ink"):
        self.icon(name, cx - size / 2, y, size, tint=tint)
        self.text(cx, y + size + 16, label, label_c, 11.5, "middle", 500)
        if sub:
            self.text(cx, y + size + 30, sub, "sub", 10, "middle", mono=sub_mono)

    # ------------------------------------------------------------ AWS groups
    def group(self, x, y, w, h, kind, label, right=None):
        """kind: cloud | region | vpc | az | public | private | sg | asg"""
        spec = {
            "cloud":   ("ink",  None,       "architecture-group/AWSCloudlogo", None),
            "region":  ("priv", None,       "architecture-group/Region", "6 4"),
            "vpc":     ("net",  None,       "architecture-group/VirtualprivatecloudVPC", None),
            "az":      ("priv", None,       None, "6 4"),
            "public":  ("pub",  "pubarea",  "architecture-group/Publicsubnet", None),
            "private": ("priv", "privarea", "architecture-group/Privatesubnet", None),
            "sg":      ("sub",  None,       None, None),   # neutral: red would read as "blocked"
            "asg":     ("cmp",  None,       "architecture-group/AutoScalinggroup", "6 4"),
        }[kind]
        stroke, fill, ic, dash = spec
        self.rect(x, y, w, h, stroke, fill, 0, 1.5, dash)
        if ic:
            self.icon(ic, x, y, 26, keep_colour=True)
            if kind == "cloud":   # the dark tile needs an edge in dark mode
                self.rect(x, y, 26, 26, "ink", None, 0, 1)
            self.text(x + 34, y + 17, label, "ink", 12, weight=500)
        else:
            self.text(x + 8, y + 15, label, "ink", 10.5 if kind == "sg" else 12, weight=600 if kind == "sg" else 500, mono=kind == "sg")
        if right:
            self.text(x + w - 10, y + 17, right, "sub", 10.5, "end", mono=True, halo=True)

    # ------------------------------------------------------------ custom assets (AWS line style)
    def home_router(self, cx, y, label=None, sub=None):
        """Generic home router in the AWS general-icon line style, 48x48."""
        x = cx - 24
        self.rect(x + 4, y + 22, 40, 16, "ink", None, 3, 2)
        self.path(f"M{x + 14} {y + 22} L{x + 10} {y + 8} M{x + 34} {y + 22} L{x + 38} {y + 8}", "ink", 2)
        for i in range(3):
            self.raw(f'<circle cx="{x + 13 + i * 6}" cy="{y + 30}" r="1.6" class="f-ink"/>')
        self.path(f"M{x + 30} {y + 30} L{x + 38} {y + 30}", "ink", 2)
        if label:
            self.text(cx, y + 64, label, "ink", 11.5, "middle", 500)
        if sub:
            self.text(cx, y + 78, sub, "sub", 10, "middle", mono=True)

    def packet(self, x, y, label=None, c="ink"):
        self.rect(x, y, 30, 20, c, "panel", 3, 1.6)
        self.path(f"M{x} {y + 6} L{x + 30} {y + 6}", c, 1.2)
        if label:
            self.text(x + 15, y + 34, label, "sub", 9.5, "middle", mono=True)

    def firewall_wall(self, x, y1, y2, label="firewall"):
        """A vertical firewall line with the AWS firewall icon on top."""
        self.icon("resource/Firewall", x - 16, y1 - 40, 32)
        self.path(f"M{x} {y1} L{x} {y2}", "sec", 3)
        self.text(x, y2 + 18, label, "sec", 10.5, "middle", 600)

    def server_closeup(self, x, y, w, h, title, sub, rows, ip=None, disk=None, header_icon="resource/AmazonEC2Instance", os_label="Amazon Linux 2023", frame="cmp", os_right="operating system"):
        """The 'opened up' server: header, OS band, processes with ports, network and disk."""
        self.rect(x, y, w, h, frame, TINT.get(frame, "surface"), 8, 1.6, glow=True)
        self.icon(header_icon, x + 10, y + 8, 26)
        self.text(x + 44, y + 21, title, frame, 12, weight=600)
        self.text(x + w - 12, y + 21, sub, "sub", 10.5, "end", mono=True)
        self.rect(x + 10, y + 42, w - 20, 22, "faint", "panel", 3, 1)
        self.text(x + 20, y + 57, os_label, "sub", 10.5)
        self.text(x + w - 20, y + 57, os_right, "sub", 10, "end")
        ry = y + 74
        for proc, port, state in rows:
            col = {"open": "ok", "closed": "faint", "you": "ok", "none": "faint", "bad": "bad"}.get(state, "ink")
            self.rect(x + 10, ry, w - 20, 28, "faint", "panel", 3, 1)
            self.text(x + 20, ry + 18, proc, "ink", 11, mono=True)
            self.rect(x + w - 74, ry + 5, 54, 18, col, None, 9, 1.4)
            self.text(x + w - 47, ry + 18, port, col, 10.5, "middle", 600, mono=True)
            ry += 34
        if ip:
            self.icon("resource/AmazonVPCElasticNetworkInterface", x + 10, y + h - 40, 30) if os.path.exists(
                f"{ICONS}/resource/AmazonVPCElasticNetworkInterface.svg") else None
            self.text(x + 46, y + h - 26, "network card", "sub", 10)
            self.text(x + 46, y + h - 12, ip, "ink", 10.5, mono=True)
        if disk:
            self.icon("resource/AmazonElasticBlockStoreVolume", x + w / 2 + 10, y + h - 40, 30)
            self.text(x + w / 2 + 46, y + h - 26, "disk (EBS)", "sub", 10)
            self.text(x + w / 2 + 46, y + h - 12, disk, "ink", 10.5, mono=True)


    # ------------------------------------------------------------ more custom assets (line style)
    def browser(self, x, y, w=72, h=52, c="ink", label=None, sub=None, url=None):
        self.raw('<g class="r-win">')    # light mode: a plain white window
        self.rect(x, y, w, h, c, TINT.get(c, "panel"), 4, 1.8)
        self.path(f"M{x} {y + 12} L{x + w} {y + 12}", c, 1.4)
        for i in range(3):
            self.raw(f'<circle cx="{x + 7 + i * 6}" cy="{y + 6}" r="1.6" class="f-{c}"/>')
        if url:
            self.rect(x + 26, y + 3, w - 32, 7, c, None, 3.5, 1)
            self.text(x + 26 + (w - 32) / 2, y + 9, url, c, 5.5, "middle", mono=True)
        for i, ww in enumerate((0.7, 0.5, 0.6)):
            self.rect(x + 9, y + 20 + i * 9, round((w - 18) * ww), 2.5, None, "faint", 1.2, 0)
        self.raw('</g>')
        cx = x + w / 2
        if label:
            self.text(cx, y + h + 17, label, "ink", 11.5, "middle", 500)
        if sub:
            self.text(cx, y + h + 31, sub, "sub", 10, "middle", mono=True)

    def building(self, cx, y, w=120, h=96, c="ink"):
        x = cx - w / 2
        self.rect(x, y + 12, w, h - 12, c, "panel", 2, 1.8)
        self.rect(x - 4, y + 6, w + 8, 8, c, "panel", 2, 1.6)
        cols, rows = 4, 2
        for r in range(rows):
            for k in range(cols):
                rx = x + 12 + k * ((w - 24) / cols)
                ry = y + 26 + r * 34
                self.rect(rx, ry, (w - 24) / cols - 8, 26, c, None, 1.5, 1.2)
                self.path(f"M{rx + 4} {ry + 7} L{rx + (w - 24) / cols - 12} {ry + 7}", c, 1)
                self.path(f"M{rx + 4} {ry + 13} L{rx + (w - 24) / cols - 12} {ry + 13}", c, 1)

    def printer(self, cx, y, c="ink", label=None, sub=None):
        x = cx - 24
        self.rect(x + 12, y + 4, 24, 12, c, "panel", 1.5, 1.8)
        self.rect(x + 4, y + 16, 40, 20, c, "panel", 3, 1.8)
        self.rect(x + 12, y + 30, 24, 14, c, "panel", 1.5, 1.6)
        self.raw(f'<circle cx="{x + 38}" cy="{y + 22}" r="1.8" class="f-{c}"/>')
        if label:
            self.text(cx, y + 64, label, "ink", 11.5, "middle", 500)
        if sub:
            self.text(cx, y + 78, sub, "sub", 10, "middle", mono=True)

    def tv(self, cx, y, c="ink", label=None, sub=None):
        x = cx - 26
        self.rect(x, y + 4, 52, 32, c, "panel", 3, 1.8)
        self.path(f"M{x + 18} {y + 44} L{x + 34} {y + 44} M{x + 26} {y + 36} L{x + 26} {y + 44}", c, 1.8)
        if label:
            self.text(cx, y + 64, label, "ink", 11.5, "middle", 500)
        if sub:
            self.text(cx, y + 78, sub, "sub", 10, "middle", mono=True)

    def card(self, x, y, w, h, title, sub=None, c="ink", fill="surface", title_c=None, size=12, align="start", rx=6, sw=1.5):
        self.rect(x, y, w, h, c, fill, rx, sw)
        tx = x + 12 if align == "start" else x + w / 2
        if sub:
            self.text(tx, y + h / 2 - 2, title, title_c or "ink", size, align, 600)
            self.text(tx, y + h / 2 + 13, sub, "sub", 10, align)
        else:
            self.text(tx, y + h / 2 + 4, title, title_c or "ink", size, align, 600)

    def tcard(self, x, y, w, h, title, sub=None, c="you", icon=None, val=None, icon_size=28, rx=8,
              dash=None, glow=False, keep_colour=False, size=12):
        """The Phase 0 card: accent border, tinted fill, title in the accent colour."""
        fill = TINT.get(c, "surface")
        self.rect(x, y, w, h, c, fill, rx, 1.5, dash, glow)
        tx = x + 12
        if icon == "sg-box":       # the security group mark: a plain neutral box
            b = icon_size * 0.85
            self.rect(x + 10 + (icon_size - b) / 2, y + (h - b) / 2, b, b, "sub", None, 3, 1.6)
            tx = x + 18 + icon_size
        elif icon:
            self.icon(icon, x + 10, y + (h - icon_size) / 2, icon_size, keep_colour=keep_colour)
            tx = x + 18 + icon_size
        lines = [l for l in (title, sub, val) if l]
        top = y + h / 2 - (len(lines) - 1) * 7.5 + 4
        self.text(tx, top, title, c if c in TINT else "ink", size, weight=600)
        if sub:
            self.text(tx, top + 15, sub, "sub", 10)
        if val:
            self.text(tx, top + (30 if sub else 15), val, "ink", 10.5, mono=True)

    def numbox(self, x, y, w, h, value, c="ink", fill="panel", size=18):
        self.rect(x, y, w, h, c, fill, 6, 1.6)
        self.text(x + w / 2, y + h / 2 + size * 0.36, value, c, size, "middle", 500, mono=True)

    def pill(self, cx, cy, text, c="ink", w=None, size=10, fill="panel", mono=True):
        w = w or (len(text) * (size * 0.62) + 20)
        self.rect(cx - w / 2, cy - 11, w, 22, c, fill, 11, 1.4)
        self.text(cx, cy + size * 0.36, text, c, size, "middle", 500, mono=mono)

    def bracket(self, x1, x2, y, label=None, sub=None, c="ink"):
        self.path(f"M{x1} {y - 6} L{x1} {y} L{x2} {y} L{x2} {y - 6}", c, 1.4)
        if label:
            self.text((x1 + x2) / 2, y + 18, label, c, 11.5, "middle", 600)
        if sub:
            self.text((x1 + x2) / 2, y + 32, sub, "sub", 10, "middle")

    def table(self, x, y, w, rows, header=None, col=0.5, c="line", row_h=26, fill="panel", mono=True):
        """rows: list of (left, right, colour or None)."""
        n = len(rows) + (1 if header else 0)
        self.rect(x, y, w, row_h * n, c, fill, 6, 1.3)
        cx = x + w * col
        ry = y
        if header:
            self.text(x + 12, ry + 17, header[0], "sub", 10)
            self.text(cx + 12, ry + 17, header[1], "sub", 10)
            ry += row_h
        for i, r in enumerate(rows):
            colour = r[2] if len(r) > 2 and r[2] else "ink"
            if i or header:
                self.path(f"M{x} {ry} L{x + w} {ry}", "faint", 1)
            self.text(x + 12, ry + 17, r[0], colour, 10.5, mono=mono)
            self.text(cx + 12, ry + 17, r[1], colour, 10.5, mono=mono)
            ry += row_h
        self.path(f"M{cx} {y} L{cx} {y + row_h * n}", "faint", 1)

    # ------------------------------------------------------------ output
    def svg(self, title="", uid="dg"):
        t = f"<title>{esc(title)}</title>" if title else ""
        body = "\n".join(self.p)
        defs = ""
        if "__GLOW__" in body:   # soft glow; the site turns it off in light mode
            gid = f"{uid}-glow"
            body = body.replace("__GLOW__", gid)
            defs = (f'<defs><filter id="{gid}" x="-20%" y="-40%" width="140%" height="180%">'
                    '<feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/>'
                    '<feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" class="dg" viewBox="0 0 {self.w} {self.h}">'
                f"{t}{_style()}{defs}\n" + body + "\n</svg>")

    def save(self, path, title=""):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        uid = re.sub(r"[^a-z0-9]+", "-", os.path.splitext(os.path.basename(path))[0].lower())
        open(path, "w").write(self.svg(title, uid))
