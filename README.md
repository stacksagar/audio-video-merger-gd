# Audio Video Merger

Merge videoplayback files sequentially in pairs with custom naming.

## Quick Start

1. **Place files** in `input/` folder:
   ```
   input/
   ├── videoplayback (1).mp4
   ├── videoplayback (2).mp4
   ├── videoplayback (3).mp4
   └── videoplayback (4).mp4
   ```

2. **Run merger**:

   **Python:**
   ```bash
   cd scripts
   python merge_sequential.py
   ```

   **Node.js:**
   ```bash
   cd scripts
   node merge_sequential.js
   ```

3. **Find results** in `output/`:
   ```
   output/
   ├── 1.mp4      # from (1)+(2)
   └── 2.mp4      # from (3)+(4)
   ```

## Options

| Option | Description | Example |
|--------|-------------|---------|
| `--class <name>` | Add prefix to files | `--class math101` → `math101_1.mp4` |
| `--start <num>` | Starting number | `--start 5` → `5.mp4, 6.mp4...` |
| `--dry-run` | Preview without merging | `--dry-run` |

## Examples

```bash
# Default: 1.mp4, 2.mp4, 3.mp4...
python merge_sequential.py

# With class: classA_1.mp4, classA_2.mp4...
node merge_sequential.js --class classA

# Custom start: 10.mp4, 11.mp4, 12.mp4...
python merge_sequential.py --start 10

# Combined: physics_5.mp4, physics_6.mp4...
node merge_sequential.js --class physics --start 5
```

## Requirements

- **ffmpeg** (required for merging)
  - macOS: `brew install ffmpeg`
  - Ubuntu: `sudo apt install ffmpeg`
  - Windows: [Download](https://ffmpeg.org/download.html)

## Directory Structure

```
audio-video-merger/
├── input/      # ← Place your videoplayback files here
├── output/     # ← Merged files appear here
└── scripts/    # ← Merger scripts
    ├── merge_sequential.py
    └── merge_sequential.js
```

## How It Works

1. Finds all `videoplayback (#).mp4` files
2. Sorts by number
3. Merges in pairs: (1+2), (3+4), (5+6)...
4. Saves with sequential numbering

## Features

- ✅ Clean directory structure
- ✅ Custom naming with class prefixes
- ✅ Progress indicators
- ✅ Dry-run mode
- ✅ Both Python and Node.js versions
- ✅ Preserves video quality
