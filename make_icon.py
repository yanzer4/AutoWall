from PIL import Image, ImageDraw, ImageFont

sizes = [16, 32, 48, 256]
images = []

for size in sizes:
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    margin = size // 8
    draw.ellipse([margin, margin, size - margin, size - margin], fill=(15, 118, 110, 255))
    font_size = max(size // 3, 8)
    try:
        font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', font_size)
    except Exception:
        font = ImageFont.load_default()
    text = 'AW'
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (size - tw) // 2
    y = (size - th) // 2
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    images.append(img)

images[0].save('autowall.ico', format='ICO', sizes=[(s, s) for s in sizes], append_images=images[1:])
print('Icone criado: autowall.ico')
