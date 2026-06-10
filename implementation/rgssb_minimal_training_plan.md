# Minimal RG-SSB Training/Debug Plan

Date: 2026-06-10

Scope: inspection-only plan for the first minimal Restoration-Guided State Space Block (RG-SSB) training/debug experiment in OSTrack. No training was run and no `external/OSTrack` source, configs, or datasets were modified for this plan.

## 1. Training Entry Point

OSTrack training starts from `external/OSTrack/tracking/train.py`.

- `tracking/train.py::parse_args()` defines the training CLI arguments: `--script`, `--config`, `--save_dir`, `--mode`, `--nproc_per_node`, `--use_lmdb`, `--use_wandb`, and distillation arguments.
- `tracking/train.py::main()` builds a shell command. In `--mode single`, it runs `python lib/train/run_training.py ...`. In `--mode multiple`, it launches `torch.distributed.launch`.
- `lib/train/run_training.py::main()` parses runtime arguments, sets CUDA device, then calls `run_training(...)`.
- `lib/train/run_training.py::run_training()` builds a `Settings` object, sets `settings.cfg_file` to `external/OSTrack/experiments/<script>/<config>.yaml`, imports `lib.train.train_script`, and calls `train_script.run(settings)`.
- `lib/train/train_script.py::run()` imports `lib.config.<script>.config`, calls `update_config_from_file(settings.cfg_file)`, then calls `update_settings(settings, cfg)`.
- `lib/train/train_script.py::run()` builds dataloaders with `build_dataloaders(cfg, settings)`.
- `lib/train/train_script.py::run()` builds the model with `build_ostrack(cfg)`.
- `lib/train/train_script.py::run()` constructs `OSTrackActor`, optimizer/scheduler, then starts `LTRTrainer.train(cfg.TRAIN.EPOCH, load_latest=True, fail_safe=True)`.

Important files and functions:

- `external/OSTrack/tracking/train.py`: CLI wrapper and launch mode selection.
- `external/OSTrack/lib/train/run_training.py`: config path setup and train script import.
- `external/OSTrack/lib/train/train_script.py::run`: config loading, dataloaders, model, actor, optimizer, trainer.
- `external/OSTrack/lib/train/base_functions.py::build_dataloaders`: training and validation dataloader construction.
- `external/OSTrack/lib/train/base_functions.py::get_optimizer_scheduler`: trainable parameter grouping and optimizer creation.
- `external/OSTrack/lib/models/ostrack/ostrack.py::build_ostrack`: OSTrack model construction and pretrained checkpoint loading.
- `external/OSTrack/lib/train/trainers/ltr_trainer.py::cycle_dataset`: forward, loss, backward, optimizer step.
- `external/OSTrack/lib/train/trainers/base_trainer.py::train`: checkpoint resume/save orchestration.

## 2. Dataset Path Requirements

Training dataset paths are defined in `external/OSTrack/lib/train/admin/local.py` through `EnvironmentSettings`.

Local inspected paths:

- `lasot_dir`: `external/OSTrack/data/lasot`
- `got10k_dir`: `external/OSTrack/data/got10k/train`
- `got10k_val_dir`: `external/OSTrack/data/got10k/val`
- `trackingnet_dir`: `external/OSTrack/data/trackingnet`
- `coco_dir`: `external/OSTrack/data/coco`
- `imagenet_dir`: `external/OSTrack/data/vid`
- LMDB variants are also defined for LaSOT, GOT-10k, TrackingNet, COCO, and VID.

`external/OSTrack/lib/train/admin/environment.py::create_default_local_file_ITP_train()` shows the expected default layout under a generic `data_dir`:

- `data_dir/lasot`
- `data_dir/got10k/train`
- `data_dir/got10k/val`
- `data_dir/trackingnet`
- `data_dir/coco`
- `data_dir/vid`

Training dataset registry:

`external/OSTrack/lib/train/base_functions.py::names2datasets()` accepts only:

- `LASOT`
- `GOT10K_vottrain`
- `GOT10K_votval`
- `GOT10K_train_full`
- `GOT10K_official_val`
- `COCO17`
- `VID`
- `TRACKINGNET`

