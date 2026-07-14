"""
VeloNEMO vocabulary — the COMPLETE ontology, read from `ontology/nemo_onto_2.rdf`.

Exposes everything that is in the ontology so nothing is hidden:
  * ALL_CLASSES        — every owl:Class (local name)
  * THEMATIC_TYPES     — the 6 metric classes directly under EvaluationMetric
  * METRICS_BY_TYPE    — {thematic type: [its specific metric classes]}   (the ~156 metrics)
  * METRICS            — flat sorted list of every specific metric class
  * CRITERIA           — subclasses of EvaluationCriterion
  * FEATURES           — subclasses of RepresentationFeature
  * SCALES             — instances of MeasurementScale
  * SUPPORT_CLASSES    — everything else (EvaluationMethod, DataSource, ScoringFunction,
                         Weight, Measure, Quantity, Unit, …)
  * PROPERTIES         — every object/data property (local name)
  * RELATIONS          — {property: {kind, domain, range}}  (the schema relations)
  * FIELD_PROPERTY     — extraction field -> grounding property (canonical = onto_manager.py)

Run `python velonemo.py` to print the whole vocabulary + all relations.
"""
from pathlib import Path
from rdflib import Graph, RDF, RDFS, OWL

ONTOLOGY_PATH = Path(__file__).resolve().parent / "ontology" / "nemo_onto_2.rdf"

_g = Graph().parse(ONTOLOGY_PATH)
_loc = lambda u: str(u).split("#")[-1].split("/")[-1]  # local name, any namespace


def _subclasses(parent: str) -> list[str]:
    return sorted({_loc(s) for s, o in _g.subject_objects(RDFS.subClassOf) if _loc(o) == parent})


def _instances(cls: str) -> list[str]:
    return sorted({_loc(s) for s, o in _g.subject_objects(RDF.type) if _loc(o) == cls})


def _dr(p) -> tuple[list[str], list[str]]:
    return ([_loc(x) for x in _g.objects(p, RDFS.domain)],
            [_loc(x) for x in _g.objects(p, RDFS.range)])


# ---- classes -------------------------------------------------------------
ALL_CLASSES = sorted({_loc(c) for c in _g.subjects(RDF.type, OWL.Class)})
THEMATIC_TYPES = _subclasses("EvaluationMetric")
METRICS_BY_TYPE = {t: _subclasses(t) for t in THEMATIC_TYPES}
METRICS = sorted({m for ms in METRICS_BY_TYPE.values() for m in ms})
CRITERIA = _subclasses("EvaluationCriterion")
FEATURES = _subclasses("RepresentationFeature")
SCALES = _instances("MeasurementScale")
_grouped = set(THEMATIC_TYPES) | set(METRICS) | set(CRITERIA) | set(FEATURES)
SUPPORT_CLASSES = sorted(c for c in ALL_CLASSES if c not in _grouped)

# ---- properties / relations ---------------------------------------------
_OBJ = {_loc(p) for p in _g.subjects(RDF.type, OWL.ObjectProperty)}
_DAT = {_loc(p) for p in _g.subjects(RDF.type, OWL.DatatypeProperty)}
PROPERTIES = sorted(_OBJ | _DAT)
RELATIONS = {}
for _p in sorted(set(_g.subjects(RDF.type, OWL.ObjectProperty)) |
                 set(_g.subjects(RDF.type, OWL.DatatypeProperty)), key=_loc):
    _d, _r = _dr(_p)
    RELATIONS[_loc(_p)] = {"kind": "object" if _loc(_p) in _OBJ else "data",
                           "domain": _d, "range": _r}

# ---- property grounding -----------------
# The OWL was reconciled to this namespace + property set on 2026-07-03.
PREFIX_NEMO = "http://www.ebikecityevaluationtool.com/ontology/nemo#"
PREFIX_OM = "http://www.ontology-of-units-of-measure.org/resource/om-2/"
_RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
_RDFS = "http://www.w3.org/2000/01/rdf-schema#"

FIELD_PROPERTY = {
    "raw_description": _RDFS + "comment",
    "thematic_type": _RDF + "type",
    "criteria": PREFIX_NEMO + "measures",
    "indirect_criteria": PREFIX_NEMO + "measures",
    "representation_feature": PREFIX_NEMO + "mapsToFeature",
    "measurement_scale": PREFIX_NEMO + "hasMeasurementScale",
    "unit": PREFIX_OM + "hasUnit",
    "buffer": PREFIX_NEMO + "measuredWithinBuffer",
    "aggregate_function": PREFIX_OM + "hasAggregateFunction",
    "scoring": PREFIX_NEMO + "hasScoringFunction",
    "weight": PREFIX_NEMO + "weightedBy",
    "data_source": PREFIX_NEMO + "hasSource",
    "parts": PREFIX_NEMO + "composedOf",
}

if __name__ == "__main__":
    print(f"ONTOLOGY: {ONTOLOGY_PATH.name}  ({len(_g)} triples, {len(ALL_CLASSES)} classes)\n")

    print(f"THEMATIC_TYPES ({len(THEMATIC_TYPES)}) and their metrics ({len(METRICS)} total): ")
    for t in THEMATIC_TYPES:
        ms = METRICS_BY_TYPE[t]
        print(f"\n  {t} ({len(ms)}): ")
        for m in ms:
            print(f"      {m}")

    print(f"\nCRITERIA ({len(CRITERIA)}): ")
    print("   ", ", ".join(CRITERIA))
    print(f"\nFEATURES ({len(FEATURES)}): ", FEATURES)
    print(f"SCALES ({len(SCALES)}): ", SCALES)
    print(f"\nSUPPORT_CLASSES ({len(SUPPORT_CLASSES)}): ")
    print("   ", ", ".join(SUPPORT_CLASSES))

    print(f"\nRELATIONS / PROPERTIES ({len(RELATIONS)}): ")
    for p, info in RELATIONS.items():
        d = "|".join(info["domain"]) or "?"
        r = "|".join(info["range"]) or "?"
        print(f"   [{info['kind'][:3]}] {p:24} {d} -> {r}")

    print(f"\nFIELD_PROPERTY (extraction field -> grounding property, {len(FIELD_PROPERTY)}): ")
    for k, v in FIELD_PROPERTY.items():
        print(f"   {k:24} -> {_loc(v)}")
