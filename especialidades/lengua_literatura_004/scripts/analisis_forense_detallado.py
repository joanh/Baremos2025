#!/usr/bin/env python3
"""
Análisis forense específico para Lengua Castellana y Literatura (011)
Investigar por qué los datos extraídos son tan raros
"""

import pdfplumber
import re
from pathlib import Path

def analizar_pagina_detalle(pdf_path, pagina_num):
    """Analiza en detalle una página específica"""
    print(f"\n{'='*60}")
    print(f"📄 ANÁLISIS DETALLADO PÁGINA {pagina_num}")
    print(f"{'='*60}")
    
    with pdfplumber.open(pdf_path) as pdf:
        if pagina_num > len(pdf.pages):
            print(f"❌ Página {pagina_num} no existe (total: {len(pdf.pages)})")
            return
            
        page = pdf.pages[pagina_num - 1]  # pdfplumber usa índice 0
        
        # Extraer texto completo
        text = page.extract_text()
        if text:
            print(f"📝 Texto extraído (primeros 500 caracteres):")
            print(text[:500])
            print(f"\n📊 Longitud total del texto: {len(text)} caracteres")
            
            # Buscar todas las puntuaciones
            puntuaciones = re.findall(r'\b\d+[,\.]\d{4}\b', text)
            print(f"\n🎯 Puntuaciones encontradas: {len(puntuaciones)}")
            if puntuaciones:
                print("Primeras 20:", puntuaciones[:20])
                
                # Convertir a float y verificar
                validas = []
                for p in puntuaciones:
                    try:
                        val = float(p.replace(',', '.'))
                        if 0.0 <= val <= 10.0:
                            validas.append(val)
                    except:
                        pass
                        
                print(f"✅ Puntuaciones válidas: {len(validas)}")
                if validas:
                    print(f"📈 Min: {min(validas):.4f}, Max: {max(validas):.4f}, Media: {sum(validas)/len(validas):.4f}")
        else:
            print("❌ No se pudo extraer texto")
            
        # Intentar extraer tablas
        tables = page.extract_tables()
        print(f"\n📋 Tablas encontradas: {len(tables)}")
        if tables:
            for i, table in enumerate(tables[:2]):  # Solo las primeras 2
                print(f"\n📊 Tabla {i+1}:")
                print(f"   Filas: {len(table)}")
                if table:
                    print(f"   Columnas: {len(table[0]) if table[0] else 0}")
                    # Mostrar primeras filas
                    for j, row in enumerate(table[:3]):
                        print(f"   Fila {j+1}: {row}")

def main():
    # Ruta al PDF
    pdf_path = Path(__file__).parent.parent / "data" / "rh03_257_2025_590_12_baremo_prov.pdf"
    
    if not pdf_path.exists():
        print(f"❌ PDF no encontrado: {pdf_path}")
        return
        
    print("🔍 ANÁLISIS FORENSE - LENGUA CASTELLANA Y LITERATURA (011)")
    print(f"📁 PDF: {pdf_path}")
    
    # Analizar páginas específicas según config
    paginas_analizar = [2, 3, 5, 8, 10]  # Muestra de páginas
    
    for pagina in paginas_analizar:
        analizar_pagina_detalle(pdf_path, pagina)
        
    print(f"\n{'='*60}")
    print("🎯 CONCLUSIONES DEL ANÁLISIS")
    print(f"{'='*60}")
    print("Si el patrón de extracción no funciona correctamente,")
    print("revisar el formato específico de las páginas de Lengua y Literatura.")

if __name__ == "__main__":
    main()
