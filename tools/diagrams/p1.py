"""Phase 1 diagrams in the v2 system. Same file names as before."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dg import D

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "public", "images", "labs")
EC2 = "resource/AmazonEC2Instance"


def save(d, path, title):
    d.save(f"{OUT}/{path}", title)


def budget_alert():
    d = D(660, 240)
    d.path("M60 200 L620 200 M60 200 L60 24", "faint", 1.4)
    d.text(52, 28, "$", "sub", 11, "end")
    d.text(60, 220, "day 1", "sub", 10)
    d.text(620, 220, "day 30", "sub", 10, "end")
    d.path("M60 96 L620 96", "you", 2, "7 5")
    d.text(612, 88, "your budget: $10", "you", 11, "end", 600)
    d.path("M60 196 C 220 194, 280 170, 340 96 S 500 44, 620 36", "ink", 2.4)
    d.text(612, 28, "what you're spending", "ink", 11, "end", 600)
    d.raw('<circle cx="340" cy="96" r="7" class="f-bad"/>')
    d.path("M340 103 V149 H386", "bad", 1.4)
    d.rect(386, 122, 210, 54, "bad", "badtint", 8, 1.5)
    d.icon("resource/Email", 396, 131, 34)
    d.text(440, 145, "email: over budget", "bad", 11.5, weight=600)
    d.text(440, 161, "go and check what's running", "sub", 10)
    save(d, "01-01/budget-alert.svg", "Spending rises over the month and crosses the budget line, which sends an email alert")


def iam_decision():
    d = D(660, 220)
    d.labelled("resource/User", 46, 70, 44, "you", tint="you", label_c="you")
    d.pill(160, 92, "create a user group", "you", 150, mono=False, size=10.5, fill="youtint")
    d.arrow([(70, 92), (84, 92)])
    d.arrow([(236, 92), (276, 92)])
    d.rect(280, 52, 160, 80, "edge", "surface", 8, 1.6)
    d.icon("architecture-service/AWSIdentityandAccessManagement", 292, 64, 30)
    d.text(330, 84, "IAM", "ink", 13, weight=700)
    d.text(360, 108, "do any of your", "sub", 10.5, "middle")
    d.text(360, 122, "policies allow it?", "sub", 10.5, "middle")
    d.arrow([(440, 76), (470, 76), (470, 42), (500, 42)], "ok")
    d.text(486, 36, "yes", "ok", 10.5, "middle", 600)
    d.rect(504, 18, 140, 48, "ok", "oktint", 8, 1.5, glow=True)
    d.ok(522, 42, 8)
    d.text(538, 38, "it happens", "ok", 11.5, weight=600)
    d.text(538, 53, "group created", "sub", 10)
    d.arrow([(440, 112), (470, 112), (470, 152), (500, 152)], "bad")
    d.text(486, 146, "no", "bad", 10.5, "middle", 600)
    d.rect(504, 128, 140, 48, "bad", "badtint", 8, 1.5)
    d.bad(522, 152, 8)
    d.text(538, 148, "AccessDenied", "bad", 11.5, weight=600, mono=True)
    d.text(538, 163, "nothing changes", "sub", 10)
    d.text(330, 206, "if no policy allows the action, it's denied", "sub", 10.5, "middle")
    save(d, "01-02/iam-decision.svg", "IAM checks whether any of your policies allow the request. If not, it fails with AccessDenied")


def users_groups_policies():
    d = D(660, 330)
    for x, t in ((80, "users"), (300, "groups"), (530, "policies")):
        d.text(x, 20, t, "sub", 10.5, "middle")

    def policy(y, name):
        d.rect(450, y - 20, 180, 40, "net", "nettint", 6, 1.4)
        d.icon("resource/AWSIdentityAccessManagementPermissions", 458, y - 14, 28)
        d.text(494, y + 4, name, "net", 11, mono=True)

    for i, (who, grp, pol) in enumerate((("senior-dev", "admins", "AdministratorAccess"), ("junior-dev", "read-only", "ReadOnlyAccess"))):
        y = 72 + i * 80
        d.labelled("resource/User", 80, y - 26, 40, who)
        d.arrow([(110, y - 6), (226, y - 6)])
        d.text(168, y - 14, "member of", "sub", 9.5, "middle")
        d.card(230, y - 26, 140, 40, grp, None, "priv", "privtint", title_c="priv", align="middle", size=12)
        d.arrow([(370, y - 6), (446, y - 6)])
        d.text(408, y - 14, "has", "sub", 9.5, "middle")
        policy(y - 6, pol)
    d.path("M30 206 L630 206", "faint", 1, "4 4")
    d.labelled(EC2, 80, 222, 44, "an EC2 server")
    d.arrow([(110, 244), (226, 244)], "line", "5 4")
    d.text(168, 236, "borrows", "sub", 9.5, "middle")
    d.rect(230, 224, 140, 40, "cmp", "cmptint", 6, 1.4, "5 4")
    d.icon("resource/AWSIdentityAccessManagementRole", 238, 230, 28)
    d.text(274, 249, "role", "cmp", 12, weight=600)
    d.text(300, 282, "temporary, no password", "sub", 10, "middle")
    d.arrow([(370, 244), (446, 244)])
    policy(244, "read one S3 bucket")
    save(d, "01-02/users-groups-policies.svg", "Users get permissions through groups; services borrow a role")


def global_vs_regional():
    d = D(660, 330)
    d.group(16, 10, 628, 310, "cloud", "AWS Cloud")
    d.rect(34, 46, 592, 74, "net", "nettint", 8, 1.4)
    d.text(48, 66, "global: the same in every Region", "ink", 11.5, weight=600)
    for i, (t, ic) in enumerate((("IAM users", "architecture-service/AWSIdentityandAccessManagement"),
                                  ("billing", "architecture-service/AWSBillingConductor"),
                                  ("Route 53", "architecture-service/AmazonRoute53"))):
        x = 60 + i * 190
        d.icon(ic, x, 80, 26)
        d.text(x + 34, 98, t, "ink", 11.5, weight=500)
    regions = [("eu-west-1", "Ireland", True), ("us-east-1", "N. Virginia", False), ("eu-central-1", "Frankfurt", False)]
    for i, (code, name, mine) in enumerate(regions):
        x = 34 + i * 200
        d.group(x, 136, 192, 168, "region", code, None)
        d.text(x + 12, 176, name, "sub", 10.5)
        if mine:
            d.icon(EC2, x + 72, 194, 48)
            d.text(x + 96, 268, "your server lives here", "you", 10.5, "middle", 600)
        else:
            d.text(x + 96, 234, "nothing here", "faint", 11, "middle", 500)
    save(d, "01-03/global-vs-regional.svg", "Global services sit above the Regions. Only eu-west-1 contains your server")


def console_cli_api():
    d = D(660, 260)
    d.browser(30, 22, 90, 62, c="cmp", label="console", sub="you click")
    d.raw('<g class="r-term">')      # light mode: a dark terminal
    d.rect(30, 140, 90, 62, "priv", "privtint", 4, 1.8)
    d.text(44, 166, ">_", "priv", 16, weight=700, mono=True)
    d.path("M44 182 L100 182", "faint", 2)
    d.raw('</g>')
    d.text(75, 219, "CLI", "ink", 11.5, "middle", 500)
    d.text(75, 233, "you type", "sub", 10, "middle")
    d.arrow([(124, 53), (190, 53), (190, 100), (256, 100)], "cmp")
    d.arrow([(124, 171), (190, 171), (190, 136), (256, 136)], "priv")
    d.rect(260, 80, 170, 76, "net", "nettint", 8, 1.6, glow=True)
    d.icon("architecture-group/AWSCloudlogo", 272, 92, 24, keep_colour=True)
    d.text(304, 109, "AWS API", "net", 13, weight=700)
    d.icon("architecture-service/AWSIdentityandAccessManagement", 272, 122, 22)
    d.text(302, 138, "checks IAM, then acts", "sub", 10.5)
    d.arrow([(430, 118), (494, 118)], "net")
    d.icon(EC2, 500, 92, 46)
    d.icon("resource/AmazonSimpleStorageServiceBucketWithObjects", 566, 92, 46)
    d.text(565, 164, "your resources", "ink", 11.5, "middle", 500)
    d.text(330, 248, "two ways to ask, one place that answers", "sub", 10.5, "middle")
    save(d, "01-04/console-cli-api.svg", "The console and the CLI both send requests to the AWS API, which checks IAM and then acts")


def phase0_to_aws():
    rows = [
        ("one or more data centres", "Availability Zone", None),
        ("network", "VPC", "architecture-group/VirtualprivatecloudVPC"),
        ("subnet", "subnet", "architecture-group/Publicsubnet"),
        ("routing table", "route table", "resource/AmazonVPCRouter"),
        ("home router's internet link", "internet gateway", "resource/AmazonVPCInternetGateway"),
        ("firewall", "security group", None),
        ("server", "EC2 instance", "resource/AmazonEC2Instance"),
        ("sharing one public IP", "NAT gateway", "resource/AmazonVPCNATGateway"),
        ("DNS", "Route 53", "architecture-service/AmazonRoute53"),
    ]
    d = D(660, 28 + len(rows) * 38 + 10)
    L, R = 70, 380            # two centred columns, no "when" column
    d.text(L + 130, 18, "what you learned in Phase 0", "you", 11, "middle", 600)
    d.text(R + 105, 18, "what AWS calls it", "ink", 11, "middle", 600)
    for i, (left, right, ic) in enumerate(rows):
        y = 30 + i * 38
        d.rect(L, y, 260, 30, "you", "youtint", 6, 1.3)
        d.text(L + 130, y + 19, left, "you", 11, "middle", 500)
        d.arrow([(L + 266, y + 15), (R - 6, y + 15)], "faint")
        d.rect(R, y, 210, 30, "ink", "surface", 6, 1.3)
        if ic:
            d.icon(ic, R + 6, y + 3, 24, keep_colour=ic.startswith("architecture"))
        elif right == "Availability Zone":
            d.rect(R + 9, y + 6, 18, 18, "priv", None, 2, 1.4, "3 2")
        else:
            d.rect(R + 9, y + 6, 18, 18, "sub", None, 2, 1.6)
        d.text(R + 38, y + 19, right, "ink", 11.5, weight=500)
    save(d, "01-05/phase-0-to-aws.svg", "Phase 0 ideas and their AWS names")


ALL = [budget_alert, iam_decision, users_groups_policies, global_vs_regional, console_cli_api, phase0_to_aws]

if __name__ == "__main__":
    for f in ALL:
        f()
    print(len(ALL), "phase 1 diagrams")
