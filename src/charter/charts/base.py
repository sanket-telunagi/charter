"""
Base chart class providing common functionality for all chart types.
"""

import asyncio
from abc import ABC, abstractmethod
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from charter.themes.base import Theme
from charter.styles.presets import Style
from charter.config.settings import get_settings


class BaseChart(ABC):
    """
    Abstract base class for all chart types.
    
    Provides common functionality for rendering charts with themes
    and styles. Subclasses must implement the _render_sync method.
    
    Attributes:
        data: Chart data dictionary
        style: Style configuration for the chart
        theme: Theme configuration for visual appearance
        title: Optional chart title
        xlabel: Optional x-axis label
        ylabel: Optional y-axis label
    """

    def __init__(
        self,
        data: dict[str, Any],
        style: Style,
        theme: Theme,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
    ) -> None:
        """
        Initialize the base chart.
        
        Args:
            data: Chart data dictionary (structure depends on chart type)
            style: Style configuration
            theme: Theme configuration
            title: Optional chart title
            xlabel: Optional x-axis label
            ylabel: Optional y-axis label
        """
        self.data = data
        self.style = style
        self.theme = theme
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self._settings = get_settings()

    async def render(self) -> Figure:
        """
        Render the chart asynchronously.
        
        Uses asyncio.to_thread to run matplotlib operations
        in a thread pool to avoid blocking the event loop.
        
        Returns:
            Figure: The rendered matplotlib Figure
        """
        return await asyncio.to_thread(self._render_sync)

    @abstractmethod
    def _render_sync(self) -> Figure:
        """
        Synchronous rendering implementation.
        
        Must be implemented by subclasses to create the actual chart.
        
        Returns:
            Figure: The rendered matplotlib Figure
        """
        pass

    def render_to_axes(self, ax: plt.Axes) -> plt.Axes:
        """
        Render the chart to an existing axes (for dashboard embedding).
        
        This method renders the chart content to a provided axes object
        rather than creating a new figure. Useful for multi-panel dashboards.
        
        Args:
            ax: matplotlib Axes to render into
            
        Returns:
            Axes: The axes with rendered content
        """
        # Apply theme to the axes
        self.theme.apply_to_axes(ax)
        
        # Call the subclass-specific axes rendering
        self._render_to_axes_impl(ax)
        
        # Apply labels
        self._apply_labels(ax)
        
        return ax
    
    def _render_to_axes_impl(self, ax: plt.Axes) -> None:
        """
        Subclass-specific axes rendering implementation.
        
        Override this method in subclasses to render chart content
        to a provided axes. Default implementation raises NotImplementedError.
        
        Args:
            ax: matplotlib Axes to render into
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} does not support render_to_axes. "
            "Override _render_to_axes_impl to add support."
        )

    def _create_figure(self) -> tuple[Figure, plt.Axes]:
        """
        Create a new figure and axes with theme applied.
        
        Returns:
            Tuple of (Figure, Axes)
        """
        # Get figsize from settings or theme
        figsize = self._settings.default_figsize or self.theme.figsize
        dpi = self._settings.default_dpi or self.theme.dpi

        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        
        # Apply theme to figure and axes
        self.theme.apply_to_figure(fig)
        self.theme.apply_to_axes(ax)
        
        return fig, ax

    def _apply_labels(self, ax: plt.Axes) -> None:
        """
        Apply title and axis labels to the axes.
        
        Args:
            ax: matplotlib Axes object
        """
        if self.title:
            ax.set_title(
                self.title,
                fontsize=self.theme.title_font_size,
                color=self.theme.title_color,
                fontfamily=self.theme.font_family,
                pad=10,
            )
        
        if self.xlabel:
            ax.set_xlabel(
                self.xlabel,
                fontsize=self.theme.label_font_size,
                color=self.theme.text_color,
                fontfamily=self.theme.font_family,
            )
        
        if self.ylabel:
            ax.set_ylabel(
                self.ylabel,
                fontsize=self.theme.label_font_size,
                color=self.theme.text_color,
                fontfamily=self.theme.font_family,
            )

    def _apply_legend(self, ax: plt.Axes, **kwargs: Any) -> None:
        """
        Apply legend to the axes if needed.
        
        Args:
            ax: matplotlib Axes object
            **kwargs: Additional legend configuration
        """
        handles, labels = ax.get_legend_handles_labels()
        if handles:
            legend = ax.legend(
                fontsize=self.theme.legend_font_size,
                framealpha=0.9,
                **kwargs,
            )
            legend.get_frame().set_facecolor(self.theme.background_color)
            for text in legend.get_texts():
                text.set_color(self.theme.text_color)

    def _finalize_figure(self, fig: Figure) -> Figure:
        """
        Finalize the figure layout.
        
        Args:
            fig: matplotlib Figure to finalize
            
        Returns:
            Figure: The finalized figure
        """
        fig.tight_layout()
        return fig

