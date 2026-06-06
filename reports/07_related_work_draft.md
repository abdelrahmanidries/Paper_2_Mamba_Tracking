# Related Work Draft

## 1. Mamba for Image Restoration

Recent image-restoration work has shown that Mamba-style state-space modeling can be adapted beyond high-level recognition and sequence modeling. MambaIR introduces a restoration-oriented Mamba baseline for low-level image recovery tasks, including super-resolution, denoising, real-world denoising, and JPEG artifact reduction [MambaIR]. Its motivation is tied to limitations of directly applying vanilla Mamba to restoration: local pixel forgetting and channel redundancy. To address these issues, MambaIR uses restoration-specific residual state-space groups and blocks, combines 2D selective scanning with local enhancement, and introduces channel attention to improve low-level feature recovery [MambaIR].

MambaIRv2 further develops this direction by targeting limitations of causal state-space modeling in image restoration [MambaIRv2]. It introduces attentive state-space restoration, including an attentive state-space equation and semantic-guided neighboring, to reduce the mismatch between causal scanning and the non-causal, spatially correlated nature of image restoration. This design is important because it frames Mamba not only as an efficient sequence model, but also as a restoration-specific mechanism for recovering degraded image observations [MambaIRv2].

However, these restoration papers optimize image recovery objectives rather than visual tracking objectives. Their experiments are organized around restoration tasks and image-quality metrics, not template-search matching, target localization, tracking response maps, dynamic template update, or tracking robustness under video degradation. Thus, MambaIR and MambaIRv2 motivate restoration-oriented Mamba design, but their objective is image restoration rather than template-search target localization.

Evidence notes:
- paper: [MambaIR]
- supports: MambaIR uses restoration-oriented state-space blocks, local enhancement, and channel attention to address local pixel forgetting and channel redundancy; evidence pages pp. 1, 3, 6, 7, 8, 9, 13, 14.
- paper: [MambaIRv2]
- supports: MambaIRv2 uses attentive state-space restoration, attentive state-space equation, and semantic-guided neighboring for image restoration; evidence pages pp. 1, 2, 3, 4, 5, 8.
- paper: [MambaIR], [MambaIRv2]
- supports: both are image restoration papers and do not report template-search tracking, response maps, dynamic template update, or target localization objectives in the reviewed cards.

## 2. Mamba for Temporal and Contextual Visual Tracking

Several visual tracking methods use Mamba primarily as a temporal or contextual modeling mechanism. MambaLCT uses Mamba to build long-term context by scanning historical search-frame features, compressing target-related information into hidden states, and propagating context across frames [MambaLCT]. MCITrack similarly uses Mamba hidden states inside contextual-information fusion blocks, storing and updating historical contextual information and integrating it into current backbone features [MCITrack]. These works show that state-space modeling can help trackers exploit temporal cues beyond a single template-search pair.

TemTrack explores compact temporal modeling through historical track tokens. Its Mamba-based temporal module models track-token sequences in a sliding window so the current token can gather historical appearance changes and motion trends [TemTrack]. SMTrack further demonstrates the strength of state-space tracking by saving scanned template hidden states into memory, sampling them during tracking, and updating hidden states through newly cropped target templates [SMTrack]. These methods are important because they show that Mamba can support temporal cue propagation, memory, and dynamic template-state modeling in RGB tracking.

Nevertheless, temporal memory and degradation-aware restoration are distinct problems. MambaLCT, MCITrack, TemTrack, and SMTrack focus on long-term context, hidden-state memory, track-token evolution, or template-state propagation. Their reviewed cards do not report restoration-oriented recovery of degraded RGB template/search observations across generic degradations such as blur, noise, low resolution, compression, and mixtures. These works demonstrate the value of Mamba for temporal tracking, but they do not systematically adapt restoration-oriented Mamba blocks to recover degraded target-discriminative features.

Evidence notes:
- paper: [MambaLCT]
- supports: Mamba hidden states aggregate target information and long-term context; evidence pages pp. 2, 4, 5, 7.
- paper: [MCITrack]
- supports: Mamba hidden states store, update, and transmit contextual information; evidence pages pp. 1, 3, 4, 5, 6, 7.
- paper: [TemTrack]
- supports: Mamba models historical track-token sequences and temporal context; evidence pages pp. 2, 3, 4, 5.
- paper: [SMTrack]
- supports: scanned template hidden states, memory sampling, and dynamic template-state updates are used for RGB tracking; evidence pages pp. 6, 7, 10, 11.
- paper: [MambaLCT], [MCITrack], [TemTrack], [SMTrack]
- supports: restoration or enhancement of degraded template/search frames is not reported as the main mechanism in the reviewed cards.

