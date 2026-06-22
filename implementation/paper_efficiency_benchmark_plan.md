# Paper Efficiency Benchmark Plan

## Purpose

This package defines a reproducible efficiency and complexity protocol for Paper Freeze V1. It compares the original OSTrack baseline against the frozen final RG-SSB method:

- Baseline: `vitb_256_mae_ce_32x4_ep300`
- Final method: `vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002`

The final method is OSTrack + RG-SSB + box head, with the backbone frozen, global clean/degraded feature consistency at lambda 0.02, response consistency disabled, and target-region consistency disabled.

## Same-Hardware Requirement

Runtime numbers are paper-ready only if both models are measured on the same GPU, in the same process environment, with the same sequence, same frame subset, same template/search sizes, same warm-up protocol, same CUDA/PyTorch settings, and the same measurement script. Historical timing files are not combined with controlled measurements because their hardware provenance is not encoded in the result files.

## Controlled Protocol

Default sequence: `Car1` under clean OTB.

Default runtime protocol:

- one GPU
- batch size 1 tracker execution
- 50 warm-up frames if available
- 3 measured repetitions
- CUDA synchronization before and after timed regions
- checkpoint/model loading excluded
- first-frame tracker initialization measured separately
- first-frame initialization excluded from tracking FPS
- one row per model per repetition plus an aggregate row
- no writes to `experiments/baseline_results.csv`

The runtime command writes to `experiments/paper_efficiency_results.csv`.

## Complexity Method

`scripts/collect_ostrack_complexity.py` builds both models from their OSTrack YAML configs and records:

- total parameters
- trainable parameters
- frozen parameters
- backbone parameters
- RG-SSB parameters
- box-head parameters
- trainable tensor count
- checkpoint size when the checkpoint exists locally

The final method applies `TRAIN.FREEZE_MODE=rgssb_head`, so only `rgssb.*` and `box_head.*` parameters remain trainable. The baseline config uses the default unfrozen model state for parameter accounting.

## FLOP/MAC Status

FLOPs/MACs are reported as unavailable unless a reliable tracer can handle the actual OSTrack forward path with template shape `[1, 3, 128, 128]` and search shape `[1, 3, 256, 256]`. Dynamic tracker operations and custom output dictionaries make ad hoc FLOP tracing risky. No FLOP value should be invented.

## Historical Timing Audit

Existing `*_time.txt` files are inspected by `scripts/verify_efficiency_benchmark_setup.py`. They can identify which configs have prior timing outputs and their apparent FPS, but they are not paper-ready unless the GPU, software environment, sequence, and measurement protocol are known and matched for both models.

## Commands

Local GTX 1080 controlled benchmark:

```bash
python3 scripts/benchmark_ostrack_efficiency.py \
  --benchmark_config configs/paper_efficiency_benchmark.json
```

Speed controlled benchmark:

```bash
python3 scripts/benchmark_ostrack_efficiency.py \
  --benchmark_config configs/paper_efficiency_benchmark.json \
  --otb_root /speed-scratch/a_idrais/otb
```

Complexity table:

```bash
python3 scripts/collect_ostrack_complexity.py \
  --benchmark_config configs/paper_efficiency_benchmark.json
```

Check-only runtime setup:

```bash
python3 scripts/benchmark_ostrack_efficiency.py \
  --benchmark_config configs/paper_efficiency_benchmark.json \
  --check_only
```

## Paper Wording

Safe wording before controlled runtime measurement:

- "The RG-SSB variant adds a small parameter overhead relative to OSTrack."
- "Runtime will be reported using a same-GPU controlled protocol."
- "Historical timing files were not used as paper-ready FPS evidence because hardware provenance is incomplete."

Do not claim:

- final FPS
- final latency
- final GPU memory
- FLOPs/MACs
- equal hardware runtime comparison

until the controlled benchmark is executed.

## Do Not Commit

Do not commit:

- checkpoints
- `external/OSTrack/output/`
- generated tracker result files
- uncontrolled timing outputs
- large benchmark output directories
