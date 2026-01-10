# Charter

A modular, async-first Python charting library built on matplotlib. Generate beautiful, customizable charts with a simple, unified API.

## Features

- **Async-first design** - Non-blocking chart generation using `asyncio`
- **Multiple chart types** - Bar, Pie, Line, Time Series, and Nightingale Rose charts
- **Customizable themes** - 15 built-in themes including ECharts-inspired palettes
- **Style presets** - Pre-configured styles for each chart type
- **Multiple output formats** - PNG, SVG, PDF, JPEG
- **Environment configuration** - Configure via environment variables or `.env` file
- **CLI and library usage** - Use standalone or integrate into your projects

## Installation

### Requirements

- Python 3.12+
- matplotlib >= 3.8.0
- pydantic >= 2.0.0
- pydantic-settings >= 2.0.0
- numpy >= 1.26.0

### Install from source

```bash
# Clone the repository
git clone <repository-url>
cd charter

# Install with pip
pip install -e .

# Or with uv
uv pip install -e .
```

### Install dependencies only

```bash
pip install matplotlib pydantic pydantic-settings numpy
```

## Quick Start

### As a Library

```python
import asyncio
from charter import generate_chart

async def main():
    # Generate a simple bar chart
    path = await generate_chart(
        chart_type="bar",
        data={
            "labels": ["January", "February", "March", "April"],
            "values": [65, 59, 80, 81],
        },
        title="Monthly Sales",
        theme="default",
    )
    print(f"Chart saved to: {path}")

asyncio.run(main())
```

### Standalone CLI

```bash
# Run the demo (generates sample charts)
python main.py

# Generate a specific chart
python main.py bar --data '{"labels": ["A", "B", "C"], "values": [10, 20, 15]}'

# With options
python main.py pie --data '{"labels": ["X", "Y"], "values": [60, 40]}' --style donut --theme dark

# Generate a Nightingale Rose chart with Westeros theme
python main.py rose --data '{"labels": ["A", "B", "C", "D"], "values": [10, 20, 30, 40]}' --theme westeros

# List available themes and styles
python main.py list
```

---

## Chart Types

### Bar Charts

Bar charts support single series and multi-series (grouped/stacked) data.

#### Single Series

```python
await generate_chart(
    chart_type="bar",
    data={
        "labels": ["Q1", "Q2", "Q3", "Q4"],
        "values": [100, 150, 120, 180],
    },
    title="Quarterly Revenue",
    xlabel="Quarter",
    ylabel="Revenue ($K)",
)
```

#### Multi-Series (Grouped)

```python
await generate_chart(
    chart_type="bar",
    data={
        "labels": ["Q1", "Q2", "Q3", "Q4"],
        "series": {
            "2023": [100, 150, 120, 180],
            "2024": [120, 160, 140, 200],
        },
    },
    style="grouped",
    title="Year over Year Comparison",
)
```

#### Bar Styles

| Style | Description |
|-------|-------------|
| `default` | Standard vertical bars |
| `grouped` | Side-by-side grouped bars for multi-series |
| `stacked` | Stacked bars for multi-series |
| `horizontal` | Horizontal bar orientation |
| `outlined` | Bars with visible borders |
| `labeled` | Shows value labels on bars |

---

### Pie Charts

Pie charts support standard, donut, exploded, and infographic styles.

#### Basic Pie Chart

```python
await generate_chart(
    chart_type="pie",
    data={
        "labels": ["Desktop", "Mobile", "Tablet"],
        "values": [45, 35, 20],
    },
    title="Traffic by Device",
)
```

#### Donut Chart

```python
await generate_chart(
    chart_type="pie",
    data={
        "labels": ["Completed", "In Progress", "Pending"],
        "values": [60, 25, 15],
    },
    style="donut",
    title="Task Status",
)
```

#### Infographic Style (External Labels)

```python
await generate_chart(
    chart_type="pie",
    data={
        "labels": ["USA", "EU", "China", "Others"],
        "values": [22, 15, 18, 45],
        "subtitle": "Global market share by region",
    },
    style="infographic",
    title="MARKET SHARE",
)
```

#### Annotated Style (Custom Colors, Gaps, Center Title)

