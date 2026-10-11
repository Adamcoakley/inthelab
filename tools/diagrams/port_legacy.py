"""Port an original (dark-only) inthelab diagram to the theme-aware system.

Every hard-coded colour is swapped for a --dg-* token, so the drawing keeps
its look in dark mode and gets a tuned light version for free. The glow
filters are kept; the site switches them off in light mode.

    python3 tools/diagrams/port_legacy.py OLD.svg NEW.svg
"""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dg import TOKENS, TEXT, _style

# old colour -> token
MAP = {
    "#22C7B8": "priv", "#F5A524": "cmp", "#8B7BF0": "net", "#34D399": "ok", "#F2739D": "bad",
    "#3D5170": "edge", "#4A5F7E": "edge", "#2D3D52": "edge2",
    "#5B7290": "mute", "#8FA0BD": "ink2",
    "#0A1220": "well", "#0C1220": "well",
    "#0D1725": "privcard", "#131620": "cmpcard", "#101526": "netcard", "#0D1824": "okcard",   # gradient ends
    "#141E2C": "body", "#182636": "bodytop", "#1B2738": "bodytop", "#223047": "bodytop", "#243347": "bodytop",
    "#161F2D": "bodyside",
    "#0F2B35": "privtint", "#27211D": "cmptint", "#1E213D": "nettint", "#122D31": "oktint",
}
# translucent accent washes -> the matching tint
RGBA = {"245,165,36": "cmptint", "34,199,184": "privtint", "139,123,240": "nettint", "52,211,153": "oktint", "242,115,157": "badtint"}


def token(value):
    v = value.strip()
    if v.upper() in MAP:
        return MAP[v.upper()]
    m = re.match(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)", v)
    if m:
        return RGBA.get(f"{m[1]},{m[2]},{m[3]}")
    return None


def var(tok):
    return f"var(--dg-{tok},{TOKENS[tok][1]})"


def port_tag(tag):
    styles = []
    for attr in ("fill", "stroke", "stop-color"):
        m = re.search(rf'\s{attr}="([^"]+)"', tag)
        if not m:
            continue
        t = token(m[1])
        if t is None:
            if m[1].startswith("#") or m[1].startswith("rgb"):
                raise SystemExit(f"unmapped colour {m[1]}")
            continue
        if tag.startswith("<text") and attr == "fill" and t in TEXT:
            styles.append(f"fill:var(--dg-{t}-text,{TEXT[t][0]})")
        else:
            styles.append(f"{attr}:{var(t)}")
        tag = tag.replace(m[0], "", 1)
    # a dark-filled card with an accent border: tint it in light mode
    fill = next((x for x in styles if x.startswith("fill:var(--dg-well,") or x.startswith("fill:var(--dg-body,")), None)
    stroke = next((x for x in styles if x.startswith("stroke:var(--dg-")), None)
    if fill and stroke:
        acc = stroke.split("--dg-")[1].split(",")[0]
        if acc + "card" in TOKENS:
            tok = acc + ("card" if "--dg-well," in fill else "cardb")
            styles[styles.index(fill)] = f"fill:{var(tok)}"
    if styles:
        if ' style="' in tag:
            tag = tag.replace(' style="', ' style="' + ";".join(styles) + ";", 1)
        else:
            tag = re.sub(r"(/?>)$", f' style="{";".join(styles)}"\\1', tag, count=1)
    return tag


def centre(tag):
    """Rough centre of a shape, to decide which role box it falls in."""
    g = lambda a: (float(re.search(rf'\s{a}="([-\d.]+)"', tag)[1]) if re.search(rf'\s{a}="([-\d.]+)"', tag) else None)
    if tag.startswith("<rect"):
        return g("x") + g("width") / 2, g("y") + g("height") / 2
    if tag.startswith(("<circle", "<ellipse")):
        return g("cx"), g("cy")
    if tag.startswith("<line"):
        return (g("x1") + g("x2")) / 2, (g("y1") + g("y2")) / 2
    if tag.startswith("<text"):
        return g("x"), g("y")
    m = re.search(r'\s(?:d|points)="([^"]+)"', tag)
    if m:
        nums = [float(n) for n in re.findall(r"-?[\d.]+", m[1])]
        xs, ys = nums[0::2], nums[1::2]
        if xs and ys:
            return sum(xs) / len(xs), sum(ys) / len(ys)
    return None


def add_roles(s, roles):
    def tag_role(m):
        tag = m[0]
        if not tag.startswith(("<rect", "<circle", "<ellipse", "<line", "<path", "<polygon", "<polyline", "<text")):
            return tag
        try:
            c = centre(tag)
        except (TypeError, ValueError):
            return tag
        if not c:
            return tag
        for role, (x1, y1, x2, y2) in roles:
            if x1 <= c[0] <= x2 and y1 <= c[1] <= y2:
                return re.sub(r"^<(\w+)", lambda t: f'<{t[1]} class="r-{role}"', tag, count=1)
        return tag
    return re.sub(r"<[a-zA-Z][^<>]*>", tag_role, s)


def port(src, prefix, roles=()):
    s = re.sub(r"<metadata>.*?</metadata>", "", src, flags=re.S)
    # ids must be unique on a page that shows several diagrams
    for i in set(re.findall(r'\sid="([^"]+)"', s)):
        s = s.replace(f'id="{i}"', f'id="{prefix}-{i}"').replace(f"url(#{i})", f"url(#{prefix}-{i})").replace(f'href="#{i}"', f'href="#{prefix}-{i}"')
    s = s.replace(' xmlns:c2pa="http://c2pa.org/manifest"', "")
    s = re.sub(r"<[a-zA-Z][^<>]*>", lambda m: port_tag(m[0]), s)
    if roles:
        s = add_roles(s, roles)
    # root: mark as a theme-aware diagram, keep the original mono labels
    s = re.sub(r"<svg ", '<svg class="dg legacy" ', s, count=1)
    s = s.replace("<style>text{", _style()[:-8] + ".dg.legacy text{", 1)
    return s


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    prefix = re.sub(r"[^a-z0-9]+", "-", os.path.splitext(os.path.basename(dst))[0].lower())
    open(dst, "w").write(port(open(src).read(), prefix))
