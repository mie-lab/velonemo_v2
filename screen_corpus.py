"""
VeloNEMO v2 — Step 2: Corpus Screening & Flagging.

Takes manifest.jsonl and assigns each work two independent judgments via Gemini
over title + abstract:

  relevance : is this about a bikeability / cycling-network evaluation and metrics (an index,
              BLOS, LTS, suitability, compatibility score)? -> separates
              out-of-scope noise (e.g. bike-sharing logistics) from the rest.
  doc_type  : among the relevant ones, does the paper PROPOSE/BUILD an index
              (primary), REVIEW/COMPARE existing ones (review), or is it a
              practice/grey-literature guideline (guideline)?

Each judgment carries a 0-1 confidence band.

Paid tier (gemini-3.1-flash-lite). Paces under a self-imposed per-minute rate and is
RESUMABLE — already screened records are skipped on the next run, so an interrupted
run can be continued by simply rerunning.

Outputs (all under <out_dir>/screening/):

  manifest_screened.jsonl   The master log: one line per screened record, appended as we go.
                            This is the source of truth and the resume point — rerunning skips anything already in here.
  manifest_screened.jsonl split by `bucket`. Regenerated at every run:
    primary.jsonl       relevant + proposes/builds/applies an index  -> the corpus core
    review.jsonl        relevant + reviews/compares indices           -> survey papers
    guideline.jsonl     relevant + practice/grey-lit design norm      -> guidelines track
    needs_review.jsonl  low confidence either way                     -> human check queue
    excluded.jsonl      confidently out of scope                      -> dropped
  summary.txt               Per-bucket counts + a needs_review breakdown.

Requirements:
  pip install google-genai pydantic

For testing, set LIMIT var. When set to None - uses the full manifest.
"""

import json
import random
import time
import tomllib
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from google import genai
from google.genai import types
from google.genai import errors as genai_errors


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
CONFIG_PATH = Path(__file__).parent / "config.toml"

with open(CONFIG_PATH, "rb") as f:
    cfg = tomllib.load(f)

OUT_DIR = Path(cfg["paths"]["out_dir"])
MANIFEST_IN = OUT_DIR / "manifest.jsonl"
SCREEN_DIR = OUT_DIR / "screening"

SCREEN_DIR.mkdir(parents=True, exist_ok=True)
SCREENED_PATH = SCREEN_DIR / "manifest_screened.jsonl"

client = genai.Client(api_key=cfg["keys"]["gemini_api_key"])
MODEL = "gemini-3.1-flash-lite"

RPM_LIMIT = 150
MIN_INTERVAL = 60.0 / RPM_LIMIT
MAX_RETRIES = 8

# When None = full corpus run.
LIMIT = 500

# confidence routing
AUTO_INCLUDE_CONF = 0.75
AUTO_EXCLUDE_CONF = 0.75

BUCKETS = ("primary", "review", "guideline", "needs_review", "excluded")

RUBRIC = """You are screening academic papers for a research corpus about how \
bikeability and cycling-network EVALUATION instruments are constructed. The target \
phenomenon is a composite index or scoring scheme that rates how good a cycling \
network/environment is — e.g. a bikeability index, Bicycle Level of Service (BLOS), \
Level of Traffic Stress (LTS), bicycle suitability/compatibility score, or a \
multi-criteria evaluation of cycling infrastructure or cycling experience quality. \
The evaluation may be objective (measured from infrastructure/network data) or \
perceived (from ratings, stated preference, or experienced comfort/safety) — both \
are in scope; do not favour one over the other.

Given a title and abstract, return TWO independent judgments.

1) relevance: is the paper ABOUT such an evaluation instrument?
   - "relevant"      : the paper proposes, applies, reviews, validates, or critiques \
a bikeability-type index / BLOS / LTS / suitability score, OR the metrics & criteria \
used to evaluate cycling network quality.
   - "out_of_scope"  : bikeability/cycling is incidental — it merely appears in \
passing without the paper being about an evaluation instrument. Examples to EXCLUDE: \
bike-sharing fleet logistics or rebalancing, demand forecasting, health-outcome \
epidemiology, pure mode-choice econometrics, traffic-flow simulation, accident \
modelling.

2) doc_type (only meaningful if relevant; use "na" if out_of_scope):
   - "primary"   : the paper itself PROPOSES, BUILDS, or OPERATIONALIZES an index / \
scoring scheme, OR APPLIES a specific named index to a case study. (Proposing and \
applying are deliberately grouped here; if a paper does only one of the two and the \
other clearly does not apply, that is fine — still "primary".)
   - "review"    : the paper REVIEWS, SURVEYS, or COMPARES existing indices/metrics \
without contributing or applying an operational instrument.
   - "guideline" : the document is practice/grey literature — a design guideline, \
manual, or standard that functions as a plain-text evaluation scheme (e.g. CROW, \
NACTO, a national cycling design norm, a municipal evaluation report) rather than an \
academic study."""


class Judgment(BaseModel):
    relevance: Literal["relevant", "out_of_scope"]
    relevance_confidence: float
    doc_type: Literal["primary", "review", "guideline", "na"]
    doc_type_confidence: float
    reason: str


