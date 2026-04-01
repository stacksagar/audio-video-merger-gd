# Audio Video Merger - Merge MP4 Files Sequentially

🎬 A powerful tool to merge videoplayback files sequentially in pairs with custom naming. Perfect for merging video lectures, recordings, and segmented MP4 files.

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

## Features

- ✅ **Batch merge** multiple MP4 files automatically
- ✅ **Sequential pairing** - merges (1+2), (3+4), (5+6)...
- ✅ **Custom naming** with class prefixes and numbering
- ✅ **No quality loss** - preserves original video quality
- ✅ **Progress tracking** with detailed progress bars
- ✅ **Cross-platform** - works on Windows, macOS, Linux
- ✅ **Dry run mode** - preview before merging

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

- **ffmpeg** (required for merging MP4 files)
  - macOS: `brew install ffmpeg`
  - Ubuntu: `sudo apt install ffmpeg`
  - Windows: [Download](https://ffmpeg.org/download.html)

## Use Cases

- 📚 **Educational content** - Merge lecture recordings
- 💼 **Meeting recordings** - Combine Zoom/Teams segments
- 🎥 **Video processing** - Join segmented video files
- 📹 **Security footage** - Merge camera recordings
- 🎮 **Game recordings** - Combine gameplay clips

## Installation

### Option 1: Clone and Run (Recommended)
```bash
git clone https://github.com/stacksagar/audio-video-merger-gd.git
cd audio-video-merger
```

### Option 2: Install as Python Package
```bash
pip install audio-video-merger
audio-video-merger --help
```

### Option 3: Install from Source
```bash
git clone https://github.com/stacksagar/audio-video-merger-gd.git
cd audio-video-merger
pip install -e .
```

Ensure ffmpeg is installed on your system.

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

1. 🔍 **Detects** all `videoplayback (#).mp4` files in input folder
2. 📊 **Sorts** files by numerical order
3. 🔗 **Merges** in pairs: (1+2), (3+4), (5+6)...
4. 💾 **Saves** with custom sequential numbering

## File Naming Convention

Input files must follow this pattern:
- `videoplayback (1).mp4`
- `videoplayback (2).mp4`
- `videoplayback (3).mp4`
- etc.

The script automatically sorts by the number in parentheses.

## Performance

- ⚡ Fast merging with ffmpeg (copy mode)
- 🎯 No re-encoding - preserves original quality
- 📊 Progress bars for large files
- 🔄 Batch processing - handles multiple pairs

## Languages

- 🐍 **Python 3.6+** - Full-featured version with advanced capabilities
  - Modular architecture with separate modules
  - Type hints and documentation
  - Enhanced error handling
  - Progress tracking with file sizes
  - Configurable settings
  - Package installation support
- 🟢 **Node.js** - Lightweight JavaScript version
- 📦 Minimal dependencies - Only requires ffmpeg

## Python Features

### Advanced Architecture
- **Modular Design**: Separate modules for utils, config, and merger
- **Type Hints**: Full type annotation support
- **Error Handling**: Comprehensive validation and error reporting
- **Progress Tracking**: Real-time progress with file sizes
- **Configuration**: Customizable settings via config module

### Python Module Structure
```
scripts/
├── __init__.py           # Package initialization
├── config.py            # Configuration settings
├── utils.py             # Utility functions
├── merger.py            # Core merger class
├── merge_sequential.py  # Original simple version
└── merge_sequential_v2.py # Enhanced version
```

## License

MIT License - feel free to use in your projects!

---

**Keywords**: video merger, MP4 joiner, video concatenation, batch video processing, ffmpeg, video editor, lecture merger, recording combiner