OTB is not listed in the training dataset registry. OTB is therefore not directly usable by the inspected OSTrack training pipeline without adding a new training dataset adapter or converting a tiny debug subset to an existing expected interface.

Expected dataset interface:

- Dataset classes inherit from `BaseVideoDataset`.
- Required methods include `get_name()`, `get_num_sequences()`, `get_sequence_info(seq_id)`, and `get_frames(seq_id, frame_ids, anno=None)`.
- `get_sequence_info()` returns at least `bbox`, `valid`, and `visible`.
- `get_frames()` returns frame images, per-frame annotation dicts, and object metadata.
- `TrackingSampler` samples template/search frame ids from visible frames, then expects `template_images`, `template_anno`, `search_images`, and `search_anno`.

Format examples:

- GOT-10k loader expects a root containing `list.txt`, per-sequence folders, `groundtruth.txt`, `absence.label`, and `cover.label`.
- LaSOT loader expects class folders, sequence folders, `img/`, `groundtruth.txt`, `full_occlusion.txt`, and `out_of_view.txt`.

## 3. Loss Computation

Losses are configured in `external/OSTrack/lib/train/train_script.py::run()`.

- `giou`: `lib.utils.box_ops.giou_loss`
- `l1`: `torch.nn.functional.l1_loss`
- `focal`: `lib.train.utils.focal_loss.FocalLoss`
- `cls`: `torch.nn.BCEWithLogitsLoss`

Default OSTrack loss computation is in `external/OSTrack/lib/train/actors/ostrack.py::OSTrackActor.compute_losses()`.

- Ground-truth heatmaps are generated with `generate_heatmap(...)`.
- Predicted boxes come from `pred_dict['pred_boxes']`.
- GIoU loss is computed between predicted boxes and ground-truth boxes.
- L1 box loss is computed between predicted boxes and ground-truth boxes.
- Location/classification-style response loss uses focal loss on `pred_dict['score_map']`.
- The default total loss is:
  - `GIOU_WEIGHT * giou_loss + L1_WEIGHT * l1_loss + focal_loss`

The inspected default path creates a `cls` BCE objective, but the normal `compute_losses()` path does not use it unless later classification-specific training code is enabled.

Later feature/response consistency insertion points:

- Feature consistency loss could be added after model forward in `OSTrackActor.forward_pass()` if the network exposes clean/degraded intermediate features.
- Response consistency loss could be added in `OSTrackActor.compute_losses()` using `score_map`, `size_map`, `offset_map`, or predicted boxes from paired clean/degraded samples.
- A cleaner later approach would require the dataloader to emit paired clean/degraded template-search samples instead of adding ad hoc loss logic to the actor first.

## 4. Minimal Training Strategy Options

### A. Train Only RG-SSB, Freeze All Existing OSTrack

- Difficulty: lowest.
- GTX 1080 memory risk: lowest, because only RG-SSB parameters need gradients.
- Expected usefulness: good first answer to whether RG-SSB can receive gradients and learn without destabilizing the pretrained tracker.
- Clean tracking risk: lowest.
- Limitation: fixed backbone and head may limit the improvement that RG-SSB can learn.
- Recommendation: best first training/debug route.

### B. Train RG-SSB + Tracking Head

- Difficulty: moderate.
- GTX 1080 memory risk: moderate.
- Expected usefulness: higher than RG-SSB-only if the head must adapt to restored features.
- Clean tracking risk: moderate; the head can overfit a tiny degraded subset and hurt clean tracking.
- Recommendation: second route after RG-SSB-only smoke training is stable.

### C. Train RG-SSB + Last Backbone Blocks

- Difficulty: higher.
- GTX 1080 memory risk: high.
- Expected usefulness: potentially useful for adapting feature representation.
- Clean tracking risk: high relative to the small local debug data.
- Recommendation: postpone until there is a validated debug dataset and a reason to adapt backbone features.

### D. Full Fine-Tuning

