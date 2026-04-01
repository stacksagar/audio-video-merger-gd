#!/usr/bin/env python3
"""
Core video merger functionality.
"""

import subprocess
import os
from pathlib import Path
from typing import Tuple, Optional
from tqdm import tqdm

from config import config
from utils import format_size, get_file_size


class VideoMerger:
    """Handles video merging operations."""
    
    def __init__(self):
        """Initialize the merger with default configuration."""
        self.config = config
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure input and output directories exist."""
        self.config.input_dir.mkdir(exist_ok=True)
        self.config.output_dir.mkdir(exist_ok=True)
    
    def merge_videos(self, file1: str, file2: str, output: str) -> Tuple[bool, Optional[str]]:
        """
        Merge two video files using ffmpeg.
        
        Args:
            file1: First input filename
            file2: Second input filename
            output: Output filename
            
        Returns:
            Tuple of (success, error_message)
        """
        # Build ffmpeg command
        cmd = self.config.get_ffmpeg_command(file1, file2, output)
        
        try:
            # Run ffmpeg with progress tracking
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Parse ffmpeg output for progress
            total_duration = None
            with tqdm(
                total=100,
                unit='%',
                desc=f"Merging {output}",
                bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'
            ) as pbar:
                
                for line in process.stdout:
                    # Parse duration from ffmpeg output
                    if "Duration:" in line and total_duration is None:
                        try:
                            time_str = line.split("Duration:")[1].split(",")[0].strip()
                            h, m, s = time_str.split(":")
                            total_duration = int(h) * 3600 + int(m) * 60 + float(s)
                        except:
                            pass
                    
                    # Parse progress
                    if "time=" in line and total_duration:
                        try:
                            time_str = line.split("time=")[1].split(" ")[0].strip()
                            h, m, s = time_str.split(":")
                            current_time = int(h) * 3600 + int(m) * 60 + float(s)
                            progress = min(100, int((current_time / total_duration) * 100))
                            pbar.update(progress - pbar.n)
                        except:
                            pass
            
            # Check if process succeeded
            if process.returncode == 0:
                # Show output file size
                output_path = self.config.output_dir / output
                if output_path.exists():
                    size = format_size(get_file_size(output_path))
                    print(f"  ✅ Created {output} ({size})")
                return True, None
            else:
                return False, f"ffmpeg exited with code {process.returncode}"
                
        except FileNotFoundError:
            return False, "ffmpeg not found. Please install ffmpeg."
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def validate_input_file(self, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a single input file.
        
        Args:
            filename: Name of the file to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        file_path = self.config.input_dir / filename
        
        if not file_path.exists():
            return False, f"File not found: {filename}"
        
        if not file_path.is_file():
            return False, f"Path is not a file: {filename}"
        
        if not os.access(file_path, os.R_OK):
            return False, f"File not readable: {filename}"
        
        # Check file size
        size = get_file_size(file_path)
        if size > self.config.max_file_size_bytes:
            return False, f"File too large: {filename} ({format_size(size)} > {self.config.max_file_size_gb}GB)"
        
        # Check file extension
        if not filename.lower().endswith('.mp4'):
            return False, f"File must be MP4: {filename}"
        
        return True, None
    
    def get_merge_plan(self, files: list, class_name: str = "", start_number: int = 1, include_duration: bool = True) -> list:
        """
        Create a plan for merging files.
        
        Args:
            files: List of input filenames
            class_name: Optional class prefix
            start_number: Starting number for output
            include_duration: Whether to include duration in filename
            
        Returns:
            List of merge operations
        """
        from utils import create_output_filename, get_video_duration
        
        plan = []
        for i in range(0, len(files), 2):
            if i + 1 < len(files):
                file1 = files[i]
                file2 = files[i + 1]
                output_num = start_number + (i // 2)
                
                # Get duration if requested
                duration = None
                if include_duration:
                    # Try to get duration from first file
                    file1_path = self.config.input_dir / file1
                    duration = get_video_duration(file1_path)
                
                output = create_output_filename(class_name, output_num, duration)
                
                plan.append({
                    'input1': file1,
                    'input2': file2,
                    'output': output,
                    'index': output_num,
                    'duration': duration
                })
        
        return plan
    
    def estimate_output_size(self, files: list) -> int:
        """
        Estimate total output size.
        
        Args:
            files: List of input files
            
        Returns:
            Estimated size in bytes
        """
        total_size = 0
        for file in files:
            file_path = self.config.input_dir / file
            if file_path.exists():
                total_size += get_file_size(file_path)
        return total_size
