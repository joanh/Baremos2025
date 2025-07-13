#!/usr/bin/env python3
"""
Visualizador de Baremos - Física y Química 007
Genera gráficos profesionales sin solapamientos

Autor: @joanh
Asistente: Claude Sonnet 4.0
"""

import os
import sys
import yaml
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

# Configurar rutas
SCRIPT_DIR = Path(__file__).parent
ESPECIALIDAD_DIR = SCRIPT_DIR.parent
CONFIG_PATH = ESPECIALIDAD_DIR / "config.yaml"
OUTPUT_DIR = ESPECIALIDAD_DIR / "output"

def cargar_configuracion():
    """Carga la configuración desde config.yaml"""
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error cargando configuración: {e}")
        sys.exit(1)

def cargar_datos():
    """Carga los datos extraídos"""
    lista_py = OUTPUT_DIR / "lista_fisica_quimica_007.py"
    
    if lista_py.exists():
        try:
            # Leer y ejecutar el archivo Python
            with open(lista_py, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Crear un namespace local para exec
            namespace = {}
            exec(contenido, namespace)
            
            if 'puntuaciones_fisica_quimica' in namespace:
                datos = namespace['puntuaciones_fisica_quimica']
                print(f"✅ Datos cargados desde Python: {len(datos)} candidatos")
                return np.array(datos)
        except Exception as e:
            print(f"⚠️ Error leyendo archivo Python: {e}")
    
    print("❌ No se pueden cargar los datos")
    print("🔄 Ejecuta primero: python extractor_fisica_quimica.py")
    return None

def main():
    """Función principal"""
    print("🎨 Iniciando visualizador de Física y Química 007...")
    
    # Cargar configuración
    config = cargar_configuracion()
    
    # Cargar datos
    puntuaciones = cargar_datos()
    
    if puntuaciones is None:
        print("❌ Visualización fallida: No hay datos")
        sys.exit(1)
    
    # Estadísticas básicas
    media = np.mean(puntuaciones)
    mediana = np.median(puntuaciones)
    desv_std = np.std(puntuaciones)
    
    print(f"📊 Total candidatos: {len(puntuaciones)}")
    print(f"📈 Media: {media:.4f}")
    print(f"📊 Mediana: {mediana:.4f}")
    print(f"📐 Desviación estándar: {desv_std:.4f}")
    
    # CONFIGURACIÓN VISUAL PROFESIONAL
    plt.style.use('default')
    plt.rcParams.update({
        'font.size': 12,
        'font.family': 'sans-serif',
        'axes.linewidth': 1.2,
        'grid.alpha': 0.3
    })
    
    # CREAR FIGURA
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Baremo Física y Química 2025 - Comunidad de Madrid', 
                 fontsize=18, fontweight='bold', y=0.95)
    
    # 1. HISTOGRAMA LIMPIO
    counts, bins, patches = ax1.hist(puntuaciones, bins=25, alpha=0.8, 
                                    color='darkgreen', edgecolor='white', linewidth=0.8)
    
    # Curva normal superpuesta CORREGIDA
    mu, sigma = stats.norm.fit(puntuaciones)
    x = np.linspace(puntuaciones.min(), puntuaciones.max(), 100)
    y_normal = stats.norm.pdf(x, mu, sigma)
    
    # Escalar correctamente la curva normal
    bin_width = (puntuaciones.max() - puntuaciones.min()) / 25
    scale_factor = len(puntuaciones) * bin_width
    y_scaled = y_normal * scale_factor
    
    ax1.plot(x, y_scaled, 'red', linewidth=2.5, alpha=0.9,
             label=f'Distribución Normal μ={mu:.2f}, σ={sigma:.2f}')
    
    # Línea de media VISIBLE
    ax1.axvline(media, color='red', linestyle='--', linewidth=3, alpha=1.0,
               label=f'Media: {media:.4f}')
    
    # Línea de mediana VISIBLE
    ax1.axvline(mediana, color='blue', linestyle='--', linewidth=3, alpha=1.0,
               label=f'Mediana: {mediana:.4f}')
    
    # ETIQUETAS SIN SOLAPAMIENTOS
    ax1.set_title('Distribución de Puntuaciones', fontsize=14, fontweight='bold', pad=15)
    ax1.set_xlabel('Puntuación (0-10)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Número de Candidatos', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # TEXTO INFORMATIVO BIEN POSICIONADO
    textstr = f'Total: {len(puntuaciones)} candidatos'
    ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=11,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    # 2. GRÁFICO DE BARRAS POR RANGOS
    ranges = ['0-2', '2-4', '4-6', '6-8', '8-10']
    counts_ranges = [
        np.sum((puntuaciones >= 0) & (puntuaciones < 2)),
        np.sum((puntuaciones >= 2) & (puntuaciones < 4)),
        np.sum((puntuaciones >= 4) & (puntuaciones < 6)),
        np.sum((puntuaciones >= 6) & (puntuaciones < 8)),
        np.sum((puntuaciones >= 8) & (puntuaciones <= 10))
    ]
    
    # Colores profesionales para Física y Química
    colors = ['#FFB6C1', '#228B22', '#FFFF99', '#228B22', '#2F4F4F']
    
    bars = ax2.bar(ranges, counts_ranges, color=colors, alpha=0.8, edgecolor='white', linewidth=1)
    
    # ETIQUETAS EN LAS BARRAS (SIN SOLAPAMIENTOS)
    for i, (bar, count) in enumerate(zip(bars, counts_ranges)):
        height = bar.get_height()
        percentage = (count / len(puntuaciones)) * 100
        
        # Etiqueta ENCIMA de la barra
        ax2.text(bar.get_x() + bar.get_width()/2., height + 10,
                f'{count}\n({percentage:.1f}%)',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax2.set_title('Distribución por Rangos de Puntuación', fontsize=14, fontweight='bold', pad=15)
    ax2.set_xlabel('Rango de Puntuaciones', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Número de Candidatos', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # MÁRGENES AJUSTADOS PARA EVITAR CORTES
    ax2.set_ylim(0, max(counts_ranges) * 1.15)
    
    # FIRMA PROFESIONAL
    fig.text(0.99, 0.01, '@joanh', fontsize=10, ha='right', va='bottom', 
             style='italic', alpha=0.7)
    
    # AJUSTAR LAYOUT PARA EVITAR SOLAPAMIENTOS
    plt.tight_layout(rect=[0, 0.03, 1, 0.93])
    
    # GUARDAR ARCHIVOS
    output_config = config['output']
    
    # PNG (alta calidad)
    png_path = OUTPUT_DIR / output_config['grafico']
    plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    # PDF (vectorial)
    pdf_path = OUTPUT_DIR / output_config['grafico'].replace('.png', '.pdf')
    plt.savefig(pdf_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    plt.close()
    
    print(f"\n💾 Gráficos guardados:")
    print(f"   - {output_config['grafico']}")
    print(f"   - {output_config['grafico'].replace('.png', '.pdf')}")
    
    print(f"\n🎉 VISUALIZACIÓN COMPLETADA")
    print(f"📈 {len(puntuaciones)} candidatos analizados")
    print(f"📊 Gráficos profesionales generados")
    print(f"✍️ Análisis realizado por @joanh")

if __name__ == "__main__":
    main()