GEN_CONFIG = types.GenerateContentConfig(
    system_instruction=RUBRIC,
    response_mime_type="application/json",
    response_schema=Judgment,
    max_output_tokens=300,
    temperature=0,
)


def screen_one(rec):
    """Returns a dict of the judgment fields, plus a status."""
    title = rec.get("title") or ""
    abstract = rec.get("abstract") or "(no abstract available)"
    prompt = f"Title: {title}\n\nAbstract: {abstract}"
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.models.generate_content(
                model=MODEL, contents=prompt, config=GEN_CONFIG)
            return resp.parsed.model_dump(), True
        except genai_errors.ClientError as e:
            if getattr(e, "code", None) != 429:
                raise                                    # real error; rerun is free
            if "daily" in str(e).lower() or "perday" in str(e).lower().replace(" ", ""):
                return None, "DAILY_LIMIT"
            wait = min(2 ** attempt + random.random(), 60)
            print(f"    rate limited, backing off {wait:.1f}s ...")
            time.sleep(wait)
    raise RuntimeError(f"still rate-limited after {MAX_RETRIES} retries")


def route(rec):
    """Routes a screened record to a bucket based on its judgments and confidence scores."""
    rel = rec["relevance"]
    rc = rec.get("relevance_confidence", 0.0)
    dc = rec.get("doc_type_confidence", 0.0)
    if rel == "out_of_scope" and rc >= AUTO_EXCLUDE_CONF:
        return "excluded"
    if rel == "relevant" and rc >= AUTO_INCLUDE_CONF:
        if rec["doc_type"] in ("primary", "review", "guideline") and dc >= AUTO_INCLUDE_CONF:
            return rec["doc_type"]
        return "needs_review"
    return "needs_review"


def load_done_ids():
    """Loads the set of already-screened OpenAlex IDs from the master log, to skip on this run."""
    done = set()
    if SCREENED_PATH.exists():
        for line in SCREENED_PATH.open(encoding="utf-8"):
            try:
                done.add(json.loads(line)["openalex_id"])
            except (json.JSONDecodeError, KeyError):
                pass
    return done


def rebuild_splits():
    buckets = {k: [] for k in BUCKETS}
    for line in SCREENED_PATH.open(encoding="utf-8"):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue            # partial line from an interrupted run; skip
        buckets.get(r.get("bucket", "needs_review"), buckets["needs_review"]).append(r)
    for name, rows in buckets.items():
        with (SCREEN_DIR / f"{name}.jsonl").open("w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
    total = sum(len(v) for v in buckets.values())
    lines = [f"total screened: {total}", ""]
    for name in BUCKETS:
        lines.append(f"  {name:14} {len(buckets[name]):5d}")
    low_rel = sum(1 for r in buckets["needs_review"]
                  if r.get("relevance_confidence", 0) < AUTO_INCLUDE_CONF)
    lines += ["", "needs_review breakdown:",
              f"  uncertain relevance      : {low_rel}",
              f"  relevant, uncertain type : {len(buckets['needs_review']) - low_rel}"]
    summary = "\n".join(lines)
    (SCREEN_DIR / "summary.txt").write_text(summary, encoding="utf-8")
    return summary


def main():
    records = [json.loads(line) for line in MANIFEST_IN.open(encoding="utf-8")]
    done = load_done_ids()
    todo = [r for r in records if r["openalex_id"] not in done]
    print(f"Loaded {len(records)} records | already screened {len(done)} | "
          f"{len(todo)} remaining")
    if LIMIT is not None:
        todo = todo[:LIMIT]
        print(f"** TEST RUN: capped to {len(todo)} record(s) this run **")
    if not todo:
        print("Nothing to do. Rebuilding splits from existing log.")
        print("\n" + rebuild_splits())
        return

    calls = 0
    stopped_for_daily = False
    last = 0.0
    with SCREENED_PATH.open("a", encoding="utf-8") as fout:
        for rec in todo:
            wait = MIN_INTERVAL - (time.time() - last)
            if wait > 0:
                time.sleep(wait)
            last = time.time()

            judgment, status = screen_one(rec)
            if status == "DAILY_LIMIT":
                print("\nGemini daily quota hit. Stopping — progress saved, rerun tomorrow.")
                stopped_for_daily = True
                break

            rec.update(judgment)
            rec["bucket"] = route(rec)
            fout.write(json.dumps(rec) + "\n")
            fout.flush()
            calls += 1
            if calls % 25 == 0:
                print(f"  screened {calls} this run "
                      f"({len(done) + calls}/{len(records)} total) ...")

    print(f"\nThis run screened {calls} records.")
    print("\n" + rebuild_splits())
    remaining = len(records) - len(done) - calls
    if remaining > 0:
        print(f"\n{remaining} still unscreened — rerun the script to continue"
              f"{' (after quota resets)' if stopped_for_daily else ''}.")
    else:
        print("\nAll records screened. Hand-review needs_review.jsonl, "
              "then freeze primary.jsonl with a git tag.")


if __name__ == "__main__":
    main()