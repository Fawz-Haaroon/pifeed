"""Base exceptions for pifeed"""

from __future__ import annotations


class PiFeedException(Exception):
    """Base class for pifeed-related exceptions."""


class ConfigError(PiFeedException):
    """Raised for invalid configuration or environment."""


class StreamError(PiFeedException):
    """Raised for streaming / pipeline level failures."""
