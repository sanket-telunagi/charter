"""
Charter CLI - Command line interface for chart generation.

Usage:
    python main.py                    # Run demo with sample charts
    python main.py --help             # Show help
    python main.py bar --data '...'   # Generate specific chart type
"""

import asyncio
import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent / "src"))

from charter import (
    generate_chart,
    generate_dashboard,
    get_settings,
    AVAILABLE_THEMES,
    get_style_registry,
)


async def demo() -> None:
    """Run demo generating sample charts of each type."""
    print("Charter Demo - Generating sample charts...")
    print("=" * 50)
    
    settings = get_settings()
    print(f"Output directory: {settings.output_dir.absolute()}")
    print()
    
    # Demo bar chart
    print("1. Generating bar chart...")
    bar_path = await generate_chart(
        chart_type="bar",
        data={
            "labels": ["January", "February", "March", "April", "May"],
            "values": [65, 59, 80, 81, 56],
        },
        style="default",
        theme="default",
        title="Monthly Sales",
        xlabel="Month",
        ylabel="Sales ($K)",
    )
    print(f"   Saved: {bar_path}")
    
    # Demo grouped bar chart
    print("2. Generating grouped bar chart...")
    grouped_path = await generate_chart(
        chart_type="bar",
        data={
            "labels": ["Q1", "Q2", "Q3", "Q4"],
            "series": {
                "2023": [45, 52, 48, 61],
                "2024": [51, 58, 55, 68],
            },
        },
        style="grouped",
        theme="vibrant",
        title="Quarterly Revenue Comparison",
        xlabel="Quarter",
        ylabel="Revenue ($M)",
    )
    print(f"   Saved: {grouped_path}")
    
    # Demo pie chart
    print("3. Generating pie chart...")
    pie_path = await generate_chart(
        chart_type="pie",
        data={
            "labels": ["Desktop", "Mobile", "Tablet", "Other"],
            "values": [45, 35, 15, 5],
        },
        style="default",
        theme="light",
        title="Traffic by Device",
    )
    print(f"   Saved: {pie_path}")
    
    # Demo donut chart
    print("4. Generating donut chart...")
    donut_path = await generate_chart(
        chart_type="pie",
        data={
            "labels": ["Completed", "In Progress", "Pending", "Cancelled"],
            "values": [42, 28, 20, 10],
        },
        style="donut",
        theme="dark",
        title="Task Status Distribution",
    )
    print(f"   Saved: {donut_path}")
    
    # Demo infographic pie chart
    print("4b. Generating infographic pie chart...")
    infographic_path = await generate_chart(
        chart_type="pie",
        data={
            "labels": [
                "United States", "European Union", "Japan", 
                "Russian Federation", "China", "India", 
                "South Asia", "Rest of World"
            ],
            "values": [22, 10, 5, 6, 16, 5, 4, 32],
            "subtitle": "Carbon dioxide emissions are dominated by just five countries, and the European Union:",
        },
        style="infographic",
        theme="light",
        title="GLOBAL SHARE OF CO₂ EMISSIONS",
    )
    print(f"   Saved: {infographic_path}")
    
    # Demo annotated pie chart with custom colors and gaps
    print("4c. Generating annotated pie chart...")
    annotated_path = await generate_chart(
        chart_type="pie",
        data={
            "labels": [
                "United\nStates, 22%",
                "European\nUnion, 10%",
                "Japan, 5%",
                "",  # Gap slice
                "Russian\nFederation, 6%",
                "",  # Gap slice
                "China, 16%",
                "",  # Gap slice
                "India, 5%",
                "",  # Gap slice
                "Rest of\nWorld",
            ],
            "values": [22, 10, 5, 0.5, 6, 4, 16, 4, 5, 2.5, 25],
            "colors": [
                "#76aab8", "#76aab8", "#76aab8",
                "#ffffff",  # Gap color
                "#d47366",
                "#eadbd9",  # Gap color
                "#e0bb5b",
                "#f5eecb",  # Gap color
                "#8dc191",
                "#d8e9da",  # Gap color
                "#dcdcdc",
            ],
            "center_title": "GLOBAL SHARE\nOF CO₂ EMISSIONS",
        },
        style="annotated",
        theme="light",
    )
    print(f"   Saved: {annotated_path}")
    
    # Demo line chart
    print("5. Generating line chart...")
    line_path = await generate_chart(
        chart_type="line",
        data={
            "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "series": {
                "This Week": [150, 180, 165, 195, 210, 185, 170],
                "Last Week": [140, 165, 155, 175, 190, 180, 160],
            },
        },
        style="smooth",
        theme="minimal",
        title="Daily Active Users",
        xlabel="Day",
        ylabel="Users",
    )
    print(f"   Saved: {line_path}")
    
    # Demo area chart
    print("6. Generating area chart...")
    area_path = await generate_chart(
        chart_type="line",
        data={
            "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "y": [10, 15, 13, 17, 20, 25, 22, 28, 32, 30],
        },
        style="area",
        theme="vibrant",
        title="Growth Trend",
        xlabel="Period",
        ylabel="Value",
    )
    print(f"   Saved: {area_path}")
    
    # Demo time series
    print("7. Generating time series chart...")
    timeseries_path = await generate_chart(
        chart_type="timeseries",
        data={
            "dates": [
                "2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04",
                "2024-01-05", "2024-01-06", "2024-01-07", "2024-01-08",
                "2024-01-09", "2024-01-10",
            ],
            "values": [100, 105, 102, 110, 108, 115, 120, 118, 125, 130],
        },
        style="trend",
        theme="default",
        title="Stock Price with Trend",
        xlabel="Date",
        ylabel="Price ($)",
    )
    print(f"   Saved: {timeseries_path}")
    
    print("8. Generating time series chart with plotly dark theme...")
    generate_chart_plotly_theme = await generate_chart(
        chart_type="timeseries",
        data={
            "dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "values": [100, 105, 110],
        },
        theme="plotly_dark",
        title="Yearly Order Volume",
    )
    print(f"   Saved: {generate_chart_plotly_theme}")
    
    # Demo high-granularity time series with automatic downsampling
    print("9. Generating high-granularity time series (50K points with LTTB downsampling)...")
    
    # Generate 50,000 data points (simulating ~35 days of 1-minute data)
    n_points = 50000
    start_date = datetime(2024, 1, 1)
    dates_large = [start_date + timedelta(minutes=i) for i in range(n_points)]
    
    # Create realistic-looking data with trend, seasonality, and noise
    t = np.arange(n_points)
    trend = 100 + 0.001 * t  # Slight upward trend
    daily_cycle = 20 * np.sin(2 * np.pi * t / 1440)  # 24-hour cycle (1440 minutes)
    noise = np.random.normal(0, 5, n_points)  # Random noise
    values_large = trend + daily_cycle + noise
    
    large_ts_path = await generate_chart(
        chart_type="timeseries",
        data={
            "dates": dates_large,
            "values": values_large.tolist(),
        },
        style="large_dataset",  # Uses auto_downsample and auto_rasterize
        theme="plotly_dark",
        title=f"Sensor Readings (Original: {n_points:,} pts → Auto-downsampled)",
        xlabel="Time",
        ylabel="Value",
    )
    print(f"   Saved: {large_ts_path}")
    
    # Demo with multiple series and high granularity
    print("10. Generating multi-series high-granularity chart...")
    n_points_multi = 25000
    dates_multi = [start_date + timedelta(minutes=i) for i in range(n_points_multi)]
    t_multi = np.arange(n_points_multi)
    
    multi_series_path = await generate_chart(
        chart_type="timeseries",
        data={
            "dates": dates_multi,
            "series": {
                "Temperature": (25 + 5 * np.sin(2 * np.pi * t_multi / 1440) + np.random.normal(0, 1, n_points_multi)).tolist(),
                "Humidity": (60 + 10 * np.cos(2 * np.pi * t_multi / 1440) + np.random.normal(0, 2, n_points_multi)).tolist(),
            },
        },
        style="large_dataset",
        theme="dark",
        title=f"Environmental Sensors ({n_points_multi:,} points each)",
        xlabel="Time",
        ylabel="Reading",
    )
    print(f"   Saved: {multi_series_path}")
    
    # Demo dashboard - Traffic Volume + Latency (like the reference image)
    print("11. Generating Traffic Volume + Latency dashboard...")
    
    # Generate realistic traffic data (1 hour of 1-minute data)
    n_dashboard_points = 60
    dashboard_start = datetime(2026, 1, 4, 20, 30)
    dashboard_dates = [dashboard_start + timedelta(minutes=i) for i in range(n_dashboard_points)]
    
    # Primary and Secondary node traffic with slight correlation
    t_dash = np.arange(n_dashboard_points)
    base_traffic = 50 + 5 * np.sin(2 * np.pi * t_dash / 30)  # 30-min cycle
    primary_traffic = base_traffic + np.random.normal(0, 3, n_dashboard_points) + 10
    secondary_traffic = base_traffic + np.random.normal(0, 2, n_dashboard_points)
    
    # Simulate a brief dip/spike around minute 30
    primary_traffic[28:35] = primary_traffic[28:35] - 20
    secondary_traffic[28:35] = secondary_traffic[28:35] - 15
    
    # Latency data for bar chart (10-minute intervals)
    latency_times = ["10:30", "10:40", "10:50", "11:00", "11:10"]
    latency_values = [91.0, 92.2, 93.0, 92.5, 92.3]
    
    dashboard_path = await generate_dashboard(
        panels=[
            {
                "chart_type": "timeseries",
                "data": {
                    "dates": dashboard_dates,
                    "series": {
                        "Secondary Node": secondary_traffic.tolist(),
                        "Primary Node": primary_traffic.tolist(),
                    },
                },
                "style": "default",
                "title": "Traffic Volume",
                "ylabel": "",
                "col": 0,
            },
            {
                "chart_type": "bar",
                "data": {
                    "labels": latency_times,
                    "values": latency_values,
                },
                "style": "default",
                "title": "Latency (ms)",
                "col": 1,
            },
        ],
        layout={
            "cols": 2,
            "width_ratios": [2.5, 1],
            "figsize": [18, 6],
            "shared_legend": True,
            "legend_position": "top",
        },
        theme="plotly_dark",
        title="",
    )
    print(f"   Saved: {dashboard_path}")
    
    # Demo a 2x2 grid dashboard
    print("12. Generating 2x2 grid dashboard...")
    
    grid_dashboard_path = await generate_dashboard(
        panels=[
            {
                "chart_type": "bar",
                "data": {
                    "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"],
                    "values": [120, 150, 135, 180, 165],
                },
                "title": "Daily Orders",
                "row": 0, "col": 0,
            },
            {
                "chart_type": "line",
                "data": {
                    "labels": ["Week 1", "Week 2", "Week 3", "Week 4"],
                    "series": {
                        "Revenue": [1200, 1350, 1280, 1500],
                        "Costs": [800, 850, 820, 900],
                    },
                },
                "style": "smooth",
                "title": "Monthly Financials",
                "row": 0, "col": 1,
            },
            {
                "chart_type": "timeseries",
                "data": {
                    "dates": [datetime(2026, 1, i) for i in range(1, 8)],
                    "values": [45, 52, 48, 61, 55, 58, 62],
                },
                "style": "area",
                "title": "Weekly Active Users",
                "row": 1, "col": 0,
            },
            {
                "chart_type": "bar",
                "data": {
                    "labels": ["Product A", "Product B", "Product C"],
                    "series": {
                        "Q1": [30, 45, 28],
                        "Q2": [35, 50, 32],
                    },
                },
                "style": "grouped",
                "title": "Product Sales",
                "row": 1, "col": 1,
            },
        ],
        layout={
            "rows": 2,
            "cols": 2,
            "figsize": [14, 10],
            "shared_legend": True,
            "legend_position": "top",
        },
        theme="plotly_dark",
        title="Business Metrics Dashboard",
    )
    print(f"   Saved: {grid_dashboard_path}")

    print("=" * 50)
    print("Demo complete! Check the output directory for generated charts.")


