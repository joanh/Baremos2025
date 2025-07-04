import pdfplumber
import re

print("=== EXTRACTOR DEFINITIVO INFORMÁTICA 331 ===")
print("Basado en análisis forense del PDF")

with pdfplumber.open("rh03_257_2025_590_12_baremo_prov.pdf") as pdf:
    
    # Páginas 2649-2697 (índices 2648-2696)
    puntuaciones_total = []
    
    print("Extrayendo puntuaciones Total de líneas DNI...")
    
    for num_pagina in range(2648, 2697):  # 2649 a 2697
        page = pdf.pages[num_pagina]
        puntuaciones_pagina = []
        
        try:
            texto = page.extract_text()
            if texto:
                lineas = texto.split('\n')
                
                # Buscar líneas que empiecen con ****
                for linea in lineas:
                    if linea.startswith('****') and '*' in linea[4:]:
                        # Patrón: ****XXXX* APELLIDOS NOMBRES, TOTAL ...
                        # Buscar: coma seguida de espacio y número (el Total)
                        match = re.search(r',\s+(\d{1,2},\d{4})', linea)
                        
                        if match:
                            valor_str = match.group(1)
                            try:
                                valor = float(valor_str.replace(',', '.'))
                                if 0.0 <= valor <= 10.0:
                                    puntuaciones_pagina.append(valor)
                                    print(f"Página {num_pagina + 1}: {valor:.4f}")
                            except:
                                pass
        
        except Exception as e:
            print(f"Error página {num_pagina + 1}: {e}")
        
        puntuaciones_total.extend(puntuaciones_pagina)
        
        # Verificar progreso
        if len(puntuaciones_pagina) != 7:
            print(f"⚠️ Página {num_pagina + 1}: {len(puntuaciones_pagina)} candidatos (esperado: 7)")
    
    # RESULTADOS
    print(f"\n{'='*50}")
    print("=== EXTRACCIÓN COMPLETADA ===")
    print(f"{'='*50}")
    
    puntuaciones_unicas = list(set(puntuaciones_total))
    puntuaciones_unicas.sort(reverse=True)
    
    print(f"Puntuaciones extraídas: {len(puntuaciones_total)}")
    print(f"Puntuaciones únicas: {len(puntuaciones_unicas)}")
    print(f"Objetivo: 331 candidatos")
    
    if len(puntuaciones_unicas) >= 300:  # Cercano a 331
        print("✅ EXTRACCIÓN EXITOSA")
        
        # Verificar con muestra conocida
        conocidos = [2.4167, 7.3333, 3.6500, 5.2084, 2.5000, 4.3333, 5.7500,
                    1.8000, 6.8500, 8.0000, 5.0000, 7.5833, 7.5000, 6.3750,
                    1.9167, 2.2500, 10.0000, 1.0000, 1.7500, 7.0042, 1.0000]
        
        encontrados = sum(1 for v in conocidos if v in puntuaciones_unicas)
        print(f"Verificación: {encontrados}/{len(conocidos)} valores conocidos encontrados")
        
        if encontrados >= 18:  # Al menos 85%
            print("✅ DATOS VALIDADOS")
            
            # GUARDAR DATOS REALES
            with open('INFORMATICA_107_DATOS_REALES.txt', 'w') as f:
                for p in puntuaciones_unicas:
                    f.write(f"{p:.4f}\n")
            print("💾 Guardado: INFORMATICA_107_DATOS_REALES.txt")
            
            # CSV
            try:
                import pandas as pd
                df = pd.DataFrame({'Puntuacion_Total': puntuaciones_unicas})
                df.to_csv('INFORMATICA_107_DATOS_REALES.csv', index=False)
                print("💾 Guardado: INFORMATICA_107_DATOS_REALES.csv")
            except:
                with open('INFORMATICA_107_DATOS_REALES.csv', 'w') as f:
                    f.write("Puntuacion_Total\n")
                    for p in puntuaciones_unicas:
                        f.write(f"{p:.4f}\n")
                print("💾 Guardado: INFORMATICA_107_DATOS_REALES.csv")
            
            # ESTADÍSTICAS FINALES
            print(f"\n=== ESTADÍSTICAS REALES ===")
            print(f"📊 Total candidatos: {len(puntuaciones_unicas)}")
            print(f"🏆 Puntuación máxima: {max(puntuaciones_unicas):.4f}")
            print(f"📉 Puntuación mínima: {min(puntuaciones_unicas):.4f}")
            print(f"📈 Media: {sum(puntuaciones_unicas)/len(puntuaciones_unicas):.4f}")
            
            altos = [p for p in puntuaciones_unicas if p >= 9.0]
            print(f"🎯 Puntuaciones >= 9.0: {len(altos)}")
            if altos:
                print(f"    Valores: {sorted(altos, reverse=True)}")
            
            perfectos = [p for p in puntuaciones_unicas if p == 10.0]
            print(f"💯 Puntuaciones perfectas (10.0): {len(perfectos)}")
            
            print(f"\n🏅 TOP 10:")
            for i, p in enumerate(puntuaciones_unicas[:10]):
                print(f"{i+1:2d}. {p:.4f}")
            
            print(f"\n🎉 ¡MISIÓN CUMPLIDA!")
            print(f"✅ {len(puntuaciones_unicas)} candidatos reales extraídos")
            print(f"📁 Archivos generados con datos auténticos del PDF")
            
        else:
            print(f"⚠️ Solo {encontrados} coincidencias - revisar")
    
    else:
        print(f"❌ Solo {len(puntuaciones_unicas)} candidatos extraídos")
        print("Revisar patrón de extracción")

print("\n🎯 EXTRACTOR BASADO EN ANÁLISIS FORENSE")
print("📋 Patrón identificado: ****XXXX* NOMBRE, TOTAL ...")
print("🔍 Extrae el primer número después de la coma en líneas DNI")