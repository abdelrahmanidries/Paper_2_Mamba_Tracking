# OSTrack RG-SSB Insertion Plan

## Scope

This is a planning-only inspection for adding a minimal Restoration-Guided State Space Block, RG-SSB, to OSTrack later. No `external/OSTrack` files were modified, no model code was implemented, no configs were changed, and no training was run.

Current baseline context from `experiments/baseline_results.csv`:

| sequence | degradation | severity | seed | success_auc | precision_20 | mean_center_error |
|---|---:|---:|---:|---:|---:|---:|
| Car1 | clean | none | 0 | 0.575995 | 0.746078 | 16.455626 |
| Car1 | low_resolution | medium | 42 | 0.214881 | 0.267647 | 55.176579 |
| Car1 | motion_blur | medium | 42 | 0.157212 | 0.198039 | 82.957024 |
| Car1 | jpeg_compression | medium | 42 | 0.240012 | 0.298039 | 57.769341 |
| Car1 | gaussian_noise | medium | 42 | 0.207270 | 0.250980 | 64.898727 |

These are local proof-of-concept baselines, not final paper results.

## 1. OSTrack Forward Path

Evaluation starts in `external/OSTrack/tracking/test.py`.

1. `tracking/test.py`
   - `run_tracker()` calls `get_dataset(dataset_name)`.
   - If `--sequence Car1` is provided, it selects `dataset[sequence]`.
   - It creates `Tracker(tracker_name, tracker_param, dataset_name, run_id)` and calls `run_dataset(...)`.

2. `lib/test/evaluation/tracker.py`
   - `Tracker.__init__()` imports `lib.test.tracker.ostrack`.
   - `Tracker.run_sequence()` loads params and creates the tracker instance.
   - `_track_sequence()` reads the first frame, calls `tracker.initialize(...)`, then calls `tracker.track(...)` for later frames.

3. `lib/test/parameter/ostrack.py`
   - `parameters(yaml_name)` loads `experiments/ostrack/<yaml_name>.yaml` using `update_config_from_file`.
   - It sets template/search factors and sizes.
   - It constructs checkpoint path `output/checkpoints/train/ostrack/<yaml_name>/OSTrack_ep0300.pth.tar`.

4. `lib/test/tracker/ostrack.py`
   - `OSTrack.__init__()` calls `build_ostrack(params.cfg, training=False)`.
   - It loads the checkpoint with `network.load_state_dict(..., strict=True)`.
   - `initialize()` crops and preprocesses the template once.
   - `track()` crops and preprocesses the search image, calls `self.network.forward(template=..., search=...)`, applies the Hann window to `score_map`, then uses `box_head.cal_bbox(...)`.

5. `lib/models/ostrack/ostrack.py`
   - `OSTrack.forward()` calls `self.backbone(z=template, x=search, ...)`.
   - `OSTrack.forward_head()` slices the final search tokens, reshapes them to a spatial feature map, and calls the tracking head.

6. `lib/models/ostrack/vit_ce.py`
   - For the active config, the backbone is `VisionTransformerCE`.
   - `forward_features()` patch-embeds template/search, adds positional embeddings, combines tokens, runs CE transformer blocks, recovers pruned search token order, then returns concatenated template/search tokens.

7. `lib/models/layers/head.py`
   - The configured head is `CenterPredictor`.
   - It outputs `score_map_ctr`, `bbox`, `size_map`, and `offset_map`.

## 2. Model Construction

Model construction:

- File: `external/OSTrack/lib/models/ostrack/ostrack.py`
- Function: `build_ostrack(cfg, training=True)`
- Model class: `OSTrack`
- Active backbone factory for current config: `vit_base_patch16_224_ce(...)`
- Active backbone class: `VisionTransformerCE`
- Active head builder: `build_box_head(cfg, hidden_dim)`
- Active head class: `CenterPredictor`

Config loading:

