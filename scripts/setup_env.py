"""
Create / complete .env: generate missing seeds, derive agent addresses, print them.

    python scripts/setup_env.py

Existing values are never overwritten, so an agent already registered on Agentverse
keeps its address as long as its seed is in .env.
"""

import os
import re
import secrets
import shutil
import sys

from uagents.crypto import Identity

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV, EXAMPLE = os.path.join(ROOT, ".env"), os.path.join(ROOT, ".env.example")

AGENTS = [  # (label, seed var, address var)
    ("Coordinator (ASI:One chat)", "RATION_COORDINATOR_SEED", None),
    ("Stock Validator", "RATION_VALIDATOR_SEED", "STOCK_VALIDATOR_ADDRESS"),
    ("Shortage Analyst", "SHORTAGE_ANALYST_SEED", "SHORTAGE_ANALYST_ADDRESS"),
    ("Notice Agent", "NOTICE_AGENT_SEED", "NOTICE_AGENT_ADDRESS"),
    ("Weighing Agent", "WEIGHING_AGENT_SEED", "WEIGHING_AGENT_ADDRESS"),
]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def get(text, key):
    m = re.search(rf"^{key}=(.*)$", text, re.M)
    return m.group(1).strip() if m else ""


def put(text, key, value):
    if re.search(rf"^{key}=", text, re.M):
        return re.sub(rf"^{key}=.*$", lambda _: f"{key}={value}", text, flags=re.M)
    return text.rstrip("\n") + f"\n{key}={value}\n"


def main():
    if not os.path.exists(ENV):
        shutil.copy(EXAMPLE, ENV)
        print("Created .env from .env.example")
    text = read(ENV)
    for label, seed_var, addr_var in AGENTS:
        seed = get(text, seed_var)
        if not seed:
            seed = f"ration-seva-{seed_var.lower()}-{secrets.token_hex(24)}"
            text = put(text, seed_var, seed)
            print(f"Generated {seed_var}")
        address = Identity.from_seed(seed, 0).address
        if addr_var:
            current = get(text, addr_var)
            if current and current != address:
                print(f"WARNING: {addr_var} in .env ({current}) does not match its seed ({address}); updating.")
            text = put(text, addr_var, address)
        print(f"  {label:28s} {address}")
    with open(ENV, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Wrote {ENV} (never commit it)")


if __name__ == "__main__":
    sys.exit(main())
