---
phase: 3
order: 5
title: A second firewall
type: lab
time: ~25 min
cost: ~$0.02 an hour while running
buildsOn: Lab 3.4
summary: Break your website with a network ACL, and see what it means for a firewall to be stateless.
draft: false
questions:
  - kind: recall
    q: "Where does a <b>network ACL</b> apply?"
    options:
      - "To one server"
      - "To the whole VPC"
      - "At the edge of a subnet, to every server in it"
      - "To your laptop"
    correct: 2
    hint: "What did you associate it with?"
    explain: "A network ACL is attached to a subnet, so it checks all traffic going in or out of that subnet. A security group is attached to individual servers."

  - kind: cause
    q: "Your network ACL allows inbound port 80, but the page still doesn't load. Why?"
    options:
      - "Network ACLs don't support port 80"
      - "The reply goes out to your browser's temporary port, and no outbound rule allows it"
      - "The security group overrides the network ACL"
      - "The rule number is too low"
    correct: 1
    hint: "Network ACLs don't remember connections."
    explain: "Network ACLs are stateless: they check every packet on its own, in each direction. The request gets in, but the reply goes out to a temporary high port on your laptop, and with no outbound rule allowing it, it's blocked."

  - kind: predict
    q: "The security group allows port 80, but the network ACL blocks all inbound traffic. Does the page load?"
    options:
      - "Yes, the security group is closer to the server"
      - "Yes, the more permissive rule wins"
      - "Only for the first request"
      - "No, traffic has to get through both firewalls"
    correct: 3
    hint: "Follow the request from the internet to the server. What does it meet first?"
    explain: "Traffic crosses the network ACL at the subnet edge before it ever reaches the security group. Both have to allow it. If either one blocks it, the page doesn't load."
---

**What you'll do:** Put a second firewall on your subnet, break your website with it, and fix it in a way that shows the difference between stateful and stateless.

---

## Two firewalls

Your VPC has two kinds of firewall:

- A **security group** wraps one server. You've been using it since Lab 3.3.
- A **network ACL** (access control list) sits at the edge of a subnet, and checks traffic for every server in it.

Your VPC came with a default network ACL in Lab 2.1. It allows everything in and out, which is why you haven't noticed it.

The two differ in how they treat replies:

- **Security groups are stateful.** They remember a connection they allowed in, and let its replies out.
- **Network ACLs are stateless.** They check every packet on its own, in each direction, and remember nothing.

Network ACLs also have **deny** rules and rule numbers. They check rules from the lowest number up, and stop at the first match.

## Step 1: Create a network ACL

1. In the VPC console, choose **Network ACLs** in the left menu, then **Create network ACL**.
2. **Name:** `{{ns}}-public-nacl`
3. **VPC:** `{{ns}}-vpc`
4. Choose **Create network ACL**.

Select it and look at its **Inbound rules** and **Outbound rules**. Each has one rule, numbered `*`, that denies everything. A new network ACL blocks all traffic until you add rules.

<div class="callout shot">screenshot: the new network ACL's inbound rules, showing only the deny-all rule<br>save as <code>/images/labs/03-05/nacl-deny-all.png</code></div>
<!--
<figure class="screenshot">
  <img
    src="/images/labs/03-05/nacl-deny-all.png"
    alt="The new network ACL's inbound rules, showing only the deny-all rule."
  />
</figure>
-->

## Step 2: Put it on your subnet

1. Open the **Subnet associations** tab and choose **Edit subnet associations**.
2. Tick `{{ns}}-public-a` and choose **Save changes**.

A subnet has exactly one network ACL, so this replaces the default one.

Reload your website. It spins and gives up. If you were connected over SSH, that session freezes too.

## Step 3: Allow web traffic in

1. Select `{{ns}}-public-nacl`, open the **Inbound rules** tab, and choose **Edit inbound rules**.
2. Choose **Add new rule**.
3. **Rule number:** `100`
4. **Type:** **HTTP (80)**
5. **Source:** `0.0.0.0/0`
6. **Allow/Deny:** **Allow**
7. Choose **Save changes**.

Reload your website. It still spins.

<div class="callout break"><b>Think about it first.</b> The request is allowed in. What about the page the server sends back?</div>

## The reply has nowhere to go

When your browser connects to port 80, your laptop picks a temporary port for the conversation, something like `52814`. The server sends its reply to that port.

The reply is outbound traffic from the subnet, and the network ACL has no outbound rule allowing it. Because the network ACL is stateless, it doesn't know this packet is a reply to a request it just let in.

<div class="diagram">
  <img
    src="/images/labs/03-05/nacl-vs-sg.svg"
    alt="A request to port 80 passes the network ACL at the subnet edge and the security group around the server. The reply back to port 52814 passes the security group, which remembers the request, but is blocked by the network ACL, which has no outbound rule for it."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the request gets in, but the reply is blocked on the way out</div>
</div>

These temporary ports are called **ephemeral ports**. Different operating systems pick them from different ranges, so network ACLs usually allow `1024` to `65535`.

## Step 4: Allow replies out

1. Open the **Outbound rules** tab and choose **Edit outbound rules**.
2. Choose **Add new rule**.
3. **Rule number:** `100`
4. **Type:** **Custom TCP**
5. **Port range:** `1024-65535`
6. **Destination:** `0.0.0.0/0`
7. **Allow/Deny:** **Allow**
8. Choose **Save changes**.

Reload the page. It loads. Check the time at the bottom of the page changes, to make sure it isn't an old copy.

<div class="callout shot">screenshot: the network ACL's outbound rules with the 1024-65535 allow rule<br>save as <code>/images/labs/03-05/nacl-outbound.png</code></div>
<!--
<figure class="screenshot">
  <img
    src="/images/labs/03-05/nacl-outbound.png"
    alt="The network ACL's outbound rules with the 1024-65535 allow rule."
  />
</figure>
-->

## Step 5: Put the default back

Most teams leave network ACLs open and do their real filtering with security groups, which are easier to get right. Network ACLs are useful for broad rules across a whole subnet, like blocking a range of addresses that's attacking you.

So you'll go back to the default:

1. In **Network ACLs**, select the one for `{{ns}}-vpc` where **Default** is **Yes**.
2. Open **Subnet associations**, choose **Edit subnet associations**, tick `{{ns}}-public-a`, and choose **Save changes**.
3. Select `{{ns}}-public-nacl`, choose **Actions**, then **Delete network ACLs**, and confirm.

Reload the page to check it still works. If SSH froze earlier, reconnect.

## Summary

- A network ACL guards a subnet; a security group guards a server. Traffic must get through both.
- Network ACLs are stateless, so replies need their own outbound rule.
- Replies go to ephemeral ports, which is why outbound rules allow `1024-65535`.
- Your subnet is back on the default network ACL, which allows everything.

Keep the server for the next lab. If you're taking a break, stop it.
