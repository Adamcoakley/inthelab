---
phase: 1
order: 1
title: Create your AWS account
type: lab
time: ~30 min
cost: Free
summary: Create an AWS account, secure the root user, and set up a budget alert.
draft: false
questions:
  - kind: recall
    q: "What is the <b>root user</b>?"
    options:
      - "Any user with admin permissions"
      - "The login created with the account, which can do anything and can't be restricted"
      - "A user that only AWS staff can access"
      - "The first server you launch"
    correct: 1
    hint: "Think about the very first email and password you used."
    explain: "The root user is the email and password you signed up with. It owns the account and can do everything, including closing it, so you protect it with MFA and barely use it."

  - kind: cause
    q: "Someone steals your root password, but MFA is turned on. Why can't they sign in?"
    options:
      - "AWS blocks every login from a new country"
      - "They also need the second factor, which only you have"
      - "Root passwords expire every day"
      - "The budget alert stops them"
    correct: 1
    hint: "MFA means something you know plus something you have."
    explain: "A password is only half of the sign-in. Without your passkey, phone app or security key, the stolen password on its own is useless."

  - kind: predict
    q: "You set a $10 monthly budget and forget a server running for a week. What happens?"
    options:
      - "AWS turns the server off automatically"
      - "Nothing, budgets only work on the Paid plan"
      - "You get an email once your spending crosses the budget"
      - "The account closes immediately"
    correct: 2
    hint: "A budget sends alerts. Does it change anything in your account?"
    explain: "A budget emails you when spending goes over the limit. It doesn't stop or delete anything, so you still need to turn the resource off yourself."
---

**What you'll do:** Create an AWS account, add MFA to the root user, and set up a budget alert.

---

## Your AWS account

Everything you create in this course will live inside your AWS account. Any AWS usage is tied to that account, which also has its own 12-digit account ID, like `123456789012`.

## The root user

When you create an AWS account, you also create the root user. It's the email address and password you signed up with.

The root user has full access to everything in the account, and its access can't be limited. If someone gets hold of it, they control the account. For that reason, AWS recommends only using it for the few tasks that require it, such as:

- changing the account name, email address or root password
- changing your support plan
- closing the account

For everything else, you'll use an IAM user. An IAM user is a separate login that only has the permissions you give it. You'll create one in the next lab.


## Step 1: Sign up

Go to `aws.amazon.com` and choose **Create account**.

You’ll be asked for an email address, password and account name.

AWS will email you a code to verify the address.

<figure class="screenshot">
  <img
    src="/images/labs/01-01/signup-start.png"
    alt="AWS sign-up page showing the root user email address and AWS account name fields."
  />
</figure>

## Step 2: Choose the Free plan

AWS asks you to pick a plan.

- **Free plan:** you get credits to spend on AWS services and can't be charged. It ends after six months or when the credits run out, whichever is first.
- **Paid plan:** same starting credits, but once they're used up, your card is billed.

Choose the **Free plan**. If you make a mistake, it costs credits rather than money. You can upgrade later.

<figure class="screenshot">
  <img
    src="/images/labs/01-01/choose-plan.png"
    alt="Choose your account plan: free vs paid plans."
  />
</figure>

## Step 3: Finish verification

AWS asks for contact details, a payment card and a phone number for verification. For the support plan, choose **Basic support** (free).

Activation usually takes a few minutes.

<figure class="screenshot">
  <img
    src="/images/labs/01-01/support-plan.png"
    alt="Choose your support plan: basic vs business support."
  />
</figure>

## Step 4: Sign in as the root user

Go to the AWS sign-in page, choose **Root user**, and sign in with your email and password.

This is the **AWS Management Console**, the website you use to manage your account. Lab 1.3 covers it properly.

<figure class="screenshot">
  <img
    src="/images/labs/01-01/root-sign-in.png"
    alt="Root user sign in"
  />
</figure>

## Step 5: Protect the root user with MFA

**MFA** (multi-factor authentication) means signing in needs your password plus a second check, like a code from your phone. A leaked password alone isn't enough to get in.

Open the account menu in the top-right corner and choose **Security credentials**. Under **Multi-factor authentication (MFA)**, choose **Assign MFA device**.

You can pick:

- **Passkey or security key:** your phone, fingerprint reader or a physical key. The easiest and most secure option.
- **Authenticator app:** e.g. Google Authenticator or Microsoft Authenticator, which shows a 6-digit code that changes every 30 seconds.

Follow the prompts, then sign out and back in to test it. AWS requires MFA on the root user anyway.

<figure class="screenshot">
  <img
    src="/images/labs/01-01/root-mfa.png"
    alt="Setup MFA for root user"
  />
</figure>

## Step 6: Set up a budget alert

A **budget** emails you when your spending goes over an amount you set. Set one up before you create anything.

<div class="diagram">
  <img
    src="/images/labs/01-01/budget-alert.svg"
    alt="A spending line rising over a month and crossing a dashed $1 budget line, which triggers an email alert."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">you get an email when spending goes over the budget</div>
</div>

Search for **Budgets** in the console search bar and open it. Choose **Create budget**, then **Use a template**, then **Monthly cost budget**.

- **Budget name:** `monthly-budget`
- **Budgeted amount:** `10` (that's $10, yours can be lower)
- **Email recipients:** your email address

Choose **Create budget**.

<figure class="screenshot">
  <img
    src="/images/labs/01-01/budget-template.png"
    alt="Monthly cost budget setup"
  />
</figure>

<div class="callout why"><b>A budget only sends alerts.</b> It doesn't stop or delete anything. If you get the email, you need to find what's running and turn it off.</div>

## Step 7: Enable IAM access to billing

This setting lets IAM users you create in the future view billing information, as long as their permissions allow it.

1. Open the account menu in the top-right corner and choose **Account**.
2. Scroll down to **IAM user and role access to Billing information** and choose **Edit**.
3. Tick **Activate IAM Access**, then choose **Update**.

<figure class="screenshot">
  <img
    src="/images/labs/01-01/billing-info.png"
    alt="AWS account settings showing the option to activate IAM access to billing information."
  />
</figure>

## Step 8: Find your account ID

Open the account menu in the top-right corner. Your account ID is shown there with a copy button. Save it somewhere, as you'll need it in the next lab.

## Summary

- You have an AWS account and know its account ID.
- The root user is protected with MFA.
- A budget will email you if you start spending money.

Next, you'll create an IAM user for everyday use, so you can stop using the root user.
