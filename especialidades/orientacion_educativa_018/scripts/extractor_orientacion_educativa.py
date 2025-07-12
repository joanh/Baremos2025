#!/usr/bin/env python3
"""
Extractor Orientación Educativa (018) - Baremo 2025
Procesa páginas 2032-2268 del PDF oficial
"""

import pdfplumber
import re
import os
import yaml

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
    
    puntuaciones = []
    caracteres_limpiar = config['patrones']['caracteres_limpiar']
    total_paginas = pagina_final - pagina_inicio + 1
    
    print(f"📄 Procesando páginas {pagina_inicio}-{pagina_final}...")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, num_pagina in enumerate(range(pagina_inicio, pagina_final + 1)):
                if i % 20 == 0:
                    print(f"   Procesadas {i}/{total_paginas} páginas...")
                
                if num_pagina <= len(pdf.pages):
                    pagina = pdf.pages[num_pagina - 1]
                    texto = pagina.extract_text() or ""
                    
                    # Limpiar caracteres problemáticos
                    for char in caracteres_limpiar:
                        texto = texto.replace(char, "")
                    
                    # Buscar líneas de candidatos de ORIENTACION EDUCATIVA específicamente
                    lineas = texto.split('\n')
                    for linea in lineas:
                        # Buscar líneas que contengan un DNI enmascarado (****) seguido de un nombre y puntuación
                        if '****' in linea and ',' in linea:
                            # Extraer la primera puntuación decimal después del nombre
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
    
    # Validar primeras puntuaciones
    validacion_inicial = config['extraccion']['validacion_inicial']
    coincidencias_inicial = 0
    for i, valor_esperado in enumerate(validacion_inicial):
        if i < len(puntuaciones) and abs(puntuaciones[i] - valor_esperado) < 0.001:
            coincidencias_inicial += 1
    
    print(f"✅ Validación página inicial: {coincidencias_inicial}/{len(validacion_inicial)} coincidencias")
    
    # Validar últimas puntuaciones
    validacion_final = config['extraccion']['validacion_final']
    coincidencias_final = 0
    puntuaciones_finales = puntuaciones[-len(validacion_final):]
    for i, valor_esperado in enumerate(validacion_final):
        if i < len(puntuaciones_finales) and abs(puntuaciones_finales[i] - valor_esperado) < 0.001:
            coincidencias_final += 1
    
    print(f"✅ Validación página final: {coincidencias_final}/{len(validacion_final)} coincidencias")
    
    return coincidencias_inicial, coincidencias_final

def guardar_resultados(puntuaciones, config):
    """Guarda los resultados en múltiples formatos"""
    print("💾 GUARDANDO RESULTADOS...")
    
    output_dir = "../output"
    
    # 1. CSV
    csv_path = os.path.join(output_dir, config['output']['csv'])
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("candidato,puntuacion\n")
        for i, puntuacion in enumerate(puntuaciones, 1):
            f.write(f"{i},{puntuacion}\n")
    print(f"✅ CSV guardado: {os.path.abspath(csv_path)}")
    
    # 2. TXT
    txt_path = os.path.join(output_dir, config['output']['txt'])
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("=== PUNTUACIONES ORIENTACIÓN EDUCATIVA (018) - 2025 ===\n\n")
        for i, puntuacion in enumerate(puntuaciones, 1):
            f.write(f"Candidato {i:4d}: {puntuacion:7.4f}\n")
    print(f"✅ TXT guardado: {os.path.abspath(txt_path)}")
    
    # 3. Python list
    python_path = os.path.join(output_dir, config['output']['python'])
    with open(python_path, 'w', encoding='utf-8') as f:
        f.write("#!/usr/bin/env python3\n")
        f.write('"""\nPuntuaciones Orientación Educativa (018) - Baremo 2025\n"""\n\n')
        f.write("puntuaciones_orientacion_educativa_018 = [\n")
        for i, puntuacion in enumerate(puntuaciones):
            if i % 10 == 0:
                f.write("    ")
            f.write(f"{puntuacion:7.4f}")
            if i < len(puntuaciones) - 1:
                f.write(", ")
            if (i + 1) % 10 == 0:
                f.write("\n")
        if len(puntuaciones) % 10 != 0:
            f.write("\n")
        f.write("]\n")
    print(f"✅ Python guardado: {os.path.abspath(python_path)}")
    
    # 4. Estadísticas
    import numpy as np
    
    estadisticas_path = os.path.join(output_dir, config['output']['estadisticas'])
    with open(estadisticas_path, 'w', encoding='utf-8') as f:
        f.write("=== ESTADÍSTICAS ORIENTACIÓN EDUCATIVA (018) - 2025 ===\n\n")
        f.write(f"Total candidatos: {len(puntuaciones)}\n")
        f.write(f"Media: {np.mean(puntuaciones):.4f}\n")
        f.write(f"Mediana: {np.median(puntuaciones):.4f}\n")
        f.write(f"Desviación estándar: {np.std(puntuaciones):.4f}\n")
        f.write(f"Mínimo: {np.min(puntuaciones):.4f}\n")
        f.write(f"Máximo: {np.max(puntuaciones):.4f}\n")
        f.write(f"Rango: {np.max(puntuaciones) - np.min(puntuaciones):.4f}\n\n")
        f.write("CUARTILES:\n")
        f.write(f"Q1 (25%): {np.percentile(puntuaciones, 25):.4f}\n")
        f.write(f"Q2 (50%): {np.percentile(puntuaciones, 50):.4f}\n")
        f.write(f"Q3 (75%): {np.percentile(puntuaciones, 75):.4f}\n")
    print(f"✅ Estadísticas guardadas: {os.path.abspath(estadisticas_path)}")

def main():
    print("⚙️ EXTRACTOR ORIENTACIÓN EDUCATIVA (018) - BAREMO 2025")
    print("=" * 50)
    
    # Cargar configuración
    config = cargar_configuracion()
    if config is None:
        return
    
    # Extraer puntuaciones
    puntuaciones = extraer_puntuaciones(config)
    if puntuaciones is None:
        return
    
    # Validar extracción
    validar_extraccion(puntuaciones, config)
    
    # Guardar resultados
    guardar_resultados(puntuaciones, config)
    
    print("🎉 ¡EXTRACCIÓN COMPLETADA CON ÉXITO!")
    print(f"✅ {len(puntuaciones)} candidatos extraídos")
    print(f"📁 Archivos generados en: {os.path.abspath('../output')}")

if __name__ == "__main__":
    main()
