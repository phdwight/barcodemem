"""Enhanced CLI for aesthetic QR code generation with presets and interactive mode."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from src.generator import QRCodeGeneratorBuilder
from src.config import StandardQRConfig, AestheticQRConfig
from src.stylers import StandardStyler, CircularDotsStyler, RoundedSquareStyler
from src.logo_processors import CircularLogoProcessor, SquareLogoProcessor, NoLogoProcessor
from src.image_savers import StandardImageSaver


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser with comprehensive options."""
    parser = argparse.ArgumentParser(
        description="Generate aesthetic QR codes with customizable styling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate with modern preset
  python cli.py --data "https://example.com" --logo logo.png --output qr.png --preset modern

  # Generate with custom colors
  python cli.py --data "https://example.com" --fg-color "#2563eb" --bg-color "white" --output qr.png

  # Generate with circular dots and rounded logo
  python cli.py --data "https://example.com" --logo logo.png --style circular --logo-shape square-rounded

  # Generate without logo
  python cli.py --data "https://example.com" --output qr.png --no-logo

Presets:
  standard - Classic QR code with square modules
  modern   - Blue circular dots with white background
  vibrant  - Bold red/yellow color scheme
  elegant  - Subtle gray rounded squares
        """
    )

    # Required arguments
    parser.add_argument(
        "--data",
        required=True,
        help="Data to encode (URL, text, etc.)"
    )

    parser.add_argument(
        "--output",
        "-o",
        default="qrcode.png",
        help="Output file path (default: qrcode.png)"
    )

    # Optional logo
    parser.add_argument(
        "--logo",
        "-l",
        help="Path to logo image"
    )

    parser.add_argument(
        "--no-logo",
        action="store_true",
        help="Generate without logo"
    )

    # Preset configurations
    parser.add_argument(
        "--preset",
        "-p",
        choices=["standard", "modern", "vibrant", "elegant"],
        help="Use a preset style configuration"
    )

    # Styling options
    parser.add_argument(
        "--style",
        choices=["standard", "circular", "rounded"],
        default="standard",
        help="QR code module style (default: standard)"
    )

    parser.add_argument(
        "--logo-shape",
        choices=["circular", "square", "square-rounded"],
        default="circular",
        help="Logo shape (default: circular)"
    )

    # Color options
    parser.add_argument(
        "--fg-color",
        default="black",
        help="Foreground color (default: black)"
    )

    parser.add_argument(
        "--bg-color",
        default="white",
        help="Background color (default: white)"
    )

    # Size and quality options
    parser.add_argument(
        "--size",
        type=int,
        default=10,
        help="Box size for QR modules (default: 10)"
    )

    parser.add_argument(
        "--border",
        type=int,
        default=4,
        help="Border size in modules (default: 4)"
    )

    parser.add_argument(
        "--quality",
        type=int,
        default=95,
        help="JPEG quality 1-100 (default: 95)"
    )

    parser.add_argument(
        "--logo-scale",
        type=float,
        default=3.5,
        help="Logo size scale divisor (larger = smaller logo, default: 3.5)"
    )

    parser.add_argument(
        "--dot-scale",
        type=float,
        default=0.8,
        help="Dot scale for circular style (0.1-1.0, default: 0.8)"
    )

    parser.add_argument(
        "--error-correction",
        "-e",
        choices=["L", "M", "Q", "H"],
        default="H",
        help="Error correction level (default: H - highest)"
    )

    return parser


def generate_from_preset(preset: str, data: str, logo_path: Optional[str], output_path: str):
    """Generate QR code using a preset configuration."""
    if preset == "standard":
        generator = QRCodeGeneratorBuilder.create_standard()
    elif preset == "modern":
        generator = QRCodeGeneratorBuilder.create_modern()
    elif preset == "vibrant":
        generator = QRCodeGeneratorBuilder.create_vibrant()
    elif preset == "elegant":
        generator = QRCodeGeneratorBuilder.create_elegant()
    else:
        raise ValueError(f"Unknown preset: {preset}")

    generator.generate(data, logo_path, output_path)


def generate_from_options(args):
    """Generate QR code from individual options."""
    # Create configuration
    config = AestheticQRConfig(
        box_size=args.size,
        border=args.border,
        fg_color=args.fg_color,
        bg_color=args.bg_color,
        error_correction=args.error_correction,
        dot_scale=args.dot_scale
    )

    # Create styler
    if args.style == "circular":
        styler = CircularDotsStyler(
            fg_color=args.fg_color,
            bg_color=args.bg_color,
            dot_scale=args.dot_scale
        )
    elif args.style == "rounded":
        styler = RoundedSquareStyler(
            fg_color=args.fg_color,
            bg_color=args.bg_color,
            corner_radius=0.3
        )
    else:
        styler = StandardStyler(
            fg_color=args.fg_color,
            bg_color=args.bg_color
        )

    # Create logo processor
    if args.no_logo:
        logo_processor = NoLogoProcessor()
    elif args.logo_shape == "square":
        logo_processor = SquareLogoProcessor(logo_scale=args.logo_scale, rounded=False)
    elif args.logo_shape == "square-rounded":
        logo_processor = SquareLogoProcessor(logo_scale=args.logo_scale, rounded=True)
    else:
        logo_processor = CircularLogoProcessor(logo_scale=args.logo_scale)

    # Create image saver
    image_saver = StandardImageSaver(quality=args.quality, optimize=True)

    # Build generator
    generator = (QRCodeGeneratorBuilder()
                 .with_config(config)
                 .with_styler(styler)
                 .with_logo_processor(logo_processor)
                 .with_image_saver(image_saver)
                 .build())

    # Generate QR code
    logo_path = args.logo if not args.no_logo else None
    generator.generate(args.data, logo_path, args.output)


def main():
    """Main entry point for CLI."""
    parser = create_parser()
    args = parser.parse_args()

    # Validate logo path if provided
    if args.logo and not args.no_logo:
        if not Path(args.logo).exists():
            print(f"Error: Logo file not found: {args.logo}", file=sys.stderr)
            return 1

    # Validate that logo is provided if not using no-logo
    if not args.no_logo and not args.logo and args.preset is None:
        print("Error: Either provide --logo, use --no-logo, or use --preset", file=sys.stderr)
        return 1

    try:
        if args.preset:
            generate_from_preset(args.preset, args.data, args.logo, args.output)
        else:
            generate_from_options(args)

        print(f"✓ QR code generated successfully: {args.output}")
        return 0

    except Exception as e:
        print(f"Error generating QR code: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
