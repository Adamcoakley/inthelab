---
phase: 0
order: 5
title: Firewalls
type: concept
time: ~15 min
cost: Free
summary: Learn how firewalls decide which network traffic is allowed through and which traffic is blocked.
draft: false
questions:
  - kind: recall
    q: "What is the main job of a <b>firewall</b>?"
    options:
      - "Give devices IP addresses"
      - "Choose the shortest route across the internet"
      - "Allow or block network traffic according to rules"
      - "Translate domain names into IP addresses"
    correct: 2
    hint: "A firewall is a gatekeeper, not an addressing or routing system."
    explain: "A firewall examines network traffic against a set of rules and decides whether that traffic should be allowed or blocked."

  - kind: cause
    q: "A web server is running correctly on port 443, but a firewall blocks inbound TCP port 443. What will a user experience?"
    options:
      - "The website will still work because the server is running"
      - "The connection will fail because the traffic cannot reach the service"
      - "DNS will automatically use another port"
      - "The server will receive the request over UDP instead"
    correct: 1
    hint: "A running service is not useful if traffic is prevented from reaching it."
    explain: "The server may be healthy and listening on port 443, but if the firewall blocks that traffic, the connection cannot reach the HTTPS service."

  - kind: predict
    q: "You want a public web server to accept HTTPS from users but not allow SSH from the whole internet. Which rule set makes the most sense?"
    options:
      - "Allow TCP 443 from anywhere; restrict TCP 22 to a trusted source"
      - "Allow every port from anywhere"
      - "Block TCP 443 and allow TCP 22 from anywhere"
      - "Allow UDP 443 only and remove all other rules"
    correct: 0
    hint: "Only expose the traffic that actually needs to be public."
    explain: "HTTPS normally needs to be reachable by users, while administrative access such as SSH should be much more restricted. This follows the principle of allowing only what is needed."
---

**What you'll learn:** What a firewall actually checks, how rules use IP addresses, ports and protocols, and why reachable does not mean allowed.

---

## Reachable does not mean allowed

In the last lab, you learned how routes move traffic toward a destination.

Suppose a packet has successfully travelled across the network and reached a server.

That does **not** automatically mean the server should accept it.

A public web server might need to accept:

- HTTPS from users

but reject:

- random SSH attempts
- database connections from the internet
- traffic to services that should stay private

That is where a **firewall** comes in.

> **A firewall is a gatekeeper for network traffic.**

<!--
VISUAL: firewall-gate.svg

Purpose:
Introduce the firewall as a gate between network traffic and a server.

Must show:
- Internet/users on one side
- Firewall boundary/gate in the middle
- Server on the other side
- HTTPS :443 allowed through
- SSH :22 blocked from an untrusted source

Key idea:
The network path can exist while the firewall still decides whether traffic may pass.

Avoid making the firewall look like a literal brick wall if that makes the visual childish.
Keep it technical and clean.
-->

## A firewall works with rules

A firewall needs instructions.

A rule might say:

> Allow TCP traffic to port 443 from anywhere.

Another might say:

> Allow TCP traffic to port 22 only from my office IP address.

Everything else can be blocked.

This should connect several ideas you already know:

- an **IP address** identifies a source or destination
- a **port** identifies a service
- a **protocol** describes how the traffic is being carried
- a **firewall rule** uses those details to decide whether traffic is allowed

A simplified rule might look like:

| Protocol | Port | Source | Action |
|---|---:|---|---|
| TCP | `443` | anywhere | allow |
| TCP | `22` | trusted IP only | allow |
| TCP | `3306` | internet | block |

<!--
VISUAL: firewall-rule-anatomy.svg

Purpose:
Show what information a firewall rule cares about.

Must show one clean example:
TCP | port 443 | source: anywhere | ALLOW

Then identify:
- protocol
- port
- source
- action

Could also show a second compact example:
TCP | port 22 | source: trusted IP | ALLOW

Key idea:
Firewall rules combine concepts the learner already knows.
-->

