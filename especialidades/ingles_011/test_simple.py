#!/usr/bin/env python3
"""
Test simple para verificar que funciona sin bloqueos
"""

import numpy as np

# Datos de muestra
datos_ingles = [6.8333, 6.5833, 10.0000, 4.7084, 4.0000, 4.9167, 4.3333, 6.0000, 9.0000, 4.7500]

print("=== TEST INGLÉS (011) ===")
print(f"Candidatos muestra: {len(datos_ingles)}")
print(f"Media: {np.mean(datos_ingles):.2f}")
print(f"Mediana: {np.median(datos_ingles):.2f}")
print(f"Mínimo: {np.min(datos_ingles):.2f}")
print(f"Máximo: {np.max(datos_ingles):.2f}")

# Generar dataset estimado
np.random.seed(123)
total = 1984
datos_generados = np.random.normal(np.mean(datos_ingles), np.std(datos_ingles), total - len(datos_ingles))
datos_generados = np.clip(datos_generados, 0.0, 10.0)

puntuaciones_completas = np.concatenate([datos_ingles, datos_generados])

print(f"\nDATASET COMPLETO:")
print(f"Total: {len(puntuaciones_completas)}")
print(f"Media: {np.mean(puntuaciones_completas):.2f}")
print(f"Máximo: {np.max(puntuaciones_completas):.2f} (≤ 10.0)")

print("\n✅ Test completado sin bloqueos")
