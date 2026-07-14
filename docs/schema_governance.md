# Schema governance — how the ontology evolves, and where reviews feed in

_Answers: (a) a clear, trackable account of how concepts are added / renamed / merged /
deprecated over time; (b) how the "learn from review papers what to add to the ontology" step
is accommodated._

## The two-track architecture (matches the one-pager)

The one-pager shows two arrows into the KG: **Top-down Modelling** and **Bottom-up
Extraction**. We make that literal:

```
 TOP-DOWN (schema / TBox)                         BOTTOM-UP (population / ABox)
 v1 VeloNEMO ontology                             541 primary papers
   + enrichment from 22 reviews + 20 guidelines     │  EDC: Extract → Define → Canonicalize
   → VeloNEMO v2 TBox  (versioned, governed)  ◀──────┤            │
              │                                       │      canonicalize against
              └────────── frozen snapshot ───────────▶│      the frozen TBox snapshot
                                                       │            │
                    UnmodeledAssertion  ◀──────────────┘   unmatched concept candidates
                          │
                    human-governed review → new/updated concept → next TBox version
```

Reviews inform the **schema**; primaries fill **instances**; the escape hatch is the feedback
loop between them. This keeps population conforming to a stable target while letting the
schema grow deliberately.

## The review-paper enrichment step (Phase A, before/alongside population)

Reviews and guidelines enumerate the field's constructs more completely than any single
primary paper, so they are the right source for *vocabulary*, not instances.

1. Run EDC's Extract+Define over the 22 `review` + 20 `guideline` docs, but keep **only the
   concept vocabulary**: candidate criteria, metric families, decision-structure terms, each
   with its NL definition and the set of surface names used for it.
2. Cluster the candidate concepts (definition embeddings) and reconcile against v1's existing
   concepts. Each cluster becomes a **proposed concept** carrying: definition, surface-name
   variants, frequency across reviews, and source spans (provenance).
3. **Human curation** (Ayda): accept → mint concept; map → add as an alt-label of an existing
   concept; reject. Output = VeloNEMO v2 TBox v0 — a review-grounded target schema that
   *reduces how much later lands in the escape hatch*.

Guidelines (CROW/NACTO/national norms) are deliberately included here because they carry the
practice-side, more perceived-balanced vocabulary — countering the academic/objective corpus
skew (design doc §4.3). Population of guideline *instances* still happens in Phase B (they are
plain-text indices too, D-008).

## Concept tracking — the governance mechanics

Every concept change is **explicit, provenance-carrying, and never destructive.**

- **Stable URIs, never reused.** A concept URI is permanent. Renames change the label, not the
  URI. Removals use `owl:deprecated true` + `dcterms:isReplacedBy <newURI>`, so historical KG
  data still resolves.
- **SKOS lexical layer.** Each concept has one `skos:prefLabel` and many `skos:altLabel` — the
  full set of surface names seen (`LandUseMix` ← "land use mix", "mixed land use", "Shannon
  Land Use Mix Index"). This turns v1's manual name-unification into a *tracked, queryable*
  artifact and is what canonicalization writes back to.
- **Concept registry** (`ontology/concept_registry.csv`, append-only + git-tracked): one row
  per concept — URI, prefLabel, definition, parent, `first_seen` (paper/review), `created_in`
  ontology version, `status` (active|deprecated), `replaced_by`, and a definition-embedding
  centroid. This is the human-readable index of what exists and why.
- **Concept changelog** (`ontology/CHANGELOG.md`, append-only, ADR-style like the decision
  log): every add / rename / merge / split / deprecate with date + rationale + evidence.
  `git log` gives the full history; the changelog gives the *why*.
- **Semantic versioning of the TBox.** `MAJOR.MINOR.PATCH`: PATCH = definitions/labels,
  MINOR = new concepts (backward-compatible), MAJOR = merges/splits/deprecations that can
  invalidate existing claims. Every ontology release is a git tag.
- **Version-stamped claims.** Each Claim records the TBox version it was canonicalized
  against, so when the schema changes we know exactly which claims to re-canonicalize.
- **Drift is a first-class output, not just bookkeeping.** Because each concept keeps its
  definition-embedding centroid over time, "has *Safety* drifted since 2000?" (design doc's
  flagship construct-drift finding) is a query over the registry history, not a new study.

## What this gives us
A schema you can *audit*: for any concept you can see when it entered, from which document,
under what definition, which names collapse into it, and what it superseded — and every
population claim is pinned to the schema version that produced it. That auditability is a core
part of the "KG earns its existence over RAG" argument (design doc §1.3).

## Sequencing (resolved) + open item
- **Resolved (D-015):** Step 1 validates extraction on the existing v1 TBox first; Phase A
  (this doc's review enrichment) is **Step 2**, after we've seen real extraction behaviour and
  before the full 541-paper run.
- **Open:** registry/labels as CSV + SKOS-in-OWL vs. a small SKOS `.ttl`. (Leaning CSV for
  editing ease + a generated `.ttl`. Decide when we build Step 2.)
