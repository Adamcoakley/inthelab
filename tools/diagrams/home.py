"""Home page hero: a server you can't reach, until one route is added.

The page animates it (ids: packet, fail, pass, route-missing, route-added).
Drawn larger and simpler than a lab diagram, because it's seen at a glance.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dg import D

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "public", "images", "home")
LANE = 150   # the height the packet travels along


def hero():
    d = D(520, 300)
    d.labelled("resource/Client", 38, LANE - 28, 48, "you")
    d.group(96, 14, 410, 272, "vpc", "your VPC")
    d.icon("resource/AmazonVPCInternetGateway", 74, LANE - 22, 44)
    d.text(96, LANE + 40, "internet", "sub", 12, "middle", halo=True)
    d.text(96, LANE + 54, "gateway", "sub", 12, "middle", halo=True)
    d.group(150, 52, 340, 220, "public", "Public subnet")
    # the security group and server
    d.group(338, 78, 136, 130, "sg", "web-sg")
    d.text(346, 112, "HTTP from anyone", "sub", 10.5, mono=True)
    d.icon("resource/AmazonEC2Instance", 384, 120, 44)
    d.text(406, 184, "web-1", "ink", 13, "middle", 600)
    d.text(406, 199, "running", "ok", 11.5, "middle", 600)
    # the route table: the one line that changes
    d.rect(160, 200, 172, 60, "net", "nettint", 8, 1.5)
    d.icon("resource/AmazonVPCRouter", 168, 215, 28)
    d.text(204, 222, "route table", "net", 12, weight=600)
    d.raw('<g id="route-missing">')
    d.text(204, 244, "0.0.0.0/0 → ?", "bad", 12.5, weight=600, mono=True)
    d.raw('</g><g id="route-added" opacity="0">')
    d.text(204, 244, "0.0.0.0/0 → igw", "pub", 12.5, weight=600, mono=True)
    d.raw('</g>')
    # the path, and where it stops
    d.path(f"M64 {LANE} L334 {LANE}", "faint", 1.6, "5 5")
    d.raw('<g id="fail" opacity="0">')
    d.bad(150, LANE, 11)
    d.raw('</g><g id="pass" opacity="0">')
    d.ok(338, LANE, 11)
    d.raw('</g>')
    d.raw(f'<circle id="packet" cx="64" cy="{LANE}" r="7" class="f-you" opacity="0"/>')
    d.save(f"{OUT}/hero.svg", "Your server is running, but you can't reach it, until one route is added")


if __name__ == "__main__":
    hero()
    print("home diagram done")