async def demo_gallery() -> None:
    """Generate complete gallery of all styles and themes."""
    print("Charter Gallery - Generating all style/theme combinations...")
    print("=" * 60)
    
    # Create gallery output directory
    gallery_dir = Path("output/gallery")
    gallery_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {gallery_dir.absolute()}")
    print()
    
    # Get style registry
    registry = get_style_registry()
    
    # =========================================================================
    # Sample Data Sets
    # =========================================================================
    
    # Bar chart data
    bar_single_data = {
        "labels": ["Jan", "Feb", "Mar", "Apr"],
        "values": [65, 78, 52, 91],
    }
    bar_multi_data = {
        "labels": ["Q1", "Q2", "Q3", "Q4"],
        "series": {
            "2023": [45, 52, 48, 61],
            "2024": [51, 58, 55, 68],
        },
    }
    
    # Pie chart data
    pie_data = {
        "labels": ["Desktop", "Mobile", "Tablet", "Other"],
        "values": [42, 35, 18, 5],
    }
    pie_annotated_data = {
        "labels": ["Desktop, 42%", "Mobile, 35%", "Tablet, 18%", "Other, 5%"],
        "values": [42, 35, 18, 5],
        "center_title": "DEVICE\nSHARE",
    }
    pie_infographic_data = {
        "labels": ["Desktop", "Mobile", "Tablet", "Other"],
        "values": [42, 35, 18, 5],
        "subtitle": "Traffic distribution by device type",
    }
    pie_transparent_data = {
        "labels": ["Desktop, 42%", "Mobile, 35%", "Tablet, 18%", "Other, 5%"],
        "values": [42, 35, 18, 5],
        "center_title": "DEVICE\nSHARE",
    }
    
    # Line chart data
    line_data = {
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "series": {
            "Sales": [120, 150, 135, 180, 165],
            "Returns": [15, 22, 18, 25, 20],
        },
    }
    
    # Time series data
    ts_dates = [datetime(2024, 1, i) for i in range(1, 15)]
    ts_data = {
        "dates": ts_dates,
        "values": [100, 105, 102, 110, 108, 115, 112, 120, 118, 125, 122, 130, 128, 135],
    }
    ts_range_data = {
        "dates": ts_dates,
        "values": [100, 105, 102, 110, 108, 115, 112, 120, 118, 125, 122, 130, 128, 135],
        "upper": [110, 115, 112, 120, 118, 125, 122, 130, 128, 135, 132, 140, 138, 145],
        "lower": [90, 95, 92, 100, 98, 105, 102, 110, 108, 115, 112, 120, 118, 125],
    }
    
    # =========================================================================
    # Bar Chart Gallery
    # =========================================================================
    print("Generating Bar Chart Gallery...")
    bar_styles = registry.list_styles().get("bar", [])
    
    for theme in AVAILABLE_THEMES:
        for style in bar_styles:
            # Use multi data for grouped/stacked styles
            if style in ["grouped", "stacked"]:
                data = bar_multi_data
            else:
                data = bar_single_data
            
            filename = f"gallery/bar_{style}_{theme}"
            try:
                path = await generate_chart(
                    chart_type="bar",
                    data=data,
                    style=style,
                    theme=theme,
                    title=f"Bar Chart ({style})",
                    filename=filename,
                )
                print(f"  [OK] {filename}.png")
            except Exception as e:
                print(f"  [ERROR] {filename}.png - Error: {e}")
    
    # =========================================================================
    # Pie Chart Gallery
    # =========================================================================
    print("\nGenerating Pie Chart Gallery...")
    pie_styles = registry.list_styles().get("pie", [])
    
    for theme in AVAILABLE_THEMES:
        for style in pie_styles:
            # Use appropriate data for special styles
            if style == "annotated":
                data = pie_annotated_data
            elif style == "infographic":
                data = pie_infographic_data
            elif style == "transparent_donut":
                data = pie_transparent_data
            elif style in ["table_legend", "table_legend_donut"]:
                data = pie_data  # Standard data works for table legend styles
            else:
                data = pie_data
            
            # Determine title for different styles
            no_title_styles = ["annotated", "transparent_donut"]
            chart_title = f"Pie Chart ({style})" if style not in no_title_styles else None
            
            filename = f"gallery/pie_{style}_{theme}"
            try:
                path = await generate_chart(
                    chart_type="pie",
                    data=data,
                    style=style,
                    theme=theme,
                    title=chart_title,
                    filename=filename,
                )
                print(f"  [OK] {filename}.png")
            except Exception as e:
                print(f"  [ERROR] {filename}.png - Error: {e}")
    
    # =========================================================================
    # Line Chart Gallery
    # =========================================================================
    print("\nGenerating Line Chart Gallery...")
    line_styles = registry.list_styles().get("line", [])
    
    for theme in AVAILABLE_THEMES:
        for style in line_styles:
            filename = f"gallery/line_{style}_{theme}"
            try:
                path = await generate_chart(
                    chart_type="line",
                    data=line_data,
                    style=style,
                    theme=theme,
                    title=f"Line Chart ({style})",
                    filename=filename,
                )
                print(f"  [OK] {filename}.png")
            except Exception as e:
                print(f"  [ERROR] {filename}.png - Error: {e}")
    
    # =========================================================================
    # Time Series Chart Gallery
    # =========================================================================
    print("\nGenerating Time Series Chart Gallery...")
    ts_styles = registry.list_styles().get("timeseries", [])
    
    for theme in AVAILABLE_THEMES:
        for style in ts_styles:
            # Skip large_dataset style in gallery (too slow)
            if style == "large_dataset":
                continue
            
            # Use range data for range style
            if style == "range":
                data = ts_range_data
            else:
                data = ts_data
            
            filename = f"gallery/timeseries_{style}_{theme}"
            try:
                path = await generate_chart(
                    chart_type="timeseries",
                    data=data,
                    style=style,
                    theme=theme,
                    title=f"Time Series ({style})",
                    filename=filename,
                )
                print(f"  [OK] {filename}.png")
            except Exception as e:
                print(f"  [ERROR] {filename}.png - Error: {e}")
    
    # =========================================================================
    # Dashboard Gallery
    # =========================================================================
    print("\nGenerating Dashboard Gallery...")
    
    # Traffic + Latency Dashboard
    n_dashboard_points = 60
    dashboard_start = datetime(2024, 1, 1, 10, 0)
    dashboard_dates = [dashboard_start + timedelta(minutes=i) for i in range(n_dashboard_points)]
    t_dash = np.arange(n_dashboard_points)
    base_traffic = 50 + 5 * np.sin(2 * np.pi * t_dash / 30)
    primary_traffic = base_traffic + np.random.normal(0, 3, n_dashboard_points) + 10
    secondary_traffic = base_traffic + np.random.normal(0, 2, n_dashboard_points)
    
    for theme in ["plotly_dark", "dark", "default"]:
        filename = f"gallery/dashboard_traffic_{theme}"
        try:
            path = await generate_dashboard(
                panels=[
                    {
                        "chart_type": "timeseries",
                        "data": {
                            "dates": dashboard_dates,
                            "series": {
                                "Secondary": secondary_traffic.tolist(),
                                "Primary": primary_traffic.tolist(),
                            },
                        },
                        "title": "Traffic Volume",
                        "col": 0,
                    },
                    {
                        "chart_type": "bar",
                        "data": {
                            "labels": ["10:00", "10:20", "10:40", "11:00"],
                            "values": [91, 92, 93, 92],
                        },
                        "title": "Latency (ms)",
                        "col": 1,
                    },
                ],
                layout={"cols": 2, "width_ratios": [2.5, 1], "figsize": [16, 5]},
                theme=theme,
                filename=filename,
            )
            print(f"  [OK] {filename}.png")
        except Exception as e:
            print(f"  [ERROR] {filename}.png - Error: {e}")
    
    # 2x2 Grid Dashboard
    for theme in ["plotly_dark", "dark", "default"]:
        filename = f"gallery/dashboard_grid_{theme}"
        try:
            path = await generate_dashboard(
                panels=[
                    {
                        "chart_type": "bar",
                        "data": {"labels": ["Mon", "Tue", "Wed", "Thu", "Fri"], "values": [120, 150, 135, 180, 165]},
                        "title": "Daily Orders",
                        "row": 0, "col": 0,
                    },
                    {
                        "chart_type": "line",
                        "data": {"labels": ["W1", "W2", "W3", "W4"], "series": {"Revenue": [1200, 1350, 1280, 1500], "Costs": [800, 850, 820, 900]}},
                        "style": "smooth",
                        "title": "Financials",
                        "row": 0, "col": 1,
                    },
                    {
                        "chart_type": "timeseries",
                        "data": {"dates": [datetime(2024, 1, i) for i in range(1, 8)], "values": [45, 52, 48, 61, 55, 58, 62]},
                        "style": "area",
                        "title": "Active Users",
                        "row": 1, "col": 0,
                    },
                    {
                        "chart_type": "bar",
                        "data": {"labels": ["A", "B", "C"], "series": {"Q1": [30, 45, 28], "Q2": [35, 50, 32]}},
                        "style": "grouped",
                        "title": "Product Sales",
                        "row": 1, "col": 1,
                    },
                ],
                layout={"rows": 2, "cols": 2, "figsize": [14, 10]},
                theme=theme,
                title="Business Metrics",
                filename=filename,
            )
            print(f"  [OK] {filename}.png")
        except Exception as e:
            print(f"  [ERROR] {filename}.png - Error: {e}")
    
    # =========================================================================
    # Summary
    # =========================================================================
    print()
    print("=" * 60)
    print("Gallery generation complete!")
    print(f"Output directory: {gallery_dir.absolute()}")
    
    # Count generated files
    generated = list(gallery_dir.glob("*.png"))
    print(f"Total images generated: {len(generated)}")


