# wp-originals-only

Copy only original images from a WordPress uploads folder, skipping all resized/scaled variants that WordPress auto-generates.

## Problem

When WordPress uploads an image it generates multiple variants alongside the original:

```
photo.jpg              ← original
photo-300x200.jpg      ← thumbnail
photo-768x512.jpg      ← medium
photo-1024x683.jpg     ← large
photo-scaled.jpg       ← scaled (for very large originals)
photo-rotated.jpg      ← auto-rotated copy
```

This script keeps only the originals.

## Usage

```bash
python copy_originals.py <src> <dst> [--dry-run]
```

| Argument    | Description                                      |
|-------------|--------------------------------------------------|
| `src`       | Source folder (your downloaded `wp-content/uploads`) |
| `dst`       | Destination folder where originals will be copied |
| `--dry-run` | Preview what would be copied without writing anything |

### Examples

```bash
# Preview first
python copy_originals.py C:\Downloads\uploads C:\Output\originals --dry-run

# Copy originals
python copy_originals.py C:\Downloads\uploads C:\Output\originals
```

The destination folder structure (year/month subfolders) is preserved.

## Requirements

Python 3.6+ — no external dependencies.
