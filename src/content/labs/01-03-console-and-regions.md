---
phase: 1
order: 3
title: The console and Regions
type: concept
time: ~20 min
cost: Free
buildsOn: Lab 1.2
summary: The parts of the AWS console you'll use most, and how Regions affect what you see.
draft: false
questions:
  - kind: recall
    q: "Which of these is <b>global</b> rather than tied to one Region?"
    options:
      - "An EC2 server"
      - "An IAM user"
      - "A VPC"
      - "A server's disk"
    correct: 1
    hint: "What did the Region selector show when you were in IAM?"
    explain: "IAM is global, so users, groups and policies work in every Region. Servers, VPCs and disks are regional: they exist in the Region where you created them."

  - kind: cause
    q: "You launched a server yesterday. Today the EC2 page shows no servers at all. What's the most likely reason?"
    options:
      - "AWS deleted it overnight"
      - "The console is showing a different Region"
      - "Your budget turned it off"
      - "Servers are hidden after 24 hours"
    correct: 1
    hint: "Servers are regional. What does the top-right corner say?"
    explain: "EC2 only shows the servers in the Region you've selected. Switch back to eu-west-1 and it'll be there."

  - kind: predict
    q: "You create an IAM user while the console shows eu-west-1. Can that user sign in if you later switch to us-east-1?"
    options:
      - "No, the user only exists in eu-west-1"
      - "Yes, IAM is global"
      - "Only after you copy the user across"
      - "Only with the root user's approval"
    correct: 1
    hint: "What did the Region selector say when you were in IAM?"
    explain: "IAM is global. Users, groups and policies work in every Region."
---

**What you'll do:** Get familiar with the console, set your default Region, and see how Regions affect what the console shows.

---

## The console

AWS has hundreds of services, but you'll only use a handful, and a few parts of the console are worth knowing from the start.

<figure class="screenshot">
  <img
    src="/images/labs/01-03/console-home.png"
    alt="AWS console dashboard"
  />
</figure>

1. **Search bar:** the quickest way to open a service. Type `EC2`, `IAM` or `Budgets` and press enter.
2. **Region selector:** which Region you're working in. More on this below.
3. **Account menu:** your user name, account ID, security credentials and sign-out.
4. **CloudShell:** a command line that runs in your browser. You'll use it in the next lab.

## Regions

As covered in Lab 0.1, AWS is split into **Regions**, each with its own data centres. Each Region has a code:

- `eu-west-1`: Ireland
- `eu-west-2`: London
- `us-east-1`: N. Virginia

All labs in this course use **`eu-west-1`** (Ireland). It's the closest Region and has every service the course uses.

<div class="callout why"><b>How do companies choose a Region?</b> Mainly by distance to their users, legal requirements on where data is stored, which services are available, and cost, which varies slightly between Regions.</div>

## Global vs regional services

A few services, like IAM, are **global**. That means they are not tied to one specific AWS Region.

For example, an IAM user you create is available across your AWS account, not just in `eu-west-1`. That’s why IAM showed **Global** in the last lab.

Most AWS services are **regional**. If you create a server in `eu-west-1`, it exists in that Region, and you need to have `eu-west-1` selected in the console to see it.

<div class="diagram">
  <img
    src="/images/labs/01-03/global-vs-regional.svg"
    alt="A global band containing IAM users, billing and Route 53, above three Regions. Only eu-west-1 contains your server; us-east-1 and eu-central-1 are empty."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the console only shows resources in the selected Region</div>
</div>

<div class="callout break"><b>Can't find something you created?</b> Check the Region selector first. It's the most common reason.</div>

## Common terms

You'll see these throughout the console:

- **Resource:** any single thing you create, like a server, a network or a user.
- **Instance:** a virtual server in EC2.
- **ID:** a unique identifier AWS gives every resource, like `i-0a1b2c3d4e5f67890` for a server.
- **Tag:** a label you add to a resource, like `Name = {{ns}}-web-1`. The **Name** tag is what most lists display.

## Summary

- Most services are regional, so the console only shows what's in the selected Region.
- IAM and billing are global.
