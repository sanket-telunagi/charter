"""
Configuration settings for Charter using pydantic-settings.

All settings can be configured via environment variables with CHARTER_ prefix.
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import field_validator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ChartSettings(BaseSettings):
    """Charter configuration settings loaded from environment variables."""

    # Output configuration
    output_dir: Path = Path("output")
    default_format: Literal["png", "svg", "pdf", "jpeg"] = "png"

    # Theme and style defaults
    default_theme: str = "default"
    default_style: str = "default"

    # Figure settings
    default_dpi: int = 150
    # Use string for env var compatibility, access via default_figsize property
    default_figsize_str: str = "10.0,6.0"

    # File naming
    include_timestamp: bool = True
    include_random_suffix: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="CHARTER_",
        extra="ignore",
    )

    @computed_field
    @property
    def default_figsize(self) -> tuple[float, float]:
        """Parse figsize from comma-separated string."""
        parts = self.default_figsize_str.split(",")
        if len(parts) != 2:
            return (10.0, 6.0)
        try:
            return (float(parts[0].strip()), float(parts[1].strip()))
        except ValueError:
            return (10.0, 6.0)

    @field_validator("output_dir", mode="after")
    @classmethod
    def ensure_output_dir_exists(cls, v: Path) -> Path:
        """Ensure output directory exists."""
        v.mkdir(parents=True, exist_ok=True)
        return v


@lru_cache
def get_settings() -> ChartSettings:
    """
    Get cached settings instance.
    
    Returns:
        ChartSettings: The application settings singleton.
    """
    return ChartSettings()


def reload_settings() -> ChartSettings:
    """
    Reload settings from environment (clears cache).
    
    Returns:
        ChartSettings: Fresh settings instance.
    """
    get_settings.cache_clear()
    return get_settings()

