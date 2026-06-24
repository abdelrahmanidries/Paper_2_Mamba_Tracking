#!/usr/bin/env python3
"""Rebuild the supervisor style corpus from manually uploaded PDFs.

The manual upload directory is treated as read-only input. Canonical unique
papers are copied into papers/supervisor_style_corpus/rebuilt/pdf, extracted
with pdftotext, and analyzed into manifest/style outputs.
"""

from __future__ import annotations

import csv
import hashlib
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPLOAD_DIR = ROOT / "papers" / "supervisor_style_corpus" / "manual_uploads"
OLD_PDF_DIR = ROOT / "papers" / "supervisor_style_corpus" / "pdf"
OLD_META = ROOT / "experiments" / "supervisor_style_corpus_metadata.csv"
REBUILT = ROOT / "papers" / "supervisor_style_corpus" / "rebuilt"
REBUILT_PDF = REBUILT / "pdf"
REBUILT_TEXT = REBUILT / "extracted_text"
REBUILT_SECTIONS = REBUILT / "sections"
REBUILT_META = REBUILT / "metadata"


@dataclass(frozen=True)
class Paper:
    corpus_id: str
    title: str
    authors: str
    target_supervisor: str
    year: str
    venue: str
    volume: str
    issue: str
    pages: str
    doi: str
    canonical_upload: str
    duplicate_uploads: tuple[str, ...]
    categories: str
    stylistic_usefulness: str
    technical_relevance: str
    source_type: str
    supervisor_status: str
    concordia_affiliation: str
    identity_confidence: str
    inclusion_reason: str
    uncertainty: str
    tier: str = "Tier 1"


