#!/usr/bin/env python3
"""
Búsqueda específica de Lengua Castellana y Literatura (011) en el PDF
"""

import pdfplumber
import re
from pathlib import Path

def buscar_especialidad_011():
    """Busca páginas que contengan la especialidad 011 - Lengua Castellana y Literatura"""
    
    pdf_path = Path(__file__).parent.parent / "data" / "rh03_257_2025_590_12_baremo_prov.pdf"
    
    if not pdf_path.exists():
        print(f"❌ PDF no encontrado: {pdf_path}")
        return
        
    print("🔍 BÚSQUEDA ESPECÍFICA LENGUA CASTELLANA Y LITERATURA (011)")
    print(f"📁 PDF: {pdf_path}")
    print("="*70)
    
    encontradas = []
    
    with pdfplumber.open(pdf_path) as pdf:
        total_paginas = len(pdf.pages)
        print(f"📖 Total páginas en PDF: {total_paginas}")
        
        # Buscar en un rango amplio
        for i in range(min(100, total_paginas)):  # Primeras 100 páginas
            page = pdf.pages[i]
            text = page.extract_text()
            
            if text:
                # Buscar específicamente 011 - Lengua
                if "011" in text and ("LENGUA" in text.upper() or "LITERATURA" in text.upper()):
                    encontradas.append(i + 1)
                    print(f"✅ Página {i+1}: Encontrada especialidad 011")
                    
                    # Mostrar contexto
                    lines = text.split('\n')
                    for line in lines[:10]:
                        if "011" in line or "LENGUA" in line.upper() or "LITERATURA" in line.upper():
                            print(f"   📄 {line.strip()}")
                    print()
                    
                    # Solo mostrar las primeras 5 coincidencias para no saturar
                    if len(encontradas) >= 5:
                        print(f"🔍 Continuando búsqueda (mostrando solo primeras 5)...")
                        break
        
        print("="*70)
        if encontradas:
            print(f"🎯 RESUMEN: Encontradas {len(encontradas)} páginas con especialidad 011")
            print(f"📊 Páginas: {encontradas}")
            
            # Buscar el rango completo si encontramos páginas
            if encontradas:
                primera = encontradas[0]
                # Buscar el final del rango
                print(f"\n🔍 Buscando final del rango desde página {primera}...")
                
                fin_rango = primera
                for i in range(primera, min(primera + 100, total_paginas)):
                    page = pdf.pages[i]
                    text = page.extract_text()
                    
                    if text and "011" in text and ("LENGUA" in text.upper() or "LITERATURA" in text.upper()):
                        fin_rango = i + 1
                    else:
                        # Si no encontramos 011, revisar si cambia de especialidad
                        if "ESPECIALIDAD:" in text:
                            lines = text.split('\n')
                            for line in lines:
                                if "ESPECIALIDAD:" in line:
                                    print(f"📄 Página {i+1}: {line.strip()}")
                                    break
                            break
                
                print(f"🎯 RANGO ESTIMADO: Páginas {primera}-{fin_rango}")
                
        else:
            print("❌ No se encontró la especialidad 011 en las primeras 100 páginas")
            print("💡 Puede estar en un rango diferente del PDF")

if __name__ == "__main__":
    buscar_especialidad_011()
