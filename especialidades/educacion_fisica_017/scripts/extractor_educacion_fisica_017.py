#!/usr/bin/env python3
"""
Extractor de puntuaciones para Educación Física (017) - Baremos 2025
Páginas: 1754-2031 (aproximadamente 278 páginas)
Especialidad con alto volumen de candidatos
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import pdfplumber
import re
import csv
from pathlib import Path
import yaml

def cargar_configuracion():
    """Carga la configuración desde config.yaml"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def extraer_puntuaciones_educacion_fisica():
    """
    Extrae puntuaciones de Educación Física del PDF principal
    Páginas: 1754-2031
    """
    
    config = cargar_configuracion()
    
    # Configuración
    PDF_PATH = Path(__file__).parent.parent.parent.parent / config['archivo']['pdf']
    PAGINA_INICIO = config['especialidad']['pagina_inicio']  # 1754
    PAGINA_FINAL = config['especialidad']['pagina_final']    # 2031
    
    print("🏃‍♂️ EXTRACTOR DE EDUCACIÓN FÍSICA (017) - BAREMOS 2025")
    print("=" * 60)
    print(f"📄 PDF: {PDF_PATH.name}")
    print(f"📊 Rango: Páginas {PAGINA_INICIO} - {PAGINA_FINAL}")
    print(f"📝 Candidatos esperados: ~1,500-2,000 (estimación)")
    
    if not PDF_PATH.exists():
        print(f"❌ Error: No se encuentra el archivo {PDF_PATH}")
        return []
    
    puntuaciones_extraidas = []
    paginas_procesadas = 0
    paginas_con_datos = 0
    
    # Patrón optimizado para Educación Física
    # Basado en el análisis de otras especialidades
    patron_educacion_fisica = r'\*\*\*\*\d+\*\s+[^0-9]+?\s+(\d+[,\.]\d+)'
    
    try:
        with pdfplumber.open(PDF_PATH) as pdf:
            total_paginas = PAGINA_FINAL - PAGINA_INICIO + 1
            
            for num_pagina in range(PAGINA_INICIO - 1, PAGINA_FINAL):
                if num_pagina >= len(pdf.pages):
                    print(f"⚠️ Página {num_pagina + 1} fuera del rango del PDF")
                    break
                
                pagina = pdf.pages[num_pagina]
                texto_pagina = pagina.extract_text() or ""
                
                # Buscar puntuaciones en esta página
                matches = re.findall(patron_educacion_fisica, texto_pagina, re.DOTALL)
                
                puntuaciones_pagina = []
                for match in matches:
                    try:
                        # Normalizar formato decimal
                        puntuacion_str = match.replace(',', '.')
                        puntuacion = float(puntuacion_str)
                        
                        # Filtro de rango válido (0-15 para incluir posibles valores)
                        if 0 <= puntuacion <= 15:
                            puntuaciones_pagina.append(puntuacion)
                        else:
                            print(f"⚠️ Puntuación fuera de rango: {puntuacion} en página {num_pagina + 1}")
                            
                    except ValueError:
                        print(f"⚠️ Error al convertir: '{match}' en página {num_pagina + 1}")
                        continue
                
                if puntuaciones_pagina:
                    puntuaciones_extraidas.extend(puntuaciones_pagina)
                    paginas_con_datos += 1
                    
                    # Log detallado para las primeras y últimas páginas
                    if num_pagina < PAGINA_INICIO + 2 or num_pagina > PAGINA_FINAL - 3:
                        print(f"📄 Página {num_pagina + 1}: {len(puntuaciones_pagina)} candidatos - Muestra: {puntuaciones_pagina[:3]}...")
                
                paginas_procesadas += 1
                
                # Progreso cada 50 páginas
                if paginas_procesadas % 50 == 0:
                    print(f"🔄 Progreso: {paginas_procesadas}/{total_paginas} páginas ({paginas_procesadas/total_paginas*100:.1f}%)")
    
    except Exception as e:
        print(f"❌ Error al procesar PDF: {str(e)}")
        return []
    
    print(f"\n📊 RESUMEN DE EXTRACCIÓN:")
    print(f"   📄 Páginas procesadas: {paginas_procesadas}")
    print(f"   📝 Páginas con datos: {paginas_con_datos}")
    print(f"   🎯 Total candidatos: {len(puntuaciones_extraidas)}")
    
    if puntuaciones_extraidas:
        print(f"   📈 Rango: {min(puntuaciones_extraidas):.4f} - {max(puntuaciones_extraidas):.4f}")
        print(f"   📊 Media aproximada: {sum(puntuaciones_extraidas)/len(puntuaciones_extraidas):.2f}")
    
    return puntuaciones_extraidas

