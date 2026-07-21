#!/bin/bash
# Deploy-watch for the sds-core/tokens.css race fix (CR-289559752, commit 95e176e5).
# Tripwires: (1) prod stops emitting the buggy "background-installing" string and
# starts emitting the fixed "blocking"/"already at" strings; (2) tokens.css ENOENT → 0.
# Read-only. Usage: ./deploy-watch.sh [lookback_minutes, default 60]
set -euo pipefail
PROFILE=design-assistant; REGION=us-east-1; LG=/mde/environments
MINS="${1:-60}"; now=$(date +%s); start=$((now - MINS*60))
echo "=== SDT tokens.css race — deploy watch @ $(date -u +%FT%TZ) (last ${MINS}m) ==="
q() {
  local qs="$1"
  local id; id=$(aws logs start-query --log-group-name "$LG" --start-time "$start" --end-time "$now" \
    --query-string "$qs" --region "$REGION" --profile "$PROFILE" --output text --query 'queryId')
  sleep 5
  aws logs get-query-results --query-id "$id" --region "$REGION" --profile "$PROFILE" --output json 2>/dev/null \
    | python3 -c "import sys,json;r=json.load(sys.stdin).get('results',[]);print({f['field']:f['value'] for f in r[0]} if r else {'n':'0'})"
}
echo -n "  BUGGY  [background-installing]      "; q 'filter @message like /background-installing sub-packages/ | stats count(*) as n'
echo -n "  FIXED  [installing (blocking)]      "; q 'filter @message like /installing sub-packages \(blocking\)/ | stats count(*) as n'
echo -n "  FIXED  [all sub-packages already]   "; q 'filter @message like /all sub-packages already at/ | stats count(*) as n'
echo -n "  CRASH  [tokens.css ENOENT lines]    "; q 'filter @message like /tokens.css/ and @message like /ENOENT/ | stats count(*) as n'
echo "  VERDICT: fix is LIVE when background-installing→0, a FIXED string>0, and ENOENT→0."
