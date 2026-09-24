---
phase: 1
order: 2
title: IAM users and permissions
type: lab
time: ~40 min
cost: Free
buildsOn: Lab 1.1
summary: How AWS decides what each user is allowed to do, and creating the admin user you'll use from now on.
draft: false
questions:
  - kind: recall
    q: "In IAM, what is a <b>policy</b>?"
    options:
      - "A password rule for users"
      - "A document that lists which actions are allowed"
      - "A group of users"
      - "A backup of your account"
    correct: 1
    hint: "It's the list IAM checks every request against."
    explain: "A policy is a document of rules: which actions are allowed on which resources. You attach policies to users, groups or roles."

  - kind: cause
    q: "Your viewer user tries to create a user group and gets <code>AccessDenied</code>. Why?"
    options:
      - "The IAM service is down"
      - "Read-only users must use the CLI"
      - "No policy attached to the viewer allows that action, so it's denied by default"
      - "Only the root user can create groups"
    correct: 2
    hint: "Think about the firewall rule list from Lab 0.5."
    explain: "IAM denies everything unless a policy allows it. ReadOnlyAccess allows looking, not creating, so the request is refused."

  - kind: predict
    q: "You add a new teammate to the <b>admins</b> group. What can they do?"
    options:
      - "Nothing until you attach policies to them directly"
      - "Everything the admins group's policies allow"
      - "Only what the root user allows each time"
      - "Only read things for the first week"
    correct: 1
    hint: "Permissions attached to a group apply to everyone in it."
    explain: "Users get the permissions of every group they're in. That's why groups are useful: set permissions once, then just add or remove people."
---

**What you'll do:** Learn how IAM permissions work, create an admin user for everyday use, and test what happens when a user doesn't have permission.

---

## How AWS checks permissions

Everything you do in AWS, like launching a server or viewing a bill, is sent to AWS as a **request**. Before a request runs, AWS checks who sent it and whether they're allowed to do it.

That check is done by **IAM** (Identity and Access Management).

<div class="diagram">
  <img
    src="/images/labs/01-02/iam-decision.svg"
    alt="A person asks to create a user group. IAM checks whether any of their policies allow it. If yes, the group is created. If no, the request fails with AccessDenied."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">if no policy allows the action, it's denied</div>
</div>

## Users, groups, policies and roles

- **User:** a login for one person, with a password and ideally MFA.
- **Group:** a set of users. Permissions attached to a group apply to everyone in it.
- **Policy:** a document that lists what's allowed. You attach it to a user, group or role.
- **Role:** permissions that can be used temporarily, with no password. Mostly used by AWS services, e.g. a server that needs to read files.

<div class="diagram">
  <img
    src="/images/labs/01-02/users-groups-policies.svg"
    alt="Users belong to groups, and groups have policies attached. Below, an EC2 server borrows a role, which has a policy that lets it read one S3 bucket."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">users get permissions through groups; services use roles</div>
</div>

## What a policy looks like

Policies are written in JSON. Here's a short example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:ListAllMyBuckets",
      "Resource": "*"
    }
  ]
}
```

You don't need to write these yet. The three parts that matter are:

- **Effect:** allow or deny
- **Action:** what can be done, written as `service:action`
- **Resource:** which things it applies to (`*` means all of them)

So this policy allows listing S3 buckets, and nothing else.

AWS also provides ready-made policies, called **AWS managed policies**, like `AdministratorAccess` and `ReadOnlyAccess`. You'll use those in this lab.

## Step 1: Open IAM

Sign in as the root user. Search for **IAM** in the console search bar and open it.

The Region selector in the top-right corner shows **Global**, because IAM isn't tied to a Region. Lab 1.3 explains Regions.

<figure class="screenshot">
  <img
    src="/images/labs/01-02/iam-dashboard.png"
    alt="IAM dashboard user interface."
  />
</figure>

## Step 2: Create an admins group

In the left menu, choose **IAM user groups**, then **Create group**.

Enter the below details:
- **Group name:** `admins`
- **Attach permissions policies:** search for and tick `AdministratorAccess`

See below screenshot for reference.

<figure class="screenshot">
  <img
    src="/images/labs/01-02/group-details.png"
    alt="Create an IAM group with AWS managed policies."
  />
</figure>

<div class="callout why"><b>Why full admin access?</b> It's your own account and you'll be creating everything in it, so admin access is reasonable here. Least privilege matters more when giving access to other people or to servers, which comes later.</div>

## Step 3: Create your everyday user

In the left menu, choose **Users**, then **Create user**.

- **User name:** `admin`
- Tick **Provide user access to the AWS Management Console**
- Set a **custom password**

<figure class="screenshot">
  <img
    src="/images/labs/01-02/create-user.png"
    alt="Create IAM user"
  />
</figure>

Then choose **Next**. On the permissions page, choose **Add user to group** and tick `admins`. Choose **Next**, then **Create user**.

## Step 4: Save your sign-in link

On the final page, AWS shows a **console sign-in URL** for your account. It looks like `https://123456789012.signin.aws.amazon.com/console`. Save it as a bookmark.

<figure class="screenshot">
  <img
    src="/images/labs/01-02/sign-in-details.png"
    alt="AWS console sign-in URL"
  />
</figure>

## Step 5: Switch to your new user

Sign out of the root user. Open your sign-in link and sign in as `admin`.

Add MFA to this user as well: open the account menu in the top-right corner, choose **Security credentials**, and assign an MFA device, the same way you did for root.

<div class="callout break"><b>Use this user from now on.</b> Only sign in as root for the few tasks that require it, like closing the account.</div>

## Step 6: Test a user without permission

Using the same steps as above, create a second group called `read-only` and attach the `ReadOnlyAccess` policy. Then create a user called `readonly-user` with console access, and add them to `read-only` group.

Open a **new browser window**, go to your sign-in link, and sign in as `readonly-user`.You can open IAM and see users and groups, because read access is allowed.

Now try to create something. In IAM, choose **User groups**, then **Create group**, give it any name, and choose **Create user group**.

<figure class="screenshot">
  <img
    src="/images/labs/01-02/access-denied.png"
    alt="Readonly user receives access denied when trying to create an IAM group"
  />
</figure>

Read the error message. It tells you:

- **who** asked: `readonly-user`
- **what** they tried: `iam:CreateGroup`
- **why** it failed: no policy allows it

You'll see errors like this again during the course. They always tell you which user and which action were involved, which makes them quick to fix.

## Summary

- IAM checks every request, and denies anything no policy allows.
- You have an `admin` user with MFA, in an `admins` group.
- You'll use this user from now on instead of root.