def validar_extraccion(puntuaciones, config):
    """Valida la extracción usando las puntuaciones de control"""
    
    print(f"\n🔍 VALIDACIÓN DE DATOS:")
    print("=" * 50)
    
    if not puntuaciones:
        print("❌ No hay puntuaciones para validar")
        return False
    
    # Validaciones de control
    validacion_inicio = config['especialidad']['validacion_inicio']
    validacion_final = config['especialidad']['validacion_final']
    
    print(f"🎯 Validando primeras {len(validacion_inicio)} puntuaciones...")
    coincidencias_inicio = 0
    for i, esperada in enumerate(validacion_inicio):
        if i < len(puntuaciones):
            if abs(puntuaciones[i] - esperada) < 0.001:
                coincidencias_inicio += 1
            else:
                print(f"   ⚠️ Diferencia en pos {i+1}: esperada {esperada}, obtenida {puntuaciones[i]}")
    
    print(f"🎯 Validando últimas {len(validacion_final)} puntuaciones...")
    coincidencias_final = 0
    inicio_final = len(puntuaciones) - len(validacion_final)
    for i, esperada in enumerate(validacion_final):
        pos_real = inicio_final + i
        if pos_real >= 0 and pos_real < len(puntuaciones):
            if abs(puntuaciones[pos_real] - esperada) < 0.001:
                coincidencias_final += 1
            else:
                print(f"   ⚠️ Diferencia en pos final {i+1}: esperada {esperada}, obtenida {puntuaciones[pos_real]}")
    
    print(f"\n📊 RESULTADOS DE VALIDACIÓN:")
    print(f"   ✅ Inicio: {coincidencias_inicio}/{len(validacion_inicio)} coincidencias")
    print(f"   ✅ Final: {coincidencias_final}/{len(validacion_final)} coincidencias")
    
    exito_inicio = coincidencias_inicio >= len(validacion_inicio) * 0.9  # 90% de coincidencias
    exito_final = coincidencias_final >= len(validacion_final) * 0.9
    
    if exito_inicio and exito_final:
        print("🎉 ¡VALIDACIÓN EXITOSA! Los datos extraídos son correctos")
        return True
    else:
        print("⚠️ VALIDACIÓN PARCIAL. Revisar el patrón de extracción")
        return False

def guardar_resultados(puntuaciones, config):
    """Guarda los resultados en múltiples formatos"""
    
    if not puntuaciones:
        print("❌ No hay puntuaciones para guardar")
        return
    
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    codigo = config['especialidad']['codigo']
    nombre_base = f"educacion_fisica_{codigo}"
    
    print(f"\n💾 GUARDANDO RESULTADOS:")
    print("=" * 40)
    
    # 1. Archivo TXT (puntuaciones simples)
    txt_path = output_dir / f"{nombre_base}.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        for puntuacion in puntuaciones:
            f.write(f"{puntuacion}\n")
    print(f"✅ TXT: {txt_path}")
    
    # 2. Archivo CSV con más detalles
    csv_path = output_dir / f"{nombre_base}.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Posicion', 'Puntuacion', 'Especialidad'])
        for i, puntuacion in enumerate(puntuaciones, 1):
            writer.writerow([i, puntuacion, 'Educación Física'])
    print(f"✅ CSV: {csv_path}")
    
    # 3. Estadísticas completas
    estadisticas_path = output_dir / f"estadisticas_{nombre_base}_completas.txt"
    with open(estadisticas_path, 'w', encoding='utf-8') as f:
        f.write("ESTADÍSTICAS COMPLETAS - EDUCACIÓN FÍSICA (017)\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total candidatos: {len(puntuaciones)}\n")
        f.write(f"Media: {sum(puntuaciones)/len(puntuaciones):.4f}\n")
        f.write(f"Mediana: {sorted(puntuaciones)[len(puntuaciones)//2]:.4f}\n")
        f.write(f"Mínimo: {min(puntuaciones):.4f}\n")
        f.write(f"Máximo: {max(puntuaciones):.4f}\n")
        
        import statistics
        f.write(f"Desviación estándar: {statistics.stdev(puntuaciones):.4f}\n")
        
        # Distribución por rangos
        f.write(f"\nDISTRIBUCIÓN POR RANGOS:\n")
        rangos = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 15)]
        for min_r, max_r in rangos:
            count = sum(1 for p in puntuaciones if min_r <= p < max_r)
            porcentaje = (count / len(puntuaciones)) * 100
            f.write(f"{min_r}-{max_r}: {count} candidatos ({porcentaje:.1f}%)\n")
    
    print(f"✅ Estadísticas: {estadisticas_path}")
    print(f"\n🎯 Total archivos generados: 3")
    print(f"📊 Candidatos procesados: {len(puntuaciones)}")

def main():
    """Función principal del extractor"""
    
    print("🏃‍♂️ INICIANDO EXTRACCIÓN DE EDUCACIÓN FÍSICA")
    print("=" * 60)
    
    # Cargar configuración
    config = cargar_configuracion()
    
    # Extraer puntuaciones
    puntuaciones = extraer_puntuaciones_educacion_fisica()
    
    if not puntuaciones:
        print("❌ No se pudieron extraer puntuaciones")
        return
    
    # Validar extracción
    validacion_exitosa = validar_extraccion(puntuaciones, config)
    
    # Guardar resultados
    guardar_resultados(puntuaciones, config)
    
    print(f"\n🎉 ¡EXTRACCIÓN COMPLETADA!")
    print(f"📊 Total candidatos: {len(puntuaciones)}")
    print(f"✅ Validación: {'EXITOSA' if validacion_exitosa else 'PARCIAL'}")
    print(f"📁 Archivos en: especialidades/educacion_fisica_017/output/")

if __name__ == "__main__":
    main()
