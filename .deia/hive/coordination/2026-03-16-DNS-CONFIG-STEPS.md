# DNS Configuration: dev.shiftcenter.com Setup

**Date:** 2026-03-16
**Status:** Ready for Manual Configuration by Q88N (Dave)
**Dependencies:** w3-01 (Vercel/Railway repoint) COMPLETE

This document provides step-by-step instructions for manually configuring DNS through Cloudflare and assigning a custom domain in Vercel for the dev branch preview environment.

---

## Section 1: Cloudflare DNS Configuration

### 1.1 Login to Cloudflare Dashboard

1. Go to **https://dash.cloudflare.com/**
2. Log in with your Cloudflare account credentials
3. Select the **shiftcenter.com** domain from the domain list
4. In the left sidebar, click **DNS** under the domain menu

### 1.2 Add CNAME Record for dev.shiftcenter.com

**IMPORTANT:** Do NOT complete this step yet. You must get the exact CNAME target from Vercel first (see Section 2.3 below). Return to this step after completing Section 2.3.

When ready to add the record:

1. Click the **+ Add Record** button (top-right of DNS records table)
2. Configure the new CNAME record with these values:
   - **Type:** CNAME
   - **Name:** `dev` (Cloudflare will auto-populate the full domain as `dev.shiftcenter.com`)
   - **Target:** (Paste the exact value from Vercel - see Section 2.3)
     - Vercel will provide a project-specific target like `cname.vercel-dns.com` OR `d1d4fc829fe7bc7c.vercel-dns-017.com`
     - **Copy it exactly**, including the trailing period (.) if shown
   - **TTL:** Auto (or 3600 seconds if you prefer explicit TTL)
   - **Proxy status:** ☑ Proxied (Orange cloud) — **RECOMMENDED**
     - Orange cloud provides DDoS protection and CDN caching
     - This is safe to enable immediately with Vercel
3. Click **Save**
4. You should see the new record in the DNS table

### 1.3 Verify DNS Propagation (Wait ~5 minutes)

1. Open a terminal or command prompt
2. Run this command to check DNS propagation:
   ```bash
   nslookup dev.shiftcenter.com
   ```
3. **Expected output:** You should see `cname.vercel-dns.com` listed as the canonical name
4. If you see an error or no results, wait another 2-3 minutes and retry

---

## Section 2: Vercel Custom Domain Assignment

### 2.1 Login to Vercel Dashboard

1. Go to **https://vercel.com/dashboard**
2. Log in with your Vercel account (GitHub OAuth or email)
3. Select the **browser** project (the ShiftCenter frontend project)

### 2.2 Add Custom Domain to Project

1. In the left sidebar, click **Settings**
2. Click **Domains**
3. Click the **Add Domain** button (top-right)
4. Enter the domain: `dev.shiftcenter.com`
5. Click **Add** or **Continue**

### 2.3 Verify Domain Ownership (TXT Record)

If Vercel asks you to verify domain ownership (because the domain is already in use elsewhere):

1. Vercel will display a **TXT record** to add. Copy the entire TXT value shown.
2. Go back to Cloudflare DNS (`https://dash.cloudflare.com/` → shiftcenter.com → DNS)
3. Click **+ Add Record**
4. Configure the TXT record:
   - **Type:** TXT
   - **Name:** `dev` (or the full `_acme-challenge.dev` if Vercel specifies)
   - **Content:** Paste the TXT value Vercel provided
   - **TTL:** Auto
5. Click **Save**
6. Return to Vercel and click **Verify** or **Continue**
7. Vercel will check the TXT record (this may take 30-60 seconds)

### 2.4 Get Vercel CNAME Target

**CRITICAL STEP:** This is where you get the exact CNAME target to use in Cloudflare.

1. After adding the domain in Vercel, it will show DNS configuration instructions
2. Vercel displays something like:
   ```
   Type: CNAME
   Name: dev
   Value: cname.vercel-dns.com
   ```
   OR a project-specific value like:
   ```
   Type: CNAME
   Name: dev
   Value: d1d4fc829fe7bc7c.vercel-dns-017.com.
   ```

3. **Copy the exact "Value" shown** (including trailing period if present)
4. **Return to Cloudflare** (Section 1.2) and complete the CNAME record creation
5. After adding the CNAME in Cloudflare, return here
6. Vercel will automatically detect the CNAME and show a **checkmark** ✓ (may take 1-2 minutes)

### 2.5 Assign Domain to dev Branch

