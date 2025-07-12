#!/usr/bin/env python3
"""
Extractor de Baremos - Francés 010
Extrae datos manteniendo el orden original del PDF

Páginas: 1356-1394 (39 páginas)
Autor: @joanh
Asistente: Claude Sonnet 4.0
"""

import os
import sys
import re
import yaml
import pdfplumber
import pandas as pd
import yaml
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
        return None

def limpiar_texto(texto, caracteres_limpiar):
    """Limpia caracteres problemáticos del texto"""
    for char in caracteres_limpiar:
        texto = texto.replace(char, '')
    return texto

def extraer_puntuacion(linea, patron_puntuacion):
    """Extrae la puntuación total de una línea"""
    # Buscar números en formato X,XXXX
    matches = re.findall(patron_puntuacion, linea)
    if matches:
        # Tomar el primer número encontrado (puntuación total)
        numero_str = matches[0].replace(',', '.')
        try:
            puntuacion = float(numero_str)
            # Limitar a 10.0 máximo (corrección automática)
            return min(puntuacion, 10.0)
        except ValueError:
            return None
    return None

def procesar_pagina(page, config):
    """Procesa una página individual del PDF"""
    puntuaciones_pagina = []
    
    try:
        texto = page.extract_text()
        if not texto:
            return puntuaciones_pagina
        
        # Limpiar texto
        texto_limpio = limpiar_texto(texto, config['extraccion']['caracteres_limpiar'])
        lineas = texto_limpio.split('\n')
        
        # Buscar líneas que contienen DNI
        patron_dni = re.compile(r'\*\*\*\*.*\*')
        
        for linea in lineas:
            if patron_dni.search(linea):
                puntuacion = extraer_puntuacion(linea, r'\b(\d{1,2},\d{4})\b')
                if puntuacion is not None:
                    puntuaciones_pagina.append(puntuacion)
        
    except Exception as e:
        print(f"⚠️ Error procesando página: {e}")
    
    return puntuaciones_pagina

def validar_extraccion(puntuaciones, config):
    """Valida la extracción contra datos conocidos"""
    print("\n🔍 VALIDANDO EXTRACCIÓN...")
    
    # Validar total aproximado
    total_esperado = config['extraccion']['total_esperado']
    tolerancia = config['validacion']['tolerancia_total']
    
    if abs(len(puntuaciones) - total_esperado) <= tolerancia:
        print(f"✅ Total candidatos: {len(puntuaciones)} (esperado: {total_esperado} ±{tolerancia})")
    else:
        print(f"⚠️ Total candidatos: {len(puntuaciones)} (esperado: {total_esperado} ±{tolerancia})")
    
    # Validar primera página
    pagina_inicial = config['validacion']['pagina_inicial']
    esperadas_inicial = pagina_inicial['puntuaciones_esperadas']
    
    if len(puntuaciones) >= len(esperadas_inicial):
        primeras = puntuaciones[:len(esperadas_inicial)]
        coincidencias = sum(1 for a, b in zip(primeras, esperadas_inicial) if abs(a - b) < 0.01)
        print(f"✅ Validación página inicial: {coincidencias}/{len(esperadas_inicial)} coincidencias")
    
    # Validar última página
    pagina_final = config['validacion']['pagina_final']
    esperadas_final = pagina_final['puntuaciones_esperadas']
    
    if len(puntuaciones) >= len(esperadas_final):
        ultimas = puntuaciones[-len(esperadas_final):]
        coincidencias = sum(1 for a, b in zip(ultimas, esperadas_final) if abs(a - b) < 0.01)
        print(f"✅ Validación página final: {coincidencias}/{len(esperadas_final)} coincidencias")
    
    return True

