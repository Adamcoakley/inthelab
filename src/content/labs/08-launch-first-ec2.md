---
number: 8
title: Launch your first EC2
phase: 3
type: lab
time: ~35 min
cost: ~$0.02 if torn down
buildsOn: Lab 07
summary: Build a real server, connect to it, and load a web page running on it.
questions:
  - kind: recall
    q: "What is an AMI?"
    options:
      - "The size of your server (its CPU and memory)"
      - "The starting disk image your server boots from"
      - "The firewall around your server"
      - "Your login key"
    correct: 1
    hint: "Think about what decides which operating system your server runs."
    explain: "An AMI is the disk image, the operating system and pre-installed software your server copies and boots from. The <b>size</b> (CPU/memory) is the instance type, a common mix-up. The firewall is the security group, and the login key is your key pair."
  - kind: cause
    q: "Your web page loaded fine. If you had left <b>Auto-assign public IP</b> set to Disable, what would have happened?"
    options:
      - "The page would load exactly the same"
      - "The server wouldn't start"
      - "The server would run, but you couldn't reach it from your laptop"
      - "nginx wouldn't install"
    correct: 2
    hint: "The server doesn't need the internet to <i>run</i>. Think about what the public IP is actually for."
    explain: "The server runs fine either way, a public IP doesn't affect whether it boots. But without one, there's no public address to reach it at, so your browser (and SSH) couldn't connect. The server would be running, just unreachable from outside."
  - kind: predict
    q: "In the next lab you'll restrict the SSH rule to only your own IP address. Why would you want to do that?"
    options:
      - "To make the website load faster"
      - "So only you can attempt to log in, not the whole internet"
      - "To save money"
      - "So nginx keeps running"
    correct: 1
    hint: "SSH (port 22) is the login door. Who can currently knock on it?"
    explain: "Right now SSH is open to the whole internet, so anyone can <i>attempt</i> to log in (they'd still need your key, but you don't want them even trying). Restricting it to your IP means only your connection can reach the login door. It has nothing to do with speed, cost, or nginx."
---

**What you'll do:** Put a real Linux server inside the network you built, connect to it, and load a web page running on it. By the end you'll have launched, connected to, and served traffic from your first cloud server.

<blockquote class="note"><b>Before you start:</b> you'll need <code>{{ns}}-vpc</code> with a working public subnet and internet gateway from the last phase. If you're not sure your route is set up, that's fine, step 4 will show you if something's off, and that's a useful thing to see.</blockquote>

---

## Step 1: Open the launch screen

In the AWS console search bar at the top, type **EC2** and press enter. On the EC2 dashboard, find the big orange **Launch instance** button and click it.

You're now on the launch screen. It looks like a lot. Don't worry, we'll go through every box that matters and ignore the ones that don't.

![The EC2 dashboard with the Launch instance button highlighted](/images/example.png)
<figure><figcaption>↑ This is how a real screenshot looks. Replace public/images/example.png with your own capture.</figcaption></figure>

## Step 2: Name your server

At the top, under **Name and tags**, type a name: <code>{{ns}}-web-1</code>.

This is just a label so you can find it later, it doesn't affect anything technical. Naming things well is a habit worth building early: in a real account with hundreds of resources, good names save you. (Notice it starts with your own name, so it won't clash with anyone else's server in this account.)

## Step 3: Pick the operating system (the AMI)

Scroll to **Application and OS Images**. This is where you choose the AMI.

<div class="callout why"><b>What's an AMI?</b> Think of it as the starting disk image for your server, the operating system and any pre-installed software, frozen and ready to copy. When your server boots, it boots from this image. "Amazon Linux" is AWS's own free, lightweight Linux, and it's perfect for learning.</div>

