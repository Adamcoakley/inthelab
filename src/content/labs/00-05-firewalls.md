---
phase: 0
order: 5
title: Firewalls
type: concept
time: ~15 min
cost: Free
summary: How firewalls decide which traffic gets through and which gets blocked.
draft: false
questions:
  - kind: recall
    q: "What is the main job of a <b>firewall</b>?"
    options:
      - "Give devices IP addresses"
      - "Choose the shortest route across the internet"
      - "Allow or block traffic based on rules"
      - "Turn domain names into IP addresses"
    correct: 2
    hint: "A firewall is a gatekeeper."
    explain: "A firewall checks each piece of traffic against its rules and decides whether to let it through or block it."

  - kind: cause
    q: "A web server is running fine on port 443, but the firewall blocks inbound TCP 443. What does a visitor see?"
    options:
      - "The website works, because the server is running"
      - "The connection fails, because the traffic never reaches the service"
      - "DNS switches to another port"
      - "The server receives the request over UDP instead"
    correct: 1
    hint: "A working service is no use if traffic can't reach it."
    explain: "The server may be healthy, but if the firewall blocks port 443 the request never gets to it. To the visitor, the site just looks broken."

  - kind: predict
    q: "You want a public web server to accept HTTPS from everyone, but not allow SSH from the whole internet. Which rules make sense?"
    options:
      - "Allow TCP 443 from anywhere, allow TCP 22 only from a trusted IP"
      - "Allow every port from anywhere"
      - "Block TCP 443 and allow TCP 22 from anywhere"
      - "Allow UDP 443 only and remove all other rules"
    correct: 0
    hint: "Only open what actually needs to be public."
    explain: "Visitors need HTTPS, so 443 is open to everyone. SSH is only for you, so 22 is limited to your own IP. Everything else stays blocked."
---

**What you'll learn:** What a firewall checks, how its rules are built from things you already know, and why a blocked connection can look exactly like a broken server.

---

## Reaching a server isn't the same as getting in

In the last lab, routes got traffic all the way to a server. However, arriving doesn't mean the server should accept it.

A public web server wants visitors to load its website. It does **not** want strangers trying to log in to it, or poking at its database.

Something has to sort the wanted traffic from the unwanted. That something is a **firewall**.

<div class="diagram">
  <img
    src="/images/labs/00-05/firewall-gate.svg"
    alt="A visitor's HTTPS traffic on port 443 passes through the firewall to the web server. A stranger's SSH traffic on port 22 is blocked at the firewall."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">both can reach the server, only one is let in</div>
</div>

## A firewall follows rules

A firewall doesn't guess. It follows a list of **rules** that you write.

Each rule is built from things you already learned in this phase:

- **protocol**: how the traffic is carried, like TCP
- **port**: which service it's for, like `443` for HTTPS
- **source**: which IP address it's coming from
- **action**: allow it, or block it

So a rule reads like a sentence: "Allow TCP traffic to port `443` from anywhere."

<div class="diagram">
  <img
    src="/images/labs/00-05/firewall-rule-anatomy.svg"
    alt="A firewall rule split into four parts: protocol TCP, port 443, source anywhere, action allow. Below, a small rule list ending with a rule that blocks everything else."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">four questions, one decision</div>
</div>

Notice the last rule. Many firewalls, including the ones you'll use in AWS, block anything that doesn't match an allow rule. You only list what's allowed in.

## Inbound and outbound

Traffic has a direction.

**Inbound** is traffic arriving at a machine. **Outbound** is traffic leaving it.

When a browser loads your website, that's inbound to your server. When your server downloads updates, that's outbound from it.

<div class="diagram">
  <img
    src="/images/labs/00-05/inbound-outbound.svg"
    alt="A browser sending traffic into a server, labelled inbound, and the server sending traffic out to another service, labelled outbound."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">in or out, from the server's point of view</div>
</div>

Firewalls often have separate rules for both inbound and outbound traffic.

## Only open what you need

The safe way to set up a firewall is to start with everything closed, then open only what the server actually needs.

This is called **least privilege**: give access to exactly what's needed, and nothing more.

Take a web server running three services:

- **HTTPS on port 443**: visitors need this, so open it to everyone.
- **SSH on port 22**: only you need to log in, so allow it from your IP only.
- **MySQL on port 3306**: nobody outside should touch the database, so leave it closed.

<div class="diagram">
  <img
    src="/images/labs/00-05/least-privilege.svg"
    alt="The internet can reach port 443 but is blocked from port 22. Your laptop can reach port 22. Port 3306 is closed to everyone outside."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">one server, three services, three different levels of access</div>
</div>

A server can run lots of services without showing all of them to the world.

## A blocked connection looks like a broken server

This is one of the most useful things to know when something stops working.

Imagine the server is on, the website is running, the IP is right and the route is right. But the firewall doesn't allow port `443`.

To the visitor, **the website just doesn't load**. Usually the browser spins for a while and then gives up. Nothing tells them a firewall was the reason.

<div class="callout break"><b>Don't blame the app first.</b> A failed connection could be DNS, the IP address, a route, a firewall rule, the port, or the app itself. Check each step in order.</div>

## Putting Phase 0 together

You now know every stop a request makes. Here's what happens when someone types `inthelab.ie` into a browser:

<div class="diagram">
  <img
    src="/images/labs/00-05/phase-0-mental-model.svg"
    alt="Six steps of a request: type a name, DNS finds the IP address, CIDR identifies the network, routes choose the next hop, the firewall allows or blocks, and the port picks the service."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">every Phase 0 idea, in the order a request meets them</div>
</div>

1. **DNS** turns the name into an IP address.
2. **CIDR** tells you which network that address belongs to.
3. **Routes** pass the traffic along, one hop at a time.
4. The **firewall** decides whether it's allowed in.
5. The **port** picks the right service on the server.
6. **Protocols** like TCP and HTTPS carry the conversation the whole way.

If any one of these fails, the page doesn't load. That's why you'll always check them in order.

## You’re ready for AWS

Networks, IP addresses, routes and firewalls were around long before the cloud. AWS uses those same networking ideas, just with its own tools and services.

Next, you’ll start seeing how they are set up in AWS.