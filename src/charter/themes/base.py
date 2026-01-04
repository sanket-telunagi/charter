"""
Base theme definitions for Charter.

Themes control the visual appearance of charts including colors,
fonts, backgrounds, and other visual elements.
"""

from dataclasses import dataclass, field
from typing import Sequence


@dataclass(frozen=True)
class Theme:
    """
    Theme configuration for chart rendering.
    
    Attributes:
        name: Unique theme identifier
        background_color: Chart background color
        text_color: Primary text color
        title_color: Chart title color
        grid_color: Grid line color
        axis_color: Axis line color
        palette: Sequence of colors for data series
        font_family: Primary font family
        title_font_size: Font size for titles
        label_font_size: Font size for axis labels
        tick_font_size: Font size for tick labels
        legend_font_size: Font size for legend text
        line_width: Default line width
        grid_alpha: Grid transparency (0-1)
        grid_style: Grid line style ('solid', 'dashed', 'dotted')
        spine_visible: Whether to show axis spines
        figsize: Default figure size (width, height)
        dpi: Default DPI for rendering
    """

    name: str
    background_color: str = "#FFFFFF"
    text_color: str = "#333333"
    title_color: str = "#1a1a1a"
    grid_color: str = "#E0E0E0"
    axis_color: str = "#666666"
    palette: Sequence[str] = field(
        default_factory=lambda: [
            "#4C72B0",  # Blue
            "#55A868",  # Green
            "#C44E52",  # Red
            "#8172B3",  # Purple
            "#CCB974",  # Yellow
            "#64B5CD",  # Cyan
            "#E377C2",  # Pink
            "#7F7F7F",  # Gray
        ]
    )
    font_family: str = "sans-serif"
    title_font_size: int = 14
    label_font_size: int = 12
    tick_font_size: int = 10
    legend_font_size: int = 10
    line_width: float = 2.0
    grid_alpha: float = 0.7
    grid_style: str = "dashed"
    spine_visible: bool = True
    figsize: tuple[float, float] = (10.0, 6.0)
    dpi: int = 150

    def get_color(self, index: int) -> str:
        """Get a color from the palette by index (wraps around)."""
        return self.palette[index % len(self.palette)]

    def apply_to_axes(self, ax) -> None:
        """
        Apply theme settings to a matplotlib Axes object.
        
        Args:
            ax: matplotlib Axes object to style
        """
        # Background
        ax.set_facecolor(self.background_color)
        
        # Grid
        ax.grid(True, alpha=self.grid_alpha, color=self.grid_color, linestyle=self.grid_style)
        
        # Spines
        for spine in ax.spines.values():
            spine.set_visible(self.spine_visible)
            spine.set_color(self.axis_color)
        
        # Tick colors
        ax.tick_params(colors=self.text_color, labelsize=self.tick_font_size)
        
        # Label colors
        ax.xaxis.label.set_color(self.text_color)
        ax.yaxis.label.set_color(self.text_color)
        ax.xaxis.label.set_fontsize(self.label_font_size)
        ax.yaxis.label.set_fontsize(self.label_font_size)

    def apply_to_figure(self, fig) -> None:
        """
        Apply theme settings to a matplotlib Figure object.
        
        Args:
            fig: matplotlib Figure object to style
        """
        fig.set_facecolor(self.background_color)

