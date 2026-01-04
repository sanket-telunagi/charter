"""
Time series chart implementation with support for various styles.

Supports:
- Time-based x-axis with proper date formatting
- Trend lines
- Confidence/range bands
- Area fills
- Automatic downsampling for large datasets (LTTB algorithm)
- Rasterization for improved performance
"""

import warnings
from typing import Any
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure

from charter.charts.base import BaseChart
from charter.config.settings import get_settings
from charter.styles.presets import TimeSeriesStyle
from charter.themes.base import Theme
from charter.utils.downsampling import lttb_downsample


class TimeSeriesChart(BaseChart):
    """
    Time series chart renderer with date handling.
    
    Expected data format:
        Basic:
        {
            "dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "values": [100, 105, 102]
        }
        
        With datetime objects:
        {
            "dates": [datetime(2024, 1, 1), datetime(2024, 1, 2)],
            "values": [100, 105]
        }
        
        With range bands (for confidence intervals):
        {
            "dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "values": [100, 105, 102],
            "upper": [110, 115, 112],
            "lower": [90, 95, 92]
        }
        
        Multiple series:
        {
            "dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "series": {
                "Series A": [100, 105, 102],
                "Series B": [95, 100, 98]
            }
        }
    """

    def __init__(
        self,
        data: dict[str, Any],
        style: TimeSeriesStyle,
        theme: Theme,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
    ) -> None:
        super().__init__(data, style, theme, title, xlabel, ylabel)
        self.style: TimeSeriesStyle = style  # Type narrowing

    def _render_sync(self) -> Figure:
        """Render the time series chart synchronously."""
        fig, ax = self._create_figure()
        
        self._render_to_axes_impl(ax)
        self._apply_labels(ax)
        self._apply_legend(ax)
        
        return self._finalize_figure(fig)
    
    def _render_to_axes_impl(self, ax: plt.Axes) -> None:
        """Render time series content to an existing axes."""
        # Parse dates
        dates = self._parse_dates(self.data.get("dates", []))
        
        # Determine if rasterization should be applied
        should_rasterize = self._should_rasterize(len(dates))
        
        # Check if we have multiple series or single series
        if "series" in self.data:
            self._render_multi_series(ax, dates, rasterize=should_rasterize)
        else:
            values = np.array(self.data.get("values", []))
            
            # Apply downsampling if needed
            dates, values = self._maybe_downsample(dates, values)
            
            self._render_single_series(
                ax, dates, values, 
                color=self.theme.get_color(0),
                rasterize=should_rasterize
            )
            
            # Add range bands if present
            if self.style.range_bands and "upper" in self.data and "lower" in self.data:
                upper = np.array(self.data["upper"])
                lower = np.array(self.data["lower"])
                # Downsample range bands too if main data was downsampled
                if len(upper) != len(dates):
                    _, upper = self._maybe_downsample(
                        self._parse_dates(self.data.get("dates", [])), upper
                    )
                    _, lower = self._maybe_downsample(
                        self._parse_dates(self.data.get("dates", [])), lower
                    )
                self._add_range_bands(ax, dates, upper, lower, self.theme.get_color(0))
        
        # Add trend line if requested (use original data for accurate trend)
        if self.style.show_trend and "values" in self.data:
            original_dates = self._parse_dates(self.data.get("dates", []))
            original_values = np.array(self.data["values"])
            self._add_trend_line(ax, original_dates, original_values)
        
        # Format date axis
        self._format_date_axis(ax)
        
        # Apply grid
        if self.style.show_grid:
            ax.grid(True, alpha=self.theme.grid_alpha, color=self.theme.grid_color)
        else:
            ax.grid(False)
    
    def _get_downsample_threshold(self) -> int:
        """Get the effective downsample threshold."""
        if self.style.downsample_threshold is not None:
            return self.style.downsample_threshold
        return self._settings.downsample_threshold
    
    def _should_rasterize(self, n_points: int) -> bool:
        """Determine if the plot should be rasterized."""
        if self.style.rasterize:
            return True
        if self.style.auto_rasterize:
            return n_points > self._settings.auto_rasterize_threshold
        return False
    
    def _maybe_downsample(
        self,
        dates: list[datetime],
        values: np.ndarray,
    ) -> tuple[list[datetime], np.ndarray]:
        """Apply LTTB downsampling if data exceeds threshold."""
        n_points = len(values)
        threshold = self._get_downsample_threshold()
        
        # Skip if downsampling is disabled or not needed
        if not self.style.auto_downsample or threshold <= 0:
            return dates, values
        
        if n_points <= threshold:
            return dates, values
        
        # Apply hard limit from settings
        target_points = min(threshold, self._settings.max_render_points)
        
        # Log warning for very large datasets
        if n_points > 100000:
            warnings.warn(
                f"Large dataset ({n_points:,} points) being downsampled to {target_points:,} points. "
                f"Set auto_downsample=False to disable.",
                UserWarning,
                stacklevel=3,
            )
        
        # Apply LTTB downsampling
        dates_arr = np.array(dates)
        downsampled_dates, downsampled_values = lttb_downsample(
            dates_arr, values, threshold=target_points
        )
        
        return list(downsampled_dates), downsampled_values

    def _parse_dates(self, dates: list) -> list[datetime]:
        """Parse dates from various formats."""
        parsed = []
        for d in dates:
            if isinstance(d, datetime):
                parsed.append(d)
            elif isinstance(d, str):
                # Try common date formats
                for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", 
                           "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]:
                    try:
                        parsed.append(datetime.strptime(d, fmt))
                        break
                    except ValueError:
                        continue
                else:
                    # Use pandas as fallback
                    parsed.append(pd.to_datetime(d).to_pydatetime())
            elif isinstance(d, (int, float)):
                # Assume timestamp
                parsed.append(datetime.fromtimestamp(d))
            else:
                # Try pandas conversion
                parsed.append(pd.to_datetime(d).to_pydatetime())
        return parsed

    def _render_single_series(
        self,
        ax: plt.Axes,
        dates: list[datetime],
        values: np.ndarray,
        color: str,
        label: str | None = None,
        rasterize: bool = False,
    ) -> None:
        """Render a single time series."""
        line_kwargs = {
            "color": color,
            "linewidth": self.theme.line_width,
            "linestyle": self._get_linestyle(),
            "rasterized": rasterize,
        }
        
        if label:
            line_kwargs["label"] = label
        
        ax.plot(dates, values, **line_kwargs)
        
        # Add markers if specified (skip for very large datasets)
        if self.style.marker and len(values) < 10000:
            ax.scatter(
                dates, values, 
                color=color, s=36, marker=self.style.marker, zorder=5,
                rasterized=rasterize
            )
        
        # Fill area if needed
        if self.style.fill_area:
            ax.fill_between(
                dates, values, 0,
                color=color,
                alpha=self.style.fill_alpha,
                rasterized=rasterize,
            )

    def _render_multi_series(
        self,
        ax: plt.Axes,
        dates: list[datetime],
        rasterize: bool = False,
    ) -> None:
        """Render multiple time series."""
        series_data = self.data.get("series", {})
        
        for i, (name, values) in enumerate(series_data.items()):
            y = np.array(values)
            color = self.theme.get_color(i)
            
            # Apply downsampling to each series
            series_dates, series_values = self._maybe_downsample(dates, y)
            
            self._render_single_series(
                ax, series_dates, series_values, 
                color=color, label=name, rasterize=rasterize
            )

    def _add_range_bands(
        self,
        ax: plt.Axes,
        dates: list[datetime],
        upper: np.ndarray,
        lower: np.ndarray,
        color: str,
    ) -> None:
        """Add confidence/range bands."""
        ax.fill_between(
            dates,
            lower,
            upper,
            color=color,
            alpha=self.style.band_alpha,
        )

    def _add_trend_line(
        self,
        ax: plt.Axes,
        dates: list[datetime],
        values: np.ndarray,
    ) -> None:
        """Add a linear trend line."""
        # Convert dates to numeric for regression
        x_numeric = mdates.date2num(dates)
        
        # Fit linear regression
        z = np.polyfit(x_numeric, values, 1)
        p = np.poly1d(z)
        
        # Plot trend line
        ax.plot(
            dates,
            p(x_numeric),
            color=self.style.trend_color,
            linewidth=self.theme.line_width * 0.75,
            linestyle="--",
            label="Trend",
            alpha=0.8,
        )

    def _format_date_axis(self, ax: plt.Axes) -> None:
        """Format the date axis with appropriate locator and formatter."""
        # Auto-format based on date range
        ax.xaxis.set_major_formatter(mdates.DateFormatter(self.style.date_format))
        
        # Rotate labels for readability
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
        
        # Auto-locate ticks
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())

    def _get_linestyle(self) -> str:
        """Convert style line_style to matplotlib format."""
        style_map = {
            "solid": "-",
            "dashed": "--",
            "dotted": ":",
            "dashdot": "-.",
        }
        return style_map.get(self.style.line_style, "-")