- Test config loader: `external/OSTrack/lib/test/parameter/ostrack.py`, function `parameters(yaml_name)`.
- Default config: `external/OSTrack/lib/config/ostrack/config.py`.
- Experiment YAML: `external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300.yaml`.
- Current config values relevant to shapes:
  - `DATA.TEMPLATE.SIZE = 128`
  - `DATA.SEARCH.SIZE = 256`
  - `MODEL.BACKBONE.STRIDE = 16`
  - `MODEL.BACKBONE.TYPE = vit_base_patch16_224_ce`
  - `MODEL.BACKBONE.CE_LOC = [3, 6, 9]`
  - `MODEL.BACKBONE.CE_KEEP_RATIO = [0.7, 0.7, 0.7]`
  - `MODEL.HEAD.TYPE = CENTER`

Checkpoint loading:

- Test-time checkpoint path is set in `lib/test/parameter/ostrack.py`.
- Test-time checkpoint load occurs in `lib/test/tracker/ostrack.py`, class `OSTrack.__init__`.
- Current code uses `strict=True`, which will fail if RG-SSB parameters are added to the model and absent from the checkpoint.
- Training-time pretrained OSTrack checkpoint loading in `build_ostrack()` uses `strict=False` only when `cfg.MODEL.PRETRAIN_FILE` contains `"OSTrack"` and `training=True`.

## 3. Backbone Output Shapes

Likely shapes for `vitb_256_mae_ce_32x4_ep300` with batch `B`.

| Stage | Likely shape | Evidence / uncertainty |
|---|---:|---|
| Template input to network | `[B, 3, 128, 128]` | Test preprocessor returns normalized tensor; actor comments match this. |
| Search input to network | `[B, 3, 256, 256]` in this config | YAML sets search size 256; actor comment says 320 for default training config, so exact runtime should be verified by hook. |
| Template patch tokens | `[B, 64, 768]` | 128 / 16 = 8, so 8x8 tokens; ViT-base dim 768. |
| Search patch tokens | `[B, 256, 768]` | 256 / 16 = 16, so 16x16 tokens. |
| Combined tokens before CE blocks | `[B, 320, 768]` | Direct concat of template + search tokens; no cls token in current config. |
| During CE blocks | Search length may shrink at CE layers | Candidate elimination occurs at blocks 3, 6, 9. Needs runtime hook verification for exact transient lengths. |
| Backbone output after recovery | `[B, 320, 768]` | `vit_ce.py` pads/reorders pruned search tokens and re-concats template/search. |
| Search feature sent to head | `[B, 256, 768]` | `OSTrack.forward_head()` selects last `feat_len_s`. |
| Head input feature map | `[B, 768, 16, 16]` | `forward_head()` reshapes search tokens using `feat_sz_s = 16`. |
| Score map | `[B, 1, 16, 16]` | `CenterPredictor.get_score_map()` center branch. |
| Size map | `[B, 2, 16, 16]` | Center head size branch. |
| Offset map | `[B, 2, 16, 16]` | Center head offset branch. |
| Pred boxes | `[B, 1, 4]` | `outputs_coord.view(bs, Nq, 4)` with `Nq=1`. |

Exact shapes should be confirmed later with a runtime hook on:

- `backbone.patch_embed`
- selected `backbone.blocks[i]`
- `OSTrack.forward_head`
- `box_head.get_score_map`

## 4. Candidate Insertion Points

### A. After Patch Embedding / Early Token Embedding

- File/function: `external/OSTrack/lib/models/ostrack/vit_ce.py`, `VisionTransformerCE.forward_features()`, after lines where `x = self.patch_embed(x)` and `z = self.patch_embed(z)`.
- Tensor modified: separate template/search token tensors, likely `z: [B, 64, 768]`, `x: [B, 256, 768]`.
- Advantages:
  - Degradation is addressed before template-search interaction.
  - Can operate separately on template and search features.
  - Feature-level restoration is conceptually clean.
