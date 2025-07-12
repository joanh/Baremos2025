#!/usr/bin/env python3
"""
Extractor de puntuaciones para Geografía e Historia (005) - Baremos 2025
Procesa páginas 360-661 del PDF oficial de baremos
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import pdfplumber
import re
import yaml
from pathlib import Path

def cargar_configuracion():
    """Carga la configuración desde config.yaml"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def extraer_puntuaciones_geografia_historia():
    """
    Extrae las puntuaciones de Geografía e Historia del PDF oficial
    Páginas: 360-661 (7 candidatos primera página, 6 candidatos última página)
    """
    
    # Cargar configuración
    config = cargar_configuracion()
    
    # Rutas
    base_dir = Path(__file__).parent.parent.parent.parent
    pdf_path = base_dir / config['extraccion']['archivo_pdf']
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    print(f"🗺️ Extrayendo puntuaciones de Geografía e Historia (005)")
    print(f"📄 PDF: {pdf_path}")
    print(f"📄 Procesando páginas {config['extraccion']['pagina_inicio']}-{config['extraccion']['pagina_fin']}")
    
    puntuaciones = []
    patron_dni = r'\*\*\*\*'
    patron_numero = r'(\d+[,\.]\d+|\d+)'
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Procesar el rango de páginas especificado
            for num_pagina in range(config['extraccion']['pagina_inicio'] - 1, config['extraccion']['pagina_fin']):
                if num_pagina >= len(pdf.pages):
                    break
                    
                pagina = pdf.pages[num_pagina]
                texto = pagina.extract_text()
                
                if texto:
                    lineas = texto.split('\n')
                    for linea in lineas:
                        # Buscar líneas que contengan DNI enmascarado
                        if re.search(patron_dni, linea):
                            # Patrón específico para Geografía e Historia:
                            # ****XXXX* APELLIDOS, NOMBRE PUNTUACION_TOTAL ...
                            patron_geografia = r'\*\*\*\*\d+\*\s+[^0-9]+\s+(\d+[,\.]\d+)'
                            match = re.search(patron_geografia, linea)
                            if match:
                                puntuacion_str = match.group(1).replace(',', '.')
                                try:
                                    puntuacion = float(puntuacion_str)
                                    # Limitar al rango válido (0-10)
                                    if puntuacion > 10.0:
                                        puntuacion = 10.0
                                    puntuaciones.append(puntuacion)
                                except ValueError:
                                    continue
                
                # Progreso cada 50 páginas
                if (num_pagina + 1) % 50 == 0:
                    print(f"📖 Procesadas {num_pagina + 1 - (config['extraccion']['pagina_inicio'] - 1)} páginas...")
    
    except Exception as e:
        print(f"❌ Error procesando PDF: {e}")
        return []
    
    print(f"✅ Extracción completada: {len(puntuaciones)} candidatos encontrados")
    
    # Validación con datos de control
    validar_extraccion(puntuaciones, config)
    
    # Guardar en múltiples formatos
    guardar_resultados(puntuaciones, output_dir, config)
    
    return puntuaciones

