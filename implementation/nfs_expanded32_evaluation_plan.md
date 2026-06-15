# NFS Expanded-32 Evaluation Plan

## Why This Expansion Is Needed

NFS is currently the weakest benchmark for the current best HPC RG-SSB lambda `0.02` checkpoint. In the paper-level result table, expanded NFS has average AUC change `-0.014195`, while broader OTB and expanded UAV123 are positive. This batch expands NFS from 16 to 32 selected sequences to test whether the NFS weakness is sequence-specific or systematic.

No training or architecture changes should be made before this expanded NFS evidence is available.

## Selected Sequences

Already evaluated sequences retained:

- `nfs_Gymnastics`
- `nfs_basketball_player`
- `nfs_car`
- `nfs_dog`
- `nfs_running`
- `nfs_bottle`
- `nfs_bird_2`
- `nfs_walking`
- `nfs_basketball_player_2`
- `nfs_car_drifting`
- `nfs_car_jumping`
- `nfs_cheetah`
- `nfs_horse_running`
- `nfs_motorcross`
- `nfs_person_scooter`
- `nfs_soccer_player_2`

Additional sequences:

- `nfs_basketball_1`
- `nfs_biker_acrobat`
- `nfs_biker_all_1`
- `nfs_biker_whole_body`
- `nfs_bowling_1`
- `nfs_car_camaro`
- `nfs_car_rc_rolling`
- `nfs_car_side`
- `nfs_dog_1`
- `nfs_drone`
- `nfs_footbal_skill`
- `nfs_helicopter`
- `nfs_parkour`
- `nfs_running_100_m`
- `nfs_soccer_ball_2`
- `nfs_tiger`

The subset covers people, vehicles, animals, sports balls, small objects, fast motion, and camera-motion-sensitive sequences. The verifier uses the existing aligned NFS annotation logic and does not compare raw annotation lines directly to frame count.

## Configs

- `configs/nfs_eval_suite_expanded32_ostrack.json`
- `configs/nfs_eval_suite_expanded32_hpc_rgssb_featcons_lam002.json`
- `configs/nfs_expanded32_eval_batch.json`

Each suite uses four conditions:

- clean, severity `none`, seed `0`
- motion blur, severity `medium`, seed `42`
- low resolution, severity `medium`, seed `42`
- Gaussian noise, severity `medium`, seed `42`

## Expected Row Counts

- 32 sequences x 4 conditions = 128 rows per config.
- 2 configs = 256 possible rows.
- The first 16 sequences have already been evaluated for both configs.
- Expected new rows with `--skip_existing`: 16 new sequences x 4 conditions x 2 configs = 128 rows.

## Dry-Run Command

```bash
python3 scripts/run_nfs_expanded_eval_batch.py \
  --batch_config configs/nfs_expanded32_eval_batch.json \
  --dry_run
```

## Real Run Command on Speed

```bash
cd /speed-scratch/a_idrais/Paper_2_Mamba_Tracking
python3 scripts/run_nfs_expanded_eval_batch.py \
  --batch_config configs/nfs_expanded32_eval_batch.json
```

The batch runner passes `--skip_existing` by default, so completed NFS rows in `experiments/baseline_results.csv` are skipped.

## What To Commit

- Expanded NFS suite configs.
- Expanded NFS batch config.
- Expanded NFS batch runner.
- Expanded NFS verifier.
- This plan.

## What Not To Commit

- checkpoints
- `external/OSTrack/output/`
- `outputs/`
- generated degraded datasets
- copied datasets
- temporary failure logs unless needed for debugging

## Next Analysis Step After Running

After the expanded NFS batch completes, parse `experiments/baseline_results.csv` and create an expanded NFS result report comparing the original OSTrack baseline against the current best HPC RG-SSB checkpoint. The key decision is whether NFS remains negative after doubling the selected sequence coverage.