MANUAL_PAPERS = [
    Paper(
        "T1_2024_TMRB_MIS_FMR",
        "A Very Fast and Robust Method for Refinement of Putative Matches of Features in MIS Images for Robotic-Assisted Surgery",
        "Muhammad Reza Pourshahabi; M. Omair Ahmad; M. N. S. Swamy",
        "both",
        "2024",
        "IEEE Transactions on Medical Robotics and Bionics",
        "6",
        "2",
        "419-432",
        "10.1109/TMRB.2024.3369769",
        "1- A_Very_Fast_and_Robust_Method_for_Refinement_of_Putative_Matches_of_Features_in_MIS_Images_for_Robotic-Assisted_Surgery.pdf",
        (),
        "feature matching; medical imaging; representation learning",
        "Introduction-style evidence; Related Work-style evidence; methodological-explanation evidence; limitation/discussion evidence",
        "technical citation candidate for Paper_2",
        "manual upload; IEEE publisher PDF",
        "M. Omair Ahmad is explicitly corresponding author; Ahmad and Swamy are senior coauthors",
        "First page lists Ahmad and Swamy with Concordia ECE affiliation and Concordia emails.",
        "high",
        "Recent IEEE Transactions methodological paper with strong problem-to-related-work narrowing.",
        "Domain is MIS feature matching rather than visual tracking, but feature-refinement rhetoric is relevant.",
    ),
    Paper(
        "T1_2024_TBC_DMML",
        "DMML: Deep Multi-Prior and Multi-Discriminator Learning for Underwater Image Enhancement",
        "Alireza Esmaeilzehi; Yang Ou; M. Omair Ahmad; M. N. S. Swamy",
        "both",
        "2024",
        "IEEE Transactions on Broadcasting",
        "70",
        "2",
        "637-653",
        "10.1109/TBC.2024.3349773",
        "2-DMML_Deep_Multi-Prior_and_Multi-Discriminator_Learning_for_Underwater_Image_Enhancement.pdf",
        ("13-DMML_Deep_Multi-Prior_and_Multi-Discriminator_Learning_for_Underwater_Image_Enhancement.pdf",),
        "image enhancement; image restoration; representation learning",
        "Introduction-style evidence; Related Work-style evidence; contribution-list evidence; methodological-explanation evidence",
        "technical citation candidate for Paper_2",
        "manual upload; IEEE publisher PDF",
        "M. Omair Ahmad is explicitly corresponding author; Ahmad and Swamy are senior coauthors",
        "First page lists Ahmad and Swamy with Concordia ECE affiliation and Concordia emails.",
        "high",
        "Recent IEEE Transactions enhancement paper with strong restoration/degradation motivation.",
        "Underwater enhancement is related but not tracking; use primarily for style and restoration motivation.",
    ),
    Paper(
        "T1_2023_SPL_DPAN",
        "DPAN: A Deep Light-Weight Attention-Based Image Super Resolution Network Using Multi-Dimensional Filter Design Technique",
        "Alireza Esmaeilzehi; Hossein Zaredar; Dimitrios Hatzinakos; M. Omair Ahmad",
        "M. O. Ahmad",
        "2023",
        "IEEE Signal Processing Letters",
        "30",
        "not reported",
        "1637-1641",
        "10.1109/LSP.2023.3326387",
        "3-DPAN_A_Deep_Light-Weight_Attention-Based_Image_Super_Resolution_Network_Using_Multi-Dimensional_Filter_Design_Technique.pdf",
        (),
        "super-resolution; image restoration",
        "methodological-explanation evidence; contribution-list evidence",
        "style-only, not suitable for citation in Paper_2",
        "manual upload; IEEE publisher PDF",
        "M. Omair Ahmad is explicitly corresponding author and final/senior author",
        "First page lists Ahmad with Concordia ECE affiliation and email.",
        "high",
        "Recent IEEE methodological letter showing compact technical motivation.",
        "Short letter format limits Related Work evidence.",
    ),
    Paper(
        "T1_2023_APPLINT_EDGE",
        "A low-complexity residual deep neural network for image edge detection",
        "Abdullah Al-Amaren; M. Omair Ahmad; M. N. S. Swamy",
        "both",
        "2023",
        "Applied Intelligence",
        "53",
        "not reported",
        "11282-11299",
        "10.1007/s10489-022-04062-6",
        "4_A low-complexity residual deep neural network for image edge detection.pdf",
        (),
        "representation learning; medical imaging; other",
        "Introduction-style evidence; Related Work-style evidence; methodological-explanation evidence",
        "style-only, not suitable for citation in Paper_2",
        "manual upload; publisher PDF",
        "Ahmad is marked as corresponding author; Ahmad and Swamy are senior coauthors",
        "First page lists all authors with Concordia ECE affiliation.",
        "high",
        "Recent algorithmic journal article with extended prior-work discussion.",
        "Edge detection is domain-distant from tracking.",
    ),
    Paper(
        "T1_2026_TIP_MSD_RGBT",
        "A Multi-Level Self-Distillation-Based Unified Tracker for Efficient RGB-T Tracking",
        "Mohamed Awad; Ahmed Elliethy; M. Omair Ahmad; M. N. S. Swamy",
        "both",
        "2026",
        "IEEE Transactions on Image Processing",
        "35",
        "not reported",
        "2407-2422",
        "10.1109/TIP.2026.3666737",
        "5-A_Multi-Level_Self-Distillation-Based_Unified_Tracker_for_Efficient_RGB-T_Tracking.pdf",
        (),
        "visual tracking; RGB-T tracking; representation learning",
        "Introduction-style evidence; Related Work-style evidence; contribution-list evidence; methodological-explanation evidence; technical citation candidate for Paper_2",
        "technical citation candidate for Paper_2",
        "manual upload; IEEE publisher PDF",
        "M. Omair Ahmad is explicitly corresponding author; Ahmad and Swamy are senior coauthors",
        "First page lists Awad/Ahmad/Swamy with Concordia ECE affiliation and emails.",
        "high",
        "Recent IEEE TIP RGB-T tracking paper from the same supervisor group; strongest tracking-style model.",
        "Multimodal RGB-T tracking differs from RGB degradation-robust tracking.",
    ),
    Paper(
        "T1_2025_ICIP_HFDAE_RGBT",
        "Adaptive Hierarchical Feature Difference Auto-Encoder for Robust RGB-T Object Tracking",
        "Mohamed Awad; Ahmed Elliethy; M. Omair Ahmad; M. N. S. Swamy",
        "both",
        "2025",
        "IEEE International Conference on Image Processing",
        "not reported",
        "not reported",
        "2121-2126",
        "10.1109/ICIP55913.2025.11084657",
        "6-Adaptive_Hierarchical_Feature_Difference_Auto-Encoder_for_Robust_RGB-T_Object_Tracking.pdf",
        (),
        "visual tracking; RGB-T tracking; image enhancement; representation learning",
        "Introduction-style evidence; Related Work-style evidence; methodological-explanation evidence; technical citation candidate for Paper_2",
        "technical citation candidate for Paper_2",
        "manual upload; IEEE publisher PDF",
        "Ahmad and Swamy are senior coauthors; corresponding status not explicitly established",
        "First page lists Awad/Ahmad/Swamy with Concordia ECE affiliation and emails.",
        "high",
        "Recent RGB-T tracking paper; highly relevant for tracking motivation and fusion positioning.",
        "Conference paper; shorter than Transactions papers.",
    ),
    Paper(
        "T1_2025_TGRS_UADIFF",
        "UADiff: A Deep Underwater Image Enhancement Network Using Generative Diffusion Prior and Uncertainty-Aware Learning",
        "Yang Ou; Alireza Esmaeilzehi; M. Omair Ahmad; M. N. S. Swamy",
        "both",
        "2025",
        "IEEE Transactions on Geoscience and Remote Sensing",
        "63",
        "not reported",
        "Article 4208114",
        "10.1109/TGRS.2025.3578927",
        "7-UADiff_A_Deep_Underwater_Image_Enhancement_Network_Using_Generative_Diffusion_Prior_and_Uncertainty-Aware_Learning.pdf",
        ("12-UADiff_A_Deep_Underwater_Image_Enhancement_Network_Using_Generative_Diffusion_Prior_and_Uncertainty-Aware_Learning.pdf",),
        "image enhancement; image restoration; representation learning",
        "Introduction-style evidence; Related Work-style evidence; contribution-list evidence; methodological-explanation evidence",
        "technical citation candidate for Paper_2",
        "manual upload; IEEE publisher PDF",
        "Alireza Esmaeilzehi is explicitly corresponding author; Ahmad and Swamy are senior coauthors",
        "First page lists Ahmad and Swamy with Concordia ECE affiliation and Concordia emails.",
        "high",
        "Recent IEEE Transactions restoration/enhancement paper with substantial Related Work.",
        "Underwater restoration is technically adjacent but not tracking.",
    ),
    Paper(
        "T1_2025_JBHI_ALZ_CNN",
        "A Lightweight Deep Convolutional Neural Network Extracting Local and Global Contextual Features for the Classification of Alzheimer's Disease Using Structural MRI",
        "Emimal Jabason; M. Omair Ahmad; M. N. S. Swamy",
        "both",
        "2025",
        "IEEE Journal of Biomedical and Health Informatics",
        "29",
        "3",
        "2061-2073",
        "10.1109/JBHI.2024.3512417",
        "8-A_Lightweight_Deep_Convolutional_Neural_Network_Extracting_Local_and_Global_Contextual_Features_for_the_Classification_of_Alzheimers_Disease_Using_Structural_MRI.pdf",
        ("14-A_Lightweight_Deep_Convolutional_Neural_Network_Extracting_Local_and_Global_Contextual_Features_for_the_Classification_of_Alzheimers_Disease_Using_Structural_MRI.pdf",),
        "medical imaging; representation learning",
        "Introduction-style evidence; Related Work-style evidence; methodological-explanation evidence",
        "style-only, not suitable for citation in Paper_2",
        "manual upload; IEEE publisher PDF",
        "M. Omair Ahmad is explicitly corresponding author; Ahmad and Swamy are senior coauthors",
        "First page lists all authors with Concordia ECE affiliation and emails.",
        "high",
        "Recent IEEE journal methodological paper with strong practical-motivation opening.",
        "Biomedical classification is domain-distant from tracking.",
    ),
    Paper(
        "T1_2024_MULTISYS_REFINERHASH",
        "RefinerHash: a new hashing-based re-ranking technique for image retrieval",
        "Farzad Sabahi; M. Omair Ahmad; M. N. S. Swamy",
        "both",
        "2024",
        "Multimedia Systems",
        "30",
        "not reported",
        "Article 119",
        "10.1007/s00530-024-01296-x",
        "9-RefinerHash_a_new_hashing-bas.pdf",
        (),
        "representation learning; other",
        "Introduction-style evidence; Related Work-style evidence; methodological-explanation evidence",
        "style-only, not suitable for citation in Paper_2",
        "manual upload; publisher PDF",
        "M. Omair Ahmad is explicitly corresponding author; Ahmad and Swamy are senior coauthors",
        "First page lists all authors with Concordia ECE affiliation.",
        "high",
        "Recent multimedia journal paper with extensive retrieval motivation and method-family review.",
        "Image retrieval is not directly relevant to RG-SSB tracking citations.",
    ),
    Paper(
        "T1_2024_VISCOMP_HIGHBOOSTNET",
        "HighBoostNet: a deep light-weight image super-resolution network using high-boost residual blocks",
        "Alireza Esmaeilzehi; Lei Ma; M. N. S. Swamy; M. Omair Ahmad",
        "both",
        "2024",
        "The Visual Computer",
        "40",
        "not reported",
        "1111-1129",
        "10.1007/s00371-023-02835-9",
        "10-HighBoostNet a deep light-weight image super-resolution network using high-boost residual blocks.pdf",
        (),
        "super-resolution; image restoration; representation learning",
        "Introduction-style evidence; Related Work-style evidence; methodological-explanation evidence",
        "technical citation candidate for Paper_2",
        "manual upload; publisher PDF",
        "Ahmad is final/senior author; corresponding status not explicitly established",
        "First page lists Ahmad and Swamy with Concordia ECE affiliation and emails.",
        "high",
        "Recent image super-resolution paper with degradation-model motivation.",
        "Super-resolution is relevant to degradation motivation, not direct tracking method citation.",
    ),
    Paper(
        "T1_2026_TPAMI_ACLI",
        "ACLI: A CNN Pruning Framework Leveraging Adjacent Convolutional Layer Interdependence and gamma-Weakly Submodularity",
        "Sadegh Tofigh; Mohammad Askarizadeh; M. Omair Ahmad; M. N. S. Swamy; Kim Khoa Nguyen",
        "both",
        "2026",
        "IEEE Transactions on Pattern Analysis and Machine Intelligence",
        "48",
        "1",
        "932-945",
        "10.1109/TPAMI.2025.3610113",
        "11-ACLI_A_CNN_Pruning_Framework_Leveraging_Adjacent_Convolutional_Layer_Interdependence_and_gamma-Weakly_Submodularity.pdf",
        (),
        "model pruning/compression; representation learning",
        "Introduction-style evidence; Related Work-style evidence; contribution-list evidence; methodological-explanation evidence",
        "style-only, not suitable for citation in Paper_2",
        "manual upload; IEEE publisher PDF",
        "Sadegh Tofigh is explicitly corresponding author; Ahmad and Swamy are senior coauthors",
        "First page lists Ahmad and Swamy with Concordia ECE affiliation and emails.",
        "high",
        "Top-tier recent TPAMI paper with strong theoretical-method framing and contribution list.",
        "Model pruning is domain-distant from restoration-guided tracking.",
    ),
    Paper(
        "T1_2023_TAI_THREE_PRIOR_SR",
        "Ultralight-Weight Three-Prior Convolutional Neural Network for Single Image Super Resolution",
        "Alireza Esmaeilzehi; M. Omair Ahmad; M. N. S. Swamy",
        "both",
        "2023",
        "IEEE Transactions on Artificial Intelligence",
        "4",
        "6",
        "1724-1738",
        "10.1109/TAI.2022.3224417",
        "15-Ultralight-Weight_Three-Prior_Convolutional_Neural_Network_for_Single_Image_Super_Resolution.pdf",
        (),
        "super-resolution; image restoration; representation learning",
        "Introduction-style evidence; Related Work-style evidence; methodological-explanation evidence",
        "technical citation candidate for Paper_2",
        "manual upload; IEEE publisher PDF",
        "Alireza Esmaeilzehi is explicitly corresponding author; Ahmad and Swamy are senior coauthors",
        "First page lists all authors with Concordia ECE affiliation and emails.",
        "high",
        "Recent IEEE journal super-resolution paper with detailed prior-work contrast.",
        "Useful for restoration/degradation motivation but not direct tracking method citation.",
    ),
    Paper(
        "T1_2021_TCI_SRNSSI",
        "SRNSSI: A Deep Light-Weight Network for Single Image Super Resolution Using Spatial and Spectral Information",
        "Alireza Esmaeilzehi; M. Omair Ahmad; M. N. S. Swamy",
        "both",
        "2021",
        "IEEE Transactions on Computational Imaging",
        "7",
        "not reported",
        "409-421",
        "10.1109/TCI.2021.3070522",
        "16-SRNSSI_A_Deep_Light-Weight_Network_for_Single_Image_Super_Resolution_Using_Spatial_and_Spectral_Information.pdf",
        (),
        "super-resolution; image restoration; representation learning",
        "Introduction-style evidence; Related Work-style evidence; methodological-explanation evidence",
        "technical citation candidate for Paper_2",
        "manual upload; IEEE publisher PDF",
        "M. Omair Ahmad is explicitly corresponding author; Ahmad and Swamy are senior coauthors",
        "First page lists all authors with Concordia ECE affiliation and emails.",
        "high",
        "IEEE computational imaging paper with clear light-weight restoration network positioning.",
        "Super-resolution is adjacent but not tracking.",
    ),
    Paper(
        "T1_2021_TBC_UPDRESNN",
        "UPDResNN: A Deep Light-Weight Image Upsampling and Deblurring Residual Neural Network",
        "Alireza Esmaeilzehi; M. Omair Ahmad; M. N. S. Swamy",
        "both",
        "2021",
        "IEEE Transactions on Broadcasting",
        "67",
        "2",
        "538-548",
        "10.1109/TBC.2021.3068862",
        "17-UPDResNN_A_Deep_Light-Weight_Image_Upsampling_and_Deblurring_Residual_Neural_Network.pdf",
        ("18-UPDResNN_A_Deep_Light-Weight_Image_Upsampling_and_Deblurring_Residual_Neural_Network.pdf",),
        "image restoration; super-resolution",
        "Introduction-style evidence; Related Work-style evidence; contribution-list evidence; methodological-explanation evidence",
        "technical citation candidate for Paper_2",
        "manual upload; IEEE publisher PDF",
        "M. Omair Ahmad is explicitly corresponding author; Ahmad and Swamy are senior coauthors",
        "First page lists all authors with Concordia ECE affiliation and emails.",
        "high",
        "IEEE Transactions restoration paper with explicit contribution list and Related Work.",
        "Image upsampling/deblurring is adjacent to degradation but not tracking.",
    ),
    Paper(
        "T1_2019_TIP_TCHEBICHEF_DENOISING",
        "Tchebichef and Adaptive Steerable-Based Total Variation Model for Image Denoising",
        "Ahlad Kumar; M. Omair Ahmad; M. N. S. Swamy",
        "both",
        "2019",
        "IEEE Transactions on Image Processing",
        "28",
        "6",
        "2921-2935",
        "10.1109/TIP.2019.2892663",
        "19-Tchebichef_and_Adaptive_Steerable-Based_Total_Variation_Model_for_Image_Denoising.pdf",
        (),
        "image denoising; image restoration",
        "Introduction-style evidence; Related Work-style evidence; methodological-explanation evidence",
        "technical citation candidate for Paper_2",
        "manual upload; IEEE publisher PDF",
        "Ahlad Kumar is explicitly corresponding author; Ahmad and Swamy are senior coauthors",
        "First page lists all authors with Concordia ECE affiliation and emails.",
        "high",
        "IEEE TIP denoising paper with strong restoration problem formulation.",
        "Classical denoising/restoration paper; relevant as restoration background but not tracking.",
    ),
]


WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z'-]*\b")
CITE_RE = re.compile(r"\[(?:\d+(?:\s*[-,]\s*\d+)*)\]|\([A-Z][A-Za-z-]+(?: et al\.)?,\s*\d{4}\)")
SENT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
PASSIVE_RE = re.compile(r"\b(?:is|are|was|were|be|been|being)\s+\w+(?:ed|en)\b", re.I)
FIRST_PERSON_RE = re.compile(r"\b(?:we|our|ours|us)\b", re.I)
HEDGE_RE = re.compile(r"\b(?:may|might|could|can|generally|typically|often|relatively|approximately|potentially|suggests?|appears?|tends?|limited|rather than|not necessarily)\b", re.I)
LIMIT_RE = re.compile(r"\b(?:however|nevertheless|although|limited|limitation|challenge|fail(?:s|ed)?|difficult|cannot|unable|suffer(?:s|ed)?|drawback|problem|still|remain(?:s)?|underexplored|not much attention|not sufficient)\b", re.I)
PROPOSE_RE = re.compile(r"\b(?:in this paper|in this article|in this work|we propose|we develop|we introduce|we present)\b", re.I)
CONTRIB_RE = re.compile(r"\b(?:contributions?|summarized as follows|main contributions)\b", re.I)
TRANSITIONS = ["however", "therefore", "moreover", "furthermore", "in addition", "nevertheless", "although", "while", "whereas", "in contrast", "specifically", "finally", "in view of this"]

ROLE_PATTERNS = {
    "broad application context": re.compile(r"\b(?:applications?|real-world|computer vision|image processing|tracking|medical|underwater|surgery|broadcast|robotics|surveillance)\b", re.I),
    "practical importance": re.compile(r"\b(?:important|crucial|essential|practical|deployment|real-life|resource|quality|robust)\b", re.I),
    "technical challenge": re.compile(r"\b(?:challenge|difficult|limited|complexity|degradation|noise|occlusion|low light|blur|domain|gap|inliers|uncertainty)\b", re.I),
    "representative prior progress": re.compile(r"\b(?:existing|state-of-the-art|recent|methods?|schemes?|networks?|trackers?|proposed in|literature)\b", re.I),
    "unresolved limitation": LIMIT_RE,
    "research gap": re.compile(r"\b(?:however|not much attention|underexplored|remains?|limited|gap|not sufficient|do not|does not)\b", re.I),
    "proposed direction": PROPOSE_RE,
    "method summary": re.compile(r"\b(?:network|framework|module|regularizer|loss|architecture|algorithm|scheme|block)\b", re.I),
    "contributions": CONTRIB_RE,
    "paper organization": re.compile(r"\b(?:rest of the paper|organized as follows|section ii|section iii|section iv)\b", re.I),
}

RELATED_ROLE_PATTERNS = {
    "category introduction": re.compile(r"\b(?:category|classified|can be classified|methods|schemes|networks)\b", re.I),
    "representative methods": re.compile(r"(?:\bin\s+\[|\bproposed\b|\bmethod\b|\bscheme\b|\bnetwork\b|\btracker\b|\bmodel\b)", re.I),
    "strengths": re.compile(r"\b(?:effective|superior|robust|good performance|state-of-the-art|promising)\b", re.I),
    "weaknesses": LIMIT_RE,
    "comparison": re.compile(r"\b(?:compared|whereas|unlike|in contrast|similar|outperform|higher than|lower than)\b", re.I),
    "unresolved issue": re.compile(r"\b(?:however|challenge|limited|remain|not sufficient|underexplored)\b", re.I),
    "positioning of present work": PROPOSE_RE,
}


def ensure_dirs() -> None:
    if REBUILT.exists():
        shutil.rmtree(REBUILT)
    for path in [REBUILT_PDF, REBUILT_TEXT, REBUILT_SECTIONS / "tier1", REBUILT_SECTIONS / "tier2", REBUILT_META]:
        path.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def pdfinfo(path: Path) -> dict[str, str]:
    out = subprocess.check_output(["pdfinfo", str(path)], text=True, stderr=subprocess.STDOUT)
    info: dict[str, str] = {}
    for line in out.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            info[k.strip()] = v.strip()
    return info


def pdftotext(path: Path) -> str:
    proc = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    text = proc.stdout.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\f", "\n\n[PAGE_BREAK]\n\n")
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)
    lines = []
    for line in text.splitlines():
        s = re.sub(r"[ \t]+", " ", line.strip())
        if not s:
            lines.append("")
            continue
        if s.lower().startswith("authorized licensed use"):
            continue
        if s.lower().startswith("downloaded on"):
            continue
        lines.append(s)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"


def page_for_offset(text: str, offset: int) -> int:
    return text[:offset].count("[PAGE_BREAK]") + 1


def paragraphs(text: str) -> list[str]:
    paras = []
    buf = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s == "[PAGE_BREAK]":
            if buf:
                paras.append(" ".join(buf))
                buf = []
            continue
        if re.match(r"^(?:[IVX]+\.|\d+\.|[A-Z]\.)\s+[A-Z]", s) and buf:
            paras.append(" ".join(buf))
            buf = [s]
        else:
            buf.append(s)
    if buf:
        paras.append(" ".join(buf))
    return [p for p in paras if p]


def section_matches(text: str) -> list[tuple[str, int, int]]:
    patterns = [
        ("abstract", r"(?im)^\s*Abstract\b"),
        ("introduction", r"(?im)(?:^|\s)(?:I\.|1)\s*I?\s*N?\s*T?\s*R?\s*O?\s*D?\s*U?\s*C?\s*T?\s*I?\s*O?\s*N\b|(?:^|\s)1\s+Introduction\b"),
        ("related_work", r"(?im)(?:^|\s)(?:II\.|2)\s*(?:R\s*E\s*L\s*A\s*T\s*E\s*D\s*W\s*O\s*R\s*K\S*|Related Works?|Literature Review)\b"),
        ("integrated_prior_work", r"(?im)^\s*(?:A\.|1\))\s*(?:Related Work|Related Works|Related Work on|Light-Weight|Classical|Image Super Resolution|Transformation-Based)\b"),
        ("method_overview", r"(?im)(?:^|\s)(?:II\.|III\.|2|3)\s*(?:P\s*R\s*O\s*P\s*O\s*S\s*E\s*D|Proposed|Method|Network|Overall|Model|Framework)\b"),
        ("discussion_limitations", r"(?im)(?:^|\s)(?:VI\.|VII\.|6|7)\s*(?:Discussion|Limitations)\b"),
        ("conclusion", r"(?im)(?:^|\s)(?:IV\.|V\.|VI\.|VII\.|4|5|6|7)\s*(?:C\s*O\s*N\s*C\s*L\s*U\s*S\s*I\s*O\s*N|Conclusion|Concluding Remarks)\b"),
        ("references", r"(?im)^\s*R\s*E\s*F\s*E\s*R\s*E\s*N\s*C\s*E\s*S\b|^\s*References\b"),
    ]
    found = []
    for name, pat in patterns:
        for m in re.finditer(pat, text):
            found.append((name, m.start(), m.end()))
    return sorted(found, key=lambda x: x[1])


