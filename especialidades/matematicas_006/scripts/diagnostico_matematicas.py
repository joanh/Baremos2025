#!/usr/bin/env python3
"""
Diagnóstico de páginas de Matemáticas
Para entender el formato real de los datos
"""

import pdfplumber
from pathlib import Path

def analizar_pagina_matematicas(pagina_num):
    """Analiza una página específica de Matemáticas"""
    
    pdf_path = Path("../data/baremo_matematicas_006_2025.pdf")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if pagina_num - 1 < len(pdf.pages):
                page = pdf.pages[pagina_num - 1]
                texto = page.extract_text()
                
                print(f"=== PÁGINA {pagina_num} ===")
                print("TEXTO COMPLETO:")
                print(texto[:1000])  # Primeros 1000 caracteres
                print("\n" + "="*50)
                
                # Analizar línea por línea
                print("LÍNEAS INDIVIDUALES:")
                lineas = texto.split('\n')
                for i, linea in enumerate(lineas[:20]):  # Primeras 20 líneas
                    if linea.strip():
                        print(f"{i+1:2d}: {linea}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Analizar varias páginas para entender el patrón
    for pagina in [662, 670, 680, 700, 800, 900, 924]:
        analizar_pagina_matematicas(pagina)
        print("\n" + "="*80 + "\n")
