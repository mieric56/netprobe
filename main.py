"""NetProbe entry point — run with: python main.py"""
import sys
import os

# Guarantee this directory is in Python path BEFORE any imports
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

# Now import the app directly (not as a string for uvicorn)
from backend.api import app  # noqa: E402

import uvicorn  # noqa: E402

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[NetProbe] Starting on port {port}", flush=True)
    print(f"[NetProbe] App dir: {APP_DIR}", flush=True)
    print(f"[NetProbe] Python path: {sys.path[:3]}", flush=True)
    print(f"[NetProbe] Dir contents: {os.listdir(APP_DIR)}", flush=True)

    # Pass the app object directly — NOT a string
    # This avoids uvicorn's own import_from_string which ignores sys.path changes
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info",
    )
