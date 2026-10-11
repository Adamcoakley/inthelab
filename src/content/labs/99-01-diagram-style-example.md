---
phase: 99
order: 1
title: How do I get in? (style example)
type: lab
time: ~35 min
cost: ~$0.03 an hour while running
buildsOn: Lab 4.3
summary: A sample lab page showing the new diagram style. Not part of the roadmap.
draft: false
---

**What you'll do:** Launch a bastion host in `public-a`, connect through it to your private server, and allow that with a security group rule that names a group instead of an address.

---

## One way in

A **bastion host** is a small server in a public subnet whose only job is to be the way in. You SSH to the bastion, and from there to your private servers.

<div class="diagram">
  <img
    src="/images/style/example-architecture.svg"
    alt="Your laptop connects to the bastion in public-a, through the internet gateway. From the bastion, the connection continues to app-1 in private-a, whose security group allows SSH from bastion-sg."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">two hops: your laptop to the bastion, then the bastion to the private server</div>
</div>

Only the bastion is reachable from the internet, and only by you. Your private servers only accept SSH from the bastion.

## Step 1: Launch the bastion

1. In the EC2 console, choose **Instances**, then **Launch instances**.
2. **Name:** `{{ns}}-bastion`
3. **Instance type:** `t3.micro`

When it's running, note down its **Public IPv4 address**:

<figure class="screenshot">
  <img
    src="/images/labs/03-01/instance-details.png"
    alt="The instance details showing the public and private IPv4 addresses."
  />
</figure>

## Why the security group matters

Remember what a firewall does: it decides which traffic gets in, port by port.

<div class="diagram">
  <img
    src="/images/style/example-concept.svg"
    alt="The internet reaches port 443 through the firewall, but is blocked from port 22. Your laptop reaches port 22. Nothing outside can reach port 3306."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">one server, three services, three different levels of access</div>
</div>

<div class="callout why"><b>Reachable isn't the same as allowed in.</b> The route gets traffic to the server. The security group decides whether it's let in.</div>

## Step 2: Connect

```bash
ssh bastion
```

Your prompt shows the bastion's private IP, something like `[ec2-user@ip-10-0-1-20 ~]$`.
