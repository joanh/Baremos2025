#!/usr/bin/env python3
"""
Visualizador de datos para Lengua Castellana y Literatura (011) - Baremo 2025
Genera gráficos profesionales y análisis estadístico
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yaml
from scipy import stats
from pathlib import Path

# Configurar matplotlib para mejor renderizado
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 10

def cargar_configuracion():
    """Carga la configuración desde config.yaml"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def cargar_datos():
    """Carga los datos desde el CSV generado"""
    csv_path = Path(__file__).parent.parent / "output" / "puntuaciones_lengua_literatura_011.csv"
    if not csv_path.exists():
        print(f"❌ ERROR: No se encuentra el archivo CSV en {csv_path}")
        print("💡 Ejecuta primero: python extractor_lengua_literatura_CORREGIDO.py")
        return None
    
    df = pd.read_csv(csv_path)
    print(f"✅ Datos cargados: {len(df)} registros")
    return df

def calcular_estadisticas(df):
    """Calcula estadísticas descriptivas"""
    puntuaciones = df['Total']
    
    stats_dict = {
        'total': len(puntuaciones),
        'media': puntuaciones.mean(),
        'mediana': puntuaciones.median(),
        'moda': puntuaciones.mode().iloc[0] if not puntuaciones.mode().empty else puntuaciones.mean(),
        'std': puntuaciones.std(),
        'min': puntuaciones.min(),
        'max': puntuaciones.max(),
        'q25': puntuaciones.quantile(0.25),
        'q75': puntuaciones.quantile(0.75),
        'rango_intercuartil': puntuaciones.quantile(0.75) - puntuaciones.quantile(0.25)
    }
    
    # Test de normalidad
    if len(puntuaciones) > 3:
        try:
            _, p_value = stats.normaltest(puntuaciones)
            stats_dict['normalidad_p'] = p_value
            stats_dict['es_normal'] = p_value > 0.05
        except:
            stats_dict['normalidad_p'] = None
            stats_dict['es_normal'] = None
    
    return stats_dict

def generar_grafico_principal(df, config):
    """Genera el gráfico principal con histograma y estadísticas"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Distribución de Puntuaciones - Lengua Castellana y Literatura (011)\nBaremo Provisional 2025 - Comunidad de Madrid', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    puntuaciones = df['Total']
    color_principal = config['visualizacion']['color_principal']
    
    # 1. Histograma principal (arriba izquierda)
    ax1.hist(puntuaciones, bins=50, alpha=0.7, color=color_principal, 
            edgecolor='black', linewidth=0.5)
    ax1.axvline(puntuaciones.mean(), color='red', linestyle='--', linewidth=2, 
               label=f'Media: {puntuaciones.mean():.2f}')
    ax1.axvline(puntuaciones.median(), color='orange', linestyle='--', linewidth=2, 
               label=f'Mediana: {puntuaciones.median():.2f}')
    ax1.set_xlabel('Puntuación')
    ax1.set_ylabel('Frecuencia')
    ax1.set_title('Distribución de Puntuaciones')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 10)
    
    # 2. Gráfico de barras por rangos (arriba derecha)
    rangos = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10)]
    labels_rangos = [f'{r[0]}-{r[1]}' for r in rangos]
    counts_rangos = []
    
    for min_r, max_r in rangos:
        count = len(puntuaciones[(puntuaciones >= min_r) & (puntuaciones < max_r)])
        counts_rangos.append(count)
    
    bars = ax2.bar(labels_rangos, counts_rangos, color=color_principal, alpha=0.7, 
                  edgecolor='black', linewidth=0.5)
    ax2.set_xlabel('Rango de Puntuación')
    ax2.set_ylabel('Número de Candidatos')
    ax2.set_title('Distribución por Rangos')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Añadir valores en las barras
    for bar, count in zip(bars, counts_rangos):
        height = bar.get_height()
        porcentaje = (count / len(puntuaciones)) * 100
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(counts_rangos)*0.01,
                f'{count}\n({porcentaje:.1f}%)', ha='center', va='bottom', fontweight='bold')
    
    # 3. Box plot (abajo izquierda)
    box_plot = ax3.boxplot(puntuaciones, patch_artist=True, labels=['Lengua y Literatura'])
    box_plot['boxes'][0].set_facecolor(color_principal)
    box_plot['boxes'][0].set_alpha(0.7)
    ax3.set_ylabel('Puntuación')
    ax3.set_title('Diagrama de Caja y Bigotes')
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 10)
    
    # 4. Estadísticas (abajo derecha)
    ax4.axis('off')
    stats_dict = calcular_estadisticas(df)
    
    estadisticas_texto = f"""
