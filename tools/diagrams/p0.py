"""Phase 0 diagrams in the v2 system. Same file names as before."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dg import D

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "public", "images", "labs")
SRV = "resource/Server"
LAPTOP = "resource/Client"


def save(d, path, title):
    d.save(f"{OUT}/{path}", title)


# =============================================================== 0.1
def server_anatomy():
    d = D(660, 270)
    d.icon(SRV, 52, 64, 96)
    d.text(100, 186, "one server", "ink", 12, "middle", 500)
    parts = [("CPU", "processing power"), ("Memory", "RAM, cleared when it restarts"),
             ("Disk", "storage, survives a restart"), ("Network", "connection to other machines")]
    for i, (t, sub) in enumerate(parts):
        y = 20 + i * 58
        d.card(330, y, 290, 46, t, sub)
        d.path(f"M150 {110 + (i - 1.5) * 14} C 240 {110 + (i - 1.5) * 14}, 240 {y + 23}, 330 {y + 23}", "line", 1.4)
    save(d, "00-01/server-anatomy.svg", "A server with CPU, memory, disk and network")


def capacity_vs_demand():
    d = D(660, 250)
    curve = "C 200 172, 236 54, 320 54 S 448 164, 620 176"
    d.path(f"M60 54 L60 172 {curve} L620 54 Z", "badtint", 0, fill="badtint")
    d.path("M60 210 L620 210 M60 210 L60 30", "faint", 1.4)
    d.path(f"M60 172 {curve}", "ink", 2.4)
    d.path("M60 54 L620 54", "you", 2, "7 5")
    d.text(68, 46, "what you bought, and pay for always", "you", 11.5, weight=600)
    d.text(330, 150, "what you actually need", "ink", 11.5, "middle", 600)
    d.text(140, 118, "wasted", "bad", 11.5, "middle", 600)
    d.text(520, 118, "wasted", "bad", 11.5, "middle", 600)
    d.text(54, 30, "load", "sub", 10, "end")
    d.text(620, 228, "time", "sub", 10, "end")
    save(d, "00-01/capacity-vs-demand.svg", "Fixed purchased capacity against changing demand")


def virtualisation():
    d = D(660, 330)
    d.text(330, 22, "three virtual machines, each behaves like its own computer", "sub", 11, "middle")
    for cx, lab, tint in ((150, "someone else's", "faint"), (330, "yours", "you"), (510, "someone else's", "faint")):
        d.labelled(SRV, cx, 40, 52, lab, tint=tint, label_c="you" if tint == "you" else "sub")
        d.arrow([(330 + (cx - 330) * 0.35, 182), (cx, 126)])
    d.card(180, 182, 300, 50, "virtualisation layer", "divides the machine up and keeps them apart", "ink", "surface", align="middle")
    d.arrow([(330, 270), (330, 236)])
    d.icon(SRV, 302, 270, 56)
    d.text(372, 296, "one physical server", "ink", 11.5, weight=500)
    d.text(372, 310, "the real hardware", "sub", 10)
    save(d, "00-01/virtualisation.svg", "One physical server divided into virtual machines")


def service_models():
    d = D(660, 320)
    layers = ["your app", "runtime", "OS", "virtualisation", "hardware"]
    cols = [("On premises", "", 5), ("IaaS", "EC2", 3), ("PaaS", "Lambda", 1), ("SaaS", "Gmail", 0)]
    for i, (name, ex, mine) in enumerate(cols):
        x = 30 + i * 154
        d.text(x + 65, 24, name, "ink", 12, "middle", 600)
        if ex:
            d.text(x + 65, 39, ex, "sub", 10, "middle")
        if mine == 0:
            d.rect(x, 52, 130, 192, "faint", "surface", 5, 1.3)
            d.text(x + 65, 152, "all of it", "sub", 11, "middle", 500)
            continue
        for j, lay in enumerate(layers):
            y = 52 + j * 40
            yours = j < mine
            d.rect(x, y, 130, 32, "you" if yours else "faint", "youtint" if yours else "surface", 5, 1.4)
            d.text(x + 65, y + 20, lay, "you" if yours else "sub", 11, "middle", 600 if yours else 400)
    d.rect(30, 278, 16, 16, "you", "youtint", 3, 1.4)
    d.text(54, 290, "you manage", "ink", 11)
    d.rect(170, 278, 16, 16, "faint", "surface", 3, 1.3)
    d.text(194, 290, "the provider manages", "ink", 11)
    save(d, "00-01/service-models.svg", "What you manage across on-premises, IaaS, PaaS and SaaS")


def regions_azs():
    d = D(660, 320)
    d.group(20, 12, 620, 296, "region", "Region: Europe (Ireland) eu-west-1")
    for i, (x, name) in enumerate(((44, "Availability Zone A"), (364, "Availability Zone B"))):
        d.group(x, 52, 252, 214, "az", name)
        d.building(x + 126, 92, 150, 104)
    d.rect(126 + 36 + 2, 120, 26, 24, "you", "youtint", 1.5, 2)
    d.path("M317 170 L343 170", "faint", 1.4, "4 3")
    d.text(330, 160, "miles apart", "sub", 10, "middle")
    d.text(330, 188, "own power", "sub", 10, "middle")
    d.path("M177 146 L177 236", "you", 1.4)
    d.text(177, 252, "your server is a slice of one of these", "you", 10.5, "middle", 600)
    save(d, "00-01/regions-azs.svg", "Two separate Availability Zones inside one AWS Region")


def shared_responsibility():
    d = D(660, 250)
    d.rect(20, 14, 290, 216, "you", "youtint", 8, 1.6)
    d.text(165, 40, "Yours", "you", 14, "middle", 700)
    d.text(165, 56, "security in the cloud", "sub", 10.5, "middle")
    for i, t in enumerate(["your application code", "the operating system and patches", "who can log in, and how",
                           "firewall rules you configure", "your data, and its encryption"]):
        d.text(40, 88 + i * 27, t, "ink", 11.5)
    d.path("M330 24 L330 222", "faint", 1.4, "4 4")
    d.rect(350, 14, 290, 216, "ink", "surface", 8, 1.6)
    d.icon("architecture-group/AWSCloudlogo", 470, 26, 24, keep_colour=True)
    d.text(500, 43, "AWS", "ink", 14, "start", 700)
    d.text(495, 60, "security of the cloud", "sub", 10.5, "middle")
    for i, t in enumerate(["the physical buildings", "the hardware and racks", "the virtualisation layer",
                           "power, cooling, guards", "the network between Regions"]):
        d.text(370, 88 + i * 27, t, "ink", 11.5)
    save(d, "00-01/shared-responsibility.svg", "The Shared Responsibility Model")


# =============================================================== 0.2
def home_network():
    d = D(660, 330)
    d.rect(16, 24, 628, 292, "net", None, 10, 1.4, "6 5")
    d.text(330, 16, "one network: devices that can reach each other", "sub", 10.5, "middle")
    devices = [("laptop", "192.168.1.10", 110, 52, "laptop"), ("phone", "192.168.1.11", 550, 52, "phone"),
               ("printer", "192.168.1.12", 110, 214, "printer"), ("television", "192.168.1.13", 550, 214, "tv")]
    for name, ip, cx, y, kind in devices:
        d.path(f"M{cx} {y + 26} L330 {158}", "line", 1.4)
    d.rect(286, 128, 88, 64, "net", "nettint", 8, 1.6)
    d.home_router(330, 134)
    d.text(330, 210, "router", "ink", 11.5, "middle", 600)
    d.text(330, 224, "192.168.1.1", "sub", 10, "middle", mono=True)
    d.text(330, 238, "hands out addresses (DHCP)", "sub", 10, "middle")
    for name, ip, cx, y, kind in devices:
        d.rect(cx - 40, y - 8, 80, 66, None, "panel", 6, 0)
        if kind == "laptop":
            d.labelled(LAPTOP, cx, y, 48, name, ip)
        elif kind == "phone":
            d.labelled("resource/Mobileclient", cx, y, 48, name, ip)
        elif kind == "printer":
            d.printer(cx, y, label=name, sub=ip)
        else:
            d.tv(cx, y, label=name, sub=ip)
    save(d, "00-02/home-network.svg", "A home network: a router and four devices, each with its own private IP address")


def private_public_ip():
    d = D(660, 330)
    d.text(160, 22, "private addresses", "you", 11.5, "middle", 600)
    d.text(540, 22, "public addresses", "ink", 11.5, "middle", 600)
    d.path("M430 34 L430 316", "faint", 1.4, "4 4")
    for i, (home, pub) in enumerate((("home A", "89.101.44.7"), ("home B", "92.51.6.22"))):
        y = 40 + i * 140
        d.rect(16, y, 210, 118, "faint", None, 8, 1.3, "5 4")
        d.text(28, y + 18, home, "sub", 10.5)
        d.labelled(LAPTOP, 121, y + 26, 44, "your laptop", "192.168.1.10")
        d.path(f"M168 {y + 50} L288 {y + 50}", "line", 1.4)
        d.home_router(320, y + 24)
        d.text(320, y + 86, "router", "ink", 11, "middle", 500)
        d.text(352, y + 72, "public IP", "sub", 9.5)
        d.text(352, y + 86, pub, "ink", 10, mono=True)
        d.path(f"M346 {y + 50} C 420 {y + 50}, 470 170, 500 172", "line", 1.4)
    d.labelled(SRV, 548, 140, 56, "a public server", "203.0.113.10")
    d.text(214, 316, "the same private address in both homes, and that's fine", "sub", 10, "middle")
    save(d, "00-02/private-public-ip.svg", "Two homes using the same private address, each with its own public address")


def ports():
    d = D(660, 300)
    d.labelled("resource/Globe", 70, 110, 52, "the internet", "anyone", sub_mono=False)
    d.server_closeup(250, 16, 390, 262, "one machine", "203.0.113.10", [
        ("ssh: logging in remotely", "22", "open"),
        ("http: web pages", "80", "open"),
        ("https: web pages, encrypted", "443", "open"),
        ("mysql: the database", "3306", "bad"),
    ], header_icon=SRV, os_label="Linux", frame="ink")
    for i, y in enumerate((104, 138, 172)):
        d.arrow([(100, 136), (220, y), (258, y)], "ok")
    d.path("M100 142 L232 206", "bad", 1.6, "5 4")
    d.bad(240, 206)
    save(d, "00-02/ports.svg", "One machine with four ports: SSH, HTTP and HTTPS open, MySQL closed to the internet")


def protocol_stack():
    d = D(660, 220)
    d.browser(16, 74, label="your browser")
    d.arrow([(92, 100), (140, 100)])
    d.rect(144, 20, 360, 180, "net", "nettint", 8, 1.6)
    d.text(160, 42, "IP", "net", 13, weight=700)
    d.text(184, 42, "which machine to send it to", "sub", 10.5)
    d.rect(162, 56, 324, 130, "net", "panel", 6, 1.4)
    d.text(178, 78, "TCP", "net", 13, weight=700)
    d.text(212, 78, "in order, nothing lost", "sub", 10.5)
    d.rect(180, 92, 288, 80, "ink", "surface", 6, 1.4)
    d.text(196, 114, "HTTP", "ink", 13, weight=700)
    d.text(240, 114, "what you actually asked for", "sub", 10.5)
    d.text(196, 146, "GET /index.html", "ink", 12, mono=True)
    d.arrow([(504, 100), (552, 100)])
    d.labelled(SRV, 594, 70, 56, "the server")
    save(d, "00-02/protocol-stack.svg", "A web request wrapped by HTTP, then TCP, then IP")


def dns_lookup():
    d = D(660, 260)
    d.card(30, 16, 150, 56, "DNS", "a directory of names", "net", "nettint", "net", 14, "middle")
    d.browser(52, 150, 106, 70, label="your browser", url="inthelab.ie")
    d.arrow([(88, 148), (88, 76)])
    d.arrow([(122, 76), (122, 148)])
    d.step(70, 112, "1")
    d.step(140, 112, "2")
    d.text(162, 106, "where is inthelab.ie?", "ink", 11)
    d.text(162, 124, "it's at 93.184.216.34", "ink", 11)
    d.arrow([(166, 186), (532, 186)])
    d.step(350, 186, "3")
    d.text(350, 214, "the page comes from here, not from DNS", "sub", 10.5, "middle")
    d.labelled(SRV, 576, 150, 60, "inthelab.ie", "93.184.216.34")
    save(d, "00-02/dns-lookup.svg", "A browser asks DNS where inthelab.ie is, gets an address back, then connects to the server")


def request_journey():
    d = D(660, 250)
    xs = [70, 200, 330, 460, 590]
    d.arrow([(xs[4], 42), (xs[4], 28), (xs[0], 28), (xs[0], 46)], "line", sw=1.4)
    d.text(330, 18, "the response travels back the same way", "sub", 10.5, "middle")
    d.browser(xs[0] - 36, 52, label=None, url="inthelab.ie")
    d.card(xs[1] - 40, 56, 80, 44, "DNS", None, "net", "nettint", "net", 13, "middle")
    d.icon("resource/Globe", xs[2] - 26, 50, 52)
    d.pill(xs[3], 58, "443", "ink", 54)
    d.icon(SRV, xs[3] - 22, 72, 44)
    d.icon(SRV, xs[4] - 26, 50, 52)
    d.path(f"M{xs[0]} 150 L{xs[4]} 150", "faint", 1.4)
    labels = [("you type the name", "inthelab.ie"), ("DNS finds the", "IP address"), ("you connect across", "the internet"),
              ("HTTPS arrives on", "port 443"), ("the server", "sends the page")]
    for i, x in enumerate(xs):
        d.step(x, 150, str(i + 1))
        d.text(x, 184, labels[i][0], "ink", 11, "middle", 500)
        d.text(x, 199, labels[i][1], "sub", 10.5, "middle")
        if i < 4:
            d.arrow([(x + 16, 150), (xs[i + 1] - 16, 150)], "faint")
    save(d, "00-02/request-journey.svg", "The five stops of a web request")


def tcp_vs_udp():
    d = D(660, 310)
    for row, (name, sub, y) in enumerate((("TCP", "notices what went missing", 20), ("UDP", "never looks back", 170))):
        d.text(16, y + 12, name, "net", 14, weight=700)
        d.text(56, y + 12, sub, "sub", 10.5)
        d.labelled(LAPTOP, 46, y + 34, 40, "your laptop")
        d.text(128, y + 42, "sends", "sub", 10, "middle")
        for k in range(4):
            d.numbox(84 + k * 22, y + 50, 18, 22, str(k + 1), "ink", "panel", 11)
        d.arrow([(180, y + 61), (330, y + 61)], "line")
        d.bad(256, y + 61, 7)
        d.text(256, y + 44, "2 goes missing", "bad", 10, "middle", 600)
        d.text(396, y + 42, "receives", "sub", 10, "middle")
        for k in range(4):
            if row == 1 and k == 1:
                d.rect(352 + k * 22, y + 50, 18, 22, "bad", "badtint", 4, 1.4, "3 2")
                d.text(361 + k * 22, y + 65, "×", "bad", 12, "middle", 700)
            else:
                d.numbox(352 + k * 22, y + 50, 18, 22, str(k + 1), "ok" if row == 0 else "ink", "panel", 11)
        d.icon(SRV, 456, y + 34, 44)
        d.text(478, y + 94, "the server", "ink", 11, "middle", 500)
        if row == 0:
            d.path(f"M256 {y + 72} C 256 {y + 104}, 200 {y + 104}, 200 {y + 76}", "ok", 1.5)
            d.text(256, y + 116, "TCP sends it again", "ok", 10, "middle", 600)
            d.text(560, y + 56, "all four arrive", "ok", 11, "middle", 600)
            d.text(560, y + 71, "in the right order", "sub", 10, "middle")
        else:
            d.text(560, y + 56, "three arrive", "bad", 11, "middle", 600)
            d.text(560, y + 71, "2 is gone for good", "sub", 10, "middle")
    d.path("M16 150 L644 150", "faint", 1, "4 4")
    save(d, "00-02/tcp-vs-udp.svg", "Four numbered messages sent over TCP and over UDP, with one lost in each case")


# =============================================================== 0.3
def address_split():
    d = D(660, 270)
    for r, (split, right, y) in enumerate(((3, "a smaller network", 30), (2, "a far bigger network", 150))):
        vals = ["192", "168", "1", "10"]
        x = 40
        for i, v in enumerate(vals):
            net = i < split
            d.numbox(x, y, 76, 50, v, "net" if net else "ink", "nettint" if net else "surface", 18)
            if i < 3:
                d.text(x + 86, y + 32, ".", "sub", 16, "middle")
            if i == split - 1:
                lx = x + 86
                d.path(f"M{lx} {y - 8} L{lx} {y + 58}", "net", 2.4)
            x += 96
        d.text(40 + split * 96 / 2 - 10, y + 76, "the network", "net", 11, "middle", 600)
        d.text(40 + split * 96 + (4 - split) * 96 / 2 - 10, y + 76, "this device", "ink", 11, "middle", 600)
        d.text(440, y + 30, right, "sub", 11)
    d.text(330, 262, "the digits never change, only where the line falls", "sub", 10.5, "middle")
    save(d, "00-03/address-split.svg", "The address 192.168.1.10 with the network part ending in two different places")


def cidr_24():
    d = D(660, 260)
    d.text(330, 24, "192.168.1.0/24", "ink", 15, "middle", 600, mono=True)
    for i, v in enumerate(["192", "168", "1", "0"]):
        x = 40 + i * 150
        net = i < 3
        d.numbox(x, 46, 120, 62, v, "net" if net else "ink", "nettint" if net else "surface", 20)
        d.text(x + 60, 128, "8 bits", "sub", 10.5, "middle")
    d.path("M475 36 L475 150", "net", 2, "5 4")
    d.text(475, 166, "/24 draws the line", "net", 11, "middle", 600)
    d.bracket(40, 450, 196, "8 + 8 + 8 = 24 bits", "the network", "net")
    d.bracket(490, 610, 196, "8 bits left", "up to 256 addresses", "ink")
    save(d, "00-03/cidr-24.svg", "192.168.1.0/24: three 8-bit numbers form the network, one is left for devices")


def cidr_size_comparison():
    d = D(660, 230)
    for i, (pfx, left, n, w) in enumerate((("/24", "8 bits left", "256 addresses", 400), ("/25", "7 bits left", "128 addresses", 200), ("/26", "6 bits left", "64 addresses", 100))):
        y = 24 + i * 62
        d.text(70, y + 24, pfx, "net", 18, "end", 600, mono=True)
        d.text(70, y + 40, left, "sub", 9.5, "end")
        d.rect(90, y, 400, 36, "faint", None, 5, 1.2, "4 4")
        d.rect(90, y, w, 36, "net", "nettint", 5, 1.6)
        d.text(510, y + 23, n, "ink", 11.5, weight=500)
    d.text(330, 218, "the number goes up, the network goes down", "net", 11, "middle", 600)
    save(d, "00-03/cidr-size-comparison.svg", "/24, /25 and /26, each half the size of the one above")


def subnet_splitting():
    d = D(660, 240)
    d.text(40, 22, "10.0.0.0", "sub", 10, mono=True)
    d.text(620, 22, "10.0.0.255", "sub", 10, "end", mono=True)
    d.rect(40, 32, 580, 44, "net", "nettint", 6, 1.6)
    d.text(330, 59, "10.0.0.0/24", "net", 13, "middle", 600, mono=True)
    d.path("M330 80 L330 150", "net", 1.6, "5 4")
    d.text(344, 104, "cut it exactly in half", "ink", 11, weight=500)
    d.text(344, 120, "the second half starts at .128", "sub", 10.5)
    for i, (lab, rng) in enumerate((("10.0.0.0/25", "10.0.0.0 to 10.0.0.127"), ("10.0.0.128/25", "10.0.0.128 to 10.0.0.255"))):
        x = 40 + i * 294
        d.rect(x, 152, 286, 44, "net", "nettint", 6, 1.6)
        d.text(x + 143, 179, lab, "net", 13, "middle", 600, mono=True)
        d.text(x + 143, 216, rng, "sub", 10, "middle", mono=True)
    save(d, "00-03/subnet-splitting.svg", "10.0.0.0/24 cut in half into two /25 subnets")


# =============================================================== 0.4
def local_vs_remote():
    d = D(660, 300)
    d.rect(16, 16, 360, 268, "net", None, 10, 1.4, "6 5")
    d.text(30, 36, "your network", "sub", 10.5)
    d.text(362, 36, "192.168.1.0/24", "net", 10.5, "end", 600, mono=True)
    d.labelled(LAPTOP, 100, 56, 48, "laptop", "192.168.1.10")
    d.arrow([(100, 150), (100, 194)], "line")
    d.text(112, 178, "same network: send it directly", "sub", 10)
    d.printer(100, 196, label="printer", sub="192.168.1.20")
    d.arrow([(130, 80), (372, 120)], "line")
    d.text(240, 66, "different network?", "ink", 11, "middle", 500)
    d.text(240, 80, "send it to the router", "sub", 10.5, "middle")
    d.rect(372, 104, 88, 64, "net", "nettint", 8, 1.6)
    d.home_router(416, 110)
    d.text(416, 186, "router", "ink", 11.5, "middle", 600)
    d.text(416, 200, "192.168.1.1", "sub", 10, "middle", mono=True)
    d.text(416, 214, "default gateway", "net", 10, "middle", 600)
    d.arrow([(460, 136), (536, 136)], "line")
    d.text(586, 80, "another network", "sub", 10.5, "middle")
    d.labelled(SRV, 586, 108, 52, "server", "8.8.8.8")
    save(d, "00-04/local-vs-remote.svg", "Same network goes direct; anything else goes to the router")


def routing_table():
    d = D(660, 300)
    d.text(330, 18, "your laptop's routing table", "sub", 10.5, "middle")
    d.table(110, 28, 440, [("192.168.1.0/24", "send directly"), ("0.0.0.0/0", "send to the router")], header=("destination", "what to do"), col=0.5)
    # flow 1
    d.pill(80, 150, "to 192.168.1.20", "ink", 130)
    d.arrow([(146, 150), (190, 150)])
    d.card(194, 128, 150, 44, "rule 1?", "yes, it's local")
    d.ok(330, 150, 8)
    d.arrow([(344, 150), (470, 150)], "line", "5 4")
    d.card(474, 128, 160, 44, "send directly", "to the printer", "ok", "panel", "ok")
    # flow 2
    d.pill(80, 236, "to 8.8.8.8", "ink", 130)
    d.arrow([(146, 236), (190, 236)])
    d.card(194, 214, 130, 44, "rule 1?", "no, not local")
    d.bad(312, 236, 8)
    d.arrow([(324, 236), (350, 236)])
    d.card(354, 214, 110, 44, "rule 2?", "yes, always")
    d.ok(452, 236, 8)
    d.arrow([(464, 236), (470, 236)])
    d.card(474, 214, 160, 44, "send to router", "192.168.1.1", "net", "nettint", "net")
    save(d, "00-04/routing-table.svg", "Traffic to 192.168.1.20 matches the local route; traffic to 8.8.8.8 matches the default route")


def longest_prefix_match():
    d = D(660, 320)
    d.pill(330, 18, "destination: 10.20.30.40", "you", 210)
    d.rect(20, 40, 620, 268, "faint", None, 10, 1.4, "6 5")
    d.text(36, 62, "0.0.0.0/0", "sub", 12, weight=600, mono=True)
    d.text(36, 77, "all 4.3 billion addresses", "sub", 10)
    d.text(624, 62, "Router A", "sub", 11, "end", 500)
    d.rect(60, 92, 560, 200, "sub", None, 10, 1.4)
    d.text(76, 114, "10.0.0.0/8", "ink", 12, weight=600, mono=True)
    d.text(76, 129, "16.7 million addresses", "sub", 10)
    d.text(604, 114, "Router B", "ink", 11, "end", 500)
    d.rect(100, 144, 500, 132, "net", "nettint", 10, 1.8)
    d.text(116, 166, "10.20.0.0/16", "net", 12, weight=700, mono=True)
    d.text(116, 181, "65,536 addresses", "sub", 10)
    d.text(584, 166, "Router C", "net", 11, "end", 700)
    d.raw('<circle cx="350" cy="220" r="8" class="f-you"/>')
    d.text(350, 248, "10.20.30.40", "you", 11, "middle", 600, mono=True)
    d.ok(584, 252, 8)
    d.text(570, 256, "smallest match wins", "ok", 10.5, "end", 600)
    save(d, "00-04/longest-prefix-match.svg", "Three nested ranges all contain 10.20.30.40; the smallest, /16, is chosen")


def hop_by_hop():
    d = D(660, 220)
    d.pill(78, 18, "to 8.8.8.8", "you", 96)
    d.labelled(LAPTOP, 46, 56, 44, "your laptop")
    d.text(46, 132, "not local, use", "sub", 9.5, "middle")
    d.text(46, 145, "the gateway", "sub", 9.5, "middle")
    routers = [(186, "home", "not mine,", "pass to ISP"), (326, "ISP", "not mine,", "pass it on"), (466, "Google", "I know that", "network")]
    prev = 72
    for i, (cx, name, a, b) in enumerate(routers):
        d.arrow([(prev, 78), (cx - 46, 78)])
        d.text((prev + cx - 46) / 2, 68, f"hop {i + 1}", "sub", 10, "middle", mono=True)
        d.rect(cx - 44, 50, 88, 56, "net", "nettint", 8, 1.6)
        d.home_router(cx, 52)
        d.text(cx, 124, name, "ink", 11.5, "middle", 600)
        d.text(cx, 140, "where next?", "net", 10.5, "middle", 600)
        d.text(cx, 155, a, "sub", 9.5, "middle")
        d.text(cx, 168, b, "sub", 9.5, "middle")
        prev = cx + 46
    d.arrow([(prev, 78), (566, 78)])
    d.text((prev + 566) / 2, 68, "hop 4", "sub", 10, "middle", mono=True)
    d.labelled(SRV, 600, 52, 48, "8.8.8.8", "arrived", sub_mono=False)
    save(d, "00-04/hop-by-hop.svg", "Traffic to 8.8.8.8 passing router to router")


# =============================================================== 0.5
def firewall_gate():
    d = D(660, 270)
    d.browser(40, 34, label="a visitor")
    d.labelled("resource/User", 76, 160, 44, "a stranger")
    d.firewall_wall(340, 54, 240)
    d.arrow([(116, 62), (340, 96), (520, 124)], "ok")
    d.ok(340, 96)
    d.pill(220, 58, "HTTPS :443", "ok", 104)
    d.path("M104 184 L332 160", "bad", 1.6, "5 4")
    d.bad(340, 158)
    d.pill(220, 196, "SSH :22", "bad", 84)
    d.labelled(SRV, 570, 96, 56, "web server")
    save(d, "00-05/firewall-gate.svg", "HTTPS on port 443 passes the firewall; SSH on port 22 is blocked")


def firewall_rule_anatomy():
    d = D(660, 330)
    parts = [("protocol", "TCP", "how is it", "carried?", "ink"), ("port", "443", "which", "service?", "ink"),
             ("source", "anywhere", "who is it", "from?", "ink"), ("action", "ALLOW", "let it", "through?", "ok")]
    for i, (h, v, a, b, c) in enumerate(parts):
        x = 30 + i * 154
        d.text(x + 65, 22, h, "sub", 10.5, "middle")
        d.numbox(x, 32, 130, 46, v, c, "panel" if c == "ink" else "panel", 15)
        d.path(f"M{x + 65} 80 L{x + 65} 92", "faint", 1.2)
        d.text(x + 65, 108, a, "sub", 10, "middle")
        d.text(x + 65, 122, b, "sub", 10, "middle")
    d.path("M30 146 L630 146", "faint", 1)
    d.text(30, 168, "a small rule list", "sub", 10.5)
    rows = [("TCP", "443", "anywhere", "ALLOW", "ok"), ("TCP", "22", "office IP only", "ALLOW", "ok"), ("any", "any", "everything else", "BLOCK", "bad")]
    for i, (pr, po, src, act, c) in enumerate(rows):
        y = 178 + i * 38
        d.rect(30, y, 600, 30, "bad" if c == "bad" else "faint", "badtint" if c == "bad" else "surface", 5, 1.2)
        for j, (t, cc) in enumerate(((pr, "ink"), (po, "ink"), (src, "ink"), (act, c))):
            d.text(95 + j * 154, y + 20, t, cc, 11, "middle", 600 if j == 3 else 400, mono=True)
    d.text(330, 312, "if no rule allows it, it's blocked", "bad", 10.5, "middle", 600)
    save(d, "00-05/firewall-rule-anatomy.svg", "A firewall rule's four parts, and a small rule list ending with block everything else")


def inbound_outbound():
    d = D(660, 160)
    d.browser(30, 40, label="a browser")
    d.arrow([(106, 66), (276, 66)])
    d.text(190, 56, "inbound", "ink", 11, "middle", 600, mono=True)
    d.labelled(SRV, 318, 38, 52, "your server")
    d.arrow([(352, 66), (500, 66)])
    d.text(426, 56, "outbound", "ink", 11, "middle", 600, mono=True)
    d.card(504, 40, 130, 52, "another service", "e.g. an update server", "ink", "surface", align="middle", size=11.5)
    d.text(330, 148, "in or out, from the server's point of view", "sub", 10.5, "middle")
    save(d, "00-05/inbound-outbound.svg", "Traffic arriving at a server is inbound; traffic leaving it is outbound")


def least_privilege():
    d = D(660, 330)
    d.labelled("resource/Globe", 64, 40, 48, "the internet", "anyone", sub_mono=False)
    d.labelled(LAPTOP, 64, 196, 48, "your laptop", "203.0.113.5")
    d.firewall_wall(300, 60, 290)
    d.server_closeup(400, 40, 240, 230, "web server", "one machine", [
        ("https", "443", "open"),
        ("ssh", "22", "you"),
        ("mysql", "3306", "none"),
    ], header_icon=SRV, os_label="Linux", frame="ink")
    d.arrow([(94, 70), (300, 120), (408, 128)], "ok")
    d.ok(300, 120)
    d.path("M94 78 L300 162", "bad", 1.6, "5 4")
    d.bad(300, 162)
    d.arrow([(94, 222), (300, 176), (408, 162)], "ok")
    d.ok(300, 176)
    d.text(520, 300, "nothing outside can reach 3306", "sub", 10.5, "middle")
    save(d, "00-05/least-privilege.svg", "The internet reaches 443, only your laptop reaches 22, and nothing outside reaches 3306")


def phase0_mental_model():
    d = D(660, 240)
    xs = [56, 166, 276, 386, 496, 606]
    d.pill(xs[0] + 6, 16, "inthelab.ie", "you", 96)
    d.browser(xs[0] - 34, 36, 68, 48)
    d.card(xs[1] - 38, 40, 76, 42, "DNS", None, "net", "nettint", "net", 13, "middle")
    d.rect(xs[2] - 32, 38, 64, 46, "net", None, 6, 1.4, "4 3")
    for r in range(2):
        for c in range(3):
            d.raw(f'<circle cx="{xs[2] - 16 + c * 16}" cy="{52 + r * 18}" r="3.2" class="f-{"you" if (r, c) == (1, 2) else "net"}"/>')
    d.rect(xs[3] - 40, 36, 80, 52, "net", "nettint", 8, 1.6)
    d.home_router(xs[3], 38)
    d.icon("resource/Firewall", xs[4] - 24, 36, 48)
    d.pill(xs[5], 30, "443", "ink", 50)
    d.icon(SRV, xs[5] - 20, 44, 40)
    d.path(f"M{xs[0]} 120 L{xs[5]} 120", "faint", 1.4)
    labels = [("you", "type a name", "in a browser"), ("DNS", "find the address", "203.0.113.10"), ("CIDR", "which network?", "203.0.113.0/24"),
              ("route", "choose next hop", "via routers"), ("firewall", "allow or block", "443 allowed"), ("port", "pick the service", ":443 HTTPS")]
    for i, x in enumerate(xs):
        d.step(x, 120, str(i + 1))
        d.text(x, 154, labels[i][0], "ink", 12, "middle", 600)
        d.text(x, 170, labels[i][1], "sub", 10.5, "middle")
        d.text(x, 185, labels[i][2], "sub", 10, "middle", mono=True)
        if i < 5:
            d.arrow([(x + 16, 120), (xs[i + 1] - 16, 120)], "faint")
    d.text(330, 222, "if any stop fails, the page never loads", "sub", 10.5, "middle")
    save(d, "00-05/phase-0-mental-model.svg", "Six steps of a request: name, DNS, CIDR, route, firewall, port")


ALL = [server_anatomy, capacity_vs_demand, virtualisation, service_models, regions_azs, shared_responsibility,
       home_network, private_public_ip, ports, protocol_stack, dns_lookup, request_journey, tcp_vs_udp,
       address_split, cidr_24, cidr_size_comparison, subnet_splitting,
       local_vs_remote, routing_table, longest_prefix_match, hop_by_hop,
       firewall_gate, firewall_rule_anatomy, inbound_outbound, least_privilege, phase0_mental_model]

if __name__ == "__main__":
    for f in ALL:
        f()
    print(len(ALL), "phase 0 diagrams")