- Risks:
  - Requires reshaping tokens to 2D grids and back.
  - Must handle template grid 8x8 and search grid 16x16.
  - Too early may disturb pretrained ViT features before all transformer processing.
  - If implemented inside `VisionTransformerCE`, checkpoint keys under `backbone.*` change.
- Expected difficulty: Medium.
- Checkpoint-loading risk: Medium to high unless module is disabled by default or checkpoint load is relaxed when enabled.
- Clean baseline unchanged with config flag: Yes, if `MODEL.RGSSB.ENABLE=False` bypasses the module exactly.

### B. After Selected Backbone Blocks

- File/function: `external/OSTrack/lib/models/ostrack/vit_ce.py`, `VisionTransformerCE.forward_features()`, inside the loop over `self.blocks`.
- Tensor modified: combined token tensor `x`, with dynamic template/search lengths due to CE.
- Advantages:
  - Can be inserted at semantic feature depths.
  - Matches the idea of restoration-guided intermediate feature recovery.
  - Could target stages after CE has removed background-heavy search tokens.
- Risks:
  - Candidate elimination changes search token length at configured blocks.
  - Reconstructing 2D search grids inside the CE loop is fragile when tokens are pruned.
  - More invasive and easier to break CE indexing.
- Expected difficulty: High.
- Checkpoint-loading risk: Medium to high.
- Clean baseline unchanged with config flag: Possible, but implementation risk is higher.

### C. After Backbone Output Before Tracking Head

- File/function: `external/OSTrack/lib/models/ostrack/ostrack.py`, `OSTrack.forward()`, between `self.backbone(...)` and `self.forward_head(...)`, or inside `forward_head()` before the current search-token reshape.
- Tensor modified:
  - Either full recovered token tensor `feat_last: [B, 320, 768]`.
  - Or only search tokens `enc_opt: [B, 256, 768]`.
- Advantages:
  - Minimum disruption to CE backbone.
  - Candidate-eliminated search tokens have already been recovered to original order.
  - Shape is stable for the head: search tokens always become `[B, 768, 16, 16]`.
  - Easy to bypass with config flag.
  - Preserves output shape if RG-SSB is residual.
  - Best first place for clean/degraded comparison without rewriting backbone internals.
- Risks:
  - Only post-backbone restoration, not early visual recovery.
  - Template tokens are not modified if applied only to `enc_opt`.
  - If applied to full tokens, template/search grid sizes differ and need careful splitting.
- Expected difficulty: Low to medium.
- Checkpoint-loading risk: Low if disabled by default; medium when enabled unless test load changes to tolerate new keys.
- Clean baseline unchanged with config flag: Yes.

### D. Inside the Head Path

- File/function: `external/OSTrack/lib/models/layers/head.py`, `CenterPredictor.forward()` or `get_score_map()`.
- Tensor modified: head input feature map `x: [B, 768, 16, 16]`, or branch-specific conv features.
- Advantages:
  - Pure 2D feature map interface.
  - No need to touch ViT token ordering or CE.
  - Directly affects response map, size map, and offset map branches.
- Risks:
  - Less clearly a backbone restoration block; may be perceived as a head enhancement.
  - Could entangle restoration with prediction head behavior.
  - If inserted inside all branches, duplicates compute and risk.
  - If inserted before branches, it still changes the head checkpoint namespace.
- Expected difficulty: Low.
- Checkpoint-loading risk: Medium if modifying `CenterPredictor`.
- Clean baseline unchanged with config flag: Yes, but this is less ideal as the first RG-SSB location.

## 5. Recommended Minimal Insertion Point

Recommended first insertion point:

**After backbone output, before the tracking head, applied only to recovered search tokens in `OSTrack.forward_head()` or immediately before calling it.**

Most conservative version:

1. Add optional `self.rgssb` to `OSTrack`.
2. In `forward_head()`, after:

```python
enc_opt = cat_feature[:, -self.feat_len_s:]
```

apply:

