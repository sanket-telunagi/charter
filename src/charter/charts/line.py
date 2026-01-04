"""
Line chart implementation with support for various styles.

Supports:
- Standard line plots
- Smooth (spline) interpolation
- Stepped lines
- Area fills
- Multiple series
"""

from typing import Any

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from scipy import interpolate

from charter.charts.base import BaseChart
from charter.styles.presets import LineStyle
from charter.themes.base import Theme


class LineChart(BaseChart):
    """
    Line chart renderer with multiple style options.
    
    Expected data format:
        Single series:
        {
            "x": [1, 2, 3, 4, 5],
            "y": [10, 15, 13, 17, 20]
        }
        
        Multiple series:
        {
            "x": [1, 2, 3, 4, 5],
            "series": {
                "Series 1": [10, 15, 13, 17, 20],
                "Series 2": [8, 12, 16, 14, 18]
            }
        }
        
        With labels instead of x values:
        {
            "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"],
            "y": [10, 15, 13, 17, 20]
        }
    """

    def __init__(
        self,
        data: dict[str, Any],
        style: LineStyle,
        theme: Theme,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
    ) -> None:
        super().__init__(data, style, theme, title, xlabel, ylabel)
        self.style: LineStyle = style  # Type narrowing

    def _render_sync(self) -> Figure:
        """Render the line chart synchronously."""
        fig, ax = self._create_figure()
        
        self._render_to_axes_impl(ax)
        self._apply_labels(ax)
        self._apply_legend(ax)
        
        return self._finalize_figure(fig)
    
    def _render_to_axes_impl(self, ax: plt.Axes) -> None:
        """Render line chart content to an existing axes."""
        # Get x values or generate from labels
        if "labels" in self.data:
            labels = self.data["labels"]
            x = np.arange(len(labels))
            ax.set_xticks(x)
            ax.set_xticklabels(labels)
        else:
            x = np.array(self.data.get("x", []))
        
        # Check if we have multiple series or single series
        if "series" in self.data:
            self._render_multi_series(ax, x)
        else:
            y = np.array(self.data.get("y", []))
            self._render_single_series(ax, x, y, color=self.theme.get_color(0))

    def _render_single_series(
        self,
        ax: plt.Axes,
        x: np.ndarray,
        y: np.ndarray,
        color: str,
        label: str | None = None,
    ) -> None:
        """Render a single line series."""
        # Apply interpolation if needed
        if self.style.smooth and len(x) > 3:
            x_plot, y_plot = self._smooth_data(x, y)
        else:
            x_plot, y_plot = x, y
        
        # Build line kwargs
        line_kwargs = {
            "color": color,
            "linewidth": self.theme.line_width,
            "linestyle": self._get_linestyle(),
            "alpha": 1.0,
        }
        
        if label:
            line_kwargs["label"] = label
        
        # Plot based on style
        if self.style.stepped:
            ax.step(x_plot, y_plot, where="mid", **line_kwargs)
        else:
            ax.plot(x_plot, y_plot, **line_kwargs)
        
        # Add markers if needed
        if self.style.show_points or self.style.marker:
            marker = self.style.marker or "o"
            ax.scatter(
                x, y,
                color=color,
                s=self.style.marker_size ** 2,
                marker=marker,
                zorder=5,
            )
        
        # Fill area if needed
        if self.style.fill_area:
            ax.fill_between(
                x_plot, y_plot, 0,
                color=color,
                alpha=self.style.fill_alpha,
            )

    def _render_multi_series(
        self,
        ax: plt.Axes,
        x: np.ndarray,
    ) -> None:
        """Render multiple line series."""
        series_data = self.data.get("series", {})
        
        for i, (name, y_values) in enumerate(series_data.items()):
            y = np.array(y_values)
            color = self.theme.get_color(i)
            self._render_single_series(ax, x, y, color=color, label=name)

    def _smooth_data(
        self,
        x: np.ndarray,
        y: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Apply spline smoothing to data."""
        try:
            # Create cubic spline
            spline = interpolate.make_interp_spline(x, y, k=3)
            
            # Generate smooth x values
            x_smooth = np.linspace(x.min(), x.max(), len(x) * 10)
            y_smooth = spline(x_smooth)
            
            return x_smooth, y_smooth
        except Exception:
            # Fall back to original data if smoothing fails
            return x, y

    def _get_linestyle(self) -> str:
        """Convert style line_style to matplotlib format."""
        style_map = {
            "solid": "-",
            "dashed": "--",
            "dotted": ":",
            "dashdot": "-.",
        }
        return style_map.get(self.style.line_style, "-")

