# Design decisions — current state

_One section per topic; inside each topic, the individual decisions keep their ID and a short
label so they can be referenced and revised one at a time. Blocks marked **Reporting** are not
decisions — they record results that motivated or de-risked a decision. New decisions get the
next free ID and join their topic. Full history: `git log -- docs/decision_log.md`.
Last consolidated: 2026-07-13._

| # | Topic | Project step |
|---|---|---|
| 1 | [Ways of working — corpus, governance, infrastructure](#1--ways-of-working--corpus-governance-infrastructure) | cross-cutting |
| 2 | [Knowledge model — Claims & perspective](#2--knowledge-model--claims--perspective) | model (populated at Step 3) |
| 3 | [v2 axes & ontology extension](#3--v2-axes--ontology-extension) | Step 2 (top-down) |
| 4 | [Extraction instrument](#4--extraction-instrument) | Steps 1–3 |
| 5 | [Step 1 — LLM-vs-human validation](#5--step-1--llm-vs-human-validation) | Step 1 · done |
| 6 | [Step 2 — review mining & contrast](#6--step-2--review-mining--contrast) | Step 2 · mining done, curation open |
| 7 | [Entity resolution](#7--entity-resolution) | Step 3 · deferred by design |
| 8 | [v1 data & vocabulary consistency](#8--v1-data--vocabulary-consistency) | cross-cutting |

---

## 1 · Ways of working — corpus, governance, infrastructure

**D-015 · One step at a time, validate before extending.** Each project step is one runnable
script, run on a fixed paper set, inspected and approved before the next step is built. In
particular, the extraction instrument was validated against the *existing* v1 ontology (Step 1)
before extending the ontology (Step 2) — extending first would have meant validating against a
moving, unvalidated target.

**D-008 · What each corpus bucket is for.** The screened corpus routes as follows: the 541
`primary` papers are the population corpus (they become knowledge-graph content); the 20
`guideline` documents are populated too, because they carry the practice-side and more
perception-balanced vocabulary; the 22 `review` papers are used only as a vocabulary source and
sanity check — never as population content; anything the screener was unsure about goes to a
human queue.

**D-013 · Schema governance.** The ontology may only change in ways that stay auditable: concept
URIs are permanent (a removed concept is marked deprecated and points to its replacement, its URI
is never reused); every surface name ever seen for a concept is kept as a SKOS label; every change
is written to `ontology/CHANGELOG.md` with its reason; releases follow semantic versioning; and
every extracted claim records which ontology version it was made against. This is what makes
questions like "has *Safety* drifted since 2000?" answerable as a query.

**D-006 · Escape hatch instead of a hard schema.** Extraction is schema-constrained, but content
that does not fit the schema is never forced into it or silently dropped — it goes to an
`UnmodeledAssertion` bucket, which is periodically clustered and reviewed by a human, who decides
whether the schema should grow. A hard schema would blind the pipeline to exactly the diversity
the project exists to map.

**D-009 / D-010 · Toolchain and hygiene.** Extraction runs on Gemini (one provider, the cheapest
path to results; the extractor is kept thin enough that a model comparison remains possible
later). Models are pinned, responses cached, prompts logged. API keys live only in gitignored
files (`config.toml`, `gemini_api_key.txt`; a placeholder `config.example.toml` is committed).
No PDFs and no corpus dumps in git. All Python runs in the `velonemo_v2` conda environment.
Publisher bot-walls are not circumvented — blocked PDFs are downloaded manually in a browser.
A triple store (GraphDB or Fuseki, with GeoSPARQL) is chosen but not yet set up.

**Working style (Ayda).** Prefer the simplest thing that works and avoid overfitting: no per-case
threshold tuning; when a distinction matters, record it as an explicit field rather than
engineering cluster or label boundaries to preserve it; keep the number of files minimal.

**D-033 · Workflow now, agency later.** The pipeline is deliberately a *workflow* with LLM
components — fixed control flow, frozen prompts, human gates — not an autonomous agent that plans
and decides its own next actions. The long-term intent IS agentic, but the technology is not yet
trusted enough for a scientific instrument whose argument rests on reproducibility: autonomy adds
nondeterminism exactly where the thesis needs repeatability. Agency is admitted only where it is
bounded and checkable (an LLM adjudicator for hard entity-resolution pairs at Step 3). Revisit
when the population run has shown the instrument stable at scale.

## 2 · Knowledge model — Claims & perspective

**D-004 · Claims, not facts.** The knowledge graph records *what documents claim* — and different
documents may disagree — rather than one reconciled truth. Every extracted assertion ("this paper
uses metric M to assess criterion C") is therefore stored as its own object, a **`Claim`**, which
can carry everything that belongs to that one assertion: which method poses it, what it links,
how it was measured, and how confident the extraction is. The shape:
`EvaluationMethod –posesClaim→ Claim`, `Claim –onMetric→ EvaluationMetric`,
`Claim –onCriterion→ EvaluationCriterion`, `Claim –viaModality→ DataModality`, plus
`extractionConfidence`. This follows the standard pattern for statements-about-statements
(n-ary-relation reification; the nanopublication paradigm for evidence-bearing scientific claims).

**D-003 · Perspective lives on the Claim, one hop.** Whether an evaluation is objective
(measured) or perceived (experienced) is an attribute of the *assertion*, not of the metric's
name: `Claim –hasPerspective→ Objective | Perceived`, where the two values are individuals of a
small class `EvaluationPerspective`. The Claim itself stays generic — perspective is one of its
attributes, never its type. This replaces v1's approach of encoding perception in class names
(`PerceivedSafety`, `ObjectiveSafety`, …): those 16 classes are deprecated and point to their base
concepts. There is also only ever *one* criterion individual per construct (a single `Safety`) —
the same criterion can simply be claimed from either perspective.
_Pending: `nemo_onto_3.rdf` still carries an earlier indirect wiring (perspective read through the
modality); the direct `hasPerspective` link is applied the next time the claim layer is touched._

**D-030a · Data modality is the method, and method ≠ viewpoint.** `DataModality` records *how* a
metric was measured — survey, interview, expert rating (subjective methods) or GIS, sensor,
count, camera (objective methods). It sits on the Claim (`viaModality`) and on the Metric
(`hasDataModality`, its typical method) and is the evidence that *justifies* a perspective. The
distinction matters: **subjective describes the method, perceived describes the viewpoint** — a
subjective method typically measures a perceived construct, but the two are separate fields.

**D-012 · Confidence is several signals, not one self-report.** An LLM's own confidence number is
uncalibrated, so each claim carries a small vector instead: does the quoted evidence actually
appear in the source text (a hard gate); did the same claim come back across repeated runs
(self-consistency — the most informative signal); how close is the definition to the matched
concept (embedding similarity); the model's self-report is kept only as a weak extra. Thresholds
are tuned once against the ground truth and then frozen, and the combined signals route each
claim: accept automatically, send to human review, or keep separate.

## 3 · v2 axes & ontology extension

**D-001 · Extend v1, never replace it.** The v1 ontology, spreadsheet shape and triple structure
remain the extraction target; v2 adds to them. This keeps every v2 result comparable with the v1
ground truth.

**D-027 · The v2 axes, and what deliberately stays out.** v2 adds: *perspective* (topic 2);
*provenance* — a `StudyArea` node per method (`studyAreaName`, `country`) plus `publicationYear`,
with city size deferred until a task actually needs it (the node makes it a cheap bolt-on later,
e.g. via `owl:sameAs` links to Wikidata); and a *criteria hierarchy* — `skos:broader`/`narrower`
between criteria (43 pairs derived from v1's `IndirectEvaluationCriterion` column, e.g.
Accessibility is narrower than Bikeability), which is exactly Cinelli's (2020) "hierarchical
criteria structure". **Deliberately not added here:** decision structure (problem type, weighting,
compensation — Cinelli's taxonomy) and per-metric commitments (orientation, normalization). Those
describe how an *individual index* combines metrics; reviews barely mention them (see topic 6
reporting), so they will be extracted from the 541 primary papers at Step 3. `isComposite` is not
a property either — being a subclass of `CompositeMetric` already says it.

**D-030 · Minimal reuse stack, authored additively.** The extension reuses only small, standard
vocabularies: SKOS (labels and the criteria hierarchy), GeoSPARQL (the metric's spatial
aggregation unit: `RepresentationFeature ⊑ geo:Feature`), OM (units, already in v1) and dcterms.
PROV-O was considered and dropped (nothing left needed it), as were evidence-quote/page properties
and `worldRegion`. Everything is authored **additively into a new file** `ontology/nemo_onto_3.rdf`
so the reconciled v1 file stays untouched; mined metric groups (e.g. "Land use") become subclasses
of the fitting thematic type during curation, not in bulk. All changes are recorded in
`ontology/CHANGELOG.md`; deprecating the `Perceived*` classes makes this a major version.

## 4 · Extraction instrument

**D-006b · EDC is the backbone.** EDC — *Extract, Define, Canonicalize* (Zhang & Soh 2024) — is a
three-move recipe for turning text into knowledge-graph content: **Extract** pulls out candidate
elements openly (not restricted to a fixed list, so field diversity survives); **Define** makes
the model write a one-sentence natural-language definition for each element it extracted;
**Canonicalize** aligns each element with the target vocabulary. The project uses all three, but
split across steps: Extract + Define happen at per-paper extraction time, and *the definition —
not the name — is the comparison key everywhere downstream* (validation matching, candidate
clustering, entity resolution), because the same concept hides behind different names across this
literature. Canonicalize is itself split: an inline, per-paper part (reuse-or-mint, next decision)
and the deferred cross-paper part (entity resolution, topic 7).

**D-021 · Reuse-or-mint naming.** The extraction prompt carries the full ontology vocabulary
(all ~200 metric names grouped by thematic type, plus criteria, features, scales). The model must
reuse an existing name whenever the metric matches one *by meaning*, and may coin a new
(CamelCase, singular) name only for a genuinely new metric, flagged `is_new`. This mirrors how the
human annotator worked, and the `is_new` flags are the signal for ontology gaps and future
entity-resolution candidates.

**D-012a · Self-consistency (K = 3).** Every document is extracted three times (temperature 0.4);
an element is kept only if a majority of runs agree, its fields are settled by majority vote, and
the agreement fraction is recorded as `support`. Single-pass extraction proved too noisy on
ambiguous fields; repetition separates noise from genuine disagreement.

**D-009a · Reproducibility of the instrument.** Model pinned (`gemini-3.1-flash-lite`, the same
model as corpus screening), output forced into a typed schema, all results cached and idempotent —
a document already processed is skipped, so reruns are cheap and adding documents processes only
the new ones.

**D-025 / D-032 · Extraction conventions are spelled out; type follows the ontology.** Some
conventions the human annotator used cannot be inferred from a paper, so the prompt states them
explicitly: the spatial feature is the index's *reporting* unit (not the raster it was computed
on); the measurement scale is the *raw* metric's scale (not the index's 1–10 scoring scale);
criteria come at two levels (specific goal + umbrella goal); named composite measures (LTS, BLOS)
*are* metrics, but a paper's overall index total or thematic bundle score is *not*; a
threshold-classification composite also yields its input attributes as metrics; and thematic
components are looked *inside* — the leaf metrics are extracted, not the component name. One
counter-lesson is part of this decision: a hand-written special-case rule ("Space Syntax measures
are Composite") turned out to contradict the ontology and was removed — **the thematic type always
follows the ontology's own grouped vocabulary**, and the Step-1 report keeps a silent check that
flags any ground-truth type that disagrees with the ontology, so this class of error cannot creep
back unnoticed.

## 5 · Step 1 — LLM-vs-human validation

**D-002 / D-011 · The validation set.** Step 1 asks one falsifiable question: *can the LLM
reproduce the human v1 extraction?* The test set is the 15 open-access papers of the 25-paper v1
ground truth (the other 10 are paywalled — a real open-access limit, not a bug). One script
(`step1_extraction_check.py`), artifacts under `step1/`; the ground truth is
`context/metrics.xlsx`, whose `Comment` column is the raw paper wording and whose other columns
are the human's abstraction of it.

**D-024 · Matching is lenient, by name OR by definition.** A model metric and a human metric
count as the same if their names are close, or if their *definitions* are close — measured both
lexically (string similarity) and semantically (embedding similarity, thresholds calibrated once
on real matched/non-matched pairs, then frozen). Definition-based matching exists because names
are unreliable in this field; it is a small preview of the entity-resolution machinery (topic 7).

**D-007 / D-022 · What is scored, and the anti-overfitting stance.** Scores are recall and
precision over metric identity, plus per-field agreement (thematic type, scale, spatial feature,
criteria) — each field scored *only where the human annotated it*, so a blank is never counted as
a disagreement. Disagreements are adjudicated by a taxonomy — LLM error vs. genuine field
ambiguity vs. legitimate alternative formalization — because raw agreement alone cannot tell model
failure from field messiness. The sparse extra fields (unit, aggregate, scoring, buffer, parts)
are reported for information only: they score low because the human used coded shorthand where the
model writes prose. Field-specific normalizers that would "fix" this were built, measured, and
**deliberately rejected** — they overfit the comparison to the ground truth's encoding instead of
measuring extraction. The real fix is a controlled vocabulary at population time.

**Reporting — outcome (context for D-027 and the Step-2 go-ahead, not itself a decision).**
Current result on the reconciled data, K = 3: recall 89 · precision 81 · type 94 · scale 84 ·
feature 80 · criteria 83. Residual disagreement is genuine ambiguity, not extraction failure.
What these runs taught, and where it flowed: the v1 ground truth is *not* gold (it contained real
labelling errors and granularity inconsistencies → the adjudication taxonomy above, and the data
repairs in topic 8); spatial representation is the hardest field because papers themselves are
spatially ambiguous (→ modeled carefully in v2); the index → component → variable hierarchy must
be explicit via `composedOf` so both abstraction levels can coexist (→ topic 3).

## 6 · Step 2 — review mining & contrast

**D-014 / D-027 · Two-track mining; the contrast is the rigor.** To grow the vocabulary without
letting v1 bias what is found, the 23 available review/guideline documents are mined **twice**
under the same frozen protocol: *guided* (the model sees the v1 vocabulary and reuses-or-mints
against it) and *blind* (no vocabulary — the document's own words). Comparing the two quantifies
anchoring bias instead of assuming it away: concepts found by both are robust; blind-only ones are
what the v1 lens would have hidden; guided-only ones may have been prompted into existence.

**D-029 · A lean concept scheme; perspective and provenance are not mined.** A first, fine-grained
14-facet scheme collapsed into noise (the model filed chapter titles and research methods as
concepts). The working scheme is five facets: criterion · metric (with a composite flag) ·
metric group (grouping applies to metrics only — criteria have their own goal hierarchy) · data
modality · spatial feature; scoring/weighting/aggregation/threshold are captured only when a
document states them explicitly. Perspective and provenance are *not* mining targets at all:
perspective is a property assigned per claim at population time, and provenance is paper metadata
— mining them from reviews only scraped noise.

**D-028 · Clustering kept deliberately simple.** Candidate concepts are grouped by exact name
first, then by one conservative pass of definition-embedding similarity. The similarity threshold
is treated as non-critical and is not tuned case by case (that would be overfitting); the facet
field and human curation carry the fine distinctions. "Robust" means attested in at least two
documents. **Curation is the only step that changes the ontology**: for each candidate — accept
(new concept), map (extra name for an existing concept), or reject — checking the model's
definition against the paper's quoted evidence.

**Reporting — outcome (informs D-027's deferral of decision structure, and validates v1's
vocabulary; not itself a decision).** The literature re-confirms 46 existing v1 concepts — the
criteria set appears essentially complete. Eleven robust novel candidates emerged, dominated by
exactly the two axes v2 set out to add (perspective and provenance), plus a few metrics and
sensing modalities. Anchoring bias measured ≈ 0: guided and blind mining agree on everything
well-attested. And a finding worth writing up: **reviews say *which* factors matter but not *how*
to combine them** — decision structure barely appears in 23 documents, which is why it will be
extracted from the primary papers at Step 3 (topic 3). Candidate curation
(`step2/report/candidates.csv`) is still open. For the eventual full-scale run: guided-only
(the bias check was a one-time question, now answered), lower K, drop the free-text fallback.

## 7 · Entity resolution

**D-016 · Deferred by design: represent everything first, then converge.** Nothing is merged at
extraction time — every paper's metrics are stored as-is, so raw extraction can be validated
before any unification is trusted. Entity resolution is its own later step (Step 3): cluster the
accumulated claims by definition similarity, adjudicate hard pairs with an LLM, and record the
outcomes as **explicit, inspectable equivalence links with tiered confidence** (auto-link / review
queue / keep separate) — never destructive merges (D-005). Matching is always on definitions and
formulas, never on names alone. The known duplicates inside v1 (LandUseMix ≡ "mixed land use" ≡
"Shannon land-use index"; the two "Complexity" metrics) are the evaluation set.

**D-017 · Two levels of abstraction.** The model performs **L1** abstraction per paper — turning
the raw description into a named, ontology-typed concept, exactly what the human's spreadsheet
columns encode. **L2** — unifying those concepts *across* papers — is entity resolution and is
deferred as above. Fields the model inferred rather than found stated are flagged, and inferred
fields carry lower confidence (feeds D-012).

## 8 · v1 data & vocabulary consistency

**D-018 / D-019 / D-020 · One reconciled v1.** The three v1 artifacts — the OWL ontology
(`ontology/nemo_onto_2.rdf`), the ground-truth spreadsheet (`context/metrics.xlsx`) and the
published knowledge graph (`context/metrics.nq`) — are the canonical copies and are kept mutually
consistent; every repair is applied to all affected files, with `.bak` backups. Concretely: the
property vocabulary follows the published KG (`measures`, `mapsToFeature`, `hasScoringFunction`,
`weightedBy`, `composedOf`, …) under the `…/ontology/nemo#` namespace, and the OWL was migrated to
match; names are singular everywhere; 17 spelling near-duplicates were unified; every class the KG
instantiates is declared in the OWL. Current counts: ~275 classes · 201 metrics · 35 criteria ·
7 features · 4 scales. `velonemo.py` loads this vocabulary and is the single access point for all
scripts.

**D-026 · Criteria gaps closed.** Four criterion labels the spreadsheet used had no home in the
OWL: `Bikeability`, `BicycleFriendliness` and `Performance` were added as criterion classes, and a
name collision around `Coverage` (a metric, used once as a criterion) was resolved in the
spreadsheet.

**D-031 / D-032 · Thematic types reconciled; one deliberate double role.** A full scan found and
fixed every type disagreement between the three artifacts: all Space-Syntax measures
(`Connectivity`, `Depth`, `Integration`, `Choice`) are `GraphMetric`; `DetourFactor` and
`SeparatedBikeLaneDensity` are `MorphologicalMetric`; the never-used `ConnectivityMetric` class
was deleted. `Connectivity` deliberately remains **both** a metric and a criterion — the two
classes disambiguate the two senses. Verified: zero mismatches remain, and the Step-1 report keeps
a silent flag that would surface any new one.

**Known quirk, accepted for now.** The spreadsheet's `unit` column mixes the counted entity with
the dimensional unit (e.g. `rightTurn,route`); validation does not force-match it, and a proper
controlled vocabulary for units is a v2 population-time item.
