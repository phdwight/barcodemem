import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import GappedSquareModuleDrawer
from PIL import Image
import argparse


def create_barcode_with_logo(
    url, logo_path, output_path, module_drawer=GappedSquareModuleDrawer()
):
    # Generate QR code
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create QR code image with the specified module drawer
    qr_img = qr.make_image(
        image_factory=StyledPilImage, module_drawer=module_drawer
    ).convert("RGB")

    # Open logo image
    logo = Image.open(logo_path)

    # Calculate dimensions for the logo
    qr_width, qr_height = qr_img.size
    logo_size = qr_width // 4
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    # Calculate position to paste the logo
    pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

    # Paste logo onto QR code
    qr_img.paste(logo, pos, mask=logo)

    # Save the final image
    qr_img.save(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a QR code with a logo in the center."
    )
    parser.add_argument("url", help="The URL to encode in the QR code.")
    parser.add_argument("logo_path", help="The path to the logo image.")
    parser.add_argument(
        "output_path", help="The path to save the generated QR code image."
    )
    parser.add_argument(
        "--module_drawer",
        help="The module drawer type to use for the QR code.",
        default="GappedSquareModuleDrawer",
        choices=[
            "GappedSquareModuleDrawer",
            "SquareModuleDrawer",
            "CircleModuleDrawer",
            "VerticalBarsDrawer",
        ],
    )

    args = parser.parse_args()

    # Map string to actual module drawer class
    module_drawer_map = {
        "GappedSquareModuleDrawer": GappedSquareModuleDrawer(),
        "SquareModuleDrawer": qrcode.image.styles.moduledrawers.SquareModuleDrawer(),
        "CircleModuleDrawer": qrcode.image.styles.moduledrawers.CircleModuleDrawer(),
        "VerticalBarsDrawer": qrcode.image.styles.moduledrawers.VerticalBarsDrawer(),
    }

    create_barcode_with_logo(
        args.url,
        args.logo_path,
        args.output_path,
        module_drawer_map[args.module_drawer],
    )