1. In the Vercel **Domains** settings, find your `dev.shiftcenter.com` entry
2. Look for a **Branch** dropdown or field
3. Select or enter **`dev`** as the target branch
4. Ensure the setting shows:
   ```
   dev.shiftcenter.com → dev branch
   ```
5. Click **Save** or let it auto-save

---

## Section 3: SSL Configuration

### 3.1 Wait for Vercel SSL Certificate Issuance

1. Vercel automatically requests an SSL certificate from Let's Encrypt once the CNAME is verified
2. This typically takes **5-15 minutes**
3. In Vercel → Domains, you will see the SSL status change:
   - Initially: ⚠️ "Pending verification"
   - After verification: ✓ "Issued"

### 3.2 Configure Cloudflare SSL/TLS Mode

1. Go to Cloudflare Dashboard → **shiftcenter.com** domain
2. In the left sidebar, click **SSL/TLS**
3. Click the **Overview** tab
4. Under **SSL/TLS encryption mode**, ensure it is set to:
   - **Full** — Required for Vercel (prevents redirect loops)
   - OR **Full (Strict)** — Also works (validates Vercel's certificate)
   - **DO NOT use "Flexible"** — causes infinite redirect loops
5. If not already set to Full or Full (Strict), select **Full** and click **Save**

**Why Full mode is required:**
- Vercel automatically redirects HTTP to HTTPS
- If Cloudflare uses "Flexible" mode, it sends HTTP to Vercel
- Vercel redirects that HTTP to HTTPS, creating an infinite loop
- "Full" mode sends HTTPS from Cloudflare to Vercel, avoiding the loop
- "Full (Strict)" also works and adds certificate validation

**Reference:** [Vercel KB: Resolve redirect loops with Cloudflare](https://vercel.com/kb/guide/resolve-err-too-many-redirects-when-using-cloudflare-proxy-with-vercel)

### 3.3 Verify Cloudflare Proxy Status

The Cloudflare proxy (orange cloud) should already be enabled if you followed Section 1.2.

1. Go to Cloudflare → shiftcenter.com → **DNS**
2. Find the `dev` CNAME record
3. Verify the cloud icon is **orange** (Proxied), not gray (DNS only)
4. If gray, click the cloud icon to toggle to orange
5. Orange cloud provides Cloudflare's CDN, DDoS protection, and caching

---

## Section 4: Railway API Domain Verification

### 4.1 Verify api.shiftcenter.com CNAME (Already Set)

1. In Cloudflare DNS, check if `api.shiftcenter.com` already has a CNAME record pointing to Railway
2. Look for an entry like:
   ```
   api    CNAME    merry-learning-production-xxxx.railway.app    DNS only
   ```
3. If **NOT present**, add it:
   - **Type:** CNAME
   - **Name:** `api`
   - **Target:** (Get this from Railway dashboard → merry-learning → Settings → Domain)
   - **TTL:** Auto
4. Click **Save**

### 4.2 Verify Railway Service URL

1. Go to **Railway Dashboard** (https://railway.app/dashboard)
2. Open the **merry-learning** service (ShiftCenter hivenode)
3. Click **Settings** → **Networking** → **Custom Domain**
4. Verify `api.shiftcenter.com` is listed and shows "Active" status
5. Railway will show the CNAME target it expects (e.g., `merry-learning-production-xxxx.up.railway.app`)
6. Ensure Cloudflare's CNAME matches this exact target

**Note on Railway SSL:**
Railway automatically issues Let's Encrypt SSL certificates for custom domains. When you add `api.shiftcenter.com`, Railway will create an `_acme-challenge` CNAME record requirement. If SSL is pending:
- Check for a required `_acme-challenge.api` CNAME in Cloudflare
- If using Cloudflare proxy (orange cloud), you may need to disable it temporarily during SSL verification
- See [Railway Custom Domain Docs](https://docs.railway.com/networking/domains/working-with-domains) for troubleshooting

---

## Section 5: Verification Checklist

Run these tests to confirm everything is working:

### 5.1 DNS Resolution Tests

**Open a terminal and run:**

```bash
# Test dev.shiftcenter.com resolution
nslookup dev.shiftcenter.com

# Expected output: Points to cname.vercel-dns.com

# Test api.shiftcenter.com resolution
nslookup api.shiftcenter.com

# Expected output: Points to Railway domain (e.g., merry-learning-production-xxxx.railway.app)
```

### 5.2 Browser HTTPS Test

1. Open your browser and visit: **https://dev.shiftcenter.com**
2. **Expected outcome:**
   - Page loads successfully
   - No SSL certificate warning ✓
   - Shows the ShiftCenter chat app (or code EGG by default)
   - URL bar shows green lock icon 🔒

3. Test EGG parameter:
   - Visit **https://dev.shiftcenter.com?egg=chat**
   - Should load the chat interface (if available)

### 5.3 API Health Check Test

1. Open your browser and visit: **https://api.shiftcenter.com/health**
2. **Expected outcome:**
   - Returns HTTP 200 status
   - Shows JSON response (or text, depending on hivenode response format)
   - Example: `{"status": "ok"}` or similar

3. Or test via curl:
   ```bash
   curl -I https://api.shiftcenter.com/health
   ```
   Should return: `HTTP/2 200` (or `HTTP/1.1 200`)

### 5.4 SSL Certificate Validation

1. In your browser, click the lock icon next to the URL
2. Click **Certificate** or **Connection is secure**
3. **Expected values:**
   - **Issued to:** `dev.shiftcenter.com` (or wildcard `*.shiftcenter.com`)
   - **Issued by:** Let's Encrypt (via Vercel)
   - **Expiration:** Should be ~90 days from now
   - **Status:** Valid ✓

---

## Troubleshooting

### DNS Not Resolving After 10 minutes

1. Check Cloudflare CNAME record is correctly entered: `cname.vercel-dns.com`
2. Flush your local DNS cache:
   ```bash
   # macOS:
   sudo dscacheutil -flushcache

   # Windows:
   ipconfig /flushdns

   # Linux:
   sudo systemctl restart systemd-resolved
   ```
3. Try nslookup again

### SSL Certificate Pending (Red ⚠️)

1. Confirm CNAME record exists in Cloudflare
2. Wait another 5-10 minutes (Let's Encrypt validation can be slow)
3. In Vercel → Domains, click **Refresh** to force a re-check
4. Check Vercel error message: it will specify the exact DNS validation step failing

### 404 Not Found on dev.shiftcenter.com

1. Verify the `dev` branch exists in GitHub (it should)
2. Confirm Vercel deployment completed: Vercel → Deployments → check `dev` branch status
3. Check that domain is assigned to `dev` branch (not `main`)

### api.shiftcenter.com Returns 502 or 503

1. Confirm Railway `merry-learning` service is running (Railway dashboard)
2. Check Railway deployment logs for errors
3. Verify CNAME in Cloudflare matches Railway's assigned domain exactly

---

## Summary of DNS Records (Final State)

After all steps, Cloudflare DNS should contain:

```
NAME                TYPE   VALUE                              PROXY
dev                 CNAME  cname.vercel-dns.com              DNS only (or Orange)
api                 CNAME  merry-learning-prod-xxxx.railway  DNS only
shiftcenter.com     A      <existing IP>                      <existing>
www                 CNAME  <existing target>                  <existing>
[others]            ...    ...                                ...
```

---

## Next Steps After Verification

1. **Mark DNS configuration complete** in task tracker
2. **Update browser env vars** in Vercel (VITE_API_URL should point to https://api.shiftcenter.com)
3. **Test full integration:** Login via GitHub on dev.shiftcenter.com, verify API calls work
4. **Consider enabling Cloudflare features:**
   - Cache rules for static assets
   - Rate limiting for API routes
   - Web Analytics

---

**Document Version:** 2.0 (Updated with Vercel project-specific CNAME research)
**Last Updated:** 2026-03-16
**Author:** BEE-HAIKU-TASK-200
**Previous Version:** BEE-2026-03-16-TASK-186

## Sources

### Vercel Documentation
- [Adding & Configuring a Custom Domain](https://vercel.com/docs/domains/working-with-domains/add-a-domain)
- [Assigning a custom domain to an environment](https://vercel.com/docs/domains/working-with-domains/add-a-domain-to-environment)
- [Troubleshooting domains](https://vercel.com/docs/domains/troubleshooting)
- [How to add a custom domain (KB)](https://vercel.com/kb/guide/how-do-i-add-a-custom-domain-to-my-vercel-project)
- [Resolve "err_too_many_redirects" with Cloudflare](https://vercel.com/kb/guide/resolve-err-too-many-redirects-when-using-cloudflare-proxy-with-vercel)

### Railway Documentation
- [Working with Domains | Railway Docs](https://docs.railway.com/networking/domains/working-with-domains)
- [Public Networking | Railway Docs](https://docs.railway.com/guides/public-networking)

### Cloudflare Documentation
- [SSL/TLS Encryption modes](https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/)
- [Full mode](https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/full/)
- [Flexible mode](https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/flexible/)
