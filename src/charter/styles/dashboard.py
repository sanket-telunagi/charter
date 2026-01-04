"""
Dashboard layout and panel configuration for multi-panel charts.

Provides dataclasses for configuring dashboard layouts with multiple
panels, each containing different chart types.
"""

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class PanelConfig:
    """
    Configuration for a single dashboard panel.
    
    Attributes:
        chart_type: Type of chart ("bar", "line", "timeseries", "pie")
        data: Chart data dictionary
        style: Chart style preset name
        title: Optional panel title
        xlabel: Optional x-axis label
        ylabel: Optional y-axis label
        row: Grid row position (0-indexed)
        col: Grid column position (0-indexed)
        colspan: Number of columns to span
        rowspan: Number of rows to span
    """
    chart_type: str
    data: dict[str, Any]
    style: str = "default"
    title: str | None = None
    xlabel: str | None = None
    ylabel: str | None = None
    row: int = 0
    col: int = 0
    colspan: int = 1
    rowspan: int = 1
    
    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "PanelConfig":
        """Create PanelConfig from a dictionary."""
        return cls(
            chart_type=d["chart_type"],
            data=d["data"],
            style=d.get("style", "default"),
            title=d.get("title"),
            xlabel=d.get("xlabel"),
            ylabel=d.get("ylabel"),
            row=d.get("row", 0),
            col=d.get("col", 0),
            colspan=d.get("colspan", 1),
            rowspan=d.get("rowspan", 1),
        )


@dataclass
class DashboardLayout:
    """
    Configuration for dashboard grid layout.
    
    Attributes:
        rows: Number of grid rows
        cols: Number of grid columns
        figsize: Figure size as (width, height) in inches
        shared_legend: Whether to show a shared legend for all panels
        legend_position: Position of shared legend ("top", "bottom", "right")
        width_ratios: Relative width ratios for columns (e.g., [2, 1])
        height_ratios: Relative height ratios for rows (e.g., [1, 2])
        hspace: Horizontal space between panels (0.0 - 1.0)
        wspace: Vertical space between panels (0.0 - 1.0)
        title_y: Y position of main title (default 0.98)
    """
    rows: int = 1
    cols: int = 2
    figsize: tuple[float, float] = (16, 6)
    shared_legend: bool = True
    legend_position: Literal["top", "bottom", "right"] = "top"
    width_ratios: list[float] | None = None
    height_ratios: list[float] | None = None
    hspace: float = 0.3
    wspace: float = 0.3
    title_y: float = 0.98
    
    @classmethod
    def from_dict(cls, d: dict[str, Any] | None) -> "DashboardLayout":
        """Create DashboardLayout from a dictionary, with defaults."""
        if d is None:
            return cls()
        return cls(
            rows=d.get("rows", 1),
            cols=d.get("cols", 2),
            figsize=tuple(d.get("figsize", (16, 6))),
            shared_legend=d.get("shared_legend", True),
            legend_position=d.get("legend_position", "top"),
            width_ratios=d.get("width_ratios"),
            height_ratios=d.get("height_ratios"),
            hspace=d.get("hspace", 0.3),
            wspace=d.get("wspace", 0.3),
            title_y=d.get("title_y", 0.98),
        )


# Built-in dashboard layout presets
DASHBOARD_LAYOUTS: dict[str, DashboardLayout] = {
    "default": DashboardLayout(),
    "side_by_side": DashboardLayout(rows=1, cols=2, figsize=(16, 6)),
    "stacked": DashboardLayout(rows=2, cols=1, figsize=(12, 10)),
    "wide_left": DashboardLayout(
        rows=1, cols=2, figsize=(16, 6), width_ratios=[2, 1]
    ),
    "wide_right": DashboardLayout(
        rows=1, cols=2, figsize=(16, 6), width_ratios=[1, 2]
    ),
    "grid_2x2": DashboardLayout(rows=2, cols=2, figsize=(14, 10)),
    "traffic_latency": DashboardLayout(
        rows=1, cols=2, figsize=(18, 6), width_ratios=[2.5, 1],
        shared_legend=True, legend_position="top"
    ),
}


def get_dashboard_layout(name: str) -> DashboardLayout:
    """
    Get a dashboard layout preset by name.
    
    Args:
        name: Preset name ("default", "side_by_side", "stacked", etc.)
        
    Returns:
        DashboardLayout configuration
        
    Raises:
        KeyError: If layout name not found
    """
    if name not in DASHBOARD_LAYOUTS:
        available = ", ".join(DASHBOARD_LAYOUTS.keys())
        raise KeyError(f"Unknown dashboard layout '{name}'. Available: {available}")
    return DASHBOARD_LAYOUTS[name]
