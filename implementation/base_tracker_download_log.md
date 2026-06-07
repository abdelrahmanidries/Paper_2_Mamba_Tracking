\# Base Tracker Download Log



\## Selected base tracker



OSTrack: Joint Feature Learning and Relation Modeling for Tracking: A One-Stream Framework.



\## Reason for selection



OSTrack is selected as the first proof-of-concept base tracker because it is a clean RGB single-object one-stream template-search tracker. This makes it suitable for inserting restoration-guided feature modules and testing degradation robustness without introducing extra temporal, multimodal, or memory components at the start.



\## Repository



https://github.com/botaoye/OSTrack



\## Local path



external/OSTrack



\## Download date



<write today's date>



\## Commit hash



33b5e12586216b7fd0e95d255bd01ba44cbec759




\## Why not use other trackers first?



\- MixFormer is strong, but OSTrack is cleaner for template-search feature modification.

\- MambaLCT, MCITrack, TemTrack, and SMTrack already include Mamba-based temporal/context designs, which could confuse the novelty of our restoration-guided Mamba contribution.

\- MambaEVT, MamTrack, MambaVT, MambaVLT, HyMamba, and All-Day MCMT use event, RGB-T, language, hyperspectral, or multi-camera settings, while the target problem is RGB-only degradation-robust tracking.

\- MambaTrack MOT, MambaMOT, MM-Tracker, and SportMamba focus on MOT motion prediction or association, not RGB SOT template-search feature recovery.

