import qrcode
from PIL import Image, ImageOps, ImageDraw


class QRCodeGenerator:
    def __init__(self, url, logo_path, output_path, qr_color="black", bg_color="white", dot_scale=0.5, corner_shape="circle", module_shape="heart"):
        self.url = url
        self.logo_path = logo_path
        self.output_path = output_path
        self.qr_color = qr_color
        self.bg_color = bg_color
        self.dot_scale = dot_scale
        self.corner_shape = corner_shape
        self.module_shape = module_shape
        self.qr = None
        self.img = None
        self.logo = None

    def generate_qr_code(self):
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        self.qr.add_data(self.url)
        self.qr.make(fit=True)
        self.img = self.qr.make_image(fill=self.qr_color, back_color=self.bg_color)
        self.img = self.img.convert("RGBA")

        # Create a new image to draw shapes
        new_img = Image.new("RGBA", self.img.size, self.bg_color)
        draw = ImageDraw.Draw(new_img)

        # Get the size of the QR code modules
        module_size = self.img.size[0] // self.qr.modules_count

        # Calculate the size of the dots
        dot_size = module_size * self.dot_scale

        # Calculate the offset to center the dots
        offset = (module_size - dot_size) / 2

        # Define the corner square positions
        corner_positions = [
            (0, 0),
            (0, self.qr.modules_count - 7),
            (self.qr.modules_count - 7, 0),
        ]

        # Draw shapes for each QR code module
        for r in range(self.qr.modules_count):
            for c in range(self.qr.modules_count):
                if self.qr.modules[r][c]:
                    # Check if the current module is part of the corner squares
                    is_corner = any(
                        r in range(corner[0], corner[0] + 7) and c in range(corner[1], corner[1] + 7)
                        for corner in corner_positions
                    )
                    if is_corner:
                        if self.corner_shape == "circle":
                            upper_left = (
                                c * module_size + offset,
                                r * module_size + offset,
                            )
                            lower_right = (
                                (c + 1) * module_size - offset,
                                (r + 1) * module_size - offset,
                            )
                            draw.ellipse([upper_left, lower_right], fill=self.qr_color)
                        elif self.corner_shape == "square":
                            upper_left = (c * module_size, r * module_size)
                            lower_right = ((c + 1) * module_size, (r + 1) * module_size)
                            draw.rectangle([upper_left, lower_right], fill=self.qr_color)
                    else:
                        if self.module_shape == "heart":
                            # Draw a heart shape
                            center_x = c * module_size + module_size / 2
                            center_y = r * module_size + module_size / 2
                            heart_size = dot_size / 2
                            points = [
                                (center_x, center_y - heart_size),
                                (center_x - heart_size, center_y),
                                (center_x, center_y + heart_size),
                                (center_x + heart_size, center_y),
                            ]
                            draw.polygon(points, fill=self.qr_color)
                        elif self.module_shape == "circle":
                            upper_left = (
                                c * module_size + offset,
                                r * module_size + offset,
                            )
                            lower_right = (
                                (c + 1) * module_size - offset,
                                (r + 1) * module_size - offset,
                            )
                            draw.ellipse([upper_left, lower_right], fill=self.qr_color)

        self.img = new_img

    def open_logo(self):
        self.logo = Image.open(self.logo_path)
        # Create a mask to make the logo circular
        mask = Image.new("L", self.logo.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + self.logo.size, fill=255)
        self.logo = ImageOps.fit(self.logo, mask.size, centering=(0.5, 0.5))
        self.logo.putalpha(mask)

    def paste_logo(self):
        img_w, img_h = self.img.size
        logo_w, logo_h = self.logo.size
        pos_w = (img_w - logo_w) // 2
        pos_h = (img_h - logo_h) // 2
        # Use the mask when pasting the logo
        self.img.paste(
            self.logo, (pos_w, pos_h, pos_w + logo_w, pos_h + logo_h), self.logo
        )

    def scale_logo(self):
        img_w, img_h = self.img.size
        logo_w, logo_h = self.logo.size
        scale = min(img_w / logo_w, img_h / logo_h) / 3.5
        new_w = int(logo_w * scale)
        new_h = int(logo_h * scale)
        self.logo = self.logo.resize((new_w, new_h))

    def save_image(self):
        self.img.save(self.output_path)

    def generate(self):
        self.generate_qr_code()
        self.open_logo()
        self.scale_logo()
        self.paste_logo()
        self.save_image()


class QRCodeBuilder:
    def __init__(self, fill_color="purple", back_color="white", dot_scale=0.5):
        self.fill_color = fill_color
        self.back_color = back_color
        self.dot_scale = dot_scale
        self.reset()

    # ...

    def set_url(self, url):
        self.qr.add_data(url)
        self.qr.make(fit=True)
        self.img = self.qr.make_image(fill=self.fill_color, back_color=self.back_color)
        self.img = self.img.convert("RGBA")

        # Create a new image to draw circles
        new_img = Image.new("RGBA", self.img.size, self.back_color)
        draw = ImageDraw.Draw(new_img)

        # Get the size of the QR code modules
        module_size = self.img.size[0] // self.qr.modules_count

        # Calculate the size of the dots
        dot_size = module_size * self.dot_scale

        # Draw a circle for each QR code module
        for r in range(self.qr.modules_count):
            for c in range(self.qr.modules_count):
                if self.qr.modules[r][c]:
                    upper_left = (
                        c * module_size + dot_size / 2,
                        r * module_size + dot_size / 2,
                    )
                    lower_right = (
                        (c + 1) * module_size - dot_size / 2,
                        (r + 1) * module_size - dot_size / 2,
                    )
                    draw.ellipse([upper_left, lower_right], fill=self.fill_color)

        self.img = new_img

        return self


# Usage
generator = QRCodeGenerator(
    url="https://www.youtube.com/embed/5uX2YXvF1to?autoplay=1&fs=1",
    logo_path="src/church.png",
    output_path="qrcode.png",
    qr_color="teal",
    bg_color="white",
    dot_scale=0.5,
    corner_shape="circle",
    module_shape="heart"
)
generator.generate()