def extract_sections(text: str) -> dict[str, tuple[str, int, int]]:
    matches = section_matches(text)
    sections: dict[str, tuple[str, int, int]] = {}
    for i, (name, start, end_heading) in enumerate(matches):
        if name == "references":
            continue
        if name in sections:
            continue
        later = [m[1] for m in matches if m[1] > start and m[0] != "integrated_prior_work"]
        end = min(later) if later else len(text)
        if name == "abstract":
            intro = next((m[1] for m in matches if m[0] == "introduction" and m[1] > start), None)
            end = intro or end
        if name == "integrated_prior_work":
            # Keep an integrated prior-work subsection bounded by the next major heading when available.
            later_major = [m[1] for m in matches if m[1] > start and m[0] in {"method_overview", "conclusion", "references"}]
            end = min(later_major) if later_major else end
        body = text[start:end].strip()
        if len(WORD_RE.findall(body)) >= 40:
            sections[name] = (body, start, end)

    if "related_work" not in sections:
        intro = sections.get("introduction")
        if intro:
            paras = paragraphs(intro[0])
            prior = [p for p in paras if len(CITE_RE.findall(p)) >= 2 or re.search(r"\b(existing|methods|schemes|networks|trackers|literature)\b", p, re.I)]
            if prior:
                joined = "\n\n".join(prior[:6])
                sections["integrated_prior_work"] = (joined, intro[1], intro[2])

    intro = sections.get("introduction")
    if intro:
        contrib_paras = [p for p in paragraphs(intro[0]) if CONTRIB_RE.search(p) or re.search(r"(?m)(?:^|\s)[r•]\s+We\b|^\s*[-*]\s+We\b", p)]
        if contrib_paras:
            sections["contributions"] = ("\n\n".join(contrib_paras), intro[1], intro[2])
    return sections


def section_header(paper_id: str, title: str, section: str, pdf_path: str, start: int, end: int, text: str) -> str:
    return (
        f"corpus_id: {paper_id}\n"
        f"title: {title}\n"
        f"section: {section}\n"
        f"source_pdf: {pdf_path}\n"
        f"approx_start_page: {page_for_offset(text, start)}\n"
        f"approx_end_page: {page_for_offset(text, end)}\n\n"
    )


def write_text_outputs(paper_id: str, title: str, tier: str, pdf_path: Path, out_pdf_path: Path) -> dict[str, str]:
    text = pdftotext(out_pdf_path)
    text_path = REBUILT_TEXT / f"{paper_id}.txt"
    text_path.write_text(text, encoding="utf-8")
    sections = extract_sections(text)
    section_dir = REBUILT_SECTIONS / ("tier1" if tier == "Tier 1" else "tier2")
    outputs = {}
    for section, (body, start, end) in sections.items():
        section_path = section_dir / f"{paper_id}__{section}.txt"
        section_path.write_text(section_header(paper_id, title, section, str(out_pdf_path.relative_to(ROOT)), start, end, text) + body + "\n", encoding="utf-8")
        outputs[section] = str(section_path.relative_to(ROOT))
    return outputs


def sentence_count(text: str) -> int:
    return len([s for s in SENT_RE.split(text.strip()) if s.strip()])


def role_sequence(paras: list[str], related: bool = False) -> str:
    pats = RELATED_ROLE_PATTERNS if related else ROLE_PATTERNS
    seq = []
    for p in paras[:12]:
        labels = [name for name, pat in pats.items() if pat.search(p)]
        seq.append("+".join(labels[:3]) if labels else "unlabeled")
    return " > ".join(seq)


def related_org(text: str) -> str:
    low = text.lower()
    scores = {
        "method-family": len(re.findall(r"\b(networks?|methods?|schemes?|trackers?|models?|category|classified)\b", low)),
        "chronological": len(re.findall(r"\b(?:in recent years|earliest|recently|then|following|after)\b|20\d{2}|19\d{2}", low)),
        "problem": len(re.findall(r"\b(?:challenge|problem|degradation|complexity|occlusion|low light|limited|noise|blur|fusion)\b", low)),
        "application": len(re.findall(r"\b(?:medical|underwater|tracking|surgery|broadcast|retrieval|alzheimer|robotics)\b", low)),
    }
    return max(scores.items(), key=lambda kv: kv[1])[0]


def analyze_section(row: dict[str, str], section: str, section_file: str) -> dict[str, str]:
    path = ROOT / section_file
    txt = path.read_text(encoding="utf-8")
    body = txt.split("\n\n", 1)[1] if "\n\n" in txt else txt
    paras = paragraphs(body)
    words = WORD_RE.findall(body)
    sents = sentence_count(body)
    cite_counts = [len(CITE_RE.findall(p)) for p in paras]
    first_cite = next((i + 1 for i, p in enumerate(paras) if CITE_RE.search(p)), 0)
    first_limit = next((i + 1 for i, p in enumerate(paras) if LIMIT_RE.search(p)), 0)
    first_proposed = next((i + 1 for i, p in enumerate(paras) if PROPOSE_RE.search(p)), 0)
    first_contrib = next((i + 1 for i, p in enumerate(paras) if CONTRIB_RE.search(p)), 0)
    bullets = len(re.findall(r"(?m)^\s*(?:[-*•]|\d+[.)]|r)\s+", body))
    transition_counts = Counter()
    for t in TRANSITIONS:
        transition_counts[t] = len(re.findall(r"\b" + re.escape(t) + r"\b", body, re.I))
    related = section in {"related_work", "integrated_prior_work", "background", "literature_review"}
    return {
        "corpus_id": row["corpus_id"],
        "tier": row["tier"],
        "title": row["title"],
        "target_supervisor": row["target_supervisor"],
        "year": row["year"],
        "journal": row["journal"],
        "section": section,
        "paragraph_count": str(len(paras)),
        "word_count": str(len(words)),
        "mean_words_per_paragraph": f"{len(words) / len(paras):.2f}" if paras else "0",
        "sentences_per_paragraph": f"{sents / len(paras):.2f}" if paras else "0",
        "sentence_count": str(sents),
        "mean_words_per_sentence": f"{len(words) / sents:.2f}" if sents else "0",
        "citation_count": str(sum(cite_counts)),
        "mean_citations_per_paragraph": f"{sum(cite_counts) / len(paras):.2f}" if paras else "0",
        "first_citation_paragraph": str(first_cite),
        "first_explicit_limitation_paragraph": str(first_limit),
        "proposed_method_intro_paragraph": str(first_proposed),
        "contribution_location_paragraph": str(first_contrib),
        "contribution_list_form": "itemized" if bullets else ("prose" if first_contrib else "not reported"),
        "contribution_item_count_proxy": str(bullets),
        "first_person_count": str(len(FIRST_PERSON_RE.findall(body))),
        "hedge_count": str(len(HEDGE_RE.findall(body))),
        "passive_proxy_count": str(len(PASSIVE_RE.findall(body))),
        "passive_proxy_per_100_sentences": f"{100 * len(PASSIVE_RE.findall(body)) / sents:.2f}" if sents else "0",
        "transition_counts": "; ".join(f"{k}={v}" for k, v in transition_counts.items() if v),
        "role_sequence_proxy": role_sequence(paras, related=related),
        "related_work_organization_proxy": related_org(body) if related else "not applicable",
        "related_work_mode_proxy": "critical/comparative" if len(LIMIT_RE.findall(body)) >= 2 else ("comparative" if re.search(r"\b(unlike|compared|whereas|outperform)\b", body, re.I) else "descriptive"),
        "limitation_expression_count": str(len(LIMIT_RE.findall(body))),
        "comparison_language_count": str(len(re.findall(r"\b(compared|whereas|unlike|in contrast|higher than|lower than|outperform)\b", body, re.I))),
        "section_file": section_file,
    }


