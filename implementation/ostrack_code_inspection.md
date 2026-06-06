# OSTrack Code Inspection

Inspection target:

- `external/OSTrack`

Purpose:

- Understand the OSTrack repository structure.
- Identify safe integration points for the existing synthetic degradation pipeline.
- Identify future integration points for a minimal Restoration-Guided State Space Block, feature consistency loss, response consistency loss, and response-map visualization.

This inspection is read-only. No OSTrack files were modified.

## 1. Main repository folders

Top-level folders:

| folder | observed purpose |
|---|---|
| `assets/` | Figures and README assets. |
| `docker/` | Dockerfile for environment setup. |
| `experiments/ostrack/` | YAML experiment configs such as `vitb_256_mae_ce_32x4_ep300.yaml`. |
| `lib/config/ostrack/` | Python config defaults and YAML update logic. |
| `lib/models/` | Model definitions, backbone, heads, and model builders. |
| `lib/train/` | Training entry points, actors, data processing, datasets, loaders, trainers, objectives. |
| `lib/test/` | Tracker wrapper, evaluation datasets, parameter loading, result analysis utilities. |
| `lib/utils/` | Box utilities, focal loss, tensor helpers, candidate-elimination helpers. |
| `lib/vis/` | Visualization helpers. |
| `tracking/` | User-facing train/test/profile/visualization scripts. |

Top-level files:

| file | observed purpose |
|---|---|
| `README.md` | Installation, data preparation, training, evaluation, visualization instructions. |
| `install.sh` | Environment setup script. Not used in this inspection. |
| `ostrack_cuda113_env.yaml` | Conda environment definition. Not installed in this inspection. |
| `LICENSE` | License file. |

## 2. Where training code is located

Main training entry path:

1. `tracking/train.py`
   - Parses command-line arguments.
   - Builds a command that calls `lib/train/run_training.py`.
   - Supports single, multiple, and multi-node modes.

2. `lib/train/run_training.py`
   - Entry point called by `tracking/train.py`.
   - Loads the selected training script.

3. `lib/train/train_script.py`
   - Loads the YAML config.
   - Calls `build_dataloaders`.
   - Builds the OSTrack model via `build_ostrack(cfg)`.
   - Creates loss objectives.
   - Creates `OSTrackActor`.
   - Creates optimizer/scheduler and `LTRTrainer`.

4. `lib/train/trainers/ltr_trainer.py`
   - Training loop wrapper.

Important observed lines:

- `lib/train/train_script.py` builds dataloaders around lines 47-48.
- `lib/train/train_script.py` builds the network around lines 53-56.
- `lib/train/train_script.py` defines losses/objectives around lines 70-75.

## 3. Where testing/evaluation code is located

Main evaluation entry path:

1. `tracking/test.py`
   - User-facing test script.
   - Calls `get_dataset`.
   - Wraps the tracker with `Tracker`.
   - Runs `run_dataset`.

2. `lib/test/parameter/ostrack.py`
   - Loads experiment YAML.
   - Builds `TrackerParams`.
   - Sets template/search sizes and checkpoint path.

3. `lib/test/tracker/ostrack.py`
   - Online tracker class.
   - `initialize()` crops the template and preprocesses it.
   - `track()` crops the search region, runs the network, applies the Hann window, predicts boxes, and updates tracker state.

4. `lib/test/evaluation/`
   - Dataset wrappers for OTB, NFS, UAV, GOT-10k, LaSOT, TrackingNet, VOT, and other benchmarks.

Important observed lines:

- `lib/test/tracker/ostrack.py` initializes the template crop around lines 50-57.
- `lib/test/tracker/ostrack.py` crops the search region around lines 73-79.
- `lib/test/tracker/ostrack.py` calls `network.forward` around lines 80-85.
- `lib/test/tracker/ostrack.py` uses `score_map`, Hann window, `size_map`, and `offset_map` around lines 87-91.
- `lib/test/tracker/ostrack.py` already has debug response-map visualization hooks around lines 109-112.

## 4. Where model/backbone code is located

Main model files:

| file | purpose |
|---|---|
| `lib/models/ostrack/ostrack.py` | Defines `OSTrack`, `forward`, `forward_head`, and `build_ostrack`. |
| `lib/models/ostrack/base_backbone.py` | Basic ViT backbone tracking adaptation; patch embedding, template/search token combination, transformer blocks, token recovery. |
| `lib/models/ostrack/vit.py` | ViT implementation. |
| `lib/models/ostrack/vit_ce.py` | ViT with candidate elimination. |
| `lib/models/ostrack/utils.py` | `combine_tokens` and `recover_tokens` for template/search token ordering. |
| `lib/models/layers/head.py` | Corner and center tracking heads. |

Observed model flow:

