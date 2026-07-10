from PIL import Image

# Gera autowall.ico a partir do logo oficial (autowall_logo.png).
SOURCE = 'autowall_logo.png'
sizes = [16, 24, 32, 48, 64, 128, 256]

logo = Image.open(SOURCE).convert('RGBA')

# Garante que a imagem seja quadrada, mantendo o logo centralizado.
w, h = logo.size
side = max(w, h)
square = Image.new('RGBA', (side, side), (0, 0, 0, 0))
square.paste(logo, ((side - w) // 2, (side - h) // 2), logo)

images = [square.resize((s, s), Image.LANCZOS) for s in sizes]

images[-1].save(
    'autowall.ico',
    format='ICO',
    sizes=[(s, s) for s in sizes],
    append_images=images[:-1],
)
print('Icone criado: autowall.ico')