Select **Amazon Linux** (it's usually the default and marked "Free tier eligible"). Leave the version as whatever's selected.

<div class="callout shot">📸 Screenshot slot: the AMI picker with Amazon Linux selected and the "Free tier eligible" tag visible.</div>

## Step 4: Pick the size (the instance type)

Under **Instance type**, you'll see something like <code>t3.micro</code> already selected.

<div class="callout why"><b>What's an instance type?</b> It's the size of your server, how much CPU and memory it gets. <code>t3.micro</code> gives you 1 CPU and 1 GB of memory. That's small, but it's free-tier eligible and plenty for a learning web server.</div>

Leave it on <code>t3.micro</code>. Resist the urge to pick something bigger, you don't need it, and bigger costs money.

## Step 5: Create a key pair (how you'll log in)

Under **Key pair (login)**, click **Create new key pair**.

<div class="callout why"><b>What's a key pair?</b> It's how you prove it's really you when you connect. AWS keeps one half (the public key), and you download the other half (the private key) as a file. When you connect, the two halves are checked against each other. Lose your half and you're locked out, there's no reset button.</div>

Name it <code>{{ns}}-key</code>, leave type as **RSA** and format as **.pem**, and click **Create key pair**. Your browser downloads the key file. Keep it somewhere safe.

<div class="callout shot">📸 Screenshot slot: the "Create key pair" dialogue filled in.</div>

## Step 6: Put it in the right place (network settings)

This is the step that matters most, so slow down here.

Under **Network settings**, click **Edit**. Then:

- **VPC:** choose <code>{{ns}}-vpc</code> (not the default one)
- **Subnet:** choose your **public** subnet
- **Auto-assign public IP:** set this to **Enable**

<div class="callout why"><b>Why enable a public IP?</b> Your server needs a public address so you can reach it from your laptop and so people can load its web page. A server in a public subnet without a public IP is like a shop on a main street with no street number, nobody can find it. (Later, you'll deliberately build servers <i>without</i> public IPs, and you'll see exactly why that's safer for real workloads.)</div>

<div class="callout shot">📸 Screenshot slot: network settings with {{ns}}-vpc, the public subnet, and auto-assign public IP set to Enable.</div>

## Step 7: Open the doors (security group)

Still in network settings, under **Firewall (security groups)**, choose **Create security group** and name it <code>{{ns}}-web-sg</code>. Tick the boxes to allow:

- **SSH** (so you can connect)
- **HTTP** (so the web page loads)

<div class="callout why"><b>What's a security group?</b> It's a firewall wrapped around <i>this specific server</i>. It decides what traffic is allowed in. Right now you're opening two doors: SSH (port 22) to log in, and HTTP (port 80) for the website. We'll go much deeper on this in the next lab.</div>

## Step 8: Launch

Scroll down and click the orange **Launch instance** button. You'll see a success message. Click **View all instances**.

Your server appears in the list. Under **Instance state** it'll say "Pending" for a moment, then "Running." Wait for the **Status check** to finish (it'll show "2/2 checks passed"). This takes a minute or two, the server is booting up.

## Step 9: Install a web server

Select your instance and click **Connect** at the top, then choose the **EC2 Instance Connect** tab and click **Connect**. A terminal opens in your browser, you're now *inside* your server.

Type these commands one at a time:

```bash
sudo yum install -y nginx
sudo systemctl start nginx
```

The first installs nginx (a web server), the second starts it running.

<div class="callout why"><b>What just happened?</b> nginx is software that listens for web requests and serves pages. You just installed it and switched it on. Your server is now ready to answer HTTP requests.</div>

## Step 10: See your website live

Go back to the instances list, select your server, and copy its **Public IPv4 address**. Paste it into a new browser tab.

You should see the nginx welcome page. **That's your server, on the internet, serving a page you turned on.** Take a second, you just did the thing.

<div class="callout shot">📸 Screenshot slot: the nginx welcome page loaded in a browser with the public IP in the address bar.</div>

---

<div class="callout break"><b>Don't forget teardown.</b> This lab's server is cheap, but leave nothing running you don't need. When you're done exploring: terminate <code>{{ns}}-web-1</code> from the console (Instance state → Terminate). We'll keep <code>{{ns}}-vpc</code> though, the next labs build on it.</div>