- Difficulty: highest.
- GTX 1080 memory risk: very high.
- Expected usefulness: not suitable for the first local debug experiment.
- Clean tracking risk: highest.
- Recommendation: avoid locally; consider only later on HPC with proper train/val splits.

## 5. First Proof-of-Training Experiment

Question: Can RG-SSB learn useful weights without breaking OSTrack?

Recommended first experiment:

- Use an OTB-derived debug training subset from `Car1` and `David2` or one tiny existing GOT-10k/LaSOT subset if already present locally.
- Treat OTB-derived training only as a sanity/debug experiment, not as paper evidence.
- Degradation: start with `motion_blur` medium or `low_resolution` medium. Motion blur is already severe in baseline results, while low resolution tests the restored-feature hypothesis directly.
- Batch size: `1` first; increase to `2` only if memory is stable.
- Iterations: 100 optimizer steps for smoke training.
- Freeze: backbone and tracking head frozen; train only RG-SSB.
- Save: RG-SSB-enabled debug checkpoint, training log, final loss summary, and exact config.
- Metrics after training:
  - Training loss is finite and decreases over the 100-step run.
  - RG-SSB gradients are nonzero.
  - No NaNs in predicted boxes or score maps.
  - Clean Car1 evaluation does not collapse.
  - Degraded Car1 evaluation is at least not worse than the untrained RG-SSB debug path.

Success indicator:

- The training loop runs for 100 iterations without OOM or NaNs, loss trends downward, RG-SSB weights change, and clean Car1 remains in the same broad performance range as the pretrained baseline.

Failure indicator:

- OOM at batch size 1, NaNs, no RG-SSB gradients, checkpoint cannot load, or clean Car1 tracking collapses after training.

## 6. Training Config Plan

Proposed future config name:

`external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_train_debug.yaml`

Do not create it until the next implementation task.

Planned properties:

- Copy the debug RG-SSB inference config as the base.
- Set `MODEL.RGSSB.ENABLE: True`.
- Use the original OSTrack checkpoint as initialization.
- Load the original checkpoint with `strict=False` because RG-SSB parameters are new.
- Set `TRAIN.BATCH_SIZE: 1` initially.
- Set `TRAIN.NUM_WORKER: 0` or `2`.
- Set `TRAIN.EPOCH: 1`.
- Set `DATA.TRAIN.SAMPLE_PER_EPOCH: 100`.
- Set `DATA.VAL.SAMPLE_PER_EPOCH: 20` or disable validation only if the trainer can safely handle it.
- Use `TRAIN.AMP: False` for the first deterministic debug run; enable AMP only if memory pressure requires it.
- Use a small learning rate for RG-SSB, e.g. `1e-4`.
- Freeze backbone and head outside the YAML if no config support exists yet.

Important implementation note:

`get_optimizer_scheduler()` currently trains all non-backbone parameters in its default path and backbone parameters with `LR * BACKBONE_MULTIPLIER`. Since RG-SSB is a non-backbone module in the current integration, a true RG-SSB-only experiment will need a later freeze or optimizer-selection patch.

## 7. Minimal Dataset Plan

Options:

1. Tiny GOT-10k train subset
   - Most compatible with the existing OSTrack training pipeline.
   - Requires local GOT-10k train files in the expected format.
   - Best if the dataset already exists locally.

2. Tiny LaSOT subset
   - Also compatible with existing loader code.
   - Requires LaSOT local files in the expected class/sequence format.
   - Good for later but heavier than an OTB sanity check.

3. OTB-based debug training subset
   - Fastest to create from local OTB sequences already used for evaluation.
   - Not natively supported by the inspected training registry.
   - Requires a small new dataset adapter or conversion to an expected loader format.
   - Suitable only for smoke training and debugging, not final evidence.

4. Synthetic template-search pairs from Car1/David2
   - Fastest and safest for a GTX 1080 local proof of gradient flow.
   - Can use clean template and degraded search pairs to test restoration-guided behavior.
   - Requires custom debug dataset/sampler code later.
   - Best first local route if GOT-10k/LaSOT are unavailable.

Fastest local recommendation:

