from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
LOGS = ROOT / "logs"
CONFIG = ROOT / "config" / "settings.json"

with CONFIG.open(encoding="utf-8") as f:
    SETTINGS = json.load(f)

for path in (PROCESSED, REPORTS, LOGS):
    path.mkdir(parents=True, exist_ok=True)
