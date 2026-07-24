"""
Download the four MEPS 2023 public-use files (Stata format) plus the CCSR
reference file, and unzip them into data/raw/.

Run from the project root:  python scripts/download_data.py
Total download is roughly 25 MB.
"""

import io
import zipfile
from pathlib import Path

import requests

# Resolve data/raw relative to this script, so it works no matter
# which directory you run it from.
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

MEPS_BASE = "https://meps.ahrq.gov/mepsweb/data_files/pufs"

# (zip URL, human-readable name) for each MEPS file.
# "dta" in the filename = Stata format, which pandas reads natively
# and which preserves category labels (e.g. "1 UNDER 65" instead of just 1).
MEPS_FILES = [
    (f"{MEPS_BASE}/h248e/h248edta.zip", "2023 ER Visits (HC-248E)"),
    (f"{MEPS_BASE}/h249/h249dta.zip", "2023 Medical Conditions (HC-249)"),
    (f"{MEPS_BASE}/h248i/h248idta.zip", "2023 Condition-Event Link (HC-248I)"),
    (f"{MEPS_BASE}/h251/h251dta.zip", "2023 Full-Year Consolidated (HC-251)"),
]

# CCSR reference file: maps condition category codes like "CIR007"
# to readable names like "Essential hypertension".
CCSR_URL = (
    "https://hcup-us.ahrq.gov/toolssoftware/ccsr/"
    "DXCCSR-Reference-File-v2026-1.xlsx"
)


def download_and_unzip(url: str, label: str) -> None:
    print(f"Downloading {label} ...")
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()  # stop with a clear error if the download failed
    # The zip arrives in memory (resp.content); extract it straight to disk.
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        zf.extractall(RAW_DIR)
        print(f"  extracted: {', '.join(zf.namelist())}")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for url, label in MEPS_FILES:
        download_and_unzip(url, label)

    # The CCSR file is optional — the notebook has a fallback if it's missing.
    print("Downloading CCSR reference file (condition category names) ...")
    try:
        resp = requests.get(CCSR_URL, timeout=120)
        resp.raise_for_status()
        (RAW_DIR / "ccsr_reference.xlsx").write_bytes(resp.content)
        print("  saved: ccsr_reference.xlsx")
    except requests.RequestException as err:
        print(f"  WARNING: CCSR download failed ({err}).")
        print("  The notebook will fall back to broad body-system labels.")

    print(f"\nDone. Files are in {RAW_DIR}")


if __name__ == "__main__":
    main()
