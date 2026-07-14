# Extraction target schema (the interface contract) — draft v0

_The KG is the interface contract between LLM extraction and downstream reasoning. This is the
JSON the **Canonicalize** step must return per document (EDC, D-006b); it derives from the v1
`metrics.xlsx` row shape (D-001) + the three v2 axes, and encodes D-003 (perspective on the
claim), D-004 (`Claim` class), and D-012 (confidence vector)._

**Alignment to the v1 ground truth** (`context/metrics.xlsx`, 275 metrics × 17 cols) — so
validation against v1 is apples-to-apples: `label_verbatim`↔`EvaluationMetric`,
`definition`↔`Comment` (the Define output / ER key), `parts`↔`Parts`, `unit`/unit_type↔
`Unit`/`UnitType`, `measurement_scale`↔`MeasurementScale`, `buffer`↔`Buffer`/`BufferUnit`,
`representation_feature`↔`RepresentationFeature`, `CellSize`, `Function`, `scoring_function`↔
`ScoringFunction`, `thematic_type`↔`MetricType`, `criterion`↔`EvaluationCriterion`. New in v2:
`perspective`, `orientation`, `normalization`, index-level `decision_structure`, `provenance`,
and — reusing a v1 field that already exists — a criteria hierarchy via v1's
`IndirectEvaluationCriterion` (e.g. Accessibility→Bikeability).

## Shape (one JSON object per document)

```jsonc
{
  "method": {
    "id": "W4361011429",                 // openalex_id (URI stem); DOI kept too
    "doi": "10.3389/ffutr.2023.1127742",
    "index_name": "Cycling Network Quality Assessment",  // the instrument's own name, verbatim
    "title": "...", "year": 2023,
    "provenance": {                        // AXIS 3 — where/when the evaluation was produced
      "study_area": "Munich, DE",          // verbatim study area(s)
      "country": "DE", "region": "EU",     // normalized (may be inferred; mark inferred=true)
      "inferred": false
    },
    "decision_structure": {                // AXIS 2 — index-level modelling commitments (MCDA)
      "aggregation": "weighted_sum",       // weighted_sum | weighted_product | outranking | ML | rule_based | none
      "compensation": "compensatory",      // compensatory | partial | non_compensatory | unknown
      "weighting_method": "expert",        // equal | expert | data_driven | AHP | none | unknown
      "spatial_interdependence": "segment_independent" // segment_independent | network_dependent | unknown
    }
  },

  "metrics": [                             // v1 row shape + orientation/normalization (AXIS 2)
    {
      "mid": "m1",                         // local id, unique within this doc
      "label_verbatim": "Bike lane width", // the metric's NAME exactly as written in the paper
      "raw_description": "width of the cycling facility in metres, per segment",  // ≈ v1 `Comment`: RAW text/formula, verbatim from paper
      // ---- L1 ABSTRACTION (LLM does this per paper, mirroring metrics.xlsx cols; D-017) ----
      "canonical_name": "BikeLaneWidth",   // LLM's abstracted concept name (per-paper; L2/ER unifies across papers later)
      "definition": "width of the cycling facility in metres, per segment",  // cleaned canonical NL def (Define) — the ER key (D-005); match on THIS, never on label
      "thematic_type": "InfrastructuralMetric",  // one of v1's 6; or null → escape hatch
      "representation_feature": "Edge",    // Node|PointOfInterest|Edge|Route|GridCell|Area|Network
      "measurement_scale": "ratio",        // nominal|ordinal|interval|ratio|null
      "unit": "metre", "buffer": null, "buffer_unit": null,
      "data_source": "OpenStreetMap",
      "orientation": "higher_better",      // AXIS 2: higher_better|lower_better|nonmonotonic|unknown
      "normalization": "minmax",           // minmax|zscore|categorical_recode|none|unknown
      "weight": {"value": 0.2, "scheme": "expert"},   // null if unweighted
      "scoring_function": "linear",
      "parts": [],                         // composite: list of mids it is composed_of
      "inferred_fields": ["thematic_type","measurement_scale","orientation"]  // D-017: fields the LLM interpreted vs. found stated; inferred → lower confidence (D-012)
    }
  ],

  "claims": [                              // reified metric→criterion assertions (D-004)
    {
      "cid": "c1",
      "metric": "m1",                      // ref to metrics[].mid
      "criterion": "Safety",               // single criterion individual (D-003)
      "indirect_criterion": "Bikeability", // optional higher-level goal (v1 IndirectEvaluationCriterion)
      "perspective": "objective",          // objective | perceived  ← lives on the CLAIM (D-003)
      "confidence": {                      // 5-signal vector (D-012), not one self-report
        "extraction_selfreport": 0.9,      // weak aux
        "evidence_grounded": true,         // GATE: quote string-checked against source text
        "self_consistency": 0.67,          // agreement over k re-runs (filled by the k-replica pass)
        "canonicalization_similarity": 0.82// def-embedding cosine to matched concept (ER score)
        // shacl_valid added at the load/validation step
      },
      "evidence": {"page": 7, "quote": "bike lane width contributes to perceived safety..."}
    }
  ],

  "unmodeled": [                           // escape hatch (D-006): out-of-schema things worth keeping
    {"text": "authors weight segments by an eye-tracking salience score", "why": "no slot for perceptual-salience weighting"}
  ]
}
```

## Field → RDF mapping (load step, D-004)
- `method` → `nemo:EvaluationMethod` individual (URI = openalex_id); provenance +
  decision_structure as data properties (new v2 props: `nemo:aggregationType`,
  `nemo:compensation`, `nemo:weightingMethod`, `nemo:spatialInterdependence`,
  `nemo:studyArea`, `nemo:country`, `nemo:region`).
- each `metrics[]` → `nemo:EvaluationMetric` individual, `rdf:type` its `thematic_type`,
  v1 props (`mapsToFeature`, `hasMeasurementScale`, `hasSource`, `weightedBy`,
  `hasScoringFunction`, `measuredWithinBuffer`, `composedOf`) + new `nemo:orientation`,
  `nemo:normalization`, and `nemo:definitionText` (the ER key).
- each `claims[]` → a `nemo:Claim` individual with `nemo:claimMetric`, `nemo:claimCriterion`
  (`nemo:EvaluationCriterion` individual, single per construct), `nemo:perspective`,
  `nemo:extractionConfidence`, `nemo:fromSource` (method), `nemo:evidencePage`,
  `nemo:evidenceQuote`, plus model+prompt-hash provenance. The plain `measures` triple is
  *derived* from accepted claims for convenience querying, but the Claim is the source of truth.
- each `unmodeled[]` → `nemo:UnmodeledAssertion` linked to the method (feeds D-006 review).

## Open schema questions for the slice to answer (don't pre-decide)
- Is `decision_structure` reliably extractable from text, or mostly `unknown`? (If mostly
  unknown, it becomes an escape-hatch/human-assist field, not an auto field.)
- Does `orientation`/`normalization` live better at metric level or index level?
- Are single criterion individuals + perspective-on-claim (D-003) enough, or do real papers
  force a construct-identity distinction we can't express? (Revisit D-003 only with evidence.)