```python
await generate_chart(
    chart_type="pie",
    data={
        "labels": ["USA, 22%", "EU, 15%", "", "China, 18%"],  # Empty = gap
        "values": [22, 15, 2, 18],
        "colors": ["#76aab8", "#76aab8", "#ffffff", "#e0bb5b"],  # Per-slice colors
        "center_title": "GLOBAL\nSHARE",  # Center text for donut
    },
    style="annotated",
)
```

#### Table Legend Style (Side Legend with Values)

Displays the pie/donut chart on the left with a compact, bordered table legend on the right showing color indicators, labels, values, and percentages.

**Visual Layout:**

```
+---------------------------+-------------------------------------------+
|                           | +-------+----------+-------+---------+   |
|                           | | [*]   | Desktop  |    42 |  42.0%  |   |
|       PIE / DONUT         | |-------|----------|-------|---------|   |
|                           | | [*]   | Mobile   |    35 |  35.0%  |   |
|      (center title        | |-------|----------|-------|---------|   |
|       for donut)          | | [*]   | Tablet   |    18 |  18.0%  |   |
|                           | |-------|----------|-------|---------|   |
|                           | | [*]   | Other    |     5 |   5.0%  |   |
|                           | +-------+----------+-------+---------+   |
+---------------------------+-------------------------------------------+
```

**Features:**
- Visible outer border and row/column separators
- Compact, centered table layout
- Color indicator squares with borders
- Configurable columns (value, percentage)
- Center title with background box for donut variant

```python
# Regular pie with table legend
await generate_chart(
    chart_type="pie",
    data={
        "labels": ["Desktop", "Mobile", "Tablet", "Other"],
        "values": [42, 35, 18, 5],
    },
    style="table_legend",
    title="Traffic by Device",
)

# Donut with center title and table legend
await generate_chart(
    chart_type="pie",
    data={
        "labels": ["Desktop", "Mobile", "Tablet", "Other"],
        "values": [42, 35, 18, 5],
    },
    style="table_legend_donut",
    title="Device Share",  # Shows in center of donut with background box
)
```

**Configuration Options:**

| Option | Values | Description |
|--------|--------|-------------|
| `table_legend_position` | `"right"`, `"left"`, `"bottom"` | Position of table legend |
| `table_legend_show_value` | `True`, `False` | Show/hide value column |
| `table_legend_show_percent` | `True`, `False` | Show/hide percentage column |
| `table_legend_header` | `True`, `False` | Show/hide column headers |

#### Pie Styles

| Style | Description |
|-------|-------------|
| `default` | Standard pie with labels and percentages |
| `donut` | Ring chart with hole in center |
| `exploded` | Slices separated from center |
| `minimal` | Labels only, no percentages |
| `detailed` | Both labels and percentages |
| `shadow` | Subtle shadow effect |
| `infographic` | External labels with leader lines |
| `annotated` | Annotation-based labels with rounded boxes, custom colors, gaps, center title |
| `transparent_donut` | Donut with transparent background and center title with rounded box |
| `table_legend` | Pie chart with centered table legend on the side showing labels, values, and percentages |
| `table_legend_donut` | Donut chart with center title (with background box) and centered table legend on the side |

---

### Nightingale Rose Charts

Nightingale Rose charts (Coxcomb charts) are polar charts where each sector has the same angle but different radius.

#### Basic Rose Chart

```python
await generate_chart(
    chart_type="rose",
    data={
        "labels": ["A", "B", "C", "D", "E"],
        "values": [10, 20, 30, 40, 50],
    },
    theme="westeros",
    title="Rose Chart",
)
```

#### Area Style (Square Root Scale)

Use `style="area"` to make the area proportional to the value (radius proportional to square root of value), which is often perceptually more accurate.

```python
await generate_chart(
    chart_type="rose",
    data={
        "labels": ["A", "B", "C", "D"],
        "values": [10, 20, 30, 40],
    },
    style="area",
    theme="wonderland",
)
```

#### Rose Styles

| Style | Description |
|-------|-------------|
| `default` | Standard radius-based rose chart (radius ~ value) |
| `radius` | Same as default |
| `area` | Area-based rose chart (area ~ value, radius ~ sqrt(value)) |

---

### Line Charts

Line charts support single and multi-series data with various styling options.

#### Basic Line Chart

```python
await generate_chart(
    chart_type="line",
    data={
        "x": [1, 2, 3, 4, 5],
        "y": [10, 15, 13, 17, 20],
    },
    title="Growth Trend",
    xlabel="Period",
    ylabel="Value",
)
```