## 3. Mamba for Multimodal and Specialized Tracking

Mamba has also been applied to multimodal and specialized tracking settings. In RGB-event tracking, Mamba-FETrack uses Mamba as a lightweight feature backbone and fusion mechanism for frame-event interaction [Mamba-FETrack]. MamTrack extends this direction with RGB-event inputs, target-aware scan, cross-modality scan, and historical Mamba modeling to combine RGB and event information for template-search tracking [MamTrack]. These methods improve robustness under adverse conditions such as fast motion, limited illumination, motion blur, and partial occlusion, but their robustness is tied to event sensing and multimodal fusion rather than RGB-only restoration.

Event-only tracking is represented by MambaEVT, which uses event streams and Memory Mamba for dynamic template generation [MambaEVT]. This line of work is important because event cameras can naturally help under high-speed motion, low light, and high dynamic range. However, event-only tracking addresses a different input modality and does not directly solve restoration-guided RGB template-search tracking under image-quality degradation.

RGB-T and infrared-based tracking form another specialized branch. MambaVT uses Mamba for spatio-temporal contextual modeling over visible and thermal inputs, including template memory and trajectory prompts [MambaVT]. All-Day MCMT uses visible and infrared information with lighting-guided Mamba fusion for all-day multi-camera multi-target tracking [All-Day MCMT]. These works demonstrate strong modality-assisted robustness, especially under challenging illumination, but thermal or infrared sensing is not the same as recovering degraded RGB template/search representations.

Vision-language and hyperspectral tracking further show the flexibility of Mamba in specialized tracking settings. In the reviewed set, the vision-language evidence comes from MambaTrack Night UAV, which combines a Mamba-based low-light enhancer, visual and language branches, and cross-modal Mamba for nighttime UAV tracking [MambaTrack Night UAV]. A separate MambaVLT paper card is not present in the reviewed evidence set, so no additional MambaVLT-specific claims are made here. HyMamba applies Mamba to hyperspectral tracking through spectral hidden-state modeling and dynamic template handling [HyMamba]. These methods are powerful but often rely on additional modalities such as event, thermal, language, or hyperspectral data, while our target problem is RGB-only degradation-robust template-search tracking.

Evidence notes:
- paper: [Mamba-FETrack]
- supports: RGB-event tracking with Mamba feature extraction and fusion; evidence pages pp. 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 15.
- paper: [MamTrack]
- supports: RGB-event Mamba fusion, Target-Aware Scan, Cross-Modality Scan, historical modeling, and score-map tracking head; evidence pages pp. 1, 2, 3, 4, 5, 6, 7, 8.
- paper: [MambaEVT]
- supports: event-only tracking with Memory Mamba and dynamic template generation; evidence pages pp. 1, 2, 3, 4, 5, 6, 7, 11, 12.
- paper: [MambaVT]
- supports: RGB-T Mamba tracking with spatio-temporal context, trajectory prompts, and online template memory; evidence pages pp. 1, 2, 3, 4, 5, 6, 7, 10.
- paper: [MambaTrack Night UAV]
- supports: night UAV vision-language tracking with Mamba low-light enhancement and cross-modal Mamba; evidence pages pp. 1, 2, 3, 4.
- paper: [HyMamba]
- supports: hyperspectral Mamba tracking with spectral hidden-state modeling and dynamic templates; evidence pages pp. 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11.
- paper: [All-Day MCMT]
- supports: all-day multi-camera multi-target tracking with RGBT/infrared fusion and lighting-guided Mamba fusion; evidence pages pp. 1, 2, 3, 4, 5, 6, 7, 8.
- paper: [MambaVLT]
- supports: no separate paper card was available in the reviewed set; no claims are made beyond the available vision-language evidence from [MambaTrack Night UAV].

## 4. Mamba for Motion Prediction and Multi-Object Tracking

Another group of Mamba trackers focuses on multi-object tracking and motion prediction. MambaTrack MOT follows a tracking-by-detection paradigm in which Mamba predicts motion from historical bounding-box trajectories and helps patch fragmented tracklets under missed detections, occlusion, or motion blur [MambaTrack MOT]. MambaMOT similarly uses Mamba as a trajectory-sequence motion predictor for multi-object tracking, operating on bounding-box tracklets rather than RGB template-search feature pairs [MambaMOT].

