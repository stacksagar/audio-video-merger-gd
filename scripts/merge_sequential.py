#!/usr/bin/env python3
"""
Merge video files sequentially in pairs.
Place your videoplayback files in the ../input directory.
Merged files will be saved to the ../output directory.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
import re

def find_video_files(input_dir):
    """Find all videoplayback files and sort them by number."""
    pattern = re.compile(r'videoplayback\s*\((\d+)\)\.mp4', re.IGNORECASE)
    
    files = []
    for file in os.listdir(input_dir):
        match = pattern.match(file)
        if match:
            num = int(match.group(1))
            files.append((num, file))
    
    # Sort by the number in parentheses
    files.sort(key=lambda x: x[0])
    return [f[1] for f in files]

def merge_videos(file1, file2, output, input_dir, output_dir):
    """Merge two video files using ffmpeg."""
    cmd = [
        'ffmpeg',
        '-i', os.path.join(input_dir, file1),
        '-i', os.path.join(input_dir, file2),
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-shortest',
        '-y',  # overwrite output file
        os.path.join(output_dir, output)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error merging {file1} + {file2}: {e}")
        if e.stderr:
            print(f"ffmpeg stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg.")
        return False

def main():
    parser = argparse.ArgumentParser(description="Merge videoplayback files in sequential pairs.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be merged without actually merging")
    parser.add_argument("--class", dest="class_name", default="", help="Class name prefix for output files (e.g., 'classA')")
    parser.add_argument("--start", type=int, default=1, help="Starting number for output files (default: 1)")
    
    args = parser.parse_args()
    
    # Set up directories
    script_dir = Path(__file__).parent
    input_dir = script_dir.parent / "input"
    output_dir = script_dir.parent / "output"
    
    # Create directories if they don't exist
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    # Find all video files
    video_files = find_video_files(input_dir)
    
    if not video_files:
        print(f"No videoplayback files found in {input_dir}!")
        print("Please place your videoplayack files in the input directory.")
        print("Files should be named like: 'videoplayback (1).mp4'")
        sys.exit(1)
    
    print(f"Found {len(video_files)} videoplayback files in {input_dir}:")
    for i, file in enumerate(video_files, 1):
        print(f"  {i}. {file}")
    
    # Process in pairs
    pairs = []
    for i in range(0, len(video_files), 2):
        if i + 1 < len(video_files):
            file1 = video_files[i]
            file2 = video_files[i + 1]
            
            # Create output filename with class prefix and sequential numbering
            output_num = args.start + (i // 2)
            prefix = f"{args.class_name}_" if args.class_name else ""
            output = f"{prefix}{output_num}.mp4"
            
            pairs.append((file1, file2, output))
        else:
            print(f"\nWarning: {video_files[i]} has no pair (odd number of files)")
    
    if not pairs:
        print("\nNo pairs to merge!")
        sys.exit(1)
    
    print(f"\nWill create {len(pairs)} merged files in {output_dir}:")
    for file1, file2, output in pairs:
        print(f"  {file1} + {file2} → {output}")
    
    if args.dry_run:
        print("\nDry run complete. Use without --dry-run to actually merge.")
        return
    
    # Confirm
    response = input("\nProceed with merging? (y/N): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    # Merge each pair
    success_count = 0
    for i, (file1, file2, output) in enumerate(pairs, 1):
        print(f"\n[{i}/{len(pairs)}] Merging {file1} + {file2}...")
        
        if merge_videos(file1, file2, output, input_dir, output_dir):
            print(f"  ✅ Created {output}")
            success_count += 1
        else:
            print(f"  ❌ Failed to merge {file1} + {file2}")
    
    print(f"\nDone! Successfully merged {success_count}/{len(pairs)} pairs.")
    print(f"Output files are in: {output_dir}")

if __name__ == "__main__":
    main()
