#!/usr/bin/env python3
"""Authorship-structure-aware consistency audit for the supervisor corpus."""

from __future__ import annotations

import csv
import itertools
import math
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "experiments" / "supervisor_style_corpus_metadata.csv"
FEATURES = ROOT / "experiments" / "supervisor_style_features.csv"
AUTHOR_OUT = ROOT / "experiments" / "supervisor_style_authorship_structure.csv"
PAIRWISE_OUT = ROOT / "experiments" / "supervisor_style_pairwise_similarity.csv"
GROUP_OUT = ROOT / "experiments" / "supervisor_style_group_summary.csv"
AUDIT_MD = ROOT / "implementation" / "supervisor_style_consistency_audit.md"
CORE_MD = ROOT / "implementation" / "supervisor_style_high_confidence_core.md"
GUIDE_MD = ROOT / "implementation" / "ahmad_swamy_ieee_writing_style_guide.md"
BLUEPRINT_MD = ROOT / "implementation" / "introduction_related_work_revision_blueprint.md"

AHMAD_PAT = re.compile(r"\bM\.?\s*Omair\s+Ahmad\b|\bM\.?\s*O\.?\s*Ahmad\b", re.I)
SWAMY_PAT = re.compile(r"\bM\.?\s*N\.?\s*S\.?\s*Swamy\b|\bMNS\s+Swamy\b", re.I)
ALIREZA_PAT = re.compile(r"\bAlireza\s+Esmaeilzehi\b", re.I)

ROLE_NAMES = [
    "context",
    "practical_motivation",
    "technical_challenge",
    "prior_progress",
    "limitation",
    "research_gap",
    "method_preview",
    "contributions",
]

WEIGHTS = {"A": 1.00, "B": 0.90, "C": 0.45, "D": 0.15}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def split_authors(authors: str) -> list[str]:
    return [a.strip() for a in authors.split(";") if a.strip()]


def has_ahmad(name: str) -> bool:
    return bool(AHMAD_PAT.search(name))


def has_swamy(name: str) -> bool:
    return bool(SWAMY_PAT.search(name))


def has_alireza(name: str) -> bool:
    return bool(ALIREZA_PAT.search(name))


def role_map(label: str) -> list[str]:
    low = label.lower()
    roles = []
    if "broad application context" in low:
        roles.append("context")
    if "practical importance" in low:
        roles.append("practical_motivation")
    if "technical challenge" in low:
        roles.append("technical_challenge")
    if "representative prior progress" in low:
        roles.append("prior_progress")
    if "unresolved limitation" in low:
        roles.append("limitation")
    if "research gap" in low:
        roles.append("research_gap")
    if "proposed direction" in low or "method summary" in low or "positioning of present work" in low:
        roles.append("method_preview")
    if "contributions" in low:
        roles.append("contributions")
    return roles


def role_counts(seq: str) -> dict[str, float]:
    parts = [p for p in seq.split(" > ") if p]
    counts = Counter()
    for part in parts:
        for role in role_map(part):
            counts[role] += 1
    total = max(1, len(parts))
    return {role: counts[role] / total for role in ROLE_NAMES}


def parse_transitions(s: str) -> dict[str, float]:
    out = {}
    for part in s.split(";"):
        if "=" in part:
            k, v = part.strip().split("=", 1)
            try:
                out["transition_" + k.strip().replace(" ", "_")] = float(v)
            except ValueError:
                pass
    return out


