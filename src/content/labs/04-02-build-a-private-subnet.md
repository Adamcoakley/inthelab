---
phase: 4
order: 2
title: Build a private subnet
type: lab
time: ~15 min
cost: Free
buildsOn: Lab 4.1
summary: Create a second subnet with no route to the internet, and see why it was private from the start.
draft: false
questions:
  - kind: recall
    q: "Which route does <code>public-rt</code> have that <code>private-rt</code> doesn't?"
    options:
      - "10.0.0.0/16 → local"
      - "10.0.2.0/24 → local"
      - "0.0.0.0/0 → internet gateway"
      - "0.0.0.0/0 → local"
    correct: 2
    hint: "Both have the local route. What's the other one?"
    explain: "Both route tables have the local route, which connects every subnet in the VPC. Only public-rt has 0.0.0.0/0 to the internet gateway. That one route is the whole difference between public and private."

  - kind: cause
    q: "<code>private-a</code> was already private the moment you created it. Why?"
    options:
      - "New subnets are always private"
      - "It used the main route table, which only has the local route"
      - "Its name starts with private"
      - "It's in a different Availability Zone"
    correct: 1
    hint: "Which route table does a subnet use before you associate it with one?"
    explain: "A subnet with no route table of its own uses the main route table. Yours only has the local route, so every new subnet starts with no way out. That's why you kept the main route table closed."

  - kind: predict
    q: "Someone adds <code>0.0.0.0/0 → igw</code> to <code>private-rt</code>. What happens to <code>private-a</code>?"
    options:
      - "Nothing, because its name is private-a"
      - "AWS refuses the change"
      - "Only outbound traffic changes"
      - "It becomes a public subnet"
    correct: 3
    hint: "What makes a subnet public?"
    explain: "A subnet with a route to the internet gateway is a public subnet, whatever it's called. Names are just labels: the route table decides."
---

**What you'll do:** Create `private-a`, a subnet with no route to the internet, and give it its own route table.

---

## Where it goes

You'll put `private-a` in the same Availability Zone as `public-a`, using the next range in your VPC: `10.0.2.0/24`. That's every address from `10.0.2.0` to `10.0.2.255`.

## Step 1: Create the subnet

1. In the VPC console, choose **Subnets**, then **Create subnet**.
2. **VPC ID:** `{{ns}}-vpc`
3. **Subnet name:** `{{ns}}-private-a`
4. **Availability Zone:** **Europe (Ireland) / eu-west-1a**
5. **IPv4 subnet CIDR block:** `10.0.2.0/24`
6. Choose **Create subnet**.

<div class="callout shot">screenshot: the Create subnet form with private-a, eu-west-1a and 10.0.2.0/24 filled in<br>save as <code>/images/labs/04-02/create-private-subnet.png</code></div>
<!--
<figure class="screenshot">
  <img
    src="/images/labs/04-02/create-private-subnet.png"
    alt="The Create subnet form with private-a, eu-west-1a and 10.0.2.0/24 filled in."
  />
</figure>
-->

## Step 2: Check its routes

1. Select `{{ns}}-private-a` and open the **Route table** tab.

It's using `{{ns}}-main-rt`, the main route table, because you haven't given it one of its own. It has one route:

- `10.0.0.0/16` → `local`

There's no route to the internet gateway. Your new subnet is already private.

<div class="callout why"><b>This is why the main route table stayed closed.</b> Any subnet you don't associate with a route table falls back to the main one. Because yours only has the local route, every new subnet starts out private. Making a subnet public is always a deliberate choice.</div>

## Step 3: Give it its own route table

It's private already, but you'll still give it a route table of its own. In the next phase you'll add a route to it, and you don't want that change to apply to every other subnet that uses the main route table.

1. Choose **Route tables**, then **Create route table**.
2. **Name:** `{{ns}}-private-rt`
3. **VPC:** `{{ns}}-vpc`
4. Choose **Create route table**.
5. Open the **Subnet associations** tab and choose **Edit subnet associations**.
6. Tick `{{ns}}-private-a` and choose **Save associations**.

Open the **Routes** tab. It has only the `local` route.

<div class="callout shot">screenshot: the Routes tab of private-rt showing only the local route<br>save as <code>/images/labs/04-02/private-rt-routes.png</code></div>
<!--
<figure class="screenshot">
  <img
    src="/images/labs/04-02/private-rt-routes.png"
    alt="The Routes tab of private-rt showing only the local route."
  />
</figure>
-->

## Public and private, side by side

Your VPC now has two subnets in the same Availability Zone. The only difference between them is one route.

<div class="diagram">
  <img
    src="/images/labs/04-02/public-vs-private.svg"
    alt="Two subnets in your VPC. public-a uses public-rt, which has the local route and 0.0.0.0/0 to the internet gateway. private-a uses private-rt, which only has the local route, so it has no way out."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">one route is the whole difference</div>
</div>

Both route tables have the `local` route, so servers in the two subnets can still reach each other. Only `public-a` can reach the internet.

## Summary

- `{{ns}}-private-a` uses `10.0.2.0/24` in `eu-west-1a`.
- It has its own route table, `{{ns}}-private-rt`, with only the `local` route.
- A new subnet starts private, because the main route table has no route out.

Subnets and route tables are free. Keep them for the next lab.
