#!/usr/bin/env python3
"""
Verificación final de la corrección de Matemáticas 008 → 006
"""

import os
from pathlib import Path
import glob

def verificar_matematicas():
    """Verifica que todas las correcciones de Matemáticas estén completas"""
    
    print("🔍 VERIFICACIÓN FINAL: Matemáticas 008 → 006")
    print("=" * 50)
    
    base_dir = Path(".")
    errores = []
    
    # 1. Verificar que existe el directorio correcto
    dir_matematicas_006 = base_dir / "especialidades" / "matematicas_006"
    if dir_matematicas_006.exists():
        print("✅ Directorio matematicas_006 existe")
    else:
        errores.append("❌ No existe el directorio matematicas_006")
    
    # 2. Verificar que NO existe el directorio viejo
    dir_matematicas_008 = base_dir / "especialidades" / "matematicas_008"
    if not dir_matematicas_008.exists():
        print("✅ Directorio matematicas_008 eliminado correctamente")
    else:
        print("⚠️ Directorio matematicas_008 aún existe (pendiente de limpieza)")
    
    # 3. Verificar archivos clave
    archivos_esperados = [
        "especialidades/matematicas_006/config.yaml",
        "especialidades/matematicas_006/README.md",
        "config/especialidades.yaml",
        "README.md",
        "img/baremo_matematicas_006_2025.png"
    ]
    
    for archivo in archivos_esperados:
        ruta = base_dir / archivo
        if ruta.exists():
            print(f"✅ {archivo}")
        else:
            errores.append(f"❌ Falta: {archivo}")
    
    # 4. Buscar referencias a 008 en archivos importantes
    archivos_revisar = [
        "config/especialidades.yaml",
        "README.md",
        "README_new.md",
        "especialidades/matematicas_006/config.yaml",
        "especialidades/matematicas_006/README.md"
    ]
    
    print("\n🔍 Buscando referencias a '008' en archivos clave:")
    referencias_008 = []
    
    for archivo in archivos_revisar:
        ruta = base_dir / archivo
        if ruta.exists():
            try:
                with open(ruta, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    if '008' in contenido and 'matematicas' in contenido.lower():
                        lineas = contenido.split('\n')
                        for i, linea in enumerate(lineas, 1):
                            if '008' in linea and 'matematicas' in linea.lower():
                                referencias_008.append(f"{archivo}:{i} - {linea.strip()}")
            except Exception as e:
                print(f"⚠️ Error leyendo {archivo}: {e}")
    
    if referencias_008:
        print("❌ Referencias a 008 encontradas:")
        for ref in referencias_008:
            print(f"   {ref}")
        errores.extend(referencias_008)
    else:
        print("✅ No se encontraron referencias a '008' en archivos clave")
    
    # 5. Verificar imagen
    img_006 = base_dir / "img" / "baremo_matematicas_006_2025.png"
    img_008 = base_dir / "img" / "baremo_matematicas_008_2025.png"
    
    if img_006.exists():
        print("✅ Imagen baremo_matematicas_006_2025.png existe")
    else:
        errores.append("❌ Falta imagen baremo_matematicas_006_2025.png")
    
    if not img_008.exists():
        print("✅ Imagen vieja baremo_matematicas_008_2025.png eliminada")
    else:
        print("⚠️ Imagen vieja baremo_matematicas_008_2025.png aún existe")
    
    # 6. Verificar config central
    config_central = base_dir / "config" / "especialidades.yaml"
    if config_central.exists():
        try:
            with open(config_central, 'r', encoding='utf-8') as f:
                contenido = f.read()
                if 'codigo: "006"' in contenido and 'matematicas' in contenido.lower():
                    print("✅ Config central tiene código 006 para Matemáticas")
                else:
                    errores.append("❌ Config central no tiene código 006 para Matemáticas")
        except Exception as e:
            errores.append(f"❌ Error leyendo config central: {e}")
    
    # RESUMEN
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE VERIFICACIÓN")
    print("=" * 50)
    
    if not errores:
        print("🎉 ¡PERFECTO! Todas las correcciones completadas")
        print("✅ Matemáticas 008 → 006: COMPLETADO")
        print("\n🎯 Estado actual:")
        print("   • Directorio: especialidades/matematicas_006/")
        print("   • Código: 006")
        print("   • Imagen: img/baremo_matematicas_006_2025.png")
        print("   • Configuración: Actualizada")
        print("   • Documentación: Actualizada")
        
        if dir_matematicas_008.exists():
            print("\n📝 PENDIENTE (opcional):")
            print("   • Eliminar directorio matematicas_008 (limpieza)")
    else:
        print("⚠️ SE ENCONTRARON ALGUNOS PROBLEMAS:")
        for error in errores:
            print(f"   {error}")
        
        print("\n🔧 SIGUIENTE PASO:")
        print("   Corregir los problemas listados arriba")
    
    return len(errores) == 0

if __name__ == "__main__":
    exito = verificar_matematicas()
    
    if exito:
        print("\n🚀 ¡Corrección de Matemáticas COMPLETADA!")
    else:
        print("\n🔄 Necesita correcciones adicionales")
