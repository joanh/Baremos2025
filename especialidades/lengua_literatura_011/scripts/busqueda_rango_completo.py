#!/usr/bin/env python3
"""
Búsqueda específica del rango completo de Lengua Castellana y Literatura
Localiza el inicio y final exacto de la especialidad
"""

import pdfplumber
import re

def buscar_rango_completo(pdf_path: str):
    """Buscar el rango completo de páginas para Lengua y Literatura."""
    print("🔍 BÚSQUEDA DEL RANGO COMPLETO")
    print("="*50)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            paginas_con_datos = []
            
            # Buscar en las primeras 100 páginas
            for i in range(min(100, len(pdf.pages))):
                try:
                    page = pdf.pages[i]
                    texto = page.extract_text()
                    
                    if texto:
                        # Buscar puntuaciones válidas (formato del baremo)
                        puntuaciones = re.findall(r'\b\d+[.,]\d{4}\b', texto)
                        
                        # Filtrar puntuaciones válidas (0.0000 a 10.0000)
                        puntuaciones_validas = []
                        for p in puntuaciones:
                            try:
                                val = float(p.replace(',', '.'))
                                if 0.0 <= val <= 10.0:
                                    puntuaciones_validas.append(val)
                            except:
                                continue
                        
                        # Si hay suficientes puntuaciones válidas, es una página de datos
                        if len(puntuaciones_validas) > 20:  # Umbral mínimo
                            paginas_con_datos.append(i + 1)
                            print(f"📄 Página {i+1}: {len(puntuaciones_validas)} puntuaciones válidas")
                            
                            # Mostrar algunas puntuaciones de muestra
                            muestra = puntuaciones_validas[:10]
                            print(f"   Muestra: {muestra}")
                            
                            # Verificar si es el inicio o final
                            if "LENGUA" in texto.upper() and "CASTELLANA" in texto.upper():
                                print(f"   🎯 Contiene referencia a LENGUA CASTELLANA")
                            
                            # Buscar indicadores de inicio/final de especialidad
                            if "ESPECIALIDAD" in texto.upper():
                                print(f"   📋 Menciona ESPECIALIDAD")
                                
                except Exception as e:
                    continue
            
            if paginas_con_datos:
                inicio = min(paginas_con_datos)
                fin = max(paginas_con_datos)
                
                print(f"\n📊 RESULTADO:")
                print(f"   Páginas con datos: {len(paginas_con_datos)}")
                print(f"   Primera página: {inicio}")
                print(f"   Última página: {fin}")
                print(f"   Rango estimado: {inicio}-{fin}")
                
                return inicio, fin
            else:
                print("❌ No se encontraron páginas con datos válidos")
                return None, None
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None

def verificar_paginas_especificas(pdf_path: str, paginas: list):
    """Verificar páginas específicas para encontrar las puntuaciones de validación."""
    print(f"\n🔍 VERIFICACIÓN DE PÁGINAS ESPECÍFICAS")
    print("="*50)
    
    validacion_inicial = [3.5000, 8.5000, 2.5000, 6.4084, 5.0000, 3.0000, 0.4792]
    validacion_final = [8.0000, 7.3333, 0.1000, 4.5000, 3.0000]
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for num_pagina in paginas:
                if num_pagina <= len(pdf.pages):
                    try:
                        page = pdf.pages[num_pagina - 1]
                        texto = page.extract_text()
                        
                        if texto:
                            puntuaciones = re.findall(r'\b\d+[.,]\d{4}\b', texto)
                            puntuaciones_float = []
                            
                            for p in puntuaciones:
                                try:
                                    puntuaciones_float.append(float(p.replace(',', '.')))
                                except:
                                    continue
                            
                            # Verificar coincidencias con validación inicial
                            coincidencias_inicial = sum(1 for val in validacion_inicial if val in puntuaciones_float)
                            coincidencias_final = sum(1 for val in validacion_final if val in puntuaciones_float)
                            
                            print(f"📄 Página {num_pagina}:")
                            print(f"   Total puntuaciones: {len(puntuaciones_float)}")
                            print(f"   Coincidencias inicial: {coincidencias_inicial}/7")
                            print(f"   Coincidencias final: {coincidencias_final}/5")
                            
                            if coincidencias_inicial >= 5:
                                print(f"   ✅ Posible página INICIAL")
                            if coincidencias_final >= 3:
                                print(f"   ✅ Posible página FINAL")
                            
                            if puntuaciones_float:
                                print(f"   Rango: {min(puntuaciones_float):.4f} - {max(puntuaciones_float):.4f}")
                            print()
                            
                    except Exception as e:
                        print(f"⚠️ Error en página {num_pagina}: {e}")
                        
    except Exception as e:
        print(f"❌ Error verificando páginas: {e}")

def main():
    pdf_path = "../../../data/rh03_257_2025_590_12_baremo_prov.pdf"
    
    # 1. Buscar rango completo
    inicio, fin = buscar_rango_completo(pdf_path)
    
    # 2. Si encontramos un rango, verificar páginas específicas
    if inicio and fin:
        # Verificar algunas páginas del rango para encontrar las de validación
        paginas_verificar = [inicio, inicio+1, inicio+2, fin-2, fin-1, fin]
        verificar_paginas_especificas(pdf_path, paginas_verificar)
        
        # También verificar las páginas originales que me dijiste
        print("\n🔍 VERIFICACIÓN DE PÁGINAS ORIGINALES (113, 359)")
        verificar_paginas_especificas(pdf_path, [113, 359])

if __name__ == "__main__":
    main()
