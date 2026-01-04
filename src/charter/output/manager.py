"""
Output manager for saving charts to files.

Handles:
- Async file saving
- Unique filename generation
- Multiple output formats (PNG, SVG, PDF, JPEG)
"""

import asyncio
import uuid
from datetime import datetime
from pathlib import Path
from typing import Literal

from matplotlib.figure import Figure

from charter.config.settings import get_settings


OutputFormat = Literal["png", "svg", "pdf", "jpeg"]


class OutputManager:
    """
    Manages chart output to files.
    
    Provides async file saving with unique timestamped filenames
    and support for multiple output formats.
    """

    def __init__(self) -> None:
        """Initialize the output manager."""
        self._settings = get_settings()

    @property
    def output_dir(self) -> Path:
        """Get the configured output directory."""
        return self._settings.output_dir

    def generate_filename(
        self,
        chart_type: str,
        output_format: OutputFormat,
        custom_name: str | None = None,
    ) -> str:
        """
        Generate a unique filename for a chart.
        
        Format: {chart_type}_{timestamp}_{random}.{format}
        Example: bar_20260104_143052_a1b2c3.png
        
        Args:
            chart_type: Type of chart (bar, pie, line, timeseries)
            output_format: File format extension
            custom_name: Optional custom name (replaces chart_type)
            
        Returns:
            Generated filename
        """
        settings = self._settings
        
        parts = []
        
        # Base name
        base = custom_name or chart_type
        parts.append(base)
        
        # Timestamp
        if settings.include_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            parts.append(timestamp)
        
        # Random suffix
        if settings.include_random_suffix:
            suffix = uuid.uuid4().hex[:6]
            parts.append(suffix)
        
        filename = "_".join(parts)
        return f"{filename}.{output_format}"

    async def save_chart(
        self,
        figure: Figure,
        chart_type: str,
        output_format: OutputFormat = "png",
        filename: str | None = None,
        dpi: int | None = None,
    ) -> Path:
        """
        Save a chart figure to file asynchronously.
        
        Args:
            figure: matplotlib Figure to save
            chart_type: Type of chart (for filename generation)
            output_format: Output file format
            filename: Optional custom filename (without extension)
            dpi: Optional DPI override (for raster formats)
            
        Returns:
            Path: Full path to the saved file
        """
        # Generate filename if not provided
        if filename:
            # Add extension if not present
            if not filename.endswith(f".{output_format}"):
                filename = f"{filename}.{output_format}"
        else:
            filename = self.generate_filename(chart_type, output_format)
        
        # Build full path
        output_path = self.output_dir / filename
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Get DPI from settings if not overridden
        save_dpi = dpi or self._settings.default_dpi
        
        # Save in thread pool to avoid blocking
        await asyncio.to_thread(
            self._save_figure_sync,
            figure,
            output_path,
            output_format,
            save_dpi,
        )
        
        return output_path

    def _save_figure_sync(
        self,
        figure: Figure,
        path: Path,
        output_format: OutputFormat,
        dpi: int,
    ) -> None:
        """
        Synchronous figure saving.
        
        Args:
            figure: matplotlib Figure to save
            path: Output file path
            output_format: File format
            dpi: Resolution for raster formats
        """
        save_kwargs = {
            "format": output_format,
            "bbox_inches": "tight",
            "facecolor": figure.get_facecolor(),
            "edgecolor": "none",
        }
        
        # Add DPI for raster formats
        if output_format in ("png", "jpeg"):
            save_kwargs["dpi"] = dpi
        
        figure.savefig(path, **save_kwargs)
        
        # Close figure to free memory
        import matplotlib.pyplot as plt
        plt.close(figure)


# Module-level singleton
_manager: OutputManager | None = None


def get_output_manager() -> OutputManager:
    """
    Get the global output manager instance.
    
    Returns:
        OutputManager: The singleton manager instance
    """
    global _manager
    if _manager is None:
        _manager = OutputManager()
    return _manager

