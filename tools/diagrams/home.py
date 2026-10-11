"""Home page diagrams in the v2 system."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dg import D

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "public", "images", "home")
EC2 = "resource/AmazonEC2Instance"


def route_note(d, x, y):
    d.icon("resource/AmazonVPCRouter", x, y, 30)
    d.text(x + 38, y + 11, "route table", "sub", 10.5, weight=500)
    d.text(x + 38, y + 26, "10.0.0.0/16 → local", "ink", 10.5, mono=True)


def hero():
    """The core moment: a server you can't reach, then one route fixes it. Animated by the page."""
    d = D(560, 264)
    d.labelled("resource/Client", 40, 114, 44, "you")
    d.group(104, 16, 444, 240, "vpc", "your VPC", "10.0.0.0/16")
    d.icon("resource/AmazonVPCInternetGateway", 84, 116, 40)
    d.text(104, 172, "internet", "sub", 9.5, "middle")
    d.text(104, 183, "gateway", "sub", 9.5, "middle")
    d.group(164, 48, 368, 196, "public", "Subnet: public-a", "10.0.1.0/24")
    route_note(d, 180, 186)
    d.raw('<g id="route-missing">')
    d.text(218, 226, "0.0.0.0/0  → ?", "bad", 10.5, mono=True)
    d.raw('</g><g id="route-added" opacity="0">')
    d.text(218, 226, "0.0.0.0/0  → igw", "pub", 10.5, weight=600, mono=True)
    d.raw('</g>')
    d.group(396, 76, 120, 118, "sg", "web-sg")
    d.text(404, 105, "HTTP from anyone", "sec", 9.5)
    d.icon(EC2, 434, 114, 44)
    d.text(456, 176, "web-1", "ink", 11, "middle", 500)
    d.text(456, 188, "running", "ok", 9.5, "middle", 600)
    d.path("M126 136 L392 136", "faint", 1.4, "4 4")
    d.raw('<g id="fail" opacity="0">')
    d.bad(164, 136, 10)
    d.raw('</g><g id="pass" opacity="0">')
    d.ok(396, 136, 10)
    d.raw('</g>')
    d.raw('<circle id="packet" cx="66" cy="136" r="6" class="f-you" opacity="0"/>')
    d.save(f"{OUT}/hero.svg", "Your server is running, but you can't reach it, until one route is added")


def step_build():
    d = D(320, 180)
    d.group(16, 12, 288, 156, "public", "Subnet: public-a")
    d.icon(EC2, 138, 56, 44)
    d.text(160, 118, "web-1", "ink", 11.5, "middle", 500)
    d.text(160, 133, "running", "ok", 10, "middle", 600)
    d.save(f"{OUT}/step-build.svg", "A server running in a subnet you built")


def step_break():
    d = D(320, 180)
    d.icon("resource/Client", 14, 66, 40)
    d.group(116, 12, 188, 156, "public", "public-a")
    d.icon(EC2, 188, 64, 44)
    d.path("M58 86 L108 86", "bad", 1.6, "5 4")
    d.bad(116, 86, 9)
    d.text(210, 136, "connection timed out", "bad", 10.5, "middle", 600)
    d.save(f"{OUT}/step-break.svg", "Trying to connect, and timing out")


def step_fix():
    d = D(320, 180)
    d.icon("resource/Client", 14, 66, 40)
    d.group(116, 12, 188, 156, "public", "public-a")
    d.icon(EC2, 188, 52, 44)
    d.arrow([(58, 74), (184, 74)], "ok")
    d.ok(116, 74, 9)
    d.icon("resource/AmazonVPCRouter", 128, 118, 26)
    d.text(160, 129, "route table", "sub", 9.5)
    d.text(160, 145, "0.0.0.0/0 → igw", "pub", 10, weight=600, mono=True)
    d.save(f"{OUT}/step-fix.svg", "One route to the internet gateway, and it connects")


def final_architecture():
    d = D(660, 470)
    d.labelled("resource/Users", 42, 196, 44, "visitors")
    d.group(96, 10, 552, 450, "cloud", "AWS Cloud")
    # global services
    d.icon("architecture-service/AmazonRoute53", 112, 92, 36)
    d.text(130, 144, "Route 53", "ink", 10.5, "middle", 500)
    d.icon("architecture-service/AWSWAF", 112, 196, 36)
    d.text(130, 248, "WAF", "ink", 10.5, "middle", 500)
    d.icon("architecture-service/AWSCertificateManager", 112, 290, 36)
    d.text(130, 342, "HTTPS", "ink", 10.5, "middle", 500)
    # region, VPC, AZs
    d.group(172, 44, 464, 352, "region", "Europe (Ireland) eu-west-1")
    d.group(188, 78, 434, 306, "vpc", "your VPC")
    for i, az in enumerate(("Availability Zone A", "Availability Zone B")):
        x = 228 + i * 196
        d.group(x, 106, 184, 268, "az", az)
        d.group(x + 10, 134, 164, 96, "public", "Public subnet")
        nx = x + 22 if i == 0 else x + 132
        d.icon("resource/AmazonVPCNATGateway", nx, 176, 30)
        d.text(nx + 15, 220, "NAT", "sub", 9.5, "middle")
        d.group(x + 10, 240, 164, 124, "private", "Private subnet")
    d.icon("resource/AmazonVPCInternetGateway", 168, 178, 40)
    # load balancer across both public subnets
    d.rect(372, 160, 92, 60, "net", "panel", 6, 1.4)
    d.icon("resource/ElasticLoadBalancingApplicationLoadBalancer", 400, 164, 36)
    d.text(418, 214, "load balancer", "ink", 9.5, "middle", 500)
    # auto scaling group across both private subnets
    d.group(252, 268, 344, 88, "asg", "Auto Scaling group")
    for x in (318, 514):
        d.icon(EC2, x - 20, 298, 40)
    # flows
    d.arrow([(66, 216), (110, 214)])
    d.arrow([(150, 214), (168, 200)])
    d.arrow([(208, 198), (370, 190)])
    d.arrow([(400, 222), (330, 296)])
    d.arrow([(436, 222), (506, 296)])
    d.path("M66 206 L110 120", "faint", 1.3, "4 3")
    # how it's run
    d.icon("architecture-service/AmazonCloudWatch", 188, 410, 30)
    d.text(226, 430, "watched by CloudWatch", "ink", 10.5, weight=500)
    d.icon("architecture-service/AWSCloudFormation", 420, 410, 30)
    d.text(458, 430, "built by CloudFormation", "ink", 10.5, weight=500)
    d.save(f"{OUT}/final-architecture.svg", "The final architecture: DNS, HTTPS and a firewall in front of a load balancer, servers in private subnets across two Availability Zones, scaling automatically, watched and built from code")


if __name__ == "__main__":
    for f in (hero, step_build, step_break, step_fix, final_architecture):
        f()
    print("home diagrams done")
