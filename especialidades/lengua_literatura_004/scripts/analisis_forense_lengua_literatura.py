#!/usr/bin/env python3
"""
Análisis forense para encontrar las páginas de Lengua Castellana y Literatura (011)
Busca patrones específicos en el PDF para identificar dónde están los datos
Autor: @joanh con Claude Sonnet 4.0
"""

import pdfplumber
import re
import sys
from typing import List, Tuple

def buscar_lengua_literatura(pdf_path: str) -> List[Tuple[int, str]]:
    """Buscar páginas que contengan datos de Lengua Castellana y Literatura."""
    patrones_busqueda = [
        r"LENGUA.*CASTELLANA.*LITERATURA",
        r"CASTELLANA.*LITERATURA", 
        r"LENGUA.*LITERATURA",
        r"011",  # Código de especialidad
        r"ESPECIALIDAD.*011",
        r"3[.,]5000",  # Puntuaciones de validación
        r"8[.,]5000",
        r"6[.,]4084",
        r"0[.,]4792"
    ]
    
    resultados = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"📄 Analizando PDF: {len(pdf.pages)} páginas totales")
            print("🔍 Buscando LENGUA CASTELLANA Y LITERATURA...")
            print("="*60)
            
            # Buscar en todas las páginas
            for i, page in enumerate(pdf.pages):
                try:
                    texto = page.extract_text()
                    if not texto:
                        continue
                    
                    # Verificar cada patrón
                    coincidencias = []
                    for patron in patrones_busqueda:
                        matches = re.findall(patron, texto, re.IGNORECASE)
                        if matches:
                            coincidencias.extend(matches)
                    
                    if coincidencias:
                        print(f"🎯 Página {i+1}: {len(coincidencias)} coincidencias")
                        
                        # Mostrar contexto de las coincidencias
                        lineas = texto.split('\n')
                        for j, linea in enumerate(lineas):
                            for patron in patrones_busqueda:
                                if re.search(patron, linea, re.IGNORECASE):
                                    print(f"   Línea {j}: {linea.strip()[:100]}...")
                                    break
                        
                        resultados.append((i+1, texto))
                        print("-" * 40)
                        
                        # Mostrar las primeras puntuaciones encontradas
                        puntuaciones = re.findall(r'\b\d+[.,]\d{4}\b', texto)
                        if puntuaciones:
                            print(f"   Puntuaciones encontradas: {puntuaciones[:10]}...")
                        print()
                        
                        # Si encontramos más de 5 páginas consecutivas, probablemente está bien
                        if len(resultados) > 5:
                            print(f"✅ Encontradas {len(resultados)} páginas consecutivas. Parece correcto.")
                            break
                            
                except Exception as e:
                    print(f"⚠️ Error en página {i+1}: {e}")
                    continue
                    
    except Exception as e:
        print(f"❌ Error abriendo PDF: {e}")
        return []
    
    return resultados

def analizar_rango_paginas(pdf_path: str, inicio: int, fin: int):
    """Analizar un rango específico de páginas."""
    print(f"\n🔍 ANÁLISIS DETALLADO - Páginas {inicio}-{fin}")
    print("="*50)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for num_pagina in range(inicio-1, min(fin, len(pdf.pages))):
                try:
                    page = pdf.pages[num_pagina]
                    texto = page.extract_text()
                    
                    if texto:
                        # Buscar puntuaciones
                        puntuaciones = re.findall(r'\b\d+[.,]\d{4}\b', texto)
                        
                        # Buscar menciones de especialidad
                        menciones_lengua = re.findall(r'LENGUA.*|CASTELLANA.*|LITERATURA.*', texto, re.IGNORECASE)
                        
                        if puntuaciones or menciones_lengua:
                            print(f"\n📄 Página {num_pagina + 1}:")
                            
                            if menciones_lengua:
                                print(f"   📚 Menciones: {menciones_lengua[:3]}...")
                            
                            if puntuaciones:
                                print(f"   🔢 Puntuaciones: {len(puntuaciones)} encontradas")
                                print(f"   🎯 Primeras 5: {puntuaciones[:5]}")
                                print(f"   🎯 Últimas 5: {puntuaciones[-5:]}")
                            
                            # Verificar si coinciden con las puntuaciones de validación
                            validacion_inicial = [3.5000, 8.5000, 2.5000, 6.4084, 5.0000, 3.0000, 0.4792]
                            validacion_final = [8.0000, 7.3333, 0.1000, 4.5000, 3.0000]
                            
                            puntuaciones_float = []
                            for p in puntuaciones:
                                try:
                                    puntuaciones_float.append(float(p.replace(',', '.')))
                                except:
                                    continue
                            
                            coincidencias_inicial = 0
                            coincidencias_final = 0
                            
                            for val in validacion_inicial:
                                if val in puntuaciones_float:
                                    coincidencias_inicial += 1
                            
                            for val in validacion_final:
                                if val in puntuaciones_float:
                                    coincidencias_final += 1
                            
                            if coincidencias_inicial > 0:
                                print(f"   ✅ Coincidencias iniciales: {coincidencias_inicial}/7")
                            if coincidencias_final > 0:
                                print(f"   ✅ Coincidencias finales: {coincidencias_final}/5")
                                
                except Exception as e:
                    print(f"⚠️ Error en página {num_pagina + 1}: {e}")
                    
    except Exception as e:
        print(f"❌ Error en análisis: {e}")

def main():
    """Función principal."""
    pdf_path = "../../../data/rh03_257_2025_590_12_baremo_prov.pdf"
    
    print("🔍 ANÁLISIS FORENSE - LENGUA CASTELLANA Y LITERATURA")
    print("="*60)
    
    # 1. Búsqueda general
    resultados = buscar_lengua_literatura(pdf_path)
    
    if resultados:
        paginas_encontradas = [r[0] for r in resultados]
        print(f"\n📋 RESUMEN:")
        print(f"   Páginas encontradas: {paginas_encontradas}")
        print(f"   Rango estimado: {min(paginas_encontradas)}-{max(paginas_encontradas)}")
        
        # 2. Análisis detallado del rango
        if len(paginas_encontradas) > 1:
            inicio = min(paginas_encontradas)
            fin = max(paginas_encontradas)
            analizar_rango_paginas(pdf_path, inicio, fin)
            
    else:
        print("❌ No se encontraron páginas de Lengua Castellana y Literatura")
        print("💡 Probando búsqueda más amplia...")
        
        # Búsqueda alternativa en rangos conocidos
        rangos_alternativos = [
            (100, 150),
            (150, 200), 
            (200, 250),
            (250, 300),
            (300, 400),
            (400, 500)
        ]
        
        for inicio, fin in rangos_alternativos:
            print(f"\n🔍 Buscando en rango {inicio}-{fin}...")
            analizar_rango_paginas(pdf_path, inicio, fin)

if __name__ == "__main__":
    main()
