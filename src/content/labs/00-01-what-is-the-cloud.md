---
phase: 0
order: 1
title: What actually is "the cloud"?
type: concept
time: ~15 min
summary: Servers are just computers. Everything else follows from that one idea.
draft: false
questions:
  - kind: recall
    q: "What does <b>virtualisation</b> let you do?"
    options:
      - "Make a physical server run faster"
      - "Split one physical computer into several independent virtual ones"
      - "Copy files between two servers"
      - "Connect a server to the internet"
    correct: 1
    hint: "Think about how AWS can rent you a small server without buying a small computer."
    explain: "Virtualisation divides one physical machine's CPU, memory and disk between several virtual machines, each behaving like its own computer. That is what makes renting a slice of a server possible, and why you can start one in seconds instead of buying hardware."
  - kind: cause
    q: "A company buys enough servers to handle its busiest day of the year. What is the problem with that?"
    options:
      - "The servers will be too slow on the busy day"
      - "They pay for that much capacity every day, even when almost none of it is used"
      - "The servers cannot be connected to the internet"
      - "They will run out of IP addresses"
    correct: 1
    hint: "Look at the gap between the flat line and the curve."
    explain: "Owning hardware means sizing for your peak and paying for that peak permanently. Every gap between the flat capacity line and the demand curve is money spent on idle machines. Renting on demand lets capacity follow the curve instead."
  - kind: predict
    q: "You rent an EC2 virtual machine from AWS. A security update is released for its operating system. Who installs it?"
    options:
      - "AWS, automatically"
      - "Nobody, it is not needed in the cloud"
      - "You do"
      - "The data centre technician"
    correct: 2
    hint: "Which side of the line is the operating system on?"
    explain: "AWS secures the building, the hardware and the virtualisation layer, everything up to where your virtual machine begins. The operating system inside it, and everything you install on it, is yours. This split is the Shared Responsibility Model, and misunderstanding it causes a lot of real breaches."
---

**What you'll learn:** What a server actually is, why renting one changes everything, and how AWS is physically laid out. 

---

## A server is just a computer

Strip away the word "cloud" for a moment. A server is a computer, the same as the one in front of you. It has a processor, memory, a disk, and a network connection. It is simply built to run continuously and be used by other machines rather than by a person sitting at it.

<div class="diagram">
  <img
    src="/images/labs/00-01/server-anatomy.svg"
    alt="A server with CPU, memory, disk and network components labelled."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">a server and four of it's core parts</div>
</div>

## Buying versus renting

If you own physical servers, you have to buy for your busiest moment: Black Friday, a concert ticket release, a big product launch. Most days, you won't need anywhere near that much capacity. The problem is that you still own and pay for all that capacity, even when it's not being used.

<div class="diagram">
  <img
    src="/images/labs/00-01/capacity-vs-demand.svg"
    alt="A capacity graph comparing fixed purchased capacity with changing demand."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">every shaded gap is capacity you paid for and did not use</div>
</div>

<div class="callout why"><b>This is the problem the cloud solves first.</b> Instead of buying enough servers for your busiest day, you can add capacity when demand rises and give it back when demand falls. </div>

## How one computer becomes many

If AWS had to hand you a whole physical machine every time you asked for a small server, none of this would work. **Virtualisation** is the answer: software divides one machine into slices, and each slice behaves like a complete, independent computer that cannot see the others.

<div class="diagram">
  <img
    src="/images/labs/00-01/virtualisation.svg"
    alt="One physical server divided by a virtualisation layer into several virtual machines."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">one real machine underneath, three independent computers on top</div>
</div>

When you launch an EC2 instance later, this is what you are getting: a slice of a machine in a building you will never visit.

## How much do you want to manage?

Running an application takes more than just your code. Someone has to look after the physical server, the operating system, the software your application needs, and the application itself.

You can manage all of that yourself, or let a cloud provider manage some of it for you. The further right you go below, the more the provider takes care of.

<div class="diagram">
  <img
    src="/images/labs/00-01/service-models.svg"
    alt="A comparison of what you manage across on-premises, IaaS, PaaS and SaaS."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the further right, the less you look after and the less you control</div>
</div>

This course starts with virtual machines (EC2). AWS looks after the physical hardware, while you manage the operating system and what runs on it. 

## Where your server physically lives

"The cloud" is an unhelpful word. It suggests something floating and placeless. It is the opposite: buildings, with security guards, full of racks of machines, in specific countries.

<div class="diagram">
  <img
    src="/images/labs/00-01/regions-azs.svg"
    alt="Two separate Availability Zones inside one AWS Region."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">a Region is an area containing several separate data centres</div>
</div>

When you create a resource in AWS, you choose a Region - a part of the world where AWS has infrastructure, such as Ireland.

Each Region is split into several Availability Zones (AZs). These are separate locations within the Region, designed so that a problem in one does not necessarily affect the others.

## So who secures what?

<div class="callout break"><b>Think about it first.</b> AWS owns the building, the physical computer, and the virtualisation layer that created your virtual machine. So when a security update comes out for the operating system inside your virtual machine, does AWS install it for you?</div>

No. The line between what they secure and what you secure is one of the most important things to get straight early.

<div class="diagram">
  <img
    src="/images/labs/00-01/shared-responsibility.svg"
    alt="The AWS Shared Responsibility Model showing what the customer secures and what AWS secures."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the Shared Responsibility Model, in one picture</div>
</div>

Almost everything on the left is something you have to configure correctly, and almost every real-world breach happens there rather than on AWS's side: a server left open to the internet, a permission set too wide, an unpatched operating system.
