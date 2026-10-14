"""
app.py - Entry point utama Proyek "2EZ4U APP"

Jalankan dengan:
    python app.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "frontend"))

from ui import main  # noqa: E402

if __name__ == "__main__":
    main()
