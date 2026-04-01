#!/usr/bin/env python3
"""
Utility functions for the audio video merger.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Optional


def find_video_files(input_dir: Path) -> List[str]:
    """
    Find all videoplayback files and sort them by number.
    
    Args:
        input_dir: Path to the input directory
        
    Returns:
        List of sorted filenames
    """
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


def validate_files(files: List[str], input_dir: Path) -> Tuple[bool, Optional[str]]:
    """
    Validate that files exist and are readable.
    
    Args:
        files: List of filenames to validate
        input_dir: Directory containing the files
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    for file in files:
        file_path = input_dir / file
        if not file_path.exists():
            return False, f"File not found: {file}"
        if not file_path.is_file():
            return False, f"Path is not a file: {file}"
        if os.access(file_path, os.R_OK):
            return False, f"File not readable: {file}"
    
    return True, None


def get_file_size(file_path: Path) -> int:
    """
    Get file size in bytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in bytes
    """
    return file_path.stat().st_size


def format_size(size_bytes: int) -> str:
    """
    Format file size in human readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def create_output_filename(class_name: str, index: int) -> str:
    """
    Create output filename with class prefix.
    
    Args:
        class_name: Class name prefix
        index: Sequential index
        
    Returns:
        Output filename
    """
    prefix = f"{class_name}_" if class_name else ""
    return f"{prefix}{index}.mp4"


def estimate_output_size(input_files: List[str], input_dir: Path) -> int:
    """
    Estimate total output size based on input files.
    
    Args:
        input_files: List of input filenames
        input_dir: Directory containing the files
        
    Returns:
        Estimated output size in bytes
    """
    total_size = 0
    for file in input_files:
        file_path = input_dir / file
        if file_path.exists():
            total_size += get_file_size(file_path)
    return total_size


def check_ffmpeg() -> bool:
    """
    Check if ffmpeg is installed and accessible.
    
    Returns:
        True if ffmpeg is available
    """
    import subprocess
    import shutil
    
    if not shutil.which("ffmpeg"):
        return False
    
    try:
        subprocess.run(["ffmpeg", "-version"], 
                      capture_output=True, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
