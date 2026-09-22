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
    q: "You type <code>inthelab.ie</code> into a browser. What does DNS do?"
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

<div class="diagram">
  <img
    src="/images/labs/00-02/home-network.svg"
    alt="A home network showing a router connected to a laptop, phone, printer and television, each with its own private IP address."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">every device gets an address so the network knows where to send data</div>
</div>

On a typical home network, a service called **DHCP** gives devices their network settings automatically when they join. You usually do not type an IP address in yourself.

<div class="callout why"><b>Keep this mental model:</b> the network is the place devices can communicate; the IP address tells the network where to send the data.</div>

## Private and public IP addresses

A **private IP address** is used inside a private network. A **public IP address** is used to communicate across the public internet.

That is why two different homes can both use `192.168.1.10` without a conflict: the address only has meaning inside each private network.

<div class="diagram">
  <img
    src="/images/labs/00-02/private-public-ip.svg"
    alt="Two separate homes using the same private address, each with a different public address, both reaching one public server."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the same private address in two homes, and that causes no conflict</div>
</div>

The three IPv4 ranges reserved for private networks are:

- `10.0.0.0/8`
- `172.16.0.0/12`
- `192.168.0.0/16`

Home networks often use `192.168.x.x`. In AWS, you will see `10.x.x.x` a lot.

## An IP finds the machine. A port finds the service.

A server can run several services at the same time. It might serve a website, accept SSH connections, and run a database.

When traffic reaches the server, it needs to know **which service the traffic is for**. That's what the port tells it.

- **Port 22** → SSH
- **Port 80** → HTTP
- **Port 443** → HTTPS
- **Port 3306** → MySQL

Think of the **IP address as the street address** and the **port as the door**. The IP gets you to the right machine; the port gets you to the right service.

<div class="diagram">
  <img
    src="/images/labs/00-02/ports.svg"
    alt="One machine with four ports, SSH, HTTP and HTTPS open and MySQL closed to the internet."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the IP finds the machine · the port finds the service</div>
</div>

When you put the IP address and port together, it looks like this: `203.0.113.10:443`

- machine IP → `203.0.113.10`
- port → `443`

You will use IP addresses and ports when configuring **firewalls and security groups** to control what traffic is allowed through.

## Protocols are the rules

An IP address gets data to the right machine and a port gets it to the right service. Computers also need to agree on **how** to talk once they are connected. Those agreed rules are called **protocols**.

A single web request uses several at once. For the labs ahead, this simplified picture is enough:

- **HTTP / HTTPS** → the web conversation
- **TCP** → reliable delivery
- **IP** → addressing

<div class="diagram">
  <img
    src="/images/labs/00-02/protocol-stack.svg"
    alt="A web request wrapped by HTTP, then TCP, then IP, travelling from a browser to a server."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">one request, wrapped by each protocol in turn</div>
</div>

## TCP and UDP

Two transport protocols you will hear about often are **TCP** and **UDP**. They both carry data, the key difference is what happens when a piece goes missing.

**TCP** sends missing data again and keeps everything in order. It is used by web pages and downloads, where one missing piece ruins the result.

**UDP** does not send missing data again, it just moves on. It is used for live video call, where a lost moment is better skipped than replayed late.

<div class="diagram">
  <img
    src="/images/labs/00-02/tcp-vs-udp.svg"
    alt="Four numbered messages sent over TCP and over UDP, with one lost in each case."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">same loss, two different reactions</div>
</div>

Neither is "better" - they solve different problems.

## DNS turns names into addresses

DNS helps turn that domain names into a destination your computer can use. Humans remember `inthelab.ie` more easily than an IP address.

<div class="diagram">
  <img
    src="/images/labs/00-02/dns-lookup.svg"
    alt="A browser asking DNS where inthelab.ie is, getting an address back, then connecting to the server directly."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">DNS hands over the address, then your browser does the rest</div>
</div>

<div class="callout why"><b>The sentence to remember:</b> DNS does not send you the website. It helps your computer find where the website lives.</div>

## Put the whole journey together

When you type `https://inthelab.ie`, several things happen in sequence:

<div class="diagram">
  <img
    src="/images/labs/00-02/request-journey.svg"
    alt="The five stops of a web request, from typing a name to the server sending the page back."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">each stop can fail on its own, which is why you check them in order</div>
</div>

1. Your browser sees the name `inthelab.ie`.
2. DNS helps it find the destination IP address.
3. Your computer connects to that machine.
4. HTTPS normally reaches the service on port `443`.
5. Protocols such as TCP and IP carry the conversation.
6. The server sends the response back.

Every one of those steps can fail separately.