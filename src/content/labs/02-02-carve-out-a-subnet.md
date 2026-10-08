---
phase: 2
order: 2
title: Carve out a subnet
type: lab
time: ~20 min
cost: Free
buildsOn: Lab 2.1
summary: Split your VPC into a subnet in one Availability Zone, and see why a /24 gives you 251 addresses, not 256.
draft: false
questions:
  - kind: recall
    q: "How many addresses can you use for your own resources in a <code>/24</code> subnet in AWS?"
    options:
      - "256"
      - "254"
      - "251"
      - "128"
    correct: 2
    hint: "Look at the Available IPv4 addresses column."
    explain: "A /24 has 256 addresses, but AWS reserves 5 in every subnet: the network address, the VPC router, DNS, one held back for future use, and the broadcast address. That leaves 251."

  - kind: cause
    q: "You tried to create a subnet with <code>10.0.1.128/25</code> and AWS refused. Why?"
    options:
      - "/25 subnets aren't allowed in AWS"
      - "It overlaps with public-a, which already uses 10.0.1.0 to 10.0.1.255"
      - "It's outside the VPC's range"
      - "You can only have one subnet per VPC"
    correct: 1
    hint: "Lab 0.3: no gap and no overlap."
    explain: "10.0.1.128/25 covers 10.0.1.128 to 10.0.1.255, which is already part of public-a. Two subnets in the same VPC can never share addresses."

  - kind: predict
    q: "You want a server to run in <code>eu-west-1b</code>. Can you launch it into <code>public-a</code>?"
    options:
      - "Yes, subnets cover the whole Region"
      - "Yes, if you pick eu-west-1b during launch"
      - "Only if the VPC is in eu-west-1b"
      - "No, public-a only exists in eu-west-1a, so you'd need a subnet in eu-west-1b"
    correct: 3
    hint: "Which one spans every AZ: the VPC or the subnet?"
    explain: "The VPC spans every AZ, but each subnet lives in exactly one. Choosing a subnet is how you choose where a server physically runs. You'll create a subnet in eu-west-1b in Phase 6."
---

**What you'll do:** Create your first subnet in one Availability Zone, check how many addresses it really has, and try to create one that doesn't fit.

---

## Subnets live in one Availability Zone

In phase 0 we learned that a subnet was a smaller network carved out of a bigger network. In AWS it's exactly that, with one extra rule: **every subnet lives in exactly one Availability Zone.**

Your VPC spans every AZ in the Region. The subnets inside it don't. So when you choose which subnet a server goes into, you're also choosing which AZ.

## The plan for your VPC

You'll build four subnets over the course, but only one today.

<div class="diagram">
  <img
    src="/images/labs/02-02/subnet-plan.svg"
    alt="Your VPC with two Availability Zones. eu-west-1a holds public-a, 10.0.1.0/24, built now, and private-a, 10.0.2.0/24, in phase 4. eu-west-1b holds public-b and private-b, 10.0.3.0/24 and 10.0.4.0/24, in phase 6."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the four subnets this course builds, and when</div>
</div>

You'll call this one `public-a`, even though it isn't public yet. In AWS, a subnet doesn't become public through a setting.

## Step 1: Create the subnet

1. In the VPC console, choose **Subnets** in the left menu, then **Create subnet**.
2. **VPC ID:** choose `{{ns}}-vpc`.
3. **Subnet name:** `{{ns}}-public-a`
4. **Availability Zone:** **Europe (Ireland) / eu-west-1a**
5. **IPv4 VPC CIDR block:** leave it as `10.0.0.0/16`.
6. **IPv4 subnet CIDR block:** `10.0.1.0/24`
7. Choose **Create subnet**.

<figure class="screenshot">
  <img
    src="/images/labs/02-02/create-subnet.png"
    alt="The Create subnet form with the name, eu-west-1a and 10.0.1.0/24 filled in."
  />
</figure>

## Step 2: Count the addresses