1. `OSTrack.forward(template, search, ...)` calls `self.backbone(z=template, x=search, ...)`.
2. The backbone patch-embeds template and search separately.
3. Template and search tokens are combined with `combine_tokens`.
4. Transformer blocks process the combined sequence.
5. Tokens are recovered with `recover_tokens`.
6. `OSTrack.forward_head` keeps the search tokens and reshapes them into a feature map.
7. The box head produces `pred_boxes`, `score_map`, and for the center head, `size_map` and `offset_map`.

Important observed lines:

- `lib/models/ostrack/ostrack.py` calls the backbone around lines 40-49.
- `lib/models/ostrack/ostrack.py` stores `out['backbone_feat']` around line 58.
- `lib/models/ostrack/ostrack.py` extracts search tokens in `forward_head` around lines 61-69.
- `lib/models/ostrack/ostrack.py` returns `score_map`, `size_map`, and `offset_map` for the center head around lines 80-89.
- `lib/models/ostrack/base_backbone.py` patch-embeds template/search around lines 110-115.
- `lib/models/ostrack/base_backbone.py` combines template/search tokens around line 127.
- `lib/models/ostrack/base_backbone.py` runs transformer blocks around lines 133-134.
- `lib/models/ostrack/base_backbone.py` recovers token ordering around lines 136-141.
- `lib/models/ostrack/vit_ce.py` has similar logic with candidate elimination around lines 102-185.

## 5. Where template/search data processing happens

Training data path:

1. Dataset wrappers return frames and annotations.
2. `lib/train/data/sampler.py` samples template and search frame IDs.
3. `TrackingSampler.getitem()` creates a `TensorDict` with:
   - `template_images`
   - `template_anno`
   - `template_masks`
   - `search_images`
   - `search_anno`
   - `search_masks`
4. `self.processing(data)` applies `STARKProcessing`.
5. `STARKProcessing.__call__()` jitter-crops template/search regions and applies transforms.
6. `build_dataloaders()` defines train/validation transforms and constructs `STARKProcessing`.

Important observed lines:

- `lib/train/data/sampler.py` creates the template/search `TensorDict` around lines 156-163.
- `lib/train/data/sampler.py` calls `self.processing(data)` around line 165.
- `lib/train/data/processing.py` crops template/search around lines 117-120.
- `lib/train/data/processing.py` applies template/search transforms around lines 121-123.
- `lib/train/base_functions.py` defines `transform_train`, `transform_val`, and `STARKProcessing` around lines 84-116.

Testing data path:

1. `lib/test/tracker/ostrack.py.initialize()` calls `sample_target` to create the initial template crop.
2. `lib/test/tracker/ostrack.py.track()` calls `sample_target` to create the search crop.
3. `Preprocessor.process()` converts the crop and mask for the model.

## 6. Where the tracking head is implemented

Main head file:

- `lib/models/layers/head.py`

Head types:

- `Corner_Predictor`
- `CenterPredictor`
- `MLP`

The default config sets:

- `cfg.MODEL.HEAD.TYPE = "CENTER"`

Observed center-head outputs:

- `score_map_ctr`
- `bbox`
- `size_map`
- `offset_map`

Important observed lines:

- `CenterPredictor.forward()` returns score, box, size, and offset around lines 130-140.
- `CenterPredictor.cal_bbox()` converts score/size/offset maps to boxes around lines 142-160.
- `CenterPredictor.get_score_map()` produces center, offset, and size maps around lines 175-201.
- `build_box_head()` creates the center head around lines 240-245.

## 7. Where losses are implemented

Main loss locations:

| file | purpose |
|---|---|
| `lib/train/train_script.py` | Creates objective dictionary: GIoU, L1, focal, BCE. |
| `lib/train/actors/ostrack.py` | Runs forward pass and computes loss. |
| `lib/utils/focal_loss.py` | Focal loss implementation. |
| `lib/utils/box_ops.py` | Box conversion and GIoU utilities. |

Observed loss flow:

1. `train_script.py` creates:
   - `giou_loss`
   - `l1_loss`
   - `FocalLoss`
   - `BCEWithLogitsLoss`
2. `OSTrackActor.forward_pass()` runs the model.
3. `OSTrackActor.compute_losses()` computes:
   - GIoU loss on predicted boxes.
   - L1 loss on predicted boxes.
   - Focal loss on `pred_dict['score_map']` against a generated Gaussian map.
4. Weighted total loss is computed from GIoU, L1, and focal losses.

Important observed lines:

- `lib/train/train_script.py` objective creation around lines 70-75.
- `lib/train/actors/ostrack.py` forward pass around lines 38-75.
- `lib/train/actors/ostrack.py` loss computation around lines 77-110.
- `lib/train/actors/ostrack.py` uses `pred_dict['score_map']` for location/focal loss around lines 99-100.

## 8. Where configs are stored

Main config locations:

| location | purpose |
|---|---|
| `experiments/ostrack/*.yaml` | Experiment-specific YAML configs. |
| `lib/config/ostrack/config.py` | Default config and YAML update logic. |
| `lib/test/parameter/ostrack.py` | Loads YAML config for testing and sets checkpoint path. |

Important default config fields:

- `cfg.MODEL.BACKBONE.TYPE`
- `cfg.MODEL.BACKBONE.STRIDE`
- `cfg.MODEL.HEAD.TYPE`
- `cfg.DATA.SEARCH.SIZE`
- `cfg.DATA.TEMPLATE.SIZE`
- `cfg.DATA.MEAN`
- `cfg.DATA.STD`
- `cfg.TRAIN.GIOU_WEIGHT`
- `cfg.TRAIN.L1_WEIGHT`
- `cfg.TEST.TEMPLATE_SIZE`
- `cfg.TEST.SEARCH_SIZE`

Future degradation-specific config should be added outside `external/OSTrack` first, then only mirrored into OSTrack configs if direct modification becomes necessary.

## 9. Safest integration points

### Synthetic degradation during data loading

Safest future training hook:

- `lib/train/data/processing.py`, inside `STARKProcessing.__call__()`, after `jittered_center_crop` returns `crops` and before `self.transform[s]` converts images to tensors and normalizes them.

Reason:

- The images are already cropped to template/search patches.
- The final image size is preserved by our degradation pipeline.
- Bounding boxes and masks do not need geometric changes.
- Template/search pair modes can be applied at this level.

Relevant area:

- `crops, boxes, att_mask, mask_crops = prutils.jittered_center_crop(...)`
- then `self.transform[s](image=crops, bbox=boxes, att=att_mask, mask=mask_crops, joint=False)`

Safer first approach:

- Do not edit `external/OSTrack` immediately.
- Create a wrapper or a small forked processing class in our own `src/` that imports OSTrack processing logic and applies degradation to cropped images.

Testing/inference degradation hook:

- `lib/test/tracker/ostrack.py.initialize()` after `z_patch_arr` is sampled and before `self.preprocessor.process(...)`.
- `lib/test/tracker/ostrack.py.track()` after `x_patch_arr` is sampled and before `self.preprocessor.process(...)`.

This is useful for controlled degraded-template/search evaluation without changing dataset files.

### Restoration-Guided State Space Block

Potential future insertion points:

1. Search-feature-only minimal insertion:
   - `lib/models/ostrack/ostrack.py`, inside `forward_head()`, after extracting `enc_opt` and reshaping `opt_feat`.
   - This is the simplest way to test whether an RG-SSB improves the search feature map used by the head.
   - Limitation: it is search-side only and does not recover template features directly.

2. Template/search token insertion after patch embedding:
   - `lib/models/ostrack/base_backbone.py` and `lib/models/ostrack/vit_ce.py`, after `x = self.patch_embed(x)` and `z = self.patch_embed(z)`, before adding position embeddings and combining tokens.
   - This is more aligned with restoration-guided template/search feature recovery.
   - Risk: requires modifying backbone internals and handling both CE and non-CE variants.

3. Combined-token insertion after several transformer blocks:
   - In `base_backbone.py` or `vit_ce.py`, inside the block loop.
   - This could model template-search interactions but is more invasive and should not be first.

Recommended for first RG-SSB implementation:

- Start outside `external/OSTrack` if possible.
- If direct integration is required, use the search-feature-only insertion in `OSTrack.forward_head()` as the minimal test.
- Move to template/search token insertion only after the minimal version works.

### Feature consistency loss

Likely future location:

- `lib/train/actors/ostrack.py`

Reason:

- The actor owns the forward pass and loss computation.
- `OSTrack.forward()` already adds `out['backbone_feat']`.
- A future clean/degraded double forward could compute consistency between clean and degraded `backbone_feat` or selected feature maps.

Minimal future design:

1. Add degraded template/search crops through data processing.
2. Keep clean template/search crops if feature consistency needs paired clean/degraded inputs.
3. Run clean and degraded forwards in `OSTrackActor.forward_pass()`.
4. Compute `L_feat` in `compute_losses()`.

Risk:

- Doubling forward passes increases memory and runtime.
- `backbone_feat` may be a list or a concatenated token tensor, so feature selection must be explicit.

### Response consistency loss

Likely future location:

- `lib/train/actors/ostrack.py`

Reason:

- `pred_dict['score_map']` is already used for focal loss.
- A clean/degraded pair can compare clean and degraded `score_map` outputs.

Minimal future design:

- Compute `L_resp` between clean and degraded `score_map` tensors.
- Use this only after a clean/degraded paired training batch format exists.

### Response-map visualization

Safest future locations:

1. `lib/test/tracker/ostrack.py`
   - `pred_score_map = out_dict['score_map']` is already available.
   - Debug mode already visualizes `score_map` and `score_map_hann`.

