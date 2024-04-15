import qrcode
from PIL import Image, ImageOps, ImageDraw

# The URL that you want the barcode to open
url = 'https://youtube.com'

# Generate the QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=2,  # Reduce the border thickness
)
qr.add_data(url)
qr.make(fit=True)

# Create an image from the QR code instance with custom colors
img = qr.make_image(fill='purple', back_color='white')

# Convert the image mode to 'RGBA'
img = img.convert('RGBA')

# Open the overlay image (the image to put at the center). 
# Make sure it's in the same directory as your script, or provide the full path.
logo = Image.open('src/church.png')

# Calculate dimensions of QR code and logo
img_w, img_h = img.size
logo_w, logo_h = logo.size

# Scale logo to fit into QR code
scale = min(img_w / logo_w, img_h / logo_h) / 3.5
new_w = int(logo_w * scale)
new_h = int(logo_h * scale)
logo = logo.resize((new_w, new_h))

# Calculate position for new logo
pos_w = (img_w - new_w) // 2
pos_h = (img_h - new_h) // 2

# Paste the logo into the QR code
img.paste(logo, (pos_w, pos_h, pos_w + new_w, pos_h + new_h))

# Create a mask for the rounded corners
mask = Image.new('L', img.size, 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0) + img.size, fill=255)

# Apply the mask to the QR code
img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
img.putalpha(mask)

# Save the image
img.save('qrcode.png')