async def generate_from_cli(args: argparse.Namespace) -> None:
    """Generate a chart from CLI arguments."""
    try:
        data = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON data - {e}", file=sys.stderr)
        sys.exit(1)
    
    path = await generate_chart(
        chart_type=args.type,
        data=data,
        style=args.style,
        theme=args.theme,
        output_format=args.format,
        filename=args.output,
        title=args.title,
        xlabel=args.xlabel,
        ylabel=args.ylabel,
    )
    
    print(f"Chart saved to: {path}")


def main() -> None:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Charter - Generate beautiful charts from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py
    Run demo with sample charts
    
  python main.py gallery
    Generate complete gallery of all styles and themes
    
  python main.py bar --data '{"labels": ["A", "B", "C"], "values": [1, 2, 3]}'
    Generate a bar chart
    
  python main.py pie --data '{"labels": ["X", "Y"], "values": [60, 40]}' --style donut --theme dark
    Generate a donut chart with dark theme
    
  python main.py list
    List all available themes and styles
        """,
    )
    
    subparsers = parser.add_subparsers(dest="type", help="Chart type to generate")
    
    # Common arguments for all chart types
    def add_common_args(subparser):
        subparser.add_argument(
            "--data", "-d",
            required=True,
            help="Chart data as JSON string",
        )
        subparser.add_argument(
            "--style", "-s",
            default="default",
            help="Chart style (default: default)",
        )
        subparser.add_argument(
            "--theme", "-t",
            default="default",
            choices=AVAILABLE_THEMES,
            help="Chart theme (default: default)",
        )
        subparser.add_argument(
            "--format", "-f",
            default="png",
            choices=["png", "svg", "pdf", "jpeg"],
            help="Output format (default: png)",
        )
        subparser.add_argument(
            "--output", "-o",
            help="Output filename (without extension)",
        )
        subparser.add_argument(
            "--title",
            help="Chart title",
        )
        subparser.add_argument(
            "--xlabel",
            help="X-axis label",
        )
        subparser.add_argument(
            "--ylabel",
            help="Y-axis label",
        )
    
    # Bar chart subcommand
    bar_parser = subparsers.add_parser("bar", help="Generate a bar chart")
    add_common_args(bar_parser)
    
    # Pie chart subcommand
    pie_parser = subparsers.add_parser("pie", help="Generate a pie chart")
    add_common_args(pie_parser)
    
    # Line chart subcommand
    line_parser = subparsers.add_parser("line", help="Generate a line chart")
    add_common_args(line_parser)
    
    # Time series subcommand
    ts_parser = subparsers.add_parser("timeseries", help="Generate a time series chart")
    add_common_args(ts_parser)
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available themes and styles")
    
    # Gallery command
    gallery_parser = subparsers.add_parser("gallery", help="Generate complete gallery of all styles and themes")
    
    args = parser.parse_args()
    
    if args.type == "list":
        print("Available Themes:")
        for theme in AVAILABLE_THEMES:
            print(f"  - {theme}")
        print()
        print("Available Styles:")
        registry = get_style_registry()
        for chart_type, styles in registry.list_styles().items():
            print(f"  {chart_type}:")
            for style in styles:
                print(f"    - {style}")
    elif args.type == "gallery":
        asyncio.run(demo_gallery())
    elif args.type:
        asyncio.run(generate_from_cli(args))
    else:
        # No subcommand - run demo
        asyncio.run(demo())


if __name__ == "__main__":
    main()
