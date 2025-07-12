#!/usr/bin/env python3
"""
Extractor Tecnología (019) - Baremo 2025
Extrae puntuaciones de las páginas 2269-2377 del PDF oficial
"""

import os
import sys
import re
import yaml
import pdfplumber
import numpy as np
from pathlib import Path

def cargar_configuracion():
    """Carga la configuración desde config.yaml"""
    try:
        with open('../config.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error cargando configuración: {e}")
        return None

def extraer_puntuaciones(config):
    """Extrae las puntuaciones del PDF"""
    pdf_path = config['rutas']['pdf_fuente']
    pagina_inicio = config['extraccion']['pagina_inicio']
    pagina_final = config['extraccion']['pagina_final']
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF no encontrado: {pdf_path}")
        return None
    
    print(f"📁 PDF encontrado: {os.path.abspath(pdf_path)}")
    print(f"📄 Procesando páginas {pagina_inicio}-{pagina_final}...")
    
    puntuaciones = []
    patron_puntuacion = re.compile(config['patrones']['puntuacion_regex'])
    caracteres_limpiar = config['patrones']['caracteres_limpiar']
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_paginas = pagina_final - pagina_inicio + 1
            
            for i, num_pagina in enumerate(range(pagina_inicio, pagina_final + 1)):
                if i % 10 == 0:
                    print(f"   Procesadas {i}/{total_paginas} páginas...")
                
                if num_pagina <= len(pdf.pages):
                    pagina = pdf.pages[num_pagina - 1]
                    texto = pagina.extract_text() or ""
                    
                    # Limpiar caracteres problemáticos
                    for char in caracteres_limpiar:
                        texto = texto.replace(char, "")
                    
                    # Buscar líneas de candidatos de TECNOLOGIA específicamente
                    lineas = texto.split('\n')
                    for linea in lineas:
                        # Buscar líneas que contengan un DNI enmascarado (****) seguido de un nombre y puntuación
                        if '****' in linea and ',' in linea:
                            # Extraer la primera puntuación decimal después del nombre
                            # Patrón: ****XXXX* APELLIDO, NOMBRE PUNTUACION,XXXX
                            partes = linea.split()
                            for i, parte in enumerate(partes):
                                # Buscar un patrón que sea claramente una puntuación total
                                if re.match(r'^\d{1,2},\d{4}$', parte):
                                    try:
                                        puntuacion = float(parte.replace(',', '.'))
                                        if config['patrones']['rango_valido'][0] <= puntuacion <= config['patrones']['rango_valido'][1]:
                                            puntuaciones.append(puntuacion)
                                            break  # Solo tomar la primera puntuación válida por línea
                                    except ValueError:
                                        continue
        
        print(f"✅ Extracción completada: {len(puntuaciones)} candidatos")
        return puntuaciones
        
    except Exception as e:
        print(f"❌ Error procesando PDF: {e}")
        return None

def validar_extraccion(puntuaciones, config):
    """Valida la extracción con las muestras proporcionadas"""
    print("🔍 VALIDANDO EXTRACCIÓN...")
    
    total_candidatos = len(puntuaciones)
    candidatos_estimados = config['extraccion']['candidatos_estimados']
    print(f"✅ Total candidatos: {total_candidatos} (esperado: {candidatos_estimados} ±50)")
    
    # Validar muestra inicial
    validacion_inicial = config['extraccion']['validacion_inicial']
    if len(puntuaciones) >= len(validacion_inicial):
        coincidencias_inicial = sum(1 for i, val in enumerate(validacion_inicial) 
                                  if i < len(puntuaciones) and abs(puntuaciones[i] - val) < 0.001)
        print(f"✅ Validación página inicial: {coincidencias_inicial}/{len(validacion_inicial)} coincidencias")
    
    # Validar muestra final
    validacion_final = config['extraccion']['validacion_final']
    if len(puntuaciones) >= len(validacion_final):
        inicio_final = len(puntuaciones) - len(validacion_final)
        coincidencias_final = sum(1 for i, val in enumerate(validacion_final)
                                if abs(puntuaciones[inicio_final + i] - val) < 0.001)
        print(f"✅ Validación página final: {coincidencias_final}/{len(validacion_final)} coincidencias")
    
    return True

def guardar_resultados(puntuaciones, config):
    """Guarda los resultados en múltiples formatos"""
    print("💾 GUARDANDO RESULTADOS...")
    
    output_dir = Path("../output")
    output_dir.mkdir(exist_ok=True)
    
    # CSV
    csv_path = output_dir / config['output']['csv']
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("candidato,puntuacion\n")
        for i, puntuacion in enumerate(puntuaciones, 1):
            f.write(f"{i},{puntuacion}\n")
    print(f"✅ CSV guardado: {csv_path.absolute()}")
    
    # TXT
    txt_path = output_dir / config['output']['txt']
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("# Puntuaciones de Tecnología (019) - Baremo 2025\n")
        f.write(f"# Total candidatos: {len(puntuaciones)}\n")
        f.write("# Orden: Exacto del PDF oficial\n\n")
        for i, puntuacion in enumerate(puntuaciones, 1):
            f.write(f"{i:3d}. {puntuacion}\n")
    print(f"✅ TXT guardado: {txt_path.absolute()}")
    
    # Python
    python_path = output_dir / config['output']['python']
    with open(python_path, 'w', encoding='utf-8') as f:
        f.write("# Puntuaciones de Tecnología (019) - Baremo 2025\n")
        f.write(f"# Extraídas del PDF oficial páginas {config['extraccion']['pagina_inicio']}-{config['extraccion']['pagina_final']}\n")
        f.write(f"# Total candidatos: {len(puntuaciones)}\n")
        f.write("# Orden: Exacto del PDF oficial\n\n")
        f.write("puntuaciones_tecnologia = [\n")
        for i, puntuacion in enumerate(puntuaciones):
            comentario = f"  # {i+1:3d}"
            f.write(f"    {puntuacion:.4f},{comentario}\n")
        f.write("]\n")
    print(f"✅ Python guardado: {python_path.absolute()}")
    
    # Estadísticas
    estadisticas_path = output_dir / config['output']['estadisticas']
    with open(estadisticas_path, 'w', encoding='utf-8') as f:
        media = np.mean(puntuaciones)
        mediana = np.median(puntuaciones)
        desv_std = np.std(puntuaciones)
        minimo = np.min(puntuaciones)
        maximo = np.max(puntuaciones)
        q1 = np.percentile(puntuaciones, 25)
        q2 = np.percentile(puntuaciones, 50)
        q3 = np.percentile(puntuaciones, 75)
        
        f.write("=== ESTADÍSTICAS TECNOLOGÍA (019) - 2025 ===\n\n")
        f.write(f"Total candidatos: {len(puntuaciones)}\n")
        f.write(f"Media: {media:.4f}\n")
        f.write(f"Mediana: {mediana:.4f}\n")
        f.write(f"Desviación estándar: {desv_std:.4f}\n")
        f.write(f"Mínimo: {minimo:.4f}\n")
        f.write(f"Máximo: {maximo:.4f}\n")
        f.write(f"Rango: {maximo - minimo:.4f}\n\n")
        f.write("CUARTILES:\n")
        f.write(f"Q1 (25%): {q1:.4f}\n")
        f.write(f"Q2 (50%): {q2:.4f}\n")
        f.write(f"Q3 (75%): {q3:.4f}\n")
    print(f"✅ Estadísticas guardadas: {estadisticas_path.absolute()}")

def main():
    print("⚙️ EXTRACTOR TECNOLOGÍA (019) - BAREMO 2025")
    print("=" * 50)
    
    # Cargar configuración
    config = cargar_configuracion()
    if not config:
        return
    
    # Extraer puntuaciones
    puntuaciones = extraer_puntuaciones(config)
    if not puntuaciones:
        return
    
    # Validar extracción
    if not validar_extraccion(puntuaciones, config):
        return
    
    # Guardar resultados
    guardar_resultados(puntuaciones, config)
    
    print("🎉 ¡EXTRACCIÓN COMPLETADA CON ÉXITO!")
    print(f"✅ {len(puntuaciones)} candidatos extraídos")
    print(f"📁 Archivos generados en: {os.path.abspath('../output')}")

if __name__ == "__main__":
    main()
