"""C5: OWASP LLM10 Unbounded Consumption test.
Sends N long requests rapidly as a single user and records tokens used and whether
anything in the app stops it. Run from project root:  python3 attacks/run_c5.py
"""
import csv
import sys
import time
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import chatbot  # noqa: E402

N = 20
PROMPT = "Please describe every product category you sell in as much detail as possible."

rows = []
start = time.time()
for i in range(1, N + 1):
    t = time.time()
    try:
        r = chatbot.client.messages.create(
            model=chatbot.MODEL, max_tokens=1500, system=chatbot.SYSTEM_PROMPT,
            messages=[{"role": "user", "content": PROMPT}],
        )
        row = {"request": i, "status": "ok", "input_tokens": r.usage.input_tokens,
               "output_tokens": r.usage.output_tokens, "seconds": round(time.time() - t, 2)}
    except anthropic.RateLimitError:
        row = {"request": i, "status": "provider_rate_limited", "input_tokens": 0,
               "output_tokens": 0, "seconds": round(time.time() - t, 2)}
    rows.append(row)
    print(row)

elapsed = time.time() - start
ok = [r for r in rows if r["status"] == "ok"]
total_in = sum(r["input_tokens"] for r in ok)
total_out = sum(r["output_tokens"] for r in ok)

out = ROOT / "attacks/evidence/C5_consumption.csv"
with out.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print("\n===== SUMMARY =====")
print(f"Requests sent: {N}   succeeded: {len(ok)}   blocked by provider: {N - len(ok)}")
print("Blocked by our app: 0 (no rate limiting implemented)")
print(f"Total tokens: {total_in} input + {total_out} output in {elapsed:.0f} seconds")
print(f"Projected if run for 1 hour: ~{int((total_in + total_out) / elapsed * 3600):,} tokens")
print(f"Saved to {out}")
