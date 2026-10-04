"""Evaluation harness - the experiments behind the README tables.
  A. Chunking comparison   (fixed vs sentence vs section, several sizes/overlaps)
  B. Feature ablation      (TF-IDF baseline -> +stemming -> +synonyms -> +bigrams -> BM25 -> hybrid)
  C. Threshold sweep       (how the 'no answer' cut-off was chosen)
Ranking metrics are computed with threshold = 0 so they measure ranking quality only.
Run:  python evaluate.py"""
import csv
import os
import statistics as st

from search import build_engine
from test_queries import QUERIES, N, judge

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUT, exist_ok=True)
ANSWERABLE = [q for q in QUERIES if q[2]]


def ranking_metrics(eng):
    hits, rr, cov = 0, [], []
    for qt, q, exp in ANSWERABLE:
        _, rank, covered, total = judge(qt, exp, eng.search(q, 3, threshold=0))
        hits += rank is not None
        rr.append(1 / rank if rank else 0)
        cov.append(covered / total)
    n = len(ANSWERABLE)
    return {"Recall@3": hits / n, "MRR": sum(rr) / n, "Coverage": sum(cov) / n}


def table(title, rows, cols, fname):
    print(f"\n=== {title} ===")
    w = max(len(r[0]) for r in rows) + 2
    print(f"{'Config':<{w}}" + "".join(f"{c:>11}" for c in cols))
    for r in rows:
        print(f"{r[0]:<{w}}" + "".join(f"{v:>11.3f}" if isinstance(v, float) else f"{v:>11}" for v in r[1:]))
    with open(os.path.join(OUT, fname), "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows([["config"] + cols] + rows)


def experiment_chunking():
    configs = [("fixed 150/0", "fixed", dict(size=150, overlap=0)), ("fixed 150/40", "fixed", dict(size=150, overlap=40)),
               ("fixed 300/0", "fixed", dict(size=300, overlap=0)), ("fixed 300/60", "fixed", dict(size=300, overlap=60)),
               ("fixed 500/100", "fixed", dict(size=500, overlap=100)),
               ("sentence 150/1", "sentence", dict(max_chars=150, overlap_sents=1)),
               ("sentence 250/0", "sentence", dict(max_chars=250, overlap_sents=0)),
               ("sentence 250/1", "sentence", dict(max_chars=250, overlap_sents=1)),
               ("sentence 250/2", "sentence", dict(max_chars=250, overlap_sents=2)),
               ("sentence 400/1", "sentence", dict(max_chars=400, overlap_sents=1)),
               ("sentence 250/1 no-heading", "sentence", dict(max_chars=250, overlap_sents=1, section_aware=False)),
               ("section (1 per heading)", "section", {}),
               ("section no-heading", "section", dict(section_aware=False))]
    rows = []
    for name, method, params in configs:      # plain TF-IDF so only the chunking varies
        eng = build_engine(method, params, verbose=False, mode="tfidf", stem=False, synonyms=False)
        m = ranking_metrics(eng)
        lens = [len(c["text"]) for c in eng.chunks]
        rows.append([name, len(eng.chunks), round(st.mean(lens)), m["Recall@3"], m["MRR"], m["Coverage"]])
    table("A. Chunking comparison (plain TF-IDF)", rows, ["Chunks", "AvgChars", "Recall@3", "MRR", "Coverage"], "chunking_comparison.csv")
    return rows


def experiment_ablation():
    base = ("sentence", dict(max_chars=250, overlap_sents=1))
    variants = [("TF-IDF baseline", dict(mode="tfidf", stem=False, synonyms=False)),
                ("+ stemming", dict(mode="tfidf", stem=True, synonyms=False)),
                ("+ synonyms", dict(mode="tfidf", stem=True, synonyms=True)),
                ("+ bigrams", dict(mode="tfidf", stem=True, synonyms=True, bigrams=True)),
                ("BM25 (stem+syn)", dict(mode="bm25", stem=True, synonyms=True)),
                ("Hybrid 0.7/0.3", dict(mode="hybrid", stem=True, synonyms=True))]
    rows = []
    for name, opts in variants:
        m = ranking_metrics(build_engine(base[0], base[1], verbose=False, **opts))
        rows.append([name, m["Recall@3"], m["MRR"], m["Coverage"]])
    table("B. Feature ablation (sentence 250/1)", rows, ["Recall@3", "MRR", "Coverage"], "ablation.csv")
    return rows


def experiment_threshold():
    eng = build_engine("sentence", dict(max_chars=250, overlap_sents=1), verbose=False, mode="hybrid")
    nomatch = [q for q in QUERIES if q[0] == N]
    rows, best = [], (-1, None)
    for thr in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]:
        rej = sum(not eng.search(q, 3, thr) for _, q, _ in nomatch) / len(nomatch)
        kept = sum(judge(t, e, eng.search(q, 3, thr))[1] is not None for t, q, e in ANSWERABLE) / len(ANSWERABLE)
        bal = (rej + kept) / 2
        rows.append([f"{thr:.2f}", rej, kept, bal])
        if bal > best[0] + 1e-9:
            best = (bal, thr)
    table("C. Threshold sweep (hybrid)", rows, ["NoMatchOK", "Recall@3", "Balanced"], "threshold_sweep.csv")
    print(f"\nBest balanced accuracy {best[0]:.3f} first reached at threshold {best[1]:.2f}")
    top = [round(eng.search(q, 1, 0)[0]["score"], 2) for _, q, _ in nomatch]
    print("Top-1 scores of the no-match queries:", top)


def chart(rows):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh([r[0] for r in rows], [r[3] for r in rows], color="#4a7fb5")
    ax.set_xlabel("Recall@3 (answerable queries)"); ax.set_title("Chunking strategy comparison")
    ax.invert_yaxis(); plt.tight_layout(); plt.savefig(os.path.join(OUT, "chunking_comparison.png"), dpi=120)


if __name__ == "__main__":
    chart(experiment_chunking())
    experiment_ablation()
    experiment_threshold()