#### Multi-Series with Labels

```python
await generate_chart(
    chart_type="line",
    data={
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "series": {
            "This Week": [150, 180, 165, 195, 210],
            "Last Week": [140, 165, 155, 175, 190],
        },
    },
    style="smooth",
    title="Daily Active Users",
)
```

#### Area Chart

```python
await generate_chart(
    chart_type="line",
    data={
        "x": [1, 2, 3, 4, 5],
        "y": [10, 15, 13, 17, 20],
    },
    style="area",
    title="Filled Area Chart",
)
```

#### Line Styles

| Style | Description |
|-------|-------------|
| `default` | Standard line |
| `smooth` | Spline-interpolated smooth curves |
| `stepped` | Step function (horizontal-vertical) |
| `area` | Filled area under the line |
| `dotted` | Dotted line with markers |
| `dashed` | Dashed line |
| `markers` | Line with data point markers |

---

### Time Series Charts

Specialized for date-based data with trend lines and range bands.

#### Basic Time Series

```python
await generate_chart(
    chart_type="timeseries",
    data={
        "dates": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
        "values": [100, 105, 102, 110],
    },
    title="Stock Price",
    xlabel="Date",
    ylabel="Price ($)",
)
```

#### With Trend Line

```python
await generate_chart(
    chart_type="timeseries",
    data={
        "dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "values": [100, 105, 110],
    },
    style="trend",
    title="Price with Trend",
)
```

#### Time Series Styles

| Style | Description |
|-------|-------------|
| `default` | Standard time series with grid |
| `area` | Filled area under the line |
| `trend` | Shows linear trend line |
| `range` | Shows confidence/range bands |
| `minimal` | No grid lines |

---

## Data Formats

### Bar Chart Data

```python
# Single series
{
    "labels": ["A", "B", "C"],
    "values": [10, 20, 15]
}

# Multi-series
{
    "labels": ["Q1", "Q2", "Q3"],
    "series": {
        "Product A": [100, 120, 140],
        "Product B": [80, 90, 110]
    }
}
```

### Pie Chart Data

```python
# Basic
{
    "labels": ["Category A", "Category B", "Category C"],
    "values": [30, 45, 25]
}

# With subtitle (for infographic style)
{
    "labels": ["Category A", "Category B"],
    "values": [60, 40],
    "subtitle": "Distribution overview"
}

# With custom colors and center title (for annotated style)
{
    "labels": ["Label A", "Label B", ""],  # Empty string = gap slice
    "values": [50, 40, 10],
    "colors": ["#ff0000", "#00ff00", "#ffffff"],  # Optional per-slice colors
    "center_title": "CENTER\nTEXT"  # Optional center text for donut
}
```

### Rose Chart Data

```python
# Same as basic pie chart data
{
    "labels": ["A", "B", "C", "D"],
    "values": [10, 20, 30, 40]
}
```

### Line Chart Data

```python
# With numeric x values
{
    "x": [1, 2, 3, 4, 5],
    "y": [10, 20, 15, 25, 30]
}

# With string labels
{
    "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "y": [10, 20, 15, 25, 30]
}

# Multi-series
{
    "labels": ["Mon", "Tue", "Wed"],
    "series": {
        "Series A": [10, 20, 15],
        "Series B": [15, 18, 22]
    }
}
```

### Time Series Data

```python
# Basic
{
    "dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
    "values": [100, 105, 102]
}

# With range bands
{
    "dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
    "values": [100, 105, 102],
    "upper": [110, 115, 112],
    "lower": [90, 95, 92]
}

# Multi-series
{
    "dates": ["2024-01-01", "2024-01-02"],
    "series": {
        "Stock A": [100, 105],
        "Stock B": [50, 52]
    }
}
```

---

## Themes

Charter includes 15 built-in themes, including many inspired by ECharts:

### Base Themes

