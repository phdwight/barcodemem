"""Logo processing implementations."""

from PIL import Image, ImageOps, ImageDraw
from typing import Tuple, Optional
from src.interfaces import LogoProcessor


class CircularLogoProcessor(LogoProcessor):
    """Process logo with circular mask and paste onto QR code."""

    def __init__(self, logo_scale: float = 3.5):
        """
        Initialize processor.

        Args:
            logo_scale: Divisor for logo size (larger = smaller logo). Default 3.5.
        """
        self.logo_scale = max(2.0, logo_scale)  # Minimum scale of 2.0

    def process_logo(self, logo_path: str, qr_size: Tuple[int, int]) -> Image.Image:
        """Process logo with circular mask."""
        logo = Image.open(logo_path)

        # Calculate logo size
        qr_width, qr_height = qr_size
        logo_width, logo_height = logo.size
        scale = min(qr_width / logo_width, qr_height / logo_height) / self.logo_scale
        new_width = int(logo_width * scale)
        new_height = int(logo_height * scale)

        # Resize logo
        logo = logo.resize((new_width, new_height), Image.LANCZOS)

        # Create circular mask
        mask = Image.new("L", logo.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + logo.size, fill=255)

        # Apply mask to logo
        logo = ImageOps.fit(logo, mask.size, centering=(0.5, 0.5))
        logo.putalpha(mask)

        return logo

    def paste_logo(self, qr_image: Image.Image, logo: Image.Image) -> Image.Image:
        """Paste logo in center of QR code."""
        qr_width, qr_height = qr_image.size
        logo_width, logo_height = logo.size

        # Calculate position (center)
        pos_x = (qr_width - logo_width) // 2
        pos_y = (qr_height - logo_height) // 2

        # Paste with alpha channel as mask
        qr_image.paste(logo, (pos_x, pos_y), logo)

        return qr_image


class SquareLogoProcessor(LogoProcessor):
    """Process logo with square shape and paste onto QR code."""

    def __init__(self, logo_scale: float = 3.5, rounded: bool = False):
        """
        Initialize processor.

        Args:
            logo_scale: Divisor for logo size (larger = smaller logo). Default 3.5.
            rounded: Whether to use rounded corners. Default False.
        """
        self.logo_scale = max(2.0, logo_scale)
        self.rounded = rounded

    def process_logo(self, logo_path: str, qr_size: Tuple[int, int]) -> Image.Image:
        """Process logo with square shape."""
        logo = Image.open(logo_path)

        # Calculate logo size
        qr_width, qr_height = qr_size
        logo_width, logo_height = logo.size
        scale = min(qr_width / logo_width, qr_height / logo_height) / self.logo_scale
        new_size = int(min(logo_width, logo_height) * scale)

        # Resize to square
        logo = ImageOps.fit(logo, (new_size, new_size), centering=(0.5, 0.5))

        if self.rounded:
            # Create rounded square mask
            mask = Image.new("L", logo.size, 0)
            draw = ImageDraw.Draw(mask)
            radius = new_size // 8
            self._draw_rounded_rectangle(draw, [(0, 0), logo.size], radius, 255)
            logo.putalpha(mask)
        else:
            # Ensure alpha channel exists
            if logo.mode != "RGBA":
                logo = logo.convert("RGBA")

        return logo

    def paste_logo(self, qr_image: Image.Image, logo: Image.Image) -> Image.Image:
        """Paste logo in center of QR code."""
        qr_width, qr_height = qr_image.size
        logo_width, logo_height = logo.size

        # Calculate position (center)
        pos_x = (qr_width - logo_width) // 2
        pos_y = (qr_height - logo_height) // 2

        # Paste with alpha channel as mask
        qr_image.paste(logo, (pos_x, pos_y), logo)

        return qr_image

    def _draw_rounded_rectangle(self, draw, bounds, radius, fill):
        """Helper to draw a rounded rectangle."""
        x0, y0 = bounds[0]
        x1, y1 = bounds[1]

        # Draw the main rectangle
        draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
        draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)

        # Draw the four corners
        draw.ellipse([x0, y0, x0 + radius * 2, y0 + radius * 2], fill=fill)
        draw.ellipse([x1 - radius * 2, y0, x1, y0 + radius * 2], fill=fill)
        draw.ellipse([x0, y1 - radius * 2, x0 + radius * 2, y1], fill=fill)
        draw.ellipse([x1 - radius * 2, y1 - radius * 2, x1, y1], fill=fill)


class NoLogoProcessor(LogoProcessor):
    """No-op processor when no logo is desired."""

    def process_logo(self, logo_path: str, qr_size: Tuple[int, int]) -> Optional[Image.Image]:
        """Return None as no logo is needed."""
        return None

    def paste_logo(self, qr_image: Image.Image, logo: Optional[Image.Image]) -> Image.Image:
        """Return QR image unchanged."""
        return qr_image
