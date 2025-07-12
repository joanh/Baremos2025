#!/usr/bin/env python3
"""
Script para verificar la integridad de enlaces e imágenes en el README
"""

from pathlib import Path
import re

def verificar_enlaces_imagenes():
    """Verifica que todas las imágenes referenciadas en el README existen"""
    
    readme_path = Path(__file__).parent.parent / "README.md"
    img_dir = Path(__file__).parent.parent / "img"
    
    print("🔍 Verificando integridad de enlaces e imágenes...")
    
    # Leer README
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # Buscar todas las referencias a imágenes
    image_pattern = r'!\[.*?\]\((img/[^)]+)\)'
    images_in_readme = re.findall(image_pattern, readme_content)
    
    print(f"📝 Encontradas {len(images_in_readme)} referencias a imágenes en README:")
    
    errores = []
    for img_ref in images_in_readme:
        img_path = Path(__file__).parent.parent / img_ref
        if img_path.exists():
            print(f"  ✅ {img_ref}")
        else:
            print(f"  ❌ {img_ref} - ARCHIVO NO ENCONTRADO")
            errores.append(img_ref)
    
    # Listar todas las imágenes disponibles
    print(f"\n📁 Imágenes disponibles en /img:")
    for img_file in sorted(img_dir.glob("*.png")):
        print(f"  📄 {img_file.name}")
    
    # Buscar archivos no referenciados
    print(f"\n🔍 Verificando archivos no referenciados:")
    referenced_files = set(Path(img_ref).name for img_ref in images_in_readme)
    available_files = set(f.name for f in img_dir.glob("*.png"))
    
    no_referenciados = available_files - referenced_files
    if no_referenciados:
        print("  ⚠️  Archivos no referenciados en README:")
        for archivo in sorted(no_referenciados):
            print(f"    📄 {archivo}")
    else:
        print("  ✅ Todos los archivos están referenciados")
    
    # Resumen
    print(f"\n📊 Resumen:")
    print(f"  • Referencias en README: {len(images_in_readme)}")
    print(f"  • Archivos disponibles: {len(available_files)}")
    print(f"  • Enlaces rotos: {len(errores)}")
    print(f"  • Archivos no referenciados: {len(no_referenciados)}")
    
    if errores:
        print(f"\n❌ Se encontraron {len(errores)} enlaces rotos que necesitan corrección")
        return False
    else:
        print(f"\n✅ Todos los enlaces a imágenes están correctos")
        return True

def verificar_enlaces_carpetas():
    """Verifica que todas las carpetas referenciadas existen"""
    
    readme_path = Path(__file__).parent.parent / "README.md"
    especialidades_dir = Path(__file__).parent.parent / "especialidades"
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # Buscar referencias a carpetas de especialidades
    folder_pattern = r'\[.*?\]\((especialidades/[^)]+)\)'
    folders_in_readme = re.findall(folder_pattern, readme_content)
    
    print(f"\n🔍 Verificando {len(folders_in_readme)} enlaces a carpetas:")
    
    errores_carpetas = []
    for folder_ref in folders_in_readme:
        folder_path = Path(__file__).parent.parent / folder_ref
        if folder_path.exists():
            print(f"  ✅ {folder_ref}")
        else:
            print(f"  ❌ {folder_ref} - CARPETA NO ENCONTRADA")
            errores_carpetas.append(folder_ref)
    
    if errores_carpetas:
        print(f"\n❌ Se encontraron {len(errores_carpetas)} enlaces a carpetas rotos")
        return False
    else:
        print(f"\n✅ Todos los enlaces a carpetas están correctos")
        return True

def main():
    """Función principal"""
    print("🚀 Iniciando verificación de integridad del README...\n")
    
    imagenes_ok = verificar_enlaces_imagenes()
    carpetas_ok = verificar_enlaces_carpetas()
    
    print(f"\n{'='*60}")
    if imagenes_ok and carpetas_ok:
        print("🎉 ¡VERIFICACIÓN COMPLETADA EXITOSAMENTE!")
        print("✅ Todos los enlaces están funcionando correctamente")
    else:
        print("⚠️  SE DETECTARON PROBLEMAS")
        if not imagenes_ok:
            print("❌ Hay enlaces rotos a imágenes")
        if not carpetas_ok:
            print("❌ Hay enlaces rotos a carpetas")
        print("📝 Revisa los errores reportados arriba")

if __name__ == "__main__":
    main()
