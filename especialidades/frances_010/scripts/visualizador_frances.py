#!/usr/bin/env python3
"""
Visualizador Francés (010) - Baremo 2025
Genera gráfico profesional siguiendo EXACTAMENTE el estándar del proyecto
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os

def cargar_puntuaciones():
    """Carga las puntuaciones desde el archivo CSV"""
    try:
        ruta_csv = "../output/puntuaciones_frances_010.csv"
        puntuaciones = []
        
        with open(ruta_csv, 'r', encoding='utf-8') as f:
            next(f)  # Saltar header
            for linea in f:
                if linea.strip():
                    candidato, puntuacion = linea.strip().split(',')
                    puntuaciones.append(float(puntuacion))
        
        return np.array(puntuaciones)
    except Exception as e:
        print(f"❌ Error cargando puntuaciones: {e}")
        return None

def main():
    print("🎨 VISUALIZADOR FRANCÉS (010) - BAREMO 2025")
    print("=" * 50)
    
    # Cargar puntuaciones
    puntuaciones = cargar_puntuaciones()
    if puntuaciones is None:
        return
    
    print(f"✅ Puntuaciones cargadas: {len(puntuaciones)} candidatos")
    
    # Configuración de matplotlib para mejor calidad
    plt.rcParams['figure.figsize'] = (16, 8)
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 11
    plt.rcParams['ytick.labelsize'] = 11
    plt.rcParams['legend.fontsize'] = 10
    
    # Crear figura con dos subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    print("🎨 Generando gráfico...")
    
    # Configuración general
    fig.suptitle('Baremo Francés 2025 - Comunidad de Madrid', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # 1. HISTOGRAMA CON DISTRIBUCIÓN NORMAL (EJE HORIZONTAL 0-10)
    bins = np.linspace(0, 10, 21)  # Rango 0-10
    n, bins_hist, patches = ax1.hist(puntuaciones, bins=bins, alpha=0.7, 
                                    color='lightblue', edgecolor='black', density=True)
    
    # Línea de distribución normal
    x = np.linspace(0, 10, 100)
    mu, sigma = np.mean(puntuaciones), np.std(puntuaciones)
    normal_dist = stats.norm.pdf(x, mu, sigma)
    ax1.plot(x, normal_dist, 'r-', linewidth=2, 
             label=f'Distribución Normal\nμ={mu:.2f}, σ={sigma:.2f}')
    
    # Líneas de media y mediana
    ax1.axvline(np.mean(puntuaciones), color='green', linestyle='--', linewidth=2, 
               label=f'Media: {np.mean(puntuaciones):.2f}')
    ax1.axvline(np.median(puntuaciones), color='red', linestyle='--', linewidth=2, 
               label=f'Mediana: {np.median(puntuaciones):.2f}')
    
    ax1.set_xlabel('Puntuación (0-10)', fontweight='bold', fontsize=12)
    ax1.set_ylabel('Densidad', fontweight='bold', fontsize=12)
    ax1.set_title('Distribución de Puntuaciones', fontweight='bold', fontsize=14)
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 10)  # FORZAR límite del eje X
    
    # Estadísticas en el gráfico
    stats_text = f'Media: {np.mean(puntuaciones):.2f}\nMediana: {np.median(puntuaciones):.2f}\nDesv. Est.: {np.std(puntuaciones):.2f}\nTotal: {len(puntuaciones):,} candidatos'
    ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes, fontsize=11,
             verticalalignment='top', 
             bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", alpha=0.9, edgecolor='gray'))
    
    # 2. DISTRIBUCIÓN POR RANGOS (0-10)
    rangos = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10)]
    rangos_nombres = ['0-2', '2-4', '4-6', '6-8', '8-10']
    rangos_counts = []
    rangos_porcentajes = []
    
    for min_r, max_r in rangos:
        count = np.sum((puntuaciones >= min_r) & (puntuaciones < max_r))
        porcentaje = (count / len(puntuaciones)) * 100
        rangos_counts.append(count)
        rangos_porcentajes.append(porcentaje)
    
    # Colores mejorados
    colors = ['#87CEEB', '#FFA07A', '#CD5C5C', '#F0E68C', '#6495ED']
    
    # Crear barras
    bars = ax2.bar(rangos_nombres, rangos_counts, 
                   color=colors, edgecolor='black', linewidth=1.2, alpha=0.8)
    
    ax2.set_xlabel('Rango de Puntuaciones', fontweight='bold', fontsize=12)
    ax2.set_ylabel('Número de Candidatos', fontweight='bold', fontsize=12)
    ax2.set_title('Distribución por Rangos de Puntuación', fontweight='bold', fontsize=14)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Añadir valores y porcentajes
    for bar, count, porcentaje in zip(bars, rangos_counts, rangos_porcentajes):
        height = bar.get_height()
        texto = f'{count:,}\n({porcentaje:.1f}%)'
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(rangos_counts)*0.02,
                 texto, ha='center', va='bottom', fontweight='bold', fontsize=11,
                 bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))
    
    # Mejorar límites del eje Y
    ax2.set_ylim(0, max(rangos_counts) * 1.15)
    
    # Firma del autor
    fig.text(0.99, 0.01, '@joanh - Baremos2025', fontsize=10, color='gray', alpha=0.8, 
             ha='right', va='bottom', style='italic', weight='bold')
    
    # Ajuste de layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Guardar gráficos
    output_path_1 = '../output/baremo_frances_010_2025.png'
    output_path_2 = '../../../img/baremo_frances_010_2025.png'
    
    plt.savefig(output_path_1, dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_path_2, dpi=300, bbox_inches='tight', facecolor='white')
    
    print(f"✅ Gráfico guardado: {os.path.abspath(output_path_1)}")
    print(f"✅ Gráfico copiado a: {os.path.abspath(output_path_2)}")
    
    plt.show()
    print("🎉 ¡VISUALIZACIÓN COMPLETADA!")
    print(f"🎯 Total candidatos visualizados: {len(puntuaciones)}")

if __name__ == "__main__":
    main()
