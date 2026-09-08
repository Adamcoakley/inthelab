---
phase: 0
order: 2
title: How computers talk to each other
type: concept
time: ~20 min
cost: Free
summary: Networks, IP addresses, ports, protocols and DNS — the pieces behind a web request.
draft: false
questions:
  - kind: recall
    q: "Which of these is a <b>private</b> IP address?"
    options:
      - "54.239.28.85"
      - "10.0.2.15"
      - "8.8.8.8"
      - "142.250.187.206"
    correct: 1
    hint: "One of the private ranges starts with 10."
    explain: "10.0.2.15 is inside the 10.0.0.0/8 private range. Private addresses are used inside private networks and are not routed directly across the public internet."

  - kind: cause
    q: "You can reach a server, but connections to port 80 fail. What should you check next?"
    options:
      - "Whether the IP address exists"
      - "Whether anything is listening on port 80, and whether traffic to that port is allowed"
      - "Whether DNS knows the server's name"
      - "Whether the server has enough disk space"
    correct: 1
    hint: "The IP got you to the machine. What does the port select?"
    explain: "The IP identifies the machine; the port identifies the service. If port 80 is not accepting traffic, there may be no web server listening there or a firewall may be blocking it."

  - kind: predict
    q: "You type <code>example.com</code> into a browser. What does DNS do?"
    options:
      - "It sends you the web page"
      - "It helps your computer find the IP address to connect to"
      - "It encrypts the connection"
      - "It opens port 443 on the server"
    correct: 1
    hint: "Think of DNS as a directory."
    explain: "DNS looks up information about a name, commonly the IP address your computer needs. Your browser then makes the connection itself. DNS does not carry the web page."
---

**What you'll learn:** What a network is, why devices need IP addresses, what ports and protocols do, and what happens when you load a website.

---

## Start with the network

A **network** is a group of devices that can communicate with each other. Your home Wi-Fi is one.

Your laptop, phone, TV and printer may all connect through the same router. Each device gets an **IP address** so the network knows where to send data.

<figure>
  <img src="/images/labs/00-02/home-network.svg" alt="A home network showing a router connected to a laptop, phone, printer and television, each with its own private IP address">
  <figcaption>A network connects devices; an IP address identifies where data should go.</figcaption>
</figure>

On a typical home network, a service called **DHCP** gives devices their network settings automatically when they join. You usually do not type an IP address in yourself.

<div class="callout why"><b>Keep this mental model:</b> the network is the place devices can communicate; the IP address tells the network where to send the data.</div>

An IPv4 address looks like `192.168.1.10`. Part of it describes the network and part identifies a destination inside it. **CIDR** tells us exactly where that split is — that is the next lab.

## Private and public IP addresses

A **private IP address** is used inside a private network. A **public IP address** is used to communicate across the public internet.

That is why two different homes can both use `192.168.1.10` without a conflict: the address only has meaning inside each private network.

<figure>
  <img src="/images/labs/00-02/private-public-ip.svg" alt="A private home network connected through a router to the public internet and a public server">
  <figcaption>Private addresses stay inside their network; public addresses are used across the internet.</figcaption>
</figure>

The three IPv4 ranges reserved for private networks are:

- `10.0.0.0/8`
- `172.16.0.0/12`
- `192.168.0.0/16`

Home networks often use `192.168.x.x`. In AWS, you will see `10.x.x.x` a lot.

<div class="callout why"><b>Don't worry about NAT yet.</b> For now, just notice the boundary between private addresses and the public internet. You will build that boundary yourself later.</div>

## An IP finds the machine. A port finds the service.

One machine can run several services at once.

The **IP address** gets traffic to the machine. The **port** identifies which service should receive it.

Think of the IP as the street address and the port as the door.

<figure>
  <img src="/images/labs/00-02/ports.svg" alt="A server with separate ports for SSH, HTTP, HTTPS and MySQL">
  <figcaption>One machine can expose several services, each on its own port.</figcaption>
</figure>

Written together, `203.0.113.10:443` means:

- machine → `203.0.113.10`
- service → port `443`

You will use this constantly when configuring firewalls and Security Groups.

## Protocols are the rules

Computers also need to agree on **how** they communicate. Those agreed rules are called **protocols**.

HTTP, TCP, DNS, SSH and IP are all protocols. They solve different parts of the same conversation.

<figure>
  <img src="/images/labs/00-02/protocol-stack.svg" alt="A browser sending a web request through HTTP or HTTPS, TCP and IP to a server">
  <figcaption>HTTP/HTTPS, TCP and IP work together; each solves a different part of the request.</figcaption>
</figure>

For the labs ahead, this simplified picture is enough:

- **HTTP / HTTPS** → the web conversation
- **TCP** → reliable delivery
- **IP** → addressing

<div class="callout why"><b>You do not need to memorise a networking model here.</b> The useful idea is that an IP address, a port and a protocol are different pieces of the same connection.</div>

## TCP and UDP

Two transport protocols you will hear about often are **TCP** and **UDP**.

**TCP** keeps track of the conversation. It keeps data in order and can resend missing data. Web traffic, SSH and database connections normally use TCP.

**UDP** is simpler. It sends individual messages without those delivery guarantees. DNS commonly uses UDP for ordinary queries, although it can use TCP too.

Neither is "better" — they solve different problems.

## DNS turns names into addresses

Humans remember `example.com` more easily than an IP address.

**DNS — the Domain Name System — helps turn that name into a destination your computer can use.**

<div class="callout why"><b>The sentence to remember:</b> DNS does not send you the website. It helps your computer find where the website lives.</div>

There is much more to DNS — records, caching, resolvers and authoritative servers — but you do not need all of that yet. You will meet it again when you use **Route 53**.

## Put the whole journey together

When you type `https://example.com`, several things happen in sequence:

<figure>
  <img src="/images/labs/00-02/request-journey.svg" alt="A web request journey showing a browser asking DNS for an IP address, connecting across the internet to port 443 on a server, and receiving a response">
  <figcaption>Name → DNS → IP → port → server → response.</figcaption>
</figure>

1. Your browser sees the name `example.com`.
2. DNS helps it find the destination IP address.
3. Your computer connects to that machine.
4. HTTPS normally reaches the service on port `443`.
5. Protocols such as TCP and IP carry the conversation.
6. The server sends the response back.

Every one of those steps can fail separately. Good network troubleshooting starts with one question:

**Which part of the journey broke?**

And there is one big question still unanswered: an IP address contains a network part and a destination part — but **how do we know exactly where one ends and the other begins?**

That is what **subnets and CIDR** solve.
