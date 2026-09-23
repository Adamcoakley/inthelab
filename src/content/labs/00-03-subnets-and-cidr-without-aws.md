---
phase: 0
order: 3
title: Subnets and CIDR without AWS
type: concept
time: ~15 min
cost: Free
summary: How an IP address identifies a network and a device, what /24 means, and how one network becomes several smaller ones.
draft: false
questions:
  - kind: recall
    q: "What does the <code>/24</code> in <code>192.168.1.0/24</code> tell you?"
    options:
      - "The network contains 24 devices"
      - "The first 24 bits identify the network"
      - "Port 24 is open"
      - "The address is private"
    correct: 1
    hint: "An IPv4 address contains 32 bits in total."
    explain: "The /24 says that the first 24 of the address's 32 bits identify the network. That leaves 8 bits for addresses inside that network."

  - kind: cause
    q: "Why does a <code>/26</code> contain fewer addresses than a <code>/24</code>?"
    options:
      - "Because /26 is an older IP format"
      - "Because more bits identify the network, leaving fewer bits for addresses inside it"
      - "Because /26 blocks public internet access"
      - "Because /26 only works with private IP addresses"
    correct: 1
    hint: "There are always 32 bits. If the network uses more of them, what is left?"
    explain: "A /24 leaves 8 bits for addresses. A /26 leaves only 6. Fewer bits are left for addresses, so the network is smaller."

  - kind: predict
    q: "You need a network with room for about 60 addresses. Which is the best fit?"
    options:
      - "/24"
      - "/25"
      - "/26"
      - "/27"
    correct: 2
    hint: "A /24 has 256 addresses. Each step up halves the size."
    explain: "A /26 contains 64 addresses. A /27 contains only 32, while /24 and /25 are larger than needed."
---

**What you'll learn:** How an IP address identifies a network and a device, what `/24` actually means, and how one network is split into smaller subnets.

---

## Every IP address has two parts

Take this address: `192.168.1.10`

Part of it says **which network**. The rest says **which device on that network**.

On a home network, every device usually shares the same first three numbers and differs only in the last one:

- laptop: `192.168.1.10`
- phone: `192.168.1.11`
- printer: `192.168.1.12`

So `192.168.1` is the network they all share, and the last number identifies each device on that network. However, the split does not always fall between the third and fourth numbers.

## The IP address does not say where the split is

Here is the problem. Look at `192.168.1.10` on its own. Nothing in it tells you where the network part stops.

It could stop after `192.168.1`. It could stop after `192.168`. The IP address alone gives you no way to tell where that split is.

<div class="diagram">
  <img
    src="/images/labs/00-03/address-split.svg"
    alt="The address 192.168.1.10 shown twice, with the boundary between the network part and the device part falling in two different places."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
</div>

## CIDR marks the line

The IP address needs something extra to mark the line. That something is a slash and a number, called the **CIDR prefix**, added to the end of an IP address: `192.168.1.0/24`

It does one job: the `/24` says how much of the address belongs to the network.

## Why /24?

Each of the four numbers represents 8 bits. You never need to work with bits directly, just remember that each number is worth 8.

<div class="diagram">
  <img
    src="/images/labs/00-03/cidr-24.svg"
    alt="192.168.1.0/24 split into four 8-bit numbers, the first three forming the network and the last one left for devices."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the slash counts bits, not the numbers you can see</div>
</div>

So `/24` is not "three numbers", it is 24 bits, which happens to be three numbers worth. That is why it is `/24` and not `/3`.

## The part that catches most people

Imagine you need a network **smaller** than a `/24`. Do you use `/25` or `/23`?

Most people say `/23`, because 23 is the smaller number. It is the other way round. A `/25` is the smaller network.

Here is why. Like we explained above, an IP address always has **32 bits**.

The slash tells you how many of those bits belong to the **network**. Whatever is left can be used for addresses inside that network.

- `/24` → 24 bits for the network, **8 left** → 256 addresses
- `/25` → 25 bits for the network, **7 left** → 128 addresses
- `/26` → 26 bits for the network, **6 left** → 64 addresses

Each time the slash number goes up by one, the network takes one more bit. That leaves half as many possible addresses.

So the rule is simple: **bigger slash number, smaller network.**

<div class="diagram">
  <img
    src="/images/labs/00-03/cidr-size-comparison.svg"
    alt="Three bars showing /24, /25 and /26, each one half the length of the bar above it."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">every slot the network takes halves what is left</div>
</div>

## Splitting a network into smaller pieces

Imagine you start with this network: `10.0.0.0/24`

It contains 256 addresses.

You do not have to keep all 256 addresses in one network. You can divide that space into smaller networks.

If you split the `/24` exactly in half, you get two `/25` networks:

- `10.0.0.0/25` → first half
- `10.0.0.128/25` → second half

Each one contains 128 IP addresses.

Nothing has been added or removed. You have simply taken one large network and divided it into two smaller ones.

<div class="callout why"><b>Those smaller networks are called subnets.</b> A subnet is simply a smaller network created from a larger address range.</div>

## Why make subnets?

Different parts of your infrastructure often need different access. For example:

- a **web server** that users need to reach from the internet
- a **database** that should stay private

Put them in different subnets, and each subnet can have its own **routes and rules**.

## The mental model to keep

- an IP address has a **network part** and a **device part**
- **CIDR** marks where one ends and the other begins
- a **bigger** slash number means a **smaller** network
- a **subnet** is a network carved out of a bigger one

You can now look at any address and work out whether it belongs to a given network.
