#!/usr/bin/env python3
"""
Visualizador de Baremos - Lengua Castellana y Literatura 004
Genera gráficos profesionales sin solapamientos - FORMATO ESTÁNDAR

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
    lista_py = OUTPUT_DIR / "lista_lengua_literatura_004.py"
    
    if lista_py.exists():
        try:
            # Leer y ejecutar el archivo Python
            with open(lista_py, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Crear un namespace local para exec
            namespace = {}
            exec(contenido, namespace)
            
            if 'puntuaciones_lengua_literatura_004' in namespace:
                datos = namespace['puntuaciones_lengua_literatura_004']
                print(f"✅ Datos cargados desde Python: {len(datos)} candidatos")
                return np.array(datos)
        except Exception as e:
            print(f"⚠️ Error leyendo archivo Python: {e}")
    
    print("❌ No se pueden cargar los datos")
    print("🔄 Ejecuta primero: python extractor_lengua_literatura_FINAL.py")
    return None

def main():
    """Función principal"""
    print("🎨 Iniciando visualizador de Lengua Castellana y Literatura 004...")
    
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
    fig.suptitle('Baremo Lengua Castellana y Literatura 2025 - Comunidad de Madrid', 
                 fontsize=16, fontweight='bold', y=0.96)
    
    # 1. HISTOGRAMA LIMPIO
    counts, bins, patches = ax1.hist(puntuaciones, bins=25, alpha=0.8, 
                                    color='#2E8B57', edgecolor='white', linewidth=0.8)
    
    # Curva normal superpuesta CORREGIDA
    x_norm = np.linspace(min(puntuaciones), max(puntuaciones), 100)
    y_norm = stats.norm.pdf(x_norm, media, desv_std)
    # Escalar la curva normal para que coincida con el histograma
    factor_escala = len(puntuaciones) * (bins[1] - bins[0])
    y_norm_escalada = y_norm * factor_escala
    ax1.plot(x_norm, y_norm_escalada, 'r-', linewidth=2, 
            label=f'Distribución Normal μ={media:.2f}, σ={desv_std:.2f}')
    
    # Líneas de referencia
    ax1.axvline(media, color='red', linestyle='--', linewidth=2, alpha=0.8)
    ax1.axvline(mediana, color='orange', linestyle='--', linewidth=2, alpha=0.8)
    
    # Anotaciones en el histograma - CORREGIDO
    ax1.text(0.02, 0.98, f'Total: {len(puntuaciones)} candidatos', 
            transform=ax1.transAxes, fontsize=12, fontweight='bold',
            verticalalignment='top', 
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    ax1.set_xlabel('Puntuación (0-10)', fontweight='bold')
    ax1.set_ylabel('Número de Candidatos', fontweight='bold')
    ax1.set_title('Distribución de Puntuaciones', fontweight='bold', pad=15)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper right', fontsize=10)
    ax1.set_xlim(0, 10)
    
    # 2. GRÁFICO DE BARRAS POR RANGOS
    rangos = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10)]
    etiquetas = ['0-2', '2-4', '4-6', '6-8', '8-10']
    colores = ['#ffcccb', '#90EE90', '#ffeb9c', '#98FB98', '#4682B4']
    
    conteos = []
    porcentajes = []
    
    for min_r, max_r in rangos:
        if min_r == 8:  # Incluir 10.0 en el último rango
            count = sum(1 for p in puntuaciones if min_r <= p <= max_r)
        else:
            count = sum(1 for p in puntuaciones if min_r <= p < max_r)
        conteos.append(count)
        porcentajes.append((count / len(puntuaciones)) * 100)
    
    barras = ax2.bar(etiquetas, conteos, color=colores, alpha=0.8, edgecolor='black', linewidth=1)
    
    # Añadir etiquetas en las barras - LIMPIO
    for i, (barra, count, porcentaje) in enumerate(zip(barras, conteos, porcentajes)):
        altura = barra.get_height()
        ax2.text(barra.get_x() + barra.get_width()/2., altura + max(conteos)*0.01,
                f'{count}\n({porcentaje:.1f}%)', ha='center', va='bottom', 
                fontweight='bold', fontsize=11)
    
    ax2.set_xlabel('Rango de Puntuaciones', fontweight='bold')
    ax2.set_ylabel('Número de Candidatos', fontweight='bold')
    ax2.set_title('Distribución por Rangos de Puntuación', fontweight='bold', pad=15)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_ylim(0, max(conteos) * 1.15)
    
    # Información adicional en la esquina - CORREGIDO
    info_text = (f'Media: {media:.2f}\n'
                f'Mediana: {mediana:.2f}\n'
                f'Desv. Std: {desv_std:.2f}')
    ax2.text(0.98, 0.98, info_text, transform=ax2.transAxes, 
            fontsize=10, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Pie de página con información
    fig.text(0.5, 0.02, '@joanh - Análisis de Baremos 2025 | Datos: Comunidad de Madrid', 
            ha='center', fontsize=10, style='italic')
    
    # AJUSTAR LAYOUT Y GUARDAR
    plt.tight_layout()
    plt.subplots_adjust(top=0.90, bottom=0.12)
    
    # Guardar archivos
    png_path = OUTPUT_DIR / "baremo_lengua_literatura_004_2025.png"
    pdf_path = OUTPUT_DIR / "baremo_lengua_literatura_004_2025.pdf"
    
    plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(pdf_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    print(f"✅ Gráfico PNG guardado: {png_path.name}")
    print(f"✅ Gráfico PDF guardado: {pdf_path.name}")
    
    # Resumen estadístico - CORREGIDO
    print("\n" + "="*60)
    print("📊 RESUMEN ESTADÍSTICO - LENGUA CASTELLANA Y LITERATURA (004)")
    print("="*60)
    print(f"Total candidatos: {len(puntuaciones):,}")
    print(f"Puntuación máxima: {np.max(puntuaciones):.4f}")
    print(f"Puntuación mínima: {np.min(puntuaciones):.4f}")
    print(f"Puntuación media: {media:.4f}")
    print(f"Desviación estándar: {desv_std:.4f}")
    print(f"Mediana: {mediana:.4f}")
    
    print("\nDISTRIBUCIÓN POR RANGOS:")
    print("-" * 30)
    for i, (etiqueta, count, porcentaje) in enumerate(zip(etiquetas, conteos, porcentajes)):
        print(f"{etiqueta} puntos: {count:4d} candidatos ({porcentaje:5.1f}%)")
    
    # Test de normalidad
    _, p_value = stats.shapiro(puntuaciones[:5000] if len(puntuaciones) > 5000 else puntuaciones)
    normalidad = "Sí" if p_value > 0.05 else "No"
    print(f"\\nDistribución normal: {normalidad} (p-value: {p_value:.4f})")
    
    print("="*60)
    print("✅ Visualización completada exitosamente")
    print("📁 Revisa la carpeta 'output' para los gráficos generados")
    print(f"🖼️ Gráfico principal: {png_path.name}")

if __name__ == "__main__":
    main()
