"""
Data validation utilities for chart data.

Provides validation functions to ensure chart data meets
the expected format before rendering.
"""

from typing import Any, Sequence


class ChartDataError(ValueError):
    """Exception raised when chart data validation fails."""
    pass


def validate_chart_data(
    chart_type: str,
    data: dict[str, Any],
) -> dict[str, Any]:
    """
    Validate chart data based on chart type.
    
    Args:
        chart_type: Type of chart (bar, pie, line, timeseries)
        data: Chart data dictionary
        
    Returns:
        Validated data dictionary
        
    Raises:
        ChartDataError: If validation fails
    """
    validators = {
        "bar": validate_bar_data,
        "pie": validate_pie_data,
        "line": validate_line_data,
        "timeseries": validate_timeseries_data,
        "rose": validate_rose_data,
    }
    
    validator = validators.get(chart_type.lower())
    if validator is None:
        raise ChartDataError(f"Unknown chart type: {chart_type}")
    
    return validator(data)


def validate_bar_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    Validate bar chart data.
    
    Expected formats:
        Single series: {"labels": [...], "values": [...]}
        Multi series: {"labels": [...], "series": {"name": [...], ...}}
    """
    if not isinstance(data, dict):
        raise ChartDataError("Bar chart data must be a dictionary")
    
    # Check for labels
    labels = data.get("labels")
    if labels is None:
        raise ChartDataError("Bar chart requires 'labels' field")
    
    if not isinstance(labels, (list, tuple)):
        raise ChartDataError("'labels' must be a list or tuple")
    
    if len(labels) == 0:
        raise ChartDataError("'labels' cannot be empty")
    
    # Check for values or series
    if "values" in data:
        values = data["values"]
        if not isinstance(values, (list, tuple)):
            raise ChartDataError("'values' must be a list or tuple")
        if len(values) != len(labels):
            raise ChartDataError(
                f"'values' length ({len(values)}) must match 'labels' length ({len(labels)})"
            )
        _validate_numeric_sequence(values, "values")
        
    elif "series" in data:
        series = data["series"]
        if not isinstance(series, dict):
            raise ChartDataError("'series' must be a dictionary")
        
        for name, values in series.items():
            if not isinstance(values, (list, tuple)):
                raise ChartDataError(f"Series '{name}' values must be a list or tuple")
            if len(values) != len(labels):
                raise ChartDataError(
                    f"Series '{name}' length ({len(values)}) must match 'labels' length ({len(labels)})"
                )
            _validate_numeric_sequence(values, f"series['{name}']")
    else:
        raise ChartDataError("Bar chart requires either 'values' or 'series' field")
    
    return data


def validate_pie_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    Validate pie chart data.
    
    Expected formats:
        Basic: {"labels": [...], "values": [...]}
        With colors: {"labels": [...], "values": [...], "colors": [...]}
        With center title: {"labels": [...], "values": [...], "center_title": "..."}
        With subtitle: {"labels": [...], "values": [...], "subtitle": "..."}
        
    Notes:
        - Empty string labels ("") are allowed for gap slices in annotated style
        - Colors array is optional; if provided, must match values length
        - center_title and subtitle are optional string fields
    """
    if not isinstance(data, dict):
        raise ChartDataError("Pie chart data must be a dictionary")
    
    # Check for labels
    labels = data.get("labels")
    if labels is None:
        raise ChartDataError("Pie chart requires 'labels' field")
    
    if not isinstance(labels, (list, tuple)):
        raise ChartDataError("'labels' must be a list or tuple")
    
    if len(labels) == 0:
        raise ChartDataError("'labels' cannot be empty")
    
    # Check for values
    values = data.get("values")
    if values is None:
        raise ChartDataError("Pie chart requires 'values' field")
    
    if not isinstance(values, (list, tuple)):
        raise ChartDataError("'values' must be a list or tuple")
    
    if len(values) != len(labels):
        raise ChartDataError(
            f"'values' length ({len(values)}) must match 'labels' length ({len(labels)})"
        )
    
    _validate_numeric_sequence(values, "values")
    
    # All values must be non-negative for pie charts
    if any(v < 0 for v in values):
        raise ChartDataError("Pie chart values must be non-negative")
    
    # Validate optional colors array
    colors = data.get("colors")
    if colors is not None:
        if not isinstance(colors, (list, tuple)):
            raise ChartDataError("'colors' must be a list or tuple")
        if len(colors) != len(values):
            raise ChartDataError(
                f"'colors' length ({len(colors)}) must match 'values' length ({len(values)})"
            )
        # Validate each color is a string
        for i, color in enumerate(colors):
            if not isinstance(color, str):
                raise ChartDataError(
                    f"'colors[{i}]' must be a string, got {type(color).__name__}"
                )
    
    # Validate optional center_title
    center_title = data.get("center_title")
    if center_title is not None and not isinstance(center_title, str):
        raise ChartDataError("'center_title' must be a string")
    
    # Validate optional subtitle
    subtitle = data.get("subtitle")
    if subtitle is not None and not isinstance(subtitle, str):
        raise ChartDataError("'subtitle' must be a string")
    
    return data


