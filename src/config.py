"""Configuration classes for QR code generation."""

import qrcode
from typing import Tuple, Optional
from src.interfaces import QRCodeConfig


class StandardQRConfig(QRCodeConfig):
    """Standard QR code configuration with sensible defaults."""

    def __init__(
        self,
        version: int = 1,
        error_correction: str = "H",
        box_size: int = 10,
        border: int = 4,
        fg_color: str = "black",
        bg_color: str = "white"
    ):
        self.version = version
        self.error_correction_level = self._get_error_correction(error_correction)
        self.box_size = box_size
        self.border = border
        self.fg_color = fg_color
        self.bg_color = bg_color

    def _get_error_correction(self, level: str):
        """Map error correction level string to qrcode constant."""
        levels = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H,
        }
        return levels.get(level, qrcode.constants.ERROR_CORRECT_H)

    def get_version(self) -> int:
        return self.version

    def get_error_correction(self):
        return self.error_correction_level

    def get_box_size(self) -> int:
        return self.box_size

    def get_border(self) -> int:
        return self.border

    def get_colors(self) -> Tuple[str, str]:
        return self.fg_color, self.bg_color


class AestheticQRConfig(StandardQRConfig):
    """Enhanced configuration with additional aesthetic options."""

    def __init__(
        self,
        version: int = 1,
        error_correction: str = "H",
        box_size: int = 10,
        border: int = 4,
        fg_color: str = "black",
        bg_color: str = "white",
        border_color: Optional[str] = None,
        rounded_corners: bool = False,
        dot_scale: float = 1.0
    ):
        super().__init__(version, error_correction, box_size, border, fg_color, bg_color)
        self.border_color = border_color or bg_color
        self.rounded_corners = rounded_corners
        self.dot_scale = dot_scale

    def get_border_color(self) -> str:
        return self.border_color

    def has_rounded_corners(self) -> bool:
        return self.rounded_corners

    def get_dot_scale(self) -> float:
        return self.dot_scale
