"""
Nightingale Rose chart implementation.

Supports:
- Radius-based (Nightingale) rose charts
- Area-based rose charts
"""

from typing import Any
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from charter.charts.base import BaseChart
from charter.styles.presets import RoseStyle
from charter.themes.base import Theme


class RoseChart(BaseChart):
    """
    Nightingale Rose chart renderer.
    
    Expected data format:
        {
            "labels": ["Category A", "Category B", "Category C"],
            "values": [30, 45, 25]
        }
    """

    def __init__(
        self,
        data: dict[str, Any],
        style: RoseStyle,
        theme: Theme,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
    ) -> None:
        super().__init__(data, style, theme, title, xlabel, ylabel)
        self.style: RoseStyle = style  # Type narrowing

    def _create_figure(self) -> tuple[Figure, plt.Axes]:
        """Create a new figure and polar axes with theme applied."""
        # Get figsize from settings or theme
        figsize = self._settings.default_figsize or self.theme.figsize
        dpi = self._settings.default_dpi or self.theme.dpi

        # Create polar plot
        fig, ax = plt.subplots(
            figsize=figsize, 
            dpi=dpi, 
            subplot_kw={'projection': 'polar'}
        )
        
        # Apply theme to figure
        self.theme.apply_to_figure(fig)
        
        # Apply specialized theme to polar axes
        ax.set_facecolor(self.theme.background_color)
        ax.grid(True, color=self.theme.grid_color, alpha=self.theme.grid_alpha, linestyle=self.theme.grid_style)
        
        # Remove spines for cleaner look
        ax.spines['polar'].set_visible(False)
        
        return fig, ax

    def _render_sync(self) -> Figure:
        """Render the rose chart synchronously."""
        fig, ax = self._create_figure()
        
        labels = self.data.get("labels", [])
        values = self.data.get("values", [])
        
        if not labels or not values:
            return self._finalize_figure(fig)
            
        n_points = len(values)
        
        # Calculate angles
        # In a rose chart, each sector has the same angle width
        theta = np.linspace(0.0, 2 * np.pi, n_points, endpoint=False)
        
        # Adjust start angle and direction
        # Convert degrees to radians
        start_angle_rad = np.deg2rad(self.style.start_angle)
        
        if self.style.counter_clockwise:
            theta += start_angle_rad
        else:
            # For clockwise, we negate angles and add start angle
            theta = start_angle_rad - theta
            
        width = (2 * np.pi) / n_points
        
        # Generate colors from theme
        colors = [self.theme.get_color(i) for i in range(n_points)]
        
        # Determine radii based on rose type
        if self.style.rose_type == "area":
            # Area is proportional to value: Area = 0.5 * r^2 * theta
            # Since theta is constant, r^2 ~ value -> r ~ sqrt(value)
            radii = np.sqrt(values)
        else:
            # Radius is proportional to value (standard Nightingale)
            radii = values
            
        # Draw the bars (petals)
        bars = ax.bar(
            theta, 
            radii, 
            width=width, 
            bottom=0.0,
            color=colors, 
            alpha=self.style.alpha,
            align='edge'  # Align edge to start of angle
        )
        
        # Add labels
        if self.style.show_labels:
            # Calculate label positions
            for i, (angle, radius, label, value) in enumerate(zip(theta, radii, labels, values)):
                # Angle for label is center of the wedge
                label_angle = angle + width / 2
                
                # Distance for label
                label_distance = np.max(radii) * self.style.label_distance
                
                # Format label
                label_text = label
                if self.style.show_percentages:
                    pct = (value / sum(values)) * 100
                    label_text += f"\n{pct:.1f}%"
                
                # Rotation logic to keep text readable
                rotation = np.rad2deg(label_angle)
                if self.style.counter_clockwise:
                    if 90 < rotation < 270:
                        rotation += 180
                else:
                    # Adjust for clockwise rotation
                    rotation = np.rad2deg(label_angle)
                    # Normalize to 0-360
                    rotation = rotation % 360
                    # Standard logic for readability
                    if 90 < rotation < 270:
                        rotation += 180
                
                ax.text(
                    label_angle, 
                    label_distance, 
                    label_text, 
                    ha='center', 
                    va='center',
                    rotation=rotation,
                    fontsize=self.theme.label_font_size,
                    color=self.theme.text_color,
                    fontfamily=self.theme.font_family
                )
        
        # Remove y-axis labels (radial values) usually for rose charts unless specified
        # But we might want them grid lines.
        ax.set_yticklabels([])
        
        # Remove x-axis labels (angular) as we added custom labels
        ax.set_xticklabels([])

        # Apply title
        if self.title:
            # Use fig.suptitle or ax.set_title with padding
            # Polar plots title positioning can be tricky
            ax.set_title(
                self.title,
                fontsize=self.theme.title_font_size,
                color=self.theme.title_color,
                fontfamily=self.theme.font_family,
                pad=30,
                y=1.1
            )
            
        return self._finalize_figure(fig)