2. External wrapper script
   - A wrapper can call the tracker and save response maps without changing OSTrack internals, if hooks expose `out_dict` or tracker state.

Recommended:

- Use an external wrapper first.
- If necessary, add a non-invasive debug/save flag later.

## 10. Minimal files likely needing modification for first proof-of-concept

Only after environment setup and baseline reproduction:

| purpose | likely files |
|---|---|
| Training-time degradation after crop | `lib/train/data/processing.py` or a copied/wrapped processing class in our `src/` |
| Test-time degraded template/search crops | `lib/test/tracker/ostrack.py` or a wrapper subclass |
| Minimal search-feature RG-SSB insertion | `lib/models/ostrack/ostrack.py` or a wrapper model class |
| Feature and response consistency losses | `lib/train/actors/ostrack.py` |
| Config toggles | `experiments/ostrack/*.yaml` and `lib/config/ostrack/config.py`, preferably copied first |
| Response-map saving | `lib/test/tracker/ostrack.py` or external visualization wrapper |

Best first modification strategy:

1. Do not edit files in `external/OSTrack` directly.
2. Create a small adapter layer in our repo after baseline setup.
3. Only patch OSTrack files if the adapter approach is too brittle.

## 11. Files that should not be touched initially

Avoid modifying these at first:

- Dataset wrappers under `lib/train/dataset/`.
- Evaluation dataset wrappers under `lib/test/evaluation/`.
- Core trainer loop under `lib/train/trainers/`.
- Distributed launch code in `tracking/train.py`.
- Environment local files.
- README/install scripts.
- Candidate-elimination internals in `lib/models/layers/attn_blocks.py`.
- All downloaded checkpoints/pretrained model files.

Reason:

- The minimal proof-of-concept only needs controlled degradation and a small feature block.
- Changing dataset wrappers or trainer infrastructure increases debugging risk before the base tracker is reproduced.

## 12. Risks of modifying OSTrack directly

1. Dirty external repository state makes future merges and debugging harder.
2. Direct changes can break baseline reproducibility.
3. Training code depends on specific tensor shapes: `template_images` and `search_images` are stacked with dimensions expected by `OSTrackActor`.
4. The CE backbone and non-CE backbone have different forward internals.
5. Feature consistency may require additional batch keys and double forwards, increasing memory.
6. Response consistency needs careful detaching or weighting to avoid destabilizing focal loss.
7. Test-time degradation must not accidentally degrade the tracker state in uncontrolled ways.
8. Environment setup may create `local.py` files inside OSTrack; those should be treated as machine-local config, not method changes.

## 13. Recommendation

Recommendation: **create a wrapper around OSTrack first**.

Decision options:

| option | recommendation | reason |
|---|---|---|
| Modify OSTrack directly | Not first | Highest risk to baseline reproducibility and external repo cleanliness. |
| Copy selected modules into our `src/` | Not first | May create a large maintenance burden and hidden divergence from OSTrack. |
| Create a wrapper around OSTrack | Recommended | Keeps external repo clean, supports controlled degradation tests, and lets us reproduce baseline first. |

Suggested path:

1. Set up OSTrack environment.
2. Reproduce a clean baseline without any method changes.
3. Add an external wrapper for degraded template/search inference.
4. Add a training-time wrapper or shallow fork for `STARKProcessing` only if training is needed.
5. Add RG-SSB after degradation evaluation is working.
6. Patch OSTrack directly only if wrapper-based integration blocks training.

## 14. Readiness assessment

The project is ready for OSTrack environment setup, with caution.

Before implementation:

- Confirm OSTrack dependencies and Python/PyTorch compatibility.
- Confirm checkpoint availability.
- Confirm a tiny clean inference run works.
- Keep `external/OSTrack` unchanged until baseline behavior is recorded.

Do not start training yet.

## 15. Verification

Files created or modified:

- `implementation/ostrack_code_inspection.md`

How the output was verified:

- Confirmed `external/OSTrack` exists and contains 176 files.
- Inspected top-level folders and key files using read-only filesystem scans.
- Read key files for training, testing, model, data processing, heads, losses, configs, and README usage.
- Did not run OSTrack setup, training, testing, dependency installation, or dataset download commands.
- Did not modify files under `external/OSTrack`.

Uncertain fields:

- Actual runtime behavior has not been verified because dependencies were not installed and no OSTrack commands were run.
- Public checkpoint availability and local path setup still need confirmation.
- The cleanest wrapper strategy depends on how much of OSTrack can be imported after environment setup.
- The future RG-SSB insertion point should be finalized only after a clean baseline and degraded-input evaluation work.

Whether the project is ready for OSTrack environment setup:

- Yes. The code structure is mapped well enough to proceed to environment setup and clean baseline reproduction, while keeping the external repository untouched.
