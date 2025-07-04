#!/usr/bin/env python3
"""
Análisis Forense de PDF - Matemáticas 008
Busca las páginas específicas de la especialidad de Matemáticas

Autor: @joanh
Asistente: Claude Sonnet 4.0
"""

import pdfplumber
import re
from pathlib import Path

# Configurar rutas
SCRIPT_DIR = Path(__file__).parent
ESPECIALIDAD_DIR = SCRIPT_DIR.parent
DATA_DIR = ESPECIALIDAD_DIR / "data"
PDF_PATH = DATA_DIR / "baremo_matematicas_008_2025.pdf"

# Si no existe, usar el PDF global
if not PDF_PATH.exists():
    PDF_PATH = ESPECIALIDAD_DIR.parent.parent / "data" / "rh03_257_2025_590_12_baremo_prov.pdf"

def buscar_matematicas_en_pdf():
    """Busca las páginas que contienen información de Matemáticas"""
    
    print("🔍 ANÁLISIS FORENSE - MATEMÁTICAS (008)")
    print("=" * 60)
    
    if not PDF_PATH.exists():
        print(f"❌ PDF no encontrado: {PDF_PATH}")
        print("📁 Coloca el PDF en la carpeta data/")
        return
    
    print(f"📄 Analizando: {PDF_PATH.name}")
    
    # Patrones a buscar
    patrones = [
        r"008.*MATEMÁTICAS",
        r"MATEMÁTICAS.*008", 
        r"PROFESORES.*MATEMÁTICAS",
        r"ENSEÑANZA SECUNDARIA.*MATEMÁTICAS"
    ]
    
    paginas_encontradas = []
    
    try:
        with pdfplumber.open(PDF_PATH) as pdf:
            print(f"📊 Total de páginas: {len(pdf.pages)}")
            print("\n🔎 Buscando referencias a Matemáticas...")
            
            for i, page in enumerate(pdf.pages, 1):
                try:
                    texto = page.extract_text()
                    if texto:
                        # Buscar patrones
                        for patron in patrones:
                            if re.search(patron, texto, re.IGNORECASE):
                                paginas_encontradas.append({
                                    'pagina': i,
                                    'patron': patron,
                                    'muestra': texto[:200] + "..."
                                })
                                print(f"✅ Página {i}: Encontrado '{patron}'")
                                break
                        
                        # Buscar candidatos (DNI + puntuación)
                        candidatos = re.findall(r'(\d{8}[A-Z]).*?(\d+[.,]\d{4})', texto)
                        if candidatos and len(candidatos) > 5:  # Más de 5 candidatos
                            print(f"📊 Página {i}: {len(candidatos)} candidatos encontrados")
                            
                except Exception as e:
                    print(f"⚠️ Error en página {i}: {e}")
                    continue
                
                # Progreso cada 100 páginas
                if i % 100 == 0:
                    print(f"🔄 Progreso: {i}/{len(pdf.pages)} páginas")
    
    except Exception as e:
        print(f"❌ Error leyendo PDF: {e}")
        return
    
    # Resultados
    print(f"\n📋 RESULTADOS:")
    print(f"🎯 Páginas con referencias: {len(paginas_encontradas)}")
    
    if paginas_encontradas:
        print(f"\n📄 PÁGINAS ENCONTRADAS:")
        for resultado in paginas_encontradas:
            print(f"  Página {resultado['pagina']}: {resultado['patron']}")
        
        # Sugerir rango
        paginas = [r['pagina'] for r in paginas_encontradas]
        rango_inicio = min(paginas)
        rango_fin = max(paginas)
        
        print(f"\n💡 CONFIGURACIÓN SUGERIDA:")
        print(f"pagina_inicio: {rango_inicio}")
        print(f"pagina_fin: {rango_fin}")
        print(f"\n✏️ Actualiza el archivo config.yaml con estos valores")
    else:
        print(f"❌ No se encontraron referencias claras a Matemáticas")
        print(f"💡 Revisa manualmente el PDF o ajusta los patrones de búsqueda")

def main():
    """Función principal"""
    buscar_matematicas_en_pdf()
    
    print(f"\n🔍 ANÁLISIS COMPLETADO")
    print(f"📝 Revisa los resultados y actualiza config.yaml")
    print(f"✍️ Análisis realizado por @joanh")

if __name__ == "__main__":
    main()
