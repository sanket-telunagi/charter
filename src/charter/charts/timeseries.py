"""
Time series chart implementation with support for various styles.

Supports:
- Time-based x-axis with proper date formatting
- Trend lines
- Confidence/range bands
- Area fills
"""

from typing import Any
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure

from charter.charts.base import BaseChart
from charter.styles.presets import TimeSeriesStyle
from charter.themes.base import Theme


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
        
        # Parse dates
        dates = self._parse_dates(self.data.get("dates", []))
        
        # Check if we have multiple series or single series
        if "series" in self.data:
            self._render_multi_series(ax, dates)
        else:
            values = np.array(self.data.get("values", []))
            self._render_single_series(ax, dates, values, color=self.theme.get_color(0))
            
            # Add range bands if present
            if self.style.range_bands and "upper" in self.data and "lower" in self.data:
                upper = np.array(self.data["upper"])
                lower = np.array(self.data["lower"])
                self._add_range_bands(ax, dates, upper, lower, self.theme.get_color(0))
        
        # Add trend line if requested
        if self.style.show_trend and "values" in self.data:
            values = np.array(self.data["values"])
            self._add_trend_line(ax, dates, values)
        
        # Format date axis
        self._format_date_axis(ax)
        
        # Apply grid
        if self.style.show_grid:
            ax.grid(True, alpha=self.theme.grid_alpha, color=self.theme.grid_color)
        else:
            ax.grid(False)
        
        self._apply_labels(ax)
        self._apply_legend(ax)
        
        return self._finalize_figure(fig)

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
    ) -> None:
        """Render a single time series."""
        line_kwargs = {
            "color": color,
            "linewidth": self.theme.line_width,
            "linestyle": self._get_linestyle(),
        }
        
        if label:
            line_kwargs["label"] = label
        
        ax.plot(dates, values, **line_kwargs)
        
        # Add markers if specified
        if self.style.marker:
            ax.scatter(dates, values, color=color, s=36, marker=self.style.marker, zorder=5)
        
        # Fill area if needed
        if self.style.fill_area:
            ax.fill_between(
                dates, values, 0,
                color=color,
                alpha=self.style.fill_alpha,
            )

    def _render_multi_series(
        self,
        ax: plt.Axes,
        dates: list[datetime],
    ) -> None:
        """Render multiple time series."""
        series_data = self.data.get("series", {})
        
        for i, (name, values) in enumerate(series_data.items()):
            y = np.array(values)
            color = self.theme.get_color(i)
            self._render_single_series(ax, dates, y, color=color, label=name)

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

