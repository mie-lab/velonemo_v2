# VeloNEMO v2 — Project Understanding (synthesis)

_**Role of this file:** the shared mental model — why the project exists, what v1 was, what v2
adds, where the novelty is. Read this first; it changes rarely. Mechanics live in the step docs,
choices in [decision_log.md](decision_log.md)._

_Last updated: 2026-07-03. Reconstructed from the context folder, the v1 paper + repo, and the v2
design document; correct anything that is wrong._

## 1. One-paragraph framing

The dissertation's thesis is that the cycling **"perception gap"** (planners' normative
"good network" vs. cyclists' lived experience) is the cumulative product of rarely
examined assumptions — **semantic** (how quality is represented), **measurement** (which
data modality is used), and **cognitive** (how routes are mentally aggregated). VeloNEMO v2
attacks the *semantic* assumption at corpus scale: it turns the manually-built v1 ontology
+ 25-paper KG into an automatically-populated knowledge graph of **how bikeability is
*constructed*** across the whole literature — not just which metric measures which
criterion, but under which **evaluation perspective** (objective vs. perceived), which
**decision structure** (orientation, normalization, weighting, compensation, spatial
interdependence), and **where/when** each evaluation was produced.

## 2. What v1 already is (the reusable substrate)

**Ontology (VeloNEMO v1)** — namespace `http://www.ebikecityevaluationtool.com/ontology/nemo#`.
Core classes: `EvaluationMethod` (paper/guideline/tool; DOI as URI), `EvaluationMetric`
(+6 thematic subclasses: `Infrastructural/Contextual/Morphological/Mode/Graph/Composite`),
`EvaluationCriterion` (Safety, Comfort, Accessibility… aligned to Triple-A 2nd-level goals),
`RepresentationFeature` (Node, PointOfInterest, Edge, Route, GridCell, Area, Network →
geoSPARQL `Feature`), `Weight`, `ScoringFunction`, `MeasurementScale` (nominal/ordinal/
interval/ratio), `DataSource`. Units delegated to **OM**; geometry to **geoSPARQL**;
cardinality units to **GCI**.
Key properties: `usedIn` (metric→method), `measures` (metric→criterion), `assessedIn`
(criterion→method), `mapsToFeature`, `measuredWithinBuffer`, `weightedBy`,
`hasScoringFunction`, `hasMeasurementScale`, `hasSource`, `composedOf`.

**Concrete v1 code** (`mie-lab/bike_network_evaluation`): a spreadsheet (`metrics.xlsx`,
one row per metric with columns EvaluationMetric, MetricType, EvaluationMethod,
EvaluationCriterion, MeasurementScale, ScoringFunction, Unit/UnitType, Function, Parts,
RepresentationFeature, Buffer/BufferUnit, Comment) → `metrics_to_nquads.py` emits N-Quads
against `onto_manager.py` constants. **This spreadsheet-to-nquads shape is essentially the
target schema of the LLM extractor** — the LLM's job is to fill that row structure (plus
the v2 extensions) from paper text instead of a human doing it by hand.

**v1's own stated limitations** (from the paper's future-work section, all directly
targeted by v2): (a) `Perceived`-prefix is too simplistic for objective/subjective;
(b) no semantic hierarchy among criteria; (c) manual → small corpus (25 papers);
(d) no provenance/trust modeling.

## 3. What v2 adds (three extension axes)

1. **Evaluation perspective** — objective vs. perceived as explicit structure, replacing
   the `Perceived` name-prefix.
2. **Decision structure** — an index's modelling commitments (metric orientation,
   normalization, weighting type, degree of compensation, spatial interdependence) as
   first-class queryable entities. Vocabulary from MCDA taxonomies (Cinelli et al., 2020).
3. **Provenance** — geographic + temporal situation of each evaluation → trend / transfer /
   drift analyses.

**Two-layer architecture**: a generic **mid-level model for composite urban indices** +
a **cycling domain layer** (VeloNEMO v2). Claim: a walkability researcher only writes a new
domain layer. Cheap proof: extract 3–5 walkability indices (e.g. Walk Score) into the same
mid-level model.

## 4. Where the defensible novelty is (per design doc)

