from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "dados"
BRONZE_DIR = ROOT / "data" / "bronze"
SILVER_DIR = ROOT / "data" / "silver"
GOLD_DIR = ROOT / "data" / "gold"
REPORT_DIR = ROOT / "reports"
TABLES = ("funcionarios", "departamentos", "filiais")
REFERENCE_DATE = "2026-01-01"
