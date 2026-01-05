"""
Pie chart implementation with support for various styles.

Supports:
- Standard pie charts
- Donut (ring) charts
- Exploded slices
- Percentage and label display options
- Infographic style with external labels and leader lines
"""

from typing import Any

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import ConnectionPatch

from charter.charts.base import BaseChart
from charter.styles.presets import PieStyle
from charter.themes.base import Theme


class PieChart(BaseChart):
    """
    Pie chart renderer with multiple style options.
    
    Expected data format:
        {
            "labels": ["Category A", "Category B", "Category C"],
            "values": [30, 45, 25]
        }
        
    For infographic style with subtitle:
        {
            "labels": ["Category A", "Category B", "Category C"],
            "values": [30, 45, 25],
            "subtitle": "Optional description text"
        }
    """

    def __init__(
        self,
        data: dict[str, Any],
        style: PieStyle,
        theme: Theme,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
    ) -> None:
        super().__init__(data, style, theme, title, xlabel, ylabel)
        self.style: PieStyle = style  # Type narrowing

    def _render_sync(self) -> Figure:
        """Render the pie chart synchronously."""
        # Use infographic rendering if style requires it
        if self.style.infographic:
            return self._render_infographic()
        
        # Use annotated rendering if style requires it
        if self.style.use_annotate:
            return self._render_annotated()
        
        fig, ax = self._create_figure()
        
        labels = self.data.get("labels", [])
        values = self.data.get("values", [])
        
        # Generate colors from theme
        colors = [self.theme.get_color(i) for i in range(len(values))]
        
        # Build pie chart kwargs
        pie_kwargs = self._build_pie_kwargs(labels, colors)
        
        # Create the pie chart
        wedges, texts, autotexts = ax.pie(values, **pie_kwargs)
        
        # Style the text elements
        self._style_texts(texts, autotexts)
        
        # Handle donut style
        if self.style.donut:
            self._create_donut_hole(ax)
        
        # Apply title (pie charts don't have x/y labels)
        if self.title:
            ax.set_title(
                self.title,
                fontsize=self.theme.title_font_size,
                color=self.theme.title_color,
                fontfamily=self.theme.font_family,
                pad=20,
            )
        
        # Equal aspect ratio ensures circular pie
        ax.set_aspect("equal")
        
        return self._finalize_figure(fig)
    
    def _render_infographic(self) -> Figure:
        """Render infographic-style pie chart with external labels and leader lines."""
        labels = self.data.get("labels", [])
        values = self.data.get("values", [])
        subtitle = self.data.get("subtitle", None)
        
        # Calculate percentages
        total = sum(values)
        percentages = [(v / total) * 100 for v in values]
        
        # Generate colors from theme
        colors = [self.theme.get_color(i) for i in range(len(values))]
        
        # Create figure with more room for external labels
        figsize = self._settings.default_figsize or self.theme.figsize
        fig, ax = plt.subplots(figsize=(figsize[0] * 1.2, figsize[1]))
        
        # Apply theme to figure
        self.theme.apply_to_figure(fig)
        ax.set_facecolor(self.theme.background_color)
        
        # Create pie without labels (we'll add external labels)
        # ax.pie() returns (patches, texts) when autopct is not set, or (patches, texts, autotexts) when it is
        wedges, _ = ax.pie(
            values,
            colors=colors,
            startangle=self.style.start_angle,
            counterclock=self.style.counter_clockwise,
            wedgeprops={
                "linewidth": 2,
                "edgecolor": self.theme.background_color,
                "width": 1 - self.style.donut_ratio if self.style.donut else 1,
            },
        )
        
        # Add external labels with leader lines
        self._add_external_labels(ax, wedges, labels, percentages)
        
        # Add title and subtitle
        title_y = 1.15
        if self.title:
            ax.text(
                0, title_y,
                self.title,
                transform=ax.transAxes,
                fontsize=self.theme.title_font_size + 2,
                fontweight="bold",
                color=self.theme.title_color,
                fontfamily=self.theme.font_family,
                ha="center",
                va="bottom",
            )
        
        if subtitle:
            ax.text(
                0, title_y - 0.08,
                subtitle,
                transform=ax.transAxes,
                fontsize=self.theme.label_font_size,
                color=self.theme.text_color,
                fontfamily=self.theme.font_family,
                ha="center",
                va="top",
                style="italic",
            )
        
        # Equal aspect ratio ensures circular pie
        ax.set_aspect("equal")
        
        # Adjust subplot to make room for labels
        plt.subplots_adjust(left=0.15, right=0.85, top=0.85, bottom=0.1)
        
        return fig
    
    def _render_annotated(self) -> Figure:
        """Render annotated-style pie chart with center title and annotation leader lines."""
        labels = self.data.get("labels", [])
        values = self.data.get("values", [])
        center_title = self.data.get("center_title", None)
        
        # Use per-slice colors from data if provided, otherwise use theme colors
        data_colors = self.data.get("colors", None)
        if data_colors and len(data_colors) == len(values):
            colors = data_colors
        else:
            colors = [self.theme.get_color(i) for i in range(len(values))]
        
        # Create figure with more room for external labels
        figsize = self._settings.default_figsize or self.theme.figsize
        fig, ax = plt.subplots(figsize=(figsize[0] * 1.2, figsize[1]))
        
        # Apply theme to figure
        self.theme.apply_to_figure(fig)
        
        # Handle transparent background
        if self.style.transparent_background:
            fig.patch.set_alpha(0.0)
            ax.set_facecolor("none")
            ax.patch.set_alpha(0.0)
        else:
            ax.set_facecolor(self.theme.background_color)
        
        # Calculate donut width (ring thickness)
        # donut_ratio is the inner radius ratio, so width = 1 - inner_ratio
        donut_width = 1 - self.style.donut_ratio if self.style.donut else 1
        
        # For transparent background, use transparent edge color
        edge_color = "none" if self.style.transparent_background else self.theme.background_color
        
        # Create pie/donut chart using wedgeprops width approach
        wedges, _ = ax.pie(
            values,
            colors=colors,
            startangle=self.style.start_angle,
            counterclock=self.style.counter_clockwise,
            wedgeprops={
                "width": donut_width,
                "edgecolor": edge_color,
                "linewidth": 1.5,
            },
        )
        
        # Add annotated labels with leader lines and bbox
        self._add_annotated_labels(ax, wedges, labels)
        
        # Add center title if enabled and provided
        if self.style.center_title and center_title:
            if self.style.center_title_bbox:
                self._add_center_title_with_box(ax, center_title)
            else:
                ax.text(
                    0, 0,
                    center_title,
                    ha="center",
                    va="center",
                    fontsize=self.theme.title_font_size,
                    fontweight="bold",
                    color=self.theme.text_color,
                    fontfamily=self.theme.font_family,
                )
        
        # Add main title at top if provided
        if self.title:
            ax.set_title(
                self.title,
                fontsize=self.theme.title_font_size + 2,
                fontweight="bold",
                color=self.theme.title_color,
                fontfamily=self.theme.font_family,
                pad=30,
            )
        
        # Equal aspect ratio ensures circular pie
        ax.set_aspect("equal")
        
        # Handle transparency settings for output
        if self.style.transparent_background:
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
        else:
            fig.patch.set_alpha(1.0)
            ax.patch.set_alpha(1.0)
        
        plt.tight_layout()
        
        return fig
    
    def _add_center_title_with_box(
        self,
        ax: plt.Axes,
        center_title: str,
    ) -> None:
        """
        Add center title with a rounded background box.
        
        Args:
            ax: matplotlib Axes object
            center_title: Text to display in center (supports newlines)
        """
        # Build bbox properties for the rounded background box
        bbox_props = {
            "boxstyle": f"round,pad={self.style.center_title_bbox_pad},rounding_size=0.3",
            "facecolor": self.style.center_title_bbox_facecolor,
            "edgecolor": "none",
            "alpha": self.style.center_title_bbox_alpha,
        }
        
        # Add the center title text with bbox
        ax.text(
            0, 0,
            center_title,
            ha="center",
            va="center",
            fontsize=self.theme.title_font_size,
            fontweight="bold",
            color=self.theme.text_color,
            fontfamily=self.theme.font_family,
            bbox=bbox_props,
            zorder=10,
        )
    
    def _add_annotated_labels(
        self,
        ax: plt.Axes,
        wedges: list,
        labels: list[str],
    ) -> None:
        """Add labels using matplotlib annotate() with angled connection lines and bbox styling."""
        # Get leader line color
        line_color = self.style.leader_line_color or "#777777"
        
        # Build bbox dict if label_bbox is enabled
        bbox_props = None
        if self.style.label_bbox:
            bbox_props = {
                "boxstyle": self.style.label_bbox_style,
                "fc": self.style.label_bbox_facecolor,
                "ec": self.style.label_bbox_edgecolor,
                "alpha": self.style.label_bbox_alpha,
                "lw": 1,
            }
        
        for i, wedge in enumerate(wedges):
            # Skip slices with empty labels (gap slices)
            if i >= len(labels) or not labels[i]:
                continue
            
            label = labels[i]
            
            # Calculate angle for label positioning (center of wedge)
            ang = (wedge.theta2 - wedge.theta1) / 2.0 + wedge.theta1
            
            # Calculate position on the wedge edge
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            
            # Determine text alignment based on position
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x)) if x != 0 else 1]
            
            # Create angled connection style for the leader line
            connectionstyle = f"angle,angleA=0,angleB={ang}"
            
            # Arrow properties for the leader line
            arrow_props = {
                "arrowstyle": "-",
                "color": line_color,
                "linewidth": self.style.leader_line_width,
                "connectionstyle": connectionstyle,
            }
            
            # Annotation kwargs
            annotate_kwargs = {
                "xy": (x * 0.75, y * 0.75),  # Anchor point on the wedge
                "xytext": (1.35 * np.sign(x) if x != 0 else 1.35, 1.35 * y),  # Text position
                "horizontalalignment": horizontalalignment,
                "fontsize": self.theme.label_font_size,
                "fontweight": "bold",
                "color": self.theme.text_color,
                "fontfamily": self.theme.font_family,
                "arrowprops": arrow_props,
                "zorder": 5,
                "va": "center",
            }
            
            # Add bbox if enabled
            if bbox_props:
                annotate_kwargs["bbox"] = bbox_props
            
            # Add the annotation
            ax.annotate(label, **annotate_kwargs)
    
    def _add_external_labels(
        self,
        ax: plt.Axes,
        wedges: list,
        labels: list[str],
        percentages: list[float],
    ) -> None:
        """Add external labels with leader lines to the pie chart."""
        # Get leader line color
        line_color = self.style.leader_line_color or self.theme.axis_color
        
        for i, (wedge, label, pct) in enumerate(zip(wedges, labels, percentages)):
            # Calculate angle for label positioning
            ang = (wedge.theta2 - wedge.theta1) / 2.0 + wedge.theta1
            
            # Calculate label position (outside the pie)
            # Use different distances based on which side
            x = np.cos(np.deg2rad(ang))
            y = np.sin(np.deg2rad(ang))
            
            # Determine if label is on left or right side
            horizontalalignment = "left" if x >= 0 else "right"
            
            # Connection point on wedge (at the outer edge)
            connection_x = 1.0 * np.cos(np.deg2rad(ang))
            connection_y = 1.0 * np.sin(np.deg2rad(ang))
            
            # Label position (further out)
            label_x = 1.35 * x
            label_y = 1.35 * y
            
            # Elbow point (intermediate)
            elbow_x = 1.15 * x
            elbow_y = 1.15 * y
            
            # Format the label text
            label_text = self.style.external_label_format.format(
                label=label,
                percent=f"{pct:.0f}%",
            )
            
            # Draw the leader line (two segments for elbow effect)
            # First segment: from wedge to elbow
            ax.plot(
                [connection_x, elbow_x],
                [connection_y, elbow_y],
                color=line_color,
                linewidth=self.style.leader_line_width,
                solid_capstyle="round",
            )
            
            # Second segment: horizontal line to label
            end_x = label_x + (0.1 if x >= 0 else -0.1)
            ax.plot(
                [elbow_x, end_x],
                [elbow_y, label_y],
                color=line_color,
                linewidth=self.style.leader_line_width,
                solid_capstyle="round",
            )
            
            # Add the label text
            ax.text(
                end_x + (0.02 if x >= 0 else -0.02),
                label_y,
                label_text,
                fontsize=self.theme.label_font_size,
                color=self.theme.text_color,
                fontfamily=self.theme.font_family,
                ha=horizontalalignment,
                va="center",
            )

    def _build_pie_kwargs(
        self,
        labels: list[str],
        colors: list[str],
    ) -> dict[str, Any]:
        """Build kwargs for matplotlib pie()."""
        kwargs: dict[str, Any] = {
            "colors": colors,
            "startangle": self.style.start_angle,
            "counterclock": self.style.counter_clockwise,
            "shadow": self.style.shadow,
        }
        
        # Labels
        if self.style.show_labels:
            kwargs["labels"] = labels
            kwargs["labeldistance"] = self.style.label_distance
        else:
            kwargs["labels"] = None
        
        # Percentages
        if self.style.show_percentages:
            kwargs["autopct"] = "%1.1f%%"
            kwargs["pctdistance"] = 0.6 if self.style.donut else 0.5
        
        # Explode
        if self.style.explode:
            explode = [self.style.explode_amount] * len(labels)
            kwargs["explode"] = explode
        
        # Wedge properties
        kwargs["wedgeprops"] = {
            "linewidth": 1,
            "edgecolor": self.theme.background_color,
        }
        
        return kwargs

    def _style_texts(self, texts: list, autotexts: list) -> None:
        """Apply theme styling to text elements."""
        # Style labels
        for text in texts:
            text.set_color(self.theme.text_color)
            text.set_fontsize(self.theme.label_font_size)
            text.set_fontfamily(self.theme.font_family)
        
        # Style percentage labels
        for autotext in autotexts:
            autotext.set_color(self.theme.background_color)
            autotext.set_fontsize(self.theme.tick_font_size)
            autotext.set_fontweight("bold")

    def _create_donut_hole(self, ax: plt.Axes) -> None:
        """Create a center hole for donut charts."""
        # Create white circle in center
        center_circle = plt.Circle(
            (0, 0),
            self.style.donut_ratio,
            fc=self.theme.background_color,
            linewidth=0,
        )
        ax.add_patch(center_circle)

