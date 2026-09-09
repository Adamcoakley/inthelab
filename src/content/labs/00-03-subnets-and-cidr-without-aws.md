---
phase: 0
order: 3
title: Subnets and CIDR without AWS
type: concept
time: ~20 min
cost: Free
summary: Learn how IP addresses are divided into networks, and how CIDR controls the size of those networks.
draft: false
questions:
  - kind: recall
    q: "What does the <code>/24</code> in <code>192.168.1.0/24</code> tell you?"
    options:
      - "The network contains exactly 24 devices"
      - "The first 24 bits identify the network"
      - "Port 24 is open"
      - "The address is public"
    correct: 1
    hint: "The number after the slash describes where the network part ends."
    explain: "CIDR tells you how many bits belong to the network portion of an IP address. In a /24, the first 24 bits identify the network and the remaining 8 bits are available for addresses inside it."

  - kind: cause
    q: "Why does a <code>/26</code> contain fewer addresses than a <code>/24</code>?"
    options:
      - "Because /26 is an older IP format"
      - "Because more bits are used to identify the network, leaving fewer bits for addresses inside it"
      - "Because /26 blocks public internet access"
      - "Because /26 only works with private IP addresses"
    correct: 1
    hint: "There are only 32 bits in an IPv4 address."
    explain: "IPv4 addresses have 32 bits. A larger CIDR prefix uses more of those bits for the network itself, leaving fewer combinations for addresses inside that network."

  - kind: predict
    q: "You split <code>10.0.0.0/24</code> into two equal-sized subnets. What size would each subnet be?"
    options:
      - "/23"
      - "/24"
      - "/25"
      - "/26"
    correct: 2
    hint: "Splitting one network in half uses one more bit for the network portion."
    explain: "Adding one bit to the prefix halves the number of addresses. A /24 split into two equal networks becomes two /25 networks."
---

**What you'll learn:** What a subnet actually is, what the number after the slash means, and why `/24`, `/25` and `/26` describe different-sized networks.

---

## An IP address is only part of the story

You already know an IP address identifies a destination on a network.

For example:

`192.168.1.10`

But there is a missing piece.

Which part means **the network**, and which part identifies an address **inside that network**?

The IP address alone does not tell you.

That is what **CIDR** does.

<!--
VISUAL: cidr-boundary.svg

Purpose:
Show that an IP address needs a boundary between the network part and the address/host part.

Must show:
- 192.168.1.10
- A clear visual split for a /24:
  192.168.1 | 10
- Left side labelled "network"
- Right side labelled "address inside the network"
- /24 shown as the thing defining that boundary

Style notes:
- Same clean technical art direction as the rest of inthelab
- Minimal text
- This should make the idea understandable before reading the paragraph below
-->

## CIDR tells us where the boundary is

You will often see an IP range written like this:

`192.168.1.0/24`

The `/24` is called the **CIDR prefix**.

IPv4 addresses contain **32 bits** in total.

A `/24` means:

- the first **24 bits** describe the network
- the remaining **8 bits** are left for addresses inside it

You do not need to become comfortable reading binary yet.

For now, think of the slash number as:

> **How much of this address belongs to the network?**

The bigger the number after the slash, the more specific — and therefore smaller — the network becomes.

<div class="callout why"><b>One useful rule.</b> A larger CIDR number means a smaller network. <code>/26</code> is smaller than <code>/24</code>.</div>

## What is a subnet?

A **subnet** is simply a network that forms part of a larger network.

Imagine you have one large office.

You could keep everybody in one huge room.

Or you could divide the space into smaller rooms:

- engineering
- finance
- support
- visitors

It is still one building, but each room is its own section.

Subnetting does the same thing with an IP address range.

<!--
VISUAL: subnet-splitting.svg

Purpose:
Make "subnet" feel obvious rather than mathematical.

Must show:
- One larger network: 10.0.0.0/24
- It being divided into two smaller equal networks
- 10.0.0.0/25
- 10.0.0.128/25
- Visually make it clear these two smaller networks together fill the original /24

