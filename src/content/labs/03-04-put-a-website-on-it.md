---
phase: 3
order: 4
title: Put a website on it
type: lab
time: ~30 min
cost: ~$0.02 an hour while running
buildsOn: Lab 3.3
summary: Download and run the course's test app, open it in your browser, and keep it running as a service.
draft: false
questions:
  - kind: recall
    q: "Why does the app need <code>sudo</code> to listen on port 80?"
    options:
      - "Because Python always needs sudo"
      - "Ports below 1024 can only be opened by the root user"
      - "Because port 80 is encrypted"
      - "So the security group allows it"
    correct: 1
    hint: "Try it with port 8000 and you won't need sudo."
    explain: "On Linux, ports below 1024 are reserved for the root user. sudo runs the command as root. The security group is a separate thing, outside the server."

  - kind: cause
    q: "The page was working. You stop the app and reload, and an error appears instantly instead of spinning. What does that tell you?"
    options:
      - "The security group has blocked you"
      - "The route to the internet has been removed"
      - "Your traffic reached the server, but nothing is listening on port 80"
      - "DNS has failed"
    correct: 2
    hint: "A firewall drops traffic silently. Who sent the error?"
    explain: "A fast \"refused\" means the server itself answered: the route and firewall are fine, but nothing is listening on that port. A slow timeout means something dropped the traffic on the way."

  - kind: predict
    q: "You start the app with <code>sudo python3 hello-server.py</code>, then close your SSH window. What happens to the website?"
    options:
      - "It stops, because the app was tied to your SSH session"
      - "It keeps running forever"
      - "It restarts automatically"
      - "It moves to port 8000"
    correct: 0
    hint: "What runs the app: your session, or the server itself?"
    explain: "A program you start in your terminal stops when that session ends. To keep it running, you hand it to systemd, which runs it as a service and starts it again after a reboot."
---

**What you'll do:** Download the course's test app onto your server, open it in your browser, and set it up to keep running after you log out.

---

## The test app

Throughout the course, you'll use a small web app that shows which server answered your request. It's a single Python file that only uses what's already installed on Amazon Linux.

You'll download the files from this website. [View the code](/files/hello-server.py) if you're curious, you don't need to understand it.

## Step 1: Download the app

SSH in to your server:

<div class="os-switch">
<div class="os-tabs"><button type="button" data-os-pick="mac">macOS / Linux</button><button type="button" data-os-pick="windows">Windows</button></div>
<div class="os-panel" data-os="mac">

```bash
ssh -i ~/Downloads/{{ns}}-key.pem ec2-user@PUBLIC_IP
```

</div>
<div class="os-panel" data-os="windows">

```powershell
ssh -i $HOME\Downloads\{{ns}}-key.pem ec2-user@PUBLIC_IP
```

</div>
</div>

Then create a folder for it and download it:

```bash
sudo mkdir -p /opt/hello
sudo curl -fsSL https://inthelab.ie/files/hello-server.py -o /opt/hello/hello-server.py
```

That download worked because `public-a` has a route to the internet, and the security group allows all outbound traffic. Remember that in Phase 4.

## Step 2: Run it

```bash
sudo python3 /opt/hello/hello-server.py
```

You'll see:

```text
hello-server listening on port 80
```

It's waiting for requests. Leave this terminal open.

<div class="callout why"><b>Why sudo?</b> On Linux, ports below 1024 can only be opened by the root user. <code>sudo</code> runs the command as root.</div>

## Step 3: Open it in your browser

In your browser, go to `http://PUBLIC_IP`. Type the `http://` yourself: the app doesn't use HTTPS yet, and some browsers try HTTPS first if you leave it out. If your browser warns that the site isn't secure, continue anyway. 

The page spins, then gives up.

<div class="callout break"><b>Think about it first.</b> SSH works, so the route is fine. What's different about this request?</div>

It's a different port. The security group allows port 22 from you, and nothing on port 80.

## Step 4: Allow web traffic

1. In the EC2 console, go to **Security Groups** and select `{{ns}}-web-sg`.
2. In the **Inbound rules** tab, choose **Edit inbound rules**, then **Add rule**.
3. **Type:** **HTTP**. The port fills in as 80.
4. **Source:** **Anywhere-IPv4**. This fills in `0.0.0.0/0`.
5. Choose **Save rules**.

Your security group now has two inbound rules: SSH from your IP, and HTTP from anywhere.

<figure class="screenshot">
  <img
    src="/images/labs/03-04/allow-port-80.png"
    alt="The security group's inbound rules: SSH on port 22 from your IP, and HTTP on port 80 from 0.0.0.0/0."
  />
</figure>

Reload the page. This time it loads:

<figure class="screenshot">
  <img
    src="/images/labs/03-04/hello-page.png"
    alt="The browser showing the Hello from page served by the EC2 instance."
  />
</figure>

That's your server answering. The page shows which server it is, which Availability Zone it's in and how many requests it has served. Those details will matter later in the course, when more than one server is answering.

## The whole path, working

Your request made it all the way from your browser to the app:

<div class="diagram">
  <img
    src="/images/labs/03-04/arch-website-live.svg"
    alt="Your laptop connects on port 22 and anyone connects on port 80. Both go through the internet gateway, across the public subnet, and through the security group, which allows 22 from your IP and 80 from anyone."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the whole path, working</div>
</div>

Your request came in through the internet gateway, the route table sent it to your subnet, and the security group let it in on port 80.

Your security group now has two inbound rules, and they give different access. Port 80 is open to everyone, because a website is meant to be visited. Port 22 is open only to you, because SSH gives full control of the server. Each port is open only as widely as it needs to be.

## Step 5: Stop the app, and reload

In your terminal, press `Ctrl+C` to stop the app. Then reload the page.

This time, the error appears instantly. That's different from before, and the difference is useful:

<div class="diagram">
  <img
    src="/images/labs/03-04/timeout-vs-refused.svg"
    alt="A timeout: traffic is dropped at a firewall and no answer comes back, so the browser keeps spinning. Refused: traffic passes the firewall and reaches the server, but nothing is listening on port 80, so the server answers no straight away."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">a slow failure and a fast failure mean different things</div>
</div>

- **Timeout (slow):** something dropped your traffic on the way, like a missing route or a firewall. Nothing answered.
- **Refused (fast):** your traffic reached the server, but nothing is listening on that port. The server itself said no.

When something doesn't load, how fast it fails tells you where to look.

## Step 6: Run it as a service

An app you start in your terminal stops when you stop it, or when your SSH session ends. A real web server needs to keep running on its own, and start again after a reboot.

On Linux, that's the job of **systemd**. It runs programs as **services**. You tell it about a service with a small file.

1. Download the service file:

```bash
sudo curl -fsSL https://inthelab.ie/files/hello.service -o /etc/systemd/system/hello.service
```

2. Tell systemd to read it:

```bash
sudo systemctl daemon-reload
```

3. Start the service now, and every time the server boots:

```bash
sudo systemctl enable --now hello
```

4. Check it's running:

```bash
systemctl status hello
```

Look for `active (running)` in green. Press `q` to get back to the prompt.

5. Log out:

```bash
exit
```

Reload the page. It still works, even though you're not logged in.

## Summary

- The test app shows which server answered your request.
- Port 80 is open to everyone; port 22 only to you.
- A timeout means traffic was dropped on the way. A fast refusal means it arrived, but nothing was listening.
- The app now runs as a systemd service, so it keeps running without you.

Keep the server for the next lab. If you're taking a break, stop it. The app will start again on its own when you start the server.