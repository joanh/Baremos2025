#!/usr/bin/env python3
"""
Script para corregir el código de Matemáticas de 008 a 006
"""

import os
import shutil
from pathlib import Path

def corregir_codigo_matematicas():
    """Corrige todas las referencias del código 008 a 006 para Matemáticas"""
    
    base_dir = Path(".")
    
    print("🔧 Iniciando corrección del código de Matemáticas (008 → 006)")
    
    # 1. Crear el nuevo directorio
    nuevo_dir = base_dir / "especialidades" / "matematicas_006"
    viejo_dir = base_dir / "especialidades" / "matematicas_008"
    
    if viejo_dir.exists() and not nuevo_dir.exists():
        print(f"📁 Copiando {viejo_dir} → {nuevo_dir}")
        shutil.copytree(viejo_dir, nuevo_dir)
    
    # 2. Actualizar archivos en el nuevo directorio
    archivos_a_corregir = [
        nuevo_dir / "scripts" / "extractor_matematicas_SIMPLE.py",
        nuevo_dir / "scripts" / "extractor_matematicas_PRUEBA.py", 
        nuevo_dir / "scripts" / "extractor_matematicas_FINAL.py",
        nuevo_dir / "scripts" / "extractor_matematicas.py",
        nuevo_dir / "scripts" / "visualizador_matematicas_CORREGIDO.py",
        nuevo_dir / "scripts" / "visualizador_matematicas.py"
    ]
    
    for archivo in archivos_a_corregir:
        if archivo.exists():
            print(f"📝 Corrigiendo {archivo}")
            
            # Leer contenido
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Reemplazar todas las referencias
            contenido = contenido.replace("008", "006")
            contenido = contenido.replace("Matemáticas 008", "Matemáticas 006")
            contenido = contenido.replace("MATEMÁTICAS (008)", "MATEMÁTICAS (006)")
            contenido = contenido.replace("matematicas_008", "matematicas_006")
            contenido = contenido.replace("baremo_matematicas_008_2025", "baremo_matematicas_006_2025")
            contenido = contenido.replace("lista_matematicas_008", "lista_matematicas_006")
            
            # Escribir contenido corregido
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write(contenido)
    
    # 3. Renombrar archivos de salida si existen
    output_dir = nuevo_dir / "output"
    if output_dir.exists():
        archivos_output = [
            "puntuaciones_matematicas_008.csv",
            "puntuaciones_matematicas_008.txt", 
            "puntuaciones_matematicas_008.py",
            "lista_matematicas_008.py",
            "estadisticas_matematicas_008.txt",
            "baremo_matematicas_008_2025.png",
            "baremo_matematicas_008_2025.pdf"
        ]
        
        for archivo_viejo in archivos_output:
            archivo_viejo_path = output_dir / archivo_viejo
            if archivo_viejo_path.exists():
                archivo_nuevo = archivo_viejo.replace("008", "006")
                archivo_nuevo_path = output_dir / archivo_nuevo
                print(f"📄 Renombrando {archivo_viejo} → {archivo_nuevo}")
                shutil.move(archivo_viejo_path, archivo_nuevo_path)
    
    # 4. Actualizar el contenido de los archivos renombrados
    archivos_contenido = [
        output_dir / "puntuaciones_matematicas_006.csv",
        output_dir / "puntuaciones_matematicas_006.txt",
        output_dir / "puntuaciones_matematicas_006.py", 
        output_dir / "lista_matematicas_006.py",
        output_dir / "estadisticas_matematicas_006.txt"
    ]
    
    for archivo in archivos_contenido:
        if archivo.exists():
            print(f"📝 Actualizando contenido de {archivo}")
            
            # Leer contenido
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Reemplazar referencias internas
            contenido = contenido.replace("008", "006")
            contenido = contenido.replace("Matemáticas (008)", "Matemáticas (006)")
            contenido = contenido.replace("MATEMÁTICAS (008)", "MATEMÁTICAS (006)")
            
            # Escribir contenido corregido
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write(contenido)
    
    # 5. Copiar imagen corregida al directorio img principal
    img_source = nuevo_dir / "output" / "baremo_matematicas_006_2025.png"
    img_dest = base_dir / "img" / "baremo_matematicas_006_2025.png"
    
    if img_source.exists():
        print(f"🖼️ Copiando imagen: {img_source} → {img_dest}")
        shutil.copy2(img_source, img_dest)
    
    # 6. Eliminar imagen antigua si existe
    img_vieja = base_dir / "img" / "baremo_matematicas_008_2025.png"
    if img_vieja.exists():
        print(f"🗑️ Eliminando imagen antigua: {img_vieja}")
        os.remove(img_vieja)
    
    print("✅ Corrección completada!")
    print("\n📋 Pasos realizados:")
    print("   • Directorio matematicas_008 copiado a matematicas_006")
    print("   • Archivos de scripts actualizados con código 006")
    print("   • Archivos de output renombrados")
    print("   • Contenido interno actualizado")
    print("   • Imagen copiada al directorio img principal")
    print("\n⚠️ Recordatorio: Eliminar manualmente el directorio matematicas_008 cuando confirmes que todo funciona")

if __name__ == "__main__":
    corregir_codigo_matematicas()