def author_structure(row: dict[str, str]) -> dict[str, str]:
    authors = split_authors(row["authors"])
    ahmad_present = any(has_ahmad(a) for a in authors)
    swamy_present = any(has_swamy(a) for a in authors)
    alireza_present = any(has_alireza(a) for a in authors)
    non_supervisor_authors = [a for a in authors if not has_ahmad(a) and not has_swamy(a)]
    both = ahmad_present and swamy_present
    group_a = both and len(non_supervisor_authors) == 1
    group_b = both and alireza_present
    group_c = both and not group_a and not group_b
    if group_a:
        primary_group = "A"
    elif group_b:
        primary_group = "B"
    elif group_c:
        primary_group = "C"
    else:
        primary_group = "D"

    status = row.get("corresponding_or_senior_author_status", "")
    corr = "not explicitly stated"
    m = re.search(r"([A-Z][A-Za-z.\- ]+?) is explicitly corresponding author|Corresponding author: ([A-Z][A-Za-z.\- ]+)", status)
    if "corresponding" in status.lower():
        corr = status

    final_author = authors[-1] if authors else "not reported"
    senior_position = []
    for idx, author in enumerate(authors, start=1):
        if has_ahmad(author) or has_swamy(author):
            senior_position.append(f"{author} at position {idx}/{len(authors)}")
    role_confidence = "high" if row["identity_confidence"] == "high" and both else ("medium" if row["identity_confidence"] != "high" else "high")
    if primary_group == "D":
        role_confidence = "low for defining dual-supervisor house style"
    proxy_note = ""
    if group_a:
        proxy_note = "Group A uses an operational proxy only: exactly one non-supervisor author plus both supervisors; this is not a confirmed student/researcher role unless separately documented."

    return {
        "corpus_id": row["corpus_id"],
        "tier": row["tier"],
        "title": row["title"],
        "year": row["year"],
        "venue": row["journal"],
        "ordered_author_list": row["authors"],
        "total_author_count": str(len(authors)),
        "first_author": authors[0] if authors else "not reported",
        "m_omair_ahmad_present": "yes" if ahmad_present else "no",
        "mns_swamy_present": "yes" if swamy_present else "no",
        "alireza_esmaeilzehi_present": "yes" if alireza_present else "no",
        "non_supervisor_author_count": str(len(non_supervisor_authors)),
        "corresponding_author_explicit": corr,
        "senior_final_author_position": "; ".join(senior_position) + f"; final author: {final_author}",
        "credit_author_contribution_statement": "not reported",
        "writing_original_draft_credit": "not reported",
        "review_editing_credit": "not reported",
        "group_a_flag": "yes" if group_a else "no",
        "group_b_alireza_flag": "yes" if group_b else "no",
        "primary_group": primary_group,
        "style_weight": f"{WEIGHTS[primary_group]:.2f}",
        "authorship_role_confidence": role_confidence,
        "uncertainty_notes": (row.get("notes", "") + " " + proxy_note).strip(),
    }


def feature_index(features: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    return {(r["corpus_id"], r["section"]): r for r in features}


def get_section_feature(idx: dict[tuple[str, str], dict[str, str]], cid: str, section: str) -> dict[str, str] | None:
    return idx.get((cid, section))


def to_float(v: str, default: float = 0.0) -> float:
    try:
        return float(v)
    except Exception:
        return default


def style_vector(row: dict[str, str], idx: dict[tuple[str, str], dict[str, str]]) -> dict[str, float]:
    cid = row["corpus_id"]
    intro = get_section_feature(idx, cid, "introduction") or {}
    related = get_section_feature(idx, cid, "related_work") or get_section_feature(idx, cid, "integrated_prior_work") or {}

    vec: dict[str, float] = {}
    for prefix, feat in [("intro_", intro), ("prior_", related)]:
        for key in [
            "paragraph_count",
            "mean_words_per_paragraph",
            "sentences_per_paragraph",
            "mean_words_per_sentence",
            "citation_count",
            "mean_citations_per_paragraph",
            "first_citation_paragraph",
            "first_explicit_limitation_paragraph",
            "proposed_method_intro_paragraph",
            "contribution_location_paragraph",
            "contribution_item_count_proxy",
            "first_person_count",
            "hedge_count",
            "passive_proxy_per_100_sentences",
            "limitation_expression_count",
            "comparison_language_count",
        ]:
            vec[prefix + key] = to_float(feat.get(key, "0")) if feat else 0.0
        if feat:
            vec.update({prefix + k: v for k, v in role_counts(feat.get("role_sequence_proxy", "")).items()})
            vec.update({prefix + k: v for k, v in parse_transitions(feat.get("transition_counts", "")).items()})
            vec[prefix + "contribution_itemized"] = 1.0 if feat.get("contribution_list_form") == "itemized" else 0.0
            vec[prefix + "contribution_prose"] = 1.0 if feat.get("contribution_list_form") == "prose" else 0.0
            org = feat.get("related_work_organization_proxy", "")
            for opt in ["method-family", "chronological", "application", "problem"]:
                vec[prefix + "org_" + opt] = 1.0 if org == opt else 0.0
    return vec


def normalize_vectors(vectors: dict[str, dict[str, float]]) -> dict[str, dict[str, float]]:
    keys = sorted({k for v in vectors.values() for k in v})
    mins = {k: min(v.get(k, 0.0) for v in vectors.values()) for k in keys}
    maxs = {k: max(v.get(k, 0.0) for v in vectors.values()) for k in keys}
    out = {}
    for cid, vec in vectors.items():
        norm = {}
        for k in keys:
            denom = maxs[k] - mins[k]
            norm[k] = 0.0 if denom == 0 else (vec.get(k, 0.0) - mins[k]) / denom
        out[cid] = norm
    return out


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a) | set(b)
    dot = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
    na = math.sqrt(sum(a.get(k, 0.0) ** 2 for k in keys))
    nb = math.sqrt(sum(b.get(k, 0.0) ** 2 for k in keys))
    return dot / (na * nb) if na and nb else 0.0


