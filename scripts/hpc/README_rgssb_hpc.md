# RG-SSB Feature-Consistency Lambda 0.02 HPC Scripts

These scripts are templates for HPC execution. They are not ready to submit until
the placeholders are edited for the target cluster.

## Files

- `scripts/hpc/slurm_rgssb_featcons_lam002_train.sh`
- `scripts/hpc/slurm_rgssb_featcons_lam002_eval.sh`
- `configs/rgssb_experiment_cycle_hpc_featcons_lam002.json`

## Required Edits

Edit both SLURM scripts:

- `<ACCOUNT>`
- `<PARTITION>`
- `<GPU_TYPE>`
- `<NUM_GPUS>`
- `<CPUS>`
- `<MEMORY>`
- `<WALL_TIME>`
- `<PROJECT_PATH>`
- `<CONDA_INITIALIZATION_PATH>`
- `<HPC_LASOT_ROOT>`
- `<HPC_OTB_ROOT>`

Edit `configs/rgssb_experiment_cycle_hpc_featcons_lam002.json` on HPC if paths
differ:

- `ostrack_root`
- `clean_otb_root`
- `output_root`
- `results_csv`
- `conda_env`

## Order

1. Run local verification:

```bash
conda run -n ostrack python scripts/verify_hpc_featcons_lam002_setup.py
```

2. Submit training on HPC.
3. Confirm checkpoint exists:

```text
external/OSTrack/output/checkpoints/train/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002/OSTrack_ep0010.pth.tar
```

4. Submit evaluation on HPC.
5. Review `experiments/baseline_results.csv`.

## Notes

The HPC config uses conservative defaults: batch size `8`, `10` epochs,
`10000` train samples per epoch, and `1000` validation samples per epoch. Adjust
batch size, workers, memory, and wall time based on actual GPU memory and queue
limits.
