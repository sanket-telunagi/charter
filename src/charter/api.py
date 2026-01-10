"""
Public API for Charter library.

This module provides the main entry point for generating charts.
"""

from pathlib import Path
from typing import Any, Literal

from charter.charts.bar import BarChart
from charter.charts.pie import PieChart
from charter.charts.line import LineChart
from charter.charts.timeseries import TimeSeriesChart
from charter.charts.rose import RoseChart
from charter.charts.dashboard import DashboardChart
from charter.config.settings import get_settings
from charter.output.manager import get_output_manager, OutputFormat
from charter.styles.registry import get_style_registry
from charter.styles.presets import ChartType
from charter.styles.dashboard import PanelConfig, DashboardLayout
from charter.themes.presets import get_theme
from charter.utils.validators import validate_chart_data


ChartTypeLiteral = Literal["bar", "pie", "line", "timeseries", "rose"]


async def generate_chart(
    chart_type: ChartTypeLiteral,
    data: dict[str, Any],
    style: str = "default",
    theme: str | None = None,
    output_format: OutputFormat | None = None,
    filename: str | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    dpi: int | None = None,
) -> Path:
    """
    Generate a chart and save it to the output directory.
    
    This is the main entry point for chart generation. It handles:
    - Data validation
    - Style and theme resolution
    - Async chart rendering
    - File output with unique naming
    
    Args:
        chart_type: Type of chart to generate ('bar', 'pie', 'line', 'timeseries', 'rose')
        data: Chart data dictionary (format depends on chart type)
        style: Style name to use (default: 'default')
        theme: Theme name to use (default: from settings)
        output_format: Output file format ('png', 'svg', 'pdf', 'jpeg')
        filename: Optional custom filename (without extension)
        title: Optional chart title
        xlabel: Optional x-axis label
        ylabel: Optional y-axis label
        dpi: Optional DPI override for raster formats
        
    Returns:
        Path: Full path to the generated chart file
        
    Raises:
        ValueError: If chart type, style, or theme is invalid
        ChartDataError: If data validation fails
        
    Examples:
        Basic bar chart:
        >>> path = await generate_chart(
        ...     chart_type="bar",
        ...     data={"labels": ["A", "B", "C"], "values": [10, 20, 15]},
        ... )
        
        Styled pie chart:
        >>> path = await generate_chart(
        ...     chart_type="pie",
        ...     data={"labels": ["Red", "Blue", "Green"], "values": [30, 45, 25]},
        ...     style="donut",
        ...     theme="dark",
        ...     title="Color Distribution",
        ... )
        
        Multi-series line chart:
        >>> path = await generate_chart(
        ...     chart_type="line",
        ...     data={
        ...         "x": [1, 2, 3, 4, 5],
        ...         "series": {
        ...             "Revenue": [100, 120, 115, 130, 145],
        ...             "Costs": [80, 85, 90, 88, 92],
        ...         }
        ...     },
        ...     style="smooth",
        ...     theme="minimal",
        ... )
        
        Time series with trend:
        >>> path = await generate_chart(
        ...     chart_type="timeseries",
        ...     data={
        ...         "dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
        ...         "values": [100, 105, 102],
        ...     },
        ...     style="trend",
        ... )
    """
    # Get settings
    settings = get_settings()
    
    # Resolve defaults from settings
    resolved_theme = theme or settings.default_theme
    resolved_format = output_format or settings.default_format
    
    # Validate chart data
    validate_chart_data(chart_type, data)
    
    # Get style and theme
    style_registry = get_style_registry()
    chart_style = style_registry.get_style(chart_type, style)
    chart_theme = get_theme(resolved_theme)
    
    # Create the appropriate chart instance
    chart_class = _get_chart_class(chart_type)
    chart = chart_class(
        data=data,
        style=chart_style,
        theme=chart_theme,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
    )
    
    # Render the chart
    figure = await chart.render()
    
    # Save to file
    output_manager = get_output_manager()
    output_path = await output_manager.save_chart(
        figure=figure,
        chart_type=chart_type,
        output_format=resolved_format,
        filename=filename,
        dpi=dpi,
    )
    
    return output_path


def _get_chart_class(chart_type: str):
    """Get the chart class for a given chart type."""
    chart_classes = {
        "bar": BarChart,
        "pie": PieChart,
        "line": LineChart,
        "timeseries": TimeSeriesChart,
        "rose": RoseChart,
    }
    
    chart_class = chart_classes.get(chart_type.lower())
    if chart_class is None:
        available = list(chart_classes.keys())
        raise ValueError(
            f"Unknown chart type '{chart_type}'. Available: {', '.join(available)}"
        )
    
    return chart_class


# Convenience functions for specific chart types

async def generate_bar_chart(
    data: dict[str, Any],
    style: str = "default",
    theme: str | None = None,
    output_format: OutputFormat | None = None,
    filename: str | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
) -> Path:
    """Generate a bar chart. Convenience wrapper around generate_chart()."""
    return await generate_chart(
        chart_type="bar",
        data=data,
        style=style,
        theme=theme,
        output_format=output_format,
        filename=filename,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
    )


