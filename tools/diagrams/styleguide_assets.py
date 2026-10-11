import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from dg import D, TOKENS, site_css

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "public", "images", "style")


# ---------------------------------------------------------------- example 1: concept (Phase 0.5)
def least_privilege():
    d = D(660, 330)
    d.labelled("resource/Globe", 64, 40, 48, "the internet", "anyone", sub_mono=False)
    d.labelled("resource/Client", 64, 196, 48, "your laptop", "203.0.113.5")
    d.firewall_wall(300, 60, 290)
    d.server_closeup(400, 40, 240, 230, "web server", "one machine", [
        ("https", "443", "open"),
        ("ssh", "22", "you"),
        ("mysql", "3306", "none"),
    ])
    # rows sit at y = 114, 148, 182 (centres 128, 162, 196)
    d.arrow([(94, 70), (300, 120), (408, 128)], "ok")
    d.ok(300, 120)
    d.path("M94 78 L300 162", "bad", 1.6, "5 4")
    d.bad(300, 162)
    d.arrow([(94, 222), (300, 176), (408, 162)], "ok")
    d.ok(300, 176)
    d.text(520, 300, "nothing outside can reach 3306", "sub", 10.5, "middle")
    d.save(f"{OUT}/example-concept.svg", "Least privilege: one firewall, three levels of access")


# ---------------------------------------------------------------- example 2: architecture (Phase 4.4)
def bastion():
    d = D(660, 482)
    d.labelled("resource/Client", 44, 176, 48, "your laptop", "your IP")
    d.group(96, 10, 552, 462, "cloud", "AWS Cloud")
    d.group(112, 46, 524, 414, "region", "Europe (Ireland) eu-west-1")
    d.group(140, 82, 482, 366, "vpc", "your VPC", "10.0.0.0/16")
    d.icon("resource/AmazonVPCInternetGateway", 118, 178, 44)
    d.text(140, 236, "internet", "sub", 10, "middle")
    d.text(140, 248, "gateway", "sub", 10, "middle")
    d.group(196, 112, 410, 156, "public", "Public subnet: public-a", "10.0.1.0/24")
    d.group(196, 280, 410, 156, "private", "Private subnet: private-a", "10.0.2.0/24")

    def route(x, y, last, last_c):
        d.icon("resource/AmazonVPCRouter", x, y, 30)
        d.text(x + 38, y + 11, "route table", "sub", 10.5, weight=500)
        d.text(x + 38, y + 26, "10.0.0.0/16 → local", "ink", 10.5, mono=True)
        d.text(x + 38, y + 40, last, last_c, 10.5, mono=True)
    route(212, 218, "0.0.0.0/0  → igw", "pub")
    route(212, 386, "nothing else", "sub")

    def inst(x0, y0, name, ip, sg, rule):
        d.group(x0, y0, 130, 120, "sg", sg)
        d.text(x0 + 8, y0 + 29, rule, "sec", 9.5)
        d.icon("resource/AmazonEC2Instance", x0 + 43, y0 + 38, 44)
        d.text(x0 + 65, y0 + 98, name, "ink", 11.5, "middle", 500)
        d.text(x0 + 65, y0 + 111, ip, "sub", 10, "middle", mono=True)
    inst(462, 140, "bastion", "10.0.1.20", "bastion-sg", "SSH from your IP")
    inst(462, 308, "app-1", "10.0.2.37", "app-sg", "SSH from bastion-sg")

    d.arrow([(70, 200), (118, 200)])
    d.arrow([(162, 200), (503, 200)])
    d.step(330, 200, "1")
    d.arrow([(527, 262), (527, 306)])
    d.step(505, 284, "2")
    d.save(f"{OUT}/example-architecture.svg", "Reaching a private server through a bastion host")


# ---------------------------------------------------------------- example 3: close-up (Phase 3.6)
def inside_server():
    d = D(660, 236)
    d.labelled("resource/Client", 62, 118, 48, "your browser")
    d.server_closeup(190, 20, 450, 196, "EC2 instance: web-1", "t3.micro", [
        ("sshd", ":22", "open"),
        ("python3 hello-server.py", ":80", "open"),
    ], ip="10.0.1.23", disk="8 GiB at /")
    d.arrow([(92, 142), (198, 142)])
    d.text(145, 134, "request to :80", "sub", 10, "middle", mono=True)
    d.save(f"{OUT}/example-closeup.svg", "Inside an EC2 instance: the OS, its processes and ports, network card and disk")


