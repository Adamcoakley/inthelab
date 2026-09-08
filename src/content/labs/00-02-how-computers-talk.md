---
phase: 0
order: 2
title: How computers talk to each other
type: lab
time: ~25 min
cost: Free
summary: Networks, addresses, ports, protocols and DNS. What actually happens when you load a website.
draft: false
questions:

* kind: recall
  q: "Which of these is a <b>private</b> IP address?"
  options:

  * "54.239.28.85"
  * "10.0.2.15"
  * "8.8.8.8"
  * "142.250.187.206"
    correct: 1
    hint: "Three ranges are reserved for private networks. One of them starts with 10."
    explain: "10.0.2.15 sits inside the 10.0.0.0/8 private range. Private addresses are used inside networks and are not routed directly across the public internet."

* kind: cause
  q: "You can reach a server's IP address, but connections to port 80 fail. What should you check next?"
  options:

  * "Whether the IP address exists"
  * "Whether anything is listening on port 80, and whether traffic to that port is allowed"
  * "Whether DNS knows the server's name"
  * "Whether the server has enough disk space"
    correct: 1
    hint: "The IP got you to the machine. What does the port number select?"
    explain: "The IP address identifies the destination machine, but the port selects the service on that machine. If port 80 is not accepting traffic, there may be no web server listening there or a firewall may be blocking it. You will troubleshoot this exact distinction repeatedly in AWS."

* kind: predict
  q: "You type <code>example.com</code> into a browser. What does DNS actually do?"
  options:

  * "It sends you the web page"
  * "It tells your computer which IP address to connect to"
  * "It encrypts the connection"
  * "It opens port 443 on the server"
    correct: 1
    hint: "Think of DNS as a directory rather than a delivery service."
    explain: "DNS translates names into information your computer can use to find a destination, commonly an IP address. Your browser then makes its own connection to that destination. DNS does not carry the web page itself."

---

**What you'll learn:** What a network actually is, how devices get IP addresses, the difference between private and public addresses, what ports and protocols do, and how DNS turns a name into somewhere your computer can connect to.

---

## Start with the network

Before talking about IP addresses, we need somewhere for those addresses to exist.

A **network** is simply a group of devices that can communicate with each other.

Your home Wi-Fi is a network.

Your laptop, phone, television, games console and printer may all be connected to the same router. Once connected, they need a way to identify one another.

<div class="diagram">
<svg viewBox="0 0 620 320">
<defs>
  <filter id="n1" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="2.2" result="b"/>
    <feMerge>
      <feMergeNode in="b"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
  <marker id="n1arrow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
    <path d="M0 1 L8 4.5 L0 8 Z" fill="#3D5170"/>
  </marker>
</defs>

<text x="310" y="24" fill="#5B7290" font-family="JetBrains Mono" font-size="10.5" text-anchor="middle">
one small network
</text>

<g filter="url(#n1)">
  <rect x="248" y="118" width="124" height="64" rx="12" fill="#0C1220" stroke="#F5A524" stroke-width="1.8"/>
</g>
<text x="310" y="145" fill="#F5A524" font-family="JetBrains Mono" font-size="12" text-anchor="middle">router</text>
<text x="310" y="163" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">connects the network</text>

<rect x="34" y="54" width="134" height="58" rx="10" fill="#0C1220" stroke="#22C7B8" stroke-width="1.5"/>
<text x="101" y="77" fill="#22C7B8" font-family="JetBrains Mono" font-size="11" text-anchor="middle">laptop</text>
<text x="101" y="96" fill="#8FA0BD" font-family="JetBrains Mono" font-size="10" text-anchor="middle">192.168.1.10</text>

<rect x="452" y="54" width="134" height="58" rx="10" fill="#0C1220" stroke="#8B7BF0" stroke-width="1.5"/>
<text x="519" y="77" fill="#8B7BF0" font-family="JetBrains Mono" font-size="11" text-anchor="middle">phone</text>
<text x="519" y="96" fill="#8FA0BD" font-family="JetBrains Mono" font-size="10" text-anchor="middle">192.168.1.11</text>