| Theme | Description |
|-------|-------------|
| `default` | Clean, professional look with blue-green palette |
| `dark` | Dark background (#1E1E1E) with bright colors |
| `light` | Bright, minimal appearance with Material colors |
| `minimal` | Reduced visual elements, focus on data |
| `vibrant` | Bold, saturated colors for impact |
| `plotly_dark` | Plotly-inspired dark theme |

### ECharts-Inspired Themes

| Theme | Description |
|-------|-------------|
| `westeros` | Cool blues and purples, elegant feel |
| `wonderland` | Fresh greens and pinks |
| `chalk` | Chalk-style graphics on dark slate background |
| `essos` | Warm reds and golds, creamy background |
| `macarons` | Soft pastel colors, playful |
| `roma` | Sophisticated red and grey palette |
| `walden` | Forest and lake tones, calming |
| `purple_passion` | Deep purple variations on dark background |
| `shine` | Bright, glossy reds and yellows |

### Using Themes

```python
await generate_chart(
    chart_type="bar",
    data={"labels": ["A", "B"], "values": [10, 20]},
    theme="westeros",  # Use westeros theme
)
```

### Custom Themes

```python
from charter import Theme, register_theme

# Create a custom theme
my_theme = Theme(
    name="corporate",
    background_color="#F5F5F5",
    text_color="#333333",
    title_color="#1a1a1a",
    grid_color="#E0E0E0",
    axis_color="#666666",
    palette=[
        "#003366",  # Corporate blue
        "#CC0000",  # Corporate red
        "#339933",  # Corporate green
        "#FF9900",  # Corporate orange
    ],
    font_family="Arial",
    title_font_size=16,
    label_font_size=12,
)

# Register it
register_theme(my_theme)

# Use it
await generate_chart(..., theme="corporate")
```

### Theme Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `name` | str | - | Unique theme identifier |
| `background_color` | str | "#FFFFFF" | Chart background color |
| `text_color` | str | "#333333" | Primary text color |
| `title_color` | str | "#1a1a1a" | Chart title color |
| `grid_color` | str | "#E0E0E0" | Grid line color |
| `axis_color` | str | "#666666" | Axis line color |
| `palette` | list[str] | [...] | Colors for data series |
| `font_family` | str | "sans-serif" | Font family |
| `title_font_size` | int | 14 | Title font size |
| `label_font_size` | int | 12 | Axis label font size |
| `tick_font_size` | int | 10 | Tick label font size |
| `legend_font_size` | int | 10 | Legend text font size |
| `line_width` | float | 2.0 | Default line width |
| `grid_alpha` | float | 0.7 | Grid transparency (0-1) |
| `grid_style` | str | "dashed" | Grid style: solid, dashed, dotted |
| `spine_visible` | bool | True | Show axis spines |
| `figsize` | tuple | (10.0, 6.0) | Default figure size (width, height) |
| `dpi` | int | 150 | Default DPI |

---

## Configuration

### Environment Variables

All settings can be configured via environment variables with the `CHARTER_` prefix:

| Variable | Default | Description |
|----------|---------|-------------|
| `CHARTER_OUTPUT_DIR` | `output` | Output directory for charts |
| `CHARTER_DEFAULT_FORMAT` | `png` | Default output format (png, svg, pdf, jpeg) |
| `CHARTER_DEFAULT_THEME` | `default` | Default theme name |
| `CHARTER_DEFAULT_STYLE` | `default` | Default style name |
| `CHARTER_DEFAULT_DPI` | `150` | Default DPI for raster outputs |
| `CHARTER_DEFAULT_FIGSIZE_STR` | `10.0,6.0` | Default figure size (width,height) |
| `CHARTER_INCLUDE_TIMESTAMP` | `true` | Include timestamp in filenames |
| `CHARTER_INCLUDE_RANDOM_SUFFIX` | `true` | Include random suffix in filenames |

### Using a .env File

Create a `.env` file in your project root:

```env
CHARTER_OUTPUT_DIR=./charts
CHARTER_DEFAULT_FORMAT=svg
CHARTER_DEFAULT_THEME=dark
CHARTER_DEFAULT_DPI=300
CHARTER_DEFAULT_FIGSIZE_STR=12.0,8.0
```

### Programmatic Configuration

```python
from charter import get_settings, reload_settings
import os

# Read current settings
settings = get_settings()
print(f"Output directory: {settings.output_dir}")
print(f"Default theme: {settings.default_theme}")

# Change settings via environment and reload
os.environ["CHARTER_DEFAULT_THEME"] = "dark"
settings = reload_settings()
```

---

## API Reference

### Main Functions

#### `generate_chart()`

```python
async def generate_chart(
    chart_type: str,           # "bar", "pie", "line", "timeseries", "rose"
    data: dict,                # Chart data (format depends on chart type)
    style: str = "default",    # Style preset name
    theme: str = None,         # Theme name (uses default if None)
    output_format: str = None, # "png", "svg", "pdf", "jpeg"
    filename: str = None,      # Custom filename (without extension)
    title: str = None,         # Chart title
    xlabel: str = None,        # X-axis label
    ylabel: str = None,        # Y-axis label
    dpi: int = None,           # DPI override for raster formats
) -> Path:
    """Generate a chart and save it to the output directory."""
```

#### Convenience Functions

```python
# Type-specific convenience functions
await generate_bar_chart(data, style, theme, ...)
await generate_pie_chart(data, style, theme, ...)
await generate_line_chart(data, style, theme, ...)
await generate_timeseries_chart(data, style, theme, ...)
await generate_rose_chart(data, style, theme, ...)
```

### Imports

```python
# Main API
from charter import generate_chart
from charter import generate_bar_chart, generate_pie_chart
from charter import generate_line_chart, generate_timeseries_chart
from charter import generate_rose_chart

# Configuration
from charter import get_settings, reload_settings, ChartSettings

# Themes
from charter import get_theme, register_theme, AVAILABLE_THEMES, Theme

# Styles
from charter import get_style_registry
from charter import Style, BarStyle, PieStyle, LineStyle, TimeSeriesStyle, RoseStyle

# Validation
from charter import validate_chart_data, ChartDataError
```

---

## CLI Reference

```
usage: main.py [-h] {bar,pie,line,timeseries,rose,list} ...

Charter - Generate beautiful charts from the command line

positional arguments:
  {bar,pie,line,timeseries,rose,list}
    bar                 Generate a bar chart
    pie                 Generate a pie chart
    line                Generate a line chart
    timeseries          Generate a time series chart
    rose                Generate a Nightingale rose chart
    list                List available themes and styles

optional arguments:
  -h, --help            Show help message
```

### Chart Generation Options

```
--data, -d        Chart data as JSON string (required)
--style, -s       Chart style (default: default)
--theme, -t       Chart theme (default: default)
--format, -f      Output format: png, svg, pdf, jpeg (default: png)
--output, -o      Output filename (without extension)
--title           Chart title
--xlabel          X-axis label
--ylabel          Y-axis label
```

### Examples

```bash
# Bar chart with title
python main.py bar \
  --data '{"labels": ["A", "B", "C"], "values": [10, 20, 15]}' \
  --title "Sales Data" \
  --theme vibrant

# Pie chart as SVG
python main.py pie \
  --data '{"labels": ["Yes", "No"], "values": [70, 30]}' \
  --style donut \
  --format svg

# Line chart with custom filename
python main.py line \
  --data '{"x": [1,2,3,4,5], "y": [2,4,6,8,10]}' \
  --output my_chart \
  --style smooth

# Rose chart
python main.py rose \
  --data '{"labels": ["A", "B", "C"], "values": [10, 20, 30]}' \
  --theme westeros
```

---

## Output

### File Naming

Generated files follow this pattern:
```
{chart_type}_{timestamp}_{random_suffix}.{format}
```

Example: `bar_20260104_143052_a1b2c3.png`

### Output Formats

| Format | Description | Best For |
|--------|-------------|----------|
| `png` | Raster, lossless | Web, presentations |
| `svg` | Vector, scalable | Print, web (scalable) |
| `pdf` | Vector, print-ready | Documents, reports |
| `jpeg` | Raster, compressed | Photos, small file size |

---

## Project Structure

```
charter/
├── main.py                    # CLI entry point
├── pyproject.toml             # Project configuration
├── output/                    # Default output directory
└── src/
    └── charter/
        ├── __init__.py        # Public API exports
        ├── api.py             # Main generate_chart() function
        ├── charts/            # Chart implementations
        │   ├── base.py        # BaseChart abstract class
        │   ├── bar.py         # BarChart
        │   ├── pie.py         # PieChart
        │   ├── line.py        # LineChart
        │   ├── rose.py        # RoseChart
        │   └── timeseries.py  # TimeSeriesChart
        ├── config/
        │   └── settings.py    # Configuration management
        ├── output/
        │   └── manager.py     # File output handling
        ├── styles/
        │   ├── presets.py     # Style definitions
        │   └── registry.py    # Style registry
        ├── themes/
        │   ├── base.py        # Theme class definition
        │   └── presets.py     # Built-in themes
        └── utils/
            └── validators.py  # Data validation
```

---

## Examples

### Complete Example: Dashboard Charts

```python
import asyncio
from charter import generate_chart

async def generate_dashboard():
    """Generate a set of dashboard charts."""
    
    # Revenue bar chart
    await generate_chart(
        chart_type="bar",
        data={
            "labels": ["Q1", "Q2", "Q3", "Q4"],
            "series": {
                "2023": [120, 150, 140, 180],
                "2024": [140, 170, 165, 210],
            },
        },
        style="grouped",
        theme="vibrant",
        title="Quarterly Revenue ($M)",
        filename="revenue_comparison",
    )
    
    # Market share pie
    await generate_chart(
        chart_type="pie",
        data={
            "labels": ["Product A", "Product B", "Product C", "Others"],
            "values": [35, 28, 22, 15],
        },
        style="donut",
        theme="light",
        title="Market Share",
        filename="market_share",
    )
    
    # Trend line chart
    await generate_chart(
        chart_type="line",
        data={
            "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "series": {
                "Users": [1000, 1200, 1150, 1400, 1600, 1800],
                "Sessions": [2500, 3000, 2800, 3500, 4000, 4500],
            },
        },
        style="smooth",
        theme="minimal",
        title="User Growth",
        filename="user_growth",
    )
    
    # Rose chart example
    await generate_chart(
        chart_type="rose",
        data={
            "labels": ["Biology", "Physics", "Chemistry", "Math", "History", "Arts"],
            "values": [85, 90, 75, 95, 70, 80],
        },
        style="radius",
        theme="westeros",
        title="Student Performance",
        filename="student_rose",
    )
    
    # Stock price time series
    await generate_chart(
        chart_type="timeseries",
        data={
            "dates": [
                "2024-01-01", "2024-01-08", "2024-01-15",
                "2024-01-22", "2024-01-29", "2024-02-05",
            ],
            "values": [150, 155, 152, 160, 158, 165],
        },
        style="trend",
        theme="default",
        title="Stock Price (ACME)",
        filename="stock_price",
    )
    
    print("Dashboard charts generated!")

asyncio.run(generate_dashboard())
```

---

## Gallery

Generate a complete gallery of all styles and themes:

```bash
python main.py gallery
```

This creates all style/theme combinations in `output/gallery/`.

### Rose Chart Styles

#### radius

| Default | Dark | Westeros |
|---------|------|----------|
| ![](output/gallery/rose_radius_default.png) | ![](output/gallery/rose_radius_dark.png) | ![](output/gallery/rose_radius_westeros.png) |

#### area

| Default | Dark | Wonderland |
|---------|------|------------|
| ![](output/gallery/rose_area_default.png) | ![](output/gallery/rose_area_dark.png) | ![](output/gallery/rose_area_wonderland.png) |

---

### Bar Chart Styles

#### default

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/bar_default_default.png) | ![](output/gallery/bar_default_dark.png) | ![](output/gallery/bar_default_plotly_dark.png) |

