#!/usr/bin/env bash

LOGFILE="${1:-connectivity.csv}"

PING_TARGETS="1.1.1.1 8.8.8.8"
HTTP_TARGETS="https://www.google.com/generate_204 https://cloudflare.com/cdn-cgi/trace"
DNS_TARGET="google.com"

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

PING_STATUS="FAIL"
PING_TIME="NA"

HTTP_STATUS="FAIL"
DNS_STATUS="FAIL"

# --- Ping test (success if ANY responds) ---
for target in $PING_TARGETS; do
    OUTPUT=$(ping -c 1 "$target" 2>/dev/null)

    if echo "$OUTPUT" | grep -q "time="; then
        PING_STATUS="OK"
        PING_TIME=$(echo "$OUTPUT" | sed -n 's/.*time=\([0-9.]*\).*/\1/p')
        break
    fi
    if echo "$OUTPUT" | grep -Eq "1 packets received|1 received"; then
        PING_STATUS="OK"
        PING_TIME=$(echo "$OUTPUT" | sed -n 's/.*time=\([0-9.]*\).*/\1/p')
        break
    fi
done

# --- DNS test ---
if nslookup "$DNS_TARGET" >/dev/null 2>&1; then
    DNS_STATUS="OK"
fi

# --- HTTP test (success if ANY responds) ---
for url in $HTTP_TARGETS; do
    if curl -fsS --max-time 5 "$url" >/dev/null 2>&1; then
        HTTP_STATUS="OK"
        break
    fi
done

HEADER="timestamp,ping_status,ping_ms,dns_status,http_status"
LINE="$TIMESTAMP,$PING_STATUS,$PING_TIME,$DNS_STATUS,$HTTP_STATUS"

# --- Create CSV if missing ---
if [ ! -f "$LOGFILE" ]; then
    echo "$HEADER" > "$LOGFILE"
fi

# --- Append log entry ---
echo "$LINE" >> "$LOGFILE"
