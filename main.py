"""NetProbe entry point — run with: python main.py"""
import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "backend.api:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        reload=False,
    )
