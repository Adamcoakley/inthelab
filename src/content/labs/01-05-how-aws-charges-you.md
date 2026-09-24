---
phase: 1
order: 5
title: How AWS charges you
type: concept
time: ~20 min
cost: Free
buildsOn: Lab 1.4
summary: What costs money in AWS, how to track your spending, and how Phase 0 concepts map to AWS services.
draft: false
questions:
  - kind: recall
    q: "You <b>stop</b> an EC2 server. What do you still pay for?"
    options:
      - "Nothing at all"
      - "The server's running time"
      - "Its disk, which still exists"
      - "Double, as a penalty"
    correct: 2
    hint: "Stopping turns the computer off. Does its storage disappear?"
    explain: "A stopped server doesn't charge for compute time, but its disk still exists and storage is still billed."

  - kind: cause
    q: "Your budget email arrives, but you're sure you deleted everything. Where should you look first?"
    options:
      - "In the IAM users list"
      - "In other Regions, and on the Bills page to see which service is charging"
      - "In the root user's password settings"
      - "Nowhere, budget emails are often wrong"
    correct: 1
    hint: "Lab 1.3: things are regional."
    explain: "The Bills page shows which services and Regions are costing money. A forgotten resource may be in a Region you weren't looking at."

  - kind: predict
    q: "Which of these keeps costing money even when nobody is using it?"
    options:
      - "An IAM user"
      - "A security group"
      - "A public IPv4 address"
      - "A tag"
    correct: 2
    hint: "Look at the types of charge at the top of the lab."
    explain: "AWS charges for public IPv4 addresses by the hour, whether or not they're being used. IAM users, security groups and tags are free."
---

**What you'll learn:** What AWS charges for, what still costs money when idle, how to check your spending, and the AWS names for the Phase 0 concepts.

---

## What AWS charges for

Most AWS pricing is based on usage: how long something runs, how much you store, or how much data you send.

That's what makes it flexible, as covered in Lab 0.1. It also means a resource you forget about can keep costing money until you delete it.

- **Running time:** servers are charged while they're running. Load balancers and NAT gateways are charged for every hour they exist, busy or not.
- **Storage:** disks, snapshots and files are charged based on how much storage you use. Disks are charged for their allocated size, even if they're mostly empty.
- **Data out:** data sent from AWS to the internet can be charged per GB. Incoming data is generally free.
- **Public IPv4 addresses:** about `$0.005` an hour each, roughly `$3.65` for a 730-hour month, even if unused.

Plenty of things are free, including IAM users, groups and policies, VPCs, subnets, route tables and security groups.

## Stop vs terminate

These are charged differently:

- **Stop a server:** it's turned off. You aren't charged for compute time, but its disk still exists and is still billed.
- **Terminate a server:** the server is deleted permanently. Its main disk is normally deleted with it.

Other services mostly just say **delete**. Each lab tells you what to delete at the end and what to keep for the next one.

## Checking your spending

Search for **Billing and Cost Management** and open it.

The **Home** page gives you a quick view of your AWS spending. This is a useful place to check whether anything you’ve created is starting to cost money.

<figure class="screenshot">
  <img
    src="/images/labs/01-05/billing-home.png"
    alt="AWS Billing and Cost Management home page."
  />
</figure>

## Names and tags

Everything you create in this course should be created with your name first, like `{{ns}}-vpc` or `{{ns}}-webserver-1`, so it's easy to tell what each resource is.

AWS resources can have tags: simple key-value labels that help you organise and identify them.

For example: `project = inthelab`

Companies use tags to track costs by project or team.

## IDs and ARNs

AWS resources are given identifiers so AWS can tell them apart.

An **ID** is usually a shorter identifier for a resource. For example:

- EC2 instance: `i-0a1b2c3d4e5f67890`
- VPC: `vpc-0a1b2c3d`

These IDs are unique within the AWS account, Region or service where the resource exists.

An **ARN** stands for Amazon Resource Name. It is the full identifier AWS uses to uniquely identify a resource across AWS.

You saw one in the last lab:

```text
arn:aws:iam::123456789012:user/admin
```

It contains several pieces:

- `arn:aws` → tells us this is an AWS resource
- `iam` → the service
- `123456789012` → the AWS account ID
- `user/admin` → the resource itself

A regional resource includes its Region. For example, an EC2 instance in Ireland might have an ARN like:

```text
arn:aws:ec2:eu-west-1:123456789012:instance/i-0a1b2c3d4e5f67890
```

You'll mostly come across ARNs in permissions, policies and error messages.

## Phase 0 concepts in AWS

Most of the networking ideas you learned in Phase 0 have an AWS equivalent.

You already know what the pieces do. From here on, you’ll start learning the AWS names for them and building them yourself.

<div class="diagram">
  <img
    src="/images/labs/01-05/pricing-meters.svg"
    alt="Four meters showing running time, storage, data sent out and public IPv4 addresses as common types of AWS charges."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the main types of charge you'll see in this course</div>
</div>

## Cleaning up after labs

Labs that create paid resources end with a cleanup step.

Each time:

1. Delete what the lab tells you to.
2. Make sure you're in the right Region.
3. Check Billing later and look into anything unexpected.

In Phase 2, you'll start building these pieces yourself in AWS.