\# Paper\_2\_Mamba\_Tracking — Codex Instructions



\## Research topic

We are writing a second research paper on visual object tracking using Mamba architecture.



The goal is to find strong research gaps by comparing:

1\. Mamba-based visual tracking papers.

2\. MambaIR and MambaIRv2 image restoration papers.

3\. InvTrack, which studies degradation-invariant tracking.



\## Main hypothesis

Existing Mamba trackers mostly use Mamba for:

\- temporal memory

\- video-level context

\- multimodal fusion

\- motion prediction

\- dynamic template update

\- efficient backbone design



MambaIR and MambaIRv2 use Mamba for restoration-specific image recovery.



We are searching for the missing intersection:

restoration-oriented Mamba + degradation-robust RGB template-search tracking.



\## Critical rules

1\. Do not invent research gaps.

2\. Every gap must be supported by evidence from papers.

3\. Do not claim "no one has used Mamba for tracking."

4\. Do not claim "no one has handled low-light tracking."

5\. Do not claim "no one has used Mamba memory."

6\. Distinguish explicit limitations from implicit limitations.

7\. If a paper does not discuss something, write "not reported."

8\. Use page numbers or evidence quotes for every major claim.

9\. Do not propose final paper ideas until the evidence matrices are complete.

10\. Prefer precise, testable research gaps over vague novelty claims.



\## Important distinction

A weak gap:

"Use Mamba for visual tracking."



A strong gap:

"Existing Mamba trackers mainly use state-space models for temporal context, multimodal fusion, dynamic template update, or motion prediction, but they do not systematically adapt restoration-oriented Mamba blocks to recover target-discriminative features under generic image-quality degradation in RGB template-search tracking."



\## Required output files

Codex should create these files during the workflow:



\- data/extracted/\*.jsonl

\- paper\_cards/\*.md

\- tables/paper\_matrix.csv

\- tables/mamba\_usage\_matrix.csv

\- tables/degradation\_matrix.csv

\- tables/missing\_intersection\_matrix.csv

\- tables/gap\_scorecard.csv

\- reports/01\_evidence\_summary.md

\- reports/02\_gap\_analysis.md

\- reports/03\_reviewer\_attack.md

\- reports/04\_novelty\_danger\_check.md

\- reports/05\_experiment\_plan.md

\- reports/06\_final\_paper\_plan.md



\## Paper card format

Each paper card must include:



1\. Title

2\. Year and venue

3\. Task

4\. Modality

5\. Motivation

6\. Main problem

7\. Main contributions

8\. Methodology

9\. Main modules

10\. How Mamba is used

11\. Whether it handles degradation

12\. Whether it handles restoration/enhancement

13\. Whether it handles temporal memory

14\. Whether it handles template update

15\. Whether it handles response-map fusion

16\. Datasets and metrics

17\. Explicit limitations

18\. Implicit limitations

19\. Evidence quotes with page numbers

20\. Relevance to our second paper



\## Verification rules

Before finishing any task, Codex must:

1\. List files created or modified.

2\. Explain how it verified the output.

3\. Mention uncertain fields.

4\. Never mark a cell "Yes" without evidence.

5\. Never rank a gap highly unless it is testable experimentally.

