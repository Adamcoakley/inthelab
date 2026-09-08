---
phase: 0
order: 1
title: What actually is "the cloud"?
type: concept
time: ~15 min
cost: Free
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

**What you'll learn:** What a server actually is, why renting one changes everything, and how AWS is physically laid out. Nothing to build here, but it is the mental model the rest of the course sits on.

---

## A server is just a computer

Strip away the word "cloud" for a moment. A server is a computer, the same as the one in front of you. It has a processor, memory, a disk, and a network connection. It is simply built to run continuously and be used by other machines rather than by a person sitting at it.

<div class="diagram">
<svg viewBox="0 0 620 280">
<defs><filter id="s1" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<path d="M70 52 L100 32 L250 32 L220 52 Z" fill="#1B2738" stroke="#3D5170" stroke-width="1.5" stroke-linejoin="round"/>
<path d="M220 52 L250 32 L250 232 L220 252 Z" fill="#161F2D" stroke="#3D5170" stroke-width="1.5" stroke-linejoin="round"/>
<rect x="70" y="52" width="150" height="200" rx="4" fill="#141E2C" stroke="#3D5170" stroke-width="1.7"/>
<rect x="84" y="68" width="122" height="26" rx="3" fill="#0C1220" stroke="#2D3D52" stroke-width="1.2"/>
<rect x="92" y="78" width="60" height="3" rx="1.5" fill="#3D5170"/>
<rect x="84" y="102" width="122" height="26" rx="3" fill="#0C1220" stroke="#2D3D52" stroke-width="1.2"/>
<rect x="92" y="112" width="60" height="3" rx="1.5" fill="#3D5170"/>
<rect x="84" y="136" width="122" height="26" rx="3" fill="#0C1220" stroke="#2D3D52" stroke-width="1.2"/>
<rect x="92" y="146" width="60" height="3" rx="1.5" fill="#3D5170"/>
<rect x="84" y="170" width="122" height="26" rx="3" fill="#0C1220" stroke="#2D3D52" stroke-width="1.2"/>
<rect x="92" y="180" width="60" height="3" rx="1.5" fill="#3D5170"/>
<circle cx="94" cy="216" r="3.4" fill="#34D399" filter="url(#s1)"/>
<circle cx="107" cy="216" r="3.4" fill="#3D5170"/>
<circle cx="120" cy="216" r="3.4" fill="#3D5170"/>
<text x="145" y="272" fill="#5B7290" font-family="JetBrains Mono" font-size="10.5" text-anchor="middle">one server</text>
<line x1="250" y1="70" x2="316" y2="60" stroke="#22C7B8" stroke-width="1.2"/>
<rect x="322" y="42" width="230" height="38" rx="7" fill="#0C1220" stroke="#22C7B8" stroke-width="1.5"/>
<text x="338" y="60" fill="#22C7B8" font-family="JetBrains Mono" font-size="12">CPU</text>
<text x="338" y="74" fill="#5B7290" font-family="JetBrains Mono" font-size="9">processing power</text>
<line x1="250" y1="110" x2="316" y2="106" stroke="#F5A524" stroke-width="1.2"/>
<rect x="322" y="88" width="230" height="38" rx="7" fill="#0C1220" stroke="#F5A524" stroke-width="1.5"/>
<text x="338" y="106" fill="#F5A524" font-family="JetBrains Mono" font-size="12">Memory</text>
<text x="338" y="120" fill="#5B7290" font-family="JetBrains Mono" font-size="9">RAM, cleared when it restarts</text>
<line x1="250" y1="150" x2="316" y2="152" stroke="#8B7BF0" stroke-width="1.2"/>
<rect x="322" y="134" width="230" height="38" rx="7" fill="#0C1220" stroke="#8B7BF0" stroke-width="1.5"/>
<text x="338" y="152" fill="#8B7BF0" font-family="JetBrains Mono" font-size="12">Disk</text>
<text x="338" y="166" fill="#5B7290" font-family="JetBrains Mono" font-size="9">storage, survives a restart</text>
<line x1="250" y1="190" x2="316" y2="198" stroke="#34D399" stroke-width="1.2"/>
<rect x="322" y="180" width="230" height="38" rx="7" fill="#0C1220" stroke="#34D399" stroke-width="1.5"/>
<text x="338" y="198" fill="#34D399" font-family="JetBrains Mono" font-size="12">Network</text>
<text x="338" y="212" fill="#5B7290" font-family="JetBrains Mono" font-size="9">connection to other machines</text>
</svg>
<div class="dcap">a server, and the four things it is made of</div>
</div>

