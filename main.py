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
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent / "src"))

from charter import (
    generate_chart,
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
    
    print()
    print("=" * 50)
    print("Demo complete! Check the output directory for generated charts.")


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
    
  python main.py bar --data '{"labels": ["A", "B", "C"], "values": [1, 2, 3]}'
    Generate a bar chart
    
  python main.py pie --data '{"labels": ["X", "Y"], "values": [60, 40]}' --style donut --theme dark
    Generate a donut chart with dark theme
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
    elif args.type:
        asyncio.run(generate_from_cli(args))
    else:
        # No subcommand - run demo
        asyncio.run(demo())


if __name__ == "__main__":
    main()
