"""Generate BSC Designer JSON files from the CSVs in data/.

Each data/<indikator>.csv (columns: bulan,value with bulan = YYYY-MM)
becomes api/<indikator>/<YYYY-MM>.json containing {"value": ..., "name": ...},
the format BSC Designer's HTTP data source reads.
"""
import csv
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"
API = ROOT / "api"


def parse_number(raw: str) -> float:
    s = raw.strip().replace(" ", "")
    # Format Indonesia: 4.931.164.624,50 -> 4931164624.50
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})+(,\d+)?", s):
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", "")
    n = float(s)
    return int(n) if n.is_integer() else n


def main() -> None:
    if API.exists():
        shutil.rmtree(API)
    index = {}
    for path in sorted(DATA.glob("*.csv")):
        slug = path.stem
        name = slug.replace("_", " ").title()
        out_dir = API / slug
        out_dir.mkdir(parents=True)
        months = []
        with path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                month = row["bulan"].strip()
                if not re.fullmatch(r"\d{4}-\d{2}", month):
                    raise ValueError(f"{path.name}: bulan '{month}' harus format YYYY-MM")
                value = parse_number(row["value"])
                body = json.dumps({"value": value, "name": name})
                yyyy, mm = month.split("-")
                # yyyy-MM (2026-04) dan MM.yyyy (04.2026), dua format yang bisa dipilih di BSC
                for fname in (f"{month}.json", f"{mm}.{yyyy}.json"):
                    (out_dir / fname).write_text(body, encoding="utf-8")
                months.append(month)
        index[slug] = {"name": name, "bulan": months}
        print(f"{slug}: {len(months)} bulan")
    (API / "index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
