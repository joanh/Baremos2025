#!/usr/bin/env python3
"""
Extractor de Baremos - Matemáticas 008
Extrae datos manteniendo el orden original del PDF

Páginas: 662-924 (262 páginas)
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

def procesar_pagina(page, config):
    """Procesa una página individual del PDF"""
    candidatos_pagina = []
    patrones = config['patrones']
    
    try:
        # Extraer texto de la página
        texto = page.extract_text()
        if not texto:
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
                    
    except Exception as e:
        print(f"⚠️ Error procesando página: {e}")
    
    return candidatos_pagina

def main():
    """Función principal"""
    print("🔧 Iniciando extractor de Matemáticas 008...")
    
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
    
    # Crear directorio de salida si no existe
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Procesar PDF
    candidatos_totales = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_paginas = pdf_config['pagina_fin'] - pdf_config['pagina_inicio'] + 1
            print(f"📖 Procesando {total_paginas} páginas...")
            
            for num_pagina in range(pdf_config['pagina_inicio'], pdf_config['pagina_fin'] + 1):
                try:
                    # Índice de página (0-based)
                    page_index = num_pagina - 1
                    
                    if page_index < len(pdf.pages):
                        page = pdf.pages[page_index]
                        candidatos_pagina = procesar_pagina(page, config)
                        candidatos_totales.extend(candidatos_pagina)
                        
                        if candidatos_pagina:
                            print(f"✅ Página {num_pagina}: {len(candidatos_pagina)} candidatos")
                        else:
                            print(f"⚠️ Página {num_pagina}: Sin candidatos")
                    
                except Exception as e:
                    print(f"❌ Error en página {num_pagina}: {e}")
                    continue
                
    except Exception as e:
        print(f"❌ Error abriendo PDF: {e}")
        sys.exit(1)
    
    # Procesar resultados
    if not candidatos_totales:
        print("❌ No se encontraron candidatos")
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
    
    # 2. TXT
    txt_path = OUTPUT_DIR / output_config['txt']
    with open(txt_path, 'w', encoding='utf-8') as f:
        for i, candidato in enumerate(candidatos_totales, 1):
            f.write(f"{i}. {candidato['puntuacion']:.4f} - {candidato['linea']}\n")
    print(f"💾 TXT guardado: {txt_path.name}")
    
    # 3. Lista Python
    lista_path = OUTPUT_DIR / output_config['lista']
    with open(lista_path, 'w', encoding='utf-8') as f:
        f.write("# Puntuaciones de Matemáticas (008) - Baremo 2025\n")
        f.write("# Extraídas en orden original del PDF\n")
        f.write("# Páginas 662-924\n\n")
        f.write(f"{output_config['variable_lista']} = [\n")
        for puntuacion in puntuaciones:
            f.write(f"    {puntuacion:.4f},\n")
        f.write("]\n")
    print(f"💾 Lista Python guardada: {lista_path.name}")
    
    # 4. Estadísticas
    stats_path = OUTPUT_DIR / output_config['estadisticas']
    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write(f"=== ESTADÍSTICAS MATEMÁTICAS (008) - 2025 ===\n")
        f.write(f"Total candidatos: {len(candidatos_totales)}\n")
        f.write(f"Puntuación máxima: {max(puntuaciones):.4f}\n")
        f.write(f"Puntuación mínima: {min(puntuaciones):.4f}\n")
        f.write(f"Puntuación media: {sum(puntuaciones)/len(puntuaciones):.4f}\n")
        f.write(f"Páginas procesadas: {pdf_config['pagina_inicio']}-{pdf_config['pagina_fin']}\n")
        f.write(f"Extraído por: @joanh\n")
    print(f"💾 Estadísticas guardadas: {stats_path.name}")
    
    print(f"\n✅ Todos los archivos guardados en: {OUTPUT_DIR}")
    print(f"🔄 Siguiente paso: python visualizador_matematicas.py")

if __name__ == "__main__":
    main()
