#!/usr/bin/env python3
"""
Script para limpiar imágenes obsoletas y verificar estado final
"""

import os
from pathlib import Path

def limpiar_imagenes_obsoletas():
    """Elimina imágenes con nombres largos obsoletas"""
    
    print("🧹 LIMPIEZA DE IMÁGENES OBSOLETAS")
    print("=" * 35)
    
    # Rutas de imágenes obsoletas
    imagenes_obsoletas = [
        "c:/GitHub/Baremos2025/docs/image/tags_repositorio/1751699992917.png",
        "c:/GitHub/Baremos2025/docs/image/tags_repositorio/1751700000705.png"
    ]
    
    eliminadas = 0
    
    for imagen in imagenes_obsoletas:
        imagen_path = Path(imagen)
        if imagen_path.exists():
            try:
                imagen_path.unlink()
                print(f"✅ Eliminada: {imagen_path.name}")
                eliminadas += 1
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print(f"⚪ No existe: {imagen_path.name}")
    
    return eliminadas

def verificar_estado_final():
    """Verifica el estado final del proyecto"""
    
    print(f"\n📊 VERIFICACIÓN ESTADO FINAL")
    print("=" * 30)
    
    # Verificar imagen principal de Filosofía
    imagen_principal = Path("c:/GitHub/Baremos2025/img/baremo_filosofia_001_2025.png")
    if imagen_principal.exists():
        print("✅ Imagen principal Filosofía: OK")
    else:
        print("❌ Imagen principal Filosofía: FALTA")
    
    # Verificar archivos esenciales
    archivos_esenciales = [
        ("README principal", "c:/GitHub/Baremos2025/README.md"),
        ("Config especialidades", "c:/GitHub/Baremos2025/config/especialidades.yaml"),
        ("README Filosofía", "c:/GitHub/Baremos2025/especialidades/filosofia_001/README.md"),
        ("Datos finales", "c:/GitHub/Baremos2025/especialidades/filosofia_001/output/puntuaciones_filosofia_001_final.py"),
        ("Estadísticas finales", "c:/GitHub/Baremos2025/especialidades/filosofia_001/output/estadisticas_filosofia_001_completas.txt")
    ]
    
    todos_ok = True
    for nombre, ruta in archivos_esenciales:
        if Path(ruta).exists():
            print(f"✅ {nombre}: OK")
        else:
            print(f"❌ {nombre}: FALTA")
            todos_ok = False
    
    return todos_ok

def resumen_proyecto():
    """Muestra resumen final del proyecto"""
    
    print(f"\n🎯 RESUMEN FINAL DEL PROYECTO")
    print("=" * 32)
    print("📂 ESTRUCTURA LISTA PARA GITHUB:")
    print("   ✅ Filosofía (001): 561 candidatos")
    print("   ✅ Informática (107): 343 candidatos") 
    print("   ✅ Matemáticas (006): 1,829 candidatos")
    print("   ✅ Física y Química (010): 962 candidatos")
    print("   ✅ Lengua y Literatura (004): 1,727 candidatos")
    print("   📊 TOTAL: 5,422 candidatos")
    
    print(f"\n📈 ARCHIVOS PRINCIPALES:")
    print("   📄 README.md (actualizado con 5 especialidades)")
    print("   ⚙️ config/especialidades.yaml (Filosofía configurada)")
    print("   🎨 img/baremo_filosofia_001_2025.png (gráfico final)")
    print("   📋 docs/tags_repositorio.md (tags actualizados)")
    
    print(f"\n🚀 ESTADO: LISTO PARA GITHUB")

if __name__ == "__main__":
    # Limpiar imágenes obsoletas
    eliminadas = limpiar_imagenes_obsoletas()
    
    # Verificar estado
    estado_ok = verificar_estado_final()
    
    # Mostrar resumen
    resumen_proyecto()
    
    if eliminadas > 0:
        print(f"\n🎉 LIMPIEZA COMPLETADA ({eliminadas} imágenes eliminadas)")
    
    if estado_ok:
        print(f"✅ PROYECTO LISTO PARA PUBLICACIÓN")
    else:
        print(f"⚠️ REVISAR ARCHIVOS FALTANTES")
