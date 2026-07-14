# Step 1 — the 15-paper validation set (the "slice")

_Step 1's fixed evaluation set: the papers the LLM extraction is validated against. Artifacts live in
the `step1/` folder (`step1/pdfs`, `step1/extracted`, `step1/report`). Step sequence lives in
the [root README](../README.md); this doc just defines the set and why._

## Paper set: v1 ground-truth ∩ open-access PDF

Each paper overlaps the manually-extracted v1 KG, so we get **validation-against-v1 for free**
on exactly these documents (D-007, D-011). The set grew from an initial 8 to **15** as more of the
25 v1 papers were sourced (10 remain paywalled). Deliberate spread of index kinds → good
perspective / decision-structure diversity.

| # | key | openalex_id | kind |
|---|-----|-------------|------|
| 1 | beecham2023 | W4353080938 | connectivity / graph |
| 2 | hardinghaus2021 | W3207880534 | GIS + survey index |
| 3 | hsu2023 | W4319011370 | hybrid model |
| 4 | krenn2015 | W2220486709 | GIS + survey index |
| 5 | schmidquerg2021 | W3118359258 | GIS + survey index |
| 6 | weikl2023 | W4361011429 | data-driven quality |
| 7 | santos2022 | W4291123807 | MCDA suitability |
| 8 | ito2021 | W3161486144 | street-view / CV |
| 9 | abad2018 | W2901426564 | Level-of-Traffic-Stress classification |
| 10 | daraei2021 | W2911593481 | routing / comfort |
| 11 | boisjoly2019 | W2941312659 | accessibility / detour |
| 12 | reggiani2021 | W3169192492 | relative-discomfort model |
| 13 | soltani2022 | W4220966335 | Space Syntax |
| 14 | karolemeas2022 | W4226421486 | MCDA suitability |
| 15 | codina2022 | W4310059561 | composite index |

## What Step 1 does on the slice (see roadmap for the gate)
Fetch the 15 PDFs → parse text (drop references) → per-paper **as-is** extraction with K=3
self-consistency (Extract + Define + L1 abstraction, D-017; no cross-paper merging) →
`step1/extracted/<openalex_id>.json` against the [extraction schema](extraction_schema.md) →
match vs the human `metrics.xlsx` rows (name/definition, lexical + semantic, D-024) → an agreement
report we inspect together.

## Explicitly NOT on the slice yet
Full 541-paper run; entity resolution / clustering (Step 3); OWL formalization of the v2 axes;
SPARQL task queries; the generative task; the GraphRAG baseline. Each is a later step, once the
slice shows the shape of real extractions.
