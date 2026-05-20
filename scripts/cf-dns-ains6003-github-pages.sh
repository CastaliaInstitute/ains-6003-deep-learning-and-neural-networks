#!/usr/bin/env bash
# Create or fix ains6003.courses.castalia.institute -> GitHub Pages (proxied CNAME).
# Proxied (orange cloud) enables Cloudflare DDoS/WAF; pair with Zero Trust Access on this hostname.
#
# Auth: CLOUDFLARE_API_TOKEN or CLOUDFLARE_TOKEN from castalia.institute/.env
#
# Usage:
#   ./scripts/cf-dns-ains6003-github-pages.sh
#   PROXIED=false ./scripts/cf-dns-ains6003-github-pages.sh   # grey cloud (GitHub TLS only)
#   DRY_RUN=1 ./scripts/cf-dns-ains6003-github-pages.sh

set -euo pipefail

DRY_RUN="${DRY_RUN:-0}"
ZONE_NAME="${ZONE_NAME:-castalia.institute}"
RECORD_NAME="${RECORD_NAME:-ains6003.courses}"
TARGET="${GITHUB_PAGES_CNAME_TARGET:-castaliainstitute.github.io}"
PROXIED="${PROXIED:-true}"

if [[ -z "${CLOUDFLARE_API_TOKEN:-}" && -n "${CLOUDFLARE_TOKEN:-}" ]]; then
  export CLOUDFLARE_API_TOKEN="$CLOUDFLARE_TOKEN"
fi

if [[ -z "${CLOUDFLARE_API_TOKEN:-}" && -f ../castalia.institute/.env ]]; then
  set -a
  # shellcheck disable=SC1091
  source ../castalia.institute/.env
  set +a
  [[ -z "${CLOUDFLARE_API_TOKEN:-}" && -n "${CLOUDFLARE_TOKEN:-}" ]] && export CLOUDFLARE_API_TOKEN="$CLOUDFLARE_TOKEN"
fi

if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]]; then
  echo "error: set CLOUDFLARE_API_TOKEN (Zone DNS Edit on ${ZONE_NAME})" >&2
  exit 1
fi

command -v curl >/dev/null || command -v jq >/dev/null || {
  echo "error: curl and jq required" >&2
  exit 1
}

API="https://api.cloudflare.com/client/v4"
AUTH=(-H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}")

zone_id="$(curl -sS "${API}/zones?name=${ZONE_NAME}" "${AUTH[@]}" | jq -r '.result[0].id // empty')"
[[ -n "$zone_id" ]] || { echo "error: zone ${ZONE_NAME} not found" >&2; exit 1; }

fqdn="${RECORD_NAME}.${ZONE_NAME}"
proxied_json="$( [[ "$PROXIED" == "true" ]] && echo true || echo false )"
body="$(jq -nc --arg name "$RECORD_NAME" --arg content "$TARGET" --argjson proxied "$proxied_json" \
  '{type:"CNAME", name:$name, content:$content, ttl:1, proxied:$proxied}')"

echo "zone=${ZONE_NAME}  record=${fqdn}  ->  ${TARGET}  proxied=${PROXIED}"

existing="$(curl -sS -G "${API}/zones/${zone_id}/dns_records" "${AUTH[@]}" \
  --data-urlencode "name=${fqdn}" --data-urlencode "per_page=5")"
id="$(echo "$existing" | jq -r '.result[0].id // empty')"

if [[ "$DRY_RUN" == "1" ]]; then
  echo "DRY_RUN body: $body"
  exit 0
fi

if [[ -n "$id" ]]; then
  curl -sS -X PUT "${API}/zones/${zone_id}/dns_records/${id}" "${AUTH[@]}" \
    -H "Content-Type: application/json" -d "$body" | jq '{success, errors, result: .result | {name, content, proxied}}'
else
  curl -sS -X POST "${API}/zones/${zone_id}/dns_records" "${AUTH[@]}" \
    -H "Content-Type: application/json" -d "$body" | jq '{success, errors, result: .result | {name, content, proxied}}'
fi

echo "Verify: dig ${fqdn} CNAME +short @1.1.1.1"
echo "GitHub Pages: gh api -X PUT repos/CastaliaInstitute/ains-6003-deep-learning-and-neural-networks/pages -f cname=${fqdn}"
