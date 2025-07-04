#!/usr/bin/env python3
"""
Obtener puntuaciones de validación para páginas 121 y 341
"""

import pdfplumber
import re
from pathlib import Path

def obtener_puntuaciones_validacion(pagina_num):
    """Obtiene puntuaciones reales de una página específica"""
    
    pdf_path = Path(__file__).parent.parent / "data" / "rh03_257_2025_590_12_baremo_prov.pdf"
    
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[pagina_num - 1]
        text = page.extract_text()
        
        print(f"\n📄 PÁGINA {pagina_num}")
        print("="*50)
        
        if text:
            # Verificar que es la especialidad correcta
            if "LENGUA CASTELLANA Y LITERATURA" in text.upper():
                print("✅ Especialidad correcta confirmada")
            else:
                print("❌ Especialidad no confirmada")
                
            # Extraer puntuaciones
            puntuaciones = re.findall(r'\b\d+[,\.]\d{4}\b', text)
            if puntuaciones:
                validas = []
                for p in puntuaciones:
                    try:
                        val = float(p.replace(',', '.'))
                        if 0.0 <= val <= 10.0:
                            validas.append(val)
                    except:
                        pass
                        
                print(f"📊 Puntuaciones encontradas: {len(validas)}")
                print(f"🎯 Primeras 10: {validas[:10]}")
                print(f"🏆 Rango: {min(validas):.4f} - {max(validas):.4f}")
                print(f"📈 Media: {sum(validas)/len(validas):.4f}")
                
                return validas[:7]  # Devolver las primeras 7 para validación
        
        return []

def main():
    print("🔍 OBTENER PUNTUACIONES DE VALIDACIÓN")
    print("📁 Lengua Castellana y Literatura (004)")
    
    # Obtener puntuaciones de las páginas inicial y final
    puntuaciones_121 = obtener_puntuaciones_validacion(121)
    puntuaciones_341 = obtener_puntuaciones_validacion(341)
    
    print("\n" + "="*60)
    print("📋 CONFIGURACIÓN DE VALIDACIÓN RECOMENDADA:")
    print("="*60)
    
    if puntuaciones_121:
        print(f"pagina_inicial:")
        print(f"  numero: 121")
        print(f"  puntuaciones_esperadas: {puntuaciones_121}")
        
    if puntuaciones_341:
        print(f"pagina_final:")
        print(f"  numero: 341") 
        print(f"  puntuaciones_esperadas: {puntuaciones_341}")

if __name__ == "__main__":
    main()
