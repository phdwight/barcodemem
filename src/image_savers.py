"""Image saving implementations."""

from PIL import Image
from typing import Optional
from src.interfaces import ImageSaver


class StandardImageSaver(ImageSaver):
    """Standard image saver with format detection and optimization."""

    def __init__(self, quality: int = 95, optimize: bool = True):
        """
        Initialize saver.

        Args:
            quality: JPEG quality (1-100). Default 95.
            optimize: Whether to optimize PNG/JPEG. Default True.
        """
        self.quality = max(1, min(100, quality))
        self.optimize = optimize

    def save(self, image: Image.Image, output_path: str, **kwargs) -> None:
        """Save image with appropriate format and settings."""
        # Determine format from file extension
        ext = output_path.lower().split('.')[-1]

        if ext in ['jpg', 'jpeg']:
            # Convert to RGB for JPEG (no alpha channel)
            if image.mode in ('RGBA', 'LA', 'P'):
                rgb_image = Image.new('RGB', image.size, 'white')
                if image.mode == 'P':
                    image = image.convert('RGBA')
                rgb_image.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
                image = rgb_image

            image.save(
                output_path,
                format='JPEG',
                quality=self.quality,
                optimize=self.optimize,
                **kwargs
            )
        elif ext == 'png':
            # PNG supports alpha channel
            image.save(
                output_path,
                format='PNG',
                optimize=self.optimize,
                **kwargs
            )
        else:
            # Default save
            image.save(output_path, **kwargs)
