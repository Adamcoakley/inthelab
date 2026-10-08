---
phase: 3
order: 1
title: Launch a server you can't reach
type: lab
time: ~30 min
cost: ~$0.02 an hour while running
buildsOn: Lab 2.3
summary: Launch your first EC2 server into your own subnet, try to connect, and find out why you can't.
draft: false
questions:
  - kind: recall
    q: "What is an <b>AMI</b>?"
    options:
      - "The amount of CPU and memory a server has"
      - "The firewall around a server"
      - "The image a server is created from"
      - "The file you log in with"
    correct: 2
    hint: "It decides which operating system your server runs."
    explain: "An AMI (Amazon Machine Image) is the starting image: the operating system and anything pre-installed. CPU and memory come from the instance type, the firewall is the security group, and the file you log in with is the key pair."

  - kind: cause
    q: "You launch a server without enabling <b>Auto-assign public IP</b>. Why can't anyone on the internet reach it?"
    options:
      - "It only has a private IP, which the internet can't route to"
      - "The instance type is too small"
      - "Private IPs are blocked by the security group"
      - "The AMI doesn't support the internet"
    correct: 0
    hint: "Lab 0.2: which kind of address works across the internet?"
    explain: "A private IP like 10.0.1.23 only has meaning inside your VPC. Without a public IP, there's no address on the internet that leads to your server at all."

  - kind: predict
    q: "You lose your <code>.pem</code> key file. What happens the next time you try to SSH in?"
    options:
      - "You can download it again from the EC2 console"
      - "AWS emails you a copy"
      - "SSH works without it from the same laptop"
      - "You can't log in with that key pair, because AWS never kept a copy"
    correct: 3
    hint: "AWS shows a warning when you download it."
    explain: "AWS only keeps the public half of the key pair, which sits on the server. The private half exists only in the file you downloaded. Lose it, and that key pair can't be used to log in again."
---

**What you'll do:** Launch your first server into `{{ns}}-public-a`, try to connect to it, and work out why you can't.

---

## What you choose when you launch a server

Launching a server in AWS means making six choices. You'll make each one in this lab.

<div class="diagram">
  <img
    src="/images/labs/03-01/what-you-choose.svg"
    alt="Six cards around a server: AMI, the starting disk image; instance type, CPU and memory; key pair, how you prove it's you; network, where it lives; public IP, how the internet finds it; and security group, what can reach it."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">six choices make a server</div>
</div>

- **AMI:** the disk image the server starts from, including its operating system. You'll use Amazon Linux 2023.
- **Instance type:** how much CPU and memory you rent. You'll use `t3.micro`: 2 virtual CPUs and 1 GiB of memory.
- **Key pair:** how you prove it's you when you log in.
- **Network:** which VPC and subnet the server goes into.
- **Public IP:** whether the server gets an address on the internet.
- **Security group:** the firewall around the server.

A server running in AWS is called an **instance**. The service is **EC2** (Elastic Compute Cloud).

## Step 1: Start the launch

1. Check the Region selector says **eu-west-1**.
2. Search for **EC2** and open it.
3. Choose **Instances** in the left menu, then **Launch instances**.
4. **Name:** `{{ns}}-web-1`
5. **Application and OS Images:** leave **Amazon Linux 2023** selected. It's marked **Free tier eligible**. Leave the architecture as **64-bit (x86)**.
6. **Instance type:** `t3.micro`

<figure class="screenshot">
  <img
    src="/images/labs/03-01/launch-name-ami.png"
    alt="The top of the launch page with the name, Amazon Linux 2023 and t3.micro selected."
  />
</figure>

## Step 2: Create a key pair

A **key pair** works like a lock and key. AWS puts the lock on your server, and you download the only copy of the key.

1. Under **Key pair (login)**, choose **Create new key pair**.
2. **Key pair name:** `{{ns}}-key`
3. **Key pair type:** **RSA**
4. **Private key file format:** `.pem`
5. Choose **Create key pair**. The file `{{ns}}-key.pem` downloads.

<div class="callout break"><b>Keep this file safe.</b> AWS doesn't keep a copy. If you lose it, you can't log in with this key pair again. Anyone who has it can log in to your servers, so never share it or commit it to Git.</div>

## Step 3: Network settings