<rect x="34" y="222" width="134" height="58" rx="10" fill="#0C1220" stroke="#34D399" stroke-width="1.5"/>
<text x="101" y="245" fill="#34D399" font-family="JetBrains Mono" font-size="11" text-anchor="middle">printer</text>
<text x="101" y="264" fill="#8FA0BD" font-family="JetBrains Mono" font-size="10" text-anchor="middle">192.168.1.20</text>

<rect x="452" y="222" width="134" height="58" rx="10" fill="#0C1220" stroke="#F26D9C" stroke-width="1.5"/>
<text x="519" y="245" fill="#F26D9C" font-family="JetBrains Mono" font-size="11" text-anchor="middle">television</text>
<text x="519" y="264" fill="#8FA0BD" font-family="JetBrains Mono" font-size="10" text-anchor="middle">192.168.1.30</text>

<path d="M168 94 L243 131" stroke="#3D5170" stroke-width="1.5" marker-end="url(#n1arrow)"/>
<path d="M452 94 L377 131" stroke="#3D5170" stroke-width="1.5" marker-end="url(#n1arrow)"/>
<path d="M168 238 L243 172" stroke="#3D5170" stroke-width="1.5" marker-end="url(#n1arrow)"/>
<path d="M452 238 L377 172" stroke="#3D5170" stroke-width="1.5" marker-end="url(#n1arrow)"/>

<text x="310" y="307" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">
each connection needs its own address
</text>
</svg>
<div class="dcap">devices connected together form a network</div>
</div>

The router is doing several jobs, but one of the most important is helping devices communicate with the network and with networks beyond it.

For that to work, each device needs an address.

## An IP address tells the network where something is

An **IP address** is an address assigned to a device's connection to a network.

Technically, an IP address belongs to a **network interface** rather than to the physical device itself. A laptop connected through Wi-Fi and Ethernet at the same time can therefore have more than one IP address.

For now, the important idea is simpler:

> **The IP address tells the network where to send the data.**

An IPv4 address contains four numbers from 0 to 255:

```text
192.168.1.10
```

You will see addresses like this constantly in AWS.

<div class="callout why"><b>Why is it called IPv4?</b> IP stands for <b>Internet Protocol</b>. IPv4 is the version of IP that uses addresses such as <code>10.0.1.5</code>. There is also IPv6, which uses much larger addresses. We will focus mainly on IPv4 while learning AWS networking.</div>

At first glance, the address looks like four unrelated numbers.

It is not.

Part of the address identifies the **network**, and another part identifies a particular connection inside that network.

Imagine a simple home network where all the addresses begin with:

```text
192.168.1
```

and the devices use different final numbers:

```text
192.168.1.10
192.168.1.11
192.168.1.20
```

They clearly belong together.

<div class="diagram">
<svg viewBox="0 0 620 210">
<defs>
  <filter id="ip1" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="2.2" result="b"/>
    <feMerge>
      <feMergeNode in="b"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
</defs>

<text x="310" y="28" fill="#5B7290" font-family="JetBrains Mono" font-size="10.5" text-anchor="middle">
a simple example
</text>

<g filter="url(#ip1)">
  <rect x="92" y="52" width="390" height="58" rx="10" fill="#0C1220" stroke="#22C7B8" stroke-width="1.7"/>
  <rect x="482" y="52" width="74" height="58" rx="10" fill="#0C1220" stroke="#F5A524" stroke-width="1.7"/>
</g>

<text x="287" y="88" fill="#22C7B8" font-family="JetBrains Mono" font-size="23" text-anchor="middle">
192.168.1
</text>
<text x="519" y="88" fill="#F5A524" font-family="JetBrains Mono" font-size="23" text-anchor="middle">
10
</text>

<path d="M287 122 L287 142" stroke="#22C7B8" stroke-width="1.4"/>
<text x="287" y="162" fill="#22C7B8" font-family="JetBrains Mono" font-size="10.5" text-anchor="middle">
the shared network part in this example
</text>

<path d="M519 122 L519 142" stroke="#F5A524" stroke-width="1.4"/>
<text x="519" y="162" fill="#F5A524" font-family="JetBrains Mono" font-size="10.5" text-anchor="middle">
this device
</text>

<text x="310" y="194" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">
CIDR tells us exactly where that split is — that is the next lab
</text>
</svg>
<div class="dcap">an IP address contains information about the network and the destination inside it</div>
</div>

