#!/usr/bin/env python3
"""
Extractor de Baremos - Física y Química 010
Basado en el extractor exitoso de Matemáticas

Páginas: 925-1062
Autor: @joanh
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

def extraer_puntuacion_total(linea):
    """
    Extrae la puntuación total de una línea de candidato
    MÉTODO EXACTO del extractor exitoso de Matemáticas
    """
    # Patrón: ****XXXX* APELLIDOS, NOMBRE [SEGUNDO_NOMBRE] PUNTUACION
    patron = r'\*{4}\d{4}\*\s+([A-ZÁÉÍÓÚÑÜ\s,]+?)\s+(\d+[,\.]\d{4})'
    
    match = re.search(patron, linea)
    if match:
        puntuacion_str = match.group(2).replace(',', '.')
        try:
            puntuacion = float(puntuacion_str)
            # Validar rango (0-10 puntos)
            if 0.0 <= puntuacion <= 10.0:
                return puntuacion
        except ValueError:
            pass
    
    return None

def es_linea_candidato(linea):
    """
    Verifica si una línea contiene datos de un candidato
    MÉTODO EXACTO del extractor exitoso de Matemáticas
    """
    # Patrón: ****XXXX* seguido de nombre y puntuación
    patron = r'\*{4}\d{4}\*\s+[A-ZÁÉÍÓÚÑÜ\s,]+\s+\d+[,\.]\d{4}'
    return bool(re.search(patron, linea))

def validar_extraccion(candidatos_validos, config):
    """Valida la extracción contra las puntuaciones de referencia"""
    validacion = config.get('validacion', {})
    
    if 'pagina_inicio' in validacion:
        ref_inicio = validacion['pagina_inicio']
        candidatos_p925 = [c for c in candidatos_validos if c['pagina'] == ref_inicio['pagina']]
        puntuaciones_p925 = [c['puntuacion'] for c in candidatos_p925]
        
        print(f"🔍 Validación página {ref_inicio['pagina']}:")
        print(f"   Esperadas: {ref_inicio['puntuaciones_esperadas']}")
        print(f"   Extraídas: {puntuaciones_p925}")
        
        if len(puntuaciones_p925) == len(ref_inicio['puntuaciones_esperadas']):
            coincidencias = sum(1 for e, r in zip(puntuaciones_p925, ref_inicio['puntuaciones_esperadas']) 
                              if abs(e - r) < 0.001)
            print(f"   ✅ Coincidencias: {coincidencias}/{len(ref_inicio['puntuaciones_esperadas'])}")
        else:
            print(f"   ⚠️ Cantidad diferente: {len(puntuaciones_p925)} vs {len(ref_inicio['puntuaciones_esperadas'])}")
    
    if 'pagina_fin' in validacion:
        ref_fin = validacion['pagina_fin']
        candidatos_p1062 = [c for c in candidatos_validos if c['pagina'] == ref_fin['pagina']]
        puntuaciones_p1062 = [c['puntuacion'] for c in candidatos_p1062]
        
        print(f"🔍 Validación página {ref_fin['pagina']}:")
        print(f"   Esperadas: {ref_fin['puntuaciones_esperadas']}")
        print(f"   Extraídas: {puntuaciones_p1062}")
        
        if len(puntuaciones_p1062) == len(ref_fin['puntuaciones_esperadas']):
            coincidencias = sum(1 for e, r in zip(puntuaciones_p1062, ref_fin['puntuaciones_esperadas']) 
                              if abs(e - r) < 0.001)
            print(f"   ✅ Coincidencias: {coincidencias}/{len(ref_fin['puntuaciones_esperadas'])}")
        else:
            print(f"   ⚠️ Cantidad diferente: {len(puntuaciones_p1062)} vs {len(ref_fin['puntuaciones_esperadas'])}")

def main():
    """Función principal"""
    print("🔧 Iniciando extractor de Física y Química 010...")
    
    # Cargar configuración
    config = cargar_configuracion()
    esp_config = config['especialidad']
    pdf_config = config['pdf']
    
    print(f"📚 Especialidad: {esp_config['nombre_completo']}")
    print(f"📄 Páginas: {pdf_config['pagina_inicio']}-{pdf_config['pagina_fin']}")
    
    # Verificar archivo PDF
    pdf_path = DATA_DIR / pdf_config['archivo_entrada']
    if not pdf_path.exists():
        print(f"❌ PDF no encontrado: {pdf_path}")
        print(f"💡 Copia el PDF del proyecto principal:")
        print(f"   copy ..\\..\\data\\rh03_257_2025_590_12_baremo_prov.pdf {pdf_path}")
        sys.exit(1)
    
    # Crear directorio de salida
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Procesar PDF
    candidatos_validos = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_paginas = pdf_config['pagina_fin'] - pdf_config['pagina_inicio'] + 1
            print(f"📖 Procesando {total_paginas} páginas...")
            
            for num_pagina in range(pdf_config['pagina_inicio'], pdf_config['pagina_fin'] + 1):
                try:
                    page_index = num_pagina - 1
                    
                    if page_index < len(pdf.pages):
                        page = pdf.pages[page_index]
                        texto = page.extract_text()
                        
                        if texto:
                            # Limpiar caracteres problemáticos
                            for char in ['€', '‚', 'Ç', '§']:
                                texto = texto.replace(char, '')
                            
                            # Procesar líneas
                            lineas = texto.split('\n')
                            candidatos_pagina = 0
                            
                            for linea in lineas:
                                linea = linea.strip()
                                if not linea:
                                    continue
                                
                                # Verificar si es línea de candidato
                                if es_linea_candidato(linea):
                                    puntuacion = extraer_puntuacion_total(linea)
                                    
                                    if puntuacion is not None:
                                        candidatos_validos.append({
                                            'linea': linea,
                                            'puntuacion': puntuacion,
                                            'pagina': num_pagina
                                        })
                                        candidatos_pagina += 1
                            
                            # Mostrar progreso cada 20 páginas
                            if num_pagina % 20 == 0 or candidatos_pagina > 0:
                                print(f"✅ Página {num_pagina}: {candidatos_pagina} candidatos")
                                
                except Exception as e:
                    print(f"❌ Error en página {num_pagina}: {e}")
                    continue
                
    except Exception as e:
        print(f"❌ Error abriendo PDF: {e}")
        sys.exit(1)
    
    # Verificar resultados
    if not candidatos_validos:
        print("❌ No se encontraron candidatos válidos")
        sys.exit(1)
    
    print(f"\n🎉 EXTRACCIÓN COMPLETADA")
    print(f"📊 Total candidatos: {len(candidatos_validos)}")
    
    # Validar extracción
    validar_extraccion(candidatos_validos, config)
    
    # Extraer puntuaciones
    puntuaciones = [c['puntuacion'] for c in candidatos_validos]
    
    # Mostrar estadísticas
    print(f"\n📈 ESTADÍSTICAS:")
    print(f"🏆 Puntuación máxima: {max(puntuaciones):.4f}")
    print(f"📉 Puntuación mínima: {min(puntuaciones):.4f}")
    print(f"📈 Puntuación media: {sum(puntuaciones)/len(puntuaciones):.4f}")
    
    # Guardar resultados
    output_config = config['output']
    
    # CSV
    df = pd.DataFrame({
        'Orden': range(1, len(candidatos_validos) + 1),
        'Linea_Completa': [c['linea'] for c in candidatos_validos],
        'Puntuacion_Total': puntuaciones,
        'Pagina': [c['pagina'] for c in candidatos_validos]
    })
    csv_path = OUTPUT_DIR / output_config['csv']
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"💾 CSV guardado: {csv_path.name}")
    
    # TXT
    txt_path = OUTPUT_DIR / output_config['txt']
    with open(txt_path, 'w', encoding='utf-8') as f:
        for i, candidato in enumerate(candidatos_validos, 1):
            f.write(f"{i}. {candidato['puntuacion']:.4f} - {candidato['linea']}\n")
    print(f"💾 TXT guardado: {txt_path.name}")
    
    # Lista Python
    lista_path = OUTPUT_DIR / output_config['lista']
    with open(lista_path, 'w', encoding='utf-8') as f:
        f.write("# Puntuaciones de Física y Química (010) - Baremo 2025\n")
        f.write("# Extraídas en orden original del PDF\n")
        f.write("# Páginas 925-1062\n\n")
        f.write(f"{output_config['variable_lista']} = [\n")
        for puntuacion in puntuaciones:
            f.write(f"    {puntuacion:.4f},\n")
        f.write("]\n")
    print(f"💾 Lista Python guardada: {lista_path.name}")
    
    # Estadísticas
    stats_path = OUTPUT_DIR / output_config['estadisticas']
    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write(f"=== ESTADÍSTICAS FÍSICA Y QUÍMICA (010) - 2025 ===\n")
        f.write(f"Total candidatos: {len(candidatos_validos)}\n")
        f.write(f"Puntuación máxima: {max(puntuaciones):.4f}\n")
        f.write(f"Puntuación mínima: {min(puntuaciones):.4f}\n")
        f.write(f"Puntuación media: {sum(puntuaciones)/len(puntuaciones):.4f}\n")
        f.write(f"Páginas procesadas: {pdf_config['pagina_inicio']}-{pdf_config['pagina_fin']}\n")
        f.write(f"Candidatos por página (aprox): {len(candidatos_validos)/(pdf_config['pagina_fin']-pdf_config['pagina_inicio']+1):.1f}\n")
        f.write(f"Extraído por: @joanh\n")
    print(f"💾 Estadísticas guardadas: {stats_path.name}")
    
    print(f"\n✅ Todos los archivos guardados en: {OUTPUT_DIR}")
    print(f"🔄 Siguiente paso: python visualizador_fisica_quimica.py")

if __name__ == "__main__":
    main()
