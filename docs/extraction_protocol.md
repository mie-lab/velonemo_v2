# Extraction protocol — EDC split across steps, confidence, consistency

_Answers three linked questions: (a) do we still use Extract-Define-Canonicalize? (b) how is
confidence measured? (c) how is every paper processed the same way. Governed by D-006b, D-012,
D-016, D-017._

## A. EDC — yes, but its three steps land in different roadmap steps

EDC stays the backbone. The key refinement (D-016): its steps do **not** all run at extraction
time. **Extract + Define run per paper now (Step 1); Canonicalize is deferred entity
resolution (Step 3).**

| EDC step | When | What it does here |
|---|---|---|
| **Extract** (open) | Step 1 | LLM pulls candidate metric / criterion / decision-structure mentions + verbatim spans, schema-aware but not schema-locked (captures out-of-schema diversity) |
| **Define** | Step 1 | LLM writes a canonical NL definition/formula per element = the v1 `Comment` column; this is the matching key — match on definitions, never names (D-005) |
| + **L1 abstraction** | Step 1 | Per paper, name + type + criterion + scale + feature — reproduces what the human `metrics.xlsx` columns encode (D-017). NOT merged across papers. |
| **Canonicalize** (= L2 / ER) | Step 3 | Cluster the accumulated as-is claims by definition similarity → converge stable concepts + explicit links; unmatched → `UnmodeledAssertion` → schema governance |

So Step 1 output is **as-is claims**: named and typed per paper, but never cross-paper-unified.
We use EDC's schema-canonicalization mode (align to the *existing* ontology), never its
auto-schema-induction mode. Structured outputs (JSON Schema) shape the returns; they do not
hard-gate Extract. Gemini stays the model (D-009). Detail on ER clustering:
the roadmap in the [root README](../README.md), Step 3; schema growth: [schema_governance.md](schema_governance.md).

## B. Confidence is a vector, and its signals phase in by step (D-012)

Self-reported LLM confidence alone is poorly calibrated, so it is never trusted standalone.
Each Claim (D-004) accumulates signals; which are available depends on the step.

| Signal | Type | Available | Meaning |
|---|---|---|---|
| `evidence_grounded` | bool, **gate** | Step 1 | verbatim quote string-checked against the parsed source; no locatable span → rejected (attacks faithfulness) |
| `shacl_valid` | bool, **gate** | Step 1 (load) | structural conformance; fail → rejected/queued |
| `self_consistency` | 0–1 | Step 1 | fraction of k≈3 re-runs in which this exact claim appears — the calibrated core signal; doubles as the §C consistency audit |
| `field_source` | stated / inferred | Step 1 | per-field flag (D-017); inferred fields carry less weight than stated ones |
| `extraction_selfreport` | 0–1 | Step 1 | model's own stated confidence — weak auxiliary only |
| `canonicalization_similarity` | 0–1 | **Step 3** | definition-embedding cosine to the matched concept — the ER-match score |

**Routing** reuses `screen_corpus.py`'s band→bucket pattern. *Step 1:* gates must pass, then
high self-consistency → accept; mid → review queue; unstable → flag. *Step 3:* adds
canonicalization-similarity to decide auto-link / review / keep-separate. Thresholds are tuned
once on the 15-paper slice against v1 ground truth, then frozen and versioned.

## C. Consistency — every paper processed identically

1. **Frozen extraction protocol**: one prompt template, one JSON schema, pinned Gemini version,
   `temperature=0` for the canonical pass (perturbation only for self-consistency replicas).
   Model id + prompt hash + schema version logged per claim → drift is auditable, any paper
   re-runnable bit-for-bit.
2. **v1 worked examples as few-shot anchors**: the paper's Appendix-B encodings
   (DestinationDensity; LandUseMix ≡ MixedLandUse ≡ Shannon Index; the two "Complexity"
   metrics) become few-shot exemplars, so the LLM reproduces the human's L1 interpretation
   conventions.
3. **Idempotent, resumable runs** (as screening already is): re-processing reproduces; no
   order-dependence.
4. **Consistency audit**: per-paper self-consistency (B) is logged; unstable claim-sets are
   flagged rather than trusted.
5. **Fixed target vocabulary** enforces *cross-paper* consistency — but that binds at Step 3,
   when Canonicalize resolves everything against one versioned ontology snapshot. At Step 1,
   consistency comes from items 1–4.

## Cost note
Extract + Define + k-replica self-consistency is more calls than one schema-locked pass; on the
slice this is negligible. At 541 papers, cap k=3, cache all responses (D-009), and if cost bites
run replicas only for claims that fail the cheaper gates.
