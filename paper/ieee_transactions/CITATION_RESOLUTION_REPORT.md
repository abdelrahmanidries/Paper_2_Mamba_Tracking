# Citation Resolution Report

## Resolved From Local Metadata

- `guo2024mambair`: MambaIR paper card provided title, authors, year, and ECCV venue.
- `guo2025mambairv2`: MambaIRv2 paper card provided title, authors, year, and CVPR venue.
- `invtrack_local`: local InvTrack paper card provided title and authors; year and venue were not reported, so the BibTeX entry is marked `@unpublished` with a note.

## Unresolved Citation Markers Remaining

1. OSTrack baseline and architecture.
   - Sentence: abstract and related-work/method use OSTrack as the base tracker.
   - Required source type: original OSTrack paper BibTeX.
   - Candidate local sources: `external/OSTrack/`, existing reports.
   - Missing metadata: exact title, authors, venue, year, pages/DOI.

2. LaSOT training dataset.
   - Sentence: final method uses degradation-aware LaSOT training.
   - Required source type: LaSOT benchmark BibTeX.
   - Candidate local sources: local dataset path and reports.
   - Missing metadata: exact bibliographic entry.

3. OTB benchmark.
   - Sentence: broader OTB subset result.
   - Required source type: OTB/OTB100 benchmark BibTeX.
   - Missing metadata: exact bibliographic entry.

4. UAV123 benchmark.
   - Sentence: expanded UAV123 subset result.
   - Required source type: UAV123 benchmark BibTeX.
   - Missing metadata: exact bibliographic entry.

5. NFS benchmark.
   - Sentence: corrected expanded NFS subset result.
   - Required source type: NFS/NfS benchmark BibTeX.
   - Missing metadata: exact bibliographic entry.

Do not replace these markers with invented references.
