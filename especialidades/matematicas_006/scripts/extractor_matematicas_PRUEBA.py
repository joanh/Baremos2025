#!/usr/bin/env python3
"""
Extractor de Baremos - Matemáticas 006 (VERSIÓN PRUEBA)
Extrae datos manteniendo el orden original del PDF

Páginas: 662-680 (18 páginas para prueba)
Autor: @joanh
Asistente: Claude Sonnet 4.0
"""

import os
import sys
import re
import yaml
import pdfplumber
import pandas as pd
from pathlib import Path
import time

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

def limpiar_texto(texto, caracteres_limpiar):
    """Limpia caracteres problemáticos del texto"""
    for char in caracteres_limpiar:
        texto = texto.replace(char, '')
    return texto.strip()

def extraer_puntuacion(linea, patron_puntuacion):
    """Extrae la puntuación total de una línea"""
    # Buscar números con coma o punto decimal al final de la línea
    matches = re.findall(patron_puntuacion, linea)
    if matches:
        # Tomar la última coincidencia (puntuación total)
        puntuacion_str = matches[-1]
        # Convertir coma a punto para formato float
        puntuacion_str = puntuacion_str.replace(',', '.')
        try:
            return float(puntuacion_str)
        except ValueError:
            return None
    return None

def procesar_pagina(page, config, num_pagina):
    """Procesa una página individual del PDF"""
    candidatos_pagina = []
    patrones = config['patrones']
    
    print(f"  📄 Procesando página {num_pagina}...", end=' ', flush=True)
    start_time = time.time()
    
    try:
        # Extraer texto de la página
        texto = page.extract_text()
        if not texto:
            print("(sin texto)")
            return candidatos_pagina
        
        # Limpiar caracteres problemáticos
        texto = limpiar_texto(texto, patrones['caracteres_limpiar'])
        
        # Dividir en líneas
        lineas = texto.split('\n')
        
        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue
            
            # Verificar si es una línea de candidato
            if re.search(patrones['linea_candidato'], linea):
                # Extraer puntuación total
                puntuacion = extraer_puntuacion(linea, patrones['puntuacion_total'])
                
                if puntuacion is not None:
                    candidatos_pagina.append({
                        'linea': linea,
                        'puntuacion': puntuacion
                    })
        
        elapsed = time.time() - start_time
        print(f"✅ {len(candidatos_pagina)} candidatos ({elapsed:.1f}s)")
                    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return candidatos_pagina

def main():
    """Función principal"""
    print("🔧 Iniciando extractor PRUEBA de Matemáticas 006...")
    
    # Cargar configuración
    config = cargar_configuracion()
    esp_config = config['especialidad']
    pdf_config = config['pdf']
    
    print(f"📚 Especialidad: {esp_config['nombre_completo']}")
    print(f"🔢 Código: {esp_config['codigo']}")
    print(f"📄 Páginas: {pdf_config['pagina_inicio']}-{pdf_config['pagina_fin']}")
    
    # Verificar archivo PDF
    pdf_path = DATA_DIR / pdf_config['archivo_entrada']
    if not pdf_path.exists():
        print(f"❌ PDF no encontrado: {pdf_path}")
        print(f"💡 Copia el PDF principal a: {pdf_path}")
        sys.exit(1)
    
    print(f"📁 PDF encontrado: {pdf_path.name}")
    
    # Crear directorio de salida si no existe
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Procesar PDF
    candidatos_totales = []
    
    try:
        print("📖 Abriendo PDF...")
        with pdfplumber.open(pdf_path) as pdf:
            total_paginas = pdf_config['pagina_fin'] - pdf_config['pagina_inicio'] + 1
            print(f"📊 Procesando {total_paginas} páginas (modo PRUEBA)...")
            
            for num_pagina in range(pdf_config['pagina_inicio'], pdf_config['pagina_fin'] + 1):
                try:
                    # Índice de página (0-based)
                    page_index = num_pagina - 1
                    
                    if page_index < len(pdf.pages):
                        page = pdf.pages[page_index]
                        candidatos_pagina = procesar_pagina(page, config, num_pagina)
                        candidatos_totales.extend(candidatos_pagina)
                    else:
                        print(f"⚠️ Página {num_pagina}: Fuera de rango")
                    
                except Exception as e:
                    print(f"❌ Error en página {num_pagina}: {e}")
                    continue
                
    except Exception as e:
        print(f"❌ Error abriendo PDF: {e}")
        sys.exit(1)
    
    # Procesar resultados
    if not candidatos_totales:
        print("❌ No se encontraron candidatos")
        print("💡 Verifica que las páginas contengan datos de Matemáticas")
        sys.exit(1)
    
    print(f"\n🎉 EXTRACCIÓN COMPLETADA")
    print(f"📊 Total candidatos encontrados: {len(candidatos_totales)}")
    
    # Extraer solo las puntuaciones para análisis
    puntuaciones = [c['puntuacion'] for c in candidatos_totales]
    
    # Mostrar estadísticas básicas
    print(f"🏆 Puntuación máxima: {max(puntuaciones):.4f}")
    print(f"📉 Puntuación mínima: {min(puntuaciones):.4f}")
    print(f"📈 Puntuación media: {sum(puntuaciones)/len(puntuaciones):.4f}")
    
    # Guardar resultados
    output_config = config['output']
    
    # 1. CSV
    df = pd.DataFrame({
        'Orden': range(1, len(candidatos_totales) + 1),
        'Linea_Completa': [c['linea'] for c in candidatos_totales],
        'Puntuacion_Total': puntuaciones
    })
    csv_path = OUTPUT_DIR / output_config['csv']
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"💾 CSV guardado: {csv_path.name}")
    
    # 2. Lista Python
    lista_path = OUTPUT_DIR / output_config['lista']
    with open(lista_path, 'w', encoding='utf-8') as f:
        f.write("# Puntuaciones de Matemáticas (006) - Baremo 2025\n")
        f.write("# Extraídas en orden original del PDF\n")
        f.write(f"# Páginas {pdf_config['pagina_inicio']}-{pdf_config['pagina_fin']} (PRUEBA)\n\n")
        f.write(f"{output_config['variable_lista']} = [\n")
        for puntuacion in puntuaciones:
            f.write(f"    {puntuacion:.4f},\n")
        f.write("]\n")
    print(f"💾 Lista Python guardada: {lista_path.name}")
    
    print(f"\n✅ Archivos guardados en: {OUTPUT_DIR}")
    print(f"🔄 Siguiente paso: python visualizador_matematicas.py")
    print(f"\n💡 NOTA: Esta es una extracción de PRUEBA de {total_paginas} páginas.")
    print(f"💡 Para extraer todas las páginas (662-924), cambia pagina_fin a 924 en config.yaml")

if __name__ == "__main__":
    main()
