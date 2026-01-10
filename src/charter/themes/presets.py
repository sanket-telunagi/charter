"""
Built-in theme presets for Charter.

Available themes:
- default: Clean, professional look
- dark: Dark background with light elements
- light: Bright, minimal appearance
- minimal: Reduced visual elements
- vibrant: Bold, saturated colors
- plotly_dark: Plotly-inspired dark theme with bright colors

ECharts-inspired themes:
- westeros: Cool blues and purples
- wonderland: Greens and pinks
- chalk: Chalk-style on dark background
- essos: Warm reds and golds
- macarons: Soft pastel colors
- roma: Red and grey elegant style
- walden: Forest and lake tones
- purple_passion: Purple variations
- shine: Bright, glossy colors
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


# Plotly Dark theme - Inspired by Plotly's dark template
PLOTLY_DARK_THEME = Theme(
    name="plotly_dark",
    background_color="#111111",
    text_color="#F2F5FA",
    title_color="#FFFFFF",
    grid_color="#283442",
    axis_color="#506784",
    palette=[
        "#636EFA",  # Plotly Blue
        "#EF553B",  # Plotly Red
        "#00CC96",  # Plotly Green
        "#AB63FA",  # Plotly Purple
        "#FFA15A",  # Plotly Orange
        "#19D3F3",  # Plotly Cyan
        "#FF6692",  # Plotly Pink
        "#B6E880",  # Plotly Lime
        "#FF97FF",  # Plotly Magenta
        "#FECB52",  # Plotly Yellow
    ],
    font_family="sans-serif",
    title_font_size=16,
    label_font_size=12,
    tick_font_size=10,
    legend_font_size=10,
    line_width=2.0,
    grid_alpha=0.3,
    grid_style="solid",
    spine_visible=False,
)


# --- ECharts-Inspired Themes ---

# Westeros
WESTEROS_THEME = Theme(
    name="westeros",
    background_color="#FFFFFF",  # Usually light, sometimes transparent
    text_color="#333333",
    title_color="#516b91",
    grid_color="#cccccc",
    axis_color="#999999",
    palette=[
        "#516b91", "#59c4e6", "#edafda", "#93b7e3", 
        "#a5e7f0", "#cbb0e3"
    ],
    font_family="sans-serif",
    grid_alpha=0.5,
    spine_visible=False,
)

# Wonderland
WONDERLAND_THEME = Theme(
    name="wonderland",
    background_color="#FFFFFF",
    text_color="#4ea397",
    title_color="#4ea397",
    grid_color="#cccccc",
    axis_color="#999999",
    palette=[
        "#4ea397", "#22c3aa", "#7bd9a5", "#d0648a", 
        "#f58db2", "#f2b3c9"
    ],
    font_family="sans-serif",
    grid_alpha=0.5,
    spine_visible=False,
)

# Chalk
CHALK_THEME = Theme(
    name="chalk",
    background_color="#293441",
    text_color="#ffffff",
    title_color="#ffffff",
    grid_color="#455466",
    axis_color="#9aa8b8",
    palette=[
        "#fc97af", "#87f7cf", "#f7f494", "#72ccff", 
        "#f7c5a0", "#d4a4eb", "#d2f5a6", "#76f2f2"
    ],
    font_family="sans-serif",
    grid_alpha=0.3,
    grid_style="dotted",
    spine_visible=True,
)

# Essos
ESSOS_THEME = Theme(
    name="essos",
    background_color="#fdfcf5",  # Warm white
    text_color="#893448",
    title_color="#893448",
    grid_color="#f0e9d6",
    axis_color="#b08b92",
    palette=[
        "#893448", "#d95850", "#eb8146", "#ffb248", 
        "#f2d643", "#ebdba4"
    ],
    font_family="sans-serif",
    grid_alpha=0.5,
    spine_visible=False,
)

# Macarons
MACARONS_THEME = Theme(
    name="macarons",
    background_color="#FFFFFF",
    text_color="#59678c",
    title_color="#59678c",
    grid_color="#e6e6e6",
    axis_color="#999999",
    palette=[
        "#2ec7c9", "#b6a2de", "#5ab1ef", "#ffb980", 
        "#d87a80", "#8d98b3", "#e5cf0d", "#97b552", 
        "#95706d", "#dc69aa", "#07a2a4", "#9a7fd1"
    ],
    font_family="sans-serif",
    grid_alpha=0.5,
    spine_visible=False,
)

# Roma
ROMA_THEME = Theme(
    name="roma",
    background_color="#FFFFFF",
    text_color="#333333",
    title_color="#E01F54",
    grid_color="#cccccc",
    axis_color="#999999",
    palette=[
        "#E01F54", "#001852", "#f5e8c8", "#b8d2c7", 
        "#c6b38e", "#a4d8c2", "#f3d999", "#d3758f"
    ],
    font_family="sans-serif",
    grid_alpha=0.5,
    spine_visible=False,
)

# Walden
WALDEN_THEME = Theme(
    name="walden",
    background_color="#FFFFFF",
    text_color="#626c91",
    title_color="#626c91",
    grid_color="#e6e6e6",
    axis_color="#999999",
    palette=[
        "#3fb1e3", "#6be6c1", "#626c91", "#a0a7e6", 
        "#c4ebad", "#96dee8"
    ],
    font_family="sans-serif",
    grid_alpha=0.5,
    spine_visible=False,
)

# Purple Passion
PURPLE_PASSION_THEME = Theme(
    name="purple_passion",
    background_color="#5b5c6e",
    text_color="#ffffff",
    title_color="#ffffff",
    grid_color="#767789",
    axis_color="#cccccc",
    palette=[
        "#9b8bba", "#e098c7", "#8fd3e8", "#71669e", 
        "#cc70af", "#7cb4cc"
    ],
    font_family="sans-serif",
    grid_alpha=0.3,
    spine_visible=True,
)

# Shine
SHINE_THEME = Theme(
    name="shine",
    background_color="#FFFFFF",
    text_color="#333333",
    title_color="#c1232b",
    grid_color="#cccccc",
    axis_color="#999999",
    palette=[
        "#c1232b", "#27727b", "#fcce10", "#e87c25", 
        "#b5c334", "#fe8463", "#9bca63", "#fad860", 
        "#f3a43b", "#60c0dd", "#d7504b", "#c6e579"
    ],
    font_family="sans-serif",
    grid_alpha=0.5,
    spine_visible=False,
)


# Theme registry
_THEMES: dict[str, Theme] = {
    "default": DEFAULT_THEME,
    "dark": DARK_THEME,
    "light": LIGHT_THEME,
    "minimal": MINIMAL_THEME,
    "vibrant": VIBRANT_THEME,
    "plotly_dark": PLOTLY_DARK_THEME,
    
    # ECharts
    "westeros": WESTEROS_THEME,
    "wonderland": WONDERLAND_THEME,
    "chalk": CHALK_THEME,
    "essos": ESSOS_THEME,
    "macarons": MACARONS_THEME,
    "roma": ROMA_THEME,
    "walden": WALDEN_THEME,
    "purple_passion": PURPLE_PASSION_THEME,
    "shine": SHINE_THEME,
}

AVAILABLE_THEMES = list(_THEMES.keys())


def get_theme(name: str) -> Theme:
    """
    Get a theme by name.
    
    Args:
        name: Theme name (default, dark, light, minimal, vibrant, plotly_dark, etc.)
        
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