That split is not always simply "the first three numbers versus the last one". The thing that tells us exactly where the network part ends is called **CIDR**.

That is what you will learn in the next lab.

## Where did your IP address come from?

You usually do not type an IP address into your phone every time you join Wi-Fi.

Instead, your device asks the network for one.

On a typical home network, the router runs a service called **DHCP**.

When your laptop joins the Wi-Fi, the conversation is roughly:

```text
Laptop:  "I've joined. Can I have network settings?"

Router:  "Yes. Use 192.168.1.10."
```

The router also tells the laptop other useful information, including where to send traffic that needs to leave the local network and which DNS server it can use.

<div class="diagram">
<svg viewBox="0 0 620 235">
<defs>
  <marker id="dhcpArrow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
    <path d="M0 1 L8 4.5 L0 8 Z" fill="#3D5170"/>
  </marker>
</defs>

<rect x="46" y="72" width="170" height="82" rx="11" fill="#0C1220" stroke="#22C7B8" stroke-width="1.6"/>
<text x="131" y="102" fill="#22C7B8" font-family="JetBrains Mono" font-size="12" text-anchor="middle">new laptop</text>
<text x="131" y="124" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">no network settings yet</text>

<rect x="404" y="72" width="170" height="82" rx="11" fill="#0C1220" stroke="#F5A524" stroke-width="1.6"/>
<text x="489" y="102" fill="#F5A524" font-family="JetBrains Mono" font-size="12" text-anchor="middle">router / DHCP</text>
<text x="489" y="124" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">hands out settings</text>

<path d="M216 94 L397 94" stroke="#3D5170" stroke-width="1.5" marker-end="url(#dhcpArrow)"/>
<text x="307" y="84" fill="#8FA0BD" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">
can I have an address?
</text>

<path d="M404 136 L223 136" stroke="#3D5170" stroke-width="1.5" marker-end="url(#dhcpArrow)"/>
<text x="313" y="158" fill="#8FA0BD" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">
use 192.168.1.10
</text>

<text x="310" y="203" fill="#5B7290" font-family="JetBrains Mono" font-size="10" text-anchor="middle">
the address is normally leased automatically
</text>
</svg>
<div class="dcap">devices usually receive their network settings automatically</div>
</div>

DHCP is another example of something you will see repeatedly in networking: computers following an agreed set of rules to communicate.

We will give that idea a name shortly.

## Private and public addresses

The address your router gives your laptop is normally a **private IP address**.

Private addresses are designed for use inside private networks.

For example:

```text
Laptop   192.168.1.10
Phone    192.168.1.11
Printer  192.168.1.20
```

Another house can use exactly the same addresses.

So can an office.

So can an AWS network.

There is no conflict because those addresses only have meaning inside their own private networks.

Think of apartment numbers.

There can be thousands of apartments called:

```text
Apartment 10
```

because "10" only makes sense once you know which building you mean.

Private IP addresses work in a similar way.

A **public IP address**, on the other hand, is used for communication across the public internet and must be globally routable.

Your home router might therefore have:

```text
Inside your home network:
192.168.1.1

Facing the internet:
a public IP address
```

Your laptop can stay private while the router handles communication with the outside world.

You will build the AWS version of this idea later.

### The private IPv4 ranges

IPv4 defines three ranges specifically for private networks:

<div class="diagram">
<svg viewBox="0 0 620 200">
<defs>
  <filter id="ranges" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="2" result="b"/>
    <feMerge>
      <feMergeNode in="b"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
</defs>

<g filter="url(#ranges)">
  <rect x="30" y="22" width="560" height="44" rx="9" fill="#0C1220" stroke="#F5A524" stroke-width="1.6"/>
</g>
<text x="52" y="50" fill="#F5A524" font-family="JetBrains Mono" font-size="14">10.0.0.0/8</text>
<text x="230" y="50" fill="#8FA0BD" font-family="JetBrains Mono" font-size="10.5">10.0.0.0 → 10.255.255.255</text>

<g filter="url(#ranges)">
  <rect x="30" y="78" width="560" height="44" rx="9" fill="#0C1220" stroke="#8B7BF0" stroke-width="1.6"/>
