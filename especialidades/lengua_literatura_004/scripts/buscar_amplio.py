#!/usr/bin/env python3
"""
Búsqueda amplia de especialidades en el PDF para encontrar 011
"""

import pdfplumber
import re
from pathlib import Path

def buscar_especialidades_amplio():
    """Busca todas las especialidades en un rango amplio del PDF"""
    
    pdf_path = Path(__file__).parent.parent / "data" / "rh03_257_2025_590_12_baremo_prov.pdf"
    
    if not pdf_path.exists():
        print(f"❌ PDF no encontrado: {pdf_path}")
        return
        
    print("🔍 BÚSQUEDA AMPLIA DE ESPECIALIDADES")
    print(f"📁 PDF: {pdf_path}")
    print("="*70)
    
    especialidades_encontradas = {}
    
    with pdfplumber.open(pdf_path) as pdf:
        total_paginas = len(pdf.pages)
        print(f"📖 Total páginas en PDF: {total_paginas}")
        
        # Buscar en saltos más grandes
        salto = 20
        for i in range(0, min(500, total_paginas), salto):  # Primeras 500 páginas, cada 20
            page = pdf.pages[i]
            text = page.extract_text()
            
            if text:
                # Buscar patrón ESPECIALIDAD: XXX
                matches = re.findall(r'ESPECIALIDAD:\s*(\d+)\s*-\s*([A-ZÁÉÍÓÚ\s]+)', text, re.IGNORECASE)
                if matches:
                    for codigo, nombre in matches:
                        if codigo not in especialidades_encontradas:
                            especialidades_encontradas[codigo] = {
                                'nombre': nombre.strip(),
                                'primera_pagina': i + 1,
                                'paginas_vistas': []
                            }
                        especialidades_encontradas[codigo]['paginas_vistas'].append(i + 1)
                        
                        if codigo == "011":
                            print(f"✅ ENCONTRADA LENGUA (011) en página {i+1}")
                            print(f"   📄 {nombre.strip()}")
        
        print("\n" + "="*70)
        print("📊 ESPECIALIDADES ENCONTRADAS:")
        print("="*70)
        
        for codigo, info in sorted(especialidades_encontradas.items()):
            print(f"🎯 {codigo}: {info['nombre']}")
            print(f"   📄 Primera aparición: página {info['primera_pagina']}")
            print(f"   👀 Vistas en páginas: {info['paginas_vistas']}")
            print()
            
        # Si encontramos 011, buscar su rango específico
        if "011" in especialidades_encontradas:
            primera_011 = especialidades_encontradas["011"]["primera_pagina"]
            print(f"\n🔍 BÚSQUEDA DETALLADA PARA LENGUA (011) desde página {primera_011}")
            
            rango_inicio = max(1, primera_011 - 10)
            rango_fin = min(total_paginas, primera_011 + 100)
            
            print(f"📊 Buscando en páginas {rango_inicio}-{rango_fin}")
            
            paginas_011 = []
            for i in range(rango_inicio - 1, rango_fin):
                page = pdf.pages[i]
                text = page.extract_text()
                
                if text and "ESPECIALIDAD: 011" in text:
                    paginas_011.append(i + 1)
                    
            if paginas_011:
                print(f"✅ Lengua (011) encontrada en páginas: {paginas_011[:10]}...")
                print(f"🎯 RANGO RECOMENDADO: {paginas_011[0]}-{paginas_011[-1]}")
            else:
                print("❌ No se encontró rango específico para 011")

if __name__ == "__main__":
    buscar_especialidades_amplio()
