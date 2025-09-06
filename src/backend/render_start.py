#!/usr/bin/env python3
"""
Simple Render startup script
"""

import os
import uvicorn

# Render'da port environment variable'dan alınır
PORT = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    print(f"🚀 Starting Luminis AI Library Backend on port {PORT}")

    # Simple FastAPI app
    uvicorn.run(
        "main_simple_render:app",
        host="0.0.0.0",
        port=PORT,
        reload=False,
        log_level="info",
    )
