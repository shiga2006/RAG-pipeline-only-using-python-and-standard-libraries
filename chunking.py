"""Step 3 - Chunking. Three strategies, all returning chunk dicts:
  {source, id, heading, text (shown to user), index_text (what gets vectorised)}
section_aware=True prepends the section heading to index_text so headings add keywords."""
import re
from itertools import groupby


def _split_sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def _by_source(docs):
    for source, secs in groupby(docs, key=lambda d: d["source"]):
        yield source, list(secs)


def _make(source, cid, heading, text, section_aware):
    idx = f"{heading}. {text}" if (section_aware and heading) else text
    return {"source": source, "id": cid, "heading": heading, "text": text, "index_text": idx}


def chunk_fixed(docs, size=500, overlap=100, section_aware=False):
    """Sliding character window over the whole document. Simple but cuts mid-sentence."""
    out, step = [], size - overlap
    for source, secs in _by_source(docs):
        full = " ".join(f"{s['heading']}. {s['text']}" for s in secs)
        for i, start in enumerate(range(0, len(full), step)):
            piece = full[start:start + size].strip()
            if piece:
                out.append(_make(source, len(out), "", piece, False))
            if start + size >= len(full):
                break
    return _renumber(out)


def chunk_sentence(docs, max_chars=400, overlap_sents=1, section_aware=True):
    """Pack whole sentences up to max_chars; carry the last N sentences into the next chunk."""
    out = []
    for source, secs in _by_source(docs):
        for sec in secs:
            cur, fresh = [], 0
            for s in _split_sentences(sec["text"]):
                if cur and sum(len(x) + 1 for x in cur) + len(s) > max_chars:
                    out.append(_make(source, 0, sec["heading"], " ".join(cur), section_aware))
                    cur = cur[-overlap_sents:] if overlap_sents else []
                    fresh = 0
                cur.append(s)
                fresh += 1
            if cur and fresh:
                out.append(_make(source, 0, sec["heading"], " ".join(cur), section_aware))
    return _renumber(out)


def chunk_section(docs, section_aware=True):
    """One chunk per heading/slide: the natural topic unit."""
    out = [_make(d["source"], 0, d["heading"], d["text"], section_aware) for d in docs if d["text"]]
    return _renumber(out)


def _renumber(chunks):
    """Give each chunk an id that is unique within its source file."""
    counters = {}
    for c in chunks:
        c["id"] = counters.get(c["source"], 0)
        counters[c["source"]] = c["id"] + 1
    return chunks


METHODS = {"fixed": chunk_fixed, "sentence": chunk_sentence, "section": chunk_section}


def chunk_docs(docs, method="sentence", **params):
    return METHODS[method](docs, **params)