```python
if self.use_rgssb:
    enc_opt = self.rgssb(enc_opt, template_len=None, search_len=self.feat_len_s)
```

3. Keep output shape `[B, 256, 768]`.
4. Existing reshape to `[B, 768, 16, 16]` and center head remain unchanged.

Why this is best:

- It avoids modifying `VisionTransformerCE` and CE token pruning.
- It uses stable recovered search-token order.
- It is easy to disable with `MODEL.RGSSB.ENABLE=False`.
- It does not alter the input/output contract of the head.
- It supports feature-level restoration under degradation.
- It can later be expanded to template+search tokens or earlier backbone stages after runtime hooks prove shapes.
- It is the least likely insertion point to break the established clean/degraded baseline.

## 6. Config Flag Plan

Do not edit configs yet. Proposed future flags:

```yaml
MODEL:
  RGSSB:
    ENABLE: false
    POSITION: "pre_head_search"
    DIM: 768
    LOCAL_KERNEL: 3
    CHANNEL_ATTENTION: true
    STATE_SPACE_BRANCH: true
    RESIDUAL_SCALE_INIT: 0.0
    APPLY_TO: "search"
    GRID_SIZE: 16
```

Suggested meanings:

- `ENABLE`: hard on/off switch. Default must be `false`.
- `POSITION`: first value should be `pre_head_search`; later values could include `post_patch`, `after_block_6`, `head_input`.
- `DIM`: token/channel dimension, 768 for ViT-base.
- `LOCAL_KERNEL`: local enhancement branch kernel size.
- `CHANNEL_ATTENTION`: enable/disable channel selection.
- `STATE_SPACE_BRANCH`: enable/disable SSM/Mamba branch for ablation.
- `RESIDUAL_SCALE_INIT`: initialize residual scale to 0.0 for a near-identity start.
- `APPLY_TO`: `search` first; later `template_search`.
- `GRID_SIZE`: 16 for Car1/current search size 256 and stride 16; better computed from `feat_sz_s` in code.

## 7. Minimal RG-SSB Module Interface

Planning-only interface:

```python
class RestorationGuidedSSB(nn.Module):
    def __init__(
        self,
        dim: int,
        local_kernel: int = 3,
        channel_attention: bool = True,
        state_space_branch: bool = True,
        residual_scale_init: float = 0.0,
    ):
        ...

    def forward(
        self,
        x: torch.Tensor,
        template_len: int | None = None,
        search_len: int | None = None,
        spatial_size: tuple[int, int] | None = None,
    ) -> torch.Tensor:
        return x
```

Expected first input/output:

- Input: search tokens `x` with shape `[B, 256, 768]`.
- `spatial_size`: `(16, 16)` or inferred from `sqrt(search_len)`.
- Internally, the module can reshape to `[B, 768, 16, 16]`, apply local/state-space/channel operations, then return `[B, 256, 768]`.
- Output shape must exactly match input shape.

For a later full token version:

- Input: combined tokens `[B, Lz + Lx, C]`.
- `template_len=64`, `search_len=256`.
- Split template/search, process either search-only or both grids, then re-concat.

## 8. Checkpoint Loading Risk

Current test-time load:

- `lib/test/tracker/ostrack.py` uses `strict=True`.
- Adding `self.rgssb` parameters will make original checkpoint loading fail unless the model is built without RG-SSB parameters when disabled or the load policy changes.

Safest policy:

1. When `MODEL.RGSSB.ENABLE=False`, do not instantiate `self.rgssb` as a parameterized module. Use `self.rgssb = None` or `nn.Identity()` with no parameters.
2. Clean baseline config stays disabled, so original checkpoint loading with `strict=True` remains unchanged.
3. When `MODEL.RGSSB.ENABLE=True`, load original OSTrack checkpoint with `strict=False` and report missing keys for RG-SSB only.
4. Initialize new RG-SSB weights randomly, with residual scale initialized to zero or near-zero for stability.
5. Do not overwrite the original checkpoint.

