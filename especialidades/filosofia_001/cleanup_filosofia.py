#!/usr/bin/env python3
"""
Script de limpieza para Filosofía (001)
Elimina archivos obsoletos y deja solo las versiones finales
"""

import os
from pathlib import Path

def limpiar_filosofia():
    """Limpia archivos obsoletos de la carpeta de Filosofía"""
    
    base_dir = Path("c:/GitHub/Baremos2025/especialidades/filosofia_001")
    output_dir = base_dir / "output"
    
    print("🧹 LIMPIEZA DE ARCHIVOS FILOSOFÍA (001)")
    print("=" * 45)
    
    # ARCHIVOS A ELIMINAR EN LA CARPETA PRINCIPAL
    archivos_principales_eliminar = [
        "extractor_filosofia_correcto.py",  # Superseded por análisis completo
        "extractor_filosofia_preciso.py",   # No era preciso
        "analisis_filosofia_completo.py",   # Reemplazado por corregido
        "baremo_filosofia_001.py"           # No se usó
    ]
    
    # ARCHIVOS A ELIMINAR EN OUTPUT
    archivos_output_eliminar = [
        "baremo_filosofia_001_2025_corregido.png",  # Duplicado
        "estadisticas_filosofia_001.txt",          # Versión inicial
        "filosofia_001_completo.csv",              # Versión defectuosa
        "filosofia_001_completo.txt",              # Versión defectuosa
        "FILOSOFIA_001_EXTRACCION.csv",            # Versión incorrecta
        "FILOSOFIA_001_EXTRACCION.txt",            # Versión incorrecta
        "filosofia_001_real.csv",                  # Versión intermedia
        "puntuaciones_filosofia_001.csv",          # Versión inicial
        "puntuaciones_filosofia_001.py",           # Versión inicial
        "puntuaciones_filosofia_001_muestra.csv", # Solo muestra
        "puntuaciones_filosofia_001_real.py"      # Versión intermedia
    ]
    
    eliminados = 0
    
    # Eliminar archivos principales
    for archivo in archivos_principales_eliminar:
        archivo_path = base_dir / archivo
        if archivo_path.exists():
            try:
                archivo_path.unlink()
                print(f"✅ Eliminado: {archivo}")
                eliminados += 1
            except Exception as e:
                print(f"❌ Error eliminando {archivo}: {e}")
        else:
            print(f"⚪ No existe: {archivo}")
    
    # Eliminar archivos de output
    for archivo in archivos_output_eliminar:
        archivo_path = output_dir / archivo
        if archivo_path.exists():
            try:
                archivo_path.unlink()
                print(f"✅ Eliminado: output/{archivo}")
                eliminados += 1
            except Exception as e:
                print(f"❌ Error eliminando output/{archivo}: {e}")
        else:
            print(f"⚪ No existe: output/{archivo}")
    
    print(f"\n🎯 ARCHIVOS FINALES CONSERVADOS:")
    print("CARPETA PRINCIPAL:")
    print("  ✅ analisis_filosofia_corregido.py (script final)")
    print("  ✅ README.md (documentación)")
    
    print("\nCARPETA OUTPUT:")
    print("  ✅ baremo_filosofia_001_2025.png (gráfico final)")
    print("  ✅ puntuaciones_filosofia_001_final.py (datos finales)")
    print("  ✅ estadisticas_filosofia_001_completas.txt (stats finales)")
    
    print(f"\n📊 RESUMEN:")
    print(f"   🗑️ Archivos eliminados: {eliminados}")
    print(f"   📁 Archivos conservados: 5")
    print(f"   ✅ Carpeta lista para GitHub")
    
    return eliminados

if __name__ == "__main__":
    eliminados = limpiar_filosofia()
    if eliminados > 0:
        print(f"\n🎉 LIMPIEZA COMPLETADA")
        print(f"La carpeta Filosofía está lista para GitHub")
    else:
        print(f"\n⚪ No había archivos que eliminar")
        print(f"La carpeta ya estaba limpia")
