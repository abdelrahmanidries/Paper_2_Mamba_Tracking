# Demonstration: WRITE_FROM_SCRATCH

## Paragraph-Role Outline

1. Crop monitoring motivation.
2. Thermal-camera drift challenge.
3. Prior calibration and learning-based progress.
4. Narrow limitation.
5. Fictional method preview.

## Claim-to-Evidence Map

- Claim: Field thermal cameras drift under daily temperature changes.
  Evidence: E1, `\cite{demoThermalDrift2026}`.
- Claim: Calibration tokens reduce drift on the supplied fictional validation split.
  Evidence: E2, `\cite{demoCalibrationTokens2026}`.

## Draft

Thermal crop monitoring can support irrigation planning when visible imagery is unreliable under shadows or strong illumination changes. In field deployments, however, the measured canopy temperature can vary with sensor warm-up, ambient temperature, and acquisition time. This makes the same crop region appear different even when its physiological state is unchanged, which weakens downstream stress estimation in the fictional setting considered here `\cite{demoThermalDrift2026}`.

Existing calibration procedures and learning-based correction modules reduce part of this variability, but the supplied evidence indicates that they are usually applied as a preprocessing step or as a global image normalization `\cite{demoThermalDrift2026}`. Such designs can improve average image consistency while leaving local crop regions sensitive to residual sensor drift. This limitation is important for plot-level monitoring because stress decisions depend on small temperature differences across neighboring regions.

To address this bounded issue, the fictional study introduces a calibration-aware token module that conditions thermal features on acquisition metadata before plot-level prediction. The module is not intended to replace physical calibration. Instead, it provides a compact feature-adaptation step for residual drift after standard preprocessing. In the supplied fictional validation split, the calibration-token variant reduces drift-sensitive errors compared with the metadata-free baseline `\cite{demoCalibrationTokens2026}`.

## Revision Report

- Citation audit: all prior-work and result claims include citation markers.
- Claim audit: both major claims are mapped to supplied fictional evidence.
- Phrase-overlap audit: to be run with `scripts/check_phrase_overlap.py`.
- Uncertain fields: dataset size, exact metric names, and numerical values were not supplied.
