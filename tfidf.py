"""Steps 4 & 5 - Text representation: tokenizer, TF-IDF (from scratch), BM25 (comparison baseline),
cosine similarity, and a tiny synonym map for query expansion."""
import math
import re
from collections import Counter
import numpy as np

STOPWORDS = set("""a an the is are was were be been am of to and in for on with at by or as it its this that
these those from do does did i me my we our you your can could should would will shall may might what which who
whom how when where why if than then so not no any each there their they them he she his her about into
over after before get got have has had""".split())

# Query-side expansion for the vocabulary-mismatch problem ("time off" vs "leave")
SYNONYMS = {
    "time off": "leave vacation", "vacation": "leave", "holiday": "leave", "pto": "leave",
    "wfh": "remote hybrid home", "work from home": "remote hybrid", "working from home": "remote hybrid",
    "reward": "bonus", "salary": "salaries pay", "paid": "credited", "harassed": "harassment ethics committee report",
    "harassment": "ethics committee report", "stolen": "lost theft", "lose": "lost", "wifi": "wi fi",
    "cab": "travel", "reimburse": "reimbursed claim",
}


def stem(w):
    """Very small suffix stripper (consistent on both sides, so exact linguistics don't matter)."""
    if len(w) <= 3:
        return w
    for suf, rep in (("ies", "y"), ("ing", ""), ("ed", ""), ("s", "")):
        if w.endswith(suf) and not w.endswith("ss") and len(w) - len(suf) >= 3:
            w = w[: -len(suf)] + rep
            break
    return w[:-1] if w.endswith("e") and len(w) > 4 else w


def tokenize(text, use_stem=False, bigrams=False):
    toks = [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOPWORDS]
    if use_stem:
        toks = [stem(w) for w in toks]
    if bigrams:
        toks = toks + [f"{a}_{b}" for a, b in zip(toks, toks[1:])]
    return toks


def expand_query(q):
    ql = q.lower()
    extra = [v for k, v in SYNONYMS.items() if re.search(rf"\b{re.escape(k)}\b", ql)]
    return q + " " + " ".join(extra) if extra else q


class TfidfVectorizer:
    def __init__(self, use_stem=False, bigrams=False):
        self.use_stem, self.bigrams = use_stem, bigrams

    def _tok(self, t):
        return tokenize(t, self.use_stem, self.bigrams)

    def fit(self, docs):
        toks = [self._tok(d) for d in docs]
        self.vocab = {w: i for i, w in enumerate(sorted({w for t in toks for w in t}))}
        n = len(docs)
        df = Counter(w for t in toks for w in set(t))
        self.idf = np.zeros(len(self.vocab))
        for w, i in self.vocab.items():
            self.idf[i] = math.log((1 + n) / (1 + df[w])) + 1      # smoothed IDF
        return self

    def transform(self, docs):
        m = np.zeros((len(docs), len(self.vocab)))
        for r, d in enumerate(docs):
            t = self._tok(d)
            for w, c in Counter(t).items():
                if w in self.vocab:                                # unseen words are ignored
                    m[r, self.vocab[w]] = (c / len(t)) * self.idf[self.vocab[w]]
        return m

    def to_dict(self):
        return {"use_stem": self.use_stem, "bigrams": self.bigrams, "vocab": self.vocab, "idf": self.idf.tolist()}

    @classmethod
    def from_dict(cls, d):
        v = cls(d["use_stem"], d["bigrams"])
        v.vocab, v.idf = d["vocab"], np.array(d["idf"])
        return v


def cosine_sim(query_vec, matrix):
    """cos(q, d) = q.d / (|q||d|) against every row of the matrix at once."""
    denom = np.linalg.norm(matrix, axis=1) * np.linalg.norm(query_vec)
    denom[denom == 0] = 1e-12
    return (matrix @ query_vec) / denom


class BM25:
    """Okapi BM25. Scores are divided by the best score the query could possibly get -> range [0, 1]."""
    def __init__(self, k1=1.5, b=0.75, use_stem=False):
        self.k1, self.b, self.use_stem = k1, b, use_stem

    def fit(self, docs):
        self.tf = [Counter(tokenize(d, self.use_stem)) for d in docs]
        self.len = np.array([sum(c.values()) for c in self.tf], dtype=float)
        self.avg = self.len.mean()
        n = len(docs)
        df = Counter(w for c in self.tf for w in c)
        self.idf = {w: math.log((n - f + 0.5) / (f + 0.5) + 1) for w, f in df.items()}
        return self

    def scores(self, query):
        q = [w for w in tokenize(query, self.use_stem) if w in self.idf]
        out = np.zeros(len(self.tf))
        for i, tf in enumerate(self.tf):
            norm = self.k1 * (1 - self.b + self.b * self.len[i] / self.avg)
            out[i] = sum(self.idf[w] * tf[w] * (self.k1 + 1) / (tf[w] + norm) for w in q if w in tf)
        best = sum(self.idf[w] * (self.k1 + 1) for w in q)
        return out / best if best else out
