import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.colors as mcolors

# DATOS REALES INFORMÁTICA 107 - 2025
# Extraídos del PDF oficial páginas 2649-2697
# Ejecutar primero: extractor_ORDEN_REAL.py

print("=== ANÁLISIS BAREMO INFORMÁTICA 107 - 2025 ===")

# Cargar datos reales
try:
    # Intentar cargar desde el archivo generado
    with open('lista_informatica_107.py', 'r') as f:
        exec(f.read())
    datos = puntuaciones_informatica
    print(f"✅ Datos cargados: {len(datos)} candidatos")
except:
    print("❌ Ejecuta primero 'extractor_ORDEN_REAL.py'")
    print("Usando datos de muestra...")
    # Datos de muestra para testing
    datos = [2.4167, 7.3333, 3.6500, 5.2084, 2.5000, 4.3333, 5.7500,
             1.8000, 6.8500, 8.0000, 5.0000, 7.5833, 7.5000, 6.3750,
             1.9167, 2.2500, 10.0000, 1.0000, 1.7500, 7.0042, 1.0000] * 16

# Convertir a numpy array
puntuaciones = np.array(datos)

print(f"📊 Total candidatos: {len(puntuaciones)}")
print(f"🏆 Puntuación máxima: {np.max(puntuaciones):.4f}")
print(f"📉 Puntuación mínima: {np.min(puntuaciones):.4f}")
print(f"📈 Media: {np.mean(puntuaciones):.4f}")
print(f"📊 Mediana: {np.median(puntuaciones):.4f}")
print(f"📐 Desviación estándar: {np.std(puntuaciones):.4f}")

# ANÁLISIS ESTADÍSTICO
print(f"\n=== ANÁLISIS ESTADÍSTICO ===")
valores_unicos = len(np.unique(puntuaciones))
print(f"🎯 Puntuaciones diferentes: {valores_unicos}")
print(f"🔄 Repeticiones: {len(puntuaciones) - valores_unicos}")

# Cuartiles
q1, q2, q3 = np.percentile(puntuaciones, [25, 50, 75])
print(f"📊 Q1 (25%): {q1:.4f}")
print(f"📊 Q2 (50%): {q2:.4f}") 
print(f"📊 Q3 (75%): {q3:.4f}")

# Análisis por rangos
rangos = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10)]
print(f"\n=== DISTRIBUCIÓN POR RANGOS ===")
for min_r, max_r in rangos:
    count = np.sum((puntuaciones >= min_r) & (puntuaciones < max_r))
    porcentaje = (count / len(puntuaciones)) * 100
    print(f"{min_r}-{max_r}: {count:3d} candidatos ({porcentaje:5.1f}%)")

# CONFIGURACIÓN DE GRÁFICOS
plt.style.use('default')
plt.rcParams['font.size'] = 12

# CREAR FIGURA CON 2 SUBPLOTS (1x2)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('ANÁLISIS BAREMO INFORMÁTICA 107 - CONVOCATORIA 2025', 
             fontsize=16, fontweight='bold', y=0.95)

# 1. HISTOGRAMA - DISTRIBUCIÓN DE PROBABILIDADES
# X: Notas (0-10), Y: Número de valores (no densidad)
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
         label=f'Distribución Normal\nμ={mu:.2f}, σ={sigma:.2f}')

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
stats_text = f'Media: {np.mean(puntuaciones):.2f}\n'
stats_text += f'Mediana: {np.median(puntuaciones):.2f}\n'
stats_text += f'Desv. Est.: {np.std(puntuaciones):.2f}\n'
stats_text += f'Total: {len(puntuaciones)} candidatos'
ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes, 
         bbox=dict(boxstyle="round,pad=0.4", facecolor="wheat", alpha=0.9),
         verticalalignment='top', fontsize=10)

# 2. CANDIDATOS POR RANGO CON GRADIENTE DE COLOR
rangos_nombres = ['0-2', '2-4', '4-6', '6-8', '8-10']
rangos_counts = []
rangos_porcentajes = []

for min_r, max_r in rangos:
    count = np.sum((puntuaciones >= min_r) & (puntuaciones < max_r))
    porcentaje = (count / len(puntuaciones)) * 100
    rangos_counts.append(count)
    rangos_porcentajes.append(porcentaje)

# Crear gradiente de color basado en porcentajes
# Normalizar porcentajes para el gradiente (0-1)
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
             f'{count}\n({porcentaje:.1f}%)',
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

# GUARDAR GRÁFICO
plt.savefig('baremo_informatica_107_2025.png', dpi=300, bbox_inches='tight')
plt.savefig('baremo_informatica_107_2025.pdf', bbox_inches='tight')
print(f"\n💾 Gráficos guardados:")
print("   - baremo_informatica_107_2025.png")
print("   - baremo_informatica_107_2025.pdf")

# MOSTRAR GRÁFICO
plt.show()

# ANÁLISIS ADICIONAL RESUMIDO
print(f"\n=== ANÁLISIS RESUMIDO ===")

# Top 10
print(f"\n🏅 TOP 10 PUNTUACIONES:")
puntuaciones_ordenadas = np.sort(puntuaciones)[::-1]  # Ordenar de mayor a menor
for i in range(min(10, len(puntuaciones_ordenadas))):
    print(f"{i+1:2d}. {puntuaciones_ordenadas[i]:.4f}")

# Percentiles importantes
print(f"\n📊 PERCENTILES CLAVE:")
for percentil in [10, 25, 50, 75, 90, 95]:
    valor = np.percentile(puntuaciones, percentil)
    print(f"P{percentil:2d}: {valor:.4f}")

# Test de normalidad simplificado
from scipy.stats import shapiro
if len(puntuaciones) <= 5000:
    statistic, p_value = shapiro(puntuaciones)
    print(f"\n📊 NORMALIDAD (Shapiro-Wilk):")
    print(f"p-value: {p_value:.6f}")
    if p_value > 0.05:
        print("✅ Distribución normal (p > 0.05)")
    else:
        print("❌ No sigue distribución normal (p < 0.05)")

print(f"\n🎉 ANÁLISIS COMPLETADO")
print(f"📈 {len(puntuaciones)} candidatos analizados")
print(f"📊 Gráficos simplificados generados")
print(f"✍️ Análisis realizado por @joanh")