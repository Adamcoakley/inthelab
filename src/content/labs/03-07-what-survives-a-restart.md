---
phase: 3
order: 7
title: What survives a restart?
type: lab
time: ~20 min
cost: ~$0.02 an hour while running
buildsOn: Lab 3.6
summary: Stop and start your server, and see what changes, what stays, and why.
draft: false
questions:
  - kind: recall
    q: "After you stop and start an instance, which of these stays the same?"
    options:
      - "The public IP"
      - "What was in memory"
      - "The public IP and the private IP"
      - "The private IP and the files on the disk"
    correct: 3
    hint: "Which ones belong to your subnet and your EBS volume?"
    explain: "The private IP belongs to your subnet and the files are on the EBS volume, so both stay. The public IP goes back to AWS when you stop, and memory is wiped."

  - kind: cause
    q: "After you started the server again, the website came back without you doing anything. Why?"
    options:
      - "You ran systemctl enable, so systemd starts the app on every boot"
      - "AWS restarts every app automatically"
      - "The app was saved in memory"
      - "The security group restarted it"
    correct: 0
    hint: "Lab 3.4, step 6."
    explain: "systemctl enable told systemd to start the hello service every time the server boots. Without it, the app would have stayed off until you started it by hand."

  - kind: predict
    q: "A friend bookmarked <code>http://54.170.12.9</code>. You stop and start your server. What happens when they open the bookmark?"
    options:
      - "It works, because the website is still running"
      - "It works after a few minutes"
      - "It fails, because your server now has a different public IP"
      - "It redirects to the new IP automatically"
    correct: 2
    hint: "What happened to the public IP when you stopped the server?"
    explain: "The old public IP went back to AWS when you stopped the server, and you got a new one when you started it. That's one reason you don't hand out a server's IP. Phase 6 and Phase 8 give your site an address that doesn't change."
---

**What you'll do:** Leave something on your server, stop it, start it again, and see what survived.

---

## Step 1: Leave a note

SSH in and write a file:

```bash
echo "written before the stop" > ~/note.txt
```

Check how long the server has been running:

```bash
uptime
```

Log out with `exit`. In the console, write down the server's **Public IPv4 address** and **Private IPv4 address**. Open the website and note the **requests served** number.

## Step 2: Stop the server

1. In the EC2 console, select `{{ns}}-web-1`.
2. Choose **Instance state**, then **Stop instance**, and confirm.

Watch **Instance state** go from **Stopping** to **Stopped**. Look at the details: the **Public IPv4 address** is now empty.

<div class="callout shot">screenshot: the stopped instance's details with no public IPv4 address<br>save as <code>/images/labs/03-07/stopped-instance.png</code></div>
<!--
<figure class="screenshot">
  <img
    src="/images/labs/03-07/stopped-instance.png"
    alt="The stopped instance's details with no public IPv4 address."
  />
</figure>
-->

## Step 3: Start it again

1. Choose **Instance state**, then **Start instance**.
2. Wait for **Running**.

Compare the addresses with what you wrote down. The private IP is the same. The public IP is different.

## Step 4: See what survived

SSH in using the **new** public IP. Then:

```bash
cat ~/note.txt
```

```bash
uptime
```

Your note is still there. The uptime started again from zero.

Open the website at the new public IP. It works, because you ran `systemctl enable` in Lab 3.4. But **requests served** has started again from 1, because that count only lived in memory.

<div class="diagram">
  <img
    src="/images/labs/03-07/stop-start.svg"
    alt="A server goes from running, to stopped, to running again. The public IP changes from 54.170.12.9 to none to 34.244.7.81. The private IP stays 10.0.1.23. Files on the disk are kept. Memory is wiped. While stopped, you only pay for the disk."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">what changes, what stays</div>
</div>

## Why

An instance is two things that AWS keeps separate:

- **Compute:** a slice of CPU and memory on a physical machine. When you stop, AWS takes it back. When you start, you get a fresh slice, maybe on a different machine. Memory starts empty.
- **Storage:** the EBS volume. It's a separate disk on AWS's network, so it doesn't care which machine you're on. Your files wait for you.

The addresses split the same way:

- The **private IP** belongs to your subnet, and stays with the instance.
- The **public IP** is borrowed from AWS's pool. When you stop, it goes back, and you get a different one next time.

<div class="callout why"><b>Need a public IP that never changes?</b> AWS offers <b>Elastic IPs</b>, which you keep until you release them. They're charged by the hour. You won't need one: later, a load balancer and a domain name give your site an address that doesn't change.</div>

## Instance types

`t3.micro` is the **instance type**: it decides how much CPU and memory you rent. The letter is the family, the number is the generation, and the word is the size:

- **t:** general purpose, good for things that are quiet most of the time, like your test app
- **m:** general purpose, for steady work
- **c:** more CPU
- **r:** more memory

You can only change an instance's type while it's stopped: choose **Actions**, **Instance settings**, then **Change instance type**. You don't need to now.

## Stop versus terminate

You've now seen **stop** for real: compute goes, the disk stays, and you keep paying for the disk. In the next lab, you'll **terminate** a server, which deletes it, disk included.

## Summary

- Stopping gives back the compute. The EBS disk and private IP stay.
- The public IP changes every time you stop and start.
- systemd started your app again on boot, because you enabled it.
- The instance type sets the CPU and memory, and can be changed while stopped.

Keep the server for the next lab.
