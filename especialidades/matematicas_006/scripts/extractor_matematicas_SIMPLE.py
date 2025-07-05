#!/usr/bin/env python3
"""
Extractor de Baremos - Matemáticas 006 (VERSIÓN SIMPLE)
Basado en el extractor exitoso de Informática

Páginas: 662-924
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

def procesar_linea(linea):
    """
    Procesa una línea para extraer puntuación
    Busca números decimales al final de la línea (columna Total)
    """
    linea = linea.strip()
    if not linea:
        return None
    
    # Buscar número decimal al final de la línea (formato X.XXXX o X,XXXX)
    patron = r'(\d+[,.]\d{1,4})\s*$'
    match = re.search(patron, linea)
    
    if match:
        puntuacion_str = match.group(1)
        # Convertir coma a punto
        puntuacion_str = puntuacion_str.replace(',', '.')
        try:
            puntuacion = float(puntuacion_str)
            # Validar rango razonable (0-10)
            if 0 <= puntuacion <= 10:
                return puntuacion
        except ValueError:
            pass
    
    return None

def main():
    """Función principal"""
    print("🔧 Iniciando extractor SIMPLE de Matemáticas 006...")
    
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
        sys.exit(1)
    
    # Crear directorio de salida
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Procesar PDF
    puntuaciones = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_paginas = pdf_config['pagina_fin'] - pdf_config['pagina_inicio'] + 1
            print(f"📖 Procesando {total_paginas} páginas...")
            
            # Procesar cada página
            for num_pagina in range(pdf_config['pagina_inicio'], pdf_config['pagina_fin'] + 1):
                try:
                    # Índice de página (0-based)
                    page_index = num_pagina - 1
                    
                    if page_index < len(pdf.pages):
                        page = pdf.pages[page_index]
                        texto = page.extract_text()
                        
                        if texto:
                            puntuaciones_pagina = 0
                            lineas = texto.split('\n')
                            
                            for linea in lineas:
                                puntuacion = procesar_linea(linea)
                                if puntuacion is not None:
                                    puntuaciones.append(puntuacion)
                                    puntuaciones_pagina += 1
                            
                            if puntuaciones_pagina > 0:
                                print(f"✅ Página {num_pagina}: {puntuaciones_pagina} candidatos")
                            
                            # Mostrar progreso cada 50 páginas
                            if (num_pagina - pdf_config['pagina_inicio']) % 50 == 0:
                                print(f"📊 Progreso: {len(puntuaciones)} candidatos extraídos hasta página {num_pagina}")
                                
                except Exception as e:
                    print(f"❌ Error en página {num_pagina}: {e}")
                    continue
                    
    except Exception as e:
        print(f"❌ Error abriendo PDF: {e}")
        sys.exit(1)
    
    # Verificar resultados
    if not puntuaciones:
        print("❌ No se encontraron candidatos")
        sys.exit(1)
    
    print(f"\n🎉 EXTRACCIÓN COMPLETADA")
    print(f"📊 Total candidatos: {len(puntuaciones)}")
    print(f"🏆 Puntuación máxima: {max(puntuaciones):.4f}")
    print(f"📉 Puntuación mínima: {min(puntuaciones):.4f}")
    print(f"📈 Puntuación media: {sum(puntuaciones)/len(puntuaciones):.4f}")
    
    # Guardar resultados
    output_config = config['output']
    
    # 1. CSV
    df = pd.DataFrame({
        'Orden': range(1, len(puntuaciones) + 1),
        'Puntuacion_Total': puntuaciones
    })
    csv_path = OUTPUT_DIR / output_config['csv']
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"💾 CSV guardado: {csv_path.name}")
    
    # 2. TXT
    txt_path = OUTPUT_DIR / output_config['txt']
    with open(txt_path, 'w', encoding='utf-8') as f:
        for i, puntuacion in enumerate(puntuaciones, 1):
            f.write(f"{i}. {puntuacion:.4f}\n")
    print(f"💾 TXT guardado: {txt_path.name}")
    
    # 3. Lista Python
    lista_path = OUTPUT_DIR / output_config['lista']
    with open(lista_path, 'w', encoding='utf-8') as f:
        f.write("# Puntuaciones de Matemáticas (006) - Baremo 2025\n")
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
        f.write(f"=== ESTADÍSTICAS MATEMÁTICAS (006) - 2025 ===\n")
        f.write(f"Total candidatos: {len(puntuaciones)}\n")
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