ESTADÍSTICAS DESCRIPTIVAS
──────────────────────────

📊 Datos Generales:
• Total candidatos: {stats_dict['total']:,}
• Puntuación máxima: {stats_dict['max']:.4f}
• Puntuación mínima: {stats_dict['min']:.4f}

📈 Medidas de Tendencia Central:
• Media: {stats_dict['media']:.4f}
• Mediana: {stats_dict['mediana']:.4f}
• Moda: {stats_dict['moda']:.4f}

📏 Medidas de Dispersión:
• Desviación estándar: {stats_dict['std']:.4f}
• Rango intercuartil: {stats_dict['rango_intercuartil']:.4f}
• Q1 (25%): {stats_dict['q25']:.4f}
• Q3 (75%): {stats_dict['q75']:.4f}
    """
    
    if stats_dict.get('normalidad_p') is not None:
        normalidad_texto = "Sí" if stats_dict['es_normal'] else "No"
        estadisticas_texto += f"\n🔬 Test de Normalidad:\n• Distribución normal: {normalidad_texto}\n• p-value: {stats_dict['normalidad_p']:.4f}"
    
    ax4.text(0.05, 0.95, estadisticas_texto, transform=ax4.transAxes, fontsize=10,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle="round,pad=0.5", facecolor=color_principal, alpha=0.1))
    
    plt.tight_layout()
    
    # Guardar como PNG
    output_dir = Path(__file__).parent.parent / "output"
    png_path = output_dir / "baremo_lengua_literatura_011_2025.png"
    plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Gráfico PNG guardado: {png_path}")
    
    # Guardar como PDF
    pdf_path = output_dir / "baremo_lengua_literatura_011_2025.pdf"
    plt.savefig(pdf_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Gráfico PDF guardado: {pdf_path}")
    
    plt.close()
    
    return png_path

def mostrar_resumen(df):
    """Muestra resumen estadístico en consola"""
    stats_dict = calcular_estadisticas(df)
    puntuaciones = df['Total']
    
    print("\n" + "="*60)
    print("📊 RESUMEN ESTADÍSTICO - LENGUA CASTELLANA Y LITERATURA (011)")
    print("="*60)
    print(f"Total candidatos: {stats_dict['total']:,}")
    print(f"Puntuación máxima: {stats_dict['max']:.4f}")
    print(f"Puntuación mínima: {stats_dict['min']:.4f}")
    print(f"Puntuación media: {stats_dict['media']:.4f}")
    print(f"Desviación estándar: {stats_dict['std']:.4f}")
    print(f"Mediana: {stats_dict['mediana']:.4f}")
    
    print(f"\nDISTRIBUCIÓN POR RANGOS:")
    print("-" * 30)
    rangos = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10)]
    
    for min_r, max_r in rangos:
        count = len(puntuaciones[(puntuaciones >= min_r) & (puntuaciones < max_r)])
        porcentaje = (count / len(puntuaciones)) * 100
        print(f"{min_r}-{max_r} puntos: {count:4d} candidatos ({porcentaje:5.1f}%)")
    
    if stats_dict.get('normalidad_p') is not None:
        normalidad = "Sí" if stats_dict['es_normal'] else "No"
        print(f"\nDistribución normal: {normalidad} (p-value: {stats_dict['normalidad_p']:.4f})")
    
    print("="*60)

def main():
    """Función principal"""
    print("📊 VISUALIZADOR LENGUA CASTELLANA Y LITERATURA (011) - BAREMO 2025")
    print("="*70)
    
    try:
        # Cargar configuración y datos
        config = cargar_configuracion()
        df = cargar_datos()
        
        if df is None:
            sys.exit(1)
        
        # Generar visualizaciones
        print("🎨 Generando gráfico principal...")
        png_path = generar_grafico_principal(df, config)
        
        # Mostrar resumen
        mostrar_resumen(df)
        
        print(f"\n✅ Visualización completada exitosamente")
        print(f"📁 Revisa la carpeta 'output' para los gráficos generados")
        print(f"🖼️ Gráfico principal: {os.path.basename(png_path)}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
