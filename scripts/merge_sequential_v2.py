#!/usr/bin/env python3
"""
Merge video files sequentially in pairs.
Place your videoplayback files in the ../input directory.
Merged files will be saved to the ../output directory.

Enhanced version with modular architecture and advanced features.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Tuple

# Import our custom modules
from utils import find_video_files, validate_files, format_size, check_ffmpeg
from config import config
from merger import VideoMerger


class SequentialMerger:
    """High-level interface for sequential video merging."""
    
    def __init__(self):
        """Initialize the merger."""
        self.merger = VideoMerger()
        self.config = config
    
    def run(self, args):
        """
        Run the merging process with given arguments.
        
        Args:
            args: Parsed command line arguments
        """
        # Check dependencies
        if not check_ffmpeg():
            print("❌ Error: ffmpeg not found!")
            print("Please install ffmpeg:")
            print("  macOS: brew install ffmpeg")
            print("  Ubuntu: sudo apt install ffmpeg")
            print("  Windows: Download from https://ffmpeg.org/download.html")
            sys.exit(1)
        
        # Find and validate files
        video_files = self._find_and_validate_files()
        
        # Create merge plan
        merge_plan = self.merger.get_merge_plan(
            video_files, 
            args.class_name, 
            args.start
        )
        
        # Show summary
        self._show_summary(video_files, merge_plan, args)
        
        # Dry run mode
        if args.dry_run:
            print("\n🔍 Dry run complete. Use without --dry-run to actually merge.")
            return
        
        # Confirm and merge
        if self._get_confirmation():
            self._execute_merge(merge_plan)
    
    def _find_and_validate_files(self) -> List[str]:
        """Find and validate all video files."""
        # Find files
        video_files = find_video_files(self.config.input_dir)
        
        if not video_files:
            print(f"❌ No videoplayback files found in {self.config.input_dir}!")
            print("\nPlease place your videoplayback files in the input directory.")
            print("Files should be named like: 'videoplayback (1).mp4'")
            sys.exit(1)
        
        # Validate files
        is_valid, error = validate_files(video_files, self.config.input_dir)
        if not is_valid:
            print(f"❌ Error: {error}")
            sys.exit(1)
        
        return video_files
    
    def _show_summary(self, video_files: List[str], merge_plan: List[dict], args):
        """Show a summary of what will be merged."""
        print(f"\n📁 Found {len(video_files)} videoplayback files:")
        
        # Show file sizes if enabled
        if self.config.show_file_sizes:
            total_size = 0
            for i, file in enumerate(video_files, 1):
                file_path = self.config.input_dir / file
                size = format_size(file_path.stat().st_size)
                total_size += file_path.stat().st_size
                print(f"  {i:2d}. {file} ({size})")
            
            print(f"\n📊 Total input size: {format_size(total_size)}")
        else:
            for i, file in enumerate(video_files, 1):
                print(f"  {i:2d}. {file}")
        
        # Show merge plan
        print(f"\n🔗 Will create {len(merge_plan)} merged files:")
        for operation in merge_plan:
            input1 = operation['input1']
            input2 = operation['input2']
            output = operation['output']
            print(f"  {input1} + {input2} → {output}")
        
        # Show output directory
        print(f"\n📂 Output directory: {self.config.output_dir}")
    
    def _get_confirmation(self) -> bool:
        """Get user confirmation to proceed."""
        try:
            response = input("\nProceed with merging? (y/N): ").strip().lower()
            return response == 'y'
        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user.")
            sys.exit(0)
    
    def _execute_merge(self, merge_plan: List[dict]):
        """Execute the merge operations."""
        print("\n🚀 Starting merge process...")
        
        success_count = 0
        failed_operations = []
        
        for i, operation in enumerate(merge_plan, 1):
            print(f"\n[{i}/{len(merge_plan)}] Merging...")
            
            success, error = self.merger.merge_videos(
                operation['input1'],
                operation['input2'],
                operation['output']
            )
            
            if success:
                success_count += 1
            else:
                failed_operations.append((operation, error))
                print(f"  ❌ Failed: {error}")
        
        # Show final results
        print(f"\n{'='*50}")
        print(f"✅ Successfully merged: {success_count}/{len(merge_plan)} files")
        
        if failed_operations:
            print(f"\n❌ Failed operations:")
            for operation, error in failed_operations:
                print(f"  - {operation['input1']} + {operation['input2']}: {error}")
        
        print(f"\n📁 Output files are in: {self.config.output_dir}")
        
        # Show output directory size
        if self.config.output_dir.exists():
            output_size = sum(
                f.stat().st_size 
                for f in self.config.output_dir.iterdir() 
                if f.is_file()
            )
            print(f"📊 Total output size: {format_size(output_size)}")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Merge videoplayback files in sequential pairs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Default: 1.mp4, 2.mp4...
  %(prog)s --class math101                   # math101_1.mp4, math101_2.mp4...
  %(prog)s --start 10                        # 10.mp4, 11.mp4, 12.mp4...
  %(prog)s --class physics --start 5         # physics_5.mp4, physics_6.mp4...
  %(prog)s --dry-run                         # Preview without merging
        """
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be merged without actually merging"
    )
    
    parser.add_argument(
        "--class",
        dest="class_name",
        default="",
        help="Class name prefix for output files (e.g., 'classA')"
    )
    
    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="Starting number for output files (default: 1)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 2.0.0"
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Create and run merger
    merger = SequentialMerger()
    merger.run(args)


if __name__ == "__main__":
    main()