Find `{{ns}}-public-a` in the subnet list and look at the **Available IPv4 addresses** column.

It says **251**, not 256.

<figure class="screenshot">
  <img
    src="/images/labs/02-02/available-addresses.png"
    alt="The subnet list showing 251 available IPv4 addresses."
  />
</figure>

AWS reserves five addresses in every subnet:

<div class="diagram">
  <img
    src="/images/labs/02-02/reserved-addresses.svg"
    alt="The 256 addresses of 10.0.1.0/24. .0, .1, .2, .3 and .255 are reserved: network address, VPC router (your default gateway), AWS DNS, held back for future use, and broadcast. .4 to .254 leaves 251 for your servers."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">five addresses in every subnet belong to AWS</div>
</div>

The address ending in `.1` is the **VPC router**. There is one router for the whole VPC, and it's reached at `.1` in every subnet. Traffic leaving a subnet goes there first, and the subnet's route table decides where it goes next.

## Step 3: Try to create subnets that don't fit

AWS checks every new subnet against two rules: it must sit inside the VPC's range, and it can't overlap another subnet. You'll break each rule once.

### A subnet outside the VPC

1. Choose **Create subnet** and pick `{{ns}}-vpc`.
2. **Subnet name:** `test`
3. **IPv4 subnet CIDR block:** `10.1.0.0/24`
4. Choose **Create subnet**.

AWS refuses.

<div class="callout break"><b>But a /24 is smaller than a /16.</b> So why doesn't it fit inside?</div>

Every address in a CIDR block starts the same way. The slash number says how much stays the same: `/16` keeps the first two numbers, and `/24` keeps the first three. The address in front tells you what those numbers are.

These are two different networks. Your VPC is `10.0.0.0/16`: every address that starts with `10.0`. The subnet you tried to create is `10.1.0.0/24`: every address that starts with `10.1.0`.

The two don't share a single address. The subnet `test` isn't a smaller piece of your VPC, it's a small network somewhere else entirely.

A subnet has to be carved out of the VPC, so its first two numbers must be the VPC's `10.0`.

5. Choose **Cancel**.

### A subnet that overlaps public-a

Remember, `public-a` is `10.0.1.0/24`: every address from `10.0.1.0` up to `10.0.1.255`.

1. Choose **Create subnet** and pick `{{ns}}-vpc`.
2. **Subnet name:** `test`
3. **IPv4 subnet CIDR block:** `10.0.1.128/25`
4. Choose **Create subnet**.

This one starts with `10.0`, so unlike the last attempt, it's inside your VPC. AWS still refuses.

A `/25` is half the size of a `/24`: 128 addresses instead of 256. Starting at `10.0.1.128`, it runs up to `10.0.1.255`. That's the second half of `public-a`, and those addresses are already taken.

<figure class="screenshot">
  <img
    src="/images/labs/02-02/overlap-error.png"
    alt="The error shown when the subnet overlaps public-a."
  />
</figure>

5. Choose **Cancel**.

Below are both attempts visualised. In each one, compare the `test` subnet's range with the range it was meant to fit inside.

<div class="diagram">
  <img
    src="/images/labs/02-02/subnets-that-dont-fit.svg"
    alt="First attempt: 10.1.0.0/24 starts with 10.1, but every address in the VPC, 10.0.0.0 to 10.0.255.255, starts with 10.0. Second attempt: test, 10.0.1.128/25, lands on the second half of public-a, 10.0.1.128 to .255, which public-a already owns."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the first starts outside your VPC, the second lands on addresses public-a already owns</div>
</div>

## Summary

- A subnet is a slice of your VPC's range, and it lives in one Availability Zone.
- You have `{{ns}}-public-a`, `10.0.1.0/24`, in `eu-west-1a`.
- AWS reserves 5 addresses in every subnet. `.1` is the router.
- A new subnet must sit inside the VPC's range, and can't overlap another subnet. Being smaller isn't enough: it has to start in the right place.

Subnets are free. Keep this one for the next lab.