The generic "LLM → schema-typed KG → validate" pipeline is **not** novel in 2026. The novelty:
- **A rare expert ground truth**: the hand-curated v1 KG is a *semantically ambiguous
  real-domain* benchmark (one metric → many criteria; same name → different constructs).
  The *validation question itself* is the contribution.
- **Extracting modelling commitments, not entity-relation facts** — meta-scientific
  extraction (closer to PICO study-design extraction than standard IE).
- **KG-grounded generative design** — synthesizing a provenance-grounded index blueprint
  from planning objectives.
- **Corpus-scale meta-scientific findings** — e.g. how "safety" operationalization drifted
  over time; how EU vs. NA indices differ structurally.

## 5. Current pipeline state (what already runs in this repo)

- `corpus_builder.py` — OpenAlex combinatorial search → `corpus/manifest.jsonl` (4422 works).
- `screen_corpus.py` — Gemini flash-lite screens title+abstract into two judgments
  (relevance; doc_type ∈ primary/review/guideline) with confidence routing →
  `corpus/screening/{primary,review,guideline,needs_review,excluded}.jsonl`.
  Current split: **primary 541, review 22, guideline 20, needs_review 10, excluded 3829.**
- Not yet built: PDF/table parsing, extraction, ontology v2 (OWL), entity resolution,
  triple store loading, SPARQL/QA, validation against v1.

## 6. The four tasks (from the one-pager diagram)

Descriptive ("which metrics measure safety?"), Comparative ("how does safety differ across
regions / over time?"), Evaluative ("how structurally similar are two indices? outliers?"),
Generative ("what index blueprint fits these planning goals?"). Validation is
**author-in-the-loop against the manually-extracted v1 KG (~25–30 papers)**.

## 7. The null hypothesis v2 must beat

Long-context RAG / GraphRAG over the same corpus. The KG earns its existence via:
exhaustive aggregation (exact SPARQL counts), auditable entity resolution, per-span
provenance, and compositionality for the generative task. An explicit
**KG-QA vs. GraphRAG vs. long-context** experiment is part of the plan.

## 8. Ground-truth artifacts (canonical copies live in `context/`)

The canonical v1 artifacts to build against are **inside** `nemo_2/context/` (self-contained;
do not use the sibling `../nemo/` copies):
- `ontology/nemo_onto_2.rdf` — the v1 ontology (newest, Mar 2024). **Source of truth for the
  extraction vocabulary**, loaded by `velonemo.py` (6 thematic types, 32 criteria, 7 features,
  4 scales, 15 properties). Note: its Protégé default namespace is `…/untitled-ontology-25/`,
  different from the KG's `…/nemo#`; vocab is matched by local class name.
- `context/metrics.xlsx` — **275 metrics × 17 cols**, the human-encoded source of the v1 KG.
  Columns: EvaluationMetric, EvaluationMethod, **Comment** (= raw description/formula, the ER
  key), Parts, Unit, MeasurementScale, UnitType, Buffer, BufferUnit, RepresentationFeature,
  CellSize, Function, ScoringFunction, MetricType, EvaluationCriterion,
  **IndirectEvaluationCriterion** (a criteria hierarchy, e.g. Accessibility→Bikeability).
- `context/metrics.nq` — the v1 KG (single named graph, UUID instance URIs + blank nodes;
  v2 replaces blank nodes with explicit `Claim` individuals).
- `../baseline_evaluations/` (sibling) — the "Rethinking Bikeability" ANP/MCDA code: loads the
  KG into **Blazegraph**, does semantic clustering of criteria/metrics
  (`*_semantic_clustering.ipynb`) — reusable for Step-3 ER candidate-generation.

Implication: the v2 "novel" axes (perspective, decision-structure, criteria-hierarchy) are
**not alien** to the v1 data — Comment/IndirectEvaluationCriterion/expert Weight already gesture
at them, which de-risks extraction and keeps validation apples-to-apples.

---
See [decision_log.md](decision_log.md) for choices + open forks,
[extraction_protocol.md](extraction_protocol.md) (EDC + confidence + consistency),
[schema_governance.md](schema_governance.md) (concept tracking + review enrichment), and
[alternatives_scan.md](alternatives_scan.md) for the 2025–2026 method landscape.
