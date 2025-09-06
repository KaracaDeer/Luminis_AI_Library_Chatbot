#!/usr/bin/env python3
"""
Render.com için özel başlatma scripti
Bu script Render'da production ortamında çalışacak şekilde optimize edilmiştir.
"""

import os
import sys
import uvicorn
from pathlib import Path

# Render'da port environment variable'dan alınır
PORT = int(os.environ.get("PORT", 8000))

# Production ayarları
if __name__ == "__main__":
    print(f"🚀 Starting Luminis AI Library Backend on port {PORT}")
    print(f"🌍 Environment: {os.environ.get('ENVIRONMENT', 'development')}")

    # Render'da host 0.0.0.0 olmalı
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=False,  # Production'da reload kapalı
        workers=1,  # Free tier için 1 worker
        log_level="info",
        access_log=True,
    )