#### grouped

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/bar_grouped_default.png) | ![](output/gallery/bar_grouped_dark.png) | ![](output/gallery/bar_grouped_plotly_dark.png) |

#### stacked

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/bar_stacked_default.png) | ![](output/gallery/bar_stacked_dark.png) | ![](output/gallery/bar_stacked_plotly_dark.png) |

#### horizontal

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/bar_horizontal_default.png) | ![](output/gallery/bar_horizontal_dark.png) | ![](output/gallery/bar_horizontal_plotly_dark.png) |

#### outlined

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/bar_outlined_default.png) | ![](output/gallery/bar_outlined_dark.png) | ![](output/gallery/bar_outlined_plotly_dark.png) |

#### labeled

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/bar_labeled_default.png) | ![](output/gallery/bar_labeled_dark.png) | ![](output/gallery/bar_labeled_plotly_dark.png) |

---

### Pie Chart Styles

#### default

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/pie_default_default.png) | ![](output/gallery/pie_default_dark.png) | ![](output/gallery/pie_default_plotly_dark.png) |

#### donut

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/pie_donut_default.png) | ![](output/gallery/pie_donut_dark.png) | ![](output/gallery/pie_donut_plotly_dark.png) |

#### exploded

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/pie_exploded_default.png) | ![](output/gallery/pie_exploded_dark.png) | ![](output/gallery/pie_exploded_plotly_dark.png) |

