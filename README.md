# Aesthetic QR Code Generator

## Description
A professional Python application for generating beautiful, customizable QR codes with logos. Built following SOLID principles with comprehensive test coverage.

## Features

✨ **Aesthetic Design Options**
- Multiple preset styles (Standard, Modern, Vibrant, Elegant)
- Circular dots, rounded squares, and standard module styles
- Full color customization for foreground and background
- Configurable logo shapes (circular, square, rounded square)

🏗️ **SOLID Architecture**
- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed**: Extensible through interfaces, closed for modification
- **Liskov Substitution**: All implementations are interchangeable
- **Interface Segregation**: Small, focused interfaces
- **Dependency Inversion**: Depends on abstractions, not concrete classes

✅ **Fully Tested**
- Comprehensive unit tests for all components
- Integration tests for end-to-end generation
- 40+ test cases with 100% pass rate

🎨 **Highly Configurable**
- Size and quality settings
- Border customization
- Logo scaling options
- Error correction levels (L, M, Q, H)

## Installation

```bash
# Clone the repository
git clone https://github.com/phdwight/barcodemem.git

# Navigate to the project directory
cd barcodemem

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Quick Start with Presets

```bash
# Modern style (blue circular dots)
python -m src.cli --data "https://example.com" --logo logo.png --output qr.png --preset modern

# Vibrant style (bold red/yellow)
python -m src.cli --data "https://example.com" --logo logo.png --output qr.png --preset vibrant

# Elegant style (subtle gray rounded squares)
python -m src.cli --data "https://example.com" --logo logo.png --output qr.png --preset elegant

# Standard style (classic black squares)
python -m src.cli --data "https://example.com" --logo logo.png --output qr.png --preset standard
```

### Custom Styling

```bash
# Custom colors with circular dots
python -m src.cli --data "https://example.com" \
  --logo logo.png \
  --style circular \
  --fg-color "#059669" \
  --bg-color "white" \
  --output qr.png

# Rounded squares without logo
python -m src.cli --data "https://example.com" \
  --no-logo \
  --style rounded \
  --fg-color "#7c3aed" \
  --bg-color "#faf5ff" \
  --output qr.png

# Custom logo shape and size
python -m src.cli --data "https://example.com" \
  --logo logo.png \
  --logo-shape square-rounded \
  --logo-scale 4.0 \
  --output qr.png
```

### All Available Options

```bash
python -m src.cli --help
```

**Required:**
- `--data`: Data to encode (URL, text, etc.)

**Output:**
- `--output`, `-o`: Output file path (default: qrcode.png)

**Logo:**
- `--logo`, `-l`: Path to logo image
- `--no-logo`: Generate without logo
- `--logo-shape`: circular, square, or square-rounded (default: circular)
- `--logo-scale`: Logo size divisor (larger = smaller logo, default: 3.5)

**Style:**
- `--preset`, `-p`: Use preset (standard, modern, vibrant, elegant)
- `--style`: Module style (standard, circular, rounded)
- `--fg-color`: Foreground color (default: black)
- `--bg-color`: Background color (default: white)

**Quality:**
- `--size`: Box size for QR modules (default: 10)
- `--border`: Border size in modules (default: 4)
- `--quality`: JPEG quality 1-100 (default: 95)
- `--error-correction`, `-e`: L, M, Q, or H (default: H)

## Examples Gallery

### Preset Styles

**Standard**: Classic black and white QR code
![Standard](output_standard.png)

**Modern**: Blue circular dots with white background
![Modern](output_modern.png)

**Vibrant**: Bold red dots on yellow background
![Vibrant](output_vibrant.png)

**Elegant**: Subtle gray rounded squares
![Elegant](output_elegant.png)

## Programmatic Usage

```python
from src.generator import QRCodeGeneratorBuilder

# Use a preset
generator = QRCodeGeneratorBuilder.create_modern()
generator.generate("https://example.com", "logo.png", "output.png")

# Custom configuration
from src.config import AestheticQRConfig
from src.stylers import CircularDotsStyler
from src.logo_processors import CircularLogoProcessor
from src.image_savers import StandardImageSaver

config = AestheticQRConfig(fg_color="#2563eb", bg_color="white")
styler = CircularDotsStyler(fg_color="#2563eb", dot_scale=0.8)
logo_processor = CircularLogoProcessor(logo_scale=3.5)
image_saver = StandardImageSaver(quality=95)

generator = (QRCodeGeneratorBuilder()
             .with_config(config)
             .with_styler(styler)
             .with_logo_processor(logo_processor)
             .with_image_saver(image_saver)
             .build())

generator.generate("https://example.com", "logo.png", "output.png")
```

## Architecture

The project follows SOLID principles with a clean separation of concerns:

- **`interfaces.py`**: Abstract base classes defining contracts
- **`config.py`**: Configuration classes for QR code settings
- **`stylers.py`**: Styling implementations (Standard, Circular, Rounded)
- **`logo_processors.py`**: Logo processing implementations
- **`image_savers.py`**: Image saving with format optimization
- **`generator.py`**: Main generator with builder pattern
- **`cli.py`**: Command-line interface

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/test_generator.py -v
```

## Legacy Code

The original implementations are preserved in:
- `barcode_memory.py`: Original QRCodeGenerator class
- `qrcode_options.py`: Extended version with circular dots
- `neo_barcode.py`: CLI version with module drawers

These are kept for reference but the new architecture in `generator.py` and related files is recommended.