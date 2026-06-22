# Citation Resolution Report

All genuine citation placeholders in the IEEE manuscript have been resolved. The helper macro was removed from `main.tex`.

## Resolved Bibliography Entries

- `ye2022ostrack`: Botao Ye, Hong Chang, Bingpeng Ma, Shiguang Shan, and Xilin Chen, "Joint Feature Learning and Relation Modeling for Tracking: A One-Stream Framework," ECCV 2022, LNCS, pp. 341--357, DOI `10.1007/978-3-031-20047-2_20`. Verified by Crossref; arXiv 2203.11991 confirms title/authors and OSTrack context.
- `fan2019lasot`: Heng Fan, Liting Lin, Fan Yang, Peng Chu, Ge Deng, Sijia Yu, Hexin Bai, Yong Xu, Chunyuan Liao, and Haibin Ling, "LaSOT: A High-Quality Benchmark for Large-Scale Single Object Tracking," CVPR 2019, pp. 5369--5378, DOI `10.1109/CVPR.2019.00552`. Verified by Crossref; local pytracking files confirm the LaSOT benchmark title.
- `wu2013otb`: Yi Wu, Jongwoo Lim, and Ming-Hsuan Yang, "Online Object Tracking: A Benchmark," CVPR 2013, pp. 2411--2418, DOI `10.1109/CVPR.2013.312`. Verified by Crossref. This is the benchmark paper cited for the OTB/OTB100 evaluation family used by the tracker code.
- `mueller2016uav123`: Matthias Mueller, Neil Smith, and Bernard Ghanem, "A Benchmark and Simulator for UAV Tracking," ECCV 2016, LNCS, pp. 445--461, DOI `10.1007/978-3-319-46448-0_27`. Verified by Crossref; local tracker dataset files confirm the UAV123 benchmark title.
- `galoogahi2017nfs`: Hamed Kiani Galoogahi, Ashton Fagg, Chen Huang, Deva Ramanan, and Simon Lucey, "Need for Speed: A Benchmark for Higher Frame Rate Object Tracking," ICCV 2017, pp. 1134--1143, DOI `10.1109/ICCV.2017.128`. Verified by Crossref; arXiv 1703.05884 confirms title/authors and NfS context.
- `guo2024mambair` and `guo2025mambairv2`: retained from local paper-card metadata.
- `invtrack_local`: retained because the manuscript genuinely cites InvTrack as local evidence for degradation-invariant tracking. The local PDF verifies title, authors, affiliation structure, corresponding-author line, and funding text, but it contains placeholder publication dates and DOI. It remains `@unpublished` until final publication metadata is confirmed.

## Counts

- Genuine citation placeholders remaining: 0.
- Unresolved citation keys in manuscript source: 0 after local static check.
- Unverifiable DOI fields inserted: 0. DOI fields are included only for Crossref-confirmed entries.
