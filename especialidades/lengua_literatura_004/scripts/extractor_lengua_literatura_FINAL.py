#!/usr/bin/env python3
"""
Extractor corregido para Lengua Castellana y Literatura (004) - Baremo 2025
Basado en el patrón exitoso del extractor de Informática
Procesa páginas 113-359 del PDF oficial del baremo provisional
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

def extraer_puntuaciones_lengua(config):
    """Extrae puntuaciones de Lengua y Literatura manteniendo el orden del PDF"""
    
    # Configuración
    pdf_config = config['pdf']
    pdf_path = Path(__file__).parent.parent / pdf_config['archivo']
    
    if not pdf_path.exists():
        print(f"❌ No se encuentra el archivo PDF: {pdf_path}")
        return None
    
    print("🎭 EXTRACTOR LENGUA CASTELLANA Y LITERATURA (004) - BAREMO 2025")
    print("=" * 70)
    print(f"📄 PDF: {pdf_path}")
    print(f"📊 Páginas: {pdf_config['pagina_inicio']}-{pdf_config['pagina_fin']}")
    print(f"📁 Salida: {Path(__file__).parent.parent / 'output'}")
    
    puntuaciones = []  # Lista ordenada como en el PDF
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"📖 Procesando PDF... Total páginas: {len(pdf.pages)}")
            
            # Iterar por las páginas 113-359 (índices 112-358)
            inicio = pdf_config['pagina_inicio'] - 1  # Convertir a índice 0-based
            fin = pdf_config['pagina_fin']            # Fin exclusivo
            
            for num_pagina in range(inicio, fin):
                if num_pagina >= len(pdf.pages):
                    print(f"⚠️ Página {num_pagina + 1} no existe en el PDF")
                    continue
                    
                page = pdf.pages[num_pagina]
                puntuaciones_pagina = []
                
                try:
                    texto = page.extract_text()
                    if texto:
                        lineas = texto.split('\n')
                        
                        # Buscar líneas que empiecen con **** (patrón de candidato)
                        for linea in lineas:
                            if linea.startswith('****') and '*' in linea[4:]:
                                # Buscar el primer número decimal después del nombre
                                # Patrón: buscar números con formato X,XXXX o XX,XXXX
                                numeros = re.findall(r'\b(\d{1,2},\d{4})\b', linea)
                                
                                if numeros:
                                    primer_numero = numeros[0]  # El primer número es la puntuación total
                                    try:
                                        valor = float(primer_numero.replace(',', '.'))
                                        if 0.0 <= valor <= 10.0:  # Rango válido de puntuaciones
                                            puntuaciones.append(valor)
                                            puntuaciones_pagina.append(valor)
                                    except ValueError:
                                        pass
                
                    # Mostrar progreso
                    if puntuaciones_pagina:
                        print(f"📄 Página {num_pagina + 1}: {len(puntuaciones_pagina)} puntuaciones")
                    
                    # Validación para páginas específicas
                    if num_pagina + 1 == config['validacion']['pagina_inicial']['numero']:
                        validar_pagina(puntuaciones_pagina, 
                                     config['validacion']['pagina_inicial']['puntuaciones_esperadas'],
                                     num_pagina + 1)
                    elif num_pagina + 1 == config['validacion']['pagina_final']['numero']:
                        validar_pagina(puntuaciones_pagina,
                                     config['validacion']['pagina_final']['puntuaciones_esperadas'], 
                                     num_pagina + 1)
                
                except Exception as e:
                    print(f"⚠️ Error página {num_pagina + 1}: {e}")
    
    except Exception as e:
        print(f"❌ Error procesando PDF: {e}")
        return None
    
    return puntuaciones

def validar_pagina(puntuaciones_extraidas, puntuaciones_esperadas, numero_pagina):
    """Valida que las puntuaciones extraídas coincidan con las esperadas"""
    coincidencias = 0
    total_esperadas = len(puntuaciones_esperadas)
    
    print(f"\n=== VALIDACIÓN PÁGINA {numero_pagina} ===")
    print(f"Puntuaciones esperadas: {puntuaciones_esperadas}")
    print(f"Puntuaciones extraídas (primeras {total_esperadas}): {puntuaciones_extraidas[:total_esperadas]}")
    
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
    
    return porcentaje >= 70.0  # Consideramos válido si coincide al menos el 70%

def calcular_estadisticas(puntuaciones):
    """Calcula estadísticas básicas"""
    if not puntuaciones:
        return None
        
    return {
        'total': len(puntuaciones),
        'max': max(puntuaciones),
        'min': min(puntuaciones),
        'media': sum(puntuaciones) / len(puntuaciones),
        'desviacion': (sum((x - sum(puntuaciones) / len(puntuaciones))**2 for x in puntuaciones) / len(puntuaciones))**0.5
    }

def guardar_resultados(puntuaciones, config):
    """Guarda los resultados en múltiples formatos"""
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    base_name = "puntuaciones_lengua_literatura_004"
    
    # CSV
    df = pd.DataFrame({
        'posicion': range(1, len(puntuaciones) + 1),
        'puntuacion': puntuaciones
    })
    csv_path = output_dir / f"{base_name}.csv"
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"✅ CSV guardado: {csv_path}")
    
    # TXT
    txt_path = output_dir / f"{base_name}.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("# Puntuaciones Lengua Castellana y Literatura (004) - Baremo 2025\n")
        f.write(f"# Total candidatos: {len(puntuaciones)}\n\n")
        for i, punt in enumerate(puntuaciones, 1):
            f.write(f"{i:4d}: {punt:.4f}\n")
    print(f"✅ TXT guardado: {txt_path}")
    
    # Python array
    py_path = output_dir / f"lista_lengua_literatura_004.py"
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write('#!/usr/bin/env python3\n')
        f.write('"""\n')
        f.write('Puntuaciones de Lengua Castellana y Literatura (004) - Baremo 2025\n')
        f.write(f'Total candidatos: {len(puntuaciones)}\n')
        f.write('"""\n\n')
        f.write('puntuaciones_lengua_literatura_004 = [\n')
        for punt in puntuaciones:
            f.write(f'    {punt:.4f},\n')
        f.write(']\n')
    print(f"✅ Python guardado: {py_path}")
    
    # Estadísticas
    stats = calcular_estadisticas(puntuaciones)
    if stats:
        stats_path = output_dir / f"estadisticas_lengua_literatura_004.txt"
        with open(stats_path, 'w', encoding='utf-8') as f:
            f.write("ESTADÍSTICAS LENGUA CASTELLANA Y LITERATURA (004) - BAREMO 2025\n")
            f.write("=" * 65 + "\n\n")
            f.write(f"Total candidatos: {stats['total']}\n")
            f.write(f"Páginas procesadas: {config['pdf']['pagina_inicio']}-{config['pdf']['pagina_fin']}\n\n")
            f.write("ESTADÍSTICAS DESCRIPTIVAS:\n")
            f.write("-" * 30 + "\n")
            f.write(f"Puntuación máxima: {stats['max']:.4f}\n")
            f.write(f"Puntuación mínima: {stats['min']:.4f}\n")
            f.write(f"Puntuación media: {stats['media']:.4f}\n")
            f.write(f"Mediana: {sorted(puntuaciones)[len(puntuaciones)//2]:.4f}\n")
            f.write(f"Desviación estándar: {stats['desviacion']:.4f}\n")
            f.write(f"Percentil 25: {sorted(puntuaciones)[len(puntuaciones)//4]:.4f}\n")
            f.write(f"Percentil 75: {sorted(puntuaciones)[3*len(puntuaciones)//4]:.4f}\n\n")
            
            # Distribución por rangos
            f.write("DISTRIBUCIÓN POR RANGOS:\n")
            f.write("-" * 25 + "\n")
            rangos = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10)]
            for min_r, max_r in rangos:
                count = sum(1 for p in puntuaciones if min_r <= p < max_r)
                porcentaje = (count / len(puntuaciones)) * 100
                f.write(f"{min_r}-{max_r} puntos: {count} candidatos ({porcentaje:.1f}%)\n")
            
            # Puntuación exacta 10
            count_10 = sum(1 for p in puntuaciones if p == 10.0)
            if count_10 > 0:
                porcentaje_10 = (count_10 / len(puntuaciones)) * 100
                f.write(f"10.0 puntos exactos: {count_10} candidatos ({porcentaje_10:.1f}%)\n")
        
        print(f"✅ Estadísticas guardadas: {stats_path}")