Your application is not mysterious either. It is a **process**: a program the operating system is running, using some of that CPU and memory.

## Buying versus renting

If you own physical servers, you have to buy for your busiest moment. Black Friday, results day, the morning you get written about. So you buy for the peak, and most of the time most of it sits idle, already paid for.

<div class="diagram">
<svg viewBox="0 0 620 250">
<defs><filter id="s2" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<line x1="60" y1="200" x2="580" y2="200" stroke="#3D5170" stroke-width="1.4"/>
<line x1="60" y1="40" x2="60" y2="200" stroke="#3D5170" stroke-width="1.4"/>
<text x="46" y="46" fill="#5B7290" font-family="JetBrains Mono" font-size="10" text-anchor="end">load</text>
<text x="580" y="218" fill="#5B7290" font-family="JetBrains Mono" font-size="10" text-anchor="end">time</text>
<path d="M60 62 L60 170 C120 168 150 150 190 120 C230 90 250 66 290 62 L290 62 Z" fill="#F5A524" opacity=".09"/>
<path d="M290 62 C330 58 350 96 400 130 C450 164 500 172 580 174 L580 62 Z" fill="#F5A524" opacity=".09"/>
<path d="M60 170 C120 168 150 150 190 120 C230 90 250 66 290 62 C330 58 350 96 400 130 C450 164 500 172 580 174" fill="none" stroke="#22C7B8" stroke-width="2.4" filter="url(#s2)"/>
<text x="300" y="48" fill="#22C7B8" font-family="JetBrains Mono" font-size="10.5" text-anchor="middle">what you actually need</text>
<line x1="60" y1="62" x2="580" y2="62" stroke="#F5A524" stroke-width="2.4" stroke-dasharray="7 5"/>
<text x="72" y="80" fill="#F5A524" font-family="JetBrains Mono" font-size="10.5">what you bought, and pay for always</text>
<text x="150" y="130" fill="#F5A524" font-family="JetBrains Mono" font-size="10" opacity=".85">wasted</text>
<text x="470" y="130" fill="#F5A524" font-family="JetBrains Mono" font-size="10" opacity=".85">wasted</text>
</svg>
<div class="dcap">every shaded gap is capacity you paid for and did not use</div>
</div>

<div class="callout why"><b>This is the problem the cloud solves first.</b> Not "servers on the internet", but the mismatch between what you own and what you need right now. If you can add capacity in seconds and give it back when you are done, you stop paying for the gaps. That is <b>elasticity</b>, and you will build it yourself in Phase 5.</div>

## How one computer becomes many

If AWS had to hand you a whole physical machine every time you asked for a small server, none of this would work. **Virtualisation** is the answer: software divides one machine into slices, and each slice behaves like a complete, independent computer that cannot see the others.

