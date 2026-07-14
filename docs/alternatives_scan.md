# Alternatives scan — LLM-KGC method landscape (2025–2026)

_**Role of this file:** the related-work justification — which method each pipeline stage adopts
(EDC as the backbone, schema-induction only in governed spots, …) and what was considered and
rejected. Feeds the thesis methods chapter._

_Last updated 2026-07-03. Purpose: check whether better off-the-shelf options exist than the
ones named in the design doc (EDC, OntoMetric, AutoSchemaKG). The pipeline is the instrument,
not the contribution — so every stage should be off-the-shelf where possible._

## Given in the context folder
- **EDC — Extract, Define, Canonicalize** (Zhang & Soh, 2024). Open extraction → LLM writes a
  natural-language *definition* of each element → canonicalize/normalize against a target
  schema. **Directly relevant**: definition-based matching is exactly the design doc's ER
  stance ("match on definitions/formulas, never names"). Adopt EDC's Define step as the ER
  candidate-representation.
- **OntoMetric** (Yu et al., 2025). Ontology-driven, LLM-assisted framework for automated ESG
  **metric** KG generation. Nearest sibling: same shape (ontology of metrics + LLM population).
  Read for its schema-to-prompt derivation and validation setup.
- **Quintana et al., 2026 — Semantic Urban Elements**. Design-science paradigm; the design doc
  aligns the mid-level "composite urban index" framing to it.

## Fresh 2025–2026 options worth weighing
- **AutoSchemaKG** (arXiv 2505.23628). Dynamic *schema induction* from web-scale corpora;
  92% semantic alignment with human schemas, zero manual schema. **Relevance to us:** we do
  NOT want autonomous schema (we have an expert ontology to conform to) — but its induction
  machinery is exactly the right engine for the **`UnmodeledAssertion` escape hatch** (mine
  out-of-schema content, cluster it, feed human-governed schema revision). Use it there, not
  as the main extractor.
- **iText2KG** (incremental extract → dedup → fuse, schema-less, globally-unique entities,
  no post-hoc ER). **Relevance:** its incremental-dedup design is an alternative architecture
  to a separate ER stage; but "schema-less + auto-fuse" conflicts with claims-not-facts
  (we must *not* silently fuse — every merge must be an inspectable artifact). Borrow the
  incremental-index idea, reject the auto-fusion.
- **LKD-KGC** (Sun et al., 2025). Embedding-based schema integration: cluster equivalent
  entity types via vectors + LLM dedup. Same role as AutoSchemaKG for schema drift.
- **Blocking-based LLM entity matching** (OpenSanctions Pairs; "Cost-Efficient RAG for Entity
  Matching") — standard 3-step ER (block → match/group → merge/link). Confirms the design
  doc's embedding-candidate-gen + LLM-pairwise plan is mainstream; reuse patterns, don't invent.
- **LLM-KGC survey** (arXiv 2510.20345) — reference map for the field; cite for "generic
  pipeline is solved" claim.

## Takeaways for our design (aligned to D-006b, D-016, D-017)
1. **EDC is the backbone, split across steps** — Extract + Define (+ L1 abstraction) per paper
   at Step 1; Canonicalize deferred to Step 3 as entity resolution. Schema-aware, not
   schema-locked, so we don't blind ourselves to the diversity we exist to map. Use EDC's
   schema-canonicalization mode (align to the *existing* ontology), not auto-schema-induction.
2. **ER = deferred clustering over as-is claims**, on definitions/formulas never names:
   embedding candidate-gen + LLM pairwise adjudication + tiered confidence (auto-link /
   review-queue / keep-separate). Reuse `baseline_evaluations` semantic clustering. Standard,
   well-supported (blocking-based LLM matching literature).
3. **Reserve schema-induction tooling (AutoSchemaKG / LKD-KGC) for two governed places only**:
   the review-paper enrichment step (D-014 Phase A) and the `UnmodeledAssertion` → schema-
   revision loop — never the main population run.
4. Nothing found supersedes the plan; it is well-aligned with 2025–26 practice. Novelty stays
   in the expert ground truth + modelling-commitment target + generative task.

## Sources
- AutoSchemaKG — https://arxiv.org/abs/2505.23628
- LLM-empowered KGC survey — https://arxiv.org/pdf/2510.20345
- Cost-Efficient RAG for Entity Matching (blocking) — https://arxiv.org/pdf/2602.05708
- OpenSanctions Pairs (LLM entity matching) — https://arxiv.org/pdf/2603.11051
- KARMA multi-agent KG enrichment — https://openreview.net/pdf?id=k0wyi4cOGy