</g>
<text x="52" y="106" fill="#8B7BF0" font-family="JetBrains Mono" font-size="14">172.16.0.0/12</text>
<text x="230" y="106" fill="#8FA0BD" font-family="JetBrains Mono" font-size="10.5">172.16.0.0 → 172.31.255.255</text>

<g filter="url(#ranges)">
  <rect x="30" y="134" width="560" height="44" rx="9" fill="#0C1220" stroke="#22C7B8" stroke-width="1.6"/>
</g>
<text x="52" y="162" fill="#22C7B8" font-family="JetBrains Mono" font-size="14">192.168.0.0/16</text>
<text x="230" y="162" fill="#8FA0BD" font-family="JetBrains Mono" font-size="10.5">192.168.0.0 → 192.168.255.255</text>
</svg>
<div class="dcap">the three IPv4 ranges reserved for private networks</div>
</div>

You do not need to memorise every address in those ranges.

For this course, recognising these three beginnings is enough:

```text
10.
172.16 — 172.31
192.168.
```

<div class="callout why"><b>One small accuracy note.</b> It is tempting to say "everything outside those three ranges is public", but IPv4 also contains other special-purpose and reserved addresses. What matters here is that these are the three ranges specifically reserved for ordinary private networks.</div>

In AWS, you will see addresses beginning with `10.` constantly.

## An IP finds the machine. A port finds the service.

Knowing the machine is not enough.

One computer can run many programs at the same time.

A server might be running:

* a website
* an SSH service for remote administration
* a database
* monitoring software

They all share the same machine.

So how does incoming traffic know which program it is meant for?

A **port**.

Think of the IP address as the street address of a building.

The port is the door.

<div class="diagram">
<svg viewBox="0 0 620 300">
<defs>
  <filter id="ports" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="2.2" result="b"/>
    <feMerge>
      <feMergeNode in="b"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
</defs>

<path d="M70 56 L100 36 L250 36 L220 56 Z" fill="#1B2738" stroke="#3D5170" stroke-width="1.5" stroke-linejoin="round"/>
<path d="M220 56 L250 36 L250 236 L220 256 Z" fill="#161F2D" stroke="#3D5170" stroke-width="1.5" stroke-linejoin="round"/>
<rect x="70" y="56" width="150" height="200" rx="4" fill="#141E2C" stroke="#3D5170" stroke-width="1.7"/>

<rect x="84" y="72" width="122" height="26" rx="3" fill="#0C1220" stroke="#2D3D52" stroke-width="1.2"/>
<rect x="84" y="106" width="122" height="26" rx="3" fill="#0C1220" stroke="#2D3D52" stroke-width="1.2"/>
<rect x="84" y="140" width="122" height="26" rx="3" fill="#0C1220" stroke="#2D3D52" stroke-width="1.2"/>
<rect x="84" y="174" width="122" height="26" rx="3" fill="#0C1220" stroke="#2D3D52" stroke-width="1.2"/>

<circle cx="94" cy="220" r="3.4" fill="#34D399" filter="url(#ports)"/>

<text x="145" y="280" fill="#8FA0BD" font-family="JetBrains Mono" font-size="11" text-anchor="middle">one machine</text> <text x="145" y="295" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">203.0.113.10</text>

<line x1="250" y1="72" x2="316" y2="62" stroke="#8B7BF0" stroke-width="1.2"/>
<rect x="322" y="44" width="250" height="36" rx="7" fill="#0C1220" stroke="#8B7BF0" stroke-width="1.5"/>
<text x="338" y="60" fill="#8B7BF0" font-family="JetBrains Mono" font-size="12">:22</text>
<text x="380" y="60" fill="#8FA0BD" font-family="JetBrains Mono" font-size="11">SSH</text>
<text x="338" y="73" fill="#5B7290" font-family="JetBrains Mono" font-size="9">remote administration</text>

<line x1="250" y1="112" x2="316" y2="108" stroke="#22C7B8" stroke-width="1.2"/>
<rect x="322" y="90" width="250" height="36" rx="7" fill="#0C1220" stroke="#22C7B8" stroke-width="1.5"/>
<text x="338" y="106" fill="#22C7B8" font-family="JetBrains Mono" font-size="12">:80</text>
<text x="380" y="106" fill="#8FA0BD" font-family="JetBrains Mono" font-size="11">HTTP</text>
<text x="338" y="119" fill="#5B7290" font-family="JetBrains Mono" font-size="9">web traffic</text>

