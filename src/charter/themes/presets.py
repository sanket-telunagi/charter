"""
Built-in theme presets for Charter.

Available themes:
- default: Clean, professional look
- dark: Dark background with light elements
- light: Bright, minimal appearance
- minimal: Reduced visual elements
- vibrant: Bold, saturated colors
"""

from charter.themes.base import Theme


# Default theme - Clean and professional
DEFAULT_THEME = Theme(
    name="default",
    background_color="#FFFFFF",
    text_color="#333333",
    title_color="#1a1a1a",
    grid_color="#E5E5E5",
    axis_color="#666666",
    palette=[
        "#4C72B0",  # Steel Blue
        "#55A868",  # Sage Green
        "#C44E52",  # Salmon Red
        "#8172B3",  # Lavender Purple
        "#CCB974",  # Goldenrod
        "#64B5CD",  # Sky Blue
        "#E377C2",  # Orchid Pink
        "#7F7F7F",  # Medium Gray
    ],
    font_family="sans-serif",
    grid_alpha=0.6,
    grid_style="dashed",
)


# Dark theme - For dark backgrounds
DARK_THEME = Theme(
    name="dark",
    background_color="#1E1E1E",
    text_color="#E0E0E0",
    title_color="#FFFFFF",
    grid_color="#3D3D3D",
    axis_color="#808080",
    palette=[
        "#5DA5DA",  # Bright Blue
        "#60BD68",  # Lime Green
        "#F15854",  # Bright Red
        "#B276B2",  # Bright Purple
        "#DECF3F",  # Yellow
        "#4DC4FF",  # Electric Blue
        "#F17CB0",  # Hot Pink
        "#B2B2B2",  # Light Gray
    ],
    font_family="sans-serif",
    grid_alpha=0.4,
    grid_style="dotted",
)


# Light theme - Bright and clean
LIGHT_THEME = Theme(
    name="light",
    background_color="#FAFAFA",
    text_color="#424242",
    title_color="#212121",
    grid_color="#EEEEEE",
    axis_color="#9E9E9E",
    palette=[
        "#1976D2",  # Material Blue
        "#388E3C",  # Material Green
        "#D32F2F",  # Material Red
        "#7B1FA2",  # Material Purple
        "#FFA000",  # Material Amber
        "#0097A7",  # Material Cyan
        "#C2185B",  # Material Pink
        "#616161",  # Material Gray
    ],
    font_family="sans-serif",
    grid_alpha=0.5,
    grid_style="solid",
    spine_visible=False,
)


# Minimal theme - Focus on data
MINIMAL_THEME = Theme(
    name="minimal",
    background_color="#FFFFFF",
    text_color="#555555",
    title_color="#333333",
    grid_color="#F0F0F0",
    axis_color="#CCCCCC",
    palette=[
        "#2E86AB",  # Ocean Blue
        "#A23B72",  # Berry
        "#F18F01",  # Orange
        "#C73E1D",  # Vermilion
        "#3B1F2B",  # Dark Purple
        "#44AF69",  # Green
        "#6E7E85",  # Slate
        "#B8D4E3",  # Powder Blue
    ],
    font_family="sans-serif",
    title_font_size=12,
    label_font_size=10,
    tick_font_size=9,
    legend_font_size=9,
    line_width=1.5,
    grid_alpha=0.3,
    grid_style="solid",
    spine_visible=False,
)


# Vibrant theme - Bold and colorful
VIBRANT_THEME = Theme(
    name="vibrant",
    background_color="#FFFFFF",
    text_color="#2C3E50",
    title_color="#1A252F",
    grid_color="#ECF0F1",
    axis_color="#7F8C8D",
    palette=[
        "#E74C3C",  # Alizarin Red
        "#3498DB",  # Peter River Blue
        "#2ECC71",  # Emerald Green
        "#9B59B6",  # Amethyst Purple
        "#F39C12",  # Sunflower Yellow
        "#1ABC9C",  # Turquoise
        "#E91E63",  # Pink
        "#00BCD4",  # Cyan
    ],
    font_family="sans-serif",
    title_font_size=16,
    line_width=2.5,
    grid_alpha=0.4,
    grid_style="dashed",
)


# Theme registry
_THEMES: dict[str, Theme] = {
    "default": DEFAULT_THEME,
    "dark": DARK_THEME,
    "light": LIGHT_THEME,
    "minimal": MINIMAL_THEME,
    "vibrant": VIBRANT_THEME,
}

AVAILABLE_THEMES = list(_THEMES.keys())


def get_theme(name: str) -> Theme:
    """
    Get a theme by name.
    
    Args:
        name: Theme name (default, dark, light, minimal, vibrant)
        
    Returns:
        Theme: The requested theme
        
    Raises:
        ValueError: If theme name is not recognized
    """
    theme = _THEMES.get(name.lower())
    if theme is None:
        available = ", ".join(AVAILABLE_THEMES)
        raise ValueError(f"Unknown theme '{name}'. Available themes: {available}")
    return theme


def register_theme(theme: Theme) -> None:
    """
    Register a custom theme.
    
    Args:
        theme: Theme instance to register
    """
    _THEMES[theme.name] = theme
    if theme.name not in AVAILABLE_THEMES:
        AVAILABLE_THEMES.append(theme.name)

