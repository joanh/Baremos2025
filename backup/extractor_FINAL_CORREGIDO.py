import pdfplumber
import re

print("=== EXTRACTOR FINAL CORREGIDO ===")
print("Patrón mejorado basado en análisis forense")

with pdfplumber.open("rh03_257_2025_590_12_baremo_prov.pdf") as pdf:
    
    puntuaciones_total = []
    
    print("Extrayendo con patrón corregido...")
    
    for num_pagina in range(2648, 2697):  # 2649 a 2697
        page = pdf.pages[num_pagina]
        puntuaciones_pagina = []
        
        try:
            texto = page.extract_text()
            if texto:
                lineas = texto.split('\n')
                
                for linea in lineas:
                    # Buscar líneas que empiecen con ****
                    if linea.startswith('****') and '*' in linea[4:]:
                        
                        # Buscar TODOS los números en la línea
                        numeros = re.findall(r'\b(\d{1,2},\d{4})\b', linea)
                        
                        if numeros:
                            # El primer número es el Total (basado en análisis forense)
                            primer_numero = numeros[0]
                            try:
                                valor = float(primer_numero.replace(',', '.'))
                                if 0.0 <= valor <= 10.0:
                                    puntuaciones_pagina.append(valor)
                                    print(f"Página {num_pagina + 1}: {valor:.4f}")
                            except:
                                pass
        
        except Exception as e:
            print(f"Error página {num_pagina + 1}: {e}")
        
        puntuaciones_total.extend(puntuaciones_pagina)
        
        # Mostrar progreso
        print(f"  → Página {num_pagina + 1}: {len(puntuaciones_pagina)} candidatos")
    
    # RESULTADOS
    print(f"\n{'='*50}")
    print("=== RESULTADOS FINALES ===")
    print(f"{'='*50}")
    
    puntuaciones_unicas = list(set(puntuaciones_total))
    puntuaciones_unicas.sort(reverse=True)
    
    print(f"Total extraído: {len(puntuaciones_total)}")
    print(f"Únicos: {len(puntuaciones_unicas)}")
    print(f"Objetivo: 331")
    
    if len(puntuaciones_unicas) > 0:
        print(f"Rango: {min(puntuaciones_unicas):.4f} - {max(puntuaciones_unicas):.4f}")
        
        # Verificar con valores conocidos
        conocidos = [2.4167, 7.3333, 3.6500, 5.2084, 2.5000, 4.3333, 5.7500,
                    1.8000, 6.8500, 8.0000, 5.0000, 7.5833, 7.5000, 6.3750,
                    1.9167, 2.2500, 10.0000, 1.0000, 1.7500, 7.0042, 1.0000]
        
        encontrados = sum(1 for v in conocidos if v in puntuaciones_unicas)
        print(f"Verificación: {encontrados}/{len(conocidos)} valores conocidos")
        
        # GUARDAR SIEMPRE (independientemente del resultado)
        print(f"\n=== GUARDANDO DATOS ===")
        
        with open('INFORMATICA_107_EXTRACCION.txt', 'w') as f:
            for p in puntuaciones_unicas:
                f.write(f"{p:.4f}\n")
        print("💾 Guardado: INFORMATICA_107_EXTRACCION.txt")
        
        with open('INFORMATICA_107_EXTRACCION.csv', 'w') as f:
            f.write("Puntuacion_Total\n")
            for p in puntuaciones_unicas:
                f.write(f"{p:.4f}\n")
        print("💾 Guardado: INFORMATICA_107_EXTRACCION.csv")
        
        # Mostrar muestra
        print(f"\n=== MUESTRA EXTRAÍDA ===")
        print("Primeros 20 valores:")
        for i, p in enumerate(puntuaciones_unicas[:20]):
            print(f"{i+1:2d}. {p:.4f}")
        
        if len(puntuaciones_unicas) < 250:
            print(f"\n⚠️ Solo {len(puntuaciones_unicas)} valores extraídos")
            print("Necesitamos analizar por qué faltan tantos...")
            
            # DIAGNÓSTICO: Mostrar qué encuentra en página 2649
            print(f"\n=== DIAGNÓSTICO PÁGINA 2649 ===")
            page_test = pdf.pages[2648]
            texto_test = page_test.extract_text()
            
            if texto_test:
                lineas_dni = [l for l in texto_test.split('\n') if l.startswith('****')]
                print(f"Líneas DNI encontradas: {len(lineas_dni)}")
                
                for i, linea in enumerate(lineas_dni):
                    numeros = re.findall(r'\b(\d{1,2},\d{4})\b', linea)
                    print(f"DNI {i+1}: {len(numeros)} números")
                    print(f"  Línea: {linea[:60]}...")
                    if numeros:
                        print(f"  Primer número: {numeros[0]}")
        
        else:
            print(f"✅ Extracción razonable: {len(puntuaciones_unicas)} candidatos")
    
    else:
        print("❌ No se extrajo ningún valor")

print("\n🔍 EXTRACTOR CON PATRÓN MEJORADO")
print("📋 Busca primer número en líneas que empiecen con ****")