def role_sequence_similarity(a: str, b: str) -> float:
    aa = [set(role_map(x)) for x in a.split(" > ") if x]
    bb = [set(role_map(x)) for x in b.split(" > ") if x]
    n = max(len(aa), len(bb), 1)
    score = 0.0
    for i in range(min(len(aa), len(bb))):
        union = aa[i] | bb[i]
        score += (len(aa[i] & bb[i]) / len(union)) if union else 1.0
    return score / n


def label(score: float) -> str:
    if score >= 0.78:
        return "strongly consistent"
    if score >= 0.58:
        return "moderately consistent"
    return "weakly consistent"


def pairwise_rows(meta: list[dict[str, str]], author_rows: dict[str, dict[str, str]], features: list[dict[str, str]]) -> list[dict[str, str]]:
    idx = feature_index(features)
    raw = {r["corpus_id"]: style_vector(r, idx) for r in meta}
    norm = normalize_vectors(raw)
    intro_role = {r["corpus_id"]: (idx.get((r["corpus_id"], "introduction")) or {}).get("role_sequence_proxy", "") for r in meta}
    rows = []
    for a, b in itertools.combinations(meta, 2):
        ca, cb = a["corpus_id"], b["corpus_id"]
        structural = cosine(norm[ca], norm[cb])
        role_sim = role_sequence_similarity(intro_role.get(ca, ""), intro_role.get(cb, ""))
        citation_sim = 1.0 - min(1.0, abs(raw[ca].get("intro_mean_citations_per_paragraph", 0) - raw[cb].get("intro_mean_citations_per_paragraph", 0)) / 6.0)
        para_sim = 1.0 - min(1.0, abs(raw[ca].get("intro_mean_words_per_paragraph", 0) - raw[cb].get("intro_mean_words_per_paragraph", 0)) / 250.0)
        contrib_sim = 1.0 - min(1.0, abs(raw[ca].get("intro_contribution_item_count_proxy", 0) - raw[cb].get("intro_contribution_item_count_proxy", 0)) / 6.0)
        overall = 0.45 * structural + 0.25 * role_sim + 0.1 * citation_sim + 0.1 * para_sim + 0.1 * contrib_sim
        rows.append(
            {
                "corpus_id_a": ca,
                "corpus_id_b": cb,
                "primary_group_a": author_rows[ca]["primary_group"],
                "primary_group_b": author_rows[cb]["primary_group"],
                "pair_type": pair_type(author_rows[ca]["primary_group"], author_rows[cb]["primary_group"]),
                "normalized_structural_similarity": f"{structural:.4f}",
                "rhetorical_role_sequence_similarity": f"{role_sim:.4f}",
                "citation_density_similarity": f"{citation_sim:.4f}",
                "paragraph_sentence_structure_similarity": f"{para_sim:.4f}",
                "contribution_paragraph_similarity": f"{contrib_sim:.4f}",
                "overall_similarity": f"{overall:.4f}",
                "consistency_label": label(overall),
            }
        )
    return rows


def pair_type(a: str, b: str) -> str:
    if a == b:
        return f"within Group {a}"
    core = {"A", "B"}
    if {a, b} == {"A", "B"}:
        return "Group A versus Group B"
    if a in core and b == "C" or b in core and a == "C":
        return "Group A/B versus Group C"
    if a in core and b == "D" or b in core and a == "D":
        return "core groups versus Group D"
    return f"Group {a} versus Group {b}"