1. Under **Network settings**, choose **Edit**.
2. **VPC:** `{{ns}}-vpc`
3. **Subnet:** `{{ns}}-public-a`
4. **Auto-assign public IP:** **Enable**

Subnets you create yourself don't give out public IPs by default. Without one, your server would have no address on the internet at all.

5. **Firewall (security groups):** **Create security group**
6. **Security group name:** `{{ns}}-web-sg`
7. **Description:** `Web server security group`
8. AWS adds an SSH rule allowing access from anywhere. Choose **Remove** next to it, so the security group has no inbound rules at all. You'll add exactly what's needed in Lab 3.3.

<figure class="screenshot">
  <img
    src="/images/labs/03-01/network-settings.png"
    alt="The network settings with the VPC, subnet, auto-assign public IP and new security group with no rules."
  />
</figure>

## Step 4: Launch it

1. Leave **Configure storage** as the default 8 GiB disk.
2. Choose **Launch instance**, then **View all instances**.
3. Wait until **Instance state** says **Running** and **Status check** shows the checks have passed. This takes a minute or two.
4. Select your instance. In the **Details** tab, find the **Public IPv4 address** and **Private IPv4 addresses**.

<figure class="screenshot">
  <img
    src="/images/labs/03-01/instance-details.png"
    alt="The instance details showing the public and private IPv4 addresses."
  />
</figure>

The private IP is from your subnet's range. The public IP is the address the internet will use.

<div class="callout why"><b>This server costs money while it runs.</b> About $0.02 an hour, which comes out of your Free plan credits. If you're taking a break between labs, select it and choose <b>Instance state</b>, then <b>Stop instance</b>. Its public IP will change when you start it again, and Lab 3.7 shows why.</div>

## Step 5: Try to connect

**SSH** lets you log in to the server's command line from your own terminal. Choose your operating system:

<div class="os-switch">
<div class="os-tabs"><button type="button" data-os-pick="mac">macOS / Linux</button><button type="button" data-os-pick="windows">Windows</button></div>
<div class="os-panel" data-os="mac">

1. Open **Terminal**.
2. Lock down the key file. SSH refuses to use a key that other users can read:

```bash
chmod 400 ~/Downloads/{{ns}}-key.pem
```

3. Connect, replacing `PUBLIC_IP` with your server's public IP:

```bash
ssh -o ConnectTimeout=10 -i ~/Downloads/{{ns}}-key.pem ec2-user@PUBLIC_IP
```

</div>
<div class="os-panel" data-os="windows">

1. Open **PowerShell**.
2. Connect, replacing `PUBLIC_IP` with your server's public IP:

```powershell
ssh -o ConnectTimeout=10 -i $HOME\Downloads\{{ns}}-key.pem ec2-user@PUBLIC_IP
```

<div class="callout why"><b>Windows says the key is unprotected?</b> Run this in PowerShell, then try again:<br><code>icacls $HOME\Downloads\{{ns}}-key.pem /inheritance:r /grant:r "$($env:USERNAME):(R)"</code></div>

</div>
</div>

After 10 seconds, it gives up:

```text
ssh: connect to host 54.170.12.9 port 22: Connection timed out
```

Nothing came back at all.

## Step 6: Check the stops in order

You previously learned to check each stop a request makes, in order. Do that now.

1. **DNS:** you used an IP address directly, so DNS isn't involved.
2. **IP address:** the server has a public IP. That's fine.
3. **Route:** open **VPC**, then **Route tables**, then `{{ns}}-public-rt`, then the **Routes** tab.

There's only the `local` route. Nothing sends traffic to the internet gateway you created, so your server has no way to reply to anything outside the VPC.

<div class="diagram">
  <img
    src="/images/labs/03-01/arch-cant-reach.svg"
    alt="Your laptop tries to connect on port 22. Traffic reaches the internet gateway but is blocked at the edge of the public-a subnet, because the route table has no 0.0.0.0/0 route. The server's security group also allows nothing in."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the first broken stop: no route between your subnet and the internet</div>
</div>

That's not the only problem. The security group has no inbound rules, so it would block you too. We'll fix this in the next lab.

## Summary

- An EC2 instance is built from an AMI, an instance type, a key pair, a network, a public IP setting and a security group.
- `{{ns}}-web-1` is running in `public-a`, with a public and a private IP.
- You can't connect, and the first reason is the route table.

Keep the server for the next lab. If you're taking a break, stop it.
