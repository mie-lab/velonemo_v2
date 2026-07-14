#!/usr/bin/env python
"""Step 2 — mine candidate ontology concepts from the review + guideline corpus, in TWO modes:

  B (blind)  — no VeloNEMO vocabulary in the prompt; open Extract+Define in the document's own terms.
  G (guided) — same document WITH v1 vocab + the agreed axes (criteria, thematic types, Cinelli 2020
               decision-structure, objective/perceived); reuse-or-mint against existing concepts.

Running both on the same docs lets the contrast (step2_contrast.py) quantify how much v1 would bias
discovery: G∩B robust · B∖G = v1-lens blind spots · G∖B = possibly analyst-imposed (D-027, docs/07).

Frozen protocol: K-sample self-consistency, same model as Step 1. PDFs are pre-fetched at
step2/pdfs/<openalex_id>.pdf; output at step2/extracted/<id>.<mode>.json. Idempotent (cached).
"""
import json, re, time, tomllib
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Optional
from pydantic import BaseModel
from pypdf import PdfReader
from google import genai
from google.genai import types
import velonemo as V

ROOT = Path(__file__).resolve().parent
STEP2 = ROOT / "step2"
for sub in ("pdfs", "parsed", "extracted", "report"):
    (STEP2 / sub).mkdir(parents=True, exist_ok=True)

cfg = tomllib.load(open(ROOT / "config.toml", "rb"))
client = genai.Client(api_key=cfg["keys"]["gemini_api_key"])
MODEL = "gemini-3.1-flash-lite"          # same model as Step 1 / corpus screening
K, TEMP = 3, 0.4                         # self-consistency: K samples, majority-vote (D-012)
MIN_INTERVAL = 1.0                       # seconds between LLM calls (rate limit)
FORCE = False                            # set True to re-mine (ignore cache)

REVIEW_JSONL = ROOT / "corpus" / "screening" / "review.jsonl"
GUIDELINE_JSONL = ROOT / "corpus" / "screening" / "guideline.jsonl"
CRITERIA = sorted(V.CRITERIA)
TYPES = sorted(V.THEMATIC_TYPES)
FEATURES = sorted(V.FEATURES)
SCALES = sorted(V.SCALES)
DECISION = ("problem type (scoring/description, classification/sorting, ranking, choice); "
            "weighting (subjective/expert vs objective/data-driven); "
            "compensation (compensatory, partial, non-compensatory); "
            "criteria structure (flat vs hierarchical)")     # Cinelli et al. 2020 taxonomy


