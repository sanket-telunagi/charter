"""
Bar chart implementation with support for various styles.

Supports:
- Vertical and horizontal bars
- Grouped bars for multiple series
- Stacked bars
- Value labels on bars
"""

from typing import Any

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from charter.charts.base import BaseChart
from charter.styles.presets import BarStyle
from charter.themes.base import Theme


class BarChart(BaseChart):
    """
    Bar chart renderer with multiple style options.
    
    Expected data format:
        Single series:
        {
            "labels": ["A", "B", "C"],
            "values": [10, 20, 15]
        }
        
        Multiple series:
        {
            "labels": ["A", "B", "C"],
            "series": {
                "Series 1": [10, 20, 15],
                "Series 2": [12, 18, 22]
            }
        }
    """

    def __init__(
        self,
        data: dict[str, Any],
        style: BarStyle,
        theme: Theme,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
    ) -> None:
        super().__init__(data, style, theme, title, xlabel, ylabel)
        self.style: BarStyle = style  # Type narrowing

    def _render_sync(self) -> Figure:
        """Render the bar chart synchronously."""
        fig, ax = self._create_figure()
        
        labels = self.data.get("labels", [])
        
        # Check if we have multiple series or single series
        if "series" in self.data:
            self._render_multi_series(ax, labels)
        else:
            values = self.data.get("values", [])
            self._render_single_series(ax, labels, values)
        
        self._apply_labels(ax)
        self._apply_legend(ax)
        
        return self._finalize_figure(fig)

    def _render_single_series(
        self,
        ax: plt.Axes,
        labels: list[str],
        values: list[float],
    ) -> None:
        """Render a single series bar chart."""
        x = np.arange(len(labels))
        colors = [self.theme.get_color(i) for i in range(len(labels))]
        
        bar_kwargs = {
            "width" if self.style.orientation == "vertical" else "height": self.style.bar_width,
            "color": colors,
            "alpha": self.style.alpha,
        }
        
        if self.style.edge_color:
            bar_kwargs["edgecolor"] = self.style.edge_color
            bar_kwargs["linewidth"] = self.style.edge_width
        
        if self.style.orientation == "vertical":
            bars = ax.bar(x, values, **bar_kwargs)
            ax.set_xticks(x)
            ax.set_xticklabels(labels)
        else:
            bars = ax.barh(x, values, **bar_kwargs)
            ax.set_yticks(x)
            ax.set_yticklabels(labels)
        
        if self.style.show_values:
            self._add_value_labels(ax, bars)

    def _render_multi_series(
        self,
        ax: plt.Axes,
        labels: list[str],
    ) -> None:
        """Render a multi-series bar chart (grouped or stacked)."""
        series_data = self.data.get("series", {})
        series_names = list(series_data.keys())
        n_series = len(series_names)
        n_labels = len(labels)
        
        x = np.arange(n_labels)
        
        if self.style.stacked:
            self._render_stacked(ax, x, labels, series_data, series_names)
        elif self.style.grouped:
            self._render_grouped(ax, x, labels, series_data, series_names, n_series)
        else:
            # Default to grouped for multiple series
            self._render_grouped(ax, x, labels, series_data, series_names, n_series)

    def _render_grouped(
        self,
        ax: plt.Axes,
        x: np.ndarray,
        labels: list[str],
        series_data: dict[str, list[float]],
        series_names: list[str],
        n_series: int,
    ) -> None:
        """Render grouped bars."""
        width = self.style.bar_width / n_series
        
        for i, name in enumerate(series_names):
            values = series_data[name]
            offset = (i - n_series / 2 + 0.5) * width
            color = self.theme.get_color(i)
            
            bar_kwargs = {
                "width": width,
                "color": color,
                "label": name,
                "alpha": self.style.alpha,
            }
            
            if self.style.edge_color:
                bar_kwargs["edgecolor"] = self.style.edge_color
                bar_kwargs["linewidth"] = self.style.edge_width
            
            if self.style.orientation == "vertical":
                bars = ax.bar(x + offset, values, **bar_kwargs)
            else:
                bars = ax.barh(x + offset, values, height=width, color=color, label=name)
            
            if self.style.show_values:
                self._add_value_labels(ax, bars)
        
        if self.style.orientation == "vertical":
            ax.set_xticks(x)
            ax.set_xticklabels(labels)
        else:
            ax.set_yticks(x)
            ax.set_yticklabels(labels)

    def _render_stacked(
        self,
        ax: plt.Axes,
        x: np.ndarray,
        labels: list[str],
        series_data: dict[str, list[float]],
        series_names: list[str],
    ) -> None:
        """Render stacked bars."""
        bottom = np.zeros(len(labels))
        
        for i, name in enumerate(series_names):
            values = np.array(series_data[name])
            color = self.theme.get_color(i)
            
            bar_kwargs = {
                "width": self.style.bar_width,
                "color": color,
                "label": name,
                "alpha": self.style.alpha,
            }
            
            if self.style.edge_color:
                bar_kwargs["edgecolor"] = self.style.edge_color
                bar_kwargs["linewidth"] = self.style.edge_width
            
            if self.style.orientation == "vertical":
                ax.bar(x, values, bottom=bottom, **bar_kwargs)
            else:
                ax.barh(x, values, left=bottom, height=self.style.bar_width, 
                       color=color, label=name)
            
            bottom += values
        
        if self.style.orientation == "vertical":
            ax.set_xticks(x)
            ax.set_xticklabels(labels)
        else:
            ax.set_yticks(x)
            ax.set_yticklabels(labels)

    def _add_value_labels(self, ax: plt.Axes, bars) -> None:
        """Add value labels to bars."""
        for bar in bars:
            if self.style.orientation == "vertical":
                height = bar.get_height()
                ax.annotate(
                    self.style.value_format.format(height),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    ha="center",
                    va="bottom",
                    fontsize=self.theme.tick_font_size,
                    color=self.theme.text_color,
                )
            else:
                width = bar.get_width()
                ax.annotate(
                    self.style.value_format.format(width),
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    ha="left",
                    va="center",
                    fontsize=self.theme.tick_font_size,
                    color=self.theme.text_color,
                )

