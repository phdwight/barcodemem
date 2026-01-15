"""Concrete implementations of styling for QR codes."""

from PIL import Image, ImageDraw
from typing import Tuple
from src.interfaces import QRCodeStyler


class StandardStyler(QRCodeStyler):
    """Standard square-based QR code styling."""

    def __init__(self, fg_color: str = "black", bg_color: str = "white"):
        self.fg_color = fg_color
        self.bg_color = bg_color

    def apply_style(self, qr_image: Image.Image, modules, modules_count: int) -> Image.Image:
        """Apply standard styling - no modifications to base QR code."""
        return qr_image


class CircularDotsStyler(QRCodeStyler):
    """Circular dots styling for a modern aesthetic look."""

    def __init__(
        self,
        fg_color: str = "black",
        bg_color: str = "white",
        dot_scale: float = 0.8
    ):
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.dot_scale = max(0.1, min(1.0, dot_scale))  # Clamp between 0.1 and 1.0

    def apply_style(self, qr_image: Image.Image, modules, modules_count: int) -> Image.Image:
        """Apply circular dot styling to QR code."""
        new_img = Image.new("RGBA", qr_image.size, self.bg_color)
        draw = ImageDraw.Draw(new_img)

        module_size = qr_image.size[0] // modules_count
        dot_size = module_size * self.dot_scale
        offset = (module_size - dot_size) / 2

        # Define corner square positions (the three large squares in corners)
        corner_positions = [
            (0, 0),
            (0, modules_count - 7),
            (modules_count - 7, 0),
        ]

        for r in range(modules_count):
            for c in range(modules_count):
                if modules[r][c]:
                    # Check if current module is part of corner squares
                    is_corner = any(
                        r in range(corner[0], corner[0] + 7)
                        and c in range(corner[1], corner[1] + 7)
                        for corner in corner_positions
                    )

                    if is_corner:
                        # Draw solid square for corners (better recognition)
                        upper_left = (c * module_size, r * module_size)
                        lower_right = ((c + 1) * module_size, (r + 1) * module_size)
                        draw.rectangle([upper_left, lower_right], fill=self.fg_color)
                    else:
                        # Draw circular dots for data area
                        upper_left = (
                            c * module_size + offset,
                            r * module_size + offset,
                        )
                        lower_right = (
                            (c + 1) * module_size - offset,
                            (r + 1) * module_size - offset,
                        )
                        draw.ellipse([upper_left, lower_right], fill=self.fg_color)

        return new_img


class RoundedSquareStyler(QRCodeStyler):
    """Rounded square styling for a softer aesthetic."""

    def __init__(
        self,
        fg_color: str = "black",
        bg_color: str = "white",
        corner_radius: float = 0.3
    ):
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.corner_radius = max(0.0, min(0.5, corner_radius))  # Clamp between 0 and 0.5

    def apply_style(self, qr_image: Image.Image, modules, modules_count: int) -> Image.Image:
        """Apply rounded square styling to QR code."""
        new_img = Image.new("RGBA", qr_image.size, self.bg_color)
        draw = ImageDraw.Draw(new_img)

        module_size = qr_image.size[0] // modules_count
        corner_radius = int(module_size * self.corner_radius)

        for r in range(modules_count):
            for c in range(modules_count):
                if modules[r][c]:
                    x0 = c * module_size
                    y0 = r * module_size
                    x1 = (c + 1) * module_size
                    y1 = (r + 1) * module_size

                    # Draw rounded rectangle
                    self._draw_rounded_rectangle(
                        draw, [(x0, y0), (x1, y1)],
                        corner_radius, self.fg_color
                    )

        return new_img

    def _draw_rounded_rectangle(self, draw, bounds, radius, fill):
        """Helper to draw a rounded rectangle."""
        x0, y0 = bounds[0]
        x1, y1 = bounds[1]

        # Draw the main rectangle
        draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
        draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)

        # Draw the four corners as circles
        draw.ellipse([x0, y0, x0 + radius * 2, y0 + radius * 2], fill=fill)
        draw.ellipse([x1 - radius * 2, y0, x1, y0 + radius * 2], fill=fill)
        draw.ellipse([x0, y1 - radius * 2, x0 + radius * 2, y1], fill=fill)
        draw.ellipse([x1 - radius * 2, y1 - radius * 2, x1, y1], fill=fill)
