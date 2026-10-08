---
phase: 3
order: 8
title: Rebuild it automatically
type: lab
time: ~25 min
cost: ~$0.02 an hour while running
buildsOn: Lab 3.7
summary: Terminate your server, lose everything you set up by hand, and rebuild it with a user data script instead.
draft: false
questions:
  - kind: recall
    q: "When does <b>user data</b> run?"
    options:
      - "Every time you SSH in"
      - "Once, on the server's first boot, as root"
      - "Every time the server starts"
      - "Only when you click Run in the console"
    correct: 1
    hint: "Check the log after you rebooted, if you're curious."
    explain: "User data runs once, the first time the server boots, as the root user. That's why it can install things and set up services without sudo."

  - kind: cause
    q: "You terminated <code>web-1</code> and everything you set up by hand was gone. Why?"
    options:
      - "Terminating wipes your security group"
      - "The app was only saved in memory"
      - "The server's EBS volume was set to delete on termination"
      - "AWS deletes your key pair"
    correct: 2
    hint: "Look at the Storage tab before terminating."
    explain: "The server's main disk is set to Delete on termination by default. Everything you installed lived on that disk, so it went too."

  - kind: predict
    q: "You launch a server whose user data downloads the app from the internet, into a subnet with no route to the internet. What happens?"
    options:
      - "The server starts, but the download fails, so the website never appears"
      - "AWS refuses to launch it"
      - "The app downloads through the local route instead"
      - "It works, because user data uses a special connection"
    correct: 0
    hint: "User data runs on the server, using the server's network."
    explain: "User data is just a script running on the server. If the server can't reach the internet, the download fails and the app is never installed. You'll meet exactly this in Phase 4."
---

**What you'll do:** Terminate your server and lose everything you set up on it. Then rebuild it with a script that sets itself up.

---

## Everything you did lives on one disk

Over the last few labs, you downloaded the app, set up a service and left a note. All of it lives on one server's disk. Delete the server, and you'd have to do it all again by hand.

## Step 1: Check what terminating deletes

1. In the EC2 console, select `{{ns}}-web-1`.
2. Open the **Storage** tab and look at the volume's **Delete on termination** setting.

It says **Yes**. Terminating the server deletes its disk too.

## Step 2: Terminate it

1. Choose **Instance state**, then **Terminate (delete) instance**, and confirm.

The state goes to **Shutting down**, then **Terminated**. After a while, it disappears from the list. The app, the service and your note are gone. Its public IP has gone back to AWS.

## User data

When you launch a server, you can give it a script called **user data**. The server runs it once, as root, the first time it boots.

<div class="diagram">
  <img
    src="/images/labs/03-08/manual-vs-user-data.svg"
    alt="By hand: launch, SSH in, download, set up the service, then it's ready, with every step done by you. With user data: launch with a script, the first boot runs it, and it's ready, with no SSH and no typing."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the same result, without you in the loop</div>
</div>

Here's the script. It does exactly what you did by hand in Lab 3.4:

```bash
#!/bin/bash
mkdir -p /opt/hello
curl -fsSL https://inthelab.ie/files/hello-server.py -o /opt/hello/hello-server.py
curl -fsSL https://inthelab.ie/files/hello.service -o /etc/systemd/system/hello.service
systemctl daemon-reload
systemctl enable --now hello
```

1. `#!/bin/bash` says this is a shell script.
2. `mkdir` creates the app's folder.
3. The two `curl` lines download the app and the service file.
4. The `systemctl` lines start the service now, and on every boot.

There's no `sudo`, because user data already runs as root. You can also [download the script](/files/user-data.sh).

## Step 3: Launch a server with user data

Launch a new server, the same way as Lab 3.1, with these differences:

1. **Name:** `{{ns}}-web-2`
2. **Key pair:** choose your existing `{{ns}}-key`.
3. Under **Network settings**, choose **Edit**, then:
    1. **VPC:** `{{ns}}-vpc`, **Subnet:** `{{ns}}-public-a`
    2. **Auto-assign public IP:** **Enable**
    3. **Firewall:** choose **Select existing security group**, then `{{ns}}-web-sg`.
4. Expand **Advanced details**, scroll to the bottom, and paste the script into **User data**.
5. Choose **Launch instance**.

<div class="callout shot">screenshot: the User data box under Advanced details with the script pasted in<br>save as <code>/images/labs/03-08/user-data-box.png</code></div>
<!--
<figure class="screenshot">
  <img
    src="/images/labs/03-08/user-data-box.png"
    alt="The User data box under Advanced details with the script pasted in."
  />
</figure>
-->

## Step 4: Open it

Wait until the instance is **Running**, then give it another minute for the script to finish.

Open `http://NEW_PUBLIC_IP` in your browser. The page loads, with a new server name. You never logged in.

## Step 5: Check it ran

SSH in to the new server, and look at the end of the user data log:

```bash
sudo tail -n 20 /var/log/cloud-init-output.log
```

**cloud-init** is the program that runs user data on boot. Its log shows what your script did.

<div class="callout break"><b>Page not loading?</b> This log is the first place to look. A typo or a failed download shows up here. Fix the script, terminate the server, and launch a new one: user data only runs on the first boot.</div>

## Summary

- Terminating deletes the server and, by default, its disk.
- User data is a script that runs once, as root, on first boot.
- `{{ns}}-web-2` set itself up without you logging in.
- If something goes wrong, `/var/log/cloud-init-output.log` shows what happened.

Keep `{{ns}}-web-2` for the next lab.
