---
phase: 4
order: 4
title: How do I get in?
type: lab
time: ~35 min
cost: ~$0.03 an hour while running
buildsOn: Lab 4.3
summary: Reach your private server through a bastion host, using a security group as the source of a rule.
draft: false
questions:
  - kind: recall
    q: "What is a <b>bastion host</b>?"
    options:
      - "A server in a public subnet whose only job is to be the way in to private servers"
      - "A backup of your private server"
      - "A type of security group"
      - "The internet gateway's other name"
    correct: 0
    hint: "Which server did you SSH to first?"
    explain: "A bastion host sits in a public subnet and accepts SSH from a small set of addresses. You connect to it, and from there to private servers. It's the one controlled way in."

  - kind: cause
    q: "Why does the rule on <code>app-sg</code> use <code>bastion-sg</code> as its source, instead of the bastion's private IP?"
    options:
      - "Security groups can't use private IPs"
      - "It's faster"
      - "The rule follows any server in the group, so it keeps working if the bastion is replaced and gets a new IP"
      - "Private IPs change every minute"
    correct: 2
    hint: "What happens to the rule if you launch a new bastion?"
    explain: "A rule with a group as its source allows any server in that group, whatever its IP. Replace the bastion, or add a second one, and the rule still works without being edited."

  - kind: predict
    q: "You launch a second server and put it in <code>bastion-sg</code>. Can it SSH to <code>app-1</code> without changing <code>app-sg</code>?"
    options:
      - "No, you need to add its IP to app-sg"
      - "Yes, any server in bastion-sg is allowed"
      - "Only if it's in private-a"
      - "Only after a reboot"
    correct: 1
    hint: "The rule names a group, not a server."
    explain: "The rule allows SSH from anything in bastion-sg. Put another server in that group and it's allowed straight away. That's also why you only put servers in a group like this deliberately."
---

**What you'll do:** Launch a bastion host in `public-a`, connect through it to your private server, and allow that with a security group rule that names a group instead of an address.

---

## One way in

A **bastion host** is a small server in a public subnet whose only job is to be the way in. You SSH to the bastion, and from there to your private servers.

<div class="diagram">
  <img
    src="/images/labs/04-04/arch-bastion.svg"
    alt="Your laptop connects to the bastion in public-a, through the internet gateway. The bastion's security group allows port 22 from your IP. From the bastion, the connection continues to app-1 in private-a, whose security group allows port 22 from bastion-sg. Your key stays on your laptop."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">two hops: your laptop to the bastion, then the bastion to the private server</div>
</div>

Only the bastion is reachable from the internet, and only by you. Your private servers only accept SSH from the bastion.

## Step 1: Launch the bastion

The bastion only needs SSH, so it uses the standard Amazon Linux image, not your AMI.

1. In the EC2 console, choose **Instances**, then **Launch instances**.
2. **Name:** `{{ns}}-bastion`
3. **Application and OS Images:** leave **Amazon Linux 2023** selected.
4. **Instance type:** `t3.micro`
5. **Key pair:** `{{ns}}-key`
6. Under **Network settings**, choose **Edit**:
    1. **VPC:** `{{ns}}-vpc`
    2. **Subnet:** `{{ns}}-public-a`
    3. **Auto-assign public IP:** **Enable**
    4. **Firewall:** **Create security group**, named `{{ns}}-bastion-sg`, with the description `Bastion host security group`.
    5. Keep the SSH rule AWS adds, but change its **Source type** to **My IP**.
7. Choose **Launch instance**.

<div class="callout shot">screenshot: the bastion's network settings with public-a, a public IP, and an SSH rule from My IP<br>save as <code>/images/labs/04-04/bastion-network.png</code></div>
<!--
<figure class="screenshot">
  <img
    src="/images/labs/04-04/bastion-network.png"
    alt="The bastion's network settings with public-a, a public IP, and an SSH rule from My IP."
  />
</figure>
-->

When it's running, note down its **Public IPv4 address**.

## Step 2: Tell SSH about the bastion

Connecting through a bastion means two hops. Rather than typing both every time, you'll describe them once in SSH's **config file**, which SSH reads every time it connects.

Replace `203.0.113.10` with your bastion's public IP before you run the first command:

<div class="os-switch">
<div class="os-tabs"><button type="button" data-os-pick="mac">macOS / Linux</button><button type="button" data-os-pick="windows">Windows</button></div>
<div class="os-panel" data-os="mac">

1. Save your bastion's public IP:

```bash
BASTION_IP=203.0.113.10
```

2. Add the entries to your SSH config:

```bash
mkdir -p ~/.ssh
cat >> ~/.ssh/config <<EOF

Host bastion
    HostName $BASTION_IP
    User ec2-user
    IdentityFile ~/Downloads/{{ns}}-key.pem

Host 10.0.*
    User ec2-user
    IdentityFile ~/Downloads/{{ns}}-key.pem
    ProxyJump bastion
EOF
```

</div>
<div class="os-panel" data-os="windows">

1. Save your bastion's public IP:

```powershell
$BASTION_IP = "203.0.113.10"
```

2. Add the entries to your SSH config:

```powershell
mkdir -Force $HOME\.ssh | Out-Null
Add-Content -Path $HOME\.ssh\config -Value @"

Host bastion
    HostName $BASTION_IP
    User ec2-user
    IdentityFile ~/Downloads/{{ns}}-key.pem

Host 10.0.*
    User ec2-user
    IdentityFile ~/Downloads/{{ns}}-key.pem
    ProxyJump bastion
"@
```

</div>
</div>

<div class="callout why"><b>Already have an SSH config file?</b> These commands add to the end of it. Nothing already in it is changed.</div>

Here's what the two entries mean:

- **Host bastion:** a nickname. `ssh bastion` connects to your bastion's public IP, as `ec2-user`, with your key.
- **Host 10.0.\*:** any address in your VPC. SSH reaches it by going through the bastion first. That's what **ProxyJump** means.

Your key never leaves your computer. The bastion only passes the connection along, so you never copy your key onto a server.

## Step 3: Connect to the bastion

From now on, the commands are the same on every operating system:

```bash
ssh bastion
```

Type `yes` when it asks whether you trust the server. Your prompt shows the bastion's private IP, something like `[ec2-user@ip-10-0-1-20 ~]$`.

Log out again:

```bash
exit
```

## Step 4: Try the private server

Now connect to your app server's private IP, replacing `10.0.2.37` with yours:

```bash
ssh 10.0.2.37
```

It hangs. Give it 20 seconds, then press `Ctrl+C`.

<div class="callout break"><b>Think about it first.</b> The bastion got you inside your VPC, and the <code>local</code> route connects every subnet in it. So what's still stopping you?</div>

The firewall. `{{ns}}-app-sg` has no inbound rules, so it drops the bastion's connection.

## A group as the source

You could add a rule allowing SSH from the bastion's private IP. But if you ever replace the bastion, its IP changes, and the rule silently stops working.

A security group rule can name **another security group** as its source instead. It then allows traffic from any server in that group, whatever its IP.

<div class="diagram">
  <img
    src="/images/labs/04-04/sg-reference.svg"
    alt="app-sg has an inbound rule allowing SSH from bastion-sg. Any server in bastion-sg, such as bastion and bastion-2, is allowed in. A server that isn't in bastion-sg, web-1, is blocked."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the rule follows the group, not an address</div>
</div>

## Step 5: Allow SSH from the bastion

1. In the EC2 console, choose **Security Groups** and select `{{ns}}-app-sg`.
2. In the **Inbound rules** tab, choose **Edit inbound rules**, then **Add rule**.
3. **Type:** **SSH**
4. **Source:** **Custom**. Click in the box next to it, and choose `{{ns}}-bastion-sg` from the list. Its ID starts with `sg-`.
5. Choose **Save rules**.

<div class="callout shot">screenshot: the app-sg inbound rule allowing SSH with bastion-sg as the source<br>save as <code>/images/labs/04-04/app-sg-rule.png</code></div>
<!--
<figure class="screenshot">
  <img
    src="/images/labs/04-04/app-sg-rule.png"
    alt="The app-sg inbound rule allowing SSH with bastion-sg as the source."
  />
</figure>
-->

## Step 6: Connect, and check the app

Try again:

```bash
ssh 10.0.2.37
```

Type `yes` when asked. You're in. Your prompt shows `ip-10-0-2-37`, an address in `private-a`.

Now ask the app on this server for its page:

```bash
curl localhost
```

```text
Hello from ip-10-0-2-37 (eu-west-1a)
```

`localhost` means "this server". The app is running. It started on its own when the server booted, from your AMI, without downloading anything. Hold on to that.

Log out:

```bash
exit
```

<div class="callout why"><b>Bastions aren't perfect.</b> The bastion is a public server with port 22 open, another server to keep updated, and another place your key works. Plenty of teams have replaced them, and you will too, in the next phase.</div>

## Summary

- A bastion host is the one controlled way in to your private servers.
- Your SSH config takes you through it with `ssh bastion` or `ssh 10.0.x.x`.
- `{{ns}}-app-sg` allows SSH from `{{ns}}-bastion-sg`: any server in that group, whatever its IP.
- The app on `{{ns}}-app-1` is running, and only reachable from inside your VPC.

Keep both servers for the next lab. If you're taking a break, stop them. The bastion's public IP will change when you start it again; the end of the next lab shows you how to update it.