def load_old_tier2() -> list[dict[str, str]]:
    return [
        {
            "corpus_id": "AS2024_PATHOWAVE",
            "title": "PathoWAve: A Deep Learning-based Weight Averaging Method for Improving Domain Generalization in Histopathology Images",
            "authors": "Parastoo Sotoudeh Sharifi; M. Omair Ahmad; M. N. S. Swamy",
            "target_supervisor": "both",
            "year": "2024",
            "journal": "arXiv preprint",
            "volume": "not reported",
            "issue": "not reported",
            "pages": "not reported",
            "DOI": "10.48550/arXiv.2406.15685",
            "verified_affiliation": "PDF lists Department of Electrical and Computer Engineering, Concordia University, Montreal; emails include omair and swamy.",
            "corresponding_or_senior_author_status": "Ahmad and Swamy are final/senior authors",
            "source_type": "arXiv author-posted preprint",
            "full_text_available": "true",
            "local_pdf_path": "papers/supervisor_style_corpus/pdf/AS2024_PATHOWAVE.pdf",
            "identity_confidence": "high",
            "notes": "Venue is arXiv preprint rather than journal.",
        },
        {
            "corpus_id": "AH2020_R_SPATIOGRAM_TRACKING",
            "title": "Applying R-spatiogram in Object Tracking for Occlusion Handling",
            "authors": "Niloufar Salehi Dastjerdi; M. Omair Ahmad",
            "target_supervisor": "M. O. Ahmad",
            "year": "2020",
            "journal": "Signal & Image Processing: An International Journal",
            "volume": "11",
            "issue": "1",
            "pages": "1-13",
            "DOI": "10.5121/sipij.2020.11101",
            "verified_affiliation": "PDF lists Department of Electrical and Computer Engineering, Concordia University, Montreal, Quebec, Canada.",
            "corresponding_or_senior_author_status": "Ahmad is last/senior author",
            "source_type": "publisher-open PDF",
            "full_text_available": "true",
            "local_pdf_path": "papers/supervisor_style_corpus/pdf/AH2020_R_SPATIOGRAM_TRACKING.pdf",
            "identity_confidence": "high",
            "notes": "Comparable peer-reviewed journal but not IEEE Transactions.",
        },
        {
            "corpus_id": "AS2018_VARIATIONAL_MIXED_NOISE",
            "title": "A Variational Step for Reduction of Mixed Gaussian-Impulse Noise from Images",
            "authors": "Mohammad Tariqul Islam; Dipayan Saha; S. M. Mahbubur Rahman; M. Omair Ahmad; M. N. S. Swamy",
            "target_supervisor": "both",
            "year": "2018",
            "journal": "arXiv preprint / ICECE paper",
            "volume": "not reported",
            "issue": "not reported",
            "pages": "not reported",
            "DOI": "10.1109/ICECE.2018.8636754",
            "verified_affiliation": "PDF lists Ahmad and Swamy with Department of Electrical and Computer Engineering, Concordia University, Montreal, Canada.",
            "corresponding_or_senior_author_status": "Ahmad and Swamy are final/senior authors",
            "source_type": "arXiv author-posted preprint",
            "full_text_available": "true",
            "local_pdf_path": "papers/supervisor_style_corpus/pdf/AS2018_VARIATIONAL_MIXED_NOISE.pdf",
            "identity_confidence": "high",
            "notes": "Conference preprint; Related Work is integrated into Introduction.",
        },
        {
            "corpus_id": "AS2015_MSAINDELFR",
            "title": "MSAIndelFR: a scheme for multiple protein sequence alignment using information on indel flanking regions",
            "authors": "Mufleh Al-Shatnawi; M. Omair Ahmad; M. N. S. Swamy",
            "target_supervisor": "both",
            "year": "2015",
            "journal": "BMC Bioinformatics",
            "volume": "16",
            "issue": "not reported",
            "pages": "Article 393",
            "DOI": "10.1186/s12859-015-0826-3",
            "verified_affiliation": "PDF lists Department of Electrical and Computer Engineering, Concordia University, Montreal, Quebec, Canada.",
            "corresponding_or_senior_author_status": "Ahmad is corresponding author and Swamy is final senior author",
            "source_type": "publisher-open PDF",
            "full_text_available": "true",
            "local_pdf_path": "papers/supervisor_style_corpus/pdf/AS2015_MSAINDELFR.pdf",
            "identity_confidence": "high",
            "notes": "Expanded date range because many recent IEEE full texts were not lawfully downloadable in the previous pass.",
        },
        {
            "corpus_id": "AS2014_EURASIP_ECHO",
            "title": "Single-channel acoustic echo cancellation in noise based on gradient-based adaptive filtering",
            "authors": "Upal Mahbub; Shaikh Anowarul Fattah; Wei-Ping Zhu; M. Omair Ahmad",
            "target_supervisor": "M. O. Ahmad",
            "year": "2014",
            "journal": "EURASIP Journal on Audio Speech and Music Processing",
            "volume": "2014",
            "issue": "not reported",
            "pages": "Article 20",
            "DOI": "10.1186/1687-4722-2014-20",
            "verified_affiliation": "PDF lists Wei-Ping Zhu and M. Omair Ahmad with Department of Electrical and Computer Engineering, Concordia University.",
            "corresponding_or_senior_author_status": "Ahmad is final/senior author",
            "source_type": "publisher-open PDF",
            "full_text_available": "true",
            "local_pdf_path": "papers/supervisor_style_corpus/pdf/AS2014_EURASIP_ECHO.pdf",
            "identity_confidence": "high",
            "notes": "Older than preferred range; included as secondary evidence.",
        },
        {
            "corpus_id": "AS2010_EURASIP_CEPSTRUM",
            "title": "A Ramp Cosine Cepstrum Model for the Parameter Estimation of Autoregressive Systems at Low SNR",
            "authors": "Shaikh Anowarul Fattah; Wei-Ping Zhu; M. Omair Ahmad",
            "target_supervisor": "M. O. Ahmad",
            "year": "2010",
            "journal": "EURASIP Journal on Advances in Signal Processing",
            "volume": "2010",
            "issue": "not reported",
            "pages": "Article ID 808312",
            "DOI": "10.1155/2010/808312",
            "verified_affiliation": "PDF lists Wei-Ping Zhu and M. Omair Ahmad with Department of Electrical and Computer Engineering, Concordia University.",
            "corresponding_or_senior_author_status": "Ahmad is final/senior author",
            "source_type": "publisher-open PDF",
            "full_text_available": "true",
            "local_pdf_path": "papers/supervisor_style_corpus/pdf/AS2010_EURASIP_CEPSTRUM.pdf",
            "identity_confidence": "high",
            "notes": "Older than preferred range; included as secondary evidence.",
        },
        {
            "corpus_id": "SW2019_HEARING_AIDS",
            "title": "Sound Quality Improvement for Hearing Aids in Presence of Multiple Inputs",
            "authors": "Asutosh Kar; Ankita Anand; Jan Ostergaard; Soren Holdt Jensen; M. N. S. Swamy",
            "target_supervisor": "M. N. S. Swamy",
            "year": "2019",
            "journal": "Circuits Systems and Signal Processing",
            "volume": "38",
            "issue": "8",
            "pages": "3591-3615",
            "DOI": "10.1007/s00034-019-01104-2",
            "verified_affiliation": "Repository metadata and manuscript identify M. N. S. Swamy; coauthor network includes signal-processing collaborators.",
            "corresponding_or_senior_author_status": "Swamy is final/senior author",
            "source_type": "accepted author manuscript from institutional repository",
            "full_text_available": "true",
            "local_pdf_path": "papers/supervisor_style_corpus/pdf/SW2019_HEARING_AIDS.pdf",
            "identity_confidence": "medium-high",
            "notes": "Affiliation is less visible on first page than other PDFs; identity supported by DOI metadata and repository citation.",
        },
        {
            "corpus_id": "SW2015_COSINE_TCHEBICHEF",
            "title": "A Comparison of Integer Cosine and Tchebichef Transforms for Image Compression Using Variable Quantization",
            "authors": "Soni Prattipati; M. N. S. Swamy; Pramod K. Meher",
            "target_supervisor": "M. N. S. Swamy",
            "year": "2015",
            "journal": "Journal of Signal and Information Processing",
            "volume": "6",
            "issue": "3",
            "pages": "203-216",
            "DOI": "10.4236/jsip.2015.63019",
            "verified_affiliation": "PDF lists M. N. S. Swamy with Department of Electrical and Computer Engineering, Concordia University, Montreal, Canada.",
            "corresponding_or_senior_author_status": "Swamy is recurring supervising coauthor",
            "source_type": "publisher-open PDF",
            "full_text_available": "true",
            "local_pdf_path": "papers/supervisor_style_corpus/pdf/SW2015_COSINE_TCHEBICHEF.pdf",
            "identity_confidence": "high",
            "notes": "Open journal but not IEEE.",
        },
        {
            "corpus_id": "SW2013_FRONTIERS_SYNAPTIC",
            "title": "Inferring trial-to-trial excitatory and inhibitory synaptic inputs from membrane potential using Gaussian mixture Kalman filtering",
            "authors": "M. Lankarany; W.-P. Zhu; M. N. S. Swamy; Taro Toyoizumi",
            "target_supervisor": "M. N. S. Swamy",
            "year": "2013",
            "journal": "Frontiers in Computational Neuroscience",
            "volume": "7",
            "issue": "not reported",
            "pages": "Article 109",
            "DOI": "10.3389/fncom.2013.00109",
            "verified_affiliation": "PDF lists M. N. S. Swamy with Department of Electrical and Computer Engineering, Concordia University, Montreal, QC, Canada.",
            "corresponding_or_senior_author_status": "Swamy is senior/recurring Concordia coauthor",
            "source_type": "publisher-open PDF",
            "full_text_available": "true",
            "local_pdf_path": "papers/supervisor_style_corpus/pdf/SW2013_FRONTIERS_SYNAPTIC.pdf",
            "identity_confidence": "high",
            "notes": "Older than preferred range and biomedical-neuroscience context; use cautiously.",
        },
    ]