#### detailed

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/pie_detailed_default.png) | ![](output/gallery/pie_detailed_dark.png) | ![](output/gallery/pie_detailed_plotly_dark.png) |

#### shadow

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/pie_shadow_default.png) | ![](output/gallery/pie_shadow_dark.png) | ![](output/gallery/pie_shadow_plotly_dark.png) |

#### infographic

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/pie_infographic_default.png) | ![](output/gallery/pie_infographic_dark.png) | ![](output/gallery/pie_infographic_plotly_dark.png) |

#### annotated

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/pie_annotated_default.png) | ![](output/gallery/pie_annotated_dark.png) | ![](output/gallery/pie_annotated_plotly_dark.png) |

#### transparent_donut

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/pie_transparent_donut_default.png) | ![](output/gallery/pie_transparent_donut_dark.png) | ![](output/gallery/pie_transparent_donut_plotly_dark.png) |

#### table_legend

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/pie_table_legend_default.png) | ![](output/gallery/pie_table_legend_dark.png) | ![](output/gallery/pie_table_legend_plotly_dark.png) |

#### table_legend_donut

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/pie_table_legend_donut_default.png) | ![](output/gallery/pie_table_legend_donut_dark.png) | ![](output/gallery/pie_table_legend_donut_plotly_dark.png) |

