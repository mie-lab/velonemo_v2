#!/usr/bin/env python
"""Step 2 contrast — cluster the mined candidate concepts (B blind + G guided), align each to v1, and
report the G∩B / B∖G / G∖B split plus v1-coverage vs novelty (D-027, docs/07). The contrast quantifies
how much the v1 lens biases discovery: B∖G that is NOVEL = concepts blind mining found but guided missed.

Reads step2/extracted/*.{B,G}.json → writes step2/report/step2_candidates.md + candidates.csv.
"""
import json, re, csv, tomllib
from pathlib import Path
from collections import defaultdict, Counter
from google import genai
import velonemo as V

ROOT = Path(__file__).resolve().parent
STEP2 = ROOT / "step2"
cfg = tomllib.load(open(ROOT / "config.toml", "rb"))
client = genai.Client(api_key=cfg["keys"]["gemini_api_key"])
EMBED_MODEL = "gemini-embedding-001"
SEM = 0.88                                  # def-embedding cosine to merge two candidates (conservative: over-splitting is safe for curation, over-merging hides concepts)
MIN_DOCS = 2                                # "robust" = attested in ≥ this many documents


def key(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())

# cache of definition embeddings (text -> embedding vector)
_emb = {}


def embed(texts):
    todo = [t for t in dict.fromkeys(texts) if t and t not in _emb]
    for i in range(0, len(todo), 100):
        b = todo[i:i + 100]
        for t, e in zip(b, client.models.embed_content(model=EMBED_MODEL, contents=b).embeddings):
            _emb[t] = e.values


def cos(a, b):
    if not a or not b:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / ((sum(x * x for x in a) ** .5) * (sum(y * y for y in b) ** .5) or 1)


# v1 vocabulary for alignment: key -> canonical name
V1 = {}
for nm in list(V.CRITERIA) + list(V.THEMATIC_TYPES) + list(V.FEATURES) + list(V.SCALES) + list(V.METRICS):
    V1[key(nm)] = nm

# coarse facet buckets for free-text B kinds (G kinds are already facets)
# facet vocabulary matches step2_mine.py's lean scheme (G facets are clean; FACET_KW only maps B free-text)
FACETS = ("criterion", "metric", "metric_group", "data_modality", "representation_feature",
          "scoring", "weighting", "aggregation", "threshold", "other")
FACET_KW = {"metric_group": ["group", "domain", "thematic", "category", "theme"],
            "metric": ["indicator", "metric", "measure", "index"],
            "criterion": ["criteri", "goal", "quality", "principle", "requirement"],
            "data_modality": ["objective ind", "subjective ind", "survey", "sensor", "gis", "camera",
                              "modality", "perceiv", "measured data"],
            "representation_feature": ["spatial", "unit of analysis", "resolution", "segment", "feature"],
            "scoring": ["scor", "normali"], "weighting": ["weight"],
            "aggregation": ["aggregat", "combin"], "threshold": ["threshold"]}


def facet_of(kind):
    kind = (kind or "").lower()
    if kind in FACETS:
        return kind
    for f, kws in FACET_KW.items():
        if any(k in kind for k in kws):
            return f
    return "other"


def _sentence(text, spans, i, k):
    """The source sentence spanning word-indices i..k (crude '.'-boundary, good enough for a snippet)."""
    s = text.rfind(".", 0, spans[i][1]) + 1
    e = text.find(".", spans[k][2])
    return re.sub(r"\s+", " ", text[s:(len(text) if e < 0 else e + 1)]).strip()[:300]


def ground(quote, text, spans, toks, first_index):
    """Snap the model's evidence to a VERBATIM span of the source: find the longest word-run of the
    quote that occurs word-for-word in the text (tolerating a couple of leading paraphrase words and
    all punctuation/case/hyphenation differences), and return the sentence containing it.
    → (source_sentence, True) if found; (original_quote, False) if the quote is not in the text."""
    qw = re.findall(r"[a-z0-9]+", (quote or "").lower())
    if len(qw) < 4:
        return quote, False
    for j in range(min(3, len(qw) - 3)):               # allow a little leading junk before the anchor
        for L in range(len(qw) - j, 3, -1):            # longest verbatim anchor first
            a = qw[j:j + L]
            for i in first_index.get(a[0], ()):        # only positions of the anchor's first word
                if toks[i:i + L] == a:
                    return _sentence(text, spans, i, i + L - 1), True
    return quote, False


