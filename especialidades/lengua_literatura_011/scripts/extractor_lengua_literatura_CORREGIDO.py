#!/usr/bin/env python3
"""
Extractor de puntuaciones para Lengua Castellana y Literatura (011) - Baremo 2025
Procesa páginas 2-10 del PDF oficial del baremo provisional
"""

import sys
import os
import yaml
import pandas as pd
import pdfplumber
import re
from pathlib import Path

def cargar_configuracion():
    """Carga la configuración desde config.yaml"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def extraer_puntuaciones_pagina(page):
    """Extrae puntuaciones de una página usando múltiples métodos"""
    puntuaciones = []
    
    try:
        # Método 1: Extraer texto completo y buscar puntuaciones
        text = page.extract_text()
        if text:
            # Buscar todas las puntuaciones válidas con formato decimal
            matches = re.findall(r'\b\d+[,\.]\d{4}\b', text)
            for match in matches:
                try:
                    puntuacion = float(match.replace(',', '.'))
                    if 0.0 <= puntuacion <= 10.0:
                        puntuaciones.append(puntuacion)
                except ValueError:
                    continue
        
        # Método 2: Extraer tablas si existen
        if not puntuaciones:
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    for row in table:
                        if row and len(row) > 0:
                            # Buscar en todas las celdas
                            for cell in row:
                                if cell and isinstance(cell, str):
                                    matches = re.findall(r'\b\d+[,\.]\d{4}\b', cell)
                                    for match in matches:
                                        try:
                                            puntuacion = float(match.replace(',', '.'))
                                            if 0.0 <= puntuacion <= 10.0:
                                                puntuaciones.append(puntuacion)
                                        except ValueError:
                                            continue
                            
    except Exception as e:
        print(f"Error procesando página: {e}")
    
    return puntuaciones

def validar_pagina(puntuaciones_extraidas, puntuaciones_esperadas, numero_pagina):
    """Valida que las puntuaciones extraídas coincidan con las esperadas"""
    coincidencias = 0
    total_esperadas = len(puntuaciones_esperadas)
    
    print(f"\n=== VALIDACIÓN PÁGINA {numero_pagina} ===")
    print(f"Puntuaciones esperadas: {puntuaciones_esperadas}")
    print(f"Puntuaciones extraídas (primeras {len(puntuaciones_esperadas)}): {puntuaciones_extraidas[:len(puntuaciones_esperadas)]}")
    
    for i, esperada in enumerate(puntuaciones_esperadas):
        if i < len(puntuaciones_extraidas):
            extraida = puntuaciones_extraidas[i]
            if abs(extraida - esperada) < 0.0001:
                coincidencias += 1
                print(f"✓ Posición {i+1}: {extraida} == {esperada}")
            else:
                print(f"✗ Posición {i+1}: {extraida} != {esperada}")
        else:
            print(f"✗ Posición {i+1}: No encontrada")
    
    porcentaje = (coincidencias / total_esperadas) * 100
    print(f"Resultado: {coincidencias}/{total_esperadas} coincidencias ({porcentaje:.1f}%)")
    
    return porcentaje >= 50.0  # Consideramos válido si coincide al menos el 50%

def main():
    """Función principal de extracción"""
    print("🎭 EXTRACTOR LENGUA CASTELLANA Y LITERATURA (011) - BAREMO 2025")
    print("=" * 70)
    
    # Cargar configuración
    config = cargar_configuracion()
    
    # Configurar rutas
    pdf_path = Path(__file__).parent.parent / config['pdf']['archivo']
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    print(f"📄 PDF: {pdf_path}")
    print(f"📊 Páginas: {config['pdf']['pagina_inicio']}-{config['pdf']['pagina_fin']}")
    print(f"📁 Salida: {output_dir}")
    
    if not pdf_path.exists():
        print(f"❌ ERROR: No se encuentra el PDF en {pdf_path}")
        return False
    
    todas_puntuaciones = []
    paginas_procesadas = 0
    errores = 0
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"\n📖 Procesando PDF... Total páginas: {len(pdf.pages)}")
            
            for i in range(config['pdf']['pagina_inicio'] - 1, config['pdf']['pagina_fin']):
                if i >= len(pdf.pages):
                    print(f"⚠️ Página {i+1} fuera de rango")
                    break
                
                pagina_actual = i + 1
                puntuaciones_pagina = extraer_puntuaciones_pagina(pdf.pages[i])
                
                if puntuaciones_pagina:
                    todas_puntuaciones.extend(puntuaciones_pagina)
                    print(f"📄 Página {pagina_actual}: {len(puntuaciones_pagina)} puntuaciones")
                    
                    # Validar páginas clave
                    if pagina_actual == config['validacion']['pagina_inicial']['numero']:
                        validar_pagina(
                            puntuaciones_pagina,
                            config['validacion']['pagina_inicial']['puntuaciones_esperadas'],
                            pagina_actual
                        )
                    elif pagina_actual == config['validacion']['pagina_final']['numero']:
                        validar_pagina(
                            puntuaciones_pagina,
                            config['validacion']['pagina_final']['puntuaciones_esperadas'],
                            pagina_actual
                        )
                        
                    paginas_procesadas += 1
                else:
                    errores += 1
                    if errores <= 5:  # Solo mostrar los primeros 5 errores
                        print(f"❌ Página {pagina_actual}: Sin puntuaciones")
    
    except Exception as e:
        print(f"❌ ERROR procesando PDF: {e}")
        return False
    
    print(f"\n📊 RESUMEN DE EXTRACCIÓN")
    print("=" * 50)
    print(f"Total candidatos encontrados: {len(todas_puntuaciones)}")
    print(f"Páginas procesadas: {paginas_procesadas}")
    print(f"Páginas con errores: {errores}")
    
    if not todas_puntuaciones:
        print("❌ No se encontraron puntuaciones válidas")
        return False
    
    # Estadísticas básicas
    df = pd.DataFrame({'Total': todas_puntuaciones})
    print(f"\n📈 ESTADÍSTICAS")
    print("-" * 30)
    print(f"Puntuación máxima: {df['Total'].max():.4f}")
    print(f"Puntuación mínima: {df['Total'].min():.4f}")
    print(f"Puntuación media: {df['Total'].mean():.4f}")
    print(f"Desviación estándar: {df['Total'].std():.4f}")
    
    # Guardar resultados
    try:
        # CSV
        csv_path = output_dir / "puntuaciones_lengua_literatura_011.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"✅ CSV guardado: {csv_path}")
        
        # TXT (lista legible)
        txt_path = output_dir / "puntuaciones_lengua_literatura_011.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("# Puntuaciones Lengua Castellana y Literatura (011) - Baremo 2025\n")
            f.write(f"# Total candidatos: {len(todas_puntuaciones)}\n\n")
            for i, puntuacion in enumerate(todas_puntuaciones, 1):
                f.write(f"{i:4d}: {puntuacion:.4f}\n")
        print(f"✅ TXT guardado: {txt_path}")
        
        # Python array
        py_path = output_dir / "lista_lengua_literatura_011.py"
        with open(py_path, 'w', encoding='utf-8') as f:
            f.write("#!/usr/bin/env python3\n")
            f.write('"""\n')
            f.write("Puntuaciones de Lengua Castellana y Literatura (011) - Baremo 2025\n")
            f.write(f"Total candidatos: {len(todas_puntuaciones)}\n")
            f.write('"""\n\n')
            f.write("puntuaciones_lengua_literatura_011 = [\n")
            for puntuacion in todas_puntuaciones:
                f.write(f"    {puntuacion:.4f},\n")
            f.write("]\n")
        print(f"✅ Python guardado: {py_path}")
        
        # Estadísticas detalladas
        stats_path = output_dir / "estadisticas_lengua_literatura_011.txt"
        with open(stats_path, 'w', encoding='utf-8') as f:
            f.write("ESTADÍSTICAS LENGUA CASTELLANA Y LITERATURA (011) - BAREMO 2025\n")
            f.write("=" * 65 + "\n\n")
            f.write(f"Total candidatos: {len(todas_puntuaciones)}\n")
            f.write(f"Páginas procesadas: {config['pdf']['pagina_inicio']}-{config['pdf']['pagina_fin']}\n\n")
            f.write("ESTADÍSTICAS DESCRIPTIVAS:\n")
            f.write("-" * 30 + "\n")
            f.write(f"Puntuación máxima: {df['Total'].max():.4f}\n")
            f.write(f"Puntuación mínima: {df['Total'].min():.4f}\n")
            f.write(f"Puntuación media: {df['Total'].mean():.4f}\n")
            f.write(f"Mediana: {df['Total'].median():.4f}\n")
            f.write(f"Desviación estándar: {df['Total'].std():.4f}\n")
            f.write(f"Percentil 25: {df['Total'].quantile(0.25):.4f}\n")
            f.write(f"Percentil 75: {df['Total'].quantile(0.75):.4f}\n")
            
            # Distribución por rangos
            rangos = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10)]
            f.write(f"\nDISTRIBUCIÓN POR RANGOS:\n")
            f.write("-" * 25 + "\n")
            for inicio, fin in rangos:
                count = len(df[(df['Total'] >= inicio) & (df['Total'] < fin)])
                porcentaje = (count / len(df)) * 100
                f.write(f"{inicio}-{fin} puntos: {count} candidatos ({porcentaje:.1f}%)\n")
            
            # Último rango (incluye 10.0)
            count_10 = len(df[df['Total'] == 10.0])
            if count_10 > 0:
                porcentaje_10 = (count_10 / len(df)) * 100
                f.write(f"10.0 puntos exactos: {count_10} candidatos ({porcentaje_10:.1f}%)\n")
        
        print(f"✅ Estadísticas guardadas: {stats_path}")
        
    except Exception as e:
        print(f"❌ ERROR guardando archivos: {e}")
        return False
    
    print(f"\n🎉 EXTRACCIÓN COMPLETADA")
    print(f"✅ {len(todas_puntuaciones)} candidatos procesados correctamente")
    print(f"📁 Archivos generados en: {output_dir}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