# ---------------------------------------------------------------- asset tiles for the guide
def tile(name, draw, w=120, h=96):
    d = D(w, h)
    draw(d)
    d.save(f"{OUT}/assets/{name}.svg")


ICON_TILES = [
    # (file, label, icon)
    ("ec2", "EC2 instance", "resource/AmazonEC2Instance"),
    ("igw", "Internet gateway", "resource/AmazonVPCInternetGateway"),
    ("nat", "NAT gateway", "resource/AmazonVPCNATGateway"),
    ("router", "Route table", "resource/AmazonVPCRouter"),
    ("nacl", "Network ACL", "resource/AmazonVPCNetworkAccessControlList"),
    ("alb", "Load balancer", "resource/ElasticLoadBalancingApplicationLoadBalancer"),
    ("ami", "AMI", "resource/AmazonEC2AMI"),
    ("ebs", "EBS volume", "resource/AmazonElasticBlockStoreVolume"),
    ("s3", "S3 bucket", "resource/AmazonSimpleStorageServiceBucketWithObjects"),
    ("role", "IAM role", "resource/AWSIdentityAccessManagementRole"),
    ("client", "Laptop", "resource/Client"),
    ("user", "Person", "resource/User"),
    ("globe", "The internet", "resource/Globe"),
    ("server", "Server (non-AWS)", "resource/Server"),
    ("firewall", "Firewall", "resource/Firewall"),
    ("phone", "Phone", "resource/Mobileclient"),
]


def assets():
    for f, label, ic in ICON_TILES:
        tile(f, lambda d, ic=ic, label=label: (d.icon(ic, 38, 10, 44), d.text(60, 78, label, "ink", 11, "middle", 500)))
    tile("router-home", lambda d: (d.home_router(60, 8), d.text(60, 78, "Home router", "ink", 11, "middle", 500)))
    tile("packet", lambda d: (d.packet(45, 22), d.text(60, 78, "Packet", "ink", 11, "middle", 500)))

    groups = [("g-cloud", "cloud", "AWS Cloud"), ("g-region", "region", "Region"), ("g-vpc", "vpc", "VPC"),
              ("g-az", "az", "Availability Zone"), ("g-public", "public", "Public subnet"),
              ("g-private", "private", "Private subnet"), ("g-sg", "sg", "Security group"), ("g-asg", "asg", "Auto Scaling group")]
    for f, kind, label in groups:
        tile(f, lambda d, kind=kind, label=label: d.group(6, 6, 188, 70, kind, label), w=200, h=84)

    # lines and marks
    tile("m-flow", lambda d: (d.arrow([(14, 40), (106, 40)]), d.text(60, 78, "Traffic", "ink", 11, "middle", 500)))
    tile("m-blocked", lambda d: (d.path("M14 40 L80 40", "bad", 1.6, "5 4"), d.bad(92, 40), d.text(60, 78, "Blocked", "ink", 11, "middle", 500)))
    tile("m-ok", lambda d: (d.arrow([(14, 40), (106, 40)], "ok"), d.ok(60, 40), d.text(60, 78, "Allowed", "ink", 11, "middle", 500)))
    tile("m-step", lambda d: (d.step(44, 40, "1"), d.step(76, 40, "2"), d.text(60, 78, "Numbered steps", "ink", 11, "middle", 500)))

    # the two server versions side by side
    d = D(560, 230)
    d.icon("resource/AmazonEC2Instance", 40, 70, 56)
    d.text(68, 146, "in architecture", "ink", 11, "middle", 500)
    d.text(68, 160, "diagrams", "ink", 11, "middle", 500)
    d.server_closeup(170, 10, 380, 210, "EC2 instance: web-1", "t3.micro",
                     [("python3 hello-server.py", ":80", "open"), ("sshd", ":22", "open")], ip="10.0.1.23", disk="8 GiB")
    d.save(f"{OUT}/assets/servers.svg")


if __name__ == "__main__":
    least_privilege(); bastion(); inside_server(); assets()
    if "--css" in sys.argv:  # print the theme tokens that live in global.css
        print(site_css())
    print("style guide assets done")
