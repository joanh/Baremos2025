#!/usr/bin/env python3
"""
Extractor de Baremos - Informática 107
Mantiene el orden exacto del PDF oficial

Autor: @joanh
Asistente: Claude Sonnet 4.0
"""

import os
import sys
import yaml
import pdfplumber
import re
from pathlib import Path

# Configurar rutas
SCRIPT_DIR = Path(__file__).parent
ESPECIALIDAD_DIR = SCRIPT_DIR.parent
CONFIG_PATH = ESPECIALIDAD_DIR / "config.yaml"
DATA_DIR = ESPECIALIDAD_DIR / "data"
OUTPUT_DIR = ESPECIALIDAD_DIR / "output"

def cargar_configuracion():
    """Carga la configuración desde config.yaml"""
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error cargando configuración: {e}")
        sys.exit(1)

def extraer_candidatos_informatica(config):
    """Extrae candidatos de Informática manteniendo el orden del PDF"""
    
    # Configuración
    esp_config = config['especialidad']
    pdf_config = config['pdf']
    patrones = config['patrones']
    
    archivo_pdf = DATA_DIR / pdf_config['archivo']
    
    if not archivo_pdf.exists():
        print(f"❌ No se encuentra el archivo PDF: {archivo_pdf}")
        print(f"📁 Coloca el archivo en: {DATA_DIR}")
        return None
    
    print("=== EXTRACTOR ORDEN REAL - INFORMÁTICA 107 ===")
    print(f"📄 Procesando: {archivo_pdf.name}")
    print(f"📊 Páginas: {pdf_config['pagina_inicio']} - {pdf_config['pagina_fin']}")
    print(f"🎯 Candidatos esperados: {pdf_config['total_candidatos_esperado']}")
    print("=" * 60)
    
    candidatos = []  # Lista ordenada como en el PDF
    
    try:
        with pdfplumber.open(archivo_pdf) as pdf:
            print("Extrayendo candidatos en orden del PDF...")
            
            # Iterar por las páginas (ajustar índice 0-based)
            inicio = pdf_config['pagina_inicio'] - 1
            fin = pdf_config['pagina_fin']
            
            for num_pagina in range(inicio, fin):
                if num_pagina >= len(pdf.pages):
                    print(f"⚠️ Página {num_pagina + 1} no existe en el PDF")
                    continue
                    
                page = pdf.pages[num_pagina]
                
                try:
                    texto = page.extract_text()
                    if texto:
                        lineas = texto.split('\\n')
                        
                        for linea in lineas:
                            if linea.startswith('****') and '*' in linea[4:]:
                                numeros = re.findall(patrones['puntuacion'], linea)
                                
                                if numeros:
                                    primer_numero = numeros[0]
                                    try:
                                        valor = float(primer_numero.replace(',', '.'))
                                        if 0.0 <= valor <= 15.0:  # Rango ampliado por seguridad
                                            candidatos.append(valor)
                                            print(f"{len(candidatos):3d}. {valor:.4f}")
                                    except ValueError:
                                        pass
                
                except Exception as e:
                    print(f"⚠️ Error página {num_pagina + 1}: {e}")
    
    except Exception as e:
        print(f"❌ Error procesando PDF: {e}")
        return None
    
    return candidatos

