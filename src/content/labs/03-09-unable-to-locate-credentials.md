---
phase: 3
order: 9
title: Unable to locate credentials
type: lab
time: ~25 min
cost: ~$0.02 an hour while running
buildsOn: Lab 3.8
summary: Give your server permission to use AWS with an IAM role, without putting any keys on it.
draft: false
questions:
  - kind: recall
    q: "What does an <b>IAM role</b> give an EC2 instance?"
    options:
      - "Temporary credentials that renew automatically"
      - "A permanent access key saved on its disk"
      - "A password for SSH"
      - "A public IP address"
    correct: 0
    hint: "Look at the Expiration line."
    explain: "The instance gets temporary credentials from the metadata service. They expire within hours, and AWS replaces them automatically. Nothing permanent is stored on the server."

  - kind: cause
    q: "With the role attached, <code>aws s3 ls</code> returns <code>AccessDenied</code>. Why?"
    options:
      - "S3 doesn't work from EC2"
      - "The role hasn't finished attaching"
      - "You need to run aws configure first"
      - "The role's policy only allows read-only EC2 actions"
    correct: 3
    hint: "Which policy did you attach to the role?"
    explain: "AmazonEC2ReadOnlyAccess only allows looking at EC2. Listing S3 buckets isn't in it, so IAM denies it by default, exactly like Lab 1.2."

  - kind: predict
    q: "You remove the role from the instance, then run <code>aws sts get-caller-identity</code> again. What happens?"
    options:
      - "It works, because the credentials were saved"
      - "It fails, because the server no longer has a role to get credentials from"
      - "It shows your admin user instead"
      - "The instance stops"
    correct: 1
    hint: "Where were the credentials coming from?"
    explain: "The credentials came from the metadata service, because of the role. With no role, the metadata service has nothing to give, and you're back to \"Unable to locate credentials\"."
---

**What you'll do:** Try to use AWS from your server, see it fail, and fix it with an IAM role instead of access keys.

---

## Servers need permissions too

So far, only you have used AWS: through the console and CloudShell, signed in as your `admin` user. But software running on a server often needs AWS too, like an app that reads files from S3.

IAM checks every request, whoever or whatever sends it. So your server needs an identity and permissions, just like you do.

## Step 1: Ask AWS who you are, from the server

SSH in to `{{ns}}-web-2` and run the command from Lab 1.4:

```bash
aws sts get-caller-identity
```

The AWS CLI is already installed on Amazon Linux. But:

```text
Unable to locate credentials. You can configure credentials by running "aws configure".
```

The server has no identity, so it can't make any AWS request at all.

<div class="callout break"><b>Don't do what the error suggests.</b> <code>aws configure</code> would save an access key on the server's disk. Those keys never expire, and anyone who gets a copy of the disk, a backup or a leaked file can use them. You'll copy this server's disk in the next lab, which would copy the keys with it.</div>

## Roles: permissions without keys

In Lab 1.2, you met **roles**: permissions that something uses temporarily, with no password. When you attach a role to an instance, the instance gets **temporary credentials** from the metadata service. They expire within hours, and AWS replaces them automatically before they do.

<div class="diagram">
  <img
    src="/images/labs/03-09/role-credentials.svg"
    alt="The IAM role web-role gives the web-2 server temporary keys through the instance metadata service. The AWS CLI uses them to call the AWS API, where IAM allows ec2:Describe but denies s3:List. Below, crossed out: access keys saved on the server, which never expire."
    style="width:100%;height:auto;display:block;margin:0;border:0;border-radius:0;box-shadow:none;position:relative;z-index:1;"
  />
  <div class="dcap">the server borrows permissions instead of storing them</div>
</div>

## Step 2: Create a role

1. Open **IAM**, choose **Roles** in the left menu, then **Create role**.
2. **Trusted entity type:** **AWS service**
3. **Use case:** **EC2**. This says who's allowed to use the role: EC2 instances.
4. Choose **Next**.
5. Search for `AmazonEC2ReadOnlyAccess` and tick it. This lets the server look at EC2, and nothing else.
6. Choose **Next**.
7. **Role name:** `{{ns}}-web-role`
8. Choose **Create role**.

<div class="callout shot">screenshot: the role's trusted entity set to AWS service, EC2<br>save as <code>/images/labs/03-09/trusted-entity.png</code></div>
<!--
<figure class="screenshot">
  <img
    src="/images/labs/03-09/trusted-entity.png"
    alt="The role's trusted entity set to AWS service, EC2."
  />
</figure>
-->

## Step 3: Attach it to your server

1. In the EC2 console, select `{{ns}}-web-2`.
2. Choose **Actions**, **Security**, then **Modify IAM role**.
3. Choose `{{ns}}-web-role`, then **Update IAM role**.

## Step 4: Try again

Back on the server:

```bash
aws sts get-caller-identity
```

This time it works:

```json
{
    "UserId": "AROAEXAMPLEID:i-0a1b2c3d4e5f67890",
    "Account": "123456789012",
    "Arn": "arn:aws:sts::123456789012:assumed-role/{{ns}}-web-role/i-0a1b2c3d4e5f67890"
}
```

Read the ARN: the server is using `{{ns}}-web-role`, and the session is named after its instance ID.

Now use the permission:

```bash
aws ec2 describe-instances --region eu-west-1 --query "Reservations[].Instances[].[InstanceId,State.Name,PrivateIpAddress]" --output table
```

The server can see itself in the list.

## Step 5: Try something it isn't allowed to do

```bash
aws s3 ls
```

`AccessDenied`. Read the error the way you did in Lab 1.2: **who** asked (`{{ns}}-web-role`), **what** it tried (`s3:ListAllMyBuckets`) and **why** it failed (no policy allows it).

The role only allows what the server needs. That's least privilege.

## Step 6: See the temporary credentials

The CLI gets its credentials from the metadata service. You can see when the current ones expire:

```bash
TOKEN=$(curl -s -X PUT http://169.254.169.254/latest/api/token -H "X-aws-ec2-metadata-token-ttl-seconds: 60")
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/{{ns}}-web-role | grep Expiration
```

The first line gets a short-lived token to talk to the metadata service. The second asks for the role's credentials and only shows when they expire. Run it again in an hour and the time will have moved on, because AWS swapped in new ones.

## Summary

- A server has no AWS permissions until you give it an identity.
- An IAM role gives it temporary credentials, with nothing saved on its disk.
- `{{ns}}-web-role` lets the server read EC2 information, and nothing else.
- Never use `aws configure` with access keys on a server.

Keep `{{ns}}-web-2` for the next lab.