---

### Line Chart Styles

#### default

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/line_default_default.png) | ![](output/gallery/line_default_dark.png) | ![](output/gallery/line_default_plotly_dark.png) |

#### smooth

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/line_smooth_default.png) | ![](output/gallery/line_smooth_dark.png) | ![](output/gallery/line_smooth_plotly_dark.png) |

#### stepped

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/line_stepped_default.png) | ![](output/gallery/line_stepped_dark.png) | ![](output/gallery/line_stepped_plotly_dark.png) |

#### area

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/line_area_default.png) | ![](output/gallery/line_area_dark.png) | ![](output/gallery/line_area_plotly_dark.png) |

#### dotted

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/line_dotted_default.png) | ![](output/gallery/line_dotted_dark.png) | ![](output/gallery/line_dotted_plotly_dark.png) |

#### dashed

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/line_dashed_default.png) | ![](output/gallery/line_dashed_dark.png) | ![](output/gallery/line_dashed_plotly_dark.png) |

#### markers

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/line_markers_default.png) | ![](output/gallery/line_markers_dark.png) | ![](output/gallery/line_markers_plotly_dark.png) |

---

### Time Series Styles

#### default

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/timeseries_default_default.png) | ![](output/gallery/timeseries_default_dark.png) | ![](output/gallery/timeseries_default_plotly_dark.png) |

#### area

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/timeseries_area_default.png) | ![](output/gallery/timeseries_area_dark.png) | ![](output/gallery/timeseries_area_plotly_dark.png) |

#### trend

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/timeseries_trend_default.png) | ![](output/gallery/timeseries_trend_dark.png) | ![](output/gallery/timeseries_trend_plotly_dark.png) |

#### range

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/timeseries_range_default.png) | ![](output/gallery/timeseries_range_dark.png) | ![](output/gallery/timeseries_range_plotly_dark.png) |

#### minimal

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/timeseries_minimal_default.png) | ![](output/gallery/timeseries_minimal_dark.png) | ![](output/gallery/timeseries_minimal_plotly_dark.png) |

---

### Dashboard Examples

#### Traffic + Latency Dashboard

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/dashboard_traffic_default.png) | ![](output/gallery/dashboard_traffic_dark.png) | ![](output/gallery/dashboard_traffic_plotly_dark.png) |

#### 2x2 Grid Dashboard

| Default | Dark | Plotly Dark |
|---------|------|-------------|
| ![](output/gallery/dashboard_grid_default.png) | ![](output/gallery/dashboard_grid_dark.png) | ![](output/gallery/dashboard_grid_plotly_dark.png) |

---

### Theme Comparison

The same bar chart rendered with all 6 themes:

| Theme | Sample |
|-------|--------|
| default | ![](output/gallery/bar_default_default.png) |
| dark | ![](output/gallery/bar_default_dark.png) |
| light | ![](output/gallery/bar_default_light.png) |
| minimal | ![](output/gallery/bar_default_minimal.png) |
| vibrant | ![](output/gallery/bar_default_vibrant.png) |
| plotly_dark | ![](output/gallery/bar_default_plotly_dark.png) |

---

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
