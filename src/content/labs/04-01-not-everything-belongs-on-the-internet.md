---
phase: 4
order: 1
title: Not everything belongs on the internet
type: concept
time: ~10 min
cost: Free
buildsOn: Lab 3.10
summary: Why real applications are split into tiers, and what makes a server private in AWS.
draft: false
questions:
  - kind: recall
    q: "What makes a server <b>private</b> in AWS?"
    options:
      - "A setting on the server called Private"
      - "It has no public IP, and its subnet has no route to the internet gateway"
      - "Its security group has no rules"
      - "It's in a different Region"
    correct: 1
    hint: "There are two pieces, and you've met both already."
    explain: "A private server has no public IP, so there's no address on the internet that leads to it, and its subnet has no route to the internet gateway, so there's no path out either. Like a public subnet, a private one isn't a special setting: it's just missing the route."

  - kind: cause
    q: "Your database has a strong password. Why should it still be in a private subnet?"
    options:
      - "Private subnets make databases faster"
      - "Passwords don't work on public servers"
      - "If it's public, anyone on the internet can keep trying; if it's private, they can't even reach it"
      - "AWS charges more for public databases"
    correct: 2
    hint: "What stands between a stranger and your data in each case?"
    explain: "A public database has one barrier: its password. Bugs, leaked passwords and weak settings happen, and the whole internet gets to keep trying. A private database can't be reached from the internet at all, so those mistakes can't be exploited from outside."

  - kind: predict
    q: "A server in a private subnet is given a public IP by mistake. Someone on the internet tries to connect. What happens?"
    options:
      - "It works, because it has a public IP"
      - "It fails, because the server's replies have no route back out of the subnet"
      - "AWS removes the public IP automatically"
      - "The security group turns itself off"
    correct: 1
    hint: "Every connection needs replies to get back."
    explain: "The request might arrive, but the server's reply needs a route out to the internet, and a private subnet doesn't have one. So the connection never completes. That's why the route matters, not just the public IP."
---

**What you'll learn:** Why real applications keep most of their servers off the internet, and what makes a server private in AWS.

---

## One server doing everything

So far, one server has done everything. It ran your app, anyone on the internet could reach it, and you logged in to it directly.

That's fine for learning. Real applications are split into layers, called **tiers**, and only one of them faces the internet.

## Three tiers

A typical web application has three:

- **Web tier:** the front door. It accepts requests from the internet.
- **App tier:** the code that does the work. Only the web tier talks to it.
- **Database:** where the data lives. Only the app tier talks to it.

<div class="diagram">
  <img
    src="/images/labs/04-01/three-tiers.svg"
    alt="The internet reaches the web tier in a public subnet. The web tier talks to the app tier, and the app tier talks to the database, both in private subnets. Direct paths from the internet to the app tier and the database are blocked."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">only the front door faces the internet</div>
</div>

Each tier only talks to the one next to it. The internet only ever reaches the front door.

## Why not make everything public?

Anything reachable from the internet gets found quickly. Automated scanners try every public address, all day. If you left your website running, its log probably already shows requests from addresses you don't recognise.

Now picture your database being public. The only thing between a stranger and your data would be its password. If that password leaks, or the database has a bug, anyone on the internet can try.

Put the database somewhere the internet can't reach, and those mistakes can't be exploited from outside. Every server you keep off the internet is one less thing that can be attacked from it.

<div class="callout why"><b>Reachable isn't the same as allowed in.</b> A firewall decides who gets in. Keeping a server private goes further: from the internet, there's no way to reach it at all.</div>

## What makes a server private in AWS

You've already seen what makes a subnet public: a route to the internet gateway. A private server is missing both halves of that:

- **No public IP.** There's no address on the internet that leads to it.
- **No route to the internet gateway.** Its subnet has no path out to the internet.

There's no setting called "private". Like a public subnet, it's defined by its routes.

## What you'll do in this phase

1. Build a private subnet next to `public-a`.
2. Launch a server in it, and find that nobody can reach it, including you.
3. Get in safely, through a server built for exactly that.
4. Find out what being private costs you.