MM-Tracker uses Motion Mamba for UAV-platform MOT, combining detector features, motion maps, and motion-aware modeling to address UAV motion and motion-blur-induced detection difficulty [MM-Tracker]. SportMamba applies Mamba-attention motion prediction and association mechanisms to team-sports MOT, where fast motion, occlusion, and motion blur can weaken detections and appearance cues [SportMamba]. These works show that Mamba can be useful for nonlinear motion, trajectory modeling, and MOT association.

However, MOT motion prediction is not the same as degraded visual feature recovery. These methods typically operate on detections, tracklets, motion maps, cost matrices, or association pipelines, whereas RGB single-object template-search tracking depends on matching target-discriminative visual representations between a template and a search region. These works show Mamba's strength in trajectory and motion modeling, but they do not directly address restoration-guided target representation learning for RGB single-object tracking under image degradation.

Evidence notes:
- paper: [MambaTrack MOT]
- supports: Mamba is used for motion prediction from historical bounding-box trajectories and tracklet patching; evidence pages pp. 1, 2, 3, 4, 5, 6, 7, 8.
- paper: [MambaMOT]
- supports: Mamba models trajectory sequences and hidden states for MOT motion prediction; evidence pages pp. 1, 2, 3, 4.
- paper: [MM-Tracker]
- supports: Motion Mamba and Motion Margin Loss address UAV MOT motion modeling and motion-blur-induced detection difficulty; evidence pages pp. 1, 2, 3, 4, 5, 6, 7.
- paper: [SportMamba]
- supports: Mamba-attention motion prediction, association, ReID/EMA updating, and severe motion-blur limitations in sports MOT; evidence pages pp. 1, 2, 3, 4, 5, 6, 7, 8.
- paper: [MambaTrack MOT], [MambaMOT], [MM-Tracker], [SportMamba]
- supports: these methods address MOT motion/association rather than restoration-guided RGB SOT template-search feature recovery.

## 5. Degradation-Robust, Low-Light, and Adverse-Condition Tracking

Degradation-robust tracking is directly studied by InvTrack, which formulates RGB template-search tracking under image-quality degradation [InvTrack]. InvTrack uses synthetic degradations including blur, downsampling/low resolution, noise, and JPEG compression; enforces clean-degraded feature consistency; introduces low-pass residual modules; and fuses multiple clean/degraded response maps for prediction [InvTrack]. This makes InvTrack a central novelty threat for any work on degraded RGB tracking. At the same time, InvTrack does not report restoration-guided Mamba, restoration-specific state-space blocks, or image reconstruction-guided target recovery.

Low-light and nighttime tracking have also been studied in Mamba-based tracking. MambaTrack Night UAV uses a Mamba-based low-light enhancer on cropped template and search regions, together with visual, language, and cross-modal Mamba components for nighttime UAV tracking [MambaTrack Night UAV]. MambaNUT uses Vision Mamba and adaptive curriculum learning for nighttime UAV tracking, focusing on low contrast, low brightness, and low signal-to-noise ratio without an image-restoration module [MambaNUT]. These works are important for night tracking, but low-light/nighttime tracking is a narrower setting than general degradation robustness across blur, noise, low resolution, compression, and mixed artifacts.

Adverse-condition robustness is also addressed through additional modalities or task-specific modeling. All-Day MCMT uses visible-infrared/RGBT fusion and lighting-guided Mamba fusion for all-day multi-camera tracking [All-Day MCMT]. MM-Tracker is relevant to motion blur, but it addresses blurred objects mainly through detection supervision, motion maps, and MOT association rather than restoration-guided template-search matching [MM-Tracker]. Thus, degradation-invariant learning is not the same as restoration-guided state-space feature recovery, low-light tracking is not the same as general degradation-robust tracking, and multimodal low-light robustness is not the same as RGB-only robustness.

Existing degradation-aware and adverse-condition trackers partially address robustness, but restoration-guided Mamba for generic RGB template-search tracking remains underexplored in the reviewed evidence.

Evidence notes:
- paper: [InvTrack]
- supports: degradation-invariant RGB template-search tracking with synthetic blur, low resolution, noise, JPEG, clean-degraded feature consistency, LPRM, and response-map fusion; evidence pages pp. 7, 8, 10, 12, 14, 15, 16.
- paper: [MambaTrack Night UAV]
- supports: Mamba low-light enhancement on cropped template/search regions in night UAV vision-language tracking; evidence pages pp. 1, 2, 3, 4.
- paper: [MambaNUT]
- supports: nighttime RGB UAV tracking with Vision Mamba and adaptive curriculum learning, without image restoration; evidence pages pp. 1, 2, 3, 4, 5, 6, 7.
- paper: [All-Day MCMT]
- supports: all-day MCMT with infrared/RGBT fusion and lighting-guided Mamba fusion; evidence pages pp. 1, 2, 3, 4, 5, 6, 7, 8.
- paper: [MM-Tracker]
- supports: motion-blur-related UAV MOT through detection/motion modeling, not restoration-guided RGB SOT; evidence pages pp. 1, 3, 4, 5, 6.