<line x1="250" y1="152" x2="316" y2="154" stroke="#34D399" stroke-width="1.2"/>
<rect x="322" y="136" width="250" height="36" rx="7" fill="#0C1220" stroke="#34D399" stroke-width="1.5"/>
<text x="338" y="152" fill="#34D399" font-family="JetBrains Mono" font-size="12">:443</text>
<text x="392" y="152" fill="#8FA0BD" font-family="JetBrains Mono" font-size="11">HTTPS</text>
<text x="338" y="165" fill="#5B7290" font-family="JetBrains Mono" font-size="9">encrypted web traffic</text>

<line x1="250" y1="192" x2="316" y2="200" stroke="#F5A524" stroke-width="1.2"/>
<rect x="322" y="182" width="250" height="36" rx="7" fill="#0C1220" stroke="#F5A524" stroke-width="1.5"/>
<text x="338" y="198" fill="#F5A524" font-family="JetBrains Mono" font-size="12">:3306</text>
<text x="404" y="198" fill="#8FA0BD" font-family="JetBrains Mono" font-size="11">MySQL</text>
<text x="338" y="211" fill="#5B7290" font-family="JetBrains Mono" font-size="9">database traffic</text>

<text x="447" y="248" fill="#5B7290" font-family="JetBrains Mono" font-size="10" text-anchor="middle">
same machine, different services
</text>
</svg>
<div class="dcap">the IP finds the machine, the port identifies the service</div>
</div>

Written together, you might see:

```text
203.0.113.10:443
```

which means:

```text
203.0.113.10  → which machine?
443           → which service?
```

Those port numbers will become important when you build firewalls and Security Groups.

## Computers need rules for talking

We now know:

```text
IP address → where?
Port       → which service?
```

But the two computers still need to agree on **how** they will communicate.

That agreed set of rules is called a **protocol**.

Humans use protocols too.

If you answer a phone call with:

```text
Hello?
```

and the other person responds:

```text
Hi, is Adam there?
```

both people understand the structure of the conversation.

Computers need the same kind of agreement, except the rules have to be exact.

There are protocols for different jobs:

```text
HTTP   → requesting and sending web content
HTTPS  → web communication protected with encryption
SSH    → remotely controlling another machine
DNS    → looking up names
DHCP   → assigning network settings
TCP    → reliably carrying data between applications
UDP    → sending individual messages with less overhead
IP     → addressing and moving packets between networks
```

The important part is that these protocols work **together** rather than replacing one another.

## Protocols sit in layers

Imagine loading a web page.

Your browser understands HTTP.

But HTTP does not itself know how to move data across several networks.

Other protocols underneath it handle that job.

<div class="diagram">
<svg viewBox="0 0 620 360">
<defs>
  <filter id="layers" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="2" result="b"/>
    <feMerge>
      <feMergeNode in="b"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
</defs>

<text x="310" y="24" fill="#5B7290" font-family="JetBrains Mono" font-size="10.5" text-anchor="middle">
one web request, several layers of rules
</text>

<g filter="url(#layers)">
  <rect x="110" y="48" width="400" height="58" rx="10" fill="#0C1220" stroke="#34D399" stroke-width="1.7"/>
</g>
<text x="310" y="72" fill="#34D399" font-family="JetBrains Mono" font-size="12.5" text-anchor="middle">HTTP / HTTPS</text>
<text x="310" y="91" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">
what the browser and web server say to each other
</text>

<text x="310" y="124" fill="#3D5170" font-family="JetBrains Mono" font-size="16" text-anchor="middle">↓</text>

<g filter="url(#layers)">
  <rect x="110" y="138" width="400" height="58" rx="10" fill="#0C1220" stroke="#8B7BF0" stroke-width="1.7"/>
</g>
<text x="310" y="162" fill="#8B7BF0" font-family="JetBrains Mono" font-size="12.5" text-anchor="middle">TCP</text>
<text x="310" y="181" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">
keeps the conversation reliable and ordered
</text>

<text x="310" y="214" fill="#3D5170" font-family="JetBrains Mono" font-size="16" text-anchor="middle">↓</text>

<g filter="url(#layers)">
  <rect x="110" y="228" width="400" height="58" rx="10" fill="#0C1220" stroke="#F5A524" stroke-width="1.7"/>
