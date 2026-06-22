# Final Reproducibility Checklist

- Use config `vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002`.
- Use normalized aligned XYWH NFS annotations for every NFS result.
- Do not use archived invalid NFS rows except as provenance.
- Do not mix historical timing files with controlled V100 efficiency measurements.
- Report FLOPs/MACs as unavailable.
- Keep TDM disabled and rejected.
- Do not commit checkpoints, generated tracker outputs, degraded datasets, or external/OSTrack outputs.
- Verify final assets with `python3 scripts/verify_final_paper_package.py`.
