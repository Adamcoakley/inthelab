---
phase: 3
order: 3
title: Why can't I connect?
type: lab
time: ~20 min
cost: ~$0.02 an hour while running
buildsOn: Lab 3.2
summary: Open the security group to SSH from your IP only, and log in to your server for the first time.
draft: false
questions:
  - kind: recall
    q: "A security group rule has the source <code>86.44.12.7/32</code>. What does it allow?"
    options:
      - "Every address starting with 86.44"
      - "32 different addresses"
      - "Every address on the internet"
      - "Exactly one address: 86.44.12.7"
    correct: 3
    hint: "Lab 0.3: how many bits are left for devices in a /32?"
    explain: "A /32 uses all 32 bits for the network, leaving none for devices. So it matches exactly one address. That's what My IP creates."

  - kind: cause
    q: "You allowed SSH from <b>My IP</b> at home. At a café, SSH times out. Why?"
    options:
      - "SSH doesn't work on public Wi-Fi"
      - "The café's network has a different public IP, which the rule doesn't allow"
      - "The key file only works on your home network"
      - "AWS blocks connections from cafés"
    correct: 1
    hint: "Which address did My IP fill in?"
    explain: "My IP filled in your home's public IP. At the café, your traffic comes from the café's public IP instead, so the rule doesn't match and the security group drops it. Update the rule to your new IP."

  - kind: predict
    q: "Your security group has an inbound SSH rule, and you never touched the outbound rules. Will the server's replies reach you?"
    options:
      - "Yes, security groups remember the connection and let the replies out"
      - "No, you need an outbound rule for port 22"
      - "Only if the server has a second security group"
      - "No, replies need an inbound rule on your laptop"
    correct: 0
    hint: "Did you add an outbound rule before you connected?"
    explain: "Security groups are stateful. When they allow a connection in, they automatically allow its replies back out. You'll see a firewall that doesn't do this in Lab 3.5."
---

**What you'll do:** Add a security group rule that lets only you connect over SSH, and log in to your server.

---

## The firewall around your server

A **security group** is a firewall wrapped around your server. It checks every connection against a list of rules. Each rule says which **protocol** (like TCP), which **port** (like 22 for SSH) and which **source** (where the traffic comes from) is allowed in.

Two defaults matter:

- **Inbound:** everything is blocked unless a rule allows it. Yours has no rules, so everything is blocked.
- **Outbound:** everything is allowed. Your server can start connections to anywhere.

## Only you need SSH

SSH gives full control of your server, so only you should be able to reach port 22. When you choose **My IP** as the source, the console fills in your current public IP with `/32` on the end.

A `/32` uses all 32 bits for the network, leaving none for devices. So it matches exactly one address: yours.

## Step 1: Allow SSH from your IP

1. In the EC2 console, choose **Security Groups** in the left menu.
2. Select `{{ns}}-web-sg` and open the **Inbound rules** tab.
3. Choose **Edit inbound rules**, then **Add rule**.
4. **Type:** **SSH**. The protocol and port fill in as TCP and 22.
5. **Source:** **My IP**
6. Choose **Save rules**.


<figure class="screenshot">
  <img
    src="/images/labs/03-03/ssh-rule.png"
    alt="The inbound rule for SSH with the source set to My IP."
  />
</figure>

## Step 2: Connect

Run the SSH command again:

<div class="os-switch">
<div class="os-tabs"><button type="button" data-os-pick="mac">macOS / Linux</button><button type="button" data-os-pick="windows">Windows</button></div>
<div class="os-panel" data-os="mac">

```bash
ssh -i ~/Downloads/{{ns}}-key.pem ec2-user@PUBLIC_IP
```

</div>
<div class="os-panel" data-os="windows">

```powershell
ssh -i $HOME\Downloads\{{ns}}-key.pem ec2-user@PUBLIC_IP
```

</div>
</div>

The first time, SSH asks whether you trust this server:

```text
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

Type `yes`. SSH remembers the server, so it won't ask again.

You're in. Your prompt changes to something like:

```text
[ec2-user@ip-10-0-1-23 ~]$
```

Look at the name: it's built from the server's **private** IP, not the public one you typed. You'll find out why later in this phase.

<div class="diagram">
  <img
    src="/images/labs/03-03/arch-ssh-allowed.svg"
    alt="The full path from your laptop on port 22: through the internet gateway, across the public subnet using the 0.0.0.0/0 route, and through the security group, which allows 22 from your IP."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the route gets you there, the security group lets you in</div>
</div>

<div class="callout why"><b>Routing got your traffic there. The security group let it in.</b> Both had to be right. When something doesn't connect, those are two separate questions.</div>

## You never added an outbound rule

When your server replies to your laptop, that reply is outbound traffic. You never added a rule allowing it, but it got through anyway.

Security groups are **stateful**: when they allow a connection in, they remember it, and let its replies back out automatically.

## Step 3: Log out

```bash
exit
```

<div class="callout break"><b>SSH stopped working on another day?</b> Your home's public IP can change, and the rule only allows the old one. Edit the rule and choose <b>My IP</b> again.</div>

## Summary

- A security group blocks all inbound traffic unless a rule allows it.
- Your rule allows SSH only from your IP, a single address written as `/32`.
- Security groups are stateful, so replies get out without an outbound rule.
- You've logged in to your server for the first time.

Keep the server for the next lab. If you're taking a break, stop it.