def guardar_resultados(candidatos, config):
    """Guarda los resultados en múltiples formatos"""
    
    if not candidatos:
        print("❌ No hay candidatos para guardar")
        return False
    
    # Crear directorio de salida si no existe
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    output_config = config['output']
    esp_config = config['especialidad']
    
    print(f"\\n{'='*60}")
    print("=== GUARDANDO RESULTADOS ===")
    print(f"{'='*60}")
    print(f"📊 Total candidatos: {len(candidatos)}")
    
    try:
        # TXT con orden del PDF
        txt_path = OUTPUT_DIR / output_config['txt']
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"# {esp_config['nombre_completo']}\\n")
            f.write(f"# Código: {esp_config['codigo']}\\n")
            f.write(f"# Total candidatos: {len(candidatos)}\\n")
            f.write(f"# Orden: Exacto del PDF oficial\\n\\n")
            for i, puntuacion in enumerate(candidatos):
                f.write(f"{i+1:3d}. {puntuacion:.4f}\\n")
        print(f"💾 Guardado: {txt_path.name}")
        
        # CSV con orden del PDF
        csv_path = OUTPUT_DIR / output_config['csv']
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write("Posicion,Puntuacion_Total\\n")
            for i, puntuacion in enumerate(candidatos):
                f.write(f"{i+1},{puntuacion:.4f}\\n")
        print(f"💾 Guardado: {csv_path.name}")
        
        # Lista Python directa
        py_path = OUTPUT_DIR / "lista_informatica_107.py"
        with open(py_path, 'w', encoding='utf-8') as f:
            f.write(f"# {esp_config['nombre_completo']}\\n")
            f.write(f"# Código: {esp_config['codigo']}\\n")
            f.write(f"# Total: {len(candidatos)} candidatos\\n")
            f.write(f"# Orden: EXACTO del PDF oficial\\n\\n")
            f.write("puntuaciones_informatica = [\\n")
            for i, puntuacion in enumerate(candidatos):
                f.write(f"    {puntuacion:.4f},  # {i+1:3d}\\n")
            f.write("]\\n")
        print(f"💾 Guardado: {py_path.name}")
        
        # Estadísticas detalladas
        stats_path = OUTPUT_DIR / output_config['estadisticas']
        with open(stats_path, 'w', encoding='utf-8') as f:
            f.write(f"ESTADÍSTICAS - {esp_config['nombre_completo']}\\n")
            f.write("=" * 60 + "\\n\\n")
            f.write(f"📊 Total candidatos: {len(candidatos)}\\n")
            f.write(f"🏆 Puntuación máxima: {max(candidatos):.4f}\\n")
            f.write(f"📉 Puntuación mínima: {min(candidatos):.4f}\\n")
            f.write(f"📈 Media: {sum(candidatos)/len(candidatos):.4f}\\n")
            
            valores_unicos = len(set(candidatos))
            f.write(f"🎯 Puntuaciones diferentes: {valores_unicos}\\n")
            f.write(f"🔄 Candidatos con misma nota: {len(candidatos) - valores_unicos}\\n\\n")
            
            f.write("=== PRIMEROS 10 (orden PDF) ===\\n")
            for i in range(min(10, len(candidatos))):
                f.write(f"{i+1:3d}. {candidatos[i]:.4f}\\n")
            
            f.write("\\n=== ÚLTIMOS 10 (orden PDF) ===\\n")
            inicio = max(0, len(candidatos) - 10)
            for i in range(inicio, len(candidatos)):
                f.write(f"{i+1:3d}. {candidatos[i]:.4f}\\n")
        
        print(f"💾 Guardado: {stats_path.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error guardando resultados: {e}")
        return False

def mostrar_estadisticas(candidatos, config):
    """Muestra estadísticas en consola"""
    
    validacion = config['validacion']
    
    print(f"\\n=== ESTADÍSTICAS (SIN CAMBIAR ORDEN) ===")
    print(f"📊 Total candidatos: {len(candidatos)}")
    print(f"🏆 Puntuación máxima: {max(candidatos):.4f}")
    print(f"📉 Puntuación mínima: {min(candidatos):.4f}")
    print(f"📈 Media: {sum(candidatos)/len(candidatos):.4f}")
    
    # Validación
    print(f"\\n=== VALIDACIÓN ===")
    if validacion['min_candidatos'] <= len(candidatos) <= validacion['max_candidatos']:
        print(f"✅ Número de candidatos: {len(candidatos)} (esperado)")
    else:
        print(f"⚠️ Número de candidatos: {len(candidatos)} (fuera de rango esperado)")
    
    # Contar valores únicos SIN alterar la lista
    valores_unicos = len(set(candidatos))
    print(f"🎯 Puntuaciones diferentes: {valores_unicos}")
    print(f"🔄 Candidatos con misma nota: {len(candidatos) - valores_unicos}")
    
    # Primeros y últimos 10
    print(f"\\n=== PRIMEROS 10 (orden PDF) ===")
    for i in range(min(10, len(candidatos))):
        print(f"{i+1:3d}. {candidatos[i]:.4f}")
    
    print(f"\\n=== ÚLTIMOS 10 (orden PDF) ===")
    inicio = max(0, len(candidatos) - 10)
    for i in range(inicio, len(candidatos)):
        print(f"{i+1:3d}. {candidatos[i]:.4f}")

def main():
    """Función principal"""
    print("🚀 Iniciando extractor de Informática 107...")
    
    # Cargar configuración
    config = cargar_configuracion()
    
    # Extraer candidatos
    candidatos = extraer_candidatos_informatica(config)
    
    if candidatos is None:
        print("❌ Extracción fallida")
        sys.exit(1)
    
    # Guardar resultados
    if guardar_resultados(candidatos, config):
        print(f"\\n🎉 ¡EXTRACCIÓN COMPLETA!")
        print(f"✅ {len(candidatos)} candidatos procesados correctamente")
        print(f"📁 Archivos guardados en: {OUTPUT_DIR}")
        
        # Mostrar estadísticas
        mostrar_estadisticas(candidatos, config)
        
        print(f"\\n📋 CANDIDATOS EN ORDEN DEL PDF - SIN MODIFICACIONES")
        print("🔗 Listos para visualización")
        
    else:
        print("❌ Error guardando resultados")
        sys.exit(1)

if __name__ == "__main__":
    main()