</g>
<text x="310" y="252" fill="#F5A524" font-family="JetBrains Mono" font-size="12.5" text-anchor="middle">IP</text>
<text x="310" y="271" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">
puts source and destination addresses on the data
</text>

<text x="310" y="314" fill="#8FA0BD" font-family="JetBrains Mono" font-size="10.5" text-anchor="middle">
each layer solves a different problem
</text>
<text x="310" y="334" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">
you do not need to memorise the layers — understand their jobs
</text>
</svg>
<div class="dcap">protocols cooperate, with each layer handling a different part of the journey</div>
</div>

For the AWS labs ahead, a useful simplified picture is:

```text
HTTP/HTTPS
    ↓
TCP
    ↓
IP
```

You ask for a web page using HTTP or HTTPS.

TCP carries that conversation reliably.

IP gets the data to the right machine.

## TCP and UDP solve different problems

TCP is not the only way applications can send data.

Two transport protocols you will hear about constantly are:

```text
TCP
UDP
```

### TCP

**TCP** is designed for situations where the data needs to arrive reliably and in the correct order.

It establishes a conversation between the two sides and keeps track of what was received.

If part of the data goes missing, TCP can send it again.

That makes it useful for things such as:

```text
web traffic
SSH
database connections
```

### UDP

**UDP** is much simpler.

It sends individual messages without creating the same kind of reliable connection.

It does not promise that every message will arrive or that messages will arrive in order.

That means less overhead.

UDP is useful when an application either:

* values speed more than perfect delivery, or
* has its own way of dealing with lost data.

DNS commonly uses UDP for ordinary queries, although it can use TCP when needed.

<div class="diagram">
<svg viewBox="0 0 620 260">
<defs>
  <filter id="transport" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="2" result="b"/>
    <feMerge>
      <feMergeNode in="b"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
</defs>

<g filter="url(#transport)">
  <rect x="28" y="28" width="268" height="190" rx="12" fill="rgba(34,199,184,.05)" stroke="#22C7B8" stroke-width="1.6"/>
</g>
<text x="162" y="56" fill="#22C7B8" font-family="JetBrains Mono" font-size="14" text-anchor="middle">TCP</text>
<text x="162" y="77" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">reliable conversation</text>

<text x="54" y="110" fill="#8FA0BD" font-family="Inter" font-size="11">✓ establishes a connection</text> <text x="54" y="137" fill="#8FA0BD" font-family="Inter" font-size="11">✓ keeps data in order</text> <text x="54" y="164" fill="#8FA0BD" font-family="Inter" font-size="11">✓ retransmits missing data</text> <text x="54" y="195" fill="#22C7B8" font-family="Inter" font-size="11">web, SSH, databases</text>

<g filter="url(#transport)">
  <rect x="324" y="28" width="268" height="190" rx="12" fill="rgba(139,123,240,.05)" stroke="#8B7BF0" stroke-width="1.6"/>
</g>
<text x="458" y="56" fill="#8B7BF0" font-family="JetBrains Mono" font-size="14" text-anchor="middle">UDP</text>
<text x="458" y="77" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">independent messages</text>

<text x="350" y="110" fill="#8FA0BD" font-family="Inter" font-size="11">• no connection setup required</text> <text x="350" y="137" fill="#8FA0BD" font-family="Inter" font-size="11">• no delivery guarantee</text> <text x="350" y="164" fill="#8FA0BD" font-family="Inter" font-size="11">• less protocol overhead</text> <text x="350" y="195" fill="#8B7BF0" font-family="Inter" font-size="11">DNS, calls, games, streaming</text>

<text x="310" y="246" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">
neither is "better" — they solve different problems
</text>
</svg>
<div class="dcap">TCP prioritises reliable delivery; UDP keeps things simpler</div>
</div>

<div class="callout why"><b>You do not need to become a protocol expert here.</b> The important thing is recognising that an IP address, a port and a protocol are different pieces of the same connection. Later, when AWS asks you to allow <code>TCP port 443</code>, that sentence will actually mean something.</div>

## Humans prefer names

Imagine having to remember this every time you wanted to visit a website:

```text
93.184.216.34
```

instead of:

```text
example.com
```

Names are easier for humans.

