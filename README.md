# QR Code Generator with Logo

## Description
A Python script that generates a QR code from a provided URL and embeds a logo image in the center.

## Installation
Instructions on how to install and set up the project.

```bash
# Clone the repository
git clone https://github.com/yourusername/qrcode-generator.git

# Navigate to the project directory
cd qrcode-generator

# Install dependencies
pip install -r requirements.txt
```

## Usage
How to use the project after installation.

# Generate a QR code with a logo
python neo_barcode.py "https://example.com" "path/to/logo.png" "path/to/output.png"

# Optionally, specify a different module drawer type
python neo_barcode.py "https://example.com" "path/to/logo.png" "path/to/output.png" --module_drawer CircleModuleDrawer