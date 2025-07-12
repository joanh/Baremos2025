#!/usr/bin/env python3
"""
Generador de imagen social preview para Baremos2025
Muestra todas las especialidades con barras horizontales
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pathlib import Path
import yaml

def load_specialties_data():
    """Carga los datos de especialidades desde YAML"""
    config_path = Path(__file__).parent.parent / "config" / "especialidades.yaml"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    specialties = []
    total_candidates = 0
    
    for key, data in config['especialidades'].items():
        if 'total_candidatos' in data:
            # Mapeo de nombres con tildes correctas
            nombres_con_tildes = {
                'FILOSOFIA': 'Filosofía',
                'INFORMATICA': 'Informática', 
                'MATEMATICAS': 'Matemáticas',
                'FISICA_QUIMICA': 'Física y Química',
                'FRANCES': 'Francés',
                'INGLES': 'Inglés',
                'TECNOLOGIA': 'Tecnología',
                'ORIENTACION_EDUCATIVA': 'Orientación Educativa',
                'BIOLOGIA_GEOLOGIA': 'Biología y Geología',
                'GEOGRAFIA_HISTORIA': 'Geografía e Historia',
                'EDUCACION_FISICA': 'Educación Física',
                'LENGUA_LITERATURA': 'Lengua y Literatura'
            }
            
            nombre_formato = nombres_con_tildes.get(data['nombre'], 
                                                   data['nombre'].replace('_', ' ').title())
            
            specialties.append({
                'nombre': nombre_formato,
                'candidatos': data['total_candidatos'],
                'codigo': data['codigo']
            })
            total_candidates += data['total_candidatos']
    
    # Ordenar por número de candidatos (descendente)
    specialties.sort(key=lambda x: x['candidatos'], reverse=True)
    
    return specialties, total_candidates

def create_social_preview():
    """Genera la imagen de social preview con barras horizontales"""
    
    # Configuración de la imagen
    fig_width = 12
    fig_height = 6.3  # Proporción 1.91:1 para redes sociales
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor='#0d1117')
    ax.set_facecolor('#0d1117')
    
    # Cargar datos
    specialties, total_candidates = load_specialties_data()
    
    # Colores vibrantes para las barras
    colors = [
        '#ff6b6b',  # Rojo coral
        '#4ecdc4',  # Turquesa
        '#45b7d1',  # Azul cielo
        '#96ceb4',  # Verde menta
        '#feca57',  # Amarillo dorado
        '#ff9ff3',  # Rosa
        '#54a0ff',  # Azul brillante
        '#5f27cd',  # Violeta
        '#00d2d3',  # Cyan
        '#ff9f43',  # Naranja
        '#7bed9f',  # Verde claro
        '#dda0dd'   # Lavanda
    ]
    
    # Título principal
    fig.text(0.5, 0.95, '⚖️ BAREMOS2025', 
             fontsize=28, weight='bold', color='white', 
             ha='center', va='top')
    
    fig.text(0.5, 0.86, 'Análisis de oposiciones de Secundaria • Comunidad de Madrid', 
             fontsize=14, color='#8b949e', 
             ha='center', va='top')
    
    # Estadísticas principales
    stats_y = 0.78
    
    # Total candidatos
    fig.text(0.25, stats_y, f'{total_candidates:,}', 
             fontsize=24, weight='bold', color='#2ea043', 
             ha='center', va='center')
    fig.text(0.25, stats_y-0.04, 'Candidatos', 
             fontsize=12, color='white', 
             ha='center', va='center')
    
    # Número de especialidades
    fig.text(0.5, stats_y, '12', 
             fontsize=24, weight='bold', color='#ff7b72', 
             ha='center', va='center')
    fig.text(0.5, stats_y-0.04, 'Especialidades', 
             fontsize=12, color='white', 
             ha='center', va='center')
    
    # Porcentaje verificable
    fig.text(0.75, stats_y, '100%', 
             fontsize=24, weight='bold', color='#a5a5f5', 
             ha='center', va='center')
    fig.text(0.75, stats_y-0.04, 'Verificable', 
             fontsize=12, color='white', 
             ha='center', va='center')
    
    # Área para las barras
    bar_area_top = 0.68
    bar_area_bottom = 0.08  # Bajamos hasta abajo sin URL
    bar_area_height = bar_area_top - bar_area_bottom
    bar_height = bar_area_height / len(specialties) * 0.6  # 60% del espacio disponible (más altas)
    bar_spacing = bar_area_height / len(specialties) * 0.4  # 40% para espaciado
    
    # Valor máximo para normalizar barras
    max_candidates = max(spec['candidatos'] for spec in specialties)
    
    # Área disponible para las barras (márgenes izq/der)
    bar_area_left = 0.15
    bar_area_width = 0.7
    
    # Crear barras horizontales
    for i, specialty in enumerate(specialties):
        # Calcular posición Y con espaciado real entre barras
        total_bar_space = bar_area_height / len(specialties)
        y_pos = bar_area_top - (i + 1) * total_bar_space + (total_bar_space - bar_height) / 2
        
        # Ancho de la barra proporcional al número de candidatos
        bar_width = (specialty['candidatos'] / max_candidates) * bar_area_width
        
        # Crear barra
        rect = patches.Rectangle(
            (bar_area_left, y_pos), bar_width, bar_height,
            facecolor=colors[i % len(colors)], 
            alpha=0.8,
            edgecolor='white',
            linewidth=0.5
        )
        ax.add_patch(rect)
        
        # Nombre de la especialidad (a la izquierda)
        specialty_name = specialty['nombre']
        if len(specialty_name) > 20:
            # Dividir nombres largos
            words = specialty_name.split()
            if len(words) > 1:
                specialty_name = f"{words[0]}\n{' '.join(words[1:])}"
        
        fig.text(bar_area_left - 0.02, y_pos + bar_height/2, 
                 specialty_name,
                 fontsize=9, color='white', weight='bold',
                 ha='right', va='center')
        
        # Número de candidatos (fuera de la barra, a la derecha, centrado verticalmente)
        fig.text(bar_area_left + bar_width + 0.02, y_pos + bar_height/2, 
                 f'{specialty["candidatos"]:,}',
                 fontsize=10, color='white', weight='bold',
                 ha='left', va='center')
    
    # Configurar ejes
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Guardar imagen
    output_path = Path(__file__).parent.parent / "social_preview.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='#0d1117', edgecolor='none',
                metadata={'Title': 'Baremos2025 - Análisis Oposiciones Secundaria'})
    
    plt.tight_layout()
    plt.show()
    
    print(f"✅ Imagen social preview generada: {output_path}")
    print(f"📊 Total especialidades: {len(specialties)}")
    print(f"👥 Total candidatos: {total_candidates:,}")

if __name__ == "__main__":
    create_social_preview()
