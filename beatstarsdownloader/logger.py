import os
from typing import Optional

from halo import Halo  # type: ignore
from simple_chalk import chalk  # type: ignore


class DebugLogger:
    """Debug logger that uses Halo spinners for consistent output styling."""

    def __init__(self) -> None:
        self.debug_enabled = self._is_debug_enabled()

    def _is_debug_enabled(self) -> bool:
        """Check if debug logging is enabled via environment variable."""
        debug_value = os.environ.get("BEATSTARS_DEBUG", "").lower()
        return debug_value in ("1", "true", "yes", "on")

    def debug_error(self, message: str, error: Optional[Exception] = None) -> None:
        """Log debug error message with Halo styling if debug is enabled."""
        if not self.debug_enabled:
            return

        error_text = f"DEBUG: {message}"
        if error:
            error_text += f" - {str(error)}"

        # Use Halo to create a consistent debug output style
        with Halo(text=chalk.yellow(error_text), spinner="dots") as halo:
            halo.stop_and_persist(
                symbol=f'{chalk.yellow("🐛")}', text=chalk.yellow.dim(error_text)
            )

    def debug_track_download_error(
        self,
        track_name: str,
        track_number: int,
        total_tracks: int,
        error: Exception,
        url: Optional[str] = None,
    ) -> None:
        """Log debug information for track download errors."""
        if not self.debug_enabled:
            return

        error_details = [
            f"Track {track_number}/{total_tracks}: {track_name}",
            f"Error: {type(error).__name__}: {str(error)}",
        ]

        if url:
            error_details.append(f"URL: {url}")

        debug_message = " | ".join(error_details)

        with Halo(
            text=chalk.yellow(f"DEBUG: Track download error - {debug_message}"),
            spinner="dots",
        ) as halo:
            halo.stop_and_persist(
                symbol=f'{chalk.yellow.dim("🐛")}',
                text=chalk.yellow.dim(f"DEBUG: Track download error - {debug_message}"),
            )


# Global debug logger instance
debug_logger = DebugLogger()