Use synthetic template-search pairs from `Car1` and `David2` for a 100-iteration sanity run, while clearly labeling the result as debug-only. If a tiny GOT-10k or LaSOT subset is already present, prefer that for a pipeline-compatible smoke run.

## 8. GTX 1080 8 GB Memory Constraints

Recommendations:

- Use one GPU.
- Use `--mode single`.
- Start with batch size `1`.
- Keep template/search sizes at OSTrack defaults: template `128`, search `256`.
- Freeze backbone and tracking head for the first run.
- Train only RG-SSB.
- Use `NUM_WORKER: 0` for first debug reproducibility; increase to `2` after the loader is stable.
- Use `AMP: False` first to simplify debugging; enable AMP only if memory is tight.
- Keep `SAMPLE_PER_EPOCH` small, e.g. `100`.
- Avoid DDP and multi-GPU launch locally.
- Avoid unfreezing ViT blocks until RG-SSB-only training is stable.

Relevant prior measurement:

Standalone RG-SSB GPU test on GTX 1080 reported `[2, 256, 768]` forward/backward success with 2,079,936 parameters and low standalone memory allocation. Full OSTrack training memory will be dominated by backbone activations unless the backbone is frozen and evaluated carefully.

## 9. Implementation Stages

Stage 1: Training code inspection only.

- Completed by this plan.

Stage 2: Create tiny dataset subset.

- Prefer synthetic OTB template-search debug pairs from Car1/David2 if no standard training dataset is available.
- Otherwise create a tiny GOT-10k/LaSOT subset using existing loader formats.

Stage 3: Create RG-SSB debug training config.

- Add `vitb_256_mae_ce_32x4_ep300_rgssb_train_debug.yaml`.
- Enable RG-SSB.
- Keep batch size, workers, and schedule small.

Stage 4: Freeze backbone and train RG-SSB only.

- Add a minimal freeze/optimizer path so only `rgssb` parameters are trainable.
- Confirm trainable parameter names before running.

Stage 5: Run 100-iteration smoke training.

- Check loss, gradients, NaNs, memory, checkpoint save.

Stage 6: Evaluate clean/degraded Car1.

- Use existing evaluation automation.
- Run clean Car1 first to detect clean collapse.
- Then run the selected degraded Car1 condition.

Stage 7: Decide whether to move to HPC.

- Move to larger data only if local smoke training is stable and does not damage clean tracking.

## 10. Files Likely Needing Modification Later

Config files:

- `external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_train_debug.yaml`
- Possibly `external/OSTrack/lib/config/ostrack/config.py` if new train freeze flags are added.

Dataset loader files:

- Possible new debug dataset adapter under `external/OSTrack/lib/train/dataset/`.
- `external/OSTrack/lib/train/base_functions.py` if the new adapter must be registered in `names2datasets()`.
- A main-project script to create tiny synthetic pairs from OTB, if using OTB debug data.

Model/checkpoint loading files:

- `external/OSTrack/lib/models/ostrack/ostrack.py` if training-time RG-SSB checkpoint behavior needs extra reporting.
- `external/OSTrack/lib/train/train_script.py` if checkpoint initialization or freeze reporting needs to be explicit.

Training actor/loss files:

- `external/OSTrack/lib/train/actors/ostrack.py` later for feature or response consistency losses.
- `external/OSTrack/lib/train/base_functions.py` for RG-SSB-only optimizer parameter selection.

Scripts/tests:

- A small training smoke wrapper script in the main project.
- A trainable-parameter inspection script.
- Existing evaluation scripts for clean/degraded Car1 after training.

## 11. Files Not To Touch Initially

Avoid modifying these during the first training/debug attempt:

- Original baseline config `external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300.yaml`
- OSTrack test entry point `external/OSTrack/tracking/test.py`
- Full dataset loader behavior for LaSOT, GOT-10k, COCO, VID, and TrackingNet unless a tiny adapter is explicitly required.
- DDP/multi-node training code.
- Original checkpoints.
- Paper reports and evidence matrices.
- Baseline automation outputs and generated degraded evaluation roots.

