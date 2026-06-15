# Failure-Focused UAV123 + NFS Evaluation Plan

## 1. Why this expansion is needed

The HPC RG-SSB + head feature-consistency lambda `0.02` checkpoint is positive on the broader OTB subset, but selected UAV123 and NFS subsets are mixed/slightly negative. The cross-benchmark failure inspection shows that the drops are not uniform: they cluster around selected sequence-condition pairs such as `uav_car11` under low resolution and `nfs_walking` under motion blur or Gaussian noise.

This batch expands UAV123 and NFS coverage before changing architecture or training. The goal is to determine whether the failures are sequence-specific, benchmark-specific, or systematic under particular degradations.

## 2. Failure patterns motivating the sequence choices

- UAV123 low-resolution failures need more car/person/truck coverage.
- UAV123 aerial viewpoint, camera motion, and target scale changes need additional person, vehicle, and wakeboard cases.
- NFS failures include high-frame-rate/sampling-sensitive walking and sports cases.
- NFS gains on `nfs_car` and `nfs_Gymnastics` should be checked against related vehicle, sports, animal, and fast-motion sequences.
- Gaussian noise is positive on OTB/UAV123 but negative on NFS, so NFS expansion should include more motion-heavy cases.

## 3. Selected UAV123 sequences

Existing evaluated sequences retained:

- `uav_car10`
- `uav_person1`
- `uav_truck1`
- `uav_bike1`
- `uav_boat1`
- `uav_building1`
- `uav_person3`
- `uav_car11`

Added failure-coverage sequences:

- `uav_car12`
- `uav_car13`
- `uav_person10`
- `uav_person12_1`
- `uav_person14_1`
- `uav_truck2`
- `uav_bike2`
- `uav_wakeboard1`

Total UAV123 sequences: `16`.

## 4. Selected NFS sequences

Existing evaluated sequences retained:

- `nfs_Gymnastics`
- `nfs_basketball_player`
- `nfs_car`
- `nfs_dog`
- `nfs_running`
- `nfs_bottle`
- `nfs_bird_2`
- `nfs_walking`

Added failure-coverage sequences:

- `nfs_basketball_player_2`
- `nfs_car_drifting`
- `nfs_car_jumping`
- `nfs_cheetah`
- `nfs_horse_running`
- `nfs_motorcross`
- `nfs_person_scooter`
- `nfs_soccer_player_2`

Total NFS sequences: `16`.

## 5. Configs created

- `configs/uav123_eval_suite_failure_expanded_ostrack.json`
- `configs/uav123_eval_suite_failure_expanded_hpc_rgssb_featcons_lam002.json`
- `configs/nfs_eval_suite_failure_expanded_ostrack.json`
- `configs/nfs_eval_suite_failure_expanded_hpc_rgssb_featcons_lam002.json`
- `configs/failure_focused_eval_batch.json`

Each suite uses four conditions:

- clean, severity `none`, seed `0`
- motion blur, severity `medium`, seed `42`
- low resolution, severity `medium`, seed `42`
- Gaussian noise, severity `medium`, seed `42`

## 6. Commands

Dry-run:

```bash
python3 scripts/run_failure_focused_eval_batch.py \
  --batch_config configs/failure_focused_eval_batch.json \
  --dry_run
```

Real batch on Speed:

```bash
cd /speed-scratch/a_idrais/Paper_2_Mamba_Tracking
python3 scripts/run_failure_focused_eval_batch.py \
  --batch_config configs/failure_focused_eval_batch.json
```

The batch runner executes suites sequentially:

1. UAV123 baseline
2. UAV123 HPC RG-SSB
3. NFS baseline
4. NFS HPC RG-SSB

It passes `--skip_existing` by default, so already logged rows in `experiments/baseline_results.csv` are skipped.

## 7. Expected rows

- UAV123: `16` sequences x `4` conditions x `2` configs = `128` possible rows.
- NFS: `16` sequences x `4` conditions x `2` configs = `128` possible rows.
- Total possible batch rows = `256`.

Because the original 8 UAV123 and 8 NFS sequences were already evaluated for both configs, `--skip_existing` should normally plan only the additional 8 sequences per dataset:

- UAV123 new rows expected with skip-existing: `64`.
- NFS new rows expected with skip-existing: `64`.
- Total new rows expected with skip-existing: `128`.

## 8. What to commit

- Expanded suite configs.
- Batch config.
- Batch runner.
- Batch verifier.
- This plan.

## 9. What not to commit

- `external/OSTrack/output/`
- `outputs/`
- `datasets/`
- generated degraded roots
- checkpoints
- `*.pth.tar`
- temporary suite failure logs unless needed for debugging

## 10. Next analysis step after running

After the batch completes on Speed, create a new failure-focused comparison report from `experiments/baseline_results.csv`. The report should compare original baseline and HPC RG-SSB on the expanded UAV123/NFS subsets, identify whether the previously observed failures persist, and decide whether to expand evaluation again or add target-region feature consistency.
