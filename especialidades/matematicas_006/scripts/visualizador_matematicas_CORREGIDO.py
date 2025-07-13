#!/usr/bin/env python3
"""
Visualizador de Baremos - Matemáticas 006 (CORREGIDO)
Genera gráficos profesionales sin solapamientos con media y mediana visibles

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
    lista_py = OUTPUT_DIR / "lista_matematicas_006.py"
    
    if lista_py.exists():
        try:
            # Leer y ejecutar el archivo Python
            with open(lista_py, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Crear un namespace local para exec
            namespace = {}
            exec(contenido, namespace)
            
            if 'puntuaciones_matematicas' in namespace:
                datos = namespace['puntuaciones_matematicas']
                print(f"✅ Datos cargados desde Python: {len(datos)} candidatos")
                return np.array(datos)
        except Exception as e:
            print(f"❌ Error ejecutando archivo Python: {e}")
    
    # Fallback: intentar CSV
    csv_path = OUTPUT_DIR / "puntuaciones_matematicas_006.csv"
    if csv_path.exists():
        try:
            import pandas as pd
            df = pd.read_csv(csv_path)
            datos = df['puntuacion'].values
            print(f"✅ Datos cargados desde CSV: {len(datos)} candidatos")
            return datos
        except Exception as e:
            print(f"❌ Error cargando CSV: {e}")
    
    print(f"❌ No se encontraron datos en {OUTPUT_DIR}")
    sys.exit(1)

def main():
    print("🎨 Iniciando visualizador de Matemáticas 006...")
    
    # Cargar datos
    puntuaciones = cargar_datos()
    
    # Estadísticas básicas
    media = np.mean(puntuaciones)
    mediana = np.median(puntuaciones)
    desviacion = np.std(puntuaciones)
    
    print(f"📊 Total candidatos: {len(puntuaciones)}")
    print(f"📈 Media: {media:.4f}")
    print(f"📊 Mediana: {mediana:.4f}")
    print(f"📐 Desviación estándar: {desviacion:.4f}")
    
    # CREAR FIGURA
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Baremo Matemáticas 2025 - Comunidad de Madrid', 
                 fontsize=18, fontweight='bold', y=0.95)
    
    # 1. HISTOGRAMA LIMPIO - RANGO LIMITADO A 0-10
    counts, bins, patches = ax1.hist(puntuaciones, bins=25, alpha=0.8, 
                                    color='steelblue', edgecolor='white', linewidth=0.8,
                                    range=(0, 10))
    
    # Curva normal superpuesta CORREGIDA - LIMITADA AL RANGO 0-10
    mu, sigma = stats.norm.fit(puntuaciones)
    x = np.linspace(0, 10, 100)  # FORZAR RANGO 0-10
    y_normal = stats.norm.pdf(x, mu, sigma)
    
    # Escalar correctamente la curva normal
    bin_width = 10.0 / 25  # USAR RANGO FIJO 0-10
    scale_factor = len(puntuaciones) * bin_width
    y_scaled = y_normal * scale_factor
    
    ax1.plot(x, y_scaled, 'red', linewidth=2.5, alpha=0.9,
             label=f'Distribución Normal μ={mu:.2f}, σ={sigma:.2f}')
    
    # Línea de media VISIBLE
    ax1.axvline(media, color='red', linestyle='--', linewidth=2, alpha=0.8,
               label=f'Media: {media:.2f}')
    
    # Línea de mediana VISIBLE
    ax1.axvline(mediana, color='blue', linestyle='--', linewidth=2, alpha=0.8,
               label=f'Mediana: {mediana:.2f}')
    
    # ETIQUETAS SIN SOLAPAMIENTOS
    ax1.set_title('Distribución de Puntuaciones', fontsize=14, fontweight='bold', pad=15)
    ax1.set_xlabel('Puntuación (0-10)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Número de Candidatos', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # FORZAR LÍMITES DEL EJE X A 0-10
    ax1.set_xlim(0, 10)
    
    # TEXTO INFORMATIVO BIEN POSICIONADO
    textstr = f'Total: {len(puntuaciones)} candidatos'
    ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=11,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # 2. GRÁFICO DE BARRAS POR RANGOS
    ranges = ['0-2', '2-4', '4-6', '6-8', '8-10']
    counts_ranges = [
        np.sum((puntuaciones >= 0) & (puntuaciones < 2)),
        np.sum((puntuaciones >= 2) & (puntuaciones < 4)),
        np.sum((puntuaciones >= 4) & (puntuaciones < 6)),
        np.sum((puntuaciones >= 6) & (puntuaciones < 8)),
        np.sum((puntuaciones >= 8) & (puntuaciones <= 10))
    ]
    
    # Colores profesionales para Matemáticas
    colors = ['#FFA07A', '#DC143C', '#F0E68C', '#DC143C', '#4682B4']
    
    bars = ax2.bar(ranges, counts_ranges, color=colors, alpha=0.8, edgecolor='white', linewidth=1)
    
    # ETIQUETAS EN LAS BARRAS (SIN SOLAPAMIENTOS)
    for i, (bar, count) in enumerate(zip(bars, counts_ranges)):
        height = bar.get_height()
        percentage = (count / len(puntuaciones)) * 100
        
        # Etiqueta ENCIMA de la barra
        ax2.text(bar.get_x() + bar.get_width()/2., height + 10,
                f'{count}\\n({percentage:.1f}%)',
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
    png_path = OUTPUT_DIR / "baremo_matematicas_006_2025.png"
    pdf_path = OUTPUT_DIR / "baremo_matematicas_006_2025.pdf"
    
    plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(pdf_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    plt.close()
    
    print(f"\\n💾 Gráficos guardados:")
    print(f"   - baremo_matematicas_006_2025.png")
    print(f"   - baremo_matematicas_006_2025.pdf")
    
    print(f"\\n🎉 VISUALIZACIÓN COMPLETADA")
    print(f"📈 {len(puntuaciones)} candidatos analizados")
    print(f"📊 Gráficos profesionales generados")
    print(f"✍️ Análisis realizado por @joanh")

if __name__ == "__main__":
    main()
