# Custom domain: `ains6003.courses.castalia.institute`

## Why this hostname

Course sites use **`{courseId}.courses.castalia.institute`** so DNS sits on the Castalia zone behind **Cloudflare** (proxied CNAME). That enables:

- DDoS mitigation and WAF at the edge
- **Cloudflare Zero Trust Access** per course (see [castalia.institute/docs/CLOUDFLARE_ZERO_TRUST_SETUP.md](https://github.com/CastaliaInstitute/castalia.institute/blob/main/docs/CLOUDFLARE_ZERO_TRUST_SETUP.md))
- Optional **castalia-chrome-injector** Worker routes on `*.courses.castalia.institute`

Entitlement JWT claims use `course_ains6003` (resource id `ains6003`).

## DNS

| Type | Name | Target | Proxy |
|------|------|--------|-------|
| CNAME | `ains6003.courses` | `castaliainstitute.github.io` | **Proxied** (orange cloud) |

Apply locally:

```bash
set -a && source ../castalia.institute/.env && set +a
./scripts/cf-dns-ains6003-github-pages.sh
```

Or run the [**Sync Cloudflare DNS**](../.github/workflows/sync-dns.yml) workflow (requires repo secret `CLOUDFLARE_API_TOKEN`).

## GitHub Pages

After DNS exists, set the custom domain on this repo:

```bash
gh api -X PUT repos/CastaliaInstitute/ains-6003-deep-learning-and-neural-networks/pages \
  -f build_type=workflow \
  -f cname='ains6003.courses.castalia.institute'
```

CI copies [`pages/CNAME`](../pages/CNAME) into the published artifact. Wait for GitHub to show the domain as verified, then enforce HTTPS in repo Pages settings.

## Cloudflare SSL

With proxy enabled, use **SSL/TLS → Full (strict)** once GitHub has issued a certificate for the custom host.

## Public URL

https://ains6003.courses.castalia.institute/
