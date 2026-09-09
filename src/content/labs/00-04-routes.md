---
phase: 0
order: 4
title: Routes
type: concept
time: ~15 min
cost: Free
summary: Learn how a computer decides where to send traffic when the destination is somewhere else.
draft: false
questions:
  - kind: recall
    q: "What does a <b>route</b> tell a device?"
    options:
      - "Which application should open the traffic"
      - "Where traffic for a destination should be sent next"
      - "Which password should be used"
      - "How large a subnet is"
    correct: 1
    hint: "A route is about the next step in a packet's journey."
    explain: "A route matches a destination network and tells the device where traffic for that destination should go next."

  - kind: cause
    q: "Your laptop wants to reach a device on its own local subnet. Why does it not need to send that traffic to the default gateway first?"
    options:
      - "Local traffic does not use IP addresses"
      - "The destination is directly reachable on the same network"
      - "Routers cannot handle private IP addresses"
      - "The firewall automatically redirects it"
    correct: 1
    hint: "Think about whether another network has to be crossed."
    explain: "Devices on the same subnet can communicate directly at the local network layer. A router is needed when traffic must leave that network for another one."

  - kind: predict
    q: "A routing table has a route for <code>10.0.0.0/8</code> and a default route for <code>0.0.0.0/0</code>. Traffic is going to <code>10.20.30.40</code>. Which route wins?"
    options:
      - "The default route"
      - "The 10.0.0.0/8 route"
      - "Both routes at the same time"
      - "Neither route"
    correct: 1
    hint: "Routers prefer the most specific matching destination."
    explain: "10.20.30.40 matches both routes, but 10.0.0.0/8 is more specific than 0.0.0.0/0, so that route is chosen."
---

**What you'll learn:** How devices decide whether a destination is local, when traffic needs a router, and how a routing table chooses the next step.

---

## You know the destination. Now what?

Suppose your laptop wants to send data to:

`192.168.1.20`

It already has the destination IP.

But knowing **where** you want to go is not the same as knowing **how to get there**.

The computer has to decide:

> Is that destination on my own network, or do I need to send this somewhere else first?

That decision is routing.

<!--
VISUAL: local-vs-remote.svg

Purpose:
Show the first routing decision visually.

Must show:
- Laptop: 192.168.1.10
- Local printer: 192.168.1.20
- Router/default gateway: 192.168.1.1
- A remote server somewhere beyond the router
- Local traffic going directly to the printer
- Remote traffic going to the router first

Key idea:
Same subnet = directly reachable.
Different network = send to a router.

Keep the routes visually distinct and minimal.
-->

## Same network? Send it directly

Imagine your laptop is:

`192.168.1.10/24`

and your printer is:

`192.168.1.20/24`

A `/24` tells us both devices are inside:

`192.168.1.0/24`

They are on the same subnet.

The laptop does not need another network to reach the printer. It can deliver the traffic locally.

That is the first routing idea:

> **If the destination is on your local network, send it there directly.**

## Different network? You need a router

Now suppose the destination is:

`8.8.8.8`

That address is not inside:

`192.168.1.0/24`

Your laptop cannot reach it directly on the local network.

So it sends the packet to a device that knows how to reach other networks:

a **router**.

At home, that is normally your home router.

Its local address might be:

`192.168.1.1`

That router becomes your **default gateway**: the place your device sends traffic when the destination is somewhere outside the local network.

<div class="callout why"><b>The router is not the final destination.</b> It is the next stop. The packet still contains the IP address of the destination it is ultimately trying to reach.</div>

## A route is a rule

A route is essentially:

> **For this destination, send traffic this way.**

A device keeps those rules in a **routing table**.

A simplified routing table might look like this:

| Destination | Send traffic to |
|---|---|
| `192.168.1.0/24` | local network |
| `0.0.0.0/0` | `192.168.1.1` |

The first route says:

> Anything for my own subnet is local.

The second says:

> Anything else goes to my router.

<!--
VISUAL: routing-table.svg

Purpose:
Turn the routing table into a visual decision rather than just another table.

Must show:
- Destination 192.168.1.20 matching 192.168.1.0/24 → LOCAL
- Destination 8.8.8.8 not matching local route → 0.0.0.0/0 → ROUTER 192.168.1.1

Key idea:
Routes are destination-based decisions.

Could be shown as two clean packet journeys beside a compact route table.
-->

## The default route

This route looks strange the first time you see it:

`0.0.0.0/0`

A `/0` uses zero bits to describe a specific network.

That means it matches **every IPv4 address**.

It is called the **default route**.

You can think of it as:

> **If no more specific route tells you what to do, use this one.**

On your laptop, the default route normally points to your home router.

Later in AWS, you will see the exact same idea.

## More specific routes win

A destination can sometimes match more than one route.

Imagine this table:

| Destination | Target |
|---|---|
| `10.0.0.0/8` | Router A |
| `10.20.0.0/16` | Router B |
| `0.0.0.0/0` | Router C |

Now traffic is going to:

`10.20.30.40`

Technically, that destination matches all three routes.

But the `/16` is the most specific match.

So the traffic goes to:

`Router B`

This is called **longest prefix match**.

You do not need to memorise the name yet. Remember the behaviour:

> **When several routes match, the most specific one wins.**

<!--
VISUAL: longest-prefix-match.svg

Purpose:
Make "most specific route wins" immediately understandable.

Must show:
Destination: 10.20.30.40

Candidate routes:
- 0.0.0.0/0
- 10.0.0.0/8
- 10.20.0.0/16

Highlight /16 as the selected route.

Key idea:
All three match, but /16 describes the destination most precisely.

Avoid binary unless it can be shown extremely lightly.
-->

## Routers do this again and again

The internet is not one giant router with a map of every individual computer.

Traffic moves through networks one step at a time.

A router receives a packet, looks at its destination IP, checks its routes, and chooses where to send it next.

Then another router may do the same thing.

And another.

<!--
VISUAL: hop-by-hop.svg

Optional visual.

Purpose:
Show routing as a sequence of next-hop decisions.

Could show:
Laptop → home router → ISP router → another router → destination server

Do not imply that every internet request always follows this exact number of hops.

Key idea:
Each router only needs to decide the next useful step.
-->

<div class="callout why"><b>Routing is about reachability.</b> A route can tell traffic where to go, but that does not mean the destination will accept it. Reaching a machine and being allowed to communicate with it are separate problems.</div>

## The mental model to keep

When a device wants to send a packet:

1. It knows the **destination IP**.
2. It checks whether that destination is on a network it can reach directly.
3. If not, it looks for a matching **route**.
4. The route tells it the **next hop**.
5. If several routes match, the **most specific** one wins.

So far, we have answered:

- **IP address** — where is the destination?
- **CIDR/subnet** — which network does it belong to?
- **route** — where should the packet go next?

But there is still another question.

Even if traffic can reach the destination:

> **Should it be allowed in?**

That is what **firewalls** solve.
