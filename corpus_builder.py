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

Requirements:
  pip install pyalex
"""

import json
import tomllib
from pathlib import Path
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

# Fields to drop (medical, chemistry, materials, etc.). OpenAlex parses `|` as OR,
# so `!11|!13` means "not 11 OR not 13" — true for every work. To exclude a set you
# must AND the negations, i.e. apply one negated filter per field (see run_query).
EXCLUDE_FIELDS = [11, 13, 14, 15, 16, 19, 24, 25, 27, 29, 30, 31, 34, 35]


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
        "abstract": reconstruct_abstract(w.get("abstract_inverted_index")),
        "screening_status": "pending",
    }


def reconstruct_abstract(inv_index):
    """OpenAlex returns abstract_inverted_index: {word: [positions]}."""
    if not inv_index:
        return None
    positions = {}
    for word, idxs in inv_index.items():
        for i in idxs:
            positions[i] = word
    return " ".join(positions[i] for i in sorted(positions))


def run_query(q, records):
    pager = (
        Works()
        .filter(title_and_abstract={"search": q})
        .filter(open_access={"is_oa": True})
        .filter(language=LANGUAGE)
        .filter(publication_year=f"{YEAR_RANGE[0]}-{YEAR_RANGE[1]}")
    )
    for fid in EXCLUDE_FIELDS:                       # AND the negations
        pager = pager.filter(**{"primary_topic.field.id": f"!fields/{fid}"})
    pager = (
        pager.select([
            "id", "doi", "title", "publication_year",
            "primary_location", "open_access", "best_oa_location",
            "cited_by_count", "abstract_inverted_index",
        ])
        .paginate(per_page=200, n_max=None)
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


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    records = {}
    print("Running corpus queries...")
    for q in QUERIES:
        run_query(q, records)

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