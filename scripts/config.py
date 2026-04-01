#!/usr/bin/env python3
"""
Configuration settings for the audio video merger.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import List


@dataclass
class MergeConfig:
    """Configuration for video merging operations."""
    
    # Directory settings
    script_dir: Path = Path(__file__).parent
    input_dir: Path = script_dir.parent / "input"
    output_dir: Path = script_dir.parent / "output"
    
    # File patterns
    input_pattern: str = r"videoplayback\s*\((\d+)\)\.mp4"
    
    # Default settings
    default_start_number: int = 1
    default_class_name: str = ""
    
    # ffmpeg settings
    ffmpeg_video_codec: str = "copy"
    ffmpeg_audio_codec: str = "aac"
    ffmpeg_extra_args: List[str] = ["-shortest", "-y"]
    
    # Progress settings
    progress_bar_width: int = 50
    show_file_sizes: bool = True
    
    # Validation settings
    max_file_size_gb: int = 10  # Maximum file size in GB
    require_even_pairs: bool = False  # Whether to require even number of files
    
    @property
    def max_file_size_bytes(self) -> int:
        """Maximum file size in bytes."""
        return self.max_file_size_gb * 1024 * 1024 * 1024
    
    def get_ffmpeg_command(self, input1: str, input2: str, output: str) -> List[str]:
        """
        Build ffmpeg command for merging two files.
        
        Args:
            input1: First input file
            input2: Second input file
            output: Output file
            
        Returns:
            List of command arguments
        """
        cmd = [
            "ffmpeg",
            "-i", str(self.input_dir / input1),
            "-i", str(self.input_dir / input2),
            "-c:v", self.ffmpeg_video_codec,
            "-c:a", self.ffmpeg_audio_codec,
        ]
        cmd.extend(self.ffmpeg_extra_args)
        cmd.append(str(self.output_dir / output))
        return cmd


# Global configuration instance
config = MergeConfig()
