---
phase: 4
order: 3
title: Launch a server nobody can reach
type: lab
time: ~20 min
cost: ~$0.01 an hour while running
buildsOn: Lab 4.2
summary: Launch your app from your AMI into the private subnet, and find out that nobody can reach it, including you.
draft: false
questions:
  - kind: recall
    q: "Why does <code>app-1</code> show no <b>Public IPv4 address</b>?"
    options:
      - "Private subnets delete public IPs"
      - "You disabled Auto-assign public IP when you launched it"
      - "AMIs can't have public IPs"
      - "The security group hides it"
    correct: 1
    hint: "Look at the network settings you chose."
    explain: "You set Auto-assign public IP to Disable, so the server only has a private IP from private-a's range. That's half of what makes it private. The other half is the subnet's route table."

  - kind: cause
    q: "You try to SSH to <code>10.0.2.37</code> from your laptop, and it times out. Why?"
    options:
      - "The address is wrong"
      - "SSH is blocked on private servers"
      - "10.0.2.37 is a private address, so nothing on the internet knows how to reach it"
      - "The key file only works on public servers"
    correct: 2
    hint: "Where does your laptop send traffic for an address outside your home network?"
    explain: "Your laptop sends it to your home router, which sends it to your internet provider. Private addresses aren't routed across the internet, so it goes nowhere. Inside your VPC, 10.0.2.37 is reachable. Outside it, the address means nothing."

  - kind: predict
    q: "Is the hello app running on <code>app-1</code> right now, even though nobody can reach it?"
    options:
      - "Yes, it was on the AMI and starts on its own when the server boots"
      - "No, you need to log in and start it"
      - "No, apps don't run on private servers"
      - "Only once a public IP is added"
    correct: 0
    hint: "What was on the disk when you made the AMI?"
    explain: "The AMI copied a disk with the app installed and its service enabled. So app-1 started the app on its first boot, with nothing to download. You'll check this in the next lab."
---

**What you'll do:** Launch your app into `private-a` from the AMI you made, then try to reach it.

---

## Start clean

This phase could be days after the last one. First, check nothing from the last phase is still running:

1. In the EC2 console, choose **Instances**.
2. If any servers are still **Running** or **Stopped**, select them, then choose **Instance state**, **Terminate (delete) instance**.

Keep your AMI, `{{ns}}-web-ami`. You're about to use it.

## Step 1: Launch from your AMI

Your AMI already has the app installed and set to start on boot. That matters here: a server in `private-a` won't be able to download anything.

1. In the left menu, choose **AMIs**.
2. Select `{{ns}}-web-ami`, then choose **Launch instance from AMI**.
3. **Name:** `{{ns}}-app-1`
4. **Instance type:** `t3.micro`
5. **Key pair:** `{{ns}}-key`

## Step 2: Network settings

1. Under **Network settings**, choose **Edit**.
2. **VPC:** `{{ns}}-vpc`
3. **Subnet:** `{{ns}}-private-a`
4. **Auto-assign public IP:** **Disable**
5. **Firewall (security groups):** **Create security group**
6. **Security group name:** `{{ns}}-app-sg`
7. **Description:** `App server security group`
8. Choose **Remove** next to the SSH rule AWS adds, so the security group has no inbound rules.
9. Choose **Launch instance**.

<div class="callout shot">screenshot: the network settings with private-a selected, Auto-assign public IP disabled and app-sg with no rules<br>save as <code>/images/labs/04-03/network-settings.png</code></div>
<!--
<figure class="screenshot">
  <img
    src="/images/labs/04-03/network-settings.png"
    alt="The network settings with private-a selected, Auto-assign public IP disabled and app-sg with no rules."
  />
</figure>
-->

## Step 3: Look at its addresses

Wait until `{{ns}}-app-1` is **Running**, then select it.

- **Public IPv4 address:** empty.
- **Private IPv4 addresses:** something like `10.0.2.37`, from `private-a`'s range.

Note down the private IP. You'll use it for the rest of this phase.

<div class="callout shot">screenshot: the instance details showing a private IP and no public IPv4 address<br>save as <code>/images/labs/04-03/no-public-ip.png</code></div>
<!--
<figure class="screenshot">
  <img
    src="/images/labs/04-03/no-public-ip.png"
    alt="The instance details showing a private IP and no public IPv4 address."
  />
</figure>
-->

## Step 4: Try to connect

There's no public IP, so the only address you have is the private one. Try SSH with it, replacing `10.0.2.37` with your server's private IP:

<div class="os-switch">
<div class="os-tabs"><button type="button" data-os-pick="mac">macOS / Linux</button><button type="button" data-os-pick="windows">Windows</button></div>
<div class="os-panel" data-os="mac">

```bash
ssh -o ConnectTimeout=10 -i ~/Downloads/{{ns}}-key.pem ec2-user@10.0.2.37
```

</div>
<div class="os-panel" data-os="windows">

```powershell
ssh -o ConnectTimeout=10 -i $HOME\Downloads\{{ns}}-key.pem ec2-user@10.0.2.37
```

</div>
</div>

After 10 seconds, it gives up:

```text
ssh: connect to host 10.0.2.37 port 22: Connection timed out
```

## Why you can't reach it

`10.0.2.37` is a private address. It only means something inside your VPC.

Your laptop sends traffic for it to your home router, which passes it to your internet provider. Nobody on the internet routes private addresses, so it goes nowhere. Even if it could get there, `{{ns}}-app-sg` allows nothing in.

<div class="diagram">
  <img
    src="/images/labs/04-03/arch-unreachable.svg"
    alt="Your laptop tries to reach 10.0.2.37 and is blocked before reaching AWS, because the address isn't on the internet. app-1 sits in private-a with no public IP, a security group that allows nothing in, and a route table with only the local route."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">no address leads here, and no route leads out</div>
</div>

<div class="callout break"><b>This isn't a problem to fix.</b> It's the point. Your app is running right now, and nobody on the internet can reach it.</div>

You still need to manage the server, though. That's the next lab.

## Summary

- `{{ns}}-app-1` runs in `private-a`, launched from your AMI.
- It has no public IP, and its subnet has no route to the internet.
- Nobody on the internet can reach it, including you.

Keep the server for the next lab. If you're taking a break, stop it.
