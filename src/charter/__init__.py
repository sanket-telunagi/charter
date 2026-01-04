"""
Charter - A modular, async-first Python charting library.

This library provides a simple, unified API for generating various chart types
with customizable styles and themes. Charts are rendered using Matplotlib and
saved to configurable output formats.

Basic Usage:
    from charter import generate_chart
    import asyncio
    
    async def main():
        path = await generate_chart(
            chart_type="bar",
            data={"labels": ["A", "B", "C"], "values": [10, 20, 15]},
            style="default",
            theme="dark",
            output_format="png"
        )
        print(f"Chart saved to: {path}")
    
    asyncio.run(main())

Available Chart Types:
    - bar: Bar charts (vertical, horizontal, grouped, stacked)
    - pie: Pie charts (standard, donut, exploded)
    - line: Line charts (standard, smooth, stepped, area)
    - timeseries: Time series charts with date handling

Available Themes:
    - default: Clean, professional look
    - dark: Dark background with light elements
    - light: Bright, minimal appearance
    - minimal: Reduced visual elements
    - vibrant: Bold, saturated colors

Configuration:
    Set environment variables with CHARTER_ prefix or create a .env file.
    See .env.example for available options.
"""

# Set non-interactive backend BEFORE any matplotlib imports (fixes thread-safety with asyncio)
import matplotlib
matplotlib.use("Agg")

from charter.api import (
    generate_chart,
    generate_bar_chart,
    generate_pie_chart,
    generate_line_chart,
    generate_timeseries_chart,
    generate_dashboard,
)
from charter.config.settings import get_settings, reload_settings, ChartSettings
from charter.themes.presets import get_theme, AVAILABLE_THEMES, register_theme
from charter.themes.base import Theme
from charter.styles.registry import get_style_registry
from charter.styles.presets import (
    Style,
    BarStyle,
    PieStyle,
    LineStyle,
    TimeSeriesStyle,
    ChartType,
)
from charter.styles.dashboard import (
    PanelConfig,
    DashboardLayout,
    DASHBOARD_LAYOUTS,
    get_dashboard_layout,
)
from charter.utils.validators import validate_chart_data, ChartDataError
from charter.utils.downsampling import lttb_downsample, simple_downsample, minmax_downsample

__version__ = "0.1.0"

__all__ = [
    # Main API
    "generate_chart",
    "generate_bar_chart",
    "generate_pie_chart",
    "generate_line_chart",
    "generate_timeseries_chart",
    "generate_dashboard",
    # Configuration
    "get_settings",
    "reload_settings",
    "ChartSettings",
    # Themes
    "get_theme",
    "register_theme",
    "AVAILABLE_THEMES",
    "Theme",
    # Styles
    "get_style_registry",
    "Style",
    "BarStyle",
    "PieStyle",
    "LineStyle",
    "TimeSeriesStyle",
    "ChartType",
    # Dashboard
    "PanelConfig",
    "DashboardLayout",
    "DASHBOARD_LAYOUTS",
    "get_dashboard_layout",
    # Validation
    "validate_chart_data",
    "ChartDataError",
    # Downsampling utilities
    "lttb_downsample",
    "simple_downsample",
    "minmax_downsample",
    # Version
    "__version__",
]
