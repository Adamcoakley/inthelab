---
phase: 3
order: 2
title: My network has no way out
type: lab
time: ~15 min
cost: ~$0.02 an hour while running
buildsOn: Lab 3.1
summary: Add the route that makes a subnet public, and find out why that still isn't enough.
draft: false
questions:
  - kind: recall
    q: "What makes a subnet <b>public</b> in AWS?"
    options:
      - "A setting on the subnet called Public"
      - "Its route table has a 0.0.0.0/0 route to an internet gateway"
      - "Having a server with a public IP inside it"
      - "Having \"public\" in its name"
    correct: 1
    hint: "What did you change in this lab?"
    explain: "A public subnet isn't a special type of resource. It's a subnet whose route table sends 0.0.0.0/0 to an internet gateway. That one route is the whole difference."

  - kind: cause
    q: "Your route table has <code>10.0.0.0/16 → local</code> and <code>0.0.0.0/0 → igw</code>. Why does traffic to <code>10.0.2.15</code> stay inside the VPC?"
    options:
      - "The internet gateway rejects private addresses"
      - "Routes are checked from top to bottom"
      - "The most specific matching route wins, and /16 is more specific than /0"
      - "Private addresses can't use routes"
    correct: 2
    hint: "Lab 0.4: both routes match. Which one is picked?"
    explain: "10.0.2.15 matches both routes. The /16 is the smaller, more specific range, so it wins and the traffic stays local. Only traffic that matches nothing else uses 0.0.0.0/0."

  - kind: predict
    q: "Later, while you're connected over SSH, someone deletes the <code>0.0.0.0/0</code> route. What happens?"
    options:
      - "Your session freezes, because the server's replies have no route back to you"
      - "Nothing, because you're already connected"
      - "The server shuts down"
      - "SSH switches to the private IP automatically"
    correct: 0
    hint: "Every reply from the server is traffic leaving the subnet."
    explain: "Routes apply to every packet, not just the first one. Without the route, the server's replies to your laptop have nowhere to go, so the connection stops responding."
---

**What you'll do:** Add a route to the internet gateway, which turns `public-a` into a public subnet, and test the connection again.

---

## A public subnet is just a route

In AWS, there's no setting that makes a subnet public. A **public subnet** is simply a subnet whose route table sends internet traffic to an internet gateway:

- `0.0.0.0/0` → internet gateway

That's the whole definition. You attached the gateway in a previous lab. Now you'll add the route that leads to it.

## Step 1: Add the route

1. In the VPC console, choose **Route tables**, then `{{ns}}-public-rt`.
2. Open the **Routes** tab and choose **Edit routes**.
3. Choose **Add route**.
4. **Destination:** `0.0.0.0/0`
5. **Target:** choose **Internet Gateway**, then `{{ns}}-igw`.
6. Choose **Save changes**.

<figure class="screenshot">
  <img
    src="/images/labs/03-02/add-route.png"
    alt="The Edit routes page with 0.0.0.0/0 pointing to the internet gateway."
  />
</figure>

Your route table now has two routes:

- `10.0.0.0/16` → `local`
- `0.0.0.0/0` → `{{ns}}-igw`

Traffic to anywhere in your VPC still matches the more specific `/16` route and stays local. Everything else now goes to the internet gateway.

<div class="callout why"><b>That one route is what made public-a public.</b> Nothing else about the subnet changed. In Phase 4, you'll build a private subnet, and the difference will be exactly this: no route to the internet gateway.</div>

## Routes work in both directions

A route doesn't just matter for traffic going out. When your server replies to your laptop, that reply is going to an address outside the VPC. It needs this route to find its way out, too.

## Step 2: Try connecting  to the server again

Run the same SSH command as before:

<div class="os-switch">
<div class="os-tabs"><button type="button" data-os-pick="mac">macOS / Linux</button><button type="button" data-os-pick="windows">Windows</button></div>
<div class="os-panel" data-os="mac">

```bash
ssh -o ConnectTimeout=10 -i ~/Downloads/{{ns}}-key.pem ec2-user@PUBLIC_IP
```

</div>
<div class="os-panel" data-os="windows">

```powershell
ssh -o ConnectTimeout=10 -i $HOME\Downloads\{{ns}}-key.pem ec2-user@PUBLIC_IP
```

</div>
</div>

It still times out.

## Why it still fails

The route was the first broken stop. The next stop is the firewall: the security group you created with no inbound rules.

From your laptop, a missing route and a blocking firewall look exactly the same: the connection times out. That's why you check stops in order rather than guessing.

<div class="diagram">
  <img
    src="/images/labs/03-02/arch-route-added.svg"
    alt="The route table now has 0.0.0.0/0 to the internet gateway. Traffic from your laptop gets through the gateway and across the subnet, but is blocked at the server's security group, which allows nothing in."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">route fixed, next stop: the security group</div>
</div>

## Summary

- A public subnet is a subnet with a `0.0.0.0/0` route to an internet gateway.
- `{{ns}}-public-a` is now public.
- You still can't connect, and the next stop is the security group.

Keep the server for the next lab. If you're taking a break, stop it.
