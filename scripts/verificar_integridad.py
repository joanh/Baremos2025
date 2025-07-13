#!/usr/bin/env python3
"""
Script de Verificación de Integridad - Baremos2025
Verifica que todos los enlaces, imágenes y archivos estén correctos

Autor: @joanh
Asistente: Claude Sonnet 4.0
"""

import os
import sys
from pathlib import Path
import re

def verificar_archivos_img():
    """Verifica que todas las imágenes referenciadas existan"""
    print("🖼️ VERIFICANDO IMÁGENES...")
    
    img_dir = Path("img")
    
    # Especialidades esperadas
    especialidades = [
        "filosofia_001",
        "lengua_y_literatura_004", 
        "geografia_e_historia_005",
        "matematicas_006",
        "fisica_y_quimica_007",
        "biologia_geologia_008",
        "frances_010",
        "ingles_011",
        "educacion_fisica_017",
        "orientacion_educativa_018",
        "tecnologia_019",
        "informatica_107"
    ]
    
    errores = []
    
    for esp in especialidades:
        archivo_img = img_dir / f"baremo_{esp}_2025.png"
        if not archivo_img.exists():
            errores.append(f"❌ Falta imagen: {archivo_img}")
        else:
            print(f"✅ {archivo_img}")
    
    # Verificar social preview
    social_preview = img_dir / "social-preview.png"
    if social_preview.exists():
        print(f"✅ {social_preview}")
    else:
        errores.append(f"❌ Falta: {social_preview}")
    
    return errores

def verificar_enlaces_readme():
    """Verifica los enlaces en el README principal"""
    print("\n📖 VERIFICANDO README PRINCIPAL...")
    
    with open("README.md", 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    errores = []
    
    # Buscar todos los enlaces a imágenes
    patron_img = r'!\[.*?\]\((.*?\.png)\)'
    imagenes = re.findall(patron_img, contenido)
    
    for img in imagenes:
        if not Path(img).exists():
            errores.append(f"❌ Imagen no encontrada: {img}")
        else:
            print(f"✅ {img}")
    
    # Buscar enlaces a directorios
    patron_dir = r'\[.*?\]\((especialidades/.*?/)\)'
    directorios = re.findall(patron_dir, contenido)
    
    for dir_path in directorios:
        if not Path(dir_path).exists():
            errores.append(f"❌ Directorio no encontrado: {dir_path}")
        else:
            print(f"✅ {dir_path}")
    
    return errores

def verificar_especialidades():
    """Verifica que cada especialidad tenga su estructura completa"""
    print("\n🔧 VERIFICANDO ESPECIALIDADES...")
    
    especialidades_dir = Path("especialidades")
    errores = []
    
    for esp_dir in especialidades_dir.iterdir():
        if esp_dir.is_dir():
            print(f"\n📁 {esp_dir.name}:")
            
            # Verificar README
            readme = esp_dir / "README.md"
            if readme.exists():
                print(f"  ✅ README.md")
            else:
                errores.append(f"❌ {esp_dir}/README.md no existe")
            
            # Verificar config.yaml
            config = esp_dir / "config.yaml"
            if config.exists():
                print(f"  ✅ config.yaml")
            else:
                errores.append(f"❌ {esp_dir}/config.yaml no existe")
            
            # Verificar directorio output
            output_dir = esp_dir / "output"
            if output_dir.exists():
                print(f"  ✅ output/")
                
                # Verificar archivos principales en output
                archivos_esperados = [".csv", ".txt", ".py", ".png"]
                for ext in archivos_esperados:
                    archivos = list(output_dir.glob(f"*{ext}"))
                    if archivos:
                        print(f"    ✅ Archivos {ext}: {len(archivos)}")
                    else:
                        errores.append(f"❌ {esp_dir}/output/ sin archivos {ext}")
            else:
                errores.append(f"❌ {esp_dir}/output/ no existe")
    
    return errores

def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN COMPLETA DE INTEGRIDAD - BAREMOS2025")
    print("=" * 60)
    
    os.chdir(Path(__file__).parent.parent)
    
    todos_errores = []
    
    # Verificar imágenes
    errores_img = verificar_archivos_img()
    todos_errores.extend(errores_img)
    
    # Verificar README
    errores_readme = verificar_enlaces_readme()
    todos_errores.extend(errores_readme)
    
    # Verificar especialidades
    errores_esp = verificar_especialidades()
    todos_errores.extend(errores_esp)
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE VERIFICACIÓN")
    
    if todos_errores:
        print(f"\n❌ Se encontraron {len(todos_errores)} errores:")
        for error in todos_errores:
            print(f"  {error}")
        sys.exit(1)
    else:
        print("\n🎉 ¡VERIFICACIÓN COMPLETADA SIN ERRORES!")
        print("✅ Repositorio listo para publicación")
        print("🚀 Todos los archivos e enlaces están correctos")

if __name__ == "__main__":
    main()