Networks still need addresses.

**DNS — the Domain Name System — connects those two worlds.**

Its job is to answer questions about names.

A very common DNS question is effectively:

```text
What IP address should I use for example.com?
```

and the answer might be:

```text
93.184.216.34
```

Your browser can then connect to that address.

<div class="callout why"><b>The sentence to remember.</b> DNS does not send you the website. DNS helps your computer find where the website lives. Your browser makes the actual connection afterwards.</div>

## What actually happens during a DNS lookup?

Your computer normally sends the question to a **DNS resolver**.

A resolver is a service whose job is to find DNS answers for you.

Your internet provider may provide one, your router may point you toward one, or you might use a public resolver.

The simplified conversation looks like this:

<div class="diagram">
<svg viewBox="0 0 620 280">
<defs>
  <filter id="dns1" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="2" result="b"/>
    <feMerge>
      <feMergeNode in="b"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
  <marker id="dnsArrow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
    <path d="M0 1 L8 4.5 L0 8 Z" fill="#3D5170"/>
  </marker>
</defs>

<g filter="url(#dns1)">
  <rect x="32" y="82" width="160" height="78" rx="11" fill="#0C1220" stroke="#22C7B8" stroke-width="1.6"/>
</g>
<text x="112" y="110" fill="#22C7B8" font-family="JetBrains Mono" font-size="11.5" text-anchor="middle">your computer</text>
<text x="112" y="132" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">example.com</text>

<g filter="url(#dns1)">
  <rect x="230" y="82" width="160" height="78" rx="11" fill="#0C1220" stroke="#8B7BF0" stroke-width="1.6"/>
</g>
<text x="310" y="110" fill="#8B7BF0" font-family="JetBrains Mono" font-size="11.5" text-anchor="middle">DNS resolver</text>
<text x="310" y="132" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">finds the answer</text>

<g filter="url(#dns1)">
  <rect x="428" y="82" width="160" height="78" rx="11" fill="#0C1220" stroke="#F5A524" stroke-width="1.6"/>
</g>
<text x="508" y="110" fill="#F5A524" font-family="JetBrains Mono" font-size="11.5" text-anchor="middle">DNS system</text>
<text x="508" y="132" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">records for names</text>

<path d="M192 101 L223 101" stroke="#3D5170" stroke-width="1.5" marker-end="url(#dnsArrow)"/>
<text x="208" y="88" fill="#8FA0BD" font-family="JetBrains Mono" font-size="8.5" text-anchor="middle">ask</text>

<path d="M390 101 L421 101" stroke="#3D5170" stroke-width="1.5" marker-end="url(#dnsArrow)"/>

<path d="M428 143 L397 143" stroke="#3D5170" stroke-width="1.5" marker-end="url(#dnsArrow)"/>
<path d="M230 143 L199 143" stroke="#3D5170" stroke-width="1.5" marker-end="url(#dnsArrow)"/>

<text x="310" y="198" fill="#F5A524" font-family="JetBrains Mono" font-size="12" text-anchor="middle">
example.com → 93.184.216.34
</text>

<text x="310" y="229" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">
now the browser knows where to connect
</text>
</svg>
<div class="dcap">DNS turns a useful human name into information the network can use</div>
</div>

There is more to DNS than this.

DNS has different types of records, caching, multiple layers of servers and many other features.

You do not need those details yet.

Later, when you use **Route 53**, this basic mental model is what matters:

```text
name
  ↓
DNS
  ↓
destination
```

## Put the whole journey together

Now we can finally follow a web request from beginning to end.

Imagine typing:

```text
https://example.com
```

into your browser.

### 1. Your computer is already on a network

It has network settings such as an IP address, usually assigned automatically.

For example:

```text
192.168.1.10
```

### 2. The browser sees a name

You entered:

```text
example.com
```

but the network needs a destination.

### 3. DNS looks up the name

Your computer asks DNS where `example.com` lives.

DNS returns an address.

For example:

```text
93.184.216.34
```

### 4. The browser connects to the web service

Because you used HTTPS, the destination service is normally reached on port:

```text
443
```

So you now have:

```text
93.184.216.34:443
```

The IP identifies the destination.

The port identifies the web service.

### 5. Protocols handle the conversation

At a simplified level:

