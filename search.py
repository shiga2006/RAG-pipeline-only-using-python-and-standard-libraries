"""Steps 5-6 - Retrieval engine + command-line interface.

    python search.py                       # interactive prompt
    python search.py "annual leave days"   # one-off query
    python search.py --mode hybrid --chunker section "lost laptop"
"""
import argparse
import hashlib
import json
import os
import numpy as np

from loaders import load_kb
from chunking import chunk_docs
from tfidf import TfidfVectorizer, BM25, cosine_sim, expand_query

HERE = os.path.dirname(os.path.abspath(__file__))
KB_DIR, INDEX_DIR = os.path.join(HERE, "kb"), os.path.join(HERE, "index")

# Tuned in evaluate.py (see README): minimum score to count as "relevant"
DEFAULT_THRESHOLD = {"tfidf": 0.25, "bm25": 0.25, "hybrid": 0.25}


class SearchEngine:
    """The 'vector store': a NumPy matrix (one row per chunk) + a parallel list of chunk metadata."""

    def __init__(self, chunks, mode="hybrid", stem=True, synonyms=True, bigrams=False):
        self.chunks, self.mode, self.stem, self.synonyms, self.bigrams = chunks, mode, stem, synonyms, bigrams
        texts = [c["index_text"] for c in chunks]
        self.vec = TfidfVectorizer(use_stem=stem, bigrams=bigrams).fit(texts)
        self.matrix = self.vec.transform(texts)
        self.bm25 = BM25(use_stem=stem).fit(texts) if mode in ("bm25", "hybrid") else None

    def score_all(self, query):
        q = expand_query(query) if self.synonyms else query
        cos = cosine_sim(self.vec.transform([q])[0], self.matrix)
        if self.mode == "tfidf":
            return cos
        bm = self.bm25.scores(q)
        return bm if self.mode == "bm25" else 0.7 * cos + 0.3 * bm

    def search(self, query, k=3, threshold=None):
        thr = DEFAULT_THRESHOLD[self.mode] if threshold is None else threshold
        scores = self.score_all(query)
        top = np.argsort(-scores)[:k]
        return [{**self.chunks[i], "score": float(scores[i])} for i in top if scores[i] >= thr]

    # ---- persistence: matrix -> .npy, everything else -> .json -------------------------------
    def save(self, path, meta):
        os.makedirs(path, exist_ok=True)
        np.save(os.path.join(path, "matrix.npy"), self.matrix)
        with open(os.path.join(path, "index.json"), "w", encoding="utf-8") as f:
            json.dump({"meta": meta, "chunks": self.chunks, "vec": self.vec.to_dict(),
                       "opts": [self.mode, self.stem, self.synonyms, self.bigrams]}, f)

    @classmethod
    def load(cls, path):
        with open(os.path.join(path, "index.json"), encoding="utf-8") as f:
            d = json.load(f)
        eng = cls.__new__(cls)
        eng.chunks, (eng.mode, eng.stem, eng.synonyms, eng.bigrams) = d["chunks"], d["opts"]
        eng.vec, eng.matrix = TfidfVectorizer.from_dict(d["vec"]), np.load(os.path.join(path, "matrix.npy"))
        texts = [c["index_text"] for c in eng.chunks]
        eng.bm25 = BM25(use_stem=eng.stem).fit(texts) if eng.mode in ("bm25", "hybrid") else None
        return eng


def build_engine(chunker="sentence", chunk_params=None, kb_dir=KB_DIR, verbose=True, **engine_opts):
    docs = load_kb(kb_dir, verbose)
    chunks = chunk_docs(docs, chunker, **(chunk_params or {}))
    return SearchEngine(chunks, **engine_opts)


def get_engine(args):
    """Load the cached index if the KB + config are unchanged, otherwise rebuild and cache it."""
    files = sorted(os.listdir(KB_DIR))
    sig = hashlib.md5(json.dumps([[f, os.path.getsize(os.path.join(KB_DIR, f)), os.path.getmtime(os.path.join(KB_DIR, f))]
                                  for f in files] + [vars(args)["chunker"], args.mode, args.max_chars,
                                                     args.overlap_sents], default=str).encode()).hexdigest()
    meta_path = os.path.join(INDEX_DIR, "index.json")
    if os.path.exists(meta_path) and not args.rebuild:
        with open(meta_path, encoding="utf-8") as f:
            if json.load(f)["meta"] == sig:
                print("(loaded cached index)")
                return SearchEngine.load(INDEX_DIR)
    print("Building index...")
    params = {"max_chars": args.max_chars, "overlap_sents": args.overlap_sents} if args.chunker == "sentence" else {}
    eng = build_engine(args.chunker, params, mode=args.mode)
    eng.save(INDEX_DIR, sig)
    print(f"Indexed {len(eng.chunks)} chunks, vocabulary {len(eng.vec.vocab)} terms.\n")
    return eng


def show(query, results):
    print(f"\nQuery: {query}")
    if not results:
        print("  -> No relevant information found in the knowledge base.")
    for rank, r in enumerate(results, 1):
        print(f"  #{rank}  score={r['score']:.3f}  [{r['source']}, chunk {r['id']}]  section: {r['heading'] or '-'}")
        print(f"      \"{r['text']}\"")


def main():
    ap = argparse.ArgumentParser(description="Employee Knowledge Assistant (retrieval only)")
    ap.add_argument("query", nargs="?")
    ap.add_argument("--chunker", default="sentence", choices=["fixed", "sentence", "section"])
    ap.add_argument("--max-chars", type=int, default=250)
    ap.add_argument("--overlap-sents", type=int, default=1)
    ap.add_argument("--mode", default="hybrid", choices=["tfidf", "bm25", "hybrid"])
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--threshold", type=float, default=None)
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()
    eng = get_engine(args)
    if args.query:
        show(args.query, eng.search(args.query, args.k, args.threshold))
        return
    print("Ask a question (blank line to quit).")
    while True:
        q = input("\n> ").strip()
        if not q:
            break
        show(q, eng.search(q, args.k, args.threshold))


if __name__ == "__main__":
    main()
