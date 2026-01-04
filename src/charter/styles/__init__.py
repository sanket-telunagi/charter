"""Styles module for Charter."""

from charter.styles.registry import StyleRegistry, get_style_registry
from charter.styles.presets import Style
from charter.styles.dashboard import (
    PanelConfig,
    DashboardLayout,
    DASHBOARD_LAYOUTS,
    get_dashboard_layout,
)

__all__ = [
    "StyleRegistry",
    "get_style_registry",
    "Style",
    "PanelConfig",
    "DashboardLayout",
    "DASHBOARD_LAYOUTS",
    "get_dashboard_layout",
]