def validar_extraccion(puntuaciones, config):
    """Valida la extracción comparando con puntuaciones de control"""
    
    print(f"\n📊 VALIDACIÓN DE DATOS:")
    print(f"Total candidatos extraídos: {len(puntuaciones)}")
    
    # Validar primeras 21 puntuaciones
    primeras_esperadas = config['validacion']['primeras_puntuaciones']
    if len(puntuaciones) >= len(primeras_esperadas):
        primeras_extraidas = puntuaciones[:len(primeras_esperadas)]
        coincidencias_primeras = sum(1 for e, r in zip(primeras_esperadas, primeras_extraidas) if abs(e - r) < 0.01)
        print(f"✅ Primeras {len(primeras_esperadas)} puntuaciones: {coincidencias_primeras}/{len(primeras_esperadas)} coincidencias")
        
        if coincidencias_primeras < len(primeras_esperadas):
            print("⚠️  Diferencias en primeras puntuaciones:")
            for i, (e, r) in enumerate(zip(primeras_esperadas, primeras_extraidas)):
                if abs(e - r) >= 0.01:
                    print(f"   Posición {i+1}: esperado {e}, obtenido {r}")
    
    # Validar últimas 20 puntuaciones
    ultimas_esperadas = config['validacion']['ultimas_puntuaciones']
    if len(puntuaciones) >= len(ultimas_esperadas):
        ultimas_extraidas = puntuaciones[-len(ultimas_esperadas):]
        coincidencias_ultimas = sum(1 for e, r in zip(ultimas_esperadas, ultimas_extraidas) if abs(e - r) < 0.01)
        print(f"✅ Últimas {len(ultimas_esperadas)} puntuaciones: {coincidencias_ultimas}/{len(ultimas_esperadas)} coincidencias")
        
        if coincidencias_ultimas < len(ultimas_esperadas):
            print("⚠️  Diferencias en últimas puntuaciones:")
            for i, (e, r) in enumerate(zip(ultimas_esperadas, ultimas_extraidas)):
                if abs(e - r) >= 0.01:
                    print(f"   Posición {i+1}: esperado {e}, obtenido {r}")

def guardar_resultados(puntuaciones, output_dir, config):
    """Guarda los resultados en múltiples formatos"""
    
    nombre_base = f"geografia_historia_{config['especialidad']['codigo']}"
    
    # CSV
    csv_path = output_dir / f"{nombre_base}.csv"
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("candidato,puntuacion\n")
        for i, punt in enumerate(puntuaciones, 1):
            f.write(f"{i},{punt}\n")
    
    # TXT simple
    txt_path = output_dir / f"{nombre_base}.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        for punt in puntuaciones:
            f.write(f"{punt}\n")
    
    # Lista Python
    py_path = output_dir / f"lista_{nombre_base}.py"
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write(f"# Puntuaciones {config['especialidad']['nombre']} ({config['especialidad']['codigo']}) - Baremos 2025\n")
        f.write(f"# Total candidatos: {len(puntuaciones)}\n\n")
        f.write(f"puntuaciones_{nombre_base} = [\n")
        for i, punt in enumerate(puntuaciones):
            f.write(f"    {punt}")
            if i < len(puntuaciones) - 1:
                f.write(",")
            f.write("\n")
        f.write("]\n")
    
    # Estadísticas básicas
    if puntuaciones:
        import numpy as np
        
        media = np.mean(puntuaciones)
        std = np.std(puntuaciones)
        mediana = np.median(puntuaciones)
        minimo = np.min(puntuaciones)
        maximo = np.max(puntuaciones)
        
        stats_path = output_dir / f"estadisticas_{nombre_base}.txt"
        with open(stats_path, 'w', encoding='utf-8') as f:
            f.write(f"Estadísticas {config['especialidad']['nombre']} ({config['especialidad']['codigo']}) - Baremos 2025\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Total candidatos: {len(puntuaciones)}\n")
            f.write(f"Media: {media:.2f}\n")
            f.write(f"Desviación estándar: {std:.2f}\n")
            f.write(f"Mediana: {mediana:.2f}\n")
            f.write(f"Mínimo: {minimo:.2f}\n")
            f.write(f"Máximo: {maximo:.2f}\n")
            f.write(f"Rango: {minimo:.2f} - {maximo:.2f}\n")
    
    print(f"💾 Resultados guardados en: {output_dir}")
    print(f"   📊 CSV: {csv_path.name}")
    print(f"   📄 TXT: {txt_path.name}")
    print(f"   🐍 Python: {py_path.name}")
    print(f"   📈 Estadísticas: estadisticas_{nombre_base}.txt")

if __name__ == "__main__":
    puntuaciones = extraer_puntuaciones_geografia_historia()
    if puntuaciones:
        print(f"\n🎯 Proceso completado exitosamente!")
        print(f"📊 {len(puntuaciones)} candidatos de Geografía e Historia procesados")
    else:
        print(f"\n❌ Error: No se pudieron extraer puntuaciones")
        sys.exit(1)
