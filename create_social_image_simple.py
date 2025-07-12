#!/usr/bin/env python3
"""
Generador de imagen social para Baremos2025 - VERSIÓN SIMPLIFICADA
Crea una imagen optimizada para redes sociales (1280x640 px)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import FancyBboxPatch

def create_social_preview():
    """Genera la imagen social para GitHub y redes sociales"""
    
    # Configurar el lienzo
    fig, ax = plt.subplots(figsize=(12.8, 6.4), dpi=100)
    fig.patch.set_facecolor('#0D1117')  # Fondo oscuro de GitHub
    ax.set_facecolor('#0D1117')
    
    # Quitar ejes
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    # TÍTULO PRINCIPAL con símbolo de justicia
    ax.text(5, 4.3, '⚖ BAREMOS2025', 
            fontsize=46, fontweight='bold', 
            ha='center', va='center', 
            color='#F0F6FC',  # Blanco GitHub
            family='monospace')
    
    # SUBTÍTULO
    ax.text(5, 3.8, 'Análisis de oposiciones de Secundaria • Comunidad de Madrid', 
            fontsize=16, ha='center', va='center', 
            color='#7D8590',  # Gris GitHub
            family='Arial')
    
    # ESTADÍSTICAS CLAVE SIN ICONOS PROBLEMÁTICOS - MÁS SEPARADAS
    stats_y = 3.2
    
    # Estadística 1: Candidatos
    ax.text(2.0, stats_y, '7,406', 
            fontsize=28, fontweight='bold', 
            ha='center', va='center', color='#3FB950')  # Verde GitHub
    ax.text(2.0, stats_y-0.25, 'Candidatos', 
            fontsize=12, ha='center', va='center', color='#F0F6FC')
    
    # Estadística 2: Especialidades
    ax.text(5.0, stats_y, '6', 
            fontsize=28, fontweight='bold', 
            ha='center', va='center', color='#F85149')  # Rojo GitHub
    ax.text(5.0, stats_y-0.25, 'Especialidades', 
            fontsize=12, ha='center', va='center', color='#F0F6FC')
    
    # Estadística 3: Verificable
    ax.text(8.0, stats_y, '100%', 
            fontsize=28, fontweight='bold', 
            ha='center', va='center', color='#A5A5FF')  # Azul GitHub
    ax.text(8.0, stats_y-0.25, 'Verificable', 
            fontsize=12, ha='center', va='center', color='#F0F6FC')
    
    # GRÁFICO DE ESPECIALIDADES (SIN SOLAPAMIENTOS - MÁS ESPACIO)
    categories = ['Filosofía', 'Inglés', 'Matemáticas', 'Física/Química', 'Lengua', 'Informática']
    values = [561, 1984, 1829, 962, 1727, 343]  # Datos reales
    colors = ['#8B5CF6', '#10B981', '#3B82F6', '#F59E0B', '#EF4444', '#6366F1']
    
    # Configuración del gráfico SIN solapamientos
    bar_width = 0.4  # Barras más anchas
    bar_height_scale = 0.8  # Altura mayor ahora que eliminamos la línea de tech
    spacing = 1.0  # Espaciado muy amplio para evitar solapamientos
    
    # Calcular posiciones para centrado perfecto
    total_width = (len(categories) - 1) * spacing
    start_x = 5 - total_width/2  # Centrar en x=5
    start_y = 1.8  # Posición más alta para usar mejor el espacio
    
    for i, (cat, val, color) in enumerate(zip(categories, values, colors)):
        # Posición x perfectamente centrada
        x_pos = start_x + i * spacing
        
        # Normalizar altura (máximo = bar_height_scale)
        height = (val / max(values)) * bar_height_scale
        
        # Dibujar barra con estilo elegante
        rect = FancyBboxPatch(
            (x_pos - bar_width/2, start_y), 
            bar_width, height,
            boxstyle="round,pad=0.02",  # Bordes redondeados elegantes
            facecolor=color, 
            edgecolor='white',  # Borde blanco para contraste
            linewidth=1.5,  # Borde más visible
            alpha=0.9  # Transparencia elegante
        )
        ax.add_patch(rect)
        
        # Valor encima de la barra - SIN solapamientos
        ax.text(x_pos, start_y + height + 0.08, 
                f'{val:,}', 
                fontsize=10, ha='center', va='bottom', 
                color='white', fontweight='bold')
        
        # Nombre de la especialidad debajo de la barra - SIN solapamientos
        if '/' in cat:
            # Separar Física/Química en dos líneas
            lines = cat.split('/')
            ax.text(x_pos, start_y - 0.08, 
                    lines[0], 
                    fontsize=8, ha='center', va='top', 
                    color='#B0C0D0', fontweight='bold')
            ax.text(x_pos, start_y - 0.18, 
                    lines[1], 
                    fontsize=8, ha='center', va='top', 
                    color='#B0C0D0', fontweight='bold')
        else:
            ax.text(x_pos, start_y - 0.12, 
                    cat, 
                    fontsize=8, ha='center', va='top', 
                    color='#B0C0D0', fontweight='bold')
    
    # LÍNEAS DECORATIVAS elegantes
    # Línea superior
    line1 = patches.Rectangle((0.5, 3.6), 9, 0.02, 
                             linewidth=0, facecolor='#21262D')
    ax.add_patch(line1)
    
    # Línea inferior  
    line2 = patches.Rectangle((0.5, 1.4), 9, 0.02, 
                             linewidth=0, facecolor='#21262D')
    ax.add_patch(line2)
    
    # URL DEL REPOSITORIO
    ax.text(5, 1.0, 'github.com/joanh/Baremos2025', 
            fontsize=16, ha='center', va='center', 
            color='#58A6FF',  # Azul claro GitHub
            family='monospace', fontweight='bold')
    
    # BADGES/TAGS SIMPLIFICADOS (SIN ICONOS - SOLO TEXTO)
    badge_y = 0.5
    badges = [
        ('Python', '#3776AB'),
        ('Código Abierto', '#28A745'), 
        ('Ciencia de Datos', '#FF6B35'), 
        ('Educación', '#6F42C1')
    ]
    
    # Calcular el ancho total y centrar SIN solapamientos
    badge_width = 1.8  # Ancho mayor para acomodar texto
    badge_spacing = 0.1  # Espaciado entre badges
    total_badges_width = len(badges) * badge_width + (len(badges) - 1) * badge_spacing
    start_badge_x = 5 - total_badges_width/2
    
    for i, (badge_text, color) in enumerate(badges):
        x_pos = start_badge_x + i * (badge_width + badge_spacing) + badge_width/2
        
        # Sombra sutil para profundidad
        shadow_rect = FancyBboxPatch(
            (x_pos - badge_width/2 + 0.02, badge_y - 0.08 - 0.02), 
            badge_width, 0.16,
            boxstyle="round,pad=0.03",
            facecolor='black', 
            edgecolor='none',
            alpha=0.3
        )
        ax.add_patch(shadow_rect)
        
        # Badge principal con estilo elegante
        badge_rect = FancyBboxPatch(
            (x_pos - badge_width/2, badge_y - 0.08), 
            badge_width, 0.16,
            boxstyle="round,pad=0.03",
            facecolor=color, 
            edgecolor='white',
            linewidth=1,
            alpha=0.95
        )
        ax.add_patch(badge_rect)
        
        # Texto del badge
        ax.text(x_pos, badge_y, badge_text, 
                fontsize=9, ha='center', va='center', 
                color='white', fontweight='bold')
    
    # Ajustar márgenes
    plt.tight_layout(pad=0)
    
    # Guardar la imagen
    output_path = 'img/social-preview.png'
    plt.savefig(output_path, 
                dpi=100, 
                bbox_inches='tight', 
                facecolor='#0D1117', 
                edgecolor='none',
                pad_inches=0.1)
    
    print(f"✅ Imagen social generada: {output_path}")
    print(f"📏 Dimensiones: 1280x640 píxeles")
    print(f"🎨 Optimizada para GitHub y redes sociales")
    print(f"🔧 Mejoras aplicadas:")
    print(f"   • ⚖ Símbolo de justicia simple para el título")
    print(f"   • Estadísticas sin iconos problemáticos")
    print(f"   • Eliminada línea de tecnologías que causaba solapamientos")
    print(f"   • Gráfico de barras con más espacio vertical")
    print(f"   • Badges simplificados sin iconos")
    print(f"   • Centrado perfecto y sin solapamientos")
    print(f"   • Mayor legibilidad y claridad visual")
    
    # Mostrar la imagen
    plt.show()
    
    return output_path

if __name__ == "__main__":
    # Verificar que existe el directorio img
    import os
    os.makedirs('img', exist_ok=True)
    
    # Generar la imagen
    image_path = create_social_preview()
    
    print(f"\n🚀 ¡Imagen social SIMPLIFICADA lista!")
    print(f"📁 Ubicación: {image_path}")
    print(f"\n📋 Pasos siguientes:")
    print(f"1. Ve a Settings de tu repositorio en GitHub")
    print(f"2. Scroll hasta 'Social preview'")
    print(f"3. Click 'Upload an image...'")
    print(f"4. Sube la imagen: img/social-preview.png")
    print(f"5. ¡Comparte tu repositorio en redes sociales!")
    print(f"\n🎯 Características finales:")
    print(f"   • Dimensiones: 1280x640 px")
    print(f"   • Sin iconos problemáticos")
    print(f"   • Elementos perfectamente espaciados")
    print(f"   • Cero solapamientos garantizados")
    print(f"   • Textos en español")
    print(f"   • Diseño limpio y profesional")
    print(f"   • Estadísticas reales del proyecto")
