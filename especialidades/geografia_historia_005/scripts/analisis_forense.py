#!/usr/bin/env python3
"""
Análisis forense de Geografía e Historia (005) - Páginas 360-365
Para entender la estructura y depurar el extractor
"""

import pdfplumber
from pathlib import Path

def analizar_estructura_geografia_historia():
    """Analiza las primeras páginas de Geografía e Historia para entender la estructura"""
    
    pdf_path = Path("data/rh03_257_2025_590_12_baremo_prov.pdf")
    
    print("🗺️ ANÁLISIS FORENSE - Geografía e Historia (005)")
    print("=" * 60)
    
    with pdfplumber.open(pdf_path) as pdf:
        # Analizar páginas 360-365 (índices 359-364)
        for num_pagina in range(359, 365):
            if num_pagina >= len(pdf.pages):
                break
                
            print(f"\n📄 PÁGINA {num_pagina + 1}:")
            print("-" * 30)
            
            pagina = pdf.pages[num_pagina]
            texto = pagina.extract_text()
            
            if texto:
                lineas = texto.split('\n')
                candidatos_encontrados = 0
                
                for i, linea in enumerate(lineas):
                    if '****' in linea:
                        candidatos_encontrados += 1
                        print(f"Candidato {candidatos_encontrados}:")
                        print(f"  Línea {i+1}: {linea[:100]}{'...' if len(linea) > 100 else ''}")
                        
                        # Buscar líneas relacionadas (anterior y posterior)
                        if i > 0:
                            print(f"  Anterior:  {lineas[i-1][:100]}{'...' if len(lineas[i-1]) > 100 else ''}")
                        if i < len(lineas) - 1:
                            print(f"  Posterior: {lineas[i+1][:100]}{'...' if len(lineas[i+1]) > 100 else ''}")
                        
                        if candidatos_encontrados >= 5:  # Limitar a 5 candidatos por página
                            break
                
                print(f"\nTotal candidatos en página {num_pagina + 1}: {candidatos_encontrados}")

if __name__ == "__main__":
    analizar_estructura_geografia_historia()
