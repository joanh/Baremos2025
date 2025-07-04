import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

print("=== ANÁLISIS DE PUNTUACIONES INFORMÁTICA (ESPECIALIDAD 107) ===")

# Datos extraídos manualmente de las primeras páginas
puntuaciones_muestra = [
    2.4167, 7.3333, 3.6500, 5.2084, 2.5000, 4.3333, 5.7500,
    1.8000, 6.8500, 8.0000, 5.0000, 7.5833, 7.5000, 6.3750,
    1.9167, 2.2500, 10.0000, 1.0000, 1.7500, 7.0042, 1.0000
]

print(f"Puntuaciones de muestra: {len(puntuaciones_muestra)} candidatos")
print(f"Rango: {min(puntuaciones_muestra):.4f} - {max(puntuaciones_muestra):.4f}")

print(f"\n=== ANÁLISIS DE LA MUESTRA REAL ===")
print(f"Media: {np.mean(puntuaciones_muestra):.4f}")
print(f"Mediana: {np.median(puntuaciones_muestra):.4f}")
print(f"Desviación estándar: {np.std(puntuaciones_muestra):.4f}")

# Verificar valores altos en la muestra
print(f"\n=== VALORES ALTOS EN LA MUESTRA ===")
for umbral in [8.0, 9.0, 9.5, 10.0]:
    altos = [p for p in puntuaciones_muestra if p >= umbral]
    porcentaje = (len(altos) / len(puntuaciones_muestra)) * 100
    print(f"Puntuaciones >= {umbral}: {len(altos)} ({porcentaje:.1f}%)")
    if altos:
        print(f"  Valores: {sorted(altos, reverse=True)}")

# ANÁLISIS SOLO DE LA MUESTRA REAL
print(f"\n=== ANÁLISIS DETALLADO DE LA MUESTRA ===")

# Distribución por rangos
rangos = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 11)]
print(f"Distribución por rangos:")
for min_r, max_r in rangos:
    count = sum(1 for p in puntuaciones_muestra if min_r <= p < max_r)
    porcentaje = (count / len(puntuaciones_muestra)) * 100
    if count > 0:
        print(f"  Rango {min_r}-{max_r}: {count:2d} candidatos ({porcentaje:5.1f}%)")

# Guardar muestra real
df_muestra = pd.DataFrame({'Puntuacion_Total': puntuaciones_muestra})
df_muestra.to_csv('puntuaciones_informatica_107_MUESTRA_REAL.csv', index=False)
print(f"\n✅ Muestra real guardada en 'puntuaciones_informatica_107_MUESTRA_REAL.csv'")

# GRÁFICO SOLO DE LA MUESTRA REAL
plt.figure(figsize=(12, 8))

bins_muestra = np.arange(0, max(puntuaciones_muestra) + 0.5, 0.5)
counts, bin_edges, patches = plt.hist(puntuaciones_muestra, bins=bins_muestra, alpha=0.8, 
                                    color='lightblue', edgecolor='black', linewidth=1)

# Resaltar valores altos
for i, (count, left_edge, right_edge) in enumerate(zip(counts, bin_edges[:-1], bin_edges[1:])):
    if left_edge >= 9.0:
        patches[i].set_facecolor('red')
        patches[i].set_alpha(1.0)
    elif left_edge >= 8.0:
        patches[i].set_facecolor('orange')
        patches[i].set_alpha(0.9)
    elif left_edge >= 7.0:
        patches[i].set_facecolor('yellow')
        patches[i].set_alpha(0.8)

plt.axvline(np.mean(puntuaciones_muestra), color='green', linestyle='-', linewidth=2, 
           label=f'Media: {np.mean(puntuaciones_muestra):.4f}')
plt.axvline(np.median(puntuaciones_muestra), color='purple', linestyle=':', linewidth=2, 
           label=f'Mediana: {np.median(puntuaciones_muestra):.4f}')

plt.xlabel('Puntuación Total')
plt.ylabel('Frecuencia')
plt.title('Muestra Real - Informática Especialidad 107 (21 candidatos)')
plt.legend()
plt.grid(True, alpha=0.3)

# Añadir texto con estadísticas
stats_text = f'Valores destacados:\n'
stats_text += f'• Máximo: {max(puntuaciones_muestra):.4f}\n'
stats_text += f'• >= 8.0: {len([p for p in puntuaciones_muestra if p >= 8.0])} candidatos\n'
stats_text += f'• >= 9.0: {len([p for p in puntuaciones_muestra if p >= 9.0])} candidatos\n'
stats_text += f'• = 10.0: {len([p for p in puntuaciones_muestra if p == 10.0])} candidatos'

plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes, 
        fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle="round,pad=0.5", facecolor="yellow", alpha=0.8))

plt.tight_layout()
plt.savefig('muestra_real_informatica_107.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico guardado como 'muestra_real_informatica_107.png'")

print(f"\n🎯 NECESITAMOS EXTRAER TODOS LOS DATOS REALES")
print(f"📋 Tu muestra de 21 candidatos es muy buena base")
print(f"🏆 Ya vemos valores altos: 8.0, 10.0")
print(f"📊 Para análisis completo necesitamos los ~400 candidatos")

# ESTRATEGIA PARA OBTENER DATOS REALES
print(f"\n=== ESTRATEGIAS PARA OBTENER DATOS COMPLETOS ===")
print("1. 📋 MANUAL: Continuar extrayendo página por página")
print("2. 🔧 OCR: Usar Tesseract para reconocimiento óptico")
print("3. 📄 CONVERSIÓN: Usar herramientas online (SmallPDF, etc.)")
print("4. 🐍 PYTHON: Probar librerías especializadas")

print("\n¿Quieres que te ayude con alguna de estas opciones?")