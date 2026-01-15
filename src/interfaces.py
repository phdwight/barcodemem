"""Abstract base classes and interfaces for QR code generation following SOLID principles."""

from abc import ABC, abstractmethod
from typing import Tuple
from PIL import Image


class QRCodeStyler(ABC):
    """Interface for styling QR codes (Open/Closed Principle)."""

    @abstractmethod
    def apply_style(self, qr_image: Image.Image, modules, modules_count: int) -> Image.Image:
        """Apply styling to the QR code image."""
        pass


class LogoProcessor(ABC):
    """Interface for processing and adding logos to QR codes (Single Responsibility)."""

    @abstractmethod
    def process_logo(self, logo_path: str, qr_size: Tuple[int, int]) -> Image.Image:
        """Process and prepare logo for QR code."""
        pass

    @abstractmethod
    def paste_logo(self, qr_image: Image.Image, logo: Image.Image) -> Image.Image:
        """Paste processed logo onto QR code."""
        pass


class QRCodeConfig(ABC):
    """Interface for QR code configuration (Dependency Inversion)."""

    @abstractmethod
    def get_version(self) -> int:
        """Get QR code version."""
        pass

    @abstractmethod
    def get_error_correction(self):
        """Get error correction level."""
        pass

    @abstractmethod
    def get_box_size(self) -> int:
        """Get box size."""
        pass

    @abstractmethod
    def get_border(self) -> int:
        """Get border size."""
        pass

    @abstractmethod
    def get_colors(self) -> Tuple[str, str]:
        """Get foreground and background colors."""
        pass


class ImageSaver(ABC):
    """Interface for saving images (Single Responsibility)."""

    @abstractmethod
    def save(self, image: Image.Image, output_path: str, **kwargs) -> None:
        """Save image to file."""
        pass
