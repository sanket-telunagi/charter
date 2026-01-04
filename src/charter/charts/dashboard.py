"""
Dashboard chart implementation for multi-panel layouts.

Creates composite figures with multiple charts arranged in a grid layout,
with shared legends and consistent theming.
"""

import asyncio
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

from charter.charts.bar import BarChart
from charter.charts.line import LineChart
from charter.charts.timeseries import TimeSeriesChart
from charter.config.settings import get_settings
from charter.styles.dashboard import PanelConfig, DashboardLayout
from charter.styles.registry import get_style_registry
from charter.themes.base import Theme


# Chart class mapping
CHART_CLASSES = {
    "bar": BarChart,
    "line": LineChart,
    "timeseries": TimeSeriesChart,
}


class DashboardChart:
    """
    Multi-panel dashboard renderer using matplotlib GridSpec.
    
    Creates a single figure with multiple chart panels arranged
    in a configurable grid layout, with optional shared legend.
    
    Example:
        dashboard = DashboardChart(
            panels=[
                PanelConfig(chart_type="timeseries", data={...}, col=0),
                PanelConfig(chart_type="bar", data={...}, col=1),
            ],
            layout=DashboardLayout(cols=2, width_ratios=[2, 1]),
            theme=get_theme("plotly_dark"),
            title="System Dashboard",
        )
        fig = await dashboard.render()
    """

    def __init__(
        self,
        panels: list[PanelConfig],
        layout: DashboardLayout,
        theme: Theme,
        title: str | None = None,
    ) -> None:
        """
        Initialize the dashboard chart.
        
        Args:
            panels: List of panel configurations
            layout: Dashboard layout configuration
            theme: Theme for all panels
            title: Optional dashboard title
        """
        self.panels = panels
        self.layout = layout
        self.theme = theme
        self.title = title
        self._settings = get_settings()
        self._style_registry = get_style_registry()

    async def render(self) -> Figure:
        """
        Render the dashboard asynchronously.
        
        Returns:
            Figure: The rendered matplotlib Figure with all panels
        """
        return await asyncio.to_thread(self._render_sync)

    def _render_sync(self) -> Figure:
        """Render the dashboard synchronously."""
        # Create figure with specified size
        fig = plt.figure(
            figsize=self.layout.figsize,
            dpi=self._settings.default_dpi,
        )
        
        # Apply theme to figure
        self.theme.apply_to_figure(fig)
        
        # Create GridSpec for layout
        gs = GridSpec(
            nrows=self.layout.rows,
            ncols=self.layout.cols,
            figure=fig,
            width_ratios=self.layout.width_ratios,
            height_ratios=self.layout.height_ratios,
            hspace=self.layout.hspace,
            wspace=self.layout.wspace,
        )
        
        # Track legend handles/labels from all panels
        all_handles = []
        all_labels = []
        
        # Render each panel
        for panel in self.panels:
            # Get axes from GridSpec
            ax = fig.add_subplot(
                gs[
                    panel.row : panel.row + panel.rowspan,
                    panel.col : panel.col + panel.colspan,
                ]
            )
            
            # Apply theme to axes
            self.theme.apply_to_axes(ax)
            
            # Create chart instance for this panel
            chart = self._create_panel_chart(panel)
            
            # Render chart to axes
            chart._render_to_axes_impl(ax)
            
            # Apply panel-specific labels
            if panel.title:
                ax.set_title(
                    panel.title,
                    fontsize=self.theme.title_font_size,
                    color=self.theme.title_color,
                    fontfamily=self.theme.font_family,
                    pad=10,
                )
            if panel.xlabel:
                ax.set_xlabel(
                    panel.xlabel,
                    fontsize=self.theme.label_font_size,
                    color=self.theme.text_color,
                    fontfamily=self.theme.font_family,
                )
            if panel.ylabel:
                ax.set_ylabel(
                    panel.ylabel,
                    fontsize=self.theme.label_font_size,
                    color=self.theme.text_color,
                    fontfamily=self.theme.font_family,
                )
            
            # Collect legend handles/labels
            handles, labels = ax.get_legend_handles_labels()
            for handle, label in zip(handles, labels):
                if label not in all_labels:
                    all_handles.append(handle)
                    all_labels.append(label)
        
        # Add shared legend if enabled
        if self.layout.shared_legend and all_handles:
            self._add_shared_legend(fig, all_handles, all_labels)
        
        # Add dashboard title
        if self.title:
            fig.suptitle(
                self.title,
                fontsize=self.theme.title_font_size + 2,
                color=self.theme.title_color,
                fontfamily=self.theme.font_family,
                y=self.layout.title_y,
            )
        
        # Adjust layout to fit legend and title
        self._adjust_layout(fig)
        
        return fig

    def _create_panel_chart(self, panel: PanelConfig) -> Any:
        """
        Create a chart instance for a panel.
        
        Args:
            panel: Panel configuration
            
        Returns:
            Chart instance (BarChart, LineChart, TimeSeriesChart, etc.)
        """
        chart_type = panel.chart_type.lower()
        
        if chart_type not in CHART_CLASSES:
            raise ValueError(
                f"Unknown chart type '{chart_type}'. "
                f"Available: {', '.join(CHART_CLASSES.keys())}"
            )
        
        chart_class = CHART_CLASSES[chart_type]
        
        # Get style for this chart type
        style = self._style_registry.get_style(chart_type, panel.style)
        
        # Create chart instance
        return chart_class(
            data=panel.data,
            style=style,
            theme=self.theme,
            title=panel.title,
            xlabel=panel.xlabel,
            ylabel=panel.ylabel,
        )

    def _add_shared_legend(
        self,
        fig: Figure,
        handles: list,
        labels: list,
    ) -> None:
        """
        Add a shared legend to the figure.
        
        Args:
            fig: matplotlib Figure
            handles: Legend handles from all panels
            labels: Legend labels from all panels
        """
        # Determine legend location based on position setting
        loc_map = {
            "top": "upper center",
            "bottom": "lower center",
            "right": "center right",
        }
        loc = loc_map.get(self.layout.legend_position, "upper center")
        
        # Determine bbox_to_anchor based on position
        bbox_map = {
            "top": (0.5, 1.02),
            "bottom": (0.5, -0.05),
            "right": (1.02, 0.5),
        }
        bbox = bbox_map.get(self.layout.legend_position, (0.5, 1.02))
        
        # Determine ncol based on position
        ncol = len(handles) if self.layout.legend_position in ["top", "bottom"] else 1
        
        legend = fig.legend(
            handles,
            labels,
            loc=loc,
            bbox_to_anchor=bbox,
            ncol=ncol,
            fontsize=self.theme.legend_font_size,
            framealpha=0.9,
            facecolor=self.theme.background_color,
            edgecolor=self.theme.grid_color,
        )
        
        # Set legend text color
        for text in legend.get_texts():
            text.set_color(self.theme.text_color)

    def _adjust_layout(self, fig: Figure) -> None:
        """
        Adjust figure layout to accommodate legend and title.
        
        Args:
            fig: matplotlib Figure
        """
        import warnings
        
        # Adjust margins based on legend position
        rect_map = {
            "top": [0.05, 0.05, 0.95, 0.88],
            "bottom": [0.05, 0.12, 0.95, 0.92],
            "right": [0.05, 0.05, 0.85, 0.92],
        }
        
        if self.layout.shared_legend:
            rect = rect_map.get(self.layout.legend_position, [0.05, 0.05, 0.95, 0.88])
        else:
            rect = [0.05, 0.05, 0.95, 0.95]
        
        # Add space for dashboard title
        if self.title:
            rect[3] = min(rect[3], 0.92)
        
        # Suppress tight_layout warning (common with GridSpec)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                fig.tight_layout(rect=rect)
            except Exception:
                # Fall back to subplots_adjust if tight_layout fails
                fig.subplots_adjust(
                    left=rect[0], bottom=rect[1], 
                    right=rect[2], top=rect[3]
                )

