"""
Start all five RationSeva agents locally, each logging to logs/<agent>.log.

    python scripts/run_local.py            # Coordinator with Agentverse mailbox (for ASI:One)
    python scripts/run_local.py --no-mailbox   # everything on local endpoints (for scripts/test_chat.py)

Ctrl+C stops all of them.
"""

import argparse
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS = ["main.py", "shortage_analyst.py", "notice_agent.py", "weighing_agent.py", "coordinator.py"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-mailbox", action="store_true", help="Coordinator on a local endpoint (local tests)")
    args = ap.parse_args()

    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1")
    if args.no_mailbox:
        env["COORDINATOR_MAILBOX"] = "false"
    os.makedirs(os.path.join(ROOT, "logs"), exist_ok=True)

    procs = []
    for script in AGENTS:
        log = open(os.path.join(ROOT, "logs", script.replace(".py", ".log")), "w", encoding="utf-8")
        procs.append((script, subprocess.Popen([sys.executable, script], cwd=ROOT, env=env,
                                               stdout=log, stderr=subprocess.STDOUT)))
        print(f"started {script} (pid {procs[-1][1].pid}) -> logs/{script.replace('.py', '.log')}", flush=True)
    reported = set()
    try:
        while True:   # a dead agent is reported, the others keep running (the Coordinator degrades gracefully)
            for script, p in procs:
                if p.poll() is not None and script not in reported:
                    reported.add(script)
                    print(f"{script} exited with code {p.returncode} - see logs/", flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        for _, p in procs:
            p.terminate()
        print("stopped")


if __name__ == "__main__":
    main()