## 12. Risks And Safeguards

Checkpoint loading risk:

- Original OSTrack checkpoints do not contain RG-SSB keys.
- Use `strict=False` only for RG-SSB-enabled configs.
- Preserve strict/default behavior for the baseline config.

OOM risk:

- Full OSTrack training can exceed GTX 1080 memory if the backbone is trainable.
- Start with batch size 1, one GPU, backbone/head frozen, and short schedule.

Overfitting tiny data:

- A 100-iteration debug run can overfit immediately.
- Treat it as a smoke test only; do not report it as performance evidence.

Clean performance collapse:

- Always evaluate clean Car1 after training before degraded runs.
- Stop if clean tracking collapses.

Training too many parameters:

- Current default optimizer includes all non-backbone trainable parameters.
- Add explicit RG-SSB-only freezing before the first training run.

Degraded improvement not transferring:

- Improvements on Car1/David2 synthetic pairs may not generalize.
- Move to tiny GOT-10k/LaSOT or HPC only after the smoke test validates training mechanics.

Accidental baseline modification:

- Keep original YAML disabled and unchanged.
- Use a separate debug training config and separate save directory.
- Keep generated checkpoints/logs out of commits unless intentionally archived as metadata.

## 13. Final Recommendation

The safest first training/debug route is:

1. Create a separate RG-SSB training debug config.
2. Load the original OSTrack checkpoint with `strict=False`.
3. Freeze the OSTrack backbone and tracking head.
4. Train only RG-SSB for 100 iterations on a tiny debug dataset.
5. Use synthetic OTB template-search pairs from Car1/David2 if no standard tiny GOT-10k/LaSOT subset is available.
6. Evaluate clean Car1 first, then one degraded Car1 condition.

This route is minimal, realistic for GTX 1080, and directly tests whether RG-SSB can be trained without breaking OSTrack.

## Inspection Commands Run

```bash
nl -ba external/OSTrack/lib/train/actors/ostrack.py | sed -n '1,220p'
nl -ba external/OSTrack/lib/train/data/processing.py | sed -n '1,240p'
nl -ba external/OSTrack/lib/train/trainers/ltr_trainer.py | sed -n '1,240p'
rg -n "load_state_dict|save_checkpoint|load_latest|resume|checkpoint|PRETRAIN_FILE|build_ostrack" external/OSTrack/lib/train external/OSTrack/lib/models/ostrack -g '*.py'
nl -ba external/OSTrack/lib/train/trainers/base_trainer.py | sed -n '1,310p'
nl -ba external/OSTrack/lib/train/dataset/base_video_dataset.py | sed -n '1,180p'
nl -ba external/OSTrack/lib/train/dataset/got10k.py | sed -n '1,240p'
nl -ba external/OSTrack/lib/train/dataset/lasot.py | sed -n '1,220p'
nl -ba external/OSTrack/lib/train/base_functions.py | sed -n '1,260p'
nl -ba external/OSTrack/lib/train/train_script.py | sed -n '1,140p'
nl -ba external/OSTrack/lib/models/ostrack/ostrack.py | sed -n '1,220p'
nl -ba external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300.yaml | sed -n '1,220p'
nl -ba external/OSTrack/tracking/train.py | sed -n '1,180p'
nl -ba external/OSTrack/lib/train/run_training.py | sed -n '1,150p'
nl -ba external/OSTrack/lib/train/admin/local.py | sed -n '1,80p'
nl -ba external/OSTrack/lib/train/admin/environment.py | sed -n '1,130p'
nl -ba external/OSTrack/lib/train/data/sampler.py | sed -n '1,280p'
git status --short
```

## Uncertain Fields

- Whether local GOT-10k or LaSOT training data is actually present and valid was not verified by opening dataset roots.
- Exact memory usage for full OSTrack RG-SSB training is not known until a smoke run is executed.
- The best degradation for first training is not proven; `motion_blur` and `low_resolution` are both reasonable debug candidates.
- Whether an OTB-derived debug dataset should be implemented as a new loader or as converted GOT/LaSOT-like folders remains a later implementation choice.