<div class="diagram">
<svg viewBox="0 0 620 400">
<defs>
<filter id="s3" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<marker id="ah3" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0 1 L8 4.5 L0 8 Z" fill="#8B7BF0"/></marker>
</defs>
<text x="310" y="22" fill="#5B7290" font-family="JetBrains Mono" font-size="10.5" text-anchor="middle">three virtual machines, each behaves like its own computer</text>
<g opacity=".65">
<path d="M104 48 L115 38 L173 38 L162 48 Z" fill="#1B2738" stroke="#22C7B8" stroke-width="1.3" stroke-linejoin="round"/>
<path d="M162 48 L173 38 L173 126 L162 136 Z" fill="#161F2D" stroke="#22C7B8" stroke-width="1.3" stroke-linejoin="round"/>
<rect x="104" y="48" width="58" height="88" rx="3" fill="#141E2C" stroke="#22C7B8" stroke-width="1.4"/>
<rect x="112" y="58" width="42" height="12" rx="2" fill="#0C1220" stroke="#2D3D52"/>
<rect x="112" y="76" width="42" height="12" rx="2" fill="#0C1220" stroke="#2D3D52"/>
<rect x="112" y="94" width="42" height="12" rx="2" fill="#0C1220" stroke="#2D3D52"/>
<circle cx="116" cy="122" r="2.6" fill="#22C7B8"/>
</g>
<text x="133" y="152" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">someone else's</text>
<g filter="url(#s3)">
<path d="M281 48 L292 38 L350 38 L339 48 Z" fill="#1B2738" stroke="#F5A524" stroke-width="1.5" stroke-linejoin="round"/>
<path d="M339 48 L350 38 L350 126 L339 136 Z" fill="#161F2D" stroke="#F5A524" stroke-width="1.5" stroke-linejoin="round"/>
<rect x="281" y="48" width="58" height="88" rx="3" fill="#141E2C" stroke="#F5A524" stroke-width="1.6"/>
</g>
<rect x="289" y="58" width="42" height="12" rx="2" fill="#0C1220" stroke="#F5A524" stroke-width="1.1"/>
<rect x="289" y="76" width="42" height="12" rx="2" fill="#0C1220" stroke="#F5A524" stroke-width="1.1"/>
<rect x="289" y="94" width="42" height="12" rx="2" fill="#0C1220" stroke="#F5A524" stroke-width="1.1"/>
<circle cx="293" cy="122" r="2.6" fill="#F5A524"/>
<text x="310" y="152" fill="#F5A524" font-family="JetBrains Mono" font-size="10" text-anchor="middle">yours</text>
<g opacity=".65">
<path d="M458 48 L469 38 L527 38 L516 48 Z" fill="#1B2738" stroke="#22C7B8" stroke-width="1.3" stroke-linejoin="round"/>
<path d="M516 48 L527 38 L527 126 L516 136 Z" fill="#161F2D" stroke="#22C7B8" stroke-width="1.3" stroke-linejoin="round"/>
<rect x="458" y="48" width="58" height="88" rx="3" fill="#141E2C" stroke="#22C7B8" stroke-width="1.4"/>
<rect x="466" y="58" width="42" height="12" rx="2" fill="#0C1220" stroke="#2D3D52"/>
<rect x="466" y="76" width="42" height="12" rx="2" fill="#0C1220" stroke="#2D3D52"/>
<rect x="466" y="94" width="42" height="12" rx="2" fill="#0C1220" stroke="#2D3D52"/>
<circle cx="470" cy="122" r="2.6" fill="#22C7B8"/>
</g>
<text x="487" y="152" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">someone else's</text>
<path d="M180 208 C160 190 145 180 133 166" fill="none" stroke="#8B7BF0" stroke-width="1.5" marker-end="url(#ah3)"/>
<path d="M310 208 L310 168" fill="none" stroke="#8B7BF0" stroke-width="1.5" marker-end="url(#ah3)"/>
<path d="M440 208 C460 190 475 180 487 166" fill="none" stroke="#8B7BF0" stroke-width="1.5" marker-end="url(#ah3)"/>
<rect x="150" y="210" width="320" height="42" rx="8" fill="rgba(139,123,240,.08)" stroke="#8B7BF0" stroke-width="1.6"/>
<text x="310" y="230" fill="#8B7BF0" font-family="JetBrains Mono" font-size="12.5" text-anchor="middle">virtualisation layer</text>
<text x="310" y="245" fill="#5B7290" font-family="JetBrains Mono" font-size="9" text-anchor="middle">divides the machine up and keeps them apart</text>
<path d="M310 296 L310 258" fill="none" stroke="#8B7BF0" stroke-width="1.5" marker-end="url(#ah3)"/>
<path d="M281 306 L292 296 L350 296 L339 306 Z" fill="#1B2738" stroke="#3D5170" stroke-width="1.4" stroke-linejoin="round"/>
<path d="M339 306 L350 296 L350 374 L339 384 Z" fill="#161F2D" stroke="#3D5170" stroke-width="1.4" stroke-linejoin="round"/>
<rect x="281" y="306" width="58" height="78" rx="3" fill="#141E2C" stroke="#3D5170" stroke-width="1.6"/>
<rect x="289" y="316" width="42" height="11" rx="2" fill="#0C1220" stroke="#2D3D52"/>
<rect x="289" y="332" width="42" height="11" rx="2" fill="#0C1220" stroke="#2D3D52"/>
<rect x="289" y="348" width="42" height="11" rx="2" fill="#0C1220" stroke="#2D3D52"/>
<circle cx="293" cy="372" r="2.8" fill="#34D399" filter="url(#s3)"/>
<text x="386" y="348" fill="#8FA0BD" font-family="JetBrains Mono" font-size="11">one physical server</text>
<text x="386" y="363" fill="#5B7290" font-family="JetBrains Mono" font-size="9">the real hardware</text>
</svg>
<div class="dcap">one real machine underneath, three independent computers on top</div>
</div>

