"""Phase 0 diagrams: the original hand-drawn set, ported to the theme tokens.

The sources live in legacy/ (dark-only originals). This script swaps their
colours for --dg-* tokens (see port_legacy.py), applies a few layout fixes,
and writes them to public/images/labs/ under the same names.
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from port_legacy import port

OUT = os.path.join(HERE, "..", "..", "public", "images", "labs")

# small fixes to the originals: (old, new), each must match exactly once
FIXES = {
    "00-01/capacity-vs-demand.svg": [
        ('<text x="300" y="48"', '<text x="300" y="152"'),      # "what you actually need" sits under the curve
        ('<text x="72" y="80"', '<text x="72" y="54"'),         # "what you bought" sits above the dashed line
        ('<text x="150" y="130"', '<text x="96" y="112"'),      # left "wasted" clear of the curve
    ],
    "00-04/local-vs-remote.svg": [
        ('<text x="390" y="210"',                               # mask the boundary behind the gateway label
         '<rect x="342" y="200" width="96" height="29" rx="3" style="fill:var(--dg-panel,#FFFFFF)"/><text x="390" y="210"'),
    ],
}

# light-mode roles: (role, box) - any shape whose centre falls in the box takes the role
# srv server/rack, dev laptop/phone/printer/TV, win browser window, bld building,
# globe the internet, ntr a neutral marker. Dark mode ignores all of this.
ROLES = {
    "00-01/server-anatomy.svg": [("srv", (60, 25, 246, 262))],
    "00-01/virtualisation.svg": [("srv", (98, 25, 192, 142)), ("srv", (275, 25, 367, 142)),
                                 ("srv", (452, 25, 546, 142)), ("srv", (275, 285, 367, 392))],
    "00-01/regions-azs.svg": [("bld", (60, 50, 262, 242)), ("bld", (360, 50, 562, 242))],
    "00-02/dns-lookup.svg": [("win", (50, 140, 192, 250)), ("srv", (425, 110, 546, 256))],
    "00-02/home-network.svg": [("dev", (60, 40, 160, 100)), ("dev", (486, 36, 534, 116)),
                               ("dev", (66, 248, 154, 328)), ("dev", (452, 250, 568, 334))],
    "00-02/ports.svg": [("srv", (60, 25, 246, 262))],
    "00-02/private-public-ip.svg": [("dev", (66, 66, 152, 120)), ("dev", (66, 220, 152, 274)),
                                    ("srv", (425, 95, 546, 236))],
    "00-02/protocol-stack.svg": [("win", (14, 68, 138, 162)), ("srv", (494, 50, 600, 176))],
    "00-02/request-journey.svg": [("win", (24, 54, 112, 126)), ("globe", (276, 54, 348, 126)),
                                  ("srv", (404, 30, 464, 128)), ("srv", (518, 40, 602, 128)),
                                  ("globe", (296, 134, 328, 166)), ("ntr", (418, 134, 450, 166)), ("ntr", (540, 134, 572, 166))],
    "00-02/tcp-vs-udp.svg": [("dev", (8, 70, 72, 112)), ("dev", (8, 232, 72, 274)),
                             ("srv", (430, 50, 502, 124)), ("srv", (430, 212, 502, 286))],
    "00-04/hop-by-hop.svg": [("dev", (16, 70, 102, 126)), ("srv", (534, 67, 598, 141))],
    "00-04/local-vs-remote.svg": [("dev", (54, 74, 138, 128)), ("dev", (58, 208, 142, 280)), ("srv", (516, 136, 580, 210))],
    "00-05/firewall-gate.svg": [("win", (34, 48, 122, 112)), ("dev", (26, 170, 132, 232)), ("srv", (488, 100, 552, 174))],
    "00-05/inbound-outbound.svg": [("win", (34, 46, 122, 110)), ("srv", (278, 42, 342, 116))],
    "00-05/least-privilege.svg": [("globe", (48, 60, 120, 132)), ("dev", (30, 192, 138, 254))],
    "00-05/phase-0-mental-model.svg": [("win", (14, 46, 106, 110)), ("srv", (588, 30, 652, 122)), ("ntr", (604, 126, 636, 158))],
}

if __name__ == "__main__":
    n = 0
    for src in sorted(glob.glob(os.path.join(HERE, "legacy", "*", "*.svg"))):
        rel = os.path.relpath(src, os.path.join(HERE, "legacy"))
        prefix = os.path.splitext(os.path.basename(rel))[0]
        s = port(open(src).read(), prefix, ROLES.get(rel, ()))
        for old, new in FIXES.get(rel, []):
            assert s.count(old) == 1, (rel, old)
            s = s.replace(old, new)
        dst = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "w").write(s)
        n += 1
    print(n, "phase 0 diagrams")