```text
HTTPS
  ↓
TCP
  ↓
IP
```

HTTPS defines the protected web conversation.

TCP provides reliable transport.

IP handles addressing and movement between networks.

### 6. The server receives the request

The operating system sees that the traffic is destined for port `443` and passes it to the service listening there.

The web server handles the request.

### 7. The response comes back

The server sends the page data back across the network.

Your browser receives it and displays the page.

<div class="diagram">
<svg viewBox="0 0 620 460">
<defs>
  <filter id="journey" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="2" result="b"/>
    <feMerge>
      <feMergeNode in="b"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
  <marker id="journeyArrow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
    <path d="M0 1 L8 4.5 L0 8 Z" fill="#3D5170"/>
  </marker>
</defs>

<g filter="url(#journey)">
  <rect x="190" y="20" width="240" height="50" rx="10" fill="#0C1220" stroke="#22C7B8" stroke-width="1.6"/>
</g>
<text x="310" y="41" fill="#22C7B8" font-family="JetBrains Mono" font-size="11.5" text-anchor="middle">1. you type example.com</text>
<text x="310" y="58" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">a human-friendly name</text>

<path d="M310 70 L310 94" stroke="#3D5170" stroke-width="1.5" marker-end="url(#journeyArrow)"/>

<g filter="url(#journey)">
  <rect x="190" y="100" width="240" height="50" rx="10" fill="#0C1220" stroke="#8B7BF0" stroke-width="1.6"/>
</g>
<text x="310" y="121" fill="#8B7BF0" font-family="JetBrains Mono" font-size="11.5" text-anchor="middle">2. DNS looks it up</text>
<text x="310" y="138" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">where does that name live?</text>

<path d="M310 150 L310 174" stroke="#3D5170" stroke-width="1.5" marker-end="url(#journeyArrow)"/>

<g filter="url(#journey)">
  <rect x="190" y="180" width="240" height="50" rx="10" fill="#0C1220" stroke="#F5A524" stroke-width="1.6"/>
</g>
<text x="310" y="201" fill="#F5A524" font-family="JetBrains Mono" font-size="11.5" text-anchor="middle">3. DNS returns an IP</text>
<text x="310" y="218" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">93.184.216.34</text>

<path d="M310 230 L310 254" stroke="#3D5170" stroke-width="1.5" marker-end="url(#journeyArrow)"/>

<g filter="url(#journey)">
  <rect x="160" y="260" width="300" height="56" rx="10" fill="#0C1220" stroke="#34D399" stroke-width="1.6"/>
</g>
<text x="310" y="282" fill="#34D399" font-family="JetBrains Mono" font-size="11.5" text-anchor="middle">4. connect to 93.184.216.34:443</text>
<text x="310" y="301" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">address finds machine · port finds service</text>

<path d="M310 316 L310 340" stroke="#3D5170" stroke-width="1.5" marker-end="url(#journeyArrow)"/>

<g filter="url(#journey)">
  <rect x="160" y="346" width="300" height="56" rx="10" fill="#0C1220" stroke="#F26D9C" stroke-width="1.6"/>
</g>
<text x="310" y="368" fill="#F26D9C" font-family="JetBrains Mono" font-size="11.5" text-anchor="middle">5. protocols carry the request</text>
<text x="310" y="387" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">HTTPS → TCP → IP</text>

<path d="M310 402 L310 422" stroke="#3D5170" stroke-width="1.5" marker-end="url(#journeyArrow)"/>

<text x="310" y="446" fill="#8FA0BD" font-family="JetBrains Mono" font-size="11" text-anchor="middle">
the server responds and the page appears
</text>
</svg>
<div class="dcap">name → address → port → protocols → response</div>
</div>

## Why this matters in AWS

Every part of that journey can fail independently.

A problem might be:

```text
the machine has the wrong IP
the destination is on another network
there is no route to that network
a firewall blocks the port
nothing is listening on the port
DNS returns the wrong destination
```

Those failures can look very similar from the outside.

The skill you are starting to build is asking:

```text
Which part of the journey broke?
```

That question is at the heart of network troubleshooting.

And from here, the next problem becomes obvious:

We know an IP contains a network part and a device part.

But **how does a computer know exactly where one ends and the other begins?**

That is what subnets and CIDR solve.
