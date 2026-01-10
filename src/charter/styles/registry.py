"""
Style registry for managing and retrieving chart styles.
"""

from functools import lru_cache
from typing import TypeVar

from charter.styles.presets import (
    Style,
    ChartType,
    BarStyle,
    PieStyle,
    LineStyle,
    TimeSeriesStyle,
    RoseStyle,
    BAR_STYLES,
    PIE_STYLES,
    LINE_STYLES,
    TIMESERIES_STYLES,
    ROSE_STYLES,
)


T = TypeVar("T", bound=Style)


class StyleRegistry:
    """
    Registry for managing chart styles.
    
    Provides methods to retrieve, register, and list available styles
    for each chart type.
    """

    def __init__(self) -> None:
        """Initialize the style registry with default styles."""
        self._styles: dict[ChartType, dict[str, Style]] = {
            ChartType.BAR: dict(BAR_STYLES),
            ChartType.PIE: dict(PIE_STYLES),
            ChartType.LINE: dict(LINE_STYLES),
            ChartType.TIMESERIES: dict(TIMESERIES_STYLES),
            ChartType.ROSE: dict(ROSE_STYLES),
        }

    def get_style(self, chart_type: ChartType | str, name: str = "default") -> Style:
        """
        Get a style by chart type and name.
        
        Args:
            chart_type: The chart type (bar, pie, line, timeseries)
            name: Style name (default if not specified)
            
        Returns:
            Style: The requested style configuration
            
        Raises:
            ValueError: If chart type or style name is not found
        """
        if isinstance(chart_type, str):
            try:
                chart_type = ChartType(chart_type.lower())
            except ValueError:
                available = [ct.value for ct in ChartType]
                raise ValueError(
                    f"Unknown chart type '{chart_type}'. Available: {', '.join(available)}"
                )

        styles = self._styles.get(chart_type)
        if styles is None:
            raise ValueError(f"No styles registered for chart type '{chart_type}'")

        style = styles.get(name.lower())
        if style is None:
            available = list(styles.keys())
            raise ValueError(
                f"Unknown style '{name}' for {chart_type.value} chart. "
                f"Available: {', '.join(available)}"
            )

        return style

    def get_bar_style(self, name: str = "default") -> BarStyle:
        """Get a bar chart style."""
        style = self.get_style(ChartType.BAR, name)
        assert isinstance(style, BarStyle)
        return style

    def get_pie_style(self, name: str = "default") -> PieStyle:
        """Get a pie chart style."""
        style = self.get_style(ChartType.PIE, name)
        assert isinstance(style, PieStyle)
        return style

    def get_line_style(self, name: str = "default") -> LineStyle:
        """Get a line chart style."""
        style = self.get_style(ChartType.LINE, name)
        assert isinstance(style, LineStyle)
        return style

    def get_timeseries_style(self, name: str = "default") -> TimeSeriesStyle:
        """Get a time series chart style."""
        style = self.get_style(ChartType.TIMESERIES, name)
        assert isinstance(style, TimeSeriesStyle)
        return style

    def get_rose_style(self, name: str = "default") -> RoseStyle:
        """Get a rose chart style."""
        style = self.get_style(ChartType.ROSE, name)
        assert isinstance(style, RoseStyle)
        return style

    def register_style(self, style: Style) -> None:
        """
        Register a custom style.
        
        Args:
            style: Style instance to register
        """
        chart_type = style.chart_type
        if chart_type not in self._styles:
            self._styles[chart_type] = {}
        self._styles[chart_type][style.name] = style

    def list_styles(self, chart_type: ChartType | str | None = None) -> dict[str, list[str]]:
        """
        List available styles.
        
        Args:
            chart_type: Optional chart type to filter by
            
        Returns:
            Dictionary mapping chart types to available style names
        """
        if chart_type is not None:
            if isinstance(chart_type, str):
                chart_type = ChartType(chart_type.lower())
            styles = self._styles.get(chart_type, {})
            return {chart_type.value: list(styles.keys())}

        return {
            ct.value: list(styles.keys())
            for ct, styles in self._styles.items()
        }


# Module-level singleton
_registry: StyleRegistry | None = None


@lru_cache
def get_style_registry() -> StyleRegistry:
    """
    Get the global style registry instance.
    
    Returns:
        StyleRegistry: The singleton registry instance
    """
    global _registry
    if _registry is None:
        _registry = StyleRegistry()
    return _registry

