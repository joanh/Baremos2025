#!/usr/bin/env python3
"""
Visualizador de Baremos - Informática 107 (VERSIÓN LIMPIA)
Genera gráficos profesionales con estadísticas completas

Autor: @joanh
Asistente: Claude Sonnet 4.0
"""

import os
import sys
import yaml
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.colors as mcolors
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
    
    # Intentar cargar desde el archivo Python generado
    lista_py = OUTPUT_DIR / "lista_informatica_107.py"
    
    if lista_py.exists():
        try:
            # Leer y ejecutar el archivo Python
            with open(lista_py, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Crear un namespace local para exec
            namespace = {}
            exec(contenido, namespace)
            
            if 'puntuaciones_informatica' in namespace:
                datos = namespace['puntuaciones_informatica']
                print(f"✅ Datos cargados desde Python: {len(datos)} candidatos")
                return np.array(datos)
        except Exception as e:
            print(f"⚠️ Error leyendo archivo Python: {e}")
    
    print("❌ No se pueden cargar los datos")
    print("🔄 Ejecuta primero: python extractor_informatica.py")
    return None

def main():
    """Función principal"""
    print("🎨 Iniciando visualizador LIMPIO de Informática 107...")
    
    # Cargar configuración
    config = cargar_configuracion()
    
    # Cargar datos
    puntuaciones = cargar_datos()
    
    if puntuaciones is None:
        print("❌ Visualización fallida: No hay datos")
        sys.exit(1)
    
    # Mostrar estadísticas básicas
    print(f"📊 Total candidatos: {len(puntuaciones)}")
    print(f"📈 Media: {np.mean(puntuaciones):.4f}")
    print(f"📊 Mediana: {np.median(puntuaciones):.4f}")
    print(f"📐 Desviación estándar: {np.std(puntuaciones):.4f}")
    
    # CONFIGURACIÓN DE GRÁFICOS
    plt.style.use('default')
    plt.rcParams['font.size'] = 12
    
    # CREAR FIGURA CON 2 SUBPLOTS (1x2)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Baremo Informática 2025 - Comunidad de Madrid', 
                 fontsize=16, fontweight='bold', y=0.95)
    
    # 1. HISTOGRAMA - DISTRIBUCIÓN DE PUNTUACIONES
    ax1.hist(puntuaciones, bins=25, alpha=0.7, color='steelblue', 
             edgecolor='black', linewidth=1)
    
    # Curva de distribución normal superpuesta (escalada)
    mu, sigma = stats.norm.fit(puntuaciones)
    x = np.linspace(0, 10, 100)
    y_normal = stats.norm.pdf(x, mu, sigma)
    # Escalar la curva normal para que coincida con el histograma
    scale_factor = len(puntuaciones) * (10 / 25)  # ajustar según bins
    y_normal_scaled = y_normal * scale_factor
    ax1.plot(x, y_normal_scaled, 'red', linewidth=3, 
             label='Distribución Normal\nμ={:.2f}, σ={:.2f}'.format(mu, sigma))
    
    ax1.set_xlabel('Puntuación (0-10)', fontweight='bold')
    ax1.set_ylabel('Número de Candidatos', fontweight='bold')
    ax1.set_title('Distribución de Puntuaciones', fontweight='bold', pad=20)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 10)
    
    # Líneas de referencia
    ax1.axvline(np.mean(puntuaciones), color='red', linestyle='--', alpha=0.8, linewidth=2)
    ax1.axvline(np.median(puntuaciones), color='green', linestyle='--', alpha=0.8, linewidth=2)
    
    # Texto con estadísticas clave
    stats_text = 'Media: {:.2f}\n'.format(np.mean(puntuaciones))
    stats_text += 'Mediana: {:.2f}\n'.format(np.median(puntuaciones))
    stats_text += 'Desv. Est.: {:.2f}\n'.format(np.std(puntuaciones))
    stats_text += 'Total: {} candidatos'.format(len(puntuaciones))
    ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes, 
             bbox=dict(boxstyle="round,pad=0.4", facecolor="wheat", alpha=0.9),
             verticalalignment='top', fontsize=10, fontweight='bold')
    
    # 2. CANDIDATOS POR RANGO CON GRADIENTE DE COLOR
    rangos = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10)]
    rangos_nombres = ['0-2', '2-4', '4-6', '6-8', '8-10']
    rangos_counts = []
    rangos_porcentajes = []
    
    for min_r, max_r in rangos:
        count = np.sum((puntuaciones >= min_r) & (puntuaciones < max_r))
        porcentaje = (count / len(puntuaciones)) * 100
        rangos_counts.append(count)
        rangos_porcentajes.append(porcentaje)
    
    # Crear gradiente de color basado en porcentajes
    norm = mcolors.Normalize(vmin=min(rangos_porcentajes), vmax=max(rangos_porcentajes))
    colormap = plt.cm.RdYlBu_r  # Rojo para pocos, azul para muchos
    
    # Crear barras con gradiente
    bars = ax2.bar(rangos_nombres, rangos_counts, 
                   color=[colormap(norm(p)) for p in rangos_porcentajes],
                   edgecolor='black', linewidth=1.5, alpha=0.8)
    
    ax2.set_xlabel('Rango de Puntuaciones', fontweight='bold')
    ax2.set_ylabel('Número de Candidatos', fontweight='bold')
    ax2.set_title('Distribución por Rangos de Puntuación', fontweight='bold', pad=20)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Añadir valores y porcentajes en las barras
    for bar, count, porcentaje in zip(bars, rangos_counts, rangos_porcentajes):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(rangos_counts)*0.01,
                 '{}\n({:.1f}%)'.format(count, porcentaje),
                 ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Añadir barra de color para explicar el gradiente
    sm = plt.cm.ScalarMappable(cmap=colormap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax2, shrink=0.6, aspect=20)
    cbar.set_label('Porcentaje de Candidatos (%)', rotation=270, labelpad=20, fontweight='bold')
    
    # AUTOR
    fig.text(0.99, 0.01, '@joanh', fontsize=10, color='gray', alpha=0.7, 
             ha='right', va='bottom', style='italic', weight='bold')
    
    plt.tight_layout()
    
    # Crear directorio de salida si no existe
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Guardar gráficos
    png_path = OUTPUT_DIR / "baremo_informatica_107_2025.png"
    pdf_path = OUTPUT_DIR / "baremo_informatica_107_2025.pdf"
    
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')
    
    print(f"\n💾 Gráficos guardados:")
    print(f"   - {png_path.name}")
    print(f"   - {pdf_path.name}")
    
    # Mostrar gráfico
    plt.show()
    
    print(f"\n🎉 VISUALIZACIÓN COMPLETADA")
    print(f"📈 {len(puntuaciones)} candidatos analizados")
    print(f"📊 Gráficos profesionales generados")
    print(f"✍️ Análisis realizado por @joanh")

if __name__ == "__main__":
    main()