Potential future code behavior:

- If enabled:
  - call `load_state_dict(..., strict=False)`
  - assert unexpected keys are empty or understood
  - assert missing keys are limited to `rgssb.*`
- If disabled:
  - keep `strict=True` to protect baseline reproducibility.

## 9. Training Loss Integration Points

Existing training flow:

- File: `external/OSTrack/lib/train/train_script.py`
  - Builds model with `build_ostrack(cfg)`.
  - Creates objectives: `giou_loss`, `l1_loss`, `FocalLoss`, and `BCEWithLogitsLoss`.
  - Creates `OSTrackActor`.

- File: `external/OSTrack/lib/train/actors/ostrack.py`
  - `forward_pass()` extracts template/search tensors and calls `self.net(...)`.
  - `compute_losses()` computes:
    - GIoU loss from `pred_dict['pred_boxes']`.
    - L1 loss from `pred_dict['pred_boxes']`.
    - Focal/location loss from `pred_dict['score_map']`.

Later feature/response losses:

- Feature consistency loss could be added in `OSTrackActor.compute_losses()` if the model returns extra keys such as:
  - `pred_dict['rgssb_feat_clean']`
  - `pred_dict['rgssb_feat_degraded']`
  - or paired `backbone_feat` from clean/degraded forwards.
- Response consistency loss could also be added in `compute_losses()` using:
  - `pred_dict['score_map']`
  - clean/degraded response maps from paired forward passes.
- Training data pair degradation would likely enter around:
  - `lib/train/data/processing.py` after crop creation and before/around transforms, or
  - a new wrapper around the sampled template/search tensors before `OSTrackActor.forward_pass()`.

Do not implement these losses in the first insertion step.

## 10. Minimal Implementation Plan

Stage 1: Standalone module

- Add RG-SSB as a standalone module outside `external/OSTrack` or in a clearly isolated future module.
- Unit test identity/shape preservation on `[B, 256, 768]` and `[B, 768, 16, 16]` if both interfaces are supported.

Stage 2: Config-gated integration, disabled by default

- Add config defaults only after unit tests pass.
- Default `MODEL.RGSSB.ENABLE=False`.
- Disabled path must instantiate no new checkpoint parameters or must keep load behavior equivalent.

Stage 3: Enable RG-SSB and run one forward pass

- Use synthetic random tensors matching template/search sizes.
- Verify output keys and shapes.

Stage 4: Load original checkpoint with new module

- With RG-SSB disabled: strict load must pass unchanged.
- With RG-SSB enabled: load with `strict=False` and verify missing keys are only RG-SSB.

Stage 5: Run clean Car1 inference

- Confirm clean baseline does not break.
- Compare metrics against current clean row before making any claims.

Stage 6: Run degraded Car1 inference

- Start with one already established degraded root, such as `low_resolution medium seed42`.
- Compare against baseline row.

Stage 7: Later training and losses

- Only after inference integration is stable, add training data degradation, feature consistency, and response consistency.

## 11. Files Likely Needing Modification Later

Model code:

- `external/OSTrack/lib/models/ostrack/ostrack.py`
- Possible new file: `external/OSTrack/lib/models/ostrack/rgssb.py`
- Possible later file: `external/OSTrack/lib/models/ostrack/vit_ce.py`

Config files:

- `external/OSTrack/lib/config/ostrack/config.py`
- New experiment YAML copied from `external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300.yaml`

Test/inference code:

- `external/OSTrack/lib/test/tracker/ostrack.py` only if checkpoint loading must switch to conditional `strict=False`.
- Existing project scripts should remain usable:
  - `scripts/run_ostrack_otb_eval.py`
  - `scripts/run_baseline_degradation_suite.py`

Training/loss code:

- `external/OSTrack/lib/train/actors/ostrack.py`
- `external/OSTrack/lib/train/train_script.py`
- Possibly `external/OSTrack/lib/train/data/processing.py`
- Possibly `external/OSTrack/lib/train/base_functions.py` if optimizer parameter grouping needs RG-SSB-specific learning rate.

