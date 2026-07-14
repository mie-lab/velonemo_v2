# VeloNEMO ontology — changelog

Append-only, ADR-style. Semantic versioning: PATCH = labels/defs · MINOR = new concepts (backward-
compatible) · MAJOR = merges/splits/deprecations that can invalidate existing claims (D-013, docs/05).

---

## v2.0.0 — 2026-07-05 · MAJOR · file `ontology/nemo_onto_3.rdf` (D-030)
First v2 TBox. Extends the reconciled v1 (`nemo_onto_2.rdf`) with the three evaluation axes. Authored
additively (v1 file untouched); +242 triples.

**Added — classes (4):** `Claim`, `EvaluationPerspective` (⊑ skos:Concept), `DataModality`
(⊑ skos:Concept), `StudyArea`.

**Added — object properties (7):** `posesClaim` (Method→Claim), `onMetric` (Claim→Metric),
`onCriterion` (Claim→Criterion), `viaModality` (Claim→DataModality), `hasDataModality`
(Metric→DataModality), `ofPerspective` (DataModality→Perspective), `hasStudyArea` (Method→StudyArea).

**Added — data properties (4):** `publicationYear` (on EvaluationMethod), `studyAreaName` + `country`
(on StudyArea), `extractionConfidence` (on Claim).

**Deferred to Step 3 (NOT added in v2, per Ayda):** the metric-commitment / decision-structure properties
`orientation`, `normalization`, `problemType`, `weightingMethod`, `compensation` describe how an
*individual index* combines metrics — that comes from the 541 primary implementation papers, not this
top-down review step (reviews don't attest it; see D-028/D-029). `isComposite` dropped as redundant:
`CompositeMetric` is already a subclass of `EvaluationMetric`.

**Added — individuals (13):** perspectives `Objective`, `Perceived`; modalities `GISBased`,
`RemoteSensing`, `FieldSensor`, `CameraVision`, `TrafficCount`, `ModelDerived`, `InstrumentedProbeBike`,
`SmartLightSensor` (→ Objective), `SurveyStated`, `InterviewStated`, `ExpertRated` (→ Perceived).

**Added — alignment:** `RepresentationFeature ⊑ geo:Feature` (GeoSPARQL — the metric aggregation unit).

**Added — criteria hierarchy:** 43 `skos:broader` + `skos:narrower` pairs derived from v1's
`IndirectEvaluationCriterion` column (e.g. `Accessibility ↔ Bikeability`).

**Deprecated (16) — MAJOR:** all `Perceived*` / `Objective*` prefix classes → `owl:deprecated true` +
`dcterms:isReplacedBy` the base concept where one exists (e.g. `PerceivedSafety → Safety`,
`ObjectiveSafety → Safety`). Perception now lives on the `Claim` via its `DataModality`'s perspective
(D-003), not in the metric name.

**Reuse:** SKOS · GeoSPARQL · OM (units, existing) · dcterms. PROV-O intentionally not used.

**Pending:** repoint `velonemo.py` to v3 after review; add curated metric-group subclasses and new metrics
from `step2/report/candidates.csv`; update `docs/extraction_schema.md`; add `concept_registry.csv`.
