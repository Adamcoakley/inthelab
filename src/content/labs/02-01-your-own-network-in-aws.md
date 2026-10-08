---
phase: 2
order: 1
title: Your own network in AWS
type: lab
time: ~20 min
cost: Free
buildsOn: Lab 1.5
summary: Create a VPC, your own private network inside AWS, and see that it only exists in one Region.
draft: false
questions:
  - kind: recall
    q: "What is a <b>VPC</b>?"
    options:
      - "A virtual server"
      - "Your own private network inside AWS, in one Region"
      - "A type of firewall rule"
      - "A backup of your AWS account"
    correct: 1
    hint: "The N stands for something you learned about all through Phase 0."
    explain: "A VPC (Virtual Private Cloud) is a private network that belongs to you, inside one AWS Region. Every server you launch in this course lives inside one."

  - kind: cause
    q: "Why give your VPC a <code>/16</code> range instead of a <code>/24</code>?"
    options:
      - "A /16 is cheaper"
      - "AWS only accepts /16 ranges"
      - "A /16 is more secure"
      - "It leaves plenty of room to carve out many subnets later"
    correct: 3
    hint: "Lab 0.3: a smaller slash number means a bigger network."
    explain: "A /16 holds 65,536 addresses, so you can split it into lots of /24 subnets. A /24 VPC would only have room for one /24 subnet, and changing a VPC's range later is awkward."

  - kind: predict
    q: "Another learner also creates a VPC with <code>10.0.0.0/16</code>, in their own account. What happens?"
    options:
      - "AWS refuses, because the range is already taken"
      - "Both VPCs share the same network"
      - "Nothing, because private ranges only have meaning inside each network"
      - "Your VPC gets renamed automatically"
    correct: 2
    hint: "Lab 0.2: two homes can both use 192.168.1.10."
    explain: "10.0.0.0/16 is a private range. Like two homes using the same 192.168.1.10, the same private range in two separate VPCs causes no conflict. It only matters if you ever connect those two networks together."
---

**What you'll do:** Learn what a VPC is, create your own, and see that it only exists in the Region you made it in.

---

## What is a VPC?

A **VPC** (Virtual Private Cloud) is your own private network inside AWS. It's the same idea as the networks from Phase 0, except AWS runs the hardware and you control everything else: which IP addresses it uses, how the network is divided into subnets, and what traffic can get in or out.

A VPC lives in one Region and stretches across all of that Region's Availability Zones. Most Regions have three.

<div class="diagram">
  <img
    src="/images/labs/02-01/vpc-in-region.svg"
    alt="Your VPC, 10.0.0.0/16, inside the eu-west-1 Region and spanning three empty Availability Zones. Underneath, three things created with it: a main route table, a network ACL and a security group."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">a VPC covers one Region, across all its Availability Zones</div>
</div>

Every server you build in this course will live inside this VPC.

## Choosing its address range

A VPC needs a range of private IP addresses. You'll use `10.0.0.0/16`.

- `/16` leaves 16 bits for addresses, which is 65,536 of them.
- That's far more than you need, and that's the point: in the next lab you'll carve it into smaller subnets, and you want room to add more later.

<div class="callout why"><b>Choose generously.</b> Changing a VPC's main range after you've built inside it is awkward. Starting big costs nothing, because AWS doesn't charge for addresses you aren't using.</div>

## The VPC that's already there

Every Region already has a **default VPC** that AWS created for you, using `172.31.0.0/16`. It comes fully wired to the internet, so you can launch a server into it without thinking about networking at all.

That's exactly why you won't use it. Building your own VPC piece by piece is how you'll learn what each piece does. Leave the default VPC alone, you don't need to delete it.

## Step 1: Open the VPC console

1. Check the Region selector in the top-right corner says **Europe (Ireland) eu-west-1**.
2. Search for **VPC** in the console search bar and open it.
3. In the left menu, choose **Your VPCs**.

You'll see one VPC already there, with **Default VPC** set to **Yes** and the range `172.31.0.0/16`.

<figure class="screenshot">
  <img
    src="/images/labs/02-01/default-vpc.png"
    alt="The Your VPCs list showing only the default VPC."
  />
</figure>

## Step 2: Create your VPC

1. Choose **Create VPC**.
2. Under **Resources to create**, choose **VPC only**.
3. **Name tag:** `{{ns}}-vpc`
4. **IPv4 CIDR block:** choose **IPv4 CIDR manual input**, then enter `10.0.0.0/16`.
5. **IPv6 CIDR block:** **No IPv6 CIDR block**
6. **Tenancy:** **Default**
7. Choose **Create VPC**.

<figure class="screenshot">
  <img
    src="/images/labs/02-01/create-vpc.png"
    alt="The Create VPC form with VPC only selected and 10.0.0.0/16 entered."
  />
</figure>

<div class="callout why"><b>Why not "VPC and more"?</b> That option builds subnets, route tables and gateways for you in one click. It's what you'd use once you know what it's doing. For now, you're going to build each of those pieces by hand.</div>

## Step 3: See what came with it

AWS created three things with your VPC automatically. You'll use each of them in later labs.

Your VPC's details page lists a **Main route table** and a **Main network ACL**:

<figure class="screenshot">
  <img
    src="/images/labs/02-01/vpc-details.png"
    alt="The VPCs details tab."
  />
</figure>

- **Route table:** decides where traffic leaving a subnet goes next.
- **Network ACL:** a firewall at the edge of each subnet. The default one allows everything.

In the left menu, **Security groups** also shows a new **default** security group for your VPC:

<figure class="screenshot">
  <img
    src="/images/labs/02-01/default-security-group.png"
    alt="The Security Groups list showing two security groups named default, each with a different VPC ID."
  />
</figure>

- **Security group:** a firewall around each server. AWS uses the default one for any server you don't give its own.

There are two called `default`: one belongs to the default VPC, and one to your new VPC. Check the **VPC ID** column to tell them apart.

## Step 4: Switch Region

1. Open the Region selector and choose **US East (N. Virginia) us-east-1**.
2. Look at **Your VPCs** again.

Your VPC has gone. There's only a default VPC, and it isn't even the same one: every Region has its own.

3. Switch back to **Europe (Ireland) eu-west-1**. Your VPC is back.

<div class="callout break"><b>Nothing was deleted.</b> A VPC is a regional resource, so it only appears in the Region you created it in. If something you built ever goes missing, check the Region first.</div>

## Summary

- A VPC is your own private network in AWS. It lives in one Region and spans all of its Availability Zones.
- Yours is `{{ns}}-vpc`, using `10.0.0.0/16`.
- Every Region has a default VPC. You'll ignore it and build your own.

VPCs are free, so keep this one. You'll build inside it for the rest of the course.