def load():
    """Pool all mined concepts and GROUND each one: locate the longest verbatim anchor of its evidence
    quote in the parsed source, and REPLACE the evidence with the actual source sentence — so the stored
    quote comes from the text, not the model (D-012's evidence-grounding gate, deterministic, no LLM).
    `grounded=False` = the quote could not be found verbatim (paraphrased or invented)."""
    docs, items = {}, []
    for p in sorted((STEP2 / "extracted").glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        doc = d["doc_id"]
        if doc not in docs:
            tp = STEP2 / "parsed" / f"{doc}.txt"
            text = tp.read_text(encoding="utf-8") if tp.exists() else ""
            spans = [(m.group().lower(), m.start(), m.end()) for m in re.finditer(r"[A-Za-z0-9]+", text)]
            fi = defaultdict(list)
            for i, (w, _, _) in enumerate(spans):
                fi[w].append(i)
            docs[doc] = (text, spans, [w for w, _, _ in spans], fi)
        text, spans, toks, fi = docs[doc]
        for c in d["concepts"]:
            src, grounded = ground(c.get("evidence"), text, spans, toks, fi)
            items.append({**c, "doc_id": doc, "bucket": d["bucket"], "mode": d["mode"],
                          "evidence": src if grounded else c.get("evidence"), "grounded": grounded})
    return items


def _centroid(members):
    es = [m["_emb"] for m in members if m.get("_emb")]
    return [sum(c) / len(es) for c in zip(*es)] if es else None


def cluster(items):
    """Exact surface-name buckets first (so identical names never fragment), then greedy-merge the
    buckets by centroid definition-embedding cosine ≥ SEM."""
    texts = [it.get("definition") or it["surface_name"] for it in items]
    embed(texts)
    buckets = defaultdict(list)
    for it, tx in zip(items, texts):
        it["_emb"] = _emb.get(tx)
        buckets[key(it["surface_name"])].append(it)
    groups = [{"members": ms, "keys": {k}, "emb": _centroid(ms)} for k, ms in buckets.items()]
    groups.sort(key=lambda g: -len({m["doc_id"] for m in g["members"]}))
    merged = []
    for g in groups:
        for cl in merged:
            if cl["emb"] and g["emb"] and cos(cl["emb"], g["emb"]) >= SEM:
                cl["members"] += g["members"]; cl["keys"] |= g["keys"]; cl["emb"] = _centroid(cl["members"]); break
        else:
            merged.append(g)
    return merged


def summarize(cl):
    ms = cl["members"]
    gm = [m for m in ms if m["mode"] == "G"]
    rep = Counter(m["surface_name"] for m in ms).most_common(1)[0][0]
    facet = Counter(facet_of(m["concept_kind"]) for m in (gm or ms)).most_common(1)[0][0]
    docs = {m["doc_id"] for m in ms}
    modes = {m["mode"] for m in ms}
    # v1 alignment: prefer a G canonical_match, else lexical hit against v1 vocab
    cand = [m.get("canonical_match") for m in gm if m.get("canonical_match")]
    v1 = Counter(cand).most_common(1)[0][0] if cand else None
    if not v1:
        for m in ms:
            if key(m["surface_name"]) in V1:
                v1 = V1[key(m["surface_name"])]; break
    seg = "G∩B" if modes >= {"B", "G"} else ("B∖G" if "B" in modes else "G∖B")
    defn = next((m.get("definition") for m in ms if m.get("definition")), "")
    ev = next((m.get("evidence") for m in ms if m.get("evidence")), "")
    variants = sorted({m["surface_name"] for m in ms}, key=str.lower)
    groups = sorted({m["group"] for m in ms if m.get("group")}, key=str.lower)
    return {"name": rep, "facet": facet, "v1": v1, "novel": v1 is None, "segment": seg,
            "n_docs": len(docs), "n_B": sum(m["mode"] == "B" for m in ms),
            "n_G": sum(m["mode"] == "G" for m in ms), "variants": variants, "groups": groups,
            "grounded": sum(bool(m.get("grounded")) for m in ms) / len(ms),
            "definition": defn, "evidence": ev, "docs": sorted(docs)}


def main():
    items = load()
    clusters = [summarize(c) for c in cluster(items)]
    clusters.sort(key=lambda c: (-c["n_docs"], c["facet"], c["name"].lower()))
    n = len(clusters)
    robust = [c for c in clusters if c["n_docs"] >= MIN_DOCS]     # attested in ≥2 docs
    novel_r = [c for c in robust if c["novel"]]
    novel_s = [c for c in clusters if c["novel"] and c["n_docs"] < MIN_DOCS]
    seg = Counter(c["segment"] for c in robust)
    bias = [c for c in robust if c["segment"] == "B∖G" and c["novel"]]
    covered = {c["v1"] for c in clusters if c["v1"]}

    L = ["# Step 2 — candidate concepts (blind B vs guided G, aligned to v1)\n",
         f"_{len(items)} raw concepts → **{n} clusters** ({len(robust)} attested in ≥{MIN_DOCS} docs) · "
         f"merge = same name OR definition-embedding cosine ≥ {SEM} · v1 via G canonical_match or lexical._\n",
         "## Headline (robust = attested in ≥2 docs; singletons are the 1-doc tail, see CSV)",
         f"- **v1 coverage:** mining re-found **{len(covered)}** existing v1 concepts.",
         f"- **Novel candidates not in v1: {len(novel_r)} robust** (+ {len(novel_s)} singletons) — robust by facet: "
         + ", ".join(f"{k} {v}" for k, v in Counter(c['facet'] for c in novel_r).most_common()) + ".",
         f"- **Track split (robust):** G∩B {seg['G∩B']} (both) · B∖G {seg['B∖G']} (blind-only) · "
         f"G∖B {seg['G∖B']} (guided-only).",
         f"- **Anchoring-bias signal:** **{len(bias)}** robust novel concepts were found by BLIND mining but "
         f"MISSED by guided — the v1 lens would have hidden them: "
         + ", ".join(f"`{c['name']}`" for c in bias[:12]) + ".",
         f"- **Evidence grounding:** {sum(bool(i['grounded']) for i in items) / len(items):.0%} of raw "
         f"concepts carry a quote verbatim-findable in their source text (normalized substring check). "
         f"Ungrounded ones are paraphrased or hallucinated quotes — scrutinize during curation "
         f"(`grounded` column in the CSV).\n"]

    by_facet = defaultdict(list)
    for c in clusters:
        by_facet[c["facet"]].append(c)
    for f in FACETS:
        cs = by_facet.get(f)
        if not cs:
            continue
        rc = [c for c in cs if c["n_docs"] >= MIN_DOCS]
        ns = [c for c in cs if c["n_docs"] < MIN_DOCS and c["novel"]]     # novel singletons = curation tail
        show = rc + ns
        L.append(f"## {f}  ({len(rc)} robust, {len(ns)} novel-singletons / {len(cs)} total)")
        for c in show:
            tag = f"→v1:{c['v1']}" if c["v1"] else "**NOVEL**"
            star = "⭐ " if c["n_docs"] >= MIN_DOCS else ""
            grp = f" · grp: {', '.join(c['groups'][:2])}" if c["groups"] else ""
            L.append(f"- {star}**{c['name']}** [{c['segment']}] docs={c['n_docs']} {tag}{grp}")
            if len(c["variants"]) > 1:
                L.append(f"    variants: {', '.join(c['variants'][:8])}")
            L.append(f"    _{(c['definition'] or '')[:140]}_")
        if len(cs) > len(show):
            L.append(f"  _+ {len(cs) - len(show)} v1-confirmed single-doc mentions (see candidates.csv)._")
        L.append("")
    (STEP2 / "report" / "step2_candidates.md").write_text("\n".join(L), encoding="utf-8")

    with (STEP2 / "report" / "candidates.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["name", "facet", "segment", "novel", "v1_match", "n_docs", "n_B", "n_G",
                    "grounded", "groups", "variants", "definition", "evidence", "docs"])
        for c in clusters:
            w.writerow([c["name"], c["facet"], c["segment"], c["novel"], c["v1"] or "", c["n_docs"],
                        c["n_B"], c["n_G"], f"{c['grounded']:.2f}",
                        " | ".join(c["groups"]), " | ".join(c["variants"]),
                        c["definition"], c["evidence"], " ".join(c["docs"])])

    print(f"clusters={n} (robust {len(robust)})  v1-coverage={len(covered)}  "
          f"novel: {len(novel_r)} robust +{len(novel_s)} singletons  "
          f"robust G∩B={seg['G∩B']} B∖G={seg['B∖G']} G∖B={seg['G∖B']}  bias(robust blind-only novel)={len(bias)}")
    print("report ->", STEP2 / "report" / "step2_candidates.md")


if __name__ == "__main__":
    main()
