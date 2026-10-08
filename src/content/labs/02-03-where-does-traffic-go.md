---
phase: 2
order: 3
title: Where does traffic go?
type: lab
time: ~25 min
cost: Free
buildsOn: Lab 2.2
summary: Read your VPC's route table, give your subnet its own, and attach an internet gateway.
draft: false
questions:
  - kind: recall
    q: "What does the <code>local</code> route in a VPC route table do?"
    options:
      - "Delivers traffic for any address in the VPC, inside the VPC"
      - "Sends traffic to the internet"
      - "Blocks traffic from outside the VPC"
      - "Sends traffic to your laptop"
    correct: 0
    hint: "Look at the destination it's paired with."
    explain: "The local route covers the whole VPC range, 10.0.0.0/16. Any traffic to an address in that range is delivered inside the VPC. It's why every subnet in a VPC can reach every other one, and you can't delete it."

  - kind: cause
    q: "Why give <code>public-a</code> its own route table, instead of adding routes to the main one?"
    options:
      - "Each subnet must have a different route table"
      - "The main route table can't hold more than one route"
      - "Custom route tables are faster"
      - "The main route table is used by every subnet you don't associate, so an internet route there would make new subnets public by accident"
    correct: 3
    hint: "What happens to a new subnet that you don't associate with anything?"
    explain: "Any subnet without an explicit association falls back to the main route table. Keeping the main one with only the local route means new subnets start out private. You choose which ones get a way out."

  - kind: predict
    q: "Your internet gateway is attached, but the route table only has the <code>local</code> route. A server in <code>public-a</code> has a public IP. Can you reach it from the internet?"
    options:
      - "Yes, attaching the gateway is enough"
      - "No, nothing in the route table sends traffic to the gateway"
      - "Yes, because it has a public IP"
      - "Only from inside the same Region"
    correct: 1
    hint: "Lab 0.4: a route tells traffic where to go next."
    explain: "Traffic only uses the internet gateway if a route sends it there. With only the local route, the server's replies have nowhere to go outside the VPC. You'll prove this with a real server in Lab 3.1."
---

**What you'll do:** Read the route table AWS created for your VPC, give your subnet its own, and attach an internet gateway.

---

## Every subnet has a route table

Every device on a network needs to know where to send traffic. Your laptop uses a routing table: a short list saying where traffic for each destination should go next. Anything on your own network is sent directly to its destination, everything else goes to your router and out to the internet.

Every subnet in AWS has a route table too. It answers the same question: for this destination, where should traffic go next?

Every VPC comes with a **main route table**, which is the default for any subnet you haven't given its own. Right now, `{{ns}}-public-a` uses it.

## Step 1: Read the main route table

1. In the VPC console, choose **Route tables** in the left menu.
2. Find the one for `{{ns}}-vpc` where **Main** is **Yes**.
3. It has no name yet. Name it `{{ns}}-main-rt` by selecting the pencil icon in the **Name** column.
4. Select it and open the **Routes** tab.

There's one route:

- `10.0.0.0/16` → `local`

<figure class="screenshot">
  <img
    src="/images/labs/02-03/main-routes.png"
    alt="The Routes tab of the main route table showing only the local route."
  />
</figure>

The `local` route covers your whole VPC range, `10.0.0.0/16`. If traffic is headed for an address in that range, the VPC router delivers it inside the VPC, and it never leaves. That's how every subnet in your VPC can reach every other one. AWS adds this route to every route table, and you can't remove it.

## Step 2: Give your subnet its own route table

You could add routes to the main route table, but there's a good reason not to. If the main route table had a route to the internet, every new subnet you created would get it too.

So instead, leave the main route table with just the `local` route, and create your own route tables for subnets that need additional routing. 

1. Choose **Create route table**.
2. **Name:** `{{ns}}-public-rt`
3. **VPC:** `{{ns}}-vpc`
4. Choose **Create route table**.
5. Open the **Subnet associations** tab and choose **Edit subnet associations**.
6. Tick `{{ns}}-public-a` and choose **Save associations**.

<figure class="screenshot">
  <img
    src="/images/labs/02-03/associate-subnet.png"
    alt="The Edit subnet associations page with public-a ticked."
  />
</figure>

Open the **Routes** tab of your new route table. It has the same single `local` route. You'll add to it later.

## Step 3: Create an internet gateway

An **internet gateway** is the connection between your VPC and the internet. It's the AWS version of your home router's internet link from Lab 1.5's map.

1. Choose **Internet gateways** in the left menu, then **Create internet gateway**.
2. **Name tag:** `{{ns}}-igw`
3. Choose **Create internet gateway**.

Its **State** is **Detached**. It exists, but it isn't connected to anything.

4. Choose **Actions**, then **Attach to VPC**.
5. Choose `{{ns}}-vpc`, then **Attach internet gateway**.

The state changes to **Attached**.

<figure class="screenshot">
  <img
    src="/images/labs/02-03/igw-attached.png"
    alt="The internet gateway with its state showing Attached."
  />
</figure>

## Is your subnet public now?

<div class="callout break"><b>Think about it first.</b> Your VPC has an internet gateway attached. Look at <code>{{ns}}-public-rt</code> again. If you put a server in <code>public-a</code>, could anyone on the internet reach it?</div>

No. Your VPC has a door, but no route leads to it.

<div class="diagram">
  <img
    src="/images/labs/02-03/arch-door-no-path.svg"
    alt="Your VPC with an internet gateway on its edge and the public-a subnet inside. The subnet's route table has 10.0.0.0/16 to local, and 0.0.0.0/0 to nothing."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">a door, but no route leads to it</div>
</div>

Traffic only goes to the internet gateway if a route sends it there. Right now, the only route is `local`. In Phase 3, you'll put a real server in this subnet and see exactly what that means.

## Summary

- Every subnet uses a route table. If you don't choose one, it uses the main route table.
- `local` delivers traffic inside the VPC, and it's in every route table.
- `public-a` now uses `{{ns}}-public-rt`, and the main route table stays closed.
- Your VPC has an internet gateway attached, but nothing routes to it yet.

That's the network built: a VPC, a subnet, a route table and an internet gateway. All of them are free, so keep everything for Phase 3.
