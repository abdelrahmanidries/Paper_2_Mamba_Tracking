# HPC Run Order

1. Clone or copy the project on HPC.

   ```bash
   git clone <PROJECT_REPOSITORY_URL> Paper_2_Mamba_Tracking
   cd Paper_2_Mamba_Tracking
   git checkout implementation-poc
   ```

2. Create or activate the conda environment.

   ```bash
   conda env create -f <ENV_FILE>
   conda activate ostrack
   ```

3. Clone OSTrack into `external/OSTrack`.

   ```bash
   mkdir -p external
   git clone https://github.com/botaoye/OSTrack external/OSTrack
   cd external/OSTrack
   git checkout 33b5e12586216b7fd0e95d255bd01ba44cbec759
   cd ../..
   ```

4. Apply `implementation/patches/ostrack_rgssb_integration.patch`.

   ```bash
   bash scripts/hpc/apply_ostrack_patch.sh
   ```

5. Download or copy the OSTrack base checkpoint.

   Required path:

   ```text
   external/OSTrack/output/checkpoints/train/ostrack/vitb_256_mae_ce_32x4_ep300/OSTrack_ep0300.pth.tar
   ```

6. Link datasets.

   Ensure LaSOT and OTB are available on HPC storage. Do not commit datasets.

7. Edit `configs/hpc_paths_template.env`.

   Set `PROJECT_ROOT`, `OSTRACK_ROOT`, `LASOT_ROOT`, `OTB_ROOT`, scheduler
   fields, scratch path, and results path.

8. Edit SLURM scripts.

   Update:

   - `scripts/hpc/slurm_rgssb_featcons_lam002_train.sh`
   - `scripts/hpc/slurm_rgssb_featcons_lam002_eval.sh`

9. Run verification.

   ```bash
   bash scripts/hpc/verify_hpc_environment.sh
   conda run -n ostrack python scripts/verify_hpc_featcons_lam002_setup.py
   ```

10. Submit training job.

   ```bash
   sbatch scripts/hpc/slurm_rgssb_featcons_lam002_train.sh
   ```

11. Submit evaluation job after the expected epoch-10 checkpoint exists.

   ```bash
   sbatch scripts/hpc/slurm_rgssb_featcons_lam002_eval.sh
   ```

12. Copy results back.

   Copy only compact result files such as CSV rows, logs, and selected summaries.
   Do not copy checkpoints into Git.

13. Update `experiments/baseline_results.csv` if needed.

   Prefer appending or replacing rows through the evaluation runner. Do not
   manually invent metric rows.

14. Analyze HPC results.

   Compare the HPC config against local lambda `0.02`, fully degraded 3000,
   balanced 3000, and original OSTrack baseline.
