# Networking Module — Domain + EC2 + DNS Project

Part of my [devops-learning](../) portfolio, built as the capstone project for the
**CoderCo DevOps Academy Networking Module**.

## What I Built

A live website served from my own AWS EC2 instance, reachable through a domain I
registered and configured myself:

**🔗 http://ilhamdevops.com**

The setup connects everything covered in the networking module — IP addressing,
DNS, routing, ports, and basic hosting — into one working, end-to-end deployment.

## Architecture

```
User Browser
     │
     │  DNS lookup (ilhamdevops.com → A record)
     ▼
Route 53 (DNS + Domain Registration)
     │
     │  Resolves to public IP
     ▼
EC2 Instance (Ubuntu, t2.micro)
     │
     │  Port 80 (HTTP)
     ▼
NGINX Web Server
```

## What I Did

1. **Registered a domain** (`ilhamdevops.com`) through AWS Route 53
2. **Launched an EC2 instance** (Ubuntu, t2.micro, Free Tier eligible)
3. **Configured the security group** to allow inbound HTTP (port 80) and SSH (port 22)
4. **Installed and started NGINX** on the instance via the terminal
5. **Created an A record** in Route 53 pointing `ilhamdevops.com` → EC2 public IP
6. **Verified DNS resolution and browser access** end-to-end

## Commands Used

Connecting and installing NGINX on the EC2 instance:

```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```

Diagnosing the DNS issue (see "Challenges" below):

```bash
nslookup ilhamdevops.com
nslookup ilhamdevops.com 8.8.8.8
```

## What I Learned

- How DNS actually resolves a domain to an IP address, step by step — from the
  resolver, through root and TLD servers, to the authoritative name server
- The difference between a **registrar** and a **DNS hosting provider** (and that
  they can be different companies, even though in this case both were Route 53)
- How **A records** work, and how to configure one to point a domain at a specific
  IPv4 address
- Why **security groups** need explicit inbound rules for each port/protocol —
  nothing gets through by default
- The full **NAT** and **routing** concepts underneath why a public IP is what the
  outside world actually sees, not a server's private IP
- Real hands-on subnetting and binary/CIDR math, used to actually understand IP
  addressing rather than just memorize it

## Challenges & How I Solved Them

**Problem:** After creating the A record and waiting overnight, the domain still
wouldn't resolve — `DNS_PROBE_FINISHED_NXDOMAIN` in the browser, and
`nslookup ilhamdevops.com` returned "No answer".

**Diagnosis:**
1. Checked the Route 53 hosted zone directly — the A record had never actually
   been created; only the default NS and SOA records were present. The original
   "Create record" click the night before hadn't fully saved.
2. Re-created the A record, this time confirming a green "INSYNC" status.
3. `nslookup ilhamdevops.com` *still* showed "No answer" — but running
   `nslookup ilhamdevops.com 8.8.8.8` (forcing the query through Google's public
   DNS instead of my local resolver) returned the correct IP immediately.

**Root cause:** the record itself was fine — my local DNS resolver had cached the
earlier "no record" response from before the A record existed.

**Fix:** confirmed the record was correct via an external resolver, then simply
waited for the local cache to expire. The domain resolved correctly in the browser
minutes later.

This was a good real-world lesson in isolating *which layer* a DNS problem lives
in — the record, the propagation, or the local cache — instead of assuming the
first failure means the whole setup is broken.

## Screenshots

See the `/screenshots` folder for:
- EC2 instance running
- NGINX installed and active (`systemctl status`)
- NGINX default page loading via public IP
- Domain registration confirmation
- Route 53 A record configuration
- Final result — NGINX page loading via `ilhamdevops.com`

---

*Built as part of the CoderCo DevOps Academy Networking Module.*
