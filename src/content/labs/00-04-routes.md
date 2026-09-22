---
phase: 0
order: 4
title: Routes
type: concept
time: ~15 min
cost: Free
summary: How a computer decides where to send traffic, and what happens when the destination is on another network.
draft: false
questions:
  - kind: recall
    q: "What does a <b>route</b> tell a device?"
    options:
      - "Which application should open the traffic"
      - "Where to send traffic for a destination next"
      - "Which password to use"
      - "How large a subnet is"
    correct: 1
    hint: "A route is about the next step in the journey."
    explain: "A route is a rule: for addresses in this range, send the traffic here next."

  - kind: cause
    q: "Your laptop sends something to a printer on the same subnet. Why doesn't it go through the router?"
    options:
      - "Local traffic doesn't use IP addresses"
      - "The printer is on the same network, so the laptop can reach it directly"
      - "Routers can't handle private IP addresses"
      - "The firewall redirects it"
    correct: 1
    hint: "Does the traffic need to leave your network?"
    explain: "Devices on the same subnet can talk to each other directly. The router is only needed when traffic has to leave for a different network."

  - kind: predict
    q: "A routing table has a route for <code>10.0.0.0/8</code> and a default route <code>0.0.0.0/0</code>. Traffic is going to <code>10.20.30.40</code>. Which route is used?"
    options:
      - "The default route"
      - "The 10.0.0.0/8 route"
      - "Both at the same time"
      - "Neither"
    correct: 1
    hint: "Both match. Which one is more specific?"
    explain: "10.20.30.40 fits inside both, but 10.0.0.0/8 is a smaller, more specific range than 0.0.0.0/0, so it wins."
---

**What you'll learn:** How a device decides whether to send traffic directly to another device or through a router.

---

## What is routing?

Let's say your laptop wants to send a document to a printer on the network. It already knows the destination IP address, now it just needs to figure out how to reach it.

So before sending anything, your laptop asks one question: is this destination IP on my own network, or somewhere else?

That decision is called **routing**.

<div class="diagram">
  <img
    src="/images/labs/00-04/local-vs-remote.svg"
    alt="A laptop sending directly to a printer on the same network, and sending to a router to reach a server on another network."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">same network goes direct, anything else goes to the router</div>
</div>

## Same network? Send it directly

Your laptop is `192.168.1.10/24` and your printer is `192.168.1.20/24`.

In the last lab, you saw that a `/24` means the first three numbers of the IP address identify the network.

Both addresses start with `192.168.1`, so they are both on the same network: `192.168.1.0/24`.

This means the laptop can send the document straight to the printer. No router needed.

## Different network? Hand it to the router

Let's say your laptop wants to reach a server at `8.8.8.8`.

That IP address doesn't start with `192.168.1`, so it isn't on your network. This means your laptop has no way to reach it on its own.

Instead, it hands the traffic to your home router at `192.168.1.1`. The router is connected to both your home network and the internet, so it can pass traffic between them.

The router is where traffic goes by default whenever it's leaving your network, the router is called your **default gateway**. It's the exit door out of your network.

## A route is a rule

Your laptop doesn’t work out where to send traffic from scratch every time. It keeps a short list of rules called a **routing table**.

Each rule is called a **route**. 

Your laptop might have just two routes:

- `192.168.1.0/24` → send it directly, because it is on the local network
- `0.0.0.0/0` → send it to the router at `192.168.1.1`

<div class="diagram">
  <img
    src="/images/labs/00-04/routing-table.svg"
    alt="Traffic to 192.168.1.20 matches the local route and goes straight to the printer. Traffic to 8.8.8.8 matches the catch-all route and goes to the router."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">look at the destination, find the matching rule, follow it</div>
</div>

## The default route means “everything else”

`0.0.0.0/0` looks strange the first time you see it. It means any IPv4 address.

So if traffic does not match a more specific route, the default route is used.

On your laptop, that usually means: anything outside your local network → send it to the router.

That is why it is called the **default route**.

## The most specific route wins

Sometimes an address matches more than one route. Say a router has these three routes:

- `0.0.0.0/0` → Router A
- `10.0.0.0/8` → Router B
- `10.20.0.0/16` → Router C

If traffic is going to `10.20.30.40`, that address fits inside all three ranges. So which one is used?

The router picks the **most specific** one, meaning the smallest range that still contains the address. Here that's `10.20.0.0/16`, so the traffic goes to Router C.

<div class="diagram">
  <img
    src="/images/labs/00-04/longest-prefix-match.svg"
    alt="Three nested ranges, 0.0.0.0/0, 10.0.0.0/8 and 10.20.0.0/16, with 10.20.30.40 inside all of them. The smallest range, /16, is chosen."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">all three match, the smallest range wins</div>
</div>

Several routes can match the same destination. The router chooses the most specific match - the smallest network that still contains the destination IP.

Remember from the last lab: a bigger number after the slash means a smaller, more specific range. You may hear this called **longest prefix match**. You don't need to remember the name, just the idea.

## Routers pass it along, one step at a time

No single router knows the whole internet. Each one only knows enough to pick the **next step**.

So your traffic gets passed from router to router. Each one asks the same question, "where next?", and hands it on. Each handover is called a **hop**.

<div class="diagram">
  <img
    src="/images/labs/00-04/hop-by-hop.svg"
    alt="Traffic to 8.8.8.8 passing from a laptop through a home router, an ISP router and Google's router before arriving at the server."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">each router only decides the next hop</div>
</div>

The number of hops changes from trip to trip. What stays the same is that every router makes the same small decision.

## Getting there isn't the same as getting in

Routing only gets traffic **to** a machine. It says nothing about whether that machine will **accept** it.

A route can deliver a request right to a server's door, and the server can still refuse to open it. That's a separate job, and it's what the next lab is about.

## What to remember

When a device sends something:

1. It looks at the destination IP.
2. If the destination is on its own network, it sends it directly.
3. If not, it checks its routing table for a matching route.
4. If several routes match, the most specific one wins.
5. If nothing else matches, the default route sends it to the router. 

So far you know three pieces:

- **IP address** tells you where the destination is.
- **CIDR** tells you which network it belongs to.
- **Route** tells traffic where to go next.

The last question is: once traffic arrives, is it allowed in? That's what **firewalls** decide.