def validate_line_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    Validate line chart data.
    
    Expected formats:
        With x values: {"x": [...], "y": [...]}
        With labels: {"labels": [...], "y": [...]}
        Multi series: {"x": [...], "series": {"name": [...], ...}}
    """
    if not isinstance(data, dict):
        raise ChartDataError("Line chart data must be a dictionary")
    
    # Get x values or labels
    if "labels" in data:
        x_len = len(data["labels"])
    elif "x" in data:
        x = data["x"]
        if not isinstance(x, (list, tuple)):
            raise ChartDataError("'x' must be a list or tuple")
        x_len = len(x)
        _validate_numeric_sequence(x, "x")
    else:
        raise ChartDataError("Line chart requires 'x' or 'labels' field")
    
    if x_len == 0:
        raise ChartDataError("X values cannot be empty")
    
    # Check for y or series
    if "y" in data:
        y = data["y"]
        if not isinstance(y, (list, tuple)):
            raise ChartDataError("'y' must be a list or tuple")
        if len(y) != x_len:
            raise ChartDataError(
                f"'y' length ({len(y)}) must match x length ({x_len})"
            )
        _validate_numeric_sequence(y, "y")
        
    elif "series" in data:
        series = data["series"]
        if not isinstance(series, dict):
            raise ChartDataError("'series' must be a dictionary")
        
        for name, y in series.items():
            if not isinstance(y, (list, tuple)):
                raise ChartDataError(f"Series '{name}' must be a list or tuple")
            if len(y) != x_len:
                raise ChartDataError(
                    f"Series '{name}' length ({len(y)}) must match x length ({x_len})"
                )
            _validate_numeric_sequence(y, f"series['{name}']")
    else:
        raise ChartDataError("Line chart requires 'y' or 'series' field")
    
    return data


def validate_timeseries_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    Validate time series chart data.
    
    Expected formats:
        Basic: {"dates": [...], "values": [...]}
        With bands: {"dates": [...], "values": [...], "upper": [...], "lower": [...]}
        Multi series: {"dates": [...], "series": {"name": [...], ...}}
    """
    if not isinstance(data, dict):
        raise ChartDataError("Time series data must be a dictionary")
    
    # Check for dates
    dates = data.get("dates")
    if dates is None:
        raise ChartDataError("Time series requires 'dates' field")
    
    if not isinstance(dates, (list, tuple)):
        raise ChartDataError("'dates' must be a list or tuple")
    
    if len(dates) == 0:
        raise ChartDataError("'dates' cannot be empty")
    
    dates_len = len(dates)
    
    # Check for values or series
    if "values" in data:
        values = data["values"]
        if not isinstance(values, (list, tuple)):
            raise ChartDataError("'values' must be a list or tuple")
        if len(values) != dates_len:
            raise ChartDataError(
                f"'values' length ({len(values)}) must match 'dates' length ({dates_len})"
            )
        _validate_numeric_sequence(values, "values")
        
        # Check optional bounds
        if "upper" in data:
            upper = data["upper"]
            if len(upper) != dates_len:
                raise ChartDataError(
                    f"'upper' length ({len(upper)}) must match 'dates' length ({dates_len})"
                )
            _validate_numeric_sequence(upper, "upper")
            
        if "lower" in data:
            lower = data["lower"]
            if len(lower) != dates_len:
                raise ChartDataError(
                    f"'lower' length ({len(lower)}) must match 'dates' length ({dates_len})"
                )
            _validate_numeric_sequence(lower, "lower")
            
    elif "series" in data:
        series = data["series"]
        if not isinstance(series, dict):
            raise ChartDataError("'series' must be a dictionary")
        
        for name, values in series.items():
            if not isinstance(values, (list, tuple)):
                raise ChartDataError(f"Series '{name}' must be a list or tuple")
            if len(values) != dates_len:
                raise ChartDataError(
                    f"Series '{name}' length ({len(values)}) must match 'dates' length ({dates_len})"
                )
            _validate_numeric_sequence(values, f"series['{name}']")
    else:
        raise ChartDataError("Time series requires 'values' or 'series' field")
    
    return data


def validate_rose_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    Validate rose chart data.
    
    Expected formats:
        Basic: {"labels": [...], "values": [...]}
    """
    if not isinstance(data, dict):
        raise ChartDataError("Rose chart data must be a dictionary")
    
    # Check for labels
    labels = data.get("labels")
    if labels is None:
        raise ChartDataError("Rose chart requires 'labels' field")
    
    if not isinstance(labels, (list, tuple)):
        raise ChartDataError("'labels' must be a list or tuple")
    
    if len(labels) == 0:
        raise ChartDataError("'labels' cannot be empty")
    
    # Check for values
    values = data.get("values")
    if values is None:
        raise ChartDataError("Rose chart requires 'values' field")
    
    if not isinstance(values, (list, tuple)):
        raise ChartDataError("'values' must be a list or tuple")
    
    if len(values) != len(labels):
        raise ChartDataError(
            f"'values' length ({len(values)}) must match 'labels' length ({len(labels)})"
        )
    
    _validate_numeric_sequence(values, "values")
    
    # All values must be non-negative for rose charts
    if any(v < 0 for v in values):
        raise ChartDataError("Rose chart values must be non-negative")
    
    return data


def _validate_numeric_sequence(seq: Sequence, name: str) -> None:
    """Validate that a sequence contains only numeric values."""
    for i, val in enumerate(seq):
        if not isinstance(val, (int, float)):
            raise ChartDataError(
                f"'{name}[{i}]' must be numeric, got {type(val).__name__}"
            )