Scripts/tests:

- New tests for RG-SSB shape preservation.
- New one-forward smoke script or test.
- Later clean/degraded comparison script reusing existing baseline automation.

## 12. Files That Should Not Be Touched Initially

Avoid modifying these during the minimal proof-of-concept:

- `external/OSTrack/tracking/test.py`
- `external/OSTrack/lib/test/evaluation/*`
- `external/OSTrack/lib/train/dataset/*`
- `external/OSTrack/lib/train/trainers/*`
- `external/OSTrack/lib/models/layers/head.py` unless the pre-head insertion fails.
- Original YAML `external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300.yaml`; create a new RG-SSB YAML later instead.
- Original checkpoints under `external/OSTrack/output/checkpoints/`.
- Baseline result files in `outputs/ostrack_runs/` except when intentionally running new evaluations.

## 13. Risks and Safeguards

Shape mismatch risk:

- RG-SSB must preserve `[B, 256, 768]` if inserted pre-head.
- Use runtime hooks before integration and unit tests after standalone implementation.

Checkpoint loading risk:

- Current test path uses `strict=True`.
- Keep disabled baseline path unchanged.
- Use `strict=False` only for enabled RG-SSB and audit missing/unexpected keys.

Memory risk on GTX 1080:

- ViT-base plus Mamba/SSM branch may exceed 8 GB if inserted too often.
- Start with one search-only block at 16x16 tokens.
- Avoid multiple blocks and template+search processing until memory is measured.

Clean performance collapse:

- Initialize residual scale to 0.0 or very small.
- First verify clean Car1 inference before degraded claims.
- Keep baseline config and checkpoint untouched.

Too many modules too early:

- Do not add degradation token, response fusion, memory, or training losses in Stage 1.
- First prove shape-safe feature-level insertion.

Accidental modification of external baseline:

- Keep a separate RG-SSB config and checkpoint path later.
- Use `git status` before and after code edits.
- Do not edit `tracking/test.py` or dataset/evaluation wrappers.

## 14. Verification

Files created or modified:

- Created: `implementation/ostrack_rgssb_insertion_plan.md`

Commands run:

- Read-only inspection commands using `sed`, `nl`, and `rg` over:
  - `implementation/*.md`
  - `reports/08_method_architecture.md`
  - `experiments/baseline_results.csv`
  - `external/OSTrack/tracking/test.py`
  - `external/OSTrack/lib/test/tracker/ostrack.py`
  - `external/OSTrack/lib/test/evaluation/tracker.py`
  - `external/OSTrack/lib/test/parameter/ostrack.py`
  - `external/OSTrack/lib/models/ostrack/ostrack.py`
  - `external/OSTrack/lib/models/ostrack/base_backbone.py`
  - `external/OSTrack/lib/models/ostrack/vit_ce.py`
  - `external/OSTrack/lib/models/layers/head.py`
  - `external/OSTrack/lib/config/ostrack/config.py`
  - `external/OSTrack/lib/train/train_script.py`
  - `external/OSTrack/lib/train/actors/ostrack.py`
  - `external/OSTrack/lib/train/base_functions.py`
  - `external/OSTrack/lib/train/data/processing.py`

Only inspection was performed:

- Yes. No `external/OSTrack` files were modified.
- No RG-SSB code was implemented.
- No config files were edited.
- No training was run.

Uncertain fields:

- Exact transient token lengths inside CE blocks need runtime hook verification.
- Exact memory overhead of an RG-SSB branch on GTX 1080 needs a forward-pass measurement after standalone implementation.
- The best enabled-checkpoint loading policy should be validated against actual missing/unexpected key lists.

Ready for standalone RG-SSB unit tests:

- Yes. The safest initial interface is search-token input `[B, 256, 768]` with output shape unchanged, optionally reshaped internally to `[B, 768, 16, 16]`.
