# Step 2 — VeloNEMO v2 ontology extension (plan)

_Extends the v1 ontology into the v2 axes and grows its vocabulary from the review + guideline
corpus. Follows the two-track architecture in [schema_governance.md](schema_governance.md);
gated like every step (D-015). Decisions: [decision_log.md](decision_log.md) D-027._

## Goal
Turn v1 (validated in Step 1) into **VeloNEMO v2 TBox v0** by (a) formalizing the three v2 axes
— perspective, decision-structure, provenance — reusing standard ontologies, and (b) enriching the
criteria/metric vocabulary from the 22 reviews + 20 guidelines **without letting v1 bias discovery**.

## Two parallel mining tracks — the contrast is the rigor
Rather than choose schema-guided vs schema-blind mining (each risks anchoring on v1), run **both on
the same documents** and treat the delta as evidence:

- **Track G (guided):** mine reviews/guidelines **with** v1 vocab + the agreed axes as context →
  targeted proposals to extend/refine v1. (Track-G guidance is seeded from the agreed axes below.)
- **Track B (blind):** mine the **same** docs with **no v1, no target list** → open discovery of the
  field's constructs in their own words.
- **Contrast:** `G ∩ B` = robustly attested (add with confidence) · `B ∖ G` = what a v1-lens would
  **miss** → the anchoring-bias / blind-spot set (scientifically the interesting one) · `G ∖ B` =
  surfaced only because we prompted for it → possibly analyst-imposed, scrutinize before adding.

Same frozen protocol for both (EDC Extract+Define, K-sample self-consistency, definition-embedding
clustering — reuse Step-1 machinery + `baseline_evaluations` clustering; AutoSchemaKG/LKD-KGC-style
induction is appropriate *here only*, per the alternatives scan). Output = **v1-coverage vs field-
novelty** numbers + a curation report Ayda adjudicates.

## The v2 axes (what Track A formalizes in OWL)

**A1 · Study provenance (where/when).** `nemo:StudyArea` individual off `EvaluationMethod`
(`nemo:hasStudyArea`): verbatim area string + `owl:sameAs` Wikidata/GeoNames, `nemo:country`
(ISO-3166), `nemo:worldRegion` (EU·NA·… for the "EU vs NA indices differ" finding), `nemo:publicationYear`
(`xsd:gYear`). **City-size deferred** (D-027): the `StudyArea` node is minted now so population/
density/size-class can bolt on later without rework — no enrichment dependency in Step 2.

**A2 · Epistemic provenance (which source/model produced a claim).** **PROV-O**:
`prov:wasDerivedFrom` the source span, `prov:wasGeneratedBy` the extraction activity (model +
prompt-hash). Already implied by D-004/D-012; this names the standard. The auditability that earns
the KG its keep over RAG.

**A3 · Perspective — objective vs perceived (2-valued, D-027).** `nemo:perspective ∈ {objective,
perceived}` on the `Claim` (D-003), **grounded** by `nemo:dataModality` (GIS/sensor/CV/count →
objective; survey/interview/VR/eye-tracking → perceived). The normative/guideline voice is queryable
via **method-type** (`guideline` vs `primary`), so we keep the axis binary without losing the
"planners vs cyclists" cut. Operationalizes the perception gap: same criterion, two perspectives → a
SPARQL query.

**A4 · Decision structure — grounded in Cinelli et al. (2020) taxonomy.** Index-level:
`nemo:problemType` (c.1: description/scoring · classification/sorting e.g. LTS · ranking · choice),
`nemo:weightingMethod` (c.3.1.1: subjective/expert vs objective/data-driven · equal/none),
`nemo:compensation` (c.4.1: compensatory · partial · non-compensatory). Metric-level:
`nemo:orientation` (higher/lower/nonmonotonic), `nemo:normalization` (minmax/zscore/categorical/none).
Modeled as a small **SKOS ConceptScheme** of Cinelli terms — vocabulary, not a heavy import.
Step-1-style reality check: is this extractable from text or mostly `unknown`? (03-doc open question.)

**A5 · Hierarchies (two).** Criteria hierarchy via **SKOS `broader`** (Safety → Bikeability),
formalizing v1's `IndirectEvaluationCriterion` + the `Bikeability` umbrella (D-026) — this is exactly
Cinelli's c.2.1 *hierarchical criteria structure*. Metric composition via the existing
`nemo:composedOf` (index → component → leaf), made first-class — the direct fix for the D-025
granularity finding so both abstraction levels coexist.

## Minimal ontology stack (reuse-first, D-027)
Four external vocabularies, all standard and mostly already committed in v1 — no bespoke heavy imports:

| axis | reuse (existing) | new `nemo:` terms |
|---|---|---|
| concept governance + criteria hierarchy (A5) | **SKOS** (`prefLabel`/`altLabel`/`broader`) | — |
| epistemic provenance (A2) | **PROV-O** | — |
| place (A1) | **GeoSPARQL** `Feature` + `owl:sameAs` Wikidata/GeoNames, ISO-3166 | `hasStudyArea` |
| units | **OM** | — |
| year (A1) | `xsd:gYear` | `publicationYear` |
| decision structure (A4, Cinelli) | small SKOS ConceptScheme | `problemType`, `weightingMethod`, `compensation`, `orientation`, `normalization` |
| perspective (A3) | — | `perspective {objective,perceived}`, `dataModality` |

Net: **nemo (v1) + SKOS + PROV-O + GeoSPARQL + OM**.

## Concretes + deliverables
1. `step2_mine.py` — one frozen extractor run in **both modes** (G / B) over reviews + guidelines →
   candidate concepts (def, surface names, spans, frequency, K-stabilized).
2. `step2_contrast.py` — cluster + align G, B to v1 and each other → the `G∩B / B∖G / G∖B` report +
   coverage/novelty numbers for curation.
3. **Track A authoring** — axes into `ontology/nemo_onto_2.rdf` (stack above, Cinelli-cited) + update
   [extraction_schema.md](extraction_schema.md), validated against what mining finds.
4. Governance — `ontology/concept_registry.csv` + `ontology/CHANGELOG.md` + decision-log entries.

## Sequencing & access (D-027)
- **Guidelines: reviews-first, best-effort.** Run the 22 (mostly-OA) reviews now; add fetchable
  guidelines; log the rest as a manual-sourcing gap (CROW/NACTO often paywalled/DOI-less).
- Track A authoring runs in parallel but is **kept out of the Track-B prompt** so blind discovery stays
  unbiased. Nothing populates the full 541 corpus (Step 3) until v2 TBox v0 + schema are signed off.

## Open items for the mining to answer (don't pre-decide)
- Is decision-structure (A4) reliably extractable, or mostly `unknown` → human-assist field?
- Does the `B∖G` set contain genuinely new construct *types*, or just surface-name variants of v1?
- Registry as CSV + generated SKOS `.ttl` vs SKOS-in-OWL (05-doc open item) — decide when building.
