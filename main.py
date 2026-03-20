"""NetProbe entry point — run with: python main.py"""
import sys
import os

# Ensure the app root is in the Python path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[NetProbe] Starting on port {port}")
    print(f"[NetProbe] App dir: {APP_DIR}")
    print(f"[NetProbe] DB path: {os.environ.get('NETPROBE_DB', '/data/netprobe.db')}")
    print(f"[NetProbe] Frontend: {os.path.join(APP_DIR, 'frontend')}")
    print(f"[NetProbe] Frontend exists: {os.path.isdir(os.path.join(APP_DIR, 'frontend'))}")

    uvicorn.run(
        "backend.api:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        reload=False,
    )
