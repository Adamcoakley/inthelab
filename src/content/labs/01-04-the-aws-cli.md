---
phase: 1
order: 4
title: The AWS CLI
type: lab
time: ~20 min
cost: Free
buildsOn: Lab 1.3
summary: Use the AWS CLI in CloudShell to check who you're signed in as and look at what's in your account.
draft: false
questions:
  - kind: recall
    q: "What does <code>aws sts get-caller-identity</code> tell you?"
    options:
      - "How much you've spent this month"
      - "Which account and which user your commands are running as"
      - "Which Region is fastest"
      - "Your password"
    correct: 1
    hint: "It answers the question: who am I?"
    explain: "It returns your account ID and the ARN of the identity you're signed in as. It's the first command to run when something doesn't behave as expected."

  - kind: cause
    q: "The console and the CLI both go through the same AWS API. What does that mean for permissions?"
    options:
      - "The CLI skips IAM checks"
      - "The CLI always has admin access"
      - "The same IAM rules apply, whichever one you use"
      - "Only the console checks MFA"
    correct: 2
    hint: "Both send requests to the same API."
    explain: "Every request goes to the same API, and IAM checks it the same way. If you're denied in the console, you'll be denied in the CLI too."

  - kind: predict
    q: "You switch the console to us-east-1, open CloudShell and run <code>aws ec2 describe-instances</code>. Your servers are in eu-west-1. What do you see?"
    options:
      - "Your eu-west-1 servers"
      - "An empty list, because CloudShell uses the Region selected in the console"
      - "An AccessDenied error"
      - "Servers from every Region"
    correct: 1
    hint: "Which Region does CloudShell use by default?"
    explain: "CloudShell uses the Region selected in the console. With us-east-1 selected, the command looks there, and your servers in eu-west-1 don't show up."
---

**What you'll do:** run AWS CLI commands in CloudShell, check who you're signed in as, and look at the IAM user and group you created in Lab 1.2.

---

## Why use the CLI?

The AWS CLI (command line interface) lets you manage AWS by typing commands instead of clicking. Commands are easy to repeat and put in scripts, and they give you quick answers to questions like "who am I signed in as?" or "what exists in this Region?".

The console and the CLI both send requests to the same AWS API, so the same IAM permissions apply to both.

<div class="diagram">
  <img
    src="/images/labs/01-04/console-cli-api.svg"
    alt="The console and the CLI both send requests to the AWS API, which checks IAM and then acts on your resources."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the console and the CLI both use the AWS API</div>
</div>

## Command structure

AWS CLI commands follow this pattern:

```text
aws <service> <action> --options
```

For example, `aws iam list-users` lists the users in IAM.

## Step 1: Open CloudShell

CloudShell is a terminal built into the AWS console. The AWS CLI is already installed, and it uses the same AWS permissions as the user you signed in with. There is nothing to install and no access keys to set up.

Click the CloudShell icon in the top bar. A terminal opens in your browser.

<figure class="screenshot">
  <img
    src="/images/labs/01-04/cloudshell.png"
    alt="The AWS console with the CloudShell icon highlighted and a CloudShell terminal open."
  />
</figure>

CloudShell uses the Region selected in the console as the default Region for AWS CLI commands.

## Step 2: Check who you are

```bash
aws sts get-caller-identity
```

The output looks like this:

```json
{
    "UserId": "AIDAEXAMPLEID",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/admin"
}
```

It shows which account and user your commands are running as. Run it whenever a command doesn't behave as expected: a surprising number of problems turn out to be "wrong account" or "wrong user".

The `Arn` value is an ARN (Amazon Resource Name). Lab 1.5 explains how to read them.

## Step 3: Look at what you created in Lab 1.2

List your IAM users:

```bash
aws iam list-users --output table
```

You should see the user: `admin`. `--output table` formats the result as a table, which can be easier to read than the default JSON.

List your groups:

```bash
aws iam list-groups --output table
```

You should see `admins`. Now check which policy is attached to it:

```bash
aws iam list-attached-group-policies --group-name admins --output table
```

This shows `AdministratorAccess`, the policy you attached in Lab 1.2. You've just checked your permissions setup without opening the IAM console.

<figure class="screenshot">
  <img
    src="/images/labs/01-04/cli-iam.png"
    alt="CloudShell showing the IAM users, groups and attached policies as tables."
  />
</figure>

## Step 4: Finding commands

You don't need to memorise commands. Add `help` after any service or action:

```bash
aws iam help
```

```bash
aws iam list-users help
```

Press `q` to exit the help page.

## Optional: install the CLI locally

You don't need this for the course, since CloudShell covers everything. It's useful if you want to run AWS commands from your own terminal.

Install it using AWS's [install guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). You need version 2.32.0 or newer, which you can check with:

```bash
aws --version
```

Then sign in using:

```bash
aws login
```

Enter `eu-west-1` as the Region and pick your admin session in the browser. To confirm it worked, use:

```bash
aws sts get-caller-identity
```

<div class="callout break"><b>Don't use access keys.</b> Older tutorials use <code>aws configure</code> with access keys. They don't expire, and leaked keys are a common way accounts get compromised.</div>

## Summary

- CloudShell runs AWS CLI commands in your browser, using the permissions of the user you're signed in as.
- `aws sts get-caller-identity` shows which account and user you're using.
- The CLI can show what's in your account, like IAM users, groups and their policies.
- Add `help` after any command to see what it can do.