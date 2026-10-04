"""Step 7 - The labelled test set (20 queries) and a runner that writes results/test_results.md.
Each query has `expect`: list of (source_file, keyword). A top-3 chunk 'satisfies' a target when it comes from
that file and contains the keyword (lower-case match). No-match queries must return an empty list."""
import os
from search import build_engine

D, P, N, M = "direct", "paraphrase", "no-match", "multi-chunk"
LP, EP, CC, RW, IT, BF, OB = ("leave_policy.pdf", "expense_policy.pdf", "code_of_conduct.docx",
                              "remote_work_policy.docx", "it_security.txt", "benefits_faq.txt", "onboarding.pptx")

QUERIES = [
    (D, "How many days of annual leave do I get?", [(LP, "18 days")]),
    (D, "What is the VPN policy?", [(IT, "globalprotect")]),
    (D, "What is the dress code on Fridays?", [(CC, "casual wear")]),
    (D, "When are salaries credited?", [(BF, "last working day")]),
    (D, "What happens on day 2 of the first week?", [(OB, "day 2")]),
    (D, "How much is the hotel reimbursement in metro cities?", [(EP, "6,000")]),
    (D, "How many weeks of maternity leave are given?", [(LP, "26 weeks")]),
    (P, "How much time off am I allowed each year?", [(LP, "18 days")]),
    (P, "Can I work from home?", [(RW, "hybrid"), (RW, "home office")]),
    (P, "How often do I have to change my password?", [(IT, "90 days")]),
    (P, "Who do I contact if I feel harassed at work?", [(CC, "ethics committee")]),
    (P, "What is the staff referral reward amount?", [(BF, "referral bonus")]),
    (N, "What is the company's stock price?", []),
    (N, "Best pizza places in Chennai", []),
    (N, "How do I request a company car?", []),
    (M, "What should I do if I lose my laptop?", [(IT, "lost or stolen"), (CC, "loss, theft")]),
    (M, "Explain sick leave and the documentation required", [(LP, "10 days of paid sick leave"), (LP, "medical certificate")]),
    (M, "How do I report a data breach?", [(IT, "security@zenvora"), (CC, "data breach")]),
    (M, "Rules for connecting from public Wi-Fi while working remotely", [(RW, "public wi-fi"), (IT, "vpn must be used")]),
    (M, "What do I need to finish in my first month?", [(OB, "e-learning"), (OB, "enroll in health insurance")]),
]


def satisfied(results, source, keyword):
    """Rank (1-based) of the first top-k chunk satisfying the target, else None."""
    for rank, r in enumerate(results, 1):
        if r["source"] == source and keyword in r["index_text"].lower():
            return rank
    return None


def judge(qtype, expect, results):
    """-> (verdict, first_hit_rank, targets_covered, targets_total)"""
    if not expect:
        return ("PASS" if not results else "FAIL"), None, 0, 0
    ranks = [satisfied(results, s, k) for s, k in expect]
    hit = [r for r in ranks if r]
    if not hit:
        return "FAIL", None, 0, len(expect)
    full = len(hit) == len(expect) or qtype != M     # single-answer queries only need one hit
    return ("PASS" if full else "PARTIAL"), min(hit), len(hit), len(expect)


if __name__ == "__main__":
    print("Building default system...")
    eng = build_engine("sentence", {"max_chars": 250, "overlap_sents": 1}, mode="hybrid", verbose=False)
    lines = ["# Test results\n", f"Chunks: {len(eng.chunks)} | mode: {eng.mode} | k=3\n",
             "| # | Type | Query | Verdict | Top-1 (source, score) |", "|---|---|---|---|---|"]
    detail, counts = [], {}
    for i, (qt, q, exp) in enumerate(QUERIES, 1):
        res = eng.search(q)
        v, *_ = judge(qt, exp, res)
        counts[v] = counts.get(v, 0) + 1
        top = f"{res[0]['source']}, {res[0]['score']:.2f}" if res else "none returned"
        lines.append(f"| {i} | {qt} | {q} | **{v}** | {top} |")
        print(f"{i:>2}. [{v:<7}] {qt:<11} {q:<62} -> {top}")
        detail.append(f"\n### {i}. {q}  ({qt}, {v})\n" + ("*No chunk above threshold.*\n" if not res else "") +
                      "".join(f"{n}. `{r['source']}` chunk {r['id']} (score {r['score']:.3f}): {r['text']}\n"
                              for n, r in enumerate(res, 1)))
    print("\nSummary:", counts)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "test_results.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + f"\n\nSummary: {counts}\n\n## Retrieved chunks\n" + "".join(detail))
    print("Wrote", out)
