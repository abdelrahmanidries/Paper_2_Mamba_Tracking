# Sample Images

Use this folder for local real-image checks of the synthetic degradation pipeline.

## Raw images

Put standalone real images here:

```text
samples/raw_images/
```

Supported extensions:

- `.jpg`
- `.jpeg`
- `.png`
- `.bmp`

Run:

```powershell
.\.venv\Scripts\python.exe scripts\test_degradation_on_samples.py --input_dir samples\raw_images --output_dir outputs\real_sample_degradation
```

## Template-search pairs

Put real tracking-pair images here:

```text
samples/tracking_pairs/
```

Suggested naming:

```text
pair_001_template.jpg
pair_001_search.jpg
```

Run:

```powershell
.\.venv\Scripts\python.exe scripts\test_degradation_on_tracking_pair.py --template samples\tracking_pairs\pair_001_template.jpg --search samples\tracking_pairs\pair_001_search.jpg --output_dir outputs\tracking_pair_degradation
```

## Dataset samples

Do not commit sample images if they come from datasets with licensing restrictions. Keep dataset-derived samples local unless the dataset license explicitly permits redistribution.

## Outputs

Generated degraded samples are written under:

```text
outputs/
```

The degradation transforms preserve final image size, so tracking bounding boxes remain unchanged. Side-by-side comparison images may resize copies for visualization only; saved degraded template/search images keep the original dimensions.
