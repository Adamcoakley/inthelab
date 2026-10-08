---
phase: 3
order: 6
title: What's inside the server?
type: lab
time: ~25 min
cost: ~$0.02 an hour while running
buildsOn: Lab 3.5
summary: Look around inside your server, find the app's process and port, and see why the server doesn't know its own public IP.
draft: false
questions:
  - kind: recall
    q: "Which command shows which programs are listening on which ports?"
    options:
      - "df -h"
      - "sudo ss -tlnp"
      - "free -h"
      - "ip addr"
    correct: 1
    hint: "Lab 0.2: the port finds the service. This command shows that link."
    explain: "ss lists network connections. -t is TCP, -l is listening, -n shows numbers instead of names, and -p shows the program. sudo lets it see every program's name."

  - kind: cause
    q: "Why does <code>ip addr</code> show <code>10.0.1.23</code> but not your server's public IP?"
    options:
      - "The public IP is hidden for security"
      - "ip addr only shows private addresses"
      - "The internet gateway swaps the public IP for the private one, so the public IP is never on the server"
      - "The public IP changes too often to show"
    correct: 2
    hint: "Where does the address get swapped?"
    explain: "The public IP only exists at the internet gateway. It swaps the public address for the private one on the way in, and back again on the way out. The server only ever sees its private address."

  - kind: predict
    q: "You reload your website, then run <code>journalctl -u hello</code>. The newest line starts with <code>86.44.12.7</code>. Whose address is that?"
    options:
      - "Yours: your network's public IP"
      - "The internet gateway's"
      - "The server's public IP"
      - "AWS's DNS server"
    correct: 0
    hint: "The app logs the address each request came from."
    explain: "The internet gateway swaps the destination address, not the source. So the server sees your real public IP as the source of the request, and the app logs it."
---

**What you'll do:** Log in and look around your server: its processes, ports, logs, hardware and network. Then find out why it doesn't know its own public IP.

---

## A server is still just a computer

In Lab 0.1, a server was a computer with a CPU, memory, a disk and a network connection. Your EC2 instance is exactly that. You've only seen it from the outside, as an icon in the console. Now look inside.

<div class="diagram">
  <img
    src="/images/labs/03-06/inside-the-server.svg"
    alt="Inside the EC2 instance runs Amazon Linux. It has a network card with the address 10.0.1.23, an 8 GiB EBS disk, and processes started by systemd: sshd on port 22 and the hello server on port 80. Requests from you arrive at the network card and go to port 80."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">from your request to the process that answers it</div>
</div>

SSH in to your server to follow along:

```bash
ssh -i ~/Downloads/{{ns}}-key.pem ec2-user@PUBLIC_IP
```

## Step 1: Find the app's process

Every running program is a **process**. List the Python ones:

```bash
pgrep -a python3
```

You'll see your app, with a number in front: its **process ID**. Now ask systemd about it:

```bash
systemctl status hello
```

It shows the same process ID, how long it's been running and how much memory it's using. Press `q` to get back to the prompt.

For a live view of everything running, use `top`. Press `q` to quit.

## Step 2: Find the ports

```bash
sudo ss -tlnp
```

This lists every program waiting for connections. Two lines matter:

```text
LISTEN  0  5    0.0.0.0:80   0.0.0.0:*  users:(("python3",pid=2034,fd=3))
LISTEN  0  128  0.0.0.0:22   0.0.0.0:*  users:(("sshd",pid=1688,fd=3))
```

That's Lab 0.2, for real: port 80 belongs to your app, and port 22 belongs to `sshd`, the SSH service you log in through. `0.0.0.0` means it's listening on every network address the server has.

## Step 3: Read the app's log

```bash
journalctl -u hello -n 10
```

This shows the last 10 lines the app wrote. Reload your website in the browser, then run the command again. A new line appears, starting with your public IP.

You'll use logs a lot more in Phase 9.

## Step 4: Check the hardware you rented

```bash
nproc
```

```bash
free -h
```

```bash
df -h /
```

`nproc` shows 2 CPUs and `free -h` shows about 1 GiB of memory. That's the `t3.micro` instance type you chose. `df -h /` shows the 8 GiB disk.

That disk isn't inside the physical machine your instance runs on. It's an **EBS volume**, a disk that AWS connects over its network. That matters in the next lab.

## Step 5: Look at the network

```bash
ip addr
```

Find the network card called `ens5`. It has one IPv4 address, from your subnet:

```text
inet 10.0.1.23/24 ...
```

There's no public IP anywhere on this server. Now ask AWS what the public IP is:

```bash
ec2-metadata --public-ipv4
```

AWS knows it. Your server doesn't have it.

## Where the public IP actually lives

Your server's public IP only exists at the internet gateway. When a request arrives for the public IP, the gateway swaps it for your server's private IP and passes it on. On the way back, it swaps them again.

<div class="diagram">
  <img
    src="/images/labs/03-06/public-ip-translation.svg"
    alt="Your browser sends a request to 54.170.12.9. The internet gateway swaps the address for 10.0.1.23 before passing it to the server. On the server, ip addr only shows 10.0.1.23."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the public IP only exists at the gateway, never on the server</div>
</div>

That's why your prompt and the website both show `ip-10-0-1-23`. As far as the server knows, that's its only address.

<div class="callout why"><b>Your home router does something similar.</b> In Lab 0.2, devices at home had private addresses and shared the router's public one. Phase 5 builds on this exact idea.</div>

## The metadata service

`ec2-metadata` asked the **instance metadata service**, a special address, `169.254.169.254`, that every EC2 instance can reach. It answers questions about the instance itself: its ID, Availability Zone, IPs and more.

Your test app uses it to find the name and Availability Zone it shows on the page. You'll use it again in Lab 3.9.

## Summary

- Your app is a process, started by systemd, listening on port 80.
- `ss`, `journalctl`, `nproc`, `free` and `df` show you what the server is doing and what it has.
- The disk is an EBS volume, connected over AWS's network.
- The server only has its private IP. The internet gateway swaps the public one for it.

Log out with `exit`. Keep the server for the next lab.