## 6. Positioning of Our Work

The reviewed literature suggests a clear but narrow opportunity. MambaIR and MambaIRv2 provide restoration-oriented Mamba designs for degraded image recovery, including local enhancement, channel attention, attentive state-space restoration, and semantic-guided neighboring [MambaIR], [MambaIRv2]. Existing Mamba trackers demonstrate the value of state-space modeling for temporal memory, contextual propagation, multimodal fusion, motion prediction, dynamic template update, and efficient tracking [MambaLCT], [MCITrack], [TemTrack], [SMTrack], [MamTrack], [MambaVT], [MambaEVT], [MambaTrack MOT], [MambaMOT]. InvTrack shows that RGB degradation-invariant template-search tracking is meaningful, but it does not use restoration-guided Mamba state-space modeling [InvTrack]. Night UAV Mamba trackers address low-light or nighttime UAV tracking, but they do not systematically cover general RGB degradation-robust tracking across blur, noise, low resolution, compression, and mixed degradation [MambaTrack Night UAV], [MambaNUT].

Therefore, our work targets an underexplored intersection: restoration-guided Mamba tracking for RGB template-search tracking under general image-quality degradation. The goal is not to claim that Mamba tracking, low-light tracking, memory, or degradation-aware tracking are absent. Instead, the goal is to investigate whether restoration-oriented state-space modeling can be adapted to recover target-discriminative RGB template/search representations and improve localization reliability under generic degradation.

## Final related-work transition paragraph

In summary, prior work establishes three complementary foundations: restoration-oriented Mamba for image recovery, Mamba-based tracking for temporal/contextual/multimodal/motion modeling, and degradation-aware tracking through invariant feature learning or adverse-condition specialization. However, these directions have not been fully connected in the reviewed evidence. This motivates a restoration-guided Mamba tracking framework that treats degraded RGB template-search matching as a tracking-aware recovery problem, with robustness evaluated by target localization, response reliability, and degradation-specific performance rather than image restoration quality alone.

## Unsafe wording removed

- Avoided: "No one has used Mamba for tracking."
- Used instead: existing Mamba trackers mainly focus on temporal/context/multimodal/motion/memory/efficiency/adverse-condition uses.
- Avoided: "No one has handled low-light tracking."
- Used instead: low-light and nighttime tracking are studied, but are narrower than generic RGB degradation robustness.
- Avoided: "No one has used memory."
- Used instead: memory and hidden-state tracking are studied; degradation-aware restoration is a different issue.
- Avoided: "This is the first degradation-robust tracker."
- Used instead: InvTrack directly studies degradation-invariant tracking; the underexplored part is restoration-guided Mamba.
- Avoided: "Existing Mamba trackers ignore degradation completely."
- Used instead: some address adverse conditions, low light, motion blur, or sensor-assisted robustness, but not systematic restoration-guided RGB template-search recovery.
- Avoided: "MambaIR has never been used in tracking."
- Used instead: the reviewed evidence does not directly show MambaIR/MambaIRv2-style restoration mechanisms fully adapted to tracking-aware template-search matching.

## Verification

1. Files created or modified:
   - `reports/07_related_work_draft.md`
2. How the output was verified:
   - Used only `paper_cards/`, the four matrices, `tables/gap_scorecard.csv`, and previous reports as evidence.
   - Checked that each subsection includes citation placeholders from reviewed paper cards.
   - Included evidence notes with paper names and page references from the paper cards or matrices.
   - Explicitly noted that no separate `MambaVLT` card exists in the reviewed set, so no unsupported MambaVLT-specific claims are made.
   - Preserved the required distinctions: image restoration versus tracking-aware restoration, temporal memory versus degradation-aware memory, multimodal robustness versus RGB-only robustness, motion prediction versus degraded visual feature recovery, and low-light tracking versus general degradation-robust tracking.
3. Uncertain fields:
   - External literature beyond the reviewed evidence set was not checked.
   - A separate MambaVLT paper was requested in the outline but is not present in `paper_cards/`; only the available vision-language evidence from MambaTrack Night UAV is used.
   - Some limitations are based on "not reported" fields in paper cards rather than explicit author-stated limitations.
4. Whether the project is ready for method architecture design:
   - Yes. The related-work draft and research-gap paragraph now establish a cautious positioning, so the project is ready for method architecture design next.
