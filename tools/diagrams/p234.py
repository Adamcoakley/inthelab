"""Phase 2, 3 and 4 diagrams in the v2 system. Same file names as before."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dg import D

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "public", "images", "labs")
EC2 = "resource/AmazonEC2Instance"
LAPTOP = "resource/Client"


def save(d, path, title):
    d.save(f"{OUT}/{path}", title)


# =============================================================== shared pieces
def route_note(d, x, y, last=None, last_c="pub"):
    d.icon("resource/AmazonVPCRouter", x, y, 30)
    d.text(x + 38, y + 11, "route table", "sub", 10.5, weight=500)
    d.text(x + 38, y + 26, "10.0.0.0/16 → local", "ink", 10.5, mono=True)
    if last:
        d.text(x + 38, y + 40, last, last_c, 10.5, mono=True)


def instance(d, x0, y0, name, ip, sg=None, rules=(), w=136, rule_c="sec"):
    """EC2 instance, optionally inside a security group box with its rules listed."""
    h = 104 + 13 * len(rules) + (16 if sg else 0)
    top = y0
    if sg:
        d.group(x0, y0, w, h, "sg", sg)
        for i, (r, c) in enumerate(rules):
            d.text(x0 + 8, y0 + 29 + i * 13, r, c or rule_c, 9.5)
        top = y0 + 16 + 13 * len(rules)
    d.icon(EC2, x0 + w / 2 - 22, top + 14, 44)
    d.text(x0 + w / 2, top + 74, name, "ink", 11.5, "middle", 500)
    d.text(x0 + w / 2, top + 88, ip, "sub", 10, "middle", mono=True)
    return h


def one_subnet(d, *, subnet_label="Public subnet: public-a", route=None, route_c="pub", server=True,
               sg="web-sg", rules=(), igw=True):
    """Region > VPC > one subnet, internet gateway on the VPC edge. Canvas 660 x 330."""
    d.labelled(LAPTOP, 46, 118, 48, "your laptop", "your IP")
    d.group(100, 10, 548, 310, "region", "Europe (Ireland) eu-west-1")
    d.group(128, 46, 506, 260, "vpc", "your VPC", "10.0.0.0/16")
    if igw:
        d.icon("resource/AmazonVPCInternetGateway", 106, 128, 44)
        d.text(128, 186, "internet", "sub", 10, "middle")
        d.text(128, 198, "gateway", "sub", 10, "middle")
    d.group(196, 76, 424, 216, "public", subnet_label, "10.0.1.0/24")
    route_note(d, 212, 236, route, route_c)
    if server:
        instance(d, 470, 96, "web-1", "10.0.1.23", sg, rules)
    else:
        d.text(538, 160, "no servers yet", "faint", 11, "middle", 500)


# =============================================================== Phase 2
def vpc_in_region():
    d = D(660, 300)
    d.group(16, 10, 628, 280, "region", "Europe (Ireland) eu-west-1")
    d.group(34, 46, 592, 226, "vpc", "your VPC", "10.0.0.0/16")
    for i, az in enumerate(("eu-west-1a", "eu-west-1b", "eu-west-1c")):
        x = 52 + i * 192
        d.group(x, 80, 172, 84, "az", az)
        d.text(x + 86, 132, "empty", "faint", 11, "middle", 500)
    d.text(52, 192, "created for you with the VPC:", "ink", 11, weight=500)
    items = [("resource/AmazonVPCRouter", "main route table"), ("resource/AmazonVPCNetworkAccessControlList", "network ACL"), (None, "security group")]
    for i, (ic, t) in enumerate(items):
        x = 52 + i * 192
        d.rect(x, 206, 172, 46, "faint", "surface", 6, 1.2)
        if ic:
            d.icon(ic, x + 10, 213, 32)
        else:
            d.rect(x + 14, 217, 24, 24, "sec", None, 2, 1.6)
        d.text(x + 52, 234, t, "ink", 11.5, weight=500)
    save(d, "02-01/vpc-in-region.svg", "Your VPC inside eu-west-1, spanning three empty Availability Zones, with the three things created alongside it")


def subnet_plan():
    d = D(660, 310)
    d.group(16, 10, 628, 290, "vpc", "your VPC", "10.0.0.0/16")
    cols = (("eu-west-1a", [("public-a", "10.0.1.0/24", None), ("private-a", "10.0.2.0/24", "phase 4")]),
            ("eu-west-1b", [("public-b", "10.0.3.0/24", "phase 6"), ("private-b", "10.0.4.0/24", "phase 6")]))
    for i, (az, subs) in enumerate(cols):
        x = 34 + i * 304
        d.group(x, 46, 288, 238, "az", az)
        for j, (name, cidr, when) in enumerate(subs):
            y = 78 + j * 102
            if when is None:
                d.group(x + 16, y, 256, 88, "public", f"Public subnet: {name}", cidr)
                d.text(x + 28, y + 64, "you build this now", "you", 11, weight=600)
            else:
                d.rect(x + 16, y, 256, 88, "faint", None, 0, 1.3, "5 4")
                d.text(x + 28, y + 22, name, "faint", 11.5, weight=500)
                d.text(x + 262, y + 22, cidr, "faint", 10.5, "end", mono=True)
                d.text(x + 28, y + 64, when, "faint", 11)
    save(d, "02-02/subnet-plan.svg", "Four subnets across two Availability Zones. public-a is built now; the rest come later")


def reserved_addresses():
    d = D(660, 220)
    d.text(30, 26, "10.0.1.0/24: 256 addresses", "ink", 11.5, weight=500, mono=True)
    y, h = 40, 42
    xs = []
    x = 30
    for t in (".0", ".1", ".2", ".3"):
        c = "net" if t == ".1" else "ink"
        d.numbox(x, y, 44, h, t, c, "nettint" if t == ".1" else "surface", 12)
        xs.append(x + 22)
        x += 48
    d.rect(x, y, 330, h, "you", "youtint", 6, 1.6)
    d.text(x + 165, y + 18, ".4 to .254", "you", 12, "middle", 600, mono=True)
    d.text(x + 165, y + 33, "251 addresses for your servers", "you", 10.5, "middle")
    x += 334
    d.numbox(x, y, 48, h, ".255", "ink", "surface", 12)
    last = x + 24
    labels = [("network address", "ink"), ("VPC router: your default gateway", "net"), ("AWS DNS", "ink"), ("held back for future use", "ink")]
    for i, (cx, (t, c)) in enumerate(zip(xs, labels)):
        ly = 112 + (3 - i) * 26
        d.path(f"M{cx} {y + h} L{cx} {ly - 4}", "faint", 1.2)
        d.raw(f'<circle cx="{cx}" cy="{ly - 4}" r="2.4" class="f-faint"/>')
        d.text(cx + 10, ly, t, c, 10.5, weight=600 if c == "net" else 400)
    d.path(f"M{last} {y + h} L{last} 108", "faint", 1.2)
    d.raw(f'<circle cx="{last}" cy="108" r="2.4" class="f-faint"/>')
    d.text(last - 10, 112, "broadcast", "ink", 10.5, "end")
    save(d, "02-02/reserved-addresses.svg", "AWS reserves .0, .1, .2, .3 and .255 in every subnet, leaving 251 addresses")


def subnets_that_dont_fit():
    d = D(660, 280)
    d.text(30, 22, "1. outside the VPC", "bad", 11, weight=600)
    d.rect(30, 36, 400, 40, "net", "nettint", 5, 1.6)
    d.text(230, 61, "your VPC: 10.0.0.0/16", "net", 11.5, "middle", 600, mono=True)
    d.text(30, 94, "10.0.0.0", "sub", 9.5, mono=True)
    d.text(230, 94, "every address starts with 10.0", "net", 10, "middle")
    d.text(430, 94, "10.0.255.255", "sub", 9.5, "end", mono=True)
    d.bad(452, 56)
    d.rect(474, 36, 156, 40, "bad", "badtint", 5, 1.4, "5 4")
    d.text(552, 61, "10.1.0.0/24", "bad", 11.5, "middle", 600, mono=True)
    d.text(552, 94, "starts with 10.1", "bad", 10, "middle")
    d.text(30, 136, "2. overlapping public-a", "bad", 11, weight=600)
    d.rect(330, 150, 300, 34, "bad", "badtint", 5, 1.4, "5 4")
    d.text(480, 172, "test: 10.0.1.128/25", "bad", 11.5, "middle", 600, mono=True)
    d.rect(30, 196, 600, 42, "pub", "pubtint", 5, 1.6)
    d.raw('<defs><pattern id="dg-hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
          '<line x1="0" y1="0" x2="0" y2="7" class="s-bad" stroke-width="2" opacity=".45"/></pattern></defs>')
    d.raw('<rect x="331" y="197" width="298" height="40" rx="4" fill="url(#dg-hatch)"/>')
    d.path("M330 196 L330 238", "pub", 1.4, "4 3")
    d.text(180, 222, "10.0.1.0 to .127", "pub", 11, "middle", 600, mono=True)
    d.rect(400, 207, 160, 20, None, "panel", 4, 0)
    d.text(480, 222, "10.0.1.128 to .255", "bad", 11, "middle", 600, mono=True)
    d.text(30, 262, "public-a: 10.0.1.0/24", "pub", 10.5, mono=True)
    d.text(480, 262, "already belongs to public-a", "bad", 10.5, "middle")
    save(d, "02-02/subnets-that-dont-fit.svg", "10.1.0.0/24 sits outside the VPC; 10.0.1.128/25 overlaps the second half of public-a")


def arch_door_no_path():
    d = D(660, 330)
    one_subnet(d, subnet_label="Subnet: public-a", route="0.0.0.0/0  → nothing yet", route_c="bad", server=False)
    save(d, "02-03/arch-door-no-path.svg", "Your VPC has an internet gateway attached, but the subnet's route table has no route to it")


# =============================================================== Phase 3
def what_you_choose():
    d = D(660, 300)
    d.icon(EC2, 294, 110, 72)
    d.text(330, 202, "your server", "ink", 12, "middle", 600)
    cards = [
        (20, 20, "AMI", "the starting disk image", "Amazon Linux 2023", "resource/AmazonEC2AMI"),
        (20, 116, "instance type", "how much CPU and memory", "t3.micro: 2 vCPU, 1 GiB", "resource/AmazonEC2Instances"),
        (20, 212, "key pair", "how you prove it's you", "your .pem file", "resource/Credentials"),
        (440, 20, "network", "where it lives", "your VPC, public-a", "architecture-group/VirtualprivatecloudVPC"),
        (440, 116, "public IP", "how the internet finds it", "enable, for now", "resource/Globe"),
        (440, 212, "security group", "what can reach it", "nothing yet", None),
    ]
    for x, y, t, desc, val, ic in cards:
        d.rect(x, y, 200, 68, "faint", "surface", 6, 1.2)
        if ic:
            d.icon(ic, x + 10, y + 10, 30, keep_colour=ic.startswith("architecture"))
        else:
            d.rect(x + 14, y + 14, 22, 22, "sec", None, 2, 1.6)
        d.text(x + 50, y + 22, t, "ink", 11.5, weight=600)
        d.text(x + 50, y + 37, desc, "sub", 10)
        d.text(x + 50, y + 54, val, "ink", 10.5, mono=True)
        if x < 300:
            d.path(f"M{x + 200} {y + 34} L 288 {146}", "faint", 1.2)
        else:
            d.path(f"M{x} {y + 34} L 372 {146}", "faint", 1.2)
    save(d, "03-01/what-you-choose.svg", "Six choices make a server: AMI, instance type, key pair, network, public IP and security group")


def arch_cant_reach():
    d = D(660, 330)
    one_subnet(d, route="0.0.0.0/0  → ?", route_c="bad", rules=(("nothing allowed in", "faint"),))
    d.arrow([(72, 146), (106, 150)], head=False)
    d.path("M150 150 L190 150", "bad", 1.6, "5 4")
    d.bad(196, 150)
    d.text(196, 132, "no route out", "bad", 10, "middle", 600)
    d.text(88, 138, ":22", "sub", 10, "middle", mono=True)
    save(d, "03-01/arch-cant-reach.svg", "SSH on port 22 fails at the subnet: its route table has no 0.0.0.0/0 route")


def arch_route_added():
    d = D(660, 330)
    one_subnet(d, route="0.0.0.0/0  → igw", rules=(("nothing allowed in", "faint"),))
    d.arrow([(72, 146), (106, 150)], head=False)
    d.path("M150 150 L462 150", "bad", 1.6, "5 4")
    d.bad(470, 150)
    d.text(88, 138, ":22", "sub", 10, "middle", mono=True)
    save(d, "03-02/arch-route-added.svg", "With the route added, traffic reaches the subnet but the security group blocks it")


def arch_ssh_allowed():
    d = D(660, 330)
    one_subnet(d, route="0.0.0.0/0  → igw", rules=(("SSH from your IP", None),))
    d.arrow([(72, 146), (106, 150)], head=False)
    d.arrow([(150, 150), (514, 150)], "ok")
    d.ok(470, 150)
    d.text(88, 138, ":22", "sub", 10, "middle", mono=True)
    save(d, "03-03/arch-ssh-allowed.svg", "The route gets traffic to the subnet; the security group allows SSH from your IP")


def arch_website_live():
    d = D(660, 330)
    one_subnet(d, route="0.0.0.0/0  → igw", rules=(("SSH from your IP", None), ("HTTP from anyone", None)))
    d.labelled("resource/Globe", 46, 236, 40, "anyone")
    d.arrow([(72, 146), (106, 150)], head=False)
    d.arrow([(68, 250), (110, 166)], head=False)
    d.text(88, 138, ":22", "sub", 10, "middle", mono=True)
    d.text(76, 214, ":80", "sub", 10, "middle", mono=True)
    d.arrow([(150, 156), (514, 156)], "ok")
    d.ok(470, 156)
    save(d, "03-04/arch-website-live.svg", "Port 22 from your IP and port 80 from anyone both reach the server")


def timeout_vs_refused():
    d = D(660, 290)
    d.text(20, 24, "timeout", "bad", 12, weight=700)
    d.text(20, 40, "dropped on the way, so no answer ever comes", "sub", 10.5)
    d.icon(LAPTOP, 40, 56, 44)
    d.path("M90 80 L318 80", "bad", 1.6, "5 4")
    d.firewall_wall(330, 60, 104, label="")
    d.bad(330, 80)
    d.icon(EC2, 520, 58, 44, tint=None)
    d.raw('<rect x="516" y="54" width="52" height="52" class="f-panel" opacity=".55"/>')
    d.text(430, 128, "the browser spins, then gives up", "ink", 10.5, "middle")
    d.path("M20 150 L640 150", "faint", 1, "4 4")
    d.text(20, 176, "refused", "ink", 12, weight=700)
    d.text(20, 192, "arrived, but nothing is listening on that port", "sub", 10.5)
    d.icon(LAPTOP, 40, 206, 44)
    d.arrow([(90, 222), (512, 222)], "ok")
    d.firewall_wall(330, 210, 254, label="")
    d.ok(330, 222)
    d.icon(EC2, 520, 206, 44)
    d.arrow([(512, 244), (92, 244)], "ink")
    d.pill(440, 264, "connection refused", "ink", 150)
    d.text(180, 264, "instant error", "ink", 10.5, "middle", 600)
    save(d, "03-04/timeout-vs-refused.svg", "A timeout means traffic was dropped on the way; a refusal means it arrived but nothing was listening")


def nacl_vs_sg():
    d = D(660, 300)
    d.browser(16, 92, label="you")
    d.group(150, 16, 494, 260, "public", "Public subnet: public-a", "10.0.1.0/24")
    d.rect(143, 46, 14, 210, "net", "panel", 3, 1.6)
    d.text(150, 292, "network ACL: checks both directions", "net", 10.5, "middle", 600)
    instance(d, 476, 70, "web-1", "10.0.1.23", "web-sg", (("remembers each request", "sub"),))
    d.arrow([(92, 112), (490, 112)], "ok")
    d.pill(300, 96, "request to :80", "ok", 124)
    d.ok(150, 112, 8)
    d.ok(476, 112, 8)
    d.arrow([(490, 160), (164, 160)], "ink")
    d.pill(330, 178, "reply to :52814", "bad", 132)
    d.ok(476, 160, 8)
    d.bad(150, 160, 9)
    d.text(184, 214, "outbound to :52814?", "bad", 10.5, weight=600, mono=True)
    d.text(184, 229, "no rule allows it", "bad", 10.5)
    save(d, "03-05/nacl-vs-sg.svg", "The request passes both firewalls; the reply passes the security group but the network ACL blocks it")


def inside_the_server():
    d = D(660, 236)
    d.labelled(LAPTOP, 62, 118, 48, "your browser")
    d.server_closeup(190, 20, 450, 196, "EC2 instance: web-1", "t3.micro", [
        ("sshd", ":22", "open"),
        ("python3 hello-server.py", ":80", "open"),
    ], ip="10.0.1.23", disk="8 GiB at /")
    d.arrow([(92, 142), (198, 142)])
    d.text(145, 134, "request to :80", "sub", 10, "middle", mono=True)
    save(d, "03-06/inside-the-server.svg", "Inside an EC2 instance: the OS, its processes and ports, network card and disk")


def public_ip_translation():
    d = D(660, 250)
    d.browser(16, 70, 84, 56, label="your browser")
    d.group(250, 16, 394, 196, "vpc", "your VPC", "10.0.0.0/16")
    d.arrow([(104, 98), (226, 98)])
    d.pill(165, 78, "to 54.170.12.9", "ink", 120)
    d.icon("resource/AmazonVPCInternetGateway", 228, 76, 44)
    d.text(250, 140, "internet gateway", "net", 10, "middle", 600)
    d.text(250, 153, "swaps the address", "sub", 10, "middle")
    d.arrow([(274, 98), (500, 98)])
    d.pill(388, 78, "to 10.0.1.23", "ink", 108)
    d.labelled(EC2, 538, 74, 48, "web-1")
    d.rect(420, 164, 210, 32, "ink", "surface", 6, 1.3)
    d.text(525, 184, "ip addr: 10.0.1.23, that's all", "ink", 10.5, "middle", mono=True)
    d.text(330, 238, "the public IP only exists at the gateway, never on the server", "sub", 10.5, "middle")
    save(d, "03-06/public-ip-translation.svg", "The internet gateway swaps the public IP for the private one; the server only ever sees 10.0.1.23")


def stop_start():
    d = D(660, 280)
    heads = [("running", "ok"), ("stopped", "faint"), ("running again", "ok")]
    xs = [270, 400, 530]
    for x, (t, c) in zip(xs, heads):
        d.pill(x, 22, t, c, 116, mono=False, size=10.5)
    d.arrow([(330, 22), (340, 22)], "faint")
    d.arrow([(460, 22), (470, 22)], "faint")
    rows = [
        ("public IP", ("54.170.12.9", "ink"), ("none", "faint"), ("34.244.7.81", "bad")),
        ("private IP", ("10.0.1.23", "ink"), ("10.0.1.23", "ink"), ("10.0.1.23", "ok")),
        ("disk (EBS)", ("your files", "ink"), ("kept", "ink"), ("still there", "ok")),
        ("memory", ("in use", "ink"), ("wiped", "faint"), ("starts empty", "bad")),
        ("you pay for", ("compute + disk", "ink"), ("disk only", "ink"), ("compute + disk", "ink")),
    ]
    for i, (name, *vals) in enumerate(rows):
        y = 48 + i * 38
        d.rect(20, y, 620, 32, "faint", "surface" if i % 2 == 0 else "panel", 5, 1)
        d.text(36, y + 21, name, "ink", 11.5, weight=500)
        for x, (v, c) in zip(xs, vals):
            d.text(x, y + 21, v, c, 11, "middle", 600 if c in ("ok", "bad") else 400, mono=True)
    d.ok(214, 254, 7)
    d.text(226, 258, "survived", "ok", 10.5, weight=600)
    d.bad(326, 254, 7)
    d.text(338, 258, "changed", "bad", 10.5, weight=600)
    save(d, "03-07/stop-start.svg", "After a stop and start: the public IP changes, the private IP and disk survive, memory is wiped")


def manual_vs_user_data():
    d = D(660, 240)
    d.text(20, 24, "by hand", "ink", 12, weight=700)
    steps = ("launch", "SSH in", "download", "set up service", "ready")
    for i, t in enumerate(steps):
        cx = 60 + i * 135
        d.step(cx, 58, str(i + 1)) if i < 4 else d.ok(cx, 58, 11)
        d.text(cx, 88, t, "ink", 11, "middle", 500)
        if i < 4:
            d.arrow([(cx + 16, 58), (cx + 119, 58)], "faint")
    d.text(20, 116, "every step is you, every time", "sub", 10.5)
    d.path("M20 134 L640 134", "faint", 1, "4 4")
    d.text(20, 160, "with user data", "you", 12, weight=700)
    steps2 = ("launch with a script", "first boot runs it", "ready")
    for i, t in enumerate(steps2):
        cx = 60 + i * 270
        d.step(cx, 192, str(i + 1)) if i < 2 else d.ok(cx, 192, 11)
        d.text(cx, 222, t, "ink", 11, "middle", 500)
        if i < 2:
            d.arrow([(cx + 16, 192), (cx + 254, 192)], "faint")
    d.text(330, 180, "no SSH, no typing", "you", 10.5, "middle", 600)
    save(d, "03-08/manual-vs-user-data.svg", "By hand takes five steps every time; user data does the same on first boot")


def role_credentials():
    d = D(660, 300)
    d.rect(20, 30, 150, 60, "sec", "panel", 8, 1.5)
    d.icon("resource/AWSIdentityAccessManagementRole", 30, 42, 36)
    d.text(76, 56, "IAM role", "ink", 12, weight=600)
    d.text(76, 72, "web-role", "sub", 10.5, mono=True)
    d.rect(210, 16, 220, 200, "cmp", None, 6, 1.6)
    d.icon(EC2, 218, 22, 26)
    d.text(252, 40, "EC2 instance: web-2", "ink", 11.5, weight=600)
    d.rect(228, 58, 184, 54, "ink", "surface", 6, 1.3)
    d.icon("resource/AWSIdentityAccessManagementTemporarySecurityCredential", 236, 66, 36)
    d.text(280, 80, "instance metadata", "ink", 11, weight=600)
    d.text(280, 95, "temporary keys, renewed", "sub", 9.5)
    d.rect(228, 146, 184, 50, "ink", "surface", 6, 1.3)
    d.icon("architecture-service/AWSCommandLineInterface", 236, 155, 32)
    d.text(278, 176, "aws cli", "ink", 11.5, weight=600, mono=True)
    d.arrow([(170, 60), (226, 78)])
    d.arrow([(320, 112), (320, 144)])
    d.rect(476, 110, 164, 104, "ink", "surface", 8, 1.5)
    d.icon("architecture-group/AWSCloudlogo", 486, 120, 22, keep_colour=True)
    d.text(516, 135, "AWS API", "ink", 12, weight=700)
    d.text(486, 156, "IAM checks each call", "sub", 9.5)
    d.ok(494, 176, 7)
    d.text(506, 180, "ec2:Describe*", "ok", 10.5, mono=True)
    d.bad(494, 198, 7)
    d.text(506, 202, "s3:ListBuckets", "bad", 10.5, mono=True)
    d.arrow([(412, 171), (472, 162)])
    d.rect(20, 238, 410, 46, "bad", "badtint", 8, 1.3, "5 4")
    d.icon("resource/AWSIdentityAccessManagementLongTermSecurityCredential", 30, 244, 34)
    d.text(74, 258, "access keys saved on the server", "bad", 11, weight=600)
    d.text(74, 273, "never expire, easy to leak: don't do this", "sub", 10)
    save(d, "03-09/role-credentials.svg", "The role gives the server temporary keys through instance metadata; IAM still checks every call")


def ami_bake():
    d = D(660, 250)
    d.labelled(EC2, 70, 70, 56, "web-2", "patched, app installed", sub_mono=False)
    d.arrow([(110, 98), (220, 98)])
    d.pill(165, 80, "create image", "ink", 104, mono=False, size=10.5)
    d.rect(226, 56, 150, 86, "cmp", "surface", 8, 1.6)
    d.icon("resource/AmazonEC2AMI", 236, 66, 36)
    d.text(280, 82, "AMI", "ink", 13, weight=700)
    d.text(280, 98, "web-ami", "sub", 10.5, mono=True)
    d.text(240, 128, "+ a disk snapshot", "sub", 10)
    for i in range(3):
        y = 16 + i * 72
        d.icon(EC2, 548, y, 44)
        d.arrow([(378, 99), (540, y + 22)], "faint")
    d.text(570, 238, "identical every time", "you", 10.5, "middle", 600)
    d.text(30, 196, "user data: build it on every boot", "sub", 10.5)
    d.text(30, 214, "AMI: build it once, copy it", "ink", 10.5, weight=600)
    save(d, "03-10/ami-bake.svg", "web-2 becomes an AMI, and every server launched from it is an identical copy")


# =============================================================== Phase 4
def two_subnets(d, *, bastion=False, app=True, app_sg="app-sg", app_rule=("nothing allowed in", "faint"),
                bastion_rule=("SSH from your IP", None)):
    d.labelled(LAPTOP, 44, 176, 48, "your laptop", "your IP")
    d.group(96, 10, 552, 462, "cloud", "AWS Cloud")
    d.group(112, 46, 524, 414, "region", "Europe (Ireland) eu-west-1")
    d.group(140, 82, 482, 366, "vpc", "your VPC", "10.0.0.0/16")
    d.icon("resource/AmazonVPCInternetGateway", 118, 178, 44)
    d.text(140, 236, "internet", "sub", 10, "middle")
    d.text(140, 248, "gateway", "sub", 10, "middle")
    d.group(196, 112, 410, 156, "public", "Public subnet: public-a", "10.0.1.0/24")
    d.group(196, 280, 410, 156, "private", "Private subnet: private-a", "10.0.2.0/24")
    route_note(d, 212, 218, "0.0.0.0/0  → igw", "pub")
    route_note(d, 212, 386, "nothing else", "sub")
    if bastion:
        instance(d, 462, 132, "bastion", "10.0.1.20", "bastion-sg", (bastion_rule,), w=130)
    else:
        d.text(527, 196, "no servers", "faint", 11, "middle", 500)
    if app:
        instance(d, 462, 300, "app-1", "10.0.2.37", app_sg, (app_rule,), w=130)


def three_tiers():
    d = D(660, 290)
    d.labelled("resource/Globe", 46, 136, 48, "internet")
    tiers = [(110, "public", "web tier", EC2), (290, "private", "app tier", EC2), (470, "private", "database", "architecture-service/AmazonRDS")]
    for x, kind, name, ic in tiers:
        d.group(x, 90, 166, 150, kind, name)
        d.icon(ic, x + 61, 140, 44)
    d.arrow([(72, 160), (166, 162)])
    d.ok(110, 161, 8)
    d.arrow([(232, 162), (346, 162)])
    d.ok(290, 162, 8)
    d.arrow([(412, 162), (526, 162)])
    d.ok(470, 162, 8)
    d.path("M46 130 L46 58 L420 58 L420 82", "bad", 1.4, "5 4")
    d.bad(420, 90, 8)
    d.path("M38 130 L38 34 L600 34 L600 82", "bad", 1.4, "5 4")
    d.bad(600, 90, 8)
    d.text(210, 52, "the internet can't reach these directly", "bad", 10.5, "middle", 600)
    d.text(373, 270, "each tier only talks to the one next to it", "sub", 10.5, "middle")
    save(d, "04-01/three-tiers.svg", "The internet reaches the web tier; the app tier and database are private")


def public_vs_private():
    d = D(660, 270)
    d.group(16, 10, 628, 250, "vpc", "your VPC", "10.0.0.0/16")
    d.icon("resource/AmazonVPCInternetGateway", 80, 70, 48)
    d.text(104, 136, "internet gateway", "net", 10, "middle", 600)
    for x, kind, name, cidr, rt, rows in (
        (180, "public", "Public subnet: public-a", "10.0.1.0/24", "public-rt", [("10.0.0.0/16", "local"), ("0.0.0.0/0", "igw", "pub")]),
        (420, "private", "Private subnet: private-a", "10.0.2.0/24", "private-rt", [("10.0.0.0/16", "local")]),
    ):
        d.group(x, 46, 214, 196, kind, name)
        d.text(x + 200, 86, cidr, "sub", 10.5, "end", mono=True)
        d.icon("resource/AmazonVPCRouter", x + 14, 98, 26)
        d.text(x + 48, 116, rt, "ink", 11, weight=600, mono=True)
        d.table(x + 14, 132, 186, rows, header=("destination", "target"), col=0.58)
    d.rect(434, 210, 186, 22, "bad", None, 4, 1.2, "4 3")
    d.text(527, 225, "no way out", "bad", 10.5, "middle", 600)
    d.arrow([(130, 94), (176, 94)])
    save(d, "04-02/public-vs-private.svg", "public-a's route table has a route to the internet gateway; private-a's only has the local route")


def arch_unreachable():
    d = D(660, 482)
    two_subnets(d, bastion=False)
    d.text(448, 360, "no public IP", "bad", 10, "end", 600)
    d.arrow([(44, 262), (44, 300)], head=False)
    d.bad(44, 312)
    d.text(44, 336, "10.0.2.37 isn't", "bad", 10, "middle", 600)
    d.text(44, 349, "on the internet", "bad", 10, "middle", 600)
    save(d, "04-03/arch-unreachable.svg", "app-1 has no public IP and no route out, so your laptop can't reach it")


def arch_bastion():
    d = D(660, 482)
    two_subnets(d, bastion=True, app_rule=("SSH from bastion-sg", None))
    d.arrow([(70, 200), (118, 200)])
    d.arrow([(162, 200), (506, 200)])
    d.step(330, 200, "1")
    d.arrow([(527, 266), (527, 312)])
    d.step(505, 289, "2")
    save(d, "04-04/arch-bastion.svg", "Two hops: your laptop to the bastion, then the bastion to app-1")


def sg_reference():
    d = D(660, 300)
    d.rect(170, 12, 280, 48, "sec", "panel", 8, 1.5)
    d.text(310, 32, "app-sg inbound rule", "sec", 11, "middle", 600)
    d.text(310, 49, "SSH, port 22, source: bastion-sg", "ink", 10.5, "middle", mono=True)
    d.group(20, 82, 240, 124, "sg", "bastion-sg")
    for i, (name, ip) in enumerate((("bastion", "10.0.1.20"), ("bastion-2", "10.0.1.88"))):
        cx = 80 + i * 120
        d.labelled(EC2, cx, 102, 40, name, ip)
    d.labelled(EC2, 80, 224, 40, "web-1")
    d.text(116, 272, "not in bastion-sg", "sub", 10.5)
    instance(d, 486, 82, "app-1", "10.0.2.37", "app-sg", (), w=130)
    d.arrow([(262, 144), (482, 144)], "ok")
    d.ok(464, 144)
    d.text(370, 134, "any server in the group", "ok", 10.5, "middle", 600)
    d.path("M104 246 L470 196", "bad", 1.6, "5 4")
    d.bad(478, 194)
    save(d, "04-04/sg-reference.svg", "Any server in bastion-sg can reach app-1; a server outside the group can't")


def no_way_out():
    d = D(660, 270)
    d.text(20, 24, "getting in", "ok", 12, weight=700)
    d.text(20, 40, "blocked, as intended", "sub", 10.5)
    d.icon("resource/Globe", 46, 62, 44)
    d.path("M94 84 L338 84", "bad", 1.6, "5 4")
    d.bad(346, 84)
    d.group(366, 52, 270, 70, "private", "Private subnet: private-a")
    d.icon(EC2, 580, 66, 40)
    d.path("M20 144 L640 144", "faint", 1, "4 4")
    d.text(20, 170, "getting out", "bad", 12, weight=700)
    d.text(20, 186, "blocked, and that's a problem", "sub", 10.5)
    d.group(366, 190, 270, 70, "private", "Private subnet: private-a")
    d.icon(EC2, 580, 204, 40)
    d.path("M574 224 L354 224", "bad", 1.6, "5 4")
    d.bad(346, 224)
    d.icon("resource/Globe", 46, 202, 44)
    d.pill(200, 212, "software updates", "bad", 128, mono=False, size=10)
    d.pill(200, 242, "downloads, AWS APIs", "bad", 144, mono=False, size=10)
    save(d, "04-05/no-way-out.svg", "A private subnet blocks both directions: nothing gets in, and nothing gets out")


ALL = [vpc_in_region, subnet_plan, reserved_addresses, subnets_that_dont_fit, arch_door_no_path,
       what_you_choose, arch_cant_reach, arch_route_added, arch_ssh_allowed, arch_website_live, timeout_vs_refused,
       nacl_vs_sg, inside_the_server, public_ip_translation, stop_start, manual_vs_user_data, role_credentials, ami_bake,
       three_tiers, public_vs_private, arch_unreachable, arch_bastion, sg_reference, no_way_out]

if __name__ == "__main__":
    for f in ALL:
        f()
    print(len(ALL), "phase 2-4 diagrams")
