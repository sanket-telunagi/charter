"""
Style definitions for different chart types.

Styles control chart-type-specific rendering options like
bar orientation, line smoothing, pie exploding, etc.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Literal


class ChartType(str, Enum):
    """Supported chart types."""
    BAR = "bar"
    PIE = "pie"
    LINE = "line"
    TIMESERIES = "timeseries"


@dataclass(frozen=True)
class Style:
    """Base style configuration."""
    name: str
    chart_type: ChartType


# ============================================================================
# Bar Chart Styles
# ============================================================================

@dataclass(frozen=True)
class BarStyle(Style):
    """
    Style configuration for bar charts.
    
    Attributes:
        orientation: 'vertical' or 'horizontal'
        grouped: Whether to group multiple series side by side
        stacked: Whether to stack multiple series
        bar_width: Width of bars (0-1, relative)
        edge_color: Bar border color (None for no border)
        edge_width: Bar border width
        show_values: Whether to show value labels on bars
        value_format: Format string for value labels
    """
    chart_type: ChartType = ChartType.BAR
    orientation: Literal["vertical", "horizontal"] = "vertical"
    grouped: bool = False
    stacked: bool = False
    bar_width: float = 0.8
    edge_color: str | None = None
    edge_width: float = 0.5
    show_values: bool = False
    value_format: str = "{:.1f}"
    alpha: float = 1.0


# Built-in bar styles
BAR_STYLES: dict[str, BarStyle] = {
    "default": BarStyle(name="default"),
    "grouped": BarStyle(name="grouped", grouped=True, bar_width=0.35),
    "stacked": BarStyle(name="stacked", stacked=True),
    "horizontal": BarStyle(name="horizontal", orientation="horizontal"),
    "outlined": BarStyle(name="outlined", edge_color="#333333", edge_width=1.0),
    "labeled": BarStyle(name="labeled", show_values=True),
}


# ============================================================================
# Pie Chart Styles
# ============================================================================

@dataclass(frozen=True)
class PieStyle(Style):
    """
    Style configuration for pie charts.
    
    Attributes:
        donut: Whether to render as a donut (ring) chart
        donut_ratio: Inner radius ratio for donut charts (0-1)
        explode: Whether to explode (separate) slices
        explode_amount: Amount to explode slices
        start_angle: Starting angle in degrees
        counter_clockwise: Direction of slices
        show_percentages: Whether to show percentage labels
        show_labels: Whether to show slice labels
        label_distance: Distance of labels from center
        shadow: Whether to add shadow effect
        infographic: Whether to use infographic style with external labels and leader lines
        leader_line_color: Color for leader lines (None uses axis color)
        leader_line_width: Width of leader lines
        external_label_format: Format for external labels ('{label}', '{percent}', '{label}, {percent}')
        center_title: Whether to show center title in donut hole
        use_annotate: Whether to use matplotlib annotate() for leader lines
        label_bbox: Whether to add rounded background boxes to labels
        label_bbox_style: Style string for bbox (e.g., 'round,pad=0.3')
        label_bbox_facecolor: Background color for label bbox
        label_bbox_edgecolor: Border color for label bbox
        label_bbox_alpha: Transparency for label bbox
        transparent_background: Whether to use fully transparent figure background
        center_title_bbox: Whether to show background box behind center title
        center_title_bbox_facecolor: Background color for center title box
        center_title_bbox_alpha: Transparency for center title box
        center_title_bbox_pad: Padding for center title box
        table_legend: Whether to show a table legend on the side instead of labels
        table_legend_position: Position of table legend ('right', 'bottom', 'left')
        table_legend_show_value: Whether to show value column in table legend
        table_legend_show_percent: Whether to show percentage column in table legend
        table_legend_header: Whether to show column headers in table legend
    """
    chart_type: ChartType = ChartType.PIE
    donut: bool = False
    donut_ratio: float = 0.5
    explode: bool = False
    explode_amount: float = 0.05
    start_angle: float = 90.0
    counter_clockwise: bool = False
    show_percentages: bool = True
    show_labels: bool = True
    label_distance: float = 1.1
    shadow: bool = False
    infographic: bool = False
    leader_line_color: str | None = None
    leader_line_width: float = 1.0
    external_label_format: str = "{label}, {percent}"
    # Annotated style options
    center_title: bool = False
    use_annotate: bool = False
    label_bbox: bool = False
    label_bbox_style: str = "round,pad=0.3"
    label_bbox_facecolor: str = "white"
    label_bbox_edgecolor: str = "#dddddd"
    label_bbox_alpha: float = 0.85
    # Transparent donut style options
    transparent_background: bool = False
    center_title_bbox: bool = False
    center_title_bbox_facecolor: str = "#333333"
    center_title_bbox_alpha: float = 0.85
    center_title_bbox_pad: float = 0.5
    # Table legend style options
    table_legend: bool = False
    table_legend_position: Literal["right", "bottom", "left"] = "right"
    table_legend_show_value: bool = True
    table_legend_show_percent: bool = True
    table_legend_header: bool = False


# Built-in pie styles
PIE_STYLES: dict[str, PieStyle] = {
    "default": PieStyle(name="default"),
    "donut": PieStyle(name="donut", donut=True),
    "exploded": PieStyle(name="exploded", explode=True),
    "minimal": PieStyle(name="minimal", show_percentages=False, show_labels=True),
    "detailed": PieStyle(name="detailed", show_percentages=True, show_labels=True),
    "shadow": PieStyle(name="shadow", shadow=True, explode=True, explode_amount=0.02),
    "infographic": PieStyle(
        name="infographic",
        donut=True,
        donut_ratio=0.65,
        infographic=True,
        show_percentages=False,
        show_labels=False,
        start_angle=90.0,
        external_label_format="{label}, {percent}",
    ),
    "annotated": PieStyle(
        name="annotated",
        donut=True,
        donut_ratio=0.6,
        center_title=True,
        use_annotate=True,
        label_bbox=True,
        show_percentages=False,
        show_labels=False,
        start_angle=90.0,
        counter_clockwise=False,
    ),
    "transparent_donut": PieStyle(
        name="transparent_donut",
        donut=True,
        donut_ratio=0.55,
        center_title=True,
        center_title_bbox=True,
        center_title_bbox_facecolor="#444444",
        center_title_bbox_alpha=0.9,
        center_title_bbox_pad=0.5,
        use_annotate=True,
        label_bbox=True,
        label_bbox_style="round,pad=0.3",
        label_bbox_facecolor="#444444",
        label_bbox_edgecolor="none",
        label_bbox_alpha=0.9,
        show_percentages=False,
        show_labels=False,
        start_angle=90.0,
        counter_clockwise=False,
        transparent_background=True,
        leader_line_color="#777777",
    ),
    "table_legend": PieStyle(
        name="table_legend",
        donut=False,
        table_legend=True,
        show_percentages=False,
        show_labels=False,
    ),
    "table_legend_donut": PieStyle(
        name="table_legend_donut",
        donut=True,
        donut_ratio=0.5,
        table_legend=True,
        center_title=True,
        center_title_bbox=True,
        center_title_bbox_facecolor="#444444",
        center_title_bbox_alpha=0.85,
        center_title_bbox_pad=0.4,
        show_percentages=False,
        show_labels=False,
    ),
}


# ============================================================================
# Line Chart Styles
# ============================================================================

@dataclass(frozen=True)
class LineStyle(Style):
    """
    Style configuration for line charts.
    
    Attributes:
        smooth: Whether to smooth the line (spline interpolation)
        stepped: Whether to use step function
        fill_area: Whether to fill area under the line
        fill_alpha: Alpha for area fill
        marker: Marker style ('o', 's', '^', None, etc.)
        marker_size: Size of markers
        line_style: Line style ('solid', 'dashed', 'dotted', 'dashdot')
        show_points: Whether to show data points
    """
    chart_type: ChartType = ChartType.LINE
    smooth: bool = False
    stepped: bool = False
    fill_area: bool = False
    fill_alpha: float = 0.3
    marker: str | None = None
    marker_size: float = 6.0
    line_style: str = "solid"
    show_points: bool = False


# Built-in line styles
LINE_STYLES: dict[str, LineStyle] = {
    "default": LineStyle(name="default"),
    "smooth": LineStyle(name="smooth", smooth=True),
    "stepped": LineStyle(name="stepped", stepped=True),
    "area": LineStyle(name="area", fill_area=True),
    "dotted": LineStyle(name="dotted", line_style="dotted", show_points=True, marker="o"),
    "dashed": LineStyle(name="dashed", line_style="dashed"),
    "markers": LineStyle(name="markers", show_points=True, marker="o", marker_size=8.0),
}


# ============================================================================
# Time Series Styles
# ============================================================================

@dataclass(frozen=True)
class TimeSeriesStyle(Style):
    """
    Style configuration for time series charts.
    
    Attributes:
        date_format: Format string for date axis labels
        show_grid: Whether to show grid lines
        fill_area: Whether to fill area under the line
        fill_alpha: Alpha for area fill
        show_trend: Whether to show trend line
        trend_color: Color for trend line
        range_bands: Whether to show confidence/range bands
        band_alpha: Alpha for range bands
        marker: Marker style for data points
        line_style: Line style (solid, dashed, dotted, dashdot)
        auto_downsample: Whether to automatically downsample large datasets
        downsample_threshold: Override settings threshold (None uses settings default)
        rasterize: Force rasterization of the plot
        auto_rasterize: Automatically rasterize large datasets
    """
    chart_type: ChartType = ChartType.TIMESERIES
    date_format: str = "%Y-%m-%d"
    show_grid: bool = True
    fill_area: bool = False
    fill_alpha: float = 0.2
    show_trend: bool = False
    trend_color: str = "#FF6B6B"
    range_bands: bool = False
    band_alpha: float = 0.15
    marker: str | None = None
    line_style: str = "solid"
    # Large dataset handling
    auto_downsample: bool = True
    downsample_threshold: int | None = None
    rasterize: bool = False
    auto_rasterize: bool = True


# Built-in time series styles
TIMESERIES_STYLES: dict[str, TimeSeriesStyle] = {
    "default": TimeSeriesStyle(name="default"),
    "area": TimeSeriesStyle(name="area", fill_area=True),
    "trend": TimeSeriesStyle(name="trend", show_trend=True),
    "range": TimeSeriesStyle(name="range", range_bands=True),
    "minimal": TimeSeriesStyle(name="minimal", show_grid=False),
    "large_dataset": TimeSeriesStyle(
        name="large_dataset",
        auto_downsample=True,
        auto_rasterize=True,
        show_grid=True,
        line_style="solid",
        date_format="%Y-%m-%d %H:%M",
    ),
}