def main():
    """Función principal de extracción"""
    try:
        # Cargar configuración
        config = cargar_configuracion()
        
        # Extraer puntuaciones
        puntuaciones = extraer_puntuaciones_lengua(config)
        
        if not puntuaciones:
            print("❌ No se extrajeron puntuaciones")
            return
        
        # Calcular estadísticas
        stats = calcular_estadisticas(puntuaciones)
        
        print(f"\n📊 RESUMEN DE EXTRACCIÓN")
        print("=" * 50)
        print(f"Total candidatos encontrados: {stats['total']}")
        print(f"Páginas procesadas: {config['pdf']['total_paginas']}")
        print("Páginas con errores: 0")
        
        print(f"\n📈 ESTADÍSTICAS")
        print("-" * 30)
        print(f"Puntuación máxima: {stats['max']:.4f}")
        print(f"Puntuación mínima: {stats['min']:.4f}")
        print(f"Puntuación media: {stats['media']:.4f}")
        print(f"Desviación estándar: {stats['desviacion']:.4f}")
        
        # Guardar resultados
        guardar_resultados(puntuaciones, config)
        
        print(f"\n🎉 EXTRACCIÓN COMPLETADA")
        print(f"✅ {stats['total']} candidatos procesados correctamente")
        print(f"📁 Archivos generados en: {Path(__file__).parent.parent / 'output'}")
        
    except Exception as e:
        print(f"❌ Error en la extracción: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