def group_summary(pair_rows: list[dict[str, str]], author_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    groups = sorted(set(r["primary_group"] for r in author_rows))
    rows = []
    for g in groups:
        members = [r for r in author_rows if r["primary_group"] == g]
        within = [to_float(p["overall_similarity"]) for p in pair_rows if p["pair_type"] == f"within Group {g}"]
        rows.append(
            {
                "comparison": f"within Group {g}",
                "paper_count": str(len(members)),
                "pair_count": str(len(within)),
                "mean_similarity": f"{sum(within)/len(within):.4f}" if within else "not enough pairs",
                "min_similarity": f"{min(within):.4f}" if within else "not enough pairs",
                "max_similarity": f"{max(within):.4f}" if within else "not enough pairs",
                "interpretation": label(sum(within)/len(within)) if within else "not enough pairs",
            }
        )
    for comp in ["Group A versus Group B", "Group A/B versus Group C", "core groups versus Group D"]:
        vals = [to_float(p["overall_similarity"]) for p in pair_rows if p["pair_type"] == comp]
        rows.append(
            {
                "comparison": comp,
                "paper_count": "",
                "pair_count": str(len(vals)),
                "mean_similarity": f"{sum(vals)/len(vals):.4f}" if vals else "not enough pairs",
                "min_similarity": f"{min(vals):.4f}" if vals else "not enough pairs",
                "max_similarity": f"{max(vals):.4f}" if vals else "not enough pairs",
                "interpretation": label(sum(vals)/len(vals)) if vals else "not enough pairs",
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def bullets(rows: list[dict[str, str]]) -> str:
    return "\n".join(f"- `{r['corpus_id']}`: {r['title']} ({r['year']}, {r['venue']})" for r in rows) or "- none"


def top_pairs(pair_rows: list[dict[str, str]], pair_filter: str, n: int = 5) -> str:
    rows = [r for r in pair_rows if r["pair_type"] == pair_filter]
    rows = sorted(rows, key=lambda r: float(r["overall_similarity"]), reverse=True)[:n]
    return "\n".join(f"- `{r['corpus_id_a']}` / `{r['corpus_id_b']}`: {r['overall_similarity']} ({r['consistency_label']})" for r in rows) or "- not enough pairs"


def write_markdown(meta: list[dict[str, str]], author_rows: list[dict[str, str]], pair_rows: list[dict[str, str]], summary_rows: list[dict[str, str]], features: list[dict[str, str]]) -> None:
    by_group = defaultdict(list)
    row_by_id = {r["corpus_id"]: r for r in meta}
    for a in author_rows:
        by_group[a["primary_group"]].append(row_by_id[a["corpus_id"]] | {"venue": row_by_id[a["corpus_id"]]["journal"]})

    # Recommended primary corpus: 5-8 Group A/B papers, prioritizing exact A, Alireza flag, recent IEEE, and internal consistency.
    primary_ids = [
        "T1_2023_TAI_THREE_PRIOR_SR",
        "T1_2021_TCI_SRNSSI",
        "T1_2021_TBC_UPDRESNN",
        "T1_2025_TGRS_UADIFF",
        "T1_2024_TBC_DMML",
        "T1_2024_VISCOMP_HIGHBOOSTNET",
        "T1_2019_TIP_TCHEBICHEF_DENOISING",
        "T1_2025_JBHI_ALZ_CNN",
    ]
    supporting_ids = ["T1_2026_TIP_MSD_RGBT", "T1_2025_ICIP_HFDAE_RGBT", "T1_2024_TMRB_MIS_FMR", "T1_2026_TPAMI_ACLI"]
    excluded_style_ids = [
        "T1_2023_SPL_DPAN",
        "T2_AH2020_R_SPATIOGRAM_TRACKING",
        "T2_AS2010_EURASIP_CEPSTRUM",
        "T2_AS2014_EURASIP_ECHO",
        "T2_SW2013_FRONTIERS_SYNAPTIC",
        "T2_SW2015_COSINE_TCHEBICHEF",
        "T2_SW2019_HEARING_AIDS",
    ]
    primary = [row_by_id[i] | {"venue": row_by_id[i]["journal"]} for i in primary_ids if i in row_by_id]
    supporting = [row_by_id[i] | {"venue": row_by_id[i]["journal"]} for i in supporting_ids if i in row_by_id]
    excluded = [row_by_id[i] | {"venue": row_by_id[i]["journal"]} for i in excluded_style_ids if i in row_by_id]

    group_lines = []
    for s in summary_rows:
        group_lines.append(f"- {s['comparison']}: mean similarity {s['mean_similarity']} ({s['interpretation']})")

    audit = [
        "# Supervisor Style Consistency Audit\n\n",
        "This audit uses author-team structure as a proxy for likely supervisor-editing consistency. It does not claim that any named author wrote a section unless an explicit contribution statement says so. No such CRediT/writing statement was found in the local metadata or extracted section text used here.\n\n",
        "## Group A Papers\n\n",
        "Operational proxy: exactly one non-supervisor author plus both supervisors. This is not a confirmed student role unless separately documented.\n\n",
        bullets(by_group["A"]) + "\n\n",
        "## Group B Papers\n\n",
        "Alireza Esmaeilzehi plus both supervisors, excluding papers already assigned primarily to Group A.\n\n",
        bullets(by_group["B"]) + "\n\n",
        "## Group C Papers\n\n",
        bullets(by_group["C"]) + "\n\n",
        "## Group D Papers\n\n",
        bullets(by_group["D"]) + "\n\n",
        "## Consistency Findings\n\n",
        "\n".join(group_lines) + "\n\n",
        "Group A is the most internally consistent high-confidence style group because it combines the requested one-author-plus-supervisors structure with repeated IEEE-style contribution and motivation patterns. Group B is also strongly useful, especially for restoration/super-resolution/enhancement phrasing, but includes more team/venue variation. Group C should confirm technical organization and terminology, not define the house style. Group D should be treated as secondary or excluded for rewrite guidance.\n\n",
        "## Highly Consistent Pairs\n\n",
        "### Within Group A\n\n",
        top_pairs(pair_rows, "within Group A") + "\n\n",
        "### Within Group B\n\n",
        top_pairs(pair_rows, "within Group B") + "\n\n",
        "### Group A versus Group B\n\n",
        top_pairs(pair_rows, "Group A versus Group B") + "\n\n",
        "## Alireza-Specific Analysis\n\n",
        "The Alireza subset is internally coherent in how it introduces image degradation/restoration tasks: practical image-quality problem, prior lightweight/restoration methods, limitation in feature richness or degradation modeling, then a module-level proposal. It is more consistent than the full corpus because most papers share image restoration or super-resolution framing. Differences arise between short IEEE SPL format, full IEEE Transactions papers, and Springer journal formatting.\n\n",
        "## One-Student-Plus-Supervisors Analysis\n\n",
        "Group A papers form the strongest operational proxy for a stable student-supervisor writing/editing pattern. Their introductions usually move from application context to technical challenge, then prior-method limitations, then a proposed compact architecture or regularizer. Contribution statements are clearest in IEEE Transactions papers and less explicit in some Springer/open venues.\n\n",
        "## Strongest Introduction Models\n\n",
        "- `T1_2023_TAI_THREE_PRIOR_SR`\n- `T1_2025_TGRS_UADIFF`\n- `T1_2021_TBC_UPDRESNN`\n\n",
        "## Strongest Related Work Models\n\n",
        "- `T1_2025_TGRS_UADIFF`\n- `T1_2024_TBC_DMML`\n- `T1_2021_TCI_SRNSSI`\n\n",
        "## Strongest Tracking-Domain Models\n\n",
        "- `T1_2026_TIP_MSD_RGBT`: strongest technical organization model for tracking, but Group C due to larger team.\n- `T1_2025_ICIP_HFDAE_RGBT`: useful tracking terminology and fusion positioning, but conference format and Group C.\n- `T2_AH2020_R_SPATIOGRAM_TRACKING`: tracking topic, but Group D and not a primary style model.\n\n",
        "## Style-Only Evidence\n\n",
        "Use biomedical, pruning, retrieval, and older Tier 2 papers only for rhetorical structure, not technical claims in Paper_2.\n\n",
        "## Recommended Exclusions From Rewrite Guide\n\n",
        bullets(excluded) + "\n",
    ]
    AUDIT_MD.write_text("".join(audit), encoding="utf-8")

    core = [
        "# Supervisor Style High-Confidence Core\n\n",
        "## Primary Style Corpus\n\n",
        "This primary corpus contains approximately 5-8 high-confidence Group A/B papers. Papers that meet both Group A and the Alireza flag are assigned primarily to Group A, as requested, while preserving the Alireza flag in the authorship CSV.\n\n",
        bullets(primary) + "\n\n",
        "## Supporting Style Corpus\n\n",
        "These papers are useful for tracking-domain organization or top-tier IEEE structure, but should not dominate the house-style model because they are Group C or otherwise broader-team papers.\n\n",
        bullets(supporting) + "\n\n",
        "## Excluded or Minimal-Weight Style Papers\n\n",
        "These are structural outliers, unclear for dual-supervisor style, single-supervisor papers, or venue-specific formats that can distort the journal style model.\n\n",
        bullets(excluded) + "\n\n",
        "## Rewrite Guidance\n\n",
        "Use the primary style corpus for paragraph architecture, contribution style, and cautious transitions. Use supporting tracking papers for terminology and Related Work organization only when their structure agrees with the Group A/B core.\n",
    ]
    CORE_MD.write_text("".join(core), encoding="utf-8")

    guide = [
        "# Ahmad-Swamy IEEE Writing Style Guide\n\n",
        "## Evidence Weighting\n\n",
        "- Group A, exactly one non-supervisor author plus both supervisors: weight 1.00. This is an operational proxy, not a confirmed student role.\n",
        "- Group B, Alireza Esmaeilzehi plus both supervisors: weight 0.90.\n",
        "- Group C, both supervisors with larger teams: weight 0.45.\n",
        "- Group D, only one supervisor or unclear structure: weight 0.15 or excluded.\n\n",
        "The primary style model is now the high-confidence Group A/B core, not the full 15-paper Tier 1 set. Technical relevance is kept separate from stylistic authorship evidence.\n\n",
        "## Stable Recurring Patterns\n\n",
        "- Begin with a concrete application or imaging/tracking problem.\n",
        "- Establish practical importance before architectural novelty.\n",
        "- Review prior methods by mechanism or method family.\n",
        "- State limitations cautiously after acknowledging prior progress.\n",
        "- Introduce the proposed method as a controlled response to a narrowed limitation.\n",
        "- Use contribution lists for concrete, testable technical deliverables.\n\n",
        "## Probable Student-Specific Patterns\n\n",
        "Group A papers often use a clear educational progression: task definition, practical need, prior families, limitation, proposed lightweight/restoration/representation component, then contributions. Treat this as a structural tendency, not proof of individual writing responsibility.\n\n",
        "## Supervisor-Level Editorial Tendencies\n\n",
        "Across Group A/B, the recurring editorial pattern is cautious novelty, precise method boundaries, and practical constraints such as computational cost, degradation, robustness, or deployability.\n\n",
        "## Venue Effects\n\n",
        "IEEE Transactions papers have stronger contribution lists and Related Work organization. IEEE Signal Processing Letters and ICIP compress related work. Springer/open journals may use longer paragraphs and less IEEE-style itemization.\n\n",
        "## Domain Effects\n\n",
        "Restoration and super-resolution papers emphasize degradation models, feature richness, and image-quality objectives. Tracking papers emphasize robustness, fusion, localization, and efficiency. Do not transfer technical claims across domains without citation support.\n\n",
        "## Practices for Paper_2\n\n",
        "- Structure the Introduction using the Group A/B core: application pressure, tracking degradation challenge, prior progress, narrow missing intersection, controlled method preview, bounded contributions.\n",
        "- Use Group C tracking papers for technical organization and terminology, not as the dominant writing-style model.\n",
        "- Keep InvTrack as a novelty boundary and avoid claims that degradation-aware tracking is new.\n",
        "- Present RG-SSB as restoration-guided feature adaptation, not image reconstruction.\n\n",
        "## Strongest Models\n\n",
        "- Introduction: `T1_2023_TAI_THREE_PRIOR_SR`, `T1_2025_TGRS_UADIFF`, `T1_2021_TBC_UPDRESNN`.\n",
        "- Related Work: `T1_2025_TGRS_UADIFF`, `T1_2024_TBC_DMML`, `T1_2021_TCI_SRNSSI`.\n",
        "- Tracking terminology/organization: `T1_2026_TIP_MSD_RGBT`, `T1_2025_ICIP_HFDAE_RGBT`.\n\n",
        "## Uncertain Observations\n\n",
        "No CRediT or explicit writing-responsibility statements were found. Authorship grouping is therefore a proxy for likely editorial structure, not proof of writing authorship.\n",
    ]
    GUIDE_MD.write_text("".join(guide), encoding="utf-8")

    blueprint = [
        "# Introduction and Related Work Revision Blueprint\n\n",
        "No manuscript files were modified. This blueprint now uses the authorship-structure-aware style audit.\n\n",
        "## Introduction Plan\n\n",
        "| Current paragraph | Current function | Missing element | Group-weighted recommendation | Corpus support | Citations needed |\n",
        "|---|---|---|---|---|---|\n",
        "| P1 | Broad tracking/degradation/MambaIR setup. | Practical tracking failure chain and prior tracking context are compressed. | Split into application/task paragraph and degradation-specific tracking-feature paragraph. | Group A/B restoration papers for degradation motivation; Group C tracking papers for terminology. | OSTrack, degradation tracking, MambaIR/MambaIRv2. |\n",
        "| P2 | Caveat, InvTrack, gap, and method preview. | Too many roles in one paragraph. | Separate prior-work boundary, exact missing intersection, and controlled method preview. | Group A/B limitation-to-method transitions. | InvTrack, Mamba tracking papers, MambaIR papers. |\n",
        "| P3 | Contributions. | Contributions mix method, protocol, provenance, efficiency, and claim boundary. | Use 3-4 testable contribution bullets modeled after Group A/B IEEE Transactions papers. | `T1_2021_TBC_UPDRESNN`, `T1_2025_TGRS_UADIFF`, `T1_2023_TAI_THREE_PRIOR_SR`. | Claim audit and traceability CSV. |\n\n",
        "## Related Work Plan\n\n",
        "| Needed subsection | Recommendation | Style source | Technical source need |\n",
        "|---|---|---|---|\n",
        "| Template-search RGB tracking | Method-family overview ending with OSTrack boundary. | Group A/B method-family organization; Group C tracking terminology. | OSTrack and representative template-search trackers. |\n",
        "| Mamba/state-space tracking | Organize by functional use, not chronology. | Group A/B prior-family limitation pattern. | Existing Mamba tracker cards/matrices. |\n",
        "| Degradation-robust tracking | Put InvTrack as direct novelty boundary. | Cautious limitation framing from Group A/B. | InvTrack and degradation-robust tracking sources. |\n",
        "| Restoration-oriented Mamba | Explain restoration feature recovery and non-tracking objective. | Alireza-centered restoration papers plus MambaIR evidence. | MambaIR, MambaIRv2. |\n",
        "| Position of present work | Synthesize missing intersection without overclaiming. | Group A/B final bridge pattern. | Evidence matrices and claim audit. |\n\n",
        "## Bibliography Note\n\n",
        "Current `references.bib` contains only the existing core entries. Later rewrite must add any new Mamba-tracking, RGB-T tracking, or supervisor-corpus citation before use.\n",
    ]
    BLUEPRINT_MD.write_text("".join(blueprint), encoding="utf-8")


def main() -> int:
    meta = [r for r in read_csv(META) if r.get("included_in_analysis", "true") == "true"]
    features = read_csv(FEATURES)
    author_rows = [author_structure(r) for r in meta]
    author_by_id = {r["corpus_id"]: r for r in author_rows}
    pairs = pairwise_rows(meta, author_by_id, features)
    summary = group_summary(pairs, author_rows)
    write_csv(AUTHOR_OUT, author_rows)
    write_csv(PAIRWISE_OUT, pairs)
    write_csv(GROUP_OUT, summary)
    write_markdown(meta, author_rows, pairs, summary, features)
    print(f"papers={len(meta)} author_rows={len(author_rows)} pairs={len(pairs)} groups={dict(Counter(r['primary_group'] for r in author_rows))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
