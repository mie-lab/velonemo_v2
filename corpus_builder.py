"""
VeloNEMO v2 — Step 1: OpenAccess Corpus Bootstrapper.

Builds a reproducible, metadata-grounded literature corpus from OpenAlex using a
combinatorial search strategy targeting composite urban indices.

Methodology:
  1. Combines structural evaluation terms (e.g., index, audit, MCDA) with targeted
     domain concepts via boolean intersections to maximize signal capture.
  2. Implements macro-level discipline screening at the API level by explicitly
     filtering out irrelevant academic fields (e.g., medical, material sciences).
  3. Generates a trackable provenance record for each work to isolate and measure
     structural differences across geographies, timelines, and evaluation objectives.

Outputs:
  <out_dir>/manifest.jsonl   Auditable line-delimited tracking JSON with inclusion paths.
  <out_dir>/pdfs/<id>.pdf    Local, rate-limited caching of open-access PDF targets.

Requirements:
  pip install pyalex requests
"""

import json
import time
import tomllib
from pathlib import Path
import requests
from pyalex import Works, config

# ---------------------------------------------------------------------------
# Configuration (config.toml — keep out of git, commit config.example.toml)
# ---------------------------------------------------------------------------

CONFIG_PATH = Path(__file__).parent / "config.toml"
with open(CONFIG_PATH, "rb") as f:
    cfg = tomllib.load(f)

config.email = cfg["openalex"]["email"]
if cfg["openalex"].get("api_key"):
    config.api_key = cfg["openalex"]["api_key"]

OUT_DIR = Path(cfg["paths"]["out_dir"])

YEAR_RANGE = (1995, 2026)
LANGUAGE = "en"

# ---------------------------------------------------------------------------
# Corpus Query
# ---------------------------------------------------------------------------
EVAL_TERMS = (
    "(index OR indices OR assessment OR evaluation OR audit OR quality "
    'OR "multi-criteria" OR multicriteria)'
)

SUBJECTS = [
    '"bikeability"',
    '"bike-friendliness" OR "bike friendliness" OR "bicycle friendliness"',
    '"bicycle level of service" OR "bike level of service" OR "cycling level of service"',
    '"bicycle compatibility" OR "bike compatibility"',
    '"bicycle suitability" OR "bike suitability"',
    '"level of traffic stress" AND (bicycle OR cycling OR bike OR cyclist)',
    '"bikeability potential" OR "bicycle potential"',
    '"bicycle network" OR "bike network" OR "cycling network"',
    '"bicycle infrastructure" OR "bike infrastructure" OR "cycling infrastructure"',
]

QUERIES = [f"({s}) AND {EVAL_TERMS}" for s in SUBJECTS]
EXCLUDE_FIELDS = "!fields/11|!fields/13|!fields/14|!fields/15|!fields16/!fields/19|!fields/24|!fields/25|!fields/27|!fields/29|!fields/30|!fields/31|!fields/34|!fields/35"


def work_record(w, query):
    oa = w.get("open_access") or {}
    best = w.get("best_oa_location") or {}
    return {
        "openalex_id": w["id"].rsplit("/", 1)[-1],
        "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
        "title": w.get("title"),
        "year": w.get("publication_year"),
        "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
        "is_oa": oa.get("is_oa", False),
        "oa_status": oa.get("oa_status"),
        "pdf_url": best.get("pdf_url"),
        "included_via": query,
        "cited_by_count": w.get("cited_by_count"),
        "screening_status": "pending",
    }


def run_query(q, records):
    pager = (
        Works()
        .search_filter(title_and_abstract=q)
        .filter(open_access={"is_oa": True})
        .filter(language=LANGUAGE)
        .filter(publication_year=f"{YEAR_RANGE[0]}-{YEAR_RANGE[1]}")
        .filter(primary_topic={"field": {"id": EXCLUDE_FIELDS}})
        .paginate(per_page=200)
    )
    n_new, n_total = 0, 0
    for page in pager:
        for w in page:
            n_total += 1
            r = work_record(w, q)
            if r["openalex_id"] not in records:
                records[r["openalex_id"]] = r
                n_new += 1
    print(f"  [query] {q[:80]}...  hits={n_total} new={n_new}")


def download_pdfs(records, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    for r in records.values():
        dest = outdir / f"{r['openalex_id']}.pdf"
        if not r.get("pdf_url") or dest.exists():
            continue
        try:
            resp = requests.get(r["pdf_url"], timeout=60)
            if resp.ok and resp.content[:4] == b"%PDF":
                dest.write_bytes(resp.content)
        except requests.RequestException:
            pass
        time.sleep(0.5)
    n = len(list(outdir.glob("*.pdf")))
    print(f"  [pdf] {n} PDFs in {outdir}")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    records = {}
    print("Running corpus queries...")
    for q in QUERIES:
        run_query(q, records)

    #print("\nDownloading OA PDFs...")
    #download_pdfs(records, OUT_DIR / "pdfs")

    manifest = OUT_DIR / "manifest.jsonl"
    with manifest.open("w") as f:
        for r in records.values():
            f.write(json.dumps(r) + "\n")

    by_query = {}
    for r in records.values():
        key = r["included_via"][:60]
        by_query[key] = by_query.get(key, 0) + 1
    print(f"\nManifest written: {manifest}")
    print(f"  total unique works: {len(records)}")
    for k, v in sorted(by_query.items(), key=lambda x: -x[1]):
        print(f"    {v:5d}  {k}...")
    print("Next: screening pass (LLM-assisted + human borderline review),")
    print("then freeze the manifest with a git tag before any extraction.")


if __name__ == "__main__":
    main()