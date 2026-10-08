---
phase: 3
order: 10
title: Patch it, then make a template
type: lab
time: ~35 min
cost: ~$0.02 an hour while running
buildsOn: Lab 3.9
summary: Install updates on your server, turn it into an AMI, and launch an identical copy from it.
draft: false
questions:
  - kind: recall
    q: "What's the difference between an <b>instance</b> and an <b>AMI</b>?"
    options:
      - "They're the same thing"
      - "An AMI is a bigger instance"
      - "An instance is a running machine; an AMI is the template you launch machines from"
      - "An AMI is an instance that's been stopped"
    correct: 2
    hint: "You launched web-3 from one, without setting anything up."
    explain: "An instance is a running server. An AMI is a saved disk image you start new instances from. One AMI can launch as many identical instances as you want."

  - kind: cause
    q: "You launched <code>web-3</code> from your AMI with no user data, and the website worked straight away. Why?"
    options:
      - "The app and its service were already on the disk image"
      - "AWS copied web-2's user data"
      - "The AMI downloads the app on boot"
      - "web-3 is sharing web-2's disk"
    correct: 0
    hint: "What did the AMI copy?"
    explain: "The AMI is a copy of web-2's disk, with the app installed and the service enabled. web-3 started with an exact copy, so systemd started the app on its first boot."

  - kind: predict
    q: "On <code>web-3</code>, you run <code>aws sts get-caller-identity</code>. What happens?"
    options:
      - "It shows web-role, copied from web-2"
      - "It shows your admin user"
      - "It shows web-2's instance ID"
      - "Unable to locate credentials, because roles are attached to instances, not saved in AMIs"
    correct: 3
    hint: "Where does the role live: on the disk, or on the instance?"
    explain: "A role is attached to an instance in AWS, not stored on its disk, so the AMI didn't copy it. web-3 has no role until you attach one. That's a good thing: copying a disk never copies permissions."
---

**What you'll do:** Install the latest updates on your server, save it as an AMI, and launch an identical server from it. Then clean up Phase 3.

---

## Your side of the line

In Lab 0.1, the Shared Responsibility Model split security between AWS and you. AWS keeps the hardware and virtualisation up to date. Everything inside your instance, starting with the operating system, is yours. Nobody else is going to install its updates.

## Step 1: Install updates

SSH in to `{{ns}}-web-2`. Check what updates are waiting:

```bash
sudo dnf check-update
```

Then install them:

```bash
sudo dnf update -y
```

`dnf` is Amazon Linux's package manager. It downloads updates from the internet, which works because `public-a` has a route out.

If nothing needs updating, that's fine: your AMI was recent. On a real server, you'd do this regularly.

<div class="callout why"><b>Amazon Linux 2023 releases.</b> <code>dnf update</code> keeps you up to date within your current release. When a newer release is out, you'll see a message when you log in. Moving to it is a separate, deliberate step.</div>

## AMIs: a server you can copy

In Lab 3.8, user data built a server from nothing on every launch. There's another way: set one server up exactly how you want it, then copy its disk into an **AMI**. Every server launched from that AMI starts as an exact copy, with nothing to install.

<div class="diagram">
  <img
    src="/images/labs/03-10/ami-bake.svg"
    alt="web-2, patched and with the app installed, is turned into an AMI called web-ami, backed by a disk snapshot. Three identical servers launch from it. User data builds a server on every boot; an AMI builds it once and copies it."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">build it once, launch it many times</div>
</div>

The Amazon Linux 2023 image you've been launching is an AMI too. Now you're making your own.

## Step 2: Create an AMI

1. In the EC2 console, select `{{ns}}-web-2`.
2. Choose **Actions**, **Image and templates**, then **Create image**.
3. **Image name:** `{{ns}}-web-ami`
4. **Image description:** `Patched Amazon Linux with the hello server`
5. Leave **Reboot instance** ticked. Rebooting makes sure everything on the disk is saved properly before it's copied.
6. Choose **Create image**.

<div class="callout shot">screenshot: the Create image form with the name and description filled in<br>save as <code>/images/labs/03-10/create-image.png</code></div>
<!--
<figure class="screenshot">
  <img
    src="/images/labs/03-10/create-image.png"
    alt="The Create image form with the name and description filled in."
  />
</figure>
-->

## Step 3: Wait for it

1. In the left menu, choose **AMIs**, under **Images**.
2. Wait for your AMI's **Status** to go from **Pending** to **Available**. This takes a few minutes.

Then choose **Snapshots**, under **Elastic Block Store**. There's a new snapshot: the copy of `web-2`'s disk that your AMI is built from.

## Step 4: Launch from your AMI

1. In **AMIs**, select `{{ns}}-web-ami` and choose **Launch instance from AMI**.
2. **Name:** `{{ns}}-web-3`
3. **Instance type:** `t3.micro`
4. **Key pair:** `{{ns}}-key`
5. Under **Network settings**, choose **Edit**: VPC `{{ns}}-vpc`, subnet `{{ns}}-public-a`, **Auto-assign public IP** **Enable**, and **Select existing security group** `{{ns}}-web-sg`.
6. Leave **User data** empty.
7. Choose **Launch instance**.

## Step 5: Open it

Once it's running, open `http://WEB_3_PUBLIC_IP`.

The page loads straight away, with a new server name. There was no script and nothing to download: the app and its service were already on the disk.

<div class="callout break"><b>An AMI copies everything on the disk.</b> If you'd saved access keys or passwords on <code>web-2</code>, every server launched from this AMI would have them too. That's one more reason Lab 3.9 used a role.</div>

## User data or AMI?

Both get you a server that's ready without logging in. They make a different trade:

- **User data** builds the server on every launch. It's easy to change, but each launch takes longer, and needs to download things.
- **An AMI** builds it once. Launches are fast and identical, and need nothing from the internet. But changing it means making a new AMI.

Real teams often combine them: an AMI with the slow, stable parts, and a little user data for the rest. Keep that "needs nothing from the internet" in mind for Phase 4.

## Clean up Phase 3

Servers cost money while they run, so delete both of them:

1. In **Instances**, select `{{ns}}-web-2` and `{{ns}}-web-3`.
2. Choose **Instance state**, then **Terminate (delete) instance**, and confirm.

Keep everything else. Most of it is free, and you'll use it in Phase 4:

- **VPC, subnet, route tables and internet gateway:** free.
- **Security group, key pair and IAM role:** free.
- **`{{ns}}-web-ami` and its snapshot:** a few cents a month for the snapshot storage. Phase 4 launches a server from it into a subnet that can't download anything.

<div class="callout why"><b>When you're done with an AMI for good:</b> deregister it, then delete its snapshot separately in <b>Snapshots</b>. Deregistering on its own leaves the snapshot behind, and you keep paying for it.</div>

## Summary

- Installing operating system updates is your job, not AWS's.
- An AMI is a saved copy of a server's disk that you launch new servers from.
- `{{ns}}-web-3` launched from your AMI ready to go, with no setup.
- AMIs copy the disk, not the role, so permissions never come along by accident.

That's Phase 3. You've launched, connected to, explored, rebuilt and copied a real server, and you know what every part of its network does.