async def generate_pie_chart(
    data: dict[str, Any],
    style: str = "default",
    theme: str | None = None,
    output_format: OutputFormat | None = None,
    filename: str | None = None,
    title: str | None = None,
) -> Path:
    """Generate a pie chart. Convenience wrapper around generate_chart()."""
    return await generate_chart(
        chart_type="pie",
        data=data,
        style=style,
        theme=theme,
        output_format=output_format,
        filename=filename,
        title=title,
    )


async def generate_line_chart(
    data: dict[str, Any],
    style: str = "default",
    theme: str | None = None,
    output_format: OutputFormat | None = None,
    filename: str | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
) -> Path:
    """Generate a line chart. Convenience wrapper around generate_chart()."""
    return await generate_chart(
        chart_type="line",
        data=data,
        style=style,
        theme=theme,
        output_format=output_format,
        filename=filename,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
    )


async def generate_timeseries_chart(
    data: dict[str, Any],
    style: str = "default",
    theme: str | None = None,
    output_format: OutputFormat | None = None,
    filename: str | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
) -> Path:
    """Generate a time series chart. Convenience wrapper around generate_chart()."""
    return await generate_chart(
        chart_type="timeseries",
        data=data,
        style=style,
        theme=theme,
        output_format=output_format,
        filename=filename,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
    )


async def generate_rose_chart(
    data: dict[str, Any],
    style: str = "default",
    theme: str | None = None,
    output_format: OutputFormat | None = None,
    filename: str | None = None,
    title: str | None = None,
) -> Path:
    """Generate a Nightingale rose chart. Convenience wrapper around generate_chart()."""
    return await generate_chart(
        chart_type="rose",
        data=data,
        style=style,
        theme=theme,
        output_format=output_format,
        filename=filename,
        title=title,
    )


async def generate_dashboard(
    panels: list[dict[str, Any]],
    layout: dict[str, Any] | None = None,
    theme: str = "plotly_dark",
    title: str | None = None,
    output_format: OutputFormat | None = None,
    filename: str | None = None,
    dpi: int | None = None,
) -> Path:
    """
    Generate a multi-panel dashboard and save it to the output directory.
    
    Creates a composite figure with multiple charts arranged in a grid layout,
    with optional shared legend and consistent theming.
    
    Args:
        panels: List of panel configurations. Each panel is a dict with:
            - chart_type: Type of chart ('bar', 'line', 'timeseries')
            - data: Chart data dictionary
            - style: Style name (default: 'default')
            - title: Panel title
            - xlabel, ylabel: Axis labels
            - row, col: Grid position (0-indexed)
            - colspan, rowspan: Grid span (default: 1)
        layout: Dashboard layout configuration dict:
            - rows: Number of grid rows (default: 1)
            - cols: Number of grid columns (default: 2)
            - figsize: Figure size as [width, height] (default: [16, 6])
            - shared_legend: Show shared legend (default: True)
            - legend_position: 'top', 'bottom', or 'right' (default: 'top')
            - width_ratios: Column width ratios (e.g., [2, 1])
            - height_ratios: Row height ratios
        theme: Theme name for all panels (default: 'plotly_dark')
        title: Dashboard title
        output_format: Output file format ('png', 'svg', 'pdf', 'jpeg')
        filename: Custom filename (without extension)
        dpi: DPI override for raster formats
        
    Returns:
        Path: Full path to the generated dashboard file
        
    Examples:
        Traffic and latency dashboard:
        >>> path = await generate_dashboard(
        ...     panels=[
        ...         {
        ...             "chart_type": "timeseries",
        ...             "data": {"dates": dates, "series": {...}},
        ...             "title": "Traffic Volume",
        ...             "col": 0,
        ...         },
        ...         {
        ...             "chart_type": "bar",
        ...             "data": {"labels": times, "values": latencies},
        ...             "title": "Latency (ms)",
        ...             "col": 1,
        ...         },
        ...     ],
        ...     layout={"cols": 2, "width_ratios": [2, 1]},
        ...     theme="plotly_dark",
        ...     title="System Dashboard",
        ... )
    """
    # Get settings
    settings = get_settings()
    
    # Resolve defaults
    resolved_format = output_format or settings.default_format
    
    # Parse panel configs
    panel_configs = [PanelConfig.from_dict(p) for p in panels]
    
    # Parse layout config
    layout_config = DashboardLayout.from_dict(layout)
    
    # Get theme
    dashboard_theme = get_theme(theme)
    
    # Create dashboard
    dashboard = DashboardChart(
        panels=panel_configs,
        layout=layout_config,
        theme=dashboard_theme,
        title=title,
    )
    
    # Render
    figure = await dashboard.render()
    
    # Save to file
    output_manager = get_output_manager()
    output_path = await output_manager.save_chart(
        figure=figure,
        chart_type="dashboard",
        output_format=resolved_format,
        filename=filename,
        dpi=dpi,
    )
    
    return output_path