## Inbound and outbound

Traffic has a direction.

**Inbound** traffic is arriving at something.

**Outbound** traffic is leaving it.

For a web server:

- a browser connecting to HTTPS is inbound traffic to the server
- the server contacting another service is outbound traffic from the server

The same connection can therefore look different depending on which machine you are standing beside.

<div class="callout why"><b>Direction is about perspective.</b> "Inbound" does not mean bad and "outbound" does not mean safe. It simply describes which way traffic is moving relative to the thing whose firewall you are looking at.</div>

<!--
VISUAL: inbound-outbound.svg

Purpose:
Make direction relative to the server obvious.

Must show:
Browser → Server labelled INBOUND near the server.
Server → external service labelled OUTBOUND near the server.

Keep this very small/simple if used.
This visual is optional if the text is already clear enough.
-->

## Allow only what you need

The safest firewall is not:

> Allow everything and block the dangerous things later.

A better starting point is:

> Block what is not needed, then explicitly allow the traffic the system requires.

This is part of the **principle of least privilege**.

If a server only needs to receive HTTPS traffic from the internet, there is no reason to expose its database port publicly.

If SSH access is only for administrators, there is no reason to allow the whole internet to try it.

<!--
VISUAL: least-privilege.svg

Purpose:
Show a server exposing only the services that need to be reachable.

Must show:
Server services:
- 443 HTTPS → public / allowed
- 22 SSH → trusted admin only
- 3306 MySQL → not public / blocked

Key idea:
A machine can run several services without exposing every service to everyone.

This could deliberately echo the ports visual from Lab 0.2 so the learner sees the concepts connect.
-->

## A blocked connection can look like a broken server

This is one of the most useful troubleshooting ideas in networking.

Imagine:

- the server is running
- the application is running
- the IP address is correct
- the route is correct
- the service is listening on port 443

but the firewall does not allow port 443.

From the user's point of view:

**the website still does not work.**

That is why troubleshooting network problems means checking the journey layer by layer.

<div class="callout break"><b>Do not jump straight to the application.</b> A failed connection does not automatically mean the program is broken. The problem could be DNS, addressing, routing, a firewall rule, the port, or the service itself.</div>

## Firewalls can exist in different places

A firewall is a concept, not one particular product.

Rules can be enforced:

- on the machine itself
- on a network device
- by the cloud platform around a resource

Later in AWS you will meet **Security Groups** and **Network ACLs**.

They both control network traffic, but they behave differently.

You do not need those AWS rules yet.

First, keep the general idea clear:

> **Routing decides where traffic can go. A firewall decides whether that traffic is allowed through.**

## Put Phase 0 together

You now have the core pieces needed to reason about a network journey.

A user types a name such as:

`example.com`

**DNS** helps find an IP address.

The IP address identifies the destination.

**CIDR** tells us which network an address belongs to.

If the destination is elsewhere, a **route** tells the packet where to go next.

When the traffic reaches a protected boundary, a **firewall** decides whether it is allowed through.

A **port** identifies the service it is trying to reach.

And protocols such as **TCP** and **HTTPS** define how the communication happens.

<!--
VISUAL: phase-0-mental-model.svg

Purpose:
Final Phase 0 recap visual.

Must show one clean request journey:
example.com
→ DNS
→ destination IP
→ subnet/network boundary
→ route/router
→ firewall
→ server :443

Small labels can connect each stage to the concept:
DNS = find the address
CIDR = identify the network
Route = choose the next hop
Firewall = allow or block
Port = choose the service

This is the most important visual in the lab.
It should feel like the Phase 0 concepts clicking together, not a dense architecture diagram.
-->

## You are ready to touch AWS

None of the ideas in Phase 0 belong only to AWS.

That is the point.

AWS gives you tools for building networks, servers, routes and firewalls, but the underlying networking concepts already existed.

In the next phase, we can start using AWS without treating every field in the console as unexplained magic.

You know what the pieces are for.

Now we can build with them.
