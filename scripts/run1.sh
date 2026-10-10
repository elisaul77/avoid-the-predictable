#!/bin/bash
# $1 = json line
id=$(jq -r .id <<<"$1"); m=$(jq -r .model <<<"$1"); p=$(jq -r .prompt <<<"$1")
f="$OUT/$(tr '|' '_' <<<"$id").txt"; [ -s "$f" ] && exit 0
cd "$OUT" && printf '%s' "$p" | timeout 300 claude -p --model "$m" --tools "" 2>/dev/null | grep -v "Permission allow rule" > "$f.tmp" && mv "$f.tmp" "$f"