When you launch an EC2 instance later, this is what you are getting: a slice of a machine in a building you will never visit, billed by the second.

## How much do you want to manage?

Renting compute is not all or nothing. The more AWS manages, the less work you do, and the less control you have.

<div class="diagram">
<svg viewBox="0 0 620 290">
<text x="118" y="30" fill="#8FA0BD" font-family="JetBrains Mono" font-size="11" text-anchor="middle">On premises</text>
<text x="278" y="30" fill="#8FA0BD" font-family="JetBrains Mono" font-size="11" text-anchor="middle">IaaS</text>
<text x="278" y="44" fill="#5B7290" font-family="JetBrains Mono" font-size="9" text-anchor="middle">(EC2)</text>
<text x="438" y="30" fill="#8FA0BD" font-family="JetBrains Mono" font-size="11" text-anchor="middle">PaaS</text>
<text x="438" y="44" fill="#5B7290" font-family="JetBrains Mono" font-size="9" text-anchor="middle">(Lambda)</text>
<text x="562" y="30" fill="#8FA0BD" font-family="JetBrains Mono" font-size="11" text-anchor="middle">SaaS</text>
<text x="562" y="44" fill="#5B7290" font-family="JetBrains Mono" font-size="9" text-anchor="middle">(Gmail)</text>
<rect x="52" y="58" width="132" height="30" rx="6" fill="rgba(245,165,36,.13)" stroke="#F5A524" stroke-width="1.2"/>
<rect x="52" y="94" width="132" height="30" rx="6" fill="rgba(245,165,36,.13)" stroke="#F5A524" stroke-width="1.2"/>
<rect x="52" y="130" width="132" height="30" rx="6" fill="rgba(245,165,36,.13)" stroke="#F5A524" stroke-width="1.2"/>
<rect x="52" y="166" width="132" height="30" rx="6" fill="rgba(245,165,36,.13)" stroke="#F5A524" stroke-width="1.2"/>
<rect x="52" y="202" width="132" height="30" rx="6" fill="rgba(245,165,36,.13)" stroke="#F5A524" stroke-width="1.2"/>
<text x="118" y="78" fill="#F5A524" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">your app</text>
<text x="118" y="114" fill="#F5A524" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">runtime</text>
<text x="118" y="150" fill="#F5A524" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">OS</text>
<text x="118" y="186" fill="#F5A524" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">virtualisation</text>
<text x="118" y="222" fill="#F5A524" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">hardware</text>
<rect x="212" y="58" width="132" height="30" rx="6" fill="rgba(245,165,36,.13)" stroke="#F5A524" stroke-width="1.2"/>
<rect x="212" y="94" width="132" height="30" rx="6" fill="rgba(245,165,36,.13)" stroke="#F5A524" stroke-width="1.2"/>
<rect x="212" y="130" width="132" height="30" rx="6" fill="rgba(245,165,36,.13)" stroke="#F5A524" stroke-width="1.2"/>
<rect x="212" y="166" width="132" height="30" rx="6" fill="rgba(34,199,184,.10)" stroke="#22C7B8" stroke-width="1.2"/>
<rect x="212" y="202" width="132" height="30" rx="6" fill="rgba(34,199,184,.10)" stroke="#22C7B8" stroke-width="1.2"/>
<text x="278" y="78" fill="#F5A524" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">your app</text>
<text x="278" y="114" fill="#F5A524" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">runtime</text>
<text x="278" y="150" fill="#F5A524" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">OS</text>
<text x="278" y="186" fill="#22C7B8" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">virtualisation</text>
<text x="278" y="222" fill="#22C7B8" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">hardware</text>
<rect x="372" y="58" width="132" height="30" rx="6" fill="rgba(245,165,36,.13)" stroke="#F5A524" stroke-width="1.2"/>
<rect x="372" y="94" width="132" height="30" rx="6" fill="rgba(34,199,184,.10)" stroke="#22C7B8" stroke-width="1.2"/>
<rect x="372" y="130" width="132" height="30" rx="6" fill="rgba(34,199,184,.10)" stroke="#22C7B8" stroke-width="1.2"/>
<rect x="372" y="166" width="132" height="30" rx="6" fill="rgba(34,199,184,.10)" stroke="#22C7B8" stroke-width="1.2"/>
<rect x="372" y="202" width="132" height="30" rx="6" fill="rgba(34,199,184,.10)" stroke="#22C7B8" stroke-width="1.2"/>
<text x="438" y="78" fill="#F5A524" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">your app</text>
<text x="438" y="114" fill="#22C7B8" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">runtime</text>
<text x="438" y="150" fill="#22C7B8" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">OS</text>
<text x="438" y="186" fill="#22C7B8" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">virtualisation</text>
<text x="438" y="222" fill="#22C7B8" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">hardware</text>
<rect x="518" y="58" width="88" height="174" rx="6" fill="rgba(34,199,184,.10)" stroke="#22C7B8" stroke-width="1.2"/>
<text x="562" y="150" fill="#22C7B8" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">all of it</text>
<rect x="52" y="252" width="14" height="12" rx="3" fill="rgba(245,165,36,.2)" stroke="#F5A524" stroke-width="1.1"/>
<text x="74" y="262" fill="#5B7290" font-family="JetBrains Mono" font-size="10">you manage</text>
<rect x="176" y="252" width="14" height="12" rx="3" fill="rgba(34,199,184,.15)" stroke="#22C7B8" stroke-width="1.1"/>
<text x="198" y="262" fill="#5B7290" font-family="JetBrains Mono" font-size="10">the provider manages</text>
</svg>
<div class="dcap">the further right, the less you look after and the less you control</div>
</div>

