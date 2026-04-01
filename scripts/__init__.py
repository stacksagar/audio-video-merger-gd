"""
Audio Video Merger - Python Package

A powerful tool to merge videoplayback files sequentially in pairs.
"""

__version__ = "2.0.0"
__author__ = "Audio Video Merger Team"
__description__ = "Merge videoplayback files sequentially with custom naming"

from .merger import VideoMerger
from .utils import find_video_files, validate_files, format_size
from .config import config, MergeConfig

__all__ = [
    "VideoMerger",
    "find_video_files",
    "validate_files", 
    "format_size",
    "config",
    "MergeConfig"
]
