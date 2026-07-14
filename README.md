# VeloNEMO v2 — an LLM-populated knowledge graph of how bikeability is constructed

**Status: active development (thesis project). Structure and APIs will change.**

VeloNEMO v2 scales [VeloNEMO](https://doi.org/10.1016/j.compenvurbsys.2024.102178) — a formal
ontology for harmonizing bike-network evaluation metrics, hand-built from 25 papers (Grisiute et
al., 2024) — into an automatically populated knowledge graph covering the whole literature. The
goal is not only *which metric measures which criterion*, but **how bikeability is constructed**:
under which evaluation **perspective** (objective vs. perceived), with which **decision structure**
(weighting, aggregation, compensation), and **where/when** each evaluation was produced. This
supports the dissertation's core question: the cycling "perception gap" between planners' normative
evaluations and cyclists' lived experience.

## The agentic workflow

An LLM does the reading; humans set the rules and make every change that matters. Each step is one
runnable script, run under a **frozen protocol** (pinned model, fixed prompts, K-sample
self-consistency, cached results — every document treated identically, every run repeatable), and
**gated by human inspection** before the next step is built:

```
   build 1 script ──▶ run on the fixed paper set ──▶ inspect output ──▶ GATE: adequate?
        ▲                                                                   │
        └────────────── refine (schema / prompt / thresholds) ◀─────────────┘ no
                                                                             │ yes
                                                                        next step
```

```
Step 0  BUILD & SCREEN THE CORPUS (done)                          corpus_builder.py · screen_corpus.py
        OpenAlex search (4 422 works) → LLM screens title+abstract into buckets:
        primary 541 · review 22 · guideline 20 · needs_review → human queue

Step 1  VALIDATE THE INSTRUMENT (done)                            step1_extraction_check.py
        Can the LLM reproduce the human v1 extraction? The 15 open-access papers of
        the v1 ground truth, extracted by the LLM (guided by the ontology vocabulary,
        reuse-or-mint) and compared to the human — matched by name OR definition
        (lexical + semantic similarity).
        GATE: does the LLM recover what the human did? → PASSED:
        recall 89 · precision 81 · type 94; residual gaps are genuine ambiguity,
        not extraction failure.

Step 2  EXTEND THE ONTOLOGY (mining done · curation open)         step2_mine.py · step2_contrast.py
        Reviews + guidelines are mined for candidate concepts TWICE — blind (no
        vocabulary) and guided (with v1) — and the contrast measures whether the v1
        lens biases discovery (it doesn't: bias ≈ 0). Clustered candidates are aligned
        to v1 and handed to HUMAN CURATION — the only step that changes the ontology.
        The v2 axes (perspective, provenance, criteria hierarchy) are authored into
        ontology/nemo_onto_3.rdf.
        GATE: Ayda curates step2/report/candidates.csv → accepted concepts enter the
        v2 ontology (governed: changelog, versioning, stable URIs).

Step 3  POPULATE & RESOLVE (planned)
        Extract claims from the 541 primary papers into the v2 model (each assertion a
        reified Claim with modality, perspective, confidence), then entity resolution
        as deferred clustering — explicit equivalence links, never silent merges.
        GATE: evaluate ER on v1's known duplicates (LandUseMix ≡ "mixed land use" ≡
        "Shannon land-use index").

Step 4+ SCALE & TASKS (later)
        Descriptive / comparative / evaluative / generative analyses over the KG;
        KG-QA vs. GraphRAG baseline (the null hypothesis the KG must beat).
```

Feedback edges: Step-1 disagreements are adjudicated (LLM error vs. field ambiguity vs. legitimate
alternative formalization) and feed what Step 2 should add; unmatched concepts at any step go to
the `UnmodeledAssertion` escape hatch and re-enter schema governance; the ontology version is
frozen per extraction run and every claim is stamped with it.

## Repository map

| Step | Script(s) | Data | Doc | Output |
|---|---|---|---|---|
| 0 | `corpus_builder.py`, `screen_corpus.py` | `corpus/` | — | `corpus/screening/*.jsonl` |
| 1 | `step1_extraction_check.py` | `step1/` | [docs/step1_validation.md](docs/step1_validation.md) | `step1/report/` |
| 2 | `step2_mine.py`, `step2_contrast.py` | `step2/` | [docs/step2_ontology_extension.md](docs/step2_ontology_extension.md) | `step2/report/`, `ontology/nemo_onto_3.rdf` |
| — | `velonemo.py` — loads the ontology vocabulary; the single access point for all scripts | `ontology/`, `context/` | — | — |

## Documentation (`docs/`)

| Read this… | …to understand |
|---|---|
| [project_understanding.md](docs/project_understanding.md) | **the why** — motivation (perception gap), what v1 is, what v2 adds, where the novelty is |
| [decision_log.md](docs/decision_log.md) | **the choices** — one self-contained decision per topic (ways of working · claims model · v2 axes · extraction instrument · Step-1 validation · Step-2 mining · entity resolution · data consistency) |
| [step1_validation.md](docs/step1_validation.md) | Step 1 — the fixed 15-paper validation set |
| [step2_ontology_extension.md](docs/step2_ontology_extension.md) | Step 2 — two-track mining, v2 axes, minimal reuse stack |
| [extraction_schema.md](docs/extraction_schema.md) | the JSON contract the extractor returns (+ mapping to v1 columns / RDF) |
| [extraction_protocol.md](docs/extraction_protocol.md) | EDC across steps, the confidence signal vector, cross-paper consistency |
| [schema_governance.md](docs/schema_governance.md) | how the ontology evolves: changelog, versioning, escape hatch |
| [alternatives_scan.md](docs/alternatives_scan.md) | the LLM→KG method landscape — what was adopted and what rejected, and why |
| [ontology/CHANGELOG.md](ontology/CHANGELOG.md) | ontology releases — every TBox change with rationale (semver) |

## Ontology (`ontology/`) and source materials (`context/`)

`ontology/` holds the evolving artifact: `nemo_onto_2.rdf` (the reconciled v1 — **source of truth
for the extraction vocabulary**), `nemo_onto_3.rdf` (v1 + the authored v2 axes), and the
`CHANGELOG.md`. `context/` holds the source materials the pipeline draws on:

- `metrics.xlsx` — the human v1 extraction (275 rows); the **ground truth** for Step 1.
- `metrics.nq` — the published v1 knowledge graph.
- Method papers the design is grounded in: Zhang & Soh 2024 (EDC — the extraction backbone),
  Yu et al. 2025 (OntoMetric), Cinelli et al. 2020 (MCDA taxonomy → decision-structure vocabulary),
  Quintana et al. 2026; plus the v1 paper and the thesis one-pager (project framing).

## Where we are / what's open

- **Done:** corpus built + screened; Step 1 validated the instrument; Step 2 mining + contrast ran
  (v1's criteria confirmed essentially complete; anchoring bias ≈ 0); the v2 axes authored; all v1
  artifacts (OWL ↔ xlsx ↔ nq) reconciled.
- **Open:** Step-2 candidate curation (`step2/report/candidates.csv`); apply the direct
  `hasPerspective` claim wiring to `nemo_onto_3.rdf`; then Step 3.

## Setup

```bash
conda env create -f environment.yml        # env: velonemo_v2
# add your Gemini key to config.toml (see config.example.toml) — never committed
python step1_extraction_check.py           # rerun the Step-1 validation (cached, idempotent)
python step2_mine.py && python step2_contrast.py   # rerun the Step-2 mining + contrast
```

## Related work

- Grisiute, A., Wiedemann, N., Herthogs, P., & Raubal, M. (2024). An ontology-based approach for
  harmonizing metrics in bike network evaluations. *CEUS*, 113, 102178.
  https://doi.org/10.1016/j.compenvurbsys.2024.102178

## Contact

Ayda Grisiute — Institute of Cartography and Geoinformation, ETH Zurich