Preferred concept:
One large horizontal address space splitting cleanly into two halves.

Avoid:
- Dense binary
- Lots of calculations
- Decorative boxes with paragraphs inside them
-->

For example, this network:

`10.0.0.0/24`

can be divided into two equal subnets:

`10.0.0.0/25`

and:

`10.0.0.128/25`

Together, those two `/25` networks cover the same address space as the original `/24`.

## Why does changing the slash change the size?

There are always **32 bits** in an IPv4 address.

If 24 bits describe the network:

`/24`

then 8 bits remain for addresses inside it.

Eight bits can form:

`2^8 = 256`

different combinations.

So a `/24` contains **256 total IPv4 addresses**.

If you move to `/25`, one more bit is used for the network:

`32 - 25 = 7`

Seven remaining bits gives:

`2^7 = 128`

addresses.

And `/26` leaves six bits:

`2^6 = 64`

addresses.

You do not need to memorise the maths. The pattern matters more.

<!--
VISUAL: cidr-size-comparison.svg

Purpose:
Show the relationship between prefix size and address count at a glance.

Must show three equal-style rows or bars:
- /24 → 256 addresses
- /25 → 128 addresses
- /26 → 64 addresses

Key visual idea:
As the slash number goes UP, the available address space goes DOWN.

Nice-to-have:
Show /24 as one full bar, /25 as half, /26 as quarter.

Keep it clean enough that the learner understands the pattern instantly.
-->

| CIDR | Total addresses |
|---|---:|
| `/24` | 256 |
| `/25` | 128 |
| `/26` | 64 |
| `/27` | 32 |
| `/28` | 16 |

<div class="callout why"><b>You do not need to memorise this table.</b> You need to understand the pattern: every time the prefix increases by one, the address space halves.</div>

## The first and last addresses are special

Take this network:

`192.168.1.0/24`

Its full range runs from:

`192.168.1.0`

to:

`192.168.1.255`

In traditional IPv4 subnetting, the first address identifies the **network itself**:

`192.168.1.0`

and the last address is the **broadcast address**:

`192.168.1.255`

That leaves the addresses between them available for devices.

So although a `/24` contains **256 total addresses**, a traditional subnet has **254 usable host addresses**.

<div class="callout why"><b>AWS will be slightly different.</b> AWS reserves additional addresses inside each subnet. Do not learn those rules yet — when we build an AWS subnet, we will look at exactly what AWS keeps and why.</div>

## Subnets must not overlap

Two separate subnets cannot claim the same address space.

For example, these are cleanly separated:

`10.0.0.0/24`

`10.0.1.0/24`

But if two subnet ranges overlap, the network can no longer make a clear decision about where an address belongs.

That idea matters a lot later when you design VPCs.

<!--
VISUAL: overlap.svg

Optional visual — only use if it genuinely improves the section.

Purpose:
Show valid non-overlapping ranges versus two ranges that overlap.

Could show:
GOOD:
10.0.0.0/24 | 10.0.1.0/24

BAD:
Two translucent address-range bars overlapping each other.

Key idea:
Each subnet needs its own distinct slice of the address space.

If Claude thinks the text already carries this clearly, this visual can be skipped.
-->

## Why make smaller networks at all?

Why not put everything into one enormous network?

Because separating a network gives you control.

Later, you might want:

- internet-facing servers in one subnet
- private application servers in another
- databases somewhere even more restricted

Those groups can then have different routes and different security rules.

For now, the important idea is simply:

> **Subnetting lets you divide one address range into smaller networks.**

## The mental model to keep

If you see:

`10.0.1.0/24`

read it as:

> **A network beginning at `10.0.1.0`, with a `/24` defining its size.**

And remember:

- an **IP address** identifies a destination
- **CIDR** tells you the network boundary and size
- a **subnet** is a smaller network carved from a larger address space
- increasing the CIDR prefix makes the network smaller

You now have enough networking knowledge to understand the next question:

If your destination is **not inside your own subnet**, where does the traffic go next?

That is what **routes** solve.
