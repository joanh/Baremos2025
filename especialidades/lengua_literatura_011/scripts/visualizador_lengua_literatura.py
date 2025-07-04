#!/usr/bin/env python3
"""
Visualizador de datos para Lengua Castellana y Literatura (011) - Baremo 2025
Genera gráficos profesionales y análisis estadístico
Autor: @joanh con Claude Sonnet 4.0
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import yaml
from scipy import stats
from matplotlib.backends.backend_pdf import PdfPages
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurar matplotlib para mejor renderizado
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 10
sns.set_palette("husl")

class VisualizadorLenguaLiteratura:
    def __init__(self, config_path: str = "../config.yaml"):
        """Inicializar el visualizador con configuración."""
        self.config = self._cargar_config(config_path)
        self.df = None
        
    def _cargar_config(self, config_path: str) -> dict:
        """Cargar configuración desde archivo YAML."""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Error cargando configuración: {e}")
            sys.exit(1)
    
    def cargar_datos(self) -> bool:
        """Cargar datos desde el archivo CSV generado."""
        try:
            especialidad = self.config['especialidad']['codigo']
            csv_path = f"../output/puntuaciones_lengua_literatura_{especialidad}.csv"
            
            if not os.path.exists(csv_path):
                logger.error(f"❌ Archivo no encontrado: {csv_path}")
                logger.info("💡 Ejecuta primero el extractor: python extractor_lengua_literatura.py")
                return False
            
            self.df = pd.read_csv(csv_path)
            logger.info(f"✅ Datos cargados: {len(self.df)} registros")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error cargando datos: {e}")
            return False
    
    def _calcular_estadisticas(self) -> dict:
        """Calcular estadísticas descriptivas."""
        if self.df is None or self.df.empty:
            return {}
        
        puntuaciones = self.df['Puntuacion']
        
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
    
    def generar_grafico_principal(self) -> str:
        """Generar el gráfico principal con histograma y estadísticas."""
        if self.df is None or self.df.empty:
            logger.error("❌ No hay datos para generar gráfico")
            return None
        
        # Configuración del gráfico
        config_viz = self.config['visualizacion']
        especialidad = self.config['especialidad']
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'{config_viz["titulo"]}\nBaremo Provisional 2025 - Comunidad de Madrid', 
                     fontsize=16, fontweight='bold', y=0.98)
        
        puntuaciones = self.df['Puntuacion']
        color_principal = config_viz['color_principal']
        
        # 1. Histograma principal (arriba izquierda)
        ax1.hist(puntuaciones, bins=config_viz['bins'], alpha=0.7, color=color_principal, 
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
        stats_dict = self._calcular_estadisticas()
        
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
            estadisticas_texto += f"\n        🔬 Test de Normalidad:\n        • Distribución normal: {normalidad_texto}\n        • p-value: {stats_dict['normalidad_p']:.4f}"
        
        ax4.text(0.05, 0.95, estadisticas_texto, transform=ax4.transAxes, fontsize=10,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.5", facecolor=color_principal, alpha=0.1))
        
        plt.tight_layout()
        
        # Guardar como PNG
        especialidad_codigo = self.config['especialidad']['codigo']
        png_path = f"../output/baremo_lengua_literatura_{especialidad_codigo}_2025.png"
        plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
        logger.info(f"💾 Gráfico PNG guardado: {png_path}")
        
        # Guardar como PDF
        pdf_path = f"../output/baremo_lengua_literatura_{especialidad_codigo}_2025.pdf"
        plt.savefig(pdf_path, dpi=300, bbox_inches='tight', facecolor='white')
        logger.info(f"💾 Gráfico PDF guardado: {pdf_path}")
        
        plt.close()
        
        return png_path
    
    def generar_analisis_detallado(self):
        """Generar análisis estadístico detallado."""
        if self.df is None or self.df.empty:
            return
        
        especialidad_codigo = self.config['especialidad']['codigo']
        
        # Crear gráfico de análisis detallado
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análisis Estadístico Detallado - Lengua Castellana y Literatura (011)', 
                     fontsize=16, fontweight='bold')
        
        puntuaciones = self.df['Puntuacion']
        color_principal = self.config['visualizacion']['color_principal']
        
        # 1. Q-Q Plot para normalidad
        stats.probplot(puntuaciones, dist="norm", plot=ax1)
        ax1.set_title('Q-Q Plot (Test de Normalidad)')
        ax1.grid(True, alpha=0.3)
        
        # 2. Densidad con curva normal superpuesta
        ax2.hist(puntuaciones, bins=50, density=True, alpha=0.7, color=color_principal, 
                edgecolor='black', linewidth=0.5, label='Datos reales')
        
        # Curva normal teórica
        mu, sigma = puntuaciones.mean(), puntuaciones.std()
        x = np.linspace(puntuaciones.min(), puntuaciones.max(), 100)
        normal_curve = stats.norm.pdf(x, mu, sigma)
        ax2.plot(x, normal_curve, 'r--', linewidth=2, label='Distribución normal teórica')
        
        ax2.set_xlabel('Puntuación')
        ax2.set_ylabel('Densidad')
        ax2.set_title('Comparación con Distribución Normal')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Percentiles
        percentiles = [5, 10, 25, 50, 75, 90, 95]
        valores_percentiles = [np.percentile(puntuaciones, p) for p in percentiles]
        
        ax3.bar(range(len(percentiles)), valores_percentiles, color=color_principal, alpha=0.7)
        ax3.set_xlabel('Percentil')
        ax3.set_ylabel('Puntuación')
        ax3.set_title('Distribución de Percentiles')
        ax3.set_xticks(range(len(percentiles)))
        ax3.set_xticklabels([f'P{p}' for p in percentiles])
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Añadir valores en las barras
        for i, valor in enumerate(valores_percentiles):
            ax3.text(i, valor + 0.1, f'{valor:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # 4. Análisis de outliers
        Q1 = puntuaciones.quantile(0.25)
        Q3 = puntuaciones.quantile(0.75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR
        
        outliers = puntuaciones[(puntuaciones < limite_inferior) | (puntuaciones > limite_superior)]
        
        ax4.scatter(range(len(puntuaciones)), sorted(puntuaciones), alpha=0.6, color=color_principal)
        ax4.axhline(y=limite_inferior, color='red', linestyle='--', alpha=0.7, label=f'Límite inferior: {limite_inferior:.2f}')
        ax4.axhline(y=limite_superior, color='red', linestyle='--', alpha=0.7, label=f'Límite superior: {limite_superior:.2f}')
        
        if len(outliers) > 0:
            ax4.scatter(range(len(outliers)), sorted(outliers), color='red', s=50, 
                       label=f'Outliers: {len(outliers)}', alpha=0.8)
        
        ax4.set_xlabel('Índice (ordenado)')
        ax4.set_ylabel('Puntuación')
        ax4.set_title('Análisis de Outliers')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Guardar análisis detallado
        analisis_path = f"../output/analisis_detallado_lengua_literatura_{especialidad_codigo}_2025.png"
        plt.savefig(analisis_path, dpi=300, bbox_inches='tight', facecolor='white')
        logger.info(f"💾 Análisis detallado guardado: {analisis_path}")
        
        plt.close()
    
    def mostrar_resumen(self):
        """Mostrar resumen estadístico en consola."""
        if self.df is None or self.df.empty:
            return
        
        stats_dict = self._calcular_estadisticas()
        
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
        puntuaciones = self.df['Puntuacion']
        
        for min_r, max_r in rangos:
            count = len(puntuaciones[(puntuaciones >= min_r) & (puntuaciones < max_r)])
            porcentaje = (count / len(puntuaciones)) * 100
            print(f"{min_r}-{max_r} puntos: {count:4d} candidatos ({porcentaje:5.1f}%)")
        
        if stats_dict.get('normalidad_p') is not None:
            normalidad = "Sí" if stats_dict['es_normal'] else "No"
            print(f"\nDistribución normal: {normalidad} (p-value: {stats_dict['normalidad_p']:.4f})")
        
        print("="*60)

def main():
    """Función principal."""
    print("📊 Visualizador de Lengua Castellana y Literatura (011) - Baremo 2025")
    print("="*65)
    
    try:
        # Crear visualizador
        visualizador = VisualizadorLenguaLiteratura()
        
        # Cargar datos
        if not visualizador.cargar_datos():
            sys.exit(1)
        
        # Generar visualizaciones
        logger.info("🎨 Generando gráfico principal...")
        png_path = visualizador.generar_grafico_principal()
        
        logger.info("🎨 Generando análisis detallado...")
        visualizador.generar_analisis_detallado()
        
        # Mostrar resumen
        visualizador.mostrar_resumen()
        
        print(f"\n✅ Visualización completada exitosamente")
        print(f"📁 Revisa la carpeta 'output' para los gráficos generados")
        
        if png_path:
            print(f"🖼️ Gráfico principal: {os.path.basename(png_path)}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
