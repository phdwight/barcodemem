"""Main QR code generator following SOLID principles."""

import qrcode
from PIL import Image
from typing import Optional
from src.interfaces import QRCodeConfig, QRCodeStyler, LogoProcessor, ImageSaver
from src.config import StandardQRConfig, AestheticQRConfig
from src.stylers import StandardStyler, CircularDotsStyler, RoundedSquareStyler
from src.logo_processors import CircularLogoProcessor, SquareLogoProcessor, NoLogoProcessor
from src.image_savers import StandardImageSaver


class QRCodeGenerator:
    """
    Main QR code generator following SOLID principles.

    This class demonstrates:
    - Single Responsibility: Only orchestrates generation, delegates specific tasks
    - Open/Closed: Open for extension through interfaces, closed for modification
    - Liskov Substitution: All implementations can be substituted
    - Interface Segregation: Small, focused interfaces
    - Dependency Inversion: Depends on abstractions, not concrete classes
    """

    def __init__(
        self,
        config: QRCodeConfig,
        styler: QRCodeStyler,
        logo_processor: LogoProcessor,
        image_saver: ImageSaver
    ):
        """
        Initialize generator with dependencies.

        Args:
            config: QR code configuration
            styler: Styling implementation
            logo_processor: Logo processing implementation
            image_saver: Image saving implementation
        """
        self.config = config
        self.styler = styler
        self.logo_processor = logo_processor
        self.image_saver = image_saver

    def generate(
        self,
        data: str,
        logo_path: Optional[str] = None,
        output_path: str = "qrcode.png"
    ) -> None:
        """
        Generate QR code with specified data.

        Args:
            data: Data to encode in QR code
            logo_path: Optional path to logo image
            output_path: Path to save generated QR code
        """
        # Step 1: Generate base QR code
        qr = qrcode.QRCode(
            version=self.config.get_version(),
            error_correction=self.config.get_error_correction(),
            box_size=self.config.get_box_size(),
            border=self.config.get_border(),
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Step 2: Create initial image
        fg_color, bg_color = self.config.get_colors()
        qr_image = qr.make_image(fill_color=fg_color, back_color=bg_color)
        qr_image = qr_image.convert("RGBA")

        # Step 3: Apply styling
        styled_image = self.styler.apply_style(qr_image, qr.modules, qr.modules_count)

        # Step 4: Add logo if provided
        if logo_path:
            logo = self.logo_processor.process_logo(logo_path, styled_image.size)
            if logo:
                styled_image = self.logo_processor.paste_logo(styled_image, logo)

        # Step 5: Save image
        self.image_saver.save(styled_image, output_path)


class QRCodeGeneratorBuilder:
    """
    Builder pattern for creating QRCodeGenerator with various presets.
    Makes it easier to create generators with common configurations.
    """

    def __init__(self):
        self._config = None
        self._styler = None
        self._logo_processor = None
        self._image_saver = None

    def with_config(self, config: QRCodeConfig):
        """Set configuration."""
        self._config = config
        return self

    def with_styler(self, styler: QRCodeStyler):
        """Set styler."""
        self._styler = styler
        return self

    def with_logo_processor(self, processor: LogoProcessor):
        """Set logo processor."""
        self._logo_processor = processor
        return self

    def with_image_saver(self, saver: ImageSaver):
        """Set image saver."""
        self._image_saver = saver
        return self

    def build(self) -> QRCodeGenerator:
        """Build QRCodeGenerator with defaults for any unset components."""
        config = self._config or StandardQRConfig()
        styler = self._styler or StandardStyler()
        logo_processor = self._logo_processor or CircularLogoProcessor()
        image_saver = self._image_saver or StandardImageSaver()

        return QRCodeGenerator(config, styler, logo_processor, image_saver)

    @staticmethod
    def create_standard() -> QRCodeGenerator:
        """Create a standard QR code generator."""
        return (QRCodeGeneratorBuilder()
                .with_config(StandardQRConfig())
                .with_styler(StandardStyler())
                .with_logo_processor(CircularLogoProcessor())
                .with_image_saver(StandardImageSaver())
                .build())

    @staticmethod
    def create_modern() -> QRCodeGenerator:
        """Create a modern QR code generator with circular dots."""
        return (QRCodeGeneratorBuilder()
                .with_config(AestheticQRConfig(
                    fg_color="#2563eb",
                    bg_color="white",
                    dot_scale=0.8
                ))
                .with_styler(CircularDotsStyler(fg_color="#2563eb", bg_color="white", dot_scale=0.8))
                .with_logo_processor(CircularLogoProcessor(logo_scale=3.5))
                .with_image_saver(StandardImageSaver(quality=95))
                .build())

    @staticmethod
    def create_vibrant() -> QRCodeGenerator:
        """Create a vibrant QR code generator with bold colors."""
        return (QRCodeGeneratorBuilder()
                .with_config(AestheticQRConfig(
                    fg_color="#dc2626",
                    bg_color="#fef3c7",
                    dot_scale=0.9
                ))
                .with_styler(CircularDotsStyler(fg_color="#dc2626", bg_color="#fef3c7", dot_scale=0.9))
                .with_logo_processor(SquareLogoProcessor(logo_scale=3.0, rounded=True))
                .with_image_saver(StandardImageSaver(quality=95))
                .build())

    @staticmethod
    def create_elegant() -> QRCodeGenerator:
        """Create an elegant QR code generator with rounded squares."""
        return (QRCodeGeneratorBuilder()
                .with_config(AestheticQRConfig(
                    fg_color="#1f2937",
                    bg_color="#f9fafb",
                    rounded_corners=True
                ))
                .with_styler(RoundedSquareStyler(fg_color="#1f2937", bg_color="#f9fafb", corner_radius=0.3))
                .with_logo_processor(CircularLogoProcessor(logo_scale=4.0))
                .with_image_saver(StandardImageSaver(quality=95))
                .build())