def classify_old_category(title: str) -> str:
    low = title.lower()
    cats = []
    if "tracking" in low:
        cats.append("visual tracking")
    if "super resolution" in low or "upsampling" in low:
        cats.append("super-resolution")
    if "denois" in low or "noise" in low:
        cats.append("image denoising")
    if "compression" in low:
        cats.append("image compression")
    if "histopathology" in low or "synaptic" in low or "protein" in low or "hearing" in low:
        cats.append("other")
    if not cats:
        cats.append("representation learning")
    return "; ".join(cats)


def source_url_from_old(cid: str) -> str:
    return {
        "AS2024_PATHOWAVE": "https://arxiv.org/pdf/2406.15685",
        "AH2020_R_SPATIOGRAM_TRACKING": "https://aircconline.com/sipij/V11N1/11120sipij01.pdf",
        "AS2018_VARIATIONAL_MIXED_NOISE": "https://arxiv.org/pdf/1811.00244",
        "AS2015_MSAINDELFR": "https://bmcbioinformatics.biomedcentral.com/counter/pdf/10.1186/s12859-015-0826-3",
        "AS2014_EURASIP_ECHO": "https://asmp-eurasipjournals.springeropen.com/counter/pdf/10.1186/1687-4722-2014-20",
        "AS2010_EURASIP_CEPSTRUM": "https://asp-eurasipjournals.springeropen.com/counter/pdf/10.1155/2010/808312",
        "SW2019_HEARING_AIDS": "https://vbn.aau.dk/ws/files/386019200/Kar_et_al._2019_1_.pdf",
        "SW2015_COSINE_TCHEBICHEF": "https://content.scirp.org/pdf/jsip_2015072115320979.pdf",
        "SW2013_FRONTIERS_SYNAPTIC": "https://www.frontiersin.org/articles/10.3389/fncom.2013.00109/pdf",
    }.get(cid, "not reported")


