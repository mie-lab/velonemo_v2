# VeloNEMO v2 — Scaling Bikeability Knowledge Extraction with LLMs and Geospatial Knowledge Graphs

**Status: early development — no stable code or releases yet. Structure and APIs will change.**

VeloNEMO v2 is the scaled successor of [VeloNEMO](https://doi.org/10.1016/j.compenvurbsys.2024.102178), a formal ontology for harmonizing bike network evaluation metrics (Grisiute et al., 2024). Where v1 was a proof of concept built from a manually curated corpus of 25 papers, v2 extends the knowledge model and populates it automatically from a large heterogeneous document corpus using a schema-constrained LLM extraction pipeline.

## What v2 extends

The knowledge model grows along three axes:

- **Evaluation perspective**: explicit modeling of objective vs. perceived evaluations, replacing v1's `Perceived` name-prefix.
- **Decision structure**: an index's modelling commitments (metric orientation, normalization, weighting, compensation, spatial interdependence) as queryable entities.
- **Provenance**: geographic and temporal context of each evaluation, so commitments can be analyzed as spatio-temporally situated choices.

The model is designed in two layers: a generic mid-level model for **composite urban indices**, and a cycling-domain specialization. The same structure is intended to extend to walkability, liveability, and related index families.

## Planned repository structure

```
ontology/     VeloNEMO v2 (OWL) + validation shapes
extraction/   schema-constrained LLM extraction pipeline
resolution/   entity resolution and canonicalization
validation/   agreement scoring against the v1 ground truth
analysis/     queries and corpus-scale analyses
```

## Setup

```bash
conda env create -f environment.yml
conda activate velonemo2
```

## Related work

- Grisiute, A., Wiedemann, N., Herthogs, P., & Raubal, M. (2024). An ontology-based approach for harmonizing metrics in bike network evaluations. *CEUS*, 113, 102178. https://doi.org/10.1016/j.compenvurbsys.2024.102178

## Contact

Ayda Grisiute — Institute of Cartography and Geoinformation, ETH Zurich
