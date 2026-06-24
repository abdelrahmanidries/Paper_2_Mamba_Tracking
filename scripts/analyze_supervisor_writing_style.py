#!/usr/bin/env python3
"""Quantitative and rule-based rhetorical analysis for the supervisor corpus."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "experiments" / "supervisor_style_corpus_metadata.csv"
SECTION_DIR = ROOT / "papers" / "supervisor_style_corpus" / "section_text"
OUT = ROOT / "experiments" / "supervisor_style_features.csv"


CITATION_RE = re.compile(r"\[(?:\d+(?:\s*[-,]\s*\d+)*)\]|\([A-Z][A-Za-z-]+(?: et al\.)?,\s*\d{4}\)")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z'-]*\b")
PASSIVE_RE = re.compile(r"\b(?:is|are|was|were|be|been|being)\s+\w+(?:ed|en)\b", re.I)
FIRST_PERSON_RE = re.compile(r"\b(?:we|our|ours|us)\b", re.I)
HEDGE_RE = re.compile(
    r"\b(?:may|might|could|can|generally|typically|often|relatively|"
    r"approximately|potentially|suggests?|appears?|tends?|limited|"
    r"rather than|not necessarily)\b",
    re.I,
)
TRANSITION_WORDS = [
    "however",
    "therefore",
    "moreover",
    "furthermore",
    "in addition",
    "nevertheless",
    "although",
    "while",
    "whereas",
    "in contrast",
    "consequently",
    "specifically",
]
LIMITATION_RE = re.compile(
    r"\b(?:however|nevertheless|although|limited|limitation|challenge|"
    r"fail(?:s|ed)?|difficult|cannot|unable|suffer(?:s|ed)?|drawback|"
    r"problem|still|remain(?:s)?)\b",
    re.I,
)
CONTRIBUTION_RE = re.compile(r"\b(?:contribution|main contributions|we propose|we present|we develop|this paper)\b", re.I)


LABEL_PATTERNS = {
    "broad_context": re.compile(r"\b(?:recent|with the development|in recent years|has attracted|important|widely)\b", re.I),
    "practical_importance": re.compile(r"\b(?:applications?|practical|real-world|clinical|embedded|portable|surveillance|remote)\b", re.I),
    "specific_problem": re.compile(r"\b(?:problem|task|challenge|objective|aims? to|difficult)\b", re.I),
    "prior_progress": re.compile(r"\b(?:existing|previous|traditional|recent methods|state-of-the-art|have been proposed)\b", re.I),
    "unresolved_limitation": LIMITATION_RE,
    "research_gap": re.compile(r"\b(?:still|remain|lack|few|not been|insufficient|gap)\b", re.I),
    "proposed_direction": re.compile(r"\b(?:we propose|we present|we develop|this paper proposes|in this paper)\b", re.I),
    "contribution_summary": re.compile(r"\b(?:contributions?|summari[sz]ed|main novelty)\b", re.I),
    "paper_organization": re.compile(r"\b(?:remainder|organized as follows|section [ivx0-9]+)\b", re.I),
    "representative_methods": re.compile(r"\b(?:method|approach|algorithm|model|network|scheme)\b", re.I),
    "comparison": re.compile(r"\b(?:compared|outperform|different from|similar to|whereas|in contrast)\b", re.I),
    "transition_present_work": re.compile(r"\b(?:to address|motivated by|therefore|hence|in this work)\b", re.I),
}


def load_metadata() -> dict[str, dict[str, str]]:
    if not METADATA.exists():
        return {}
    with METADATA.open(newline="", encoding="utf-8") as f:
        return {row["corpus_id"]: row for row in csv.DictReader(f)}


def split_body(text: str) -> str:
    parts = text.split("\n\n", 1)
    return parts[1] if len(parts) == 2 and parts[0].startswith("corpus_id:") else text


def paragraphs(text: str) -> list[str]:
    return [p.strip().replace("\n", " ") for p in text.split("\n\n") if p.strip() and not p.startswith("corpus_id:")]


def sentences(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE_RE.split(text.strip()) if s.strip()]


def classify_order(paras: list[str]) -> str:
    labels = []
    for p in paras:
        found = [name for name, pat in LABEL_PATTERNS.items() if pat.search(p)]
        labels.append("+".join(found[:3]) if found else "unlabeled")
    return " > ".join(labels[:10])


def infer_related_organization(paras: list[str]) -> str:
    text = " ".join(paras).lower()
    years = len(re.findall(r"\b20\d{2}|19\d{2}\b", text))
    category_markers = len(re.findall(r"\b(?:can be divided|categories|class|family|type|first|second|third)\b", text))
    problem_markers = len(re.findall(r"\b(?:challenge|problem|degradation|noise|resolution|occlusion|motion)\b", text))
    method_markers = len(re.findall(r"\b(?:cnn|network|filter|sparse|transform|fusion|model|algorithm)\b", text))
    scores = {
        "chronological": years,
        "taxonomy-based": category_markers,
        "problem-based": problem_markers,
        "method-family based": method_markers,
    }
    best, value = max(scores.items(), key=lambda kv: kv[1])
    return best if value else "not reported"


def contribution_count(paras: list[str]) -> int:
    text = "\n".join(paras)
    bullets = len(re.findall(r"(?m)^\s*(?:[-*]|\d+[.)])\s+", text))
    if bullets:
        return bullets
    match = re.search(r"\b(?:first|firstly)\b.*\b(?:second|secondly)\b", text, re.I | re.S)
    if match:
        return len(re.findall(r"\b(?:first(?:ly)?|second(?:ly)?|third(?:ly)?|finally|lastly)\b", text, re.I))
    return 0


def analyze_section(corpus_id: str, section_name: str, text: str, meta: dict[str, str]) -> dict[str, str]:
    body = split_body(text)
    paras = paragraphs(body)
    sent = sentences(body)
    words = WORD_RE.findall(body)
    cites_per_para = [len(CITATION_RE.findall(p)) for p in paras]
    first_citation_para = next((i + 1 for i, p in enumerate(paras) if CITATION_RE.search(p)), 0)
    transition_counter = Counter()
    for tw in TRANSITION_WORDS:
        transition_counter[tw] = len(re.findall(r"\b" + re.escape(tw) + r"\b", body, re.I))
    labels = classify_order(paras)
    return {
        "corpus_id": corpus_id,
        "title": meta.get("title", ""),
        "target_supervisor": meta.get("target_supervisor", ""),
        "year": meta.get("year", ""),
        "journal": meta.get("journal", ""),
        "section": section_name,
        "paragraph_count": str(len(paras)),
        "word_count": str(len(words)),
        "mean_words_per_paragraph": f"{(len(words) / len(paras)):.2f}" if paras else "0",
        "sentence_count": str(len(sent)),
        "mean_words_per_sentence": f"{(len(words) / len(sent)):.2f}" if sent else "0",
        "citation_count": str(len(CITATION_RE.findall(body))),
        "mean_citations_per_paragraph": f"{(sum(cites_per_para) / len(paras)):.2f}" if paras else "0",
        "first_citation_paragraph": str(first_citation_para),
        "passive_proxy_count": str(len(PASSIVE_RE.findall(body))),
        "passive_proxy_per_100_sentences": f"{(100 * len(PASSIVE_RE.findall(body)) / len(sent)):.2f}" if sent else "0",
        "first_person_count": str(len(FIRST_PERSON_RE.findall(body))),
        "hedge_count": str(len(HEDGE_RE.findall(body))),
        "transition_counts": "; ".join(f"{k}={v}" for k, v in transition_counter.items() if v),
        "rhetorical_order_proxy": labels,
        "contribution_list_form": "explicit-list" if contribution_count(paras) else ("prose" if CONTRIBUTION_RE.search(body) else "not reported"),
        "typical_number_of_contributions_proxy": str(contribution_count(paras)),
        "related_work_organization_proxy": infer_related_organization(paras) if section_name == "related_work" else "not applicable",
        "limitation_expression_count": str(len(LIMITATION_RE.findall(body))),
        "final_paragraph_bridge_proxy": classify_order(paras[-1:]) if paras else "not reported",
    }


def main() -> int:
    meta = load_metadata()
    rows = []
    for path in sorted(SECTION_DIR.glob("*__*.txt")):
        corpus_id, section_part = path.stem.split("__", 1)
        rows.append(analyze_section(corpus_id, section_part, path.read_text(encoding="utf-8"), meta.get(corpus_id, {})))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "corpus_id",
        "title",
        "target_supervisor",
        "year",
        "journal",
        "section",
        "paragraph_count",
        "word_count",
        "mean_words_per_paragraph",
        "sentence_count",
        "mean_words_per_sentence",
        "citation_count",
        "mean_citations_per_paragraph",
        "first_citation_paragraph",
        "passive_proxy_count",
        "passive_proxy_per_100_sentences",
        "first_person_count",
        "hedge_count",
        "transition_counts",
        "rhetorical_order_proxy",
        "contribution_list_form",
        "typical_number_of_contributions_proxy",
        "related_work_organization_proxy",
        "limitation_expression_count",
        "final_paragraph_bridge_proxy",
    ]
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {OUT} rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
