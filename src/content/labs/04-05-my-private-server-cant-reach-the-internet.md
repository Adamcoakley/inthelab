---
phase: 4
order: 5
title: My private server can't reach the internet
type: lab
time: ~20 min
cost: ~$0.03 an hour while running
buildsOn: Lab 4.4
summary: Try to install updates on your private server, watch it fail, and work out why.
draft: false
questions:
  - kind: recall
    q: "In the <code>curl -v</code> output, which line shows that DNS worked?"
    options:
      - "Trying 18.239.83.48:443..."
      - "Connection timed out"
      - "curl: (28)"
      - "None, DNS failed"
    correct: 0
    hint: "To try an address, curl must already know it."
    explain: "curl only tries an IP address once DNS has turned the name into one. So DNS worked, and the connection failed after that."

  - kind: cause
    q: "<code>app-sg</code> allows all outbound traffic. Why can't <code>dnf</code> reach the internet?"
    options:
      - "dnf is blocked on Amazon Linux"
      - "The security group's outbound rules are ignored"
      - "DNS is broken"
      - "private-rt has no route out of the VPC, so the traffic has nowhere to go"
    correct: 3
    hint: "The firewall allowed it. Which stop comes after the firewall on the way out?"
    explain: "The security group let the traffic leave the server, but the subnet's route table only has the local route. Nothing tells the traffic how to get beyond the VPC, so it goes nowhere."

  - kind: predict
    q: "You add <code>0.0.0.0/0 → igw</code> to <code>private-rt</code>. Can <code>app-1</code> download updates now?"
    options:
      - "Yes, it now has a route out"
      - "Yes, but only from the bastion"
      - "No, it has no public IP, and the internet gateway only passes traffic for servers that have one"
      - "No, because of DNS"
    correct: 2
    hint: "What does the internet gateway swap for the private IP on the way out?"
    explain: "The internet gateway swaps a server's private IP for its public IP. app-1 has no public IP, so the gateway can't do that and its traffic still doesn't get out. And giving it a public IP would make it public, the thing you're trying to avoid."
---

**What you'll do:** Try to install updates on your private server, see it fail, and find out exactly which stop is broken.

---

## Servers need things from the internet

A private server still needs the internet, in one direction. It downloads software updates. It calls AWS services. It sends its logs and metrics out to be stored.

All of those are connections the server starts itself, going out.

## Step 1: Connect to your app server

```bash
ssh 10.0.2.37
```

Replace `10.0.2.37` with your app server's private IP.

## Step 2: Try to check for updates

```bash
sudo dnf check-update --refresh
```

`--refresh` makes it ask the update servers for the latest list, instead of using a saved one.

It shows `Amazon Linux 2023 repository` and then sits there. Give it 30 seconds, then press `Ctrl+C`.

## Step 3: Try a simpler request

Ask for a web page, and show what happens along the way:

```bash
curl -m 10 -v -o /dev/null https://aws.amazon.com
```

- `-m 10` gives up after 10 seconds.
- `-v` shows each step curl takes.
- `-o /dev/null` throws the page away, since you only care whether it arrives.

You'll see something like:

```text
*   Trying 18.239.83.48:443...
* Connection timed out after 10002 milliseconds
curl: (28) Connection timed out after 10002 milliseconds
```

Your address will be different.

<div class="callout shot">screenshot: the terminal showing curl trying an address and timing out<br>save as <code>/images/labs/04-05/curl-timeout.png</code></div>
<!--
<figure class="screenshot">
  <img
    src="/images/labs/04-05/curl-timeout.png"
    alt="The terminal showing curl trying an address and timing out."
  />
</figure>
-->

## Step 4: Check the stops in order

Work through it the same way as any connection that fails: one stop at a time.

1. **DNS:** curl was **Trying** an address, so it already had one. DNS worked. That's because AWS runs a DNS server inside every VPC, so name lookups never need the internet.
2. **Firewall:** in the EC2 console, select `{{ns}}-app-sg` and open the **Outbound rules** tab. One rule allows **All traffic** to `0.0.0.0/0`. The firewall let it out.
3. **Route:** in the VPC console, open `{{ns}}-private-rt` and the **Routes** tab. There's only `10.0.0.0/16` → `local`.

The traffic left the server, but the route table has nowhere to send anything outside your VPC.

<div class="callout shot">screenshot: the outbound rules of app-sg allowing all traffic<br>save as <code>/images/labs/04-05/app-sg-outbound.png</code></div>
<!--
<figure class="screenshot">
  <img
    src="/images/labs/04-05/app-sg-outbound.png"
    alt="The outbound rules of app-sg allowing all traffic."
  />
</figure>
-->

## Private works both ways

Making the subnet private did two things:

<div class="diagram">
  <img
    src="/images/labs/04-05/no-way-out.svg"
    alt="Getting in: the internet is blocked from reaching private-a, as intended. Getting out: a server in private-a is blocked from reaching the internet, which stops software updates, downloads and AWS APIs."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the same missing route blocks both directions</div>
</div>

- **Nobody can get in.** That's what you wanted.
- **Nothing can get out.** That's a problem: your server can't install security updates, and keeping it patched is your job.

This is also why it mattered that the app was already on your AMI. If it had needed downloading on boot, this server could never have started it.

<div class="callout break"><b>Why not just add a route to the internet gateway?</b> Two reasons. The internet gateway works by swapping a server's private IP for its public IP, and this server doesn't have one, so its traffic still couldn't get out. And if you gave it a public IP, it would be public again, which is exactly what you set out to avoid.</div>

What you need is a way out that isn't a way in: something that lets your server start connections to the internet, without letting the internet start connections to it.

Your home router already does this for your laptop. In the next phase, you'll build the AWS version.

## Before you take a break

Keep both servers for the next phase. To save money in the meantime, stop them: select both, then choose **Instance state**, **Stop instance**.

When you start the bastion again, it gets a new public IP, and your SSH config still points at the old one. To fix it, open the config file and change the `HostName` line under `Host bastion`:

<div class="os-switch">
<div class="os-tabs"><button type="button" data-os-pick="mac">macOS / Linux</button><button type="button" data-os-pick="windows">Windows</button></div>
<div class="os-panel" data-os="mac">

```bash
nano ~/.ssh/config
```

</div>
<div class="os-panel" data-os="windows">

```powershell
notepad $HOME\.ssh\config
```

</div>
</div>

## Summary

- DNS works in a private subnet, because AWS runs DNS inside your VPC.
- Your security group lets traffic out, but `private-rt` has no route to anywhere outside the VPC.
- A private subnet blocks connections in both directions.
- You need a way out that isn't a way in.
