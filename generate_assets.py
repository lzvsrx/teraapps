from PIL import Image, ImageDraw, ImageFont
import os

def generate_logo():
    # Cores
    deep_black = (5, 6, 10)
    neon_purple = (168, 85, 247)
    neon_blue = (59, 130, 246)
    
    # Criar imagem
    size = (512, 512)
    img = Image.new('RGB', size, deep_black)
    draw = ImageDraw.Draw(img)
    
    # Desenhar um gradiente simples ou formas geométricas futuristas
    # Vamos desenhar um "T" estilizado
    # Linha vertical
    draw.rectangle([230, 150, 282, 400], fill=neon_purple)
    # Linha horizontal superior
    draw.rectangle([150, 150, 362, 202], fill=neon_blue)
    
    # Adicionar um brilho (glow) simples
    # (Em uma implementação real usaríamos blur, mas aqui faremos algo geométrico)
    draw.line([140, 140, 372, 140], fill=neon_purple, width=2)
    draw.line([220, 410, 292, 410], fill=neon_blue, width=2)

    # Salvar
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    img.save('assets/logo.png')
    img.save('icon.png') # Para o Buildozer
    print("Logo e ícone gerados em assets/logo.png e icon.png")

if __name__ == '__main__':
    generate_logo()