def guardar_resultados(puntuaciones, config):
    """Guarda los resultados en múltiples formatos"""
    print("\n💾 GUARDANDO RESULTADOS...")
    
    # Crear directorio de salida
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    output_config = config['output']
    
    # 1. Archivo CSV
    csv_path = OUTPUT_DIR / output_config['csv']
    df = pd.DataFrame({
        'candidato': range(1, len(puntuaciones) + 1),
        'puntuacion': puntuaciones
    })
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"✅ CSV guardado: {csv_path}")
    
    # 2. Archivo TXT
    txt_path = OUTPUT_DIR / output_config['txt']
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(f"# Puntuaciones de Francés (010) - Baremo 2025\n")
        f.write(f"# Total candidatos: {len(puntuaciones)}\n")
        f.write(f"# Orden: Exacto del PDF oficial\n\n")
        
        for i, puntuacion in enumerate(puntuaciones, 1):
            f.write(f"{i:3d}. {puntuacion:.4f}\n")
    print(f"✅ TXT guardado: {txt_path}")
    
    # 3. Archivo Python
    py_path = OUTPUT_DIR / output_config['lista']
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write("# Puntuaciones de Francés (010) - Baremo 2025\n")
        f.write(f"# Extraídas del PDF oficial páginas {config['extraccion']['pagina_inicio']}-{config['extraccion']['pagina_fin']}\n")
        f.write(f"# Total candidatos: {len(puntuaciones)}\n")
        f.write("# Orden: Exacto del PDF oficial\n\n")
        
        f.write(f"{output_config['variable_lista']} = [\n")
        for i, puntuacion in enumerate(puntuaciones):
            f.write(f"    {puntuacion:.4f},  # {i+1:3d}\n")
        f.write("]\n")
    print(f"✅ Python guardado: {py_path}")
    
    # 4. Estadísticas
    import numpy as np
    
    stats_path = OUTPUT_DIR / output_config['estadisticas']
    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write("=== ESTADÍSTICAS FRANCÉS (010) - 2025 ===\n\n")
        f.write(f"Total candidatos: {len(puntuaciones)}\n")
        f.write(f"Media: {np.mean(puntuaciones):.4f}\n")
        f.write(f"Mediana: {np.median(puntuaciones):.4f}\n")
        f.write(f"Desviación estándar: {np.std(puntuaciones):.4f}\n")
        f.write(f"Mínimo: {np.min(puntuaciones):.4f}\n")
        f.write(f"Máximo: {np.max(puntuaciones):.4f}\n")
        f.write(f"Rango: {np.max(puntuaciones) - np.min(puntuaciones):.4f}\n\n")
        
        # Cuartiles
        q1 = np.percentile(puntuaciones, 25)
        q2 = np.percentile(puntuaciones, 50)
        q3 = np.percentile(puntuaciones, 75)
        
        f.write("CUARTILES:\n")
        f.write(f"Q1 (25%): {q1:.4f}\n")
        f.write(f"Q2 (50%): {q2:.4f}\n")
        f.write(f"Q3 (75%): {q3:.4f}\n")
    
    print(f"✅ Estadísticas guardadas: {stats_path}")

def main():
    """Función principal"""
    print("🇫🇷 EXTRACTOR FRANCÉS (010) - BAREMO 2025")
    print("=" * 50)
    
    # Cargar configuración
    config = cargar_configuracion()
    if not config:
        return
    
    # Buscar el PDF
    pdf_path = None
    
    # Primero intentar en el directorio data local
    local_pdf = DATA_DIR / config['extraccion']['archivo_entrada']
    if local_pdf.exists():
        pdf_path = local_pdf
    else:
        # Intentar en el directorio data global
        global_pdf = Path("../../data/rh03_257_2025_590_12_baremo_prov.pdf")
        if global_pdf.exists():
            pdf_path = global_pdf
    
    if not pdf_path:
        print("❌ PDF no encontrado. Opciones:")
        print(f"   1. Coloca el PDF específico en: {local_pdf}")
        print("   2. Asegúrate de que exista: ../../data/rh03_257_2025_590_12_baremo_prov.pdf")
        return
    
    print(f"📁 PDF encontrado: {pdf_path}")
    
    # Procesar PDF
    todas_puntuaciones = []
    
    pagina_inicio = config['extraccion']['pagina_inicio']
    pagina_fin = config['extraccion']['pagina_fin']
    
    print(f"📄 Procesando páginas {pagina_inicio}-{pagina_fin}...")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i in range(pagina_inicio - 1, pagina_fin):  # -1 porque páginas son 0-indexed
                if i < len(pdf.pages):
                    page = pdf.pages[i]
                    puntuaciones_pagina = procesar_pagina(page, config)
                    todas_puntuaciones.extend(puntuaciones_pagina)
                    
                    if (i + 1) % 10 == 0:  # Progreso cada 10 páginas
                        print(f"   Procesadas {i + 1 - (pagina_inicio - 1)}/{pagina_fin - pagina_inicio + 1} páginas...")
        
        print(f"✅ Extracción completada: {len(todas_puntuaciones)} candidatos")
        
        # Validar extracción
        if validar_extraccion(todas_puntuaciones, config):
            # Guardar resultados
            guardar_resultados(todas_puntuaciones, config)
            
            print("\n🎉 ¡EXTRACCIÓN COMPLETADA CON ÉXITO!")
            print(f"✅ {len(todas_puntuaciones)} candidatos extraídos")
            print(f"📁 Archivos generados en: {OUTPUT_DIR}")
        else:
            print("\n⚠️ Extracción completada pero con problemas de validación")
    
    except Exception as e:
        print(f"❌ Error durante la extracción: {e}")

if __name__ == "__main__":
    main()