This course lives in the middle. You rent virtual machines and stay responsible for what runs on them, because that is where you learn how everything fits together.

## Where your server physically is

"The cloud" is an unhelpful word. It suggests something floating and placeless. It is the opposite: buildings, with security guards, full of racks of machines, in specific countries.

<div class="diagram">
<svg viewBox="0 0 620 290">
<defs><filter id="s5" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<text x="160" y="24" fill="#22C7B8" font-family="JetBrains Mono" font-size="12" text-anchor="middle">Data centre A</text>
<text x="160" y="40" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">Availability Zone A</text>
<text x="460" y="24" fill="#22C7B8" font-family="JetBrains Mono" font-size="12" text-anchor="middle">Data centre B</text>
<text x="460" y="40" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">Availability Zone B</text>
<line x1="30" y1="240" x2="590" y2="240" stroke="#243347" stroke-width="1.5"/>
<rect x="92" y="56" width="26" height="16" rx="2" fill="#182636" stroke="#3D5170" stroke-width="1.2"/>
<rect x="128" y="56" width="26" height="16" rx="2" fill="#182636" stroke="#3D5170" stroke-width="1.2"/>
<rect x="164" y="56" width="26" height="16" rx="2" fill="#182636" stroke="#3D5170" stroke-width="1.2"/>
<rect x="64" y="72" width="192" height="10" rx="2" fill="#182636" stroke="#22C7B8" stroke-width="1.5"/>
<rect x="72" y="82" width="176" height="158" fill="#141E2C" stroke="#22C7B8" stroke-width="1.6"/>
<rect x="92" y="104" width="26" height="56" rx="2" fill="#0A1220" stroke="#2D3D52"/><rect x="96" y="110" width="18" height="3" fill="#22C7B8" opacity=".8"/><rect x="96" y="118" width="18" height="3" fill="#22C7B8" opacity=".55"/><rect x="96" y="126" width="18" height="3" fill="#22C7B8" opacity=".75"/>
<rect x="126" y="104" width="26" height="56" rx="2" fill="#0A1220" stroke="#2D3D52"/><rect x="130" y="110" width="18" height="3" fill="#22C7B8" opacity=".6"/><rect x="130" y="118" width="18" height="3" fill="#22C7B8" opacity=".85"/><rect x="130" y="126" width="18" height="3" fill="#22C7B8" opacity=".5"/>
<rect x="194" y="104" width="26" height="56" rx="2" fill="#0A1220" stroke="#2D3D52"/><rect x="198" y="110" width="18" height="3" fill="#22C7B8" opacity=".7"/><rect x="198" y="118" width="18" height="3" fill="#22C7B8" opacity=".6"/><rect x="198" y="126" width="18" height="3" fill="#22C7B8" opacity=".85"/>
<rect x="92" y="172" width="26" height="56" rx="2" fill="#0A1220" stroke="#2D3D52"/><rect x="96" y="178" width="18" height="3" fill="#22C7B8" opacity=".65"/><rect x="96" y="186" width="18" height="3" fill="#22C7B8" opacity=".8"/>
<rect x="126" y="172" width="26" height="56" rx="2" fill="#0A1220" stroke="#2D3D52"/><rect x="130" y="178" width="18" height="3" fill="#22C7B8" opacity=".8"/><rect x="130" y="186" width="18" height="3" fill="#22C7B8" opacity=".55"/>
<rect x="160" y="172" width="26" height="56" rx="2" fill="#0A1220" stroke="#2D3D52"/><rect x="164" y="178" width="18" height="3" fill="#22C7B8" opacity=".7"/><rect x="164" y="186" width="18" height="3" fill="#22C7B8" opacity=".9"/>
<rect x="194" y="172" width="26" height="56" rx="2" fill="#0A1220" stroke="#2D3D52"/><rect x="198" y="178" width="18" height="3" fill="#22C7B8" opacity=".6"/><rect x="198" y="186" width="18" height="3" fill="#22C7B8" opacity=".75"/>
<g filter="url(#s5)">
<rect x="160" y="104" width="26" height="56" rx="2" fill="#0A1220" stroke="#F5A524" stroke-width="1.6"/>
<rect x="164" y="110" width="18" height="3" fill="#F5A524"/><rect x="164" y="118" width="18" height="3" fill="#F5A524" opacity=".7"/><rect x="164" y="126" width="18" height="3" fill="#F5A524" opacity=".5"/>
</g>
<line x1="173" y1="160" x2="140" y2="264" stroke="#F5A524" stroke-width="1.2"/>
<text x="132" y="278" fill="#F5A524" font-family="JetBrains Mono" font-size="10" text-anchor="middle">your server is a slice of one of these</text>
<rect x="392" y="56" width="26" height="16" rx="2" fill="#182636" stroke="#3D5170" stroke-width="1.2"/>
<rect x="428" y="56" width="26" height="16" rx="2" fill="#182636" stroke="#3D5170" stroke-width="1.2"/>
<rect x="464" y="56" width="26" height="16" rx="2" fill="#182636" stroke="#3D5170" stroke-width="1.2"/>
<rect x="364" y="72" width="192" height="10" rx="2" fill="#182636" stroke="#22C7B8" stroke-width="1.5"/>
<rect x="372" y="82" width="176" height="158" fill="#141E2C" stroke="#22C7B8" stroke-width="1.6"/>
<rect x="392" y="104" width="26" height="56" rx="2" fill="#0A1220" stroke="#2D3D52"/><rect x="396" y="110" width="18" height="3" fill="#22C7B8" opacity=".7"/><rect x="396" y="118" width="18" height="3" fill="#22C7B8" opacity=".85"/>
<rect x="426" y="104" width="26" height="56" rx="2" fill="#0A1220" stroke="#2D3D52"/><rect x="430" y="110" width="18" height="3" fill="#22C7B8" opacity=".6"/><rect x="430" y="118" width="18" height="3" fill="#22C7B8" opacity=".7"/>
<rect x="460" y="104" width="26" height="56" rx="2" fill="#0A1220" stroke="#2D3D52"/><rect x="464" y="110" width="18" height="3" fill="#22C7B8" opacity=".9"/><rect x="464" y="118" width="18" height="3" fill="#22C7B8" opacity=".55"/>
<rect x="494" y="104" width="26" height="56" rx="2" fill="#0A1220" stroke="#2D3D52"/><rect x="498" y="110" width="18" height="3" fill="#22C7B8" opacity=".65"/><rect x="498" y="118" width="18" height="3" fill="#22C7B8" opacity=".8"/>
<rect x="392" y="172" width="26" height="56" rx="2" fill="#0A1220" stroke="#2D3D52"/><rect x="396" y="178" width="18" height="3" fill="#22C7B8" opacity=".8"/><rect x="396" y="186" width="18" height="3" fill="#22C7B8" opacity=".6"/>
<rect x="426" y="172" width="26" height="56" rx="2" fill="#0A1220" stroke="#2D3D52"/><rect x="430" y="178" width="18" height="3" fill="#22C7B8" opacity=".55"/><rect x="430" y="186" width="18" height="3" fill="#22C7B8" opacity=".85"/>
<rect x="460" y="172" width="26" height="56" rx="2" fill="#0A1220" stroke="#2D3D52"/><rect x="464" y="178" width="18" height="3" fill="#22C7B8" opacity=".75"/><rect x="464" y="186" width="18" height="3" fill="#22C7B8" opacity=".6"/>
<rect x="494" y="172" width="26" height="56" rx="2" fill="#0A1220" stroke="#2D3D52"/><rect x="498" y="178" width="18" height="3" fill="#22C7B8" opacity=".7"/><rect x="498" y="186" width="18" height="3" fill="#22C7B8" opacity=".8"/>
<line x1="256" y1="150" x2="364" y2="150" stroke="#3D5170" stroke-width="1.2" stroke-dasharray="4 4"/>
<text x="310" y="142" fill="#5B7290" font-family="JetBrains Mono" font-size="9.5" text-anchor="middle">miles apart</text>
<text x="310" y="166" fill="#5B7290" font-family="JetBrains Mono" font-size="9" text-anchor="middle">own power</text>
<text x="430" y="278" fill="#8B7BF0" font-family="JetBrains Mono" font-size="10.5" text-anchor="middle">both inside one Region, eu-west-1</text>
</svg>
<div class="dcap">a Region is an area containing several separate data centres</div>
</div>