# --------------------------------------------------------------------------- helpers
def key(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def strip_refs(t):
    m = list(re.finditer(r"(?im)^\s*(references|bibliography|works cited)\s*$", t))
    return t[:m[-1].start()] if m else t


def get_text(oaid):
    tp = STEP2 / "parsed" / f"{oaid}.txt"
    if tp.exists():
        return tp.read_text(encoding="utf-8")
    pdf = STEP2 / "pdfs" / f"{oaid}.pdf"
    if not pdf.exists():
        return None
    try:
        text = strip_refs("\n".join((p.extract_text() or "") for p in PdfReader(str(pdf)).pages))
    except Exception as e:                                                    # noqa
        print(f"  [{oaid}] parse error: {e}"); return None
    tp.write_text(text, encoding="utf-8")
    return text


# --------------------------------------------------------------------------- schema
class ConceptB(BaseModel):
    surface_name: str            # the term as the document writes it, verbatim
    concept_kind: str            # the model's OWN word for what role it plays (NOT a fixed list)
    composite: Optional[bool]    # for an indicator: true if built by combining other indicators
    group: Optional[str]         # the metric group/heading it falls under, if any (metrics only)
    definition: str              # ONE-sentence NL definition in the model's own words (the ER key)
    evidence: str                # short quote from the document


class ConceptG(BaseModel):
    surface_name: str
    concept_kind: str            # VeloNEMO dimension: criterion | metric | metric_group | data_modality |
                                 # representation_feature | scoring | weighting | aggregation | threshold | other
    composite: Optional[bool]    # metrics only: true if it combines other metrics (e.g. an index)
    group: Optional[str]         # the metric group it belongs to, if any (metrics only)
    definition: str
    evidence: str
    canonical_match: Optional[str]   # existing VeloNEMO concept it maps to BY MEANING, or null
    is_new: bool                     # true only if VeloNEMO does not already model it


class MiningB(BaseModel):
    concepts: List[ConceptB]


class MiningG(BaseModel):
    concepts: List[ConceptG]


PROMPT_B = """You are reading a REVIEW or GUIDELINE about how cycling networks are evaluated.
Inventory, in the document's OWN words, every distinct concept it uses to evaluate cycling networks.
Assume NO predefined schema — describe what the document itself contains.

For EACH concept give:
- surface_name: the term verbatim.
- concept_kind: what it IS / how it functions, in YOUR OWN words (do not pick from a fixed list).
- group: if the concept sits under a thematic heading/category, name that heading; else null.
- definition: one sentence in your own words.
- evidence: a short phrase copied VERBATIM (word-for-word) from the document — an exact anchor we can
  find in the text again, NOT a paraphrase or a summary.

Cast a wide net. Things worth capturing include — but are explicitly NOT limited to — the goals/qualities
a network is judged on; the indicators used to measure them (mark `composite`=true if an indicator is
built by combining several others, e.g. an index); how indicators are grouped into themes; the data or
method behind an indicator (survey, GIS, sensor, count…); the spatial unit an indicator applies to; and —
only if the document actually states them (rare in reviews) — how indicators are scored, weighted, or
combined. Capture anything else evaluation-relevant too; do not force concepts into these examples.

IMPORTANT — grouping applies to INDICATORS, not goals: indicators are often organized into thematic groups
(e.g. "Infrastructure", "Comfort"). Capture the group heading as its own concept AND each indicator under
it separately (set the member's `group`). Never collapse a group into one indicator.

Do NOT capture as concepts: the document's section/chapter titles, the review's own research methodology,
or its study region/year — these are not evaluation concepts.

List each concept once; prefer the document's own naming; do not invent concepts it does not discuss.

DOCUMENT:
{text}
"""

PROMPT_G = """You are extending the VeloNEMO cycling-evaluation ontology from a REVIEW or GUIDELINE.
For every evaluation concept the document uses, say which VeloNEMO dimension it belongs to and whether
VeloNEMO already models it or it is NEW.

VeloNEMO models (reuse these where they fit):
- criterion — a goal a metric measures: {criteria}
- metric — an indicator; mark composite=true if it combines other metrics (e.g. an index like BLOS/LTS).
- metric_group — the thematic TYPE that groups metrics (grouping applies to metrics, NOT criteria): {types}
- data_modality — HOW a metric is measured: GIS/OSM/sensor/camera/count/model (objective) vs
  survey/interview/rating (subjective). Capture the method.
- representation_feature — the spatial unit a metric applies to: {features}
- ONLY if the document explicitly states them (rare in reviews — reviews say WHICH factors matter, not HOW
  to combine them): scoring/normalization, weighting, aggregation, threshold.

For EACH concept give: surface_name (verbatim); concept_kind (criterion | metric | metric_group |
data_modality | representation_feature | scoring | weighting | aggregation | threshold | other);
composite (metrics only: true/false); group (the metric group it sits under, or null); a one-sentence
definition in your own words; evidence (a short phrase copied VERBATIM from the document, not
paraphrased); canonical_match (the EXISTING VeloNEMO concept it
matches BY MEANING, or null); is_new (true only if VeloNEMO does not already model it). Reuse existing
names where they fit; propose a new CamelCase name only for a genuinely new concept.

Do NOT extract: the document's chapter/section titles, the review's own methodology, or perspective
(objective/perceived) and provenance (location/year) — those are assigned per-claim at population, not here.

DOCUMENT:
{text}
"""


def consolidate(runs):
    """Keep concepts present in a majority of the K samples; vote concept_kind / is_new (D-012)."""
    thr = len(runs) // 2 + 1
    groups = defaultdict(list)
    for run in runs:
        for kk, c in {key(x["surface_name"]): x for x in run}.items():   # dedup within a sample
            groups[kk].append(c)
    out = []
    for cs in groups.values():
        if len(cs) < thr:
            continue
        c = dict(cs[0])
        c["concept_kind"] = Counter(x["concept_kind"] for x in cs).most_common(1)[0][0]
        if "is_new" in cs[0]:
            c["is_new"] = sum(bool(x.get("is_new")) for x in cs) > len(cs) / 2
        c["support"] = round(len(cs) / len(runs), 2)
        out.append(c)
    return out


# --------------------------------------------------------------------------- mine
def mine(oaid, bucket, text, mode):
    out = STEP2 / "extracted" / f"{oaid}.{mode}.json"
    if out.exists() and not FORCE:
        return json.loads(out.read_text(encoding="utf-8"))
    schema = MiningG if mode == "G" else MiningB
    prompt = (PROMPT_G.format(criteria=CRITERIA, types=TYPES, features=FEATURES, text=text)
              if mode == "G" else PROMPT_B.format(text=text))
    gen = types.GenerateContentConfig(response_mime_type="application/json",
                                      response_schema=schema, temperature=TEMP)
    runs = [client.models.generate_content(model=MODEL, contents=prompt, config=gen)
            .parsed.model_dump()["concepts"] for _ in range(K)]
    data = {"doc_id": oaid, "bucket": bucket, "mode": mode, "concepts": consolidate(runs)}
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"  [{oaid}.{mode}] {len(data['concepts'])} concepts (majority of {K})")
    return data


def main():
    docs = [("review", json.loads(l)) for l in open(REVIEW_JSONL, encoding="utf-8")] + \
           [("guideline", json.loads(l)) for l in open(GUIDELINE_JSONL, encoding="utf-8")]
    present = [(b, r) for b, r in docs if (STEP2 / "pdfs" / f"{r['openalex_id']}.pdf").exists()]
    print(f"{len(present)}/{len(docs)} docs have a PDF; mining B + G "
          f"({len(present) * 2} doc-passes, K={K})\n")
    last = 0.0
    for b, r in present:
        oaid = r["openalex_id"]
        print(f"[{oaid}] {b} · {r['title'][:60]}")
        text = get_text(oaid)
        if not text or len(text) < 500:
            print("  skip: no usable text"); continue
        for mode in ("B", "G"):
            if (STEP2 / "extracted" / f"{oaid}.{mode}.json").exists() and not FORCE:
                continue
            wait = MIN_INTERVAL - (time.time() - last)
            if wait > 0:
                time.sleep(wait)
            last = time.time()
            try:
                mine(oaid, b, text, mode)
            except Exception as e:                                            # noqa
                print(f"  [{oaid}.{mode}] error: {e}")
    print("\ndone -> step2/extracted/  (next: step2_contrast.py)")


if __name__ == "__main__":
    main()