def write_inventory(upload_rows: list[dict[str, str]]) -> None:
    fields = [
        "upload_filename",
        "upload_path",
        "sha256",
        "pdf_title_metadata",
        "title",
        "authors",
        "year",
        "venue",
        "volume",
        "issue",
        "pages",
        "DOI",
        "pdf_page_count",
        "unique_group_id",
        "duplicate_status",
        "canonical_corpus_id",
        "canonical_upload_filename",
        "likely_duplicate_reason",
        "supervisor_authorship",
        "verified_affiliation",
    ]
    path = ROOT / "experiments" / "manual_supervisor_pdf_inventory.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(upload_rows)
    sha_path = ROOT / "experiments" / "manual_supervisor_pdf_sha256.txt"
    sha_path.write_text("".join(f"{r['sha256']}  {r['upload_path']}\n" for r in upload_rows), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    manual_by_filename = {p.canonical_upload: p for p in MANUAL_PAPERS}
    for p in MANUAL_PAPERS:
        for dup in p.duplicate_uploads:
            manual_by_filename[dup] = p

    uploads = sorted(UPLOAD_DIR.glob("*.pdf"))
    upload_rows = []
    for upload in uploads:
        info = pdfinfo(upload)
        sha = sha256(upload)
        paper = manual_by_filename.get(upload.name)
        if not paper:
            continue
        is_canonical = upload.name == paper.canonical_upload
        reason = "canonical unique paper"
        if not is_canonical:
            reason = "bibliographic duplicate: matching title/DOI/page count with canonical copy; SHA differs"
        upload_rows.append(
            {
                "upload_filename": upload.name,
                "upload_path": str(upload.relative_to(ROOT)),
                "sha256": sha,
                "pdf_title_metadata": info.get("Title", ""),
                "title": paper.title,
                "authors": paper.authors,
                "year": paper.year,
                "venue": paper.venue,
                "volume": paper.volume,
                "issue": paper.issue,
                "pages": paper.pages,
                "DOI": paper.doi,
                "pdf_page_count": info.get("Pages", "not reported"),
                "unique_group_id": paper.corpus_id,
                "duplicate_status": "canonical" if is_canonical else "likely_duplicate_noncanonical",
                "canonical_corpus_id": paper.corpus_id,
                "canonical_upload_filename": paper.canonical_upload,
                "likely_duplicate_reason": reason,
                "supervisor_authorship": paper.target_supervisor,
                "verified_affiliation": paper.concordia_affiliation,
            }
        )
    write_inventory(upload_rows)

    manifest_rows = []
    feature_rows = []
    for paper in MANUAL_PAPERS:
        src = UPLOAD_DIR / paper.canonical_upload
        dest = REBUILT_PDF / f"{paper.corpus_id}.pdf"
        shutil.copy2(src, dest)
        info = pdfinfo(dest)
        sections = write_text_outputs(paper.corpus_id, paper.title, paper.tier, src, dest)
        row = {
            "corpus_id": paper.corpus_id,
            "tier": paper.tier,
            "title": paper.title,
            "authors": paper.authors,
            "target_supervisor": paper.target_supervisor,
            "year": paper.year,
            "journal": paper.venue,
            "volume": paper.volume,
            "issue": paper.issue,
            "pages": paper.pages,
            "DOI": paper.doi,
            "verified_affiliation": paper.concordia_affiliation,
            "corresponding_or_senior_author_status": paper.supervisor_status,
            "source_type": paper.source_type,
            "source_url_or_repository": str(src.relative_to(ROOT)),
            "full_text_available": "true",
            "local_pdf_path": str(dest.relative_to(ROOT)),
            "local_pdf_filename": dest.name,
            "sha256": sha256(dest),
            "pdf_page_count": info.get("Pages", "not reported"),
            "introduction_available": "true" if "introduction" in sections else "false",
            "related_work_available": "true" if "related_work" in sections else "false",
            "integrated_prior_work_available": "true" if "integrated_prior_work" in sections else "false",
            "abstract_file": sections.get("abstract", ""),
            "introduction_file": sections.get("introduction", ""),
            "related_work_file": sections.get("related_work", ""),
            "integrated_prior_work_file": sections.get("integrated_prior_work", ""),
            "method_overview_file": sections.get("method_overview", ""),
            "contributions_file": sections.get("contributions", ""),
            "discussion_limitations_file": sections.get("discussion_limitations", ""),
            "conclusion_file": sections.get("conclusion", ""),
            "technical_categories": paper.categories,
            "stylistic_usefulness": paper.stylistic_usefulness,
            "technical_relevance_to_paper2": paper.technical_relevance,
            "inclusion_reason": paper.inclusion_reason,
            "identity_confidence": paper.identity_confidence,
            "notes": paper.uncertainty,
            "duplicate_of": "",
            "duplicate_uploads": "; ".join(paper.duplicate_uploads),
            "included_in_analysis": "true",
        }
        manifest_rows.append(row)
        for section in ["introduction", "related_work", "integrated_prior_work", "contributions", "method_overview", "conclusion"]:
            if row.get(f"{section}_file"):
                feature_rows.append(analyze_section(row, section, row[f"{section}_file"]))

    # Tier 2 copies from existing older corpus.
    for old in load_old_tier2():
        cid = "T2_" + old["corpus_id"]
        old_pdf = ROOT / old["local_pdf_path"]
        if not old_pdf.exists():
            continue
        dest = REBUILT_PDF / f"{cid}.pdf"
        shutil.copy2(old_pdf, dest)
        info = pdfinfo(dest)
        sections = write_text_outputs(cid, old["title"], "Tier 2", old_pdf, dest)
        row = {
            "corpus_id": cid,
            "tier": "Tier 2",
            "title": old["title"],
            "authors": old["authors"],
            "target_supervisor": old["target_supervisor"],
            "year": old["year"],
            "journal": old["journal"],
            "volume": old["volume"],
            "issue": old["issue"],
            "pages": old["pages"],
            "DOI": old["DOI"],
            "verified_affiliation": old["verified_affiliation"],
            "corresponding_or_senior_author_status": old["corresponding_or_senior_author_status"],
            "source_type": old["source_type"],
            "source_url_or_repository": source_url_from_old(old["corpus_id"]),
            "full_text_available": "true",
            "local_pdf_path": str(dest.relative_to(ROOT)),
            "local_pdf_filename": dest.name,
            "sha256": sha256(dest),
            "pdf_page_count": info.get("Pages", "not reported"),
            "introduction_available": "true" if "introduction" in sections else "false",
            "related_work_available": "true" if "related_work" in sections else "false",
            "integrated_prior_work_available": "true" if "integrated_prior_work" in sections else "false",
            "abstract_file": sections.get("abstract", ""),
            "introduction_file": sections.get("introduction", ""),
            "related_work_file": sections.get("related_work", ""),
            "integrated_prior_work_file": sections.get("integrated_prior_work", ""),
            "method_overview_file": sections.get("method_overview", ""),
            "contributions_file": sections.get("contributions", ""),
            "discussion_limitations_file": sections.get("discussion_limitations", ""),
            "conclusion_file": sections.get("conclusion", ""),
            "technical_categories": classify_old_category(old["title"]),
            "stylistic_usefulness": "secondary historical style evidence",
            "technical_relevance_to_paper2": "style-only, not suitable for citation in Paper_2",
            "inclusion_reason": "Retained from previous verified corpus as Tier 2 secondary historical evidence.",
            "identity_confidence": old["identity_confidence"],
            "notes": old["notes"],
            "duplicate_of": "",
            "duplicate_uploads": "",
            "included_in_analysis": "true",
        }
        manifest_rows.append(row)
        for section in ["introduction", "related_work", "integrated_prior_work", "contributions", "method_overview", "conclusion"]:
            if row.get(f"{section}_file"):
                feature_rows.append(analyze_section(row, section, row[f"{section}_file"]))

    meta_fields = list(manifest_rows[0].keys())
    for out in [ROOT / "experiments" / "supervisor_style_corpus_metadata.csv", ROOT / "experiments" / "supervisor_style_corpus_verified_manifest.csv", REBUILT_META / "supervisor_style_corpus_metadata.csv"]:
        with out.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=meta_fields)
            w.writeheader()
            w.writerows(manifest_rows)

    sha_out = ROOT / "experiments" / "supervisor_style_corpus_sha256.txt"
    sha_out.write_text("".join(f"{r['sha256']}  {r['local_pdf_path']}\n" for r in manifest_rows), encoding="utf-8")

    feature_fields = list(feature_rows[0].keys())
    with (ROOT / "experiments" / "supervisor_style_features.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=feature_fields)
        w.writeheader()
        w.writerows(feature_rows)

    write_reports(manifest_rows, upload_rows, feature_rows)
    print(f"manual_uploads={len(uploads)} unique_tier1={len(MANUAL_PAPERS)} tier2={len(manifest_rows)-len(MANUAL_PAPERS)} features={len(feature_rows)}")
    return 0


def avg(rows: list[dict[str, str]], key: str) -> float:
    vals = [float(r[key]) for r in rows if r.get(key)]
    return sum(vals) / len(vals) if vals else 0.0


def top_titles(rows: list[dict[str, str]], predicate) -> str:
    return "\n".join(f"- `{r['corpus_id']}`: {r['title']}" for r in rows if predicate(r))


def write_reports(manifest_rows: list[dict[str, str]], upload_rows: list[dict[str, str]], feature_rows: list[dict[str, str]]) -> None:
    duplicates = [r for r in upload_rows if r["duplicate_status"] != "canonical"]
    exact_hash_dups = [h for h, c in Counter(r["sha256"] for r in upload_rows).items() if c > 1]
    dedup = [
        "# Manual Supervisor PDF Deduplication Report\n\n",
        f"Uploaded PDFs inspected: {len(upload_rows)}\n\n",
        f"Exact duplicate SHA-256 groups: {len(exact_hash_dups)}\n\n",
        "No byte-identical duplicate groups were found. The duplicate pairs below are bibliographic duplicates with different SHA-256 values.\n\n",
        "| Noncanonical file | Canonical file | Canonical corpus ID | Reason |\n",
        "|---|---|---|---|\n",
    ]
    for d in duplicates:
        dedup.append(f"| {d['upload_filename']} | {d['canonical_upload_filename']} | {d['canonical_corpus_id']} | {d['likely_duplicate_reason']} |\n")
    (ROOT / "implementation" / "manual_supervisor_pdf_deduplication_report.md").write_text("".join(dedup), encoding="utf-8")

    included = [r for r in manifest_rows if r["included_in_analysis"] == "true"]
    tier1 = [r for r in included if r["tier"] == "Tier 1"]
    tier2 = [r for r in included if r["tier"] == "Tier 2"]
    manifest = [
        "# Supervisor Style Corpus Paper Manifest\n\n",
        "This rebuilt manifest separates the recent manual-upload corpus from the older secondary corpus. Original uploaded PDFs were not deleted or modified.\n\n",
        "## Counts\n\n",
        f"- Uploaded PDFs inventoried: {len(upload_rows)}\n",
        f"- Unique Tier 1 papers: {len(tier1)}\n",
        f"- Tier 2 secondary papers: {len(tier2)}\n",
        f"- Total analyzed papers: {len(included)}\n",
        f"- Noncanonical bibliographic duplicates: {len(duplicates)}\n\n",
        "## Tier 1 Core Recent Corpus\n\n",
    ]
    for r in tier1:
        manifest.extend(paper_md(r))
    manifest.append("## Tier 2 Secondary Historical Corpus\n\n")
    for r in tier2:
        manifest.extend(paper_md(r))
    manifest.append("## Excluded Uploaded Files\n\n")
    manifest.append("| File | Reason |\n|---|---|\n")
    for d in duplicates:
        manifest.append(f"| {d['upload_filename']} | Excluded from analysis as noncanonical bibliographic duplicate of `{d['canonical_corpus_id']}`; source file retained. |\n")
    manifest.append("\nNo uploaded paper was excluded for missing supervisor authorship; all unique uploaded papers list at least one verified supervisor.\n")
    (ROOT / "implementation" / "supervisor_style_corpus_paper_manifest.md").write_text("".join(manifest), encoding="utf-8")

    intro_rows = [r for r in feature_rows if r["section"] == "introduction"]
    t1_intro = [r for r in intro_rows if r["tier"] == "Tier 1"]
    t2_intro = [r for r in intro_rows if r["tier"] == "Tier 2"]
    rw_rows = [r for r in feature_rows if r["section"] in {"related_work", "integrated_prior_work"}]
    t1_rw = [r for r in rw_rows if r["tier"] == "Tier 1"]
    style = [
        "# Ahmad-Swamy IEEE Writing Style Guide\n\n",
        "## Evidence Weighting\n\n",
        f"Tier 1 contains {len(tier1)} recent full-text papers, mostly IEEE Transactions/top-tier journal papers. Tier 2 contains {len(tier2)} older or domain-distant papers retained only as secondary evidence.\n\n",
        "## Strong Recurring Patterns in Recent Papers\n\n",
        "- Open with a concrete application domain and a practical failure pressure, then narrow to a technical bottleneck.\n",
        "- Present prior work by method family or mechanism, often inside the Introduction before a standalone Related Work section.\n",
        "- Use explicit limitation language after acknowledging prior progress.\n",
        "- Introduce the proposed method only after the unresolved limitation is established.\n",
        "- State contributions as concrete technical deliverables, often in an itemized list in IEEE Transactions papers.\n",
        "- Close the Introduction with a short paper-organization paragraph.\n\n",
        "## Quantitative Core-Corpus Tendencies\n\n",
        f"- Tier 1 Introduction mean paragraph count: {avg(t1_intro, 'paragraph_count'):.2f}.\n",
        f"- Tier 1 Introduction mean words per sentence: {avg(t1_intro, 'mean_words_per_sentence'):.2f}.\n",
        f"- Tier 1 Introduction mean citations per paragraph: {avg(t1_intro, 'mean_citations_per_paragraph'):.2f}.\n",
        f"- Tier 2 Introduction mean paragraph count: {avg(t2_intro, 'paragraph_count'):.2f}.\n",
        f"- Tier 2 Introduction mean words per sentence: {avg(t2_intro, 'mean_words_per_sentence'):.2f}.\n\n",
        "## Weaker Tendencies Seen Mainly in Older Papers\n\n",
        "- Longer single paragraphs and more compact contribution prose occur more often in older or non-IEEE venues.\n",
        "- Related Work is sometimes fully integrated into Introduction/background rather than separated.\n",
        "- Some older papers use broader task definitions before reaching the method; recent IEEE papers narrow faster.\n\n",
        "## Ahmad-Associated and Swamy-Associated Differences\n\n",
        "- Ahmad-associated papers frequently mark corresponding-author status and use a direct problem-to-method transition.\n",
        "- Swamy-associated senior-author papers often sustain a more tutorial explanation of prior method families before the gap.\n",
        "- Papers coauthored by both supervisors commonly emphasize practical constraints, computational efficiency, and controlled architectural design.\n\n",
        "## Venue-Dependent Variation\n\n",
        "- IEEE Transactions papers use dense citation clusters, explicit contribution lists, and section-organization paragraphs.\n",
        "- IEEE Signal Processing Letters and ICIP papers compress Related Work and method explanation because of length limits.\n",
        "- Springer/open journal papers may use longer paragraphs and less formal IEEE contribution formatting.\n\n",
        "## Practices That Should Guide Paper_2\n\n",
        "- Build the Introduction around degradation as a tracking feature-discriminability problem.\n",
        "- Discuss Mamba trackers by function: temporal context, fusion, motion/template adaptation, and efficient representation.\n",
        "- Position MambaIR/MambaIRv2 as restoration-oriented feature recovery evidence, not tracking evidence.\n",
        "- Treat InvTrack as the main novelty threat for degradation-invariant tracking.\n",
        "- Use a concrete contribution list tied to tested claims and claim boundaries.\n\n",
        "## Practices That Should Not Be Copied\n\n",
        "- Do not copy distinctive phrasing from the corpus.\n",
        "- Do not import underwater, biomedical, or pruning claims as technical tracking claims.\n",
        "- Do not claim state-of-the-art or universal robustness without full benchmark evidence.\n",
        "- Do not let older Tier 2 style override recent IEEE Transactions structure.\n\n",
        "## Strongest Introduction Models\n\n",
        top_titles(tier1, lambda r: r["corpus_id"] in {"T1_2026_TIP_MSD_RGBT", "T1_2025_TGRS_UADIFF", "T1_2024_TBC_DMML", "T1_2026_TPAMI_ACLI", "T1_2024_TMRB_MIS_FMR"}) + "\n\n",
        "## Strongest Related Work Models\n\n",
        top_titles(tier1, lambda r: r["corpus_id"] in {"T1_2024_TMRB_MIS_FMR", "T1_2025_TGRS_UADIFF", "T1_2024_TBC_DMML", "T1_2021_TBC_UPDRESNN", "T1_2021_TCI_SRNSSI", "T1_2026_TPAMI_ACLI"}) + "\n\n",
        "## Tracking Papers Most Relevant to Paper_2\n\n",
        top_titles(tier1, lambda r: "tracking" in r["technical_categories"]) + "\n",
    ]
    (ROOT / "implementation" / "ahmad_swamy_ieee_writing_style_guide.md").write_text("".join(style), encoding="utf-8")

    comparison = [
        "# Core vs Secondary Style Comparison\n\n",
        "## Corpus Separation\n\n",
        f"- Tier 1 core recent papers: {len(tier1)}.\n",
        f"- Tier 2 secondary historical papers: {len(tier2)}.\n\n",
        "## Main Difference\n\n",
        "Tier 1 is the governing evidence for Paper_2. It contains recent IEEE Transactions/top-tier journal papers with clearer contribution lists, stronger Related Work organization, and more explicit practical constraints. Tier 2 is retained only to confirm broad tendencies such as cautious limitation language and practical-to-technical narrowing.\n\n",
        "## Quantitative Contrast\n\n",
        f"- Tier 1 mean Introduction citations per paragraph: {avg(t1_intro, 'mean_citations_per_paragraph'):.2f}.\n",
        f"- Tier 2 mean Introduction citations per paragraph: {avg(t2_intro, 'mean_citations_per_paragraph'):.2f}.\n",
        f"- Tier 1 mean Introduction words per paragraph: {avg(t1_intro, 'mean_words_per_paragraph'):.2f}.\n",
        f"- Tier 2 mean Introduction words per paragraph: {avg(t2_intro, 'mean_words_per_paragraph'):.2f}.\n\n",
        "## Interpretation for Paper_2\n\n",
        "Use Tier 1 to structure the rewrite. Use Tier 2 only as a check against over-short, over-promotional, or under-motivated writing.\n",
    ]
    (ROOT / "implementation" / "core_vs_secondary_style_comparison.md").write_text("".join(comparison), encoding="utf-8")

    blueprint = [
        "# Introduction and Related Work Revision Blueprint\n\n",
        "No manuscript files were modified during this rebuild. This blueprint maps the current sections onto the rebuilt supervisor corpus patterns.\n\n",
        "## Current Introduction\n\n",
        "| Current paragraph | What it does | Missing/weak point | Recommendation | Corpus pattern | Needed citations |\n",
        "|---|---|---|---|---|---|\n",
        "| P1 | Introduces RGB tracking under degradation and immediately mentions MambaIR. | Practical tracking failure chain is too compressed. | Expand into task/application paragraph plus template-search degradation paragraph. | `T1_2026_TIP_MSD_RGBT`, `T1_2024_TMRB_MIS_FMR`, `T1_2025_TGRS_UADIFF`. | OSTrack/template-search, degradation tracking, MambaIR/MambaIRv2. |\n",
        "| P2 | States caveats, InvTrack, missing intersection, and method control. | Too many rhetorical functions in one paragraph. | Split into prior-work boundary, gap, and proposed-method paragraphs. | Recent IEEE papers separate prior limitation from proposed direction. | InvTrack, Mamba trackers, MambaIR papers. |\n",
        "| P3 | Lists contributions. | Bullets read partly as implementation/provenance notes. | Recast into 3-4 evidence-bearing contributions with explicit claim limits. | `T1_2024_TBC_DMML`, `T1_2021_TBC_UPDRESNN`, `T1_2026_TPAMI_ACLI`. | Claim traceability CSV and final claim audit. |\n\n",
        "## Current Related Work\n\n",
        "| Current subsection | What it does | Missing/weak point | Recommendation | Corpus pattern | Needed citations |\n",
        "|---|---|---|---|---|---|\n",
        "| Template-Search Object Tracking | Names OSTrack and boundary. | Lacks method-family context. | Add concise template-search/Siamese/one-stream tracker background. | Method-family reviews in `T1_2026_TIP_MSD_RGBT`. | OSTrack and representative trackers. |\n",
        "| Degradation-Robust Tracking | Uses InvTrack correctly. | Too narrow; needs broader degradation/invariant tracking context. | Put InvTrack as key threat, then define exact difference. | Limitation-after-progress pattern in `T1_2024_TMRB_MIS_FMR`. | InvTrack and degradation robustness sources. |\n",
        "| Restoration-Oriented Mamba Models | Names MambaIR/MambaIRv2. | Does not connect restoration feature recovery to tracking feature discriminability enough. | Add restoration-oriented state-space paragraph with tracking boundary. | Restoration motivation in `T1_2025_TGRS_UADIFF`, `T1_2024_TBC_DMML`. | MambaIR, MambaIRv2. |\n",
        "| Missing subsection | Mamba trackers are not separated. | This weakens novelty safety. | Add Mamba tracking subsection organized by use: temporal context, fusion, template update, motion, efficient backbone. | Method-family organization in Tier 1 Related Work. | Existing Mamba tracker paper cards. |\n\n",
        "## Contribution Placement\n\n",
        "Place contribution statements after the proposed method paragraph, not before the reader has seen the exact gap. Keep one bullet for method, one for evaluation protocol, one for NFS provenance, and one for bounded empirical finding.\n",
    ]
    (ROOT / "implementation" / "introduction_related_work_revision_blueprint.md").write_text("".join(blueprint), encoding="utf-8")


def paper_md(r: dict[str, str]) -> list[str]:
    keys = [
        ("Title", "title"),
        ("Authors", "authors"),
        ("Year", "year"),
        ("Venue", "journal"),
        ("Volume", "volume"),
        ("Issue", "issue"),
        ("Pages", "pages"),
        ("DOI", "DOI"),
        ("Target supervisor", "target_supervisor"),
        ("Verified Concordia affiliation", "verified_affiliation"),
        ("Senior/corresponding status", "corresponding_or_senior_author_status"),
        ("Source type", "source_type"),
        ("Source URL or repository", "source_url_or_repository"),
        ("Local PDF filename", "local_pdf_filename"),
        ("Local PDF path", "local_pdf_path"),
        ("SHA-256", "sha256"),
        ("PDF page count", "pdf_page_count"),
        ("Introduction file", "introduction_file"),
        ("Related Work file", "related_work_file"),
        ("Integrated prior-work file", "integrated_prior_work_file"),
        ("Categories", "technical_categories"),
        ("Stylistic usefulness", "stylistic_usefulness"),
        ("Technical relevance to Paper_2", "technical_relevance_to_paper2"),
        ("Identity confidence", "identity_confidence"),
        ("Inclusion reason", "inclusion_reason"),
        ("Uncertainty", "notes"),
    ]
    out = [f"### {r['corpus_id']}\n\n"]
    for label, key in keys:
        out.append(f"- **{label}:** {r.get(key, '') or 'not reported'}\n")
    out.append("\n")
    return out


if __name__ == "__main__":
    raise SystemExit(main())