<div class="callout why"><b>Why two buildings matter.</b> A Region is a geographic area, like Ireland. Inside it are several Availability Zones, each a physically separate data centre with its own power, far enough apart that a fire or flood in one does not touch the others. Run in only one Zone and a bad day there is a bad day for you. Spreading across two is how you survive it, and you will do that in Phase 5.</div>

## So who secures what?

<div class="callout break"><b>Think about it first.</b> AWS owns the building, the physical computer, and the virtualisation layer that created your virtual machine. So when a security update comes out for the operating system inside your virtual machine, does AWS install it for you?</div>

No. The line between what they secure and what you secure is one of the most important things to get straight early.

<div class="diagram">
<svg viewBox="0 0 620 260">
<defs><filter id="s6" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<g filter="url(#s6)"><rect x="46" y="26" width="250" height="200" rx="12" fill="rgba(245,165,36,.05)" stroke="#F5A524" stroke-width="1.6"/></g>
<text x="171" y="50" fill="#F5A524" font-family="JetBrains Mono" font-size="11.5" text-anchor="middle">YOURS</text>
<text x="171" y="66" fill="#5B7290" font-family="JetBrains Mono" font-size="9" text-anchor="middle">security IN the cloud</text>
<text x="70" y="94" fill="#8FA0BD" font-family="Inter" font-size="11">your application code</text>
<text x="70" y="118" fill="#8FA0BD" font-family="Inter" font-size="11">the operating system and patches</text>
<text x="70" y="142" fill="#8FA0BD" font-family="Inter" font-size="11">who can log in, and how</text>
<text x="70" y="166" fill="#8FA0BD" font-family="Inter" font-size="11">firewall rules you configure</text>
<text x="70" y="190" fill="#8FA0BD" font-family="Inter" font-size="11">your data, and its encryption</text>
<line x1="310" y1="40" x2="310" y2="212" stroke="#3D5170" stroke-width="1.5" stroke-dasharray="4 4"/>
<g filter="url(#s6)"><rect x="324" y="26" width="250" height="200" rx="12" fill="rgba(34,199,184,.05)" stroke="#22C7B8" stroke-width="1.6"/></g>
<text x="449" y="50" fill="#22C7B8" font-family="JetBrains Mono" font-size="11.5" text-anchor="middle">AWS</text>
<text x="449" y="66" fill="#5B7290" font-family="JetBrains Mono" font-size="9" text-anchor="middle">security OF the cloud</text>
<text x="348" y="94" fill="#8FA0BD" font-family="Inter" font-size="11">the physical buildings</text>
<text x="348" y="118" fill="#8FA0BD" font-family="Inter" font-size="11">the hardware and racks</text>
<text x="348" y="142" fill="#8FA0BD" font-family="Inter" font-size="11">the virtualisation layer</text>
<text x="348" y="166" fill="#8FA0BD" font-family="Inter" font-size="11">power, cooling, guards</text>
<text x="348" y="190" fill="#8FA0BD" font-family="Inter" font-size="11">the network between Regions</text>
<text x="310" y="246" fill="#5B7290" font-family="JetBrains Mono" font-size="10" text-anchor="middle">the line sits exactly where your virtual machine begins</text>
</svg>
<div class="dcap">the Shared Responsibility Model, in one picture</div>
</div>

Almost everything on the left is something you have to configure correctly, and almost every real-world breach happens there rather than on AWS's side: a server left open to the internet, a permission set too wide, an unpatched operating system.