import os
import re

print("=== EXTRACTOR ESPECÍFICO INFORMÁTICA 331 CANDIDATOS ===")
print("Páginas: 2649-2697")
print("Candidatos esperados: 331")
print()

# Verificar pdfplumber
try:
    import pdfplumber
    print("✅ pdfplumber disponible")
except ImportError:
    print("❌ Instalar: python -m pip install pdfplumber")
    exit()

# Verificar PDF
pdf_file = "rh03_257_2025_590_12_baremo_prov.pdf"
if not os.path.exists(pdf_file):
    print(f"❌ PDF no encontrado: {pdf_file}")
    exit()

print(f"✅ PDF encontrado: {pdf_file}")

# EXTRACCIÓN ESPECÍFICA
with pdfplumber.open(pdf_file) as pdf:
    print(f"PDF: {len(pdf.pages)} páginas totales")
    
    # Páginas específicas de Informática: 2649-2697 (índices 2648-2696)
    pagina_inicio = 2648  # Página 2649 (índice 0-based)
    pagina_fin = 2697     # Página 2697 incluida
    
    todas_puntuaciones = []
    estadisticas_paginas = {}
    
    print(f"Procesando páginas {pagina_inicio + 1} a {pagina_fin}...")
    
    for num_pagina in range(pagina_inicio, min(pagina_fin, len(pdf.pages))):
        page = pdf.pages[num_pagina]
        puntuaciones_pagina = []
        
        try:
            # Extraer texto completo de la página
            texto = page.extract_text()
            
            if texto:
                # Dividir en líneas
                lineas = texto.split('\n')
                
                # Buscar líneas que contengan DNI (patrón con asteriscos)
                for linea in lineas:
                    if '****' in linea and linea.count('*') >= 4:
                        # Buscar TODOS los números en formato x,xxxx
                        numeros = re.findall(r'\b(\d{1,2},\d{4})\b', linea)
                        
                        if numeros:
                            # El último número en línea de DNI es típicamente el Total
                            ultimo = numeros[-1]
                            try:
                                valor = float(ultimo.replace(',', '.'))
                                if 0.0 <= valor <= 10.0:
                                    puntuaciones_pagina.append(valor)
                            except:
                                pass
                
                # MÉTODO ALTERNATIVO: Buscar patrones de fin de línea
                for linea in lineas:
                    # Líneas que terminen con x,xxxx
                    match = re.search(r'\b(\d{1,2},\d{4})\s*$', linea.strip())
                    if match:
                        try:
                            valor = float(match.group(1).replace(',', '.'))
                            if 0.0 <= valor <= 10.0:
                                puntuaciones_pagina.append(valor)
                        except:
                            pass
        
        except Exception as e:
            print(f"Error en página {num_pagina + 1}: {e}")
        
        # Eliminar duplicados de esta página
        puntuaciones_unicas_pagina = list(set(puntuaciones_pagina))
        estadisticas_paginas[num_pagina + 1] = len(puntuaciones_unicas_pagina)
        todas_puntuaciones.extend(puntuaciones_unicas_pagina)
        
        print(f"Página {num_pagina + 1}: {len(puntuaciones_unicas_pagina)} puntuaciones")
    
    # ANÁLISIS FINAL
    puntuaciones_finales = list(set(todas_puntuaciones))  # Eliminar duplicados globales
    puntuaciones_finales.sort(reverse=True)
    
    print(f"\n{'='*50}")
    print("=== RESULTADOS EXTRACCIÓN ===")
    print(f"{'='*50}")
    print(f"Páginas procesadas: {pagina_fin - pagina_inicio}")
    print(f"Puntuaciones extraídas: {len(todas_puntuaciones)}")
    print(f"Puntuaciones únicas: {len(puntuaciones_finales)}")
    print(f"Objetivo (331 candidatos): {331}")
    
    if len(puntuaciones_finales) > 0:
        print(f"Rango: {min(puntuaciones_finales):.4f} - {max(puntuaciones_finales):.4f}")
        
        # Verificar con muestra conocida
        muestra_conocida = [
            2.4167, 7.3333, 3.6500, 5.2084, 2.5000, 4.3333, 5.7500,  # Página 2649
            1.8000, 6.8500, 8.0000, 5.0000, 7.5833, 7.5000, 6.3750,  # Página 2650
            1.9167, 2.2500, 10.0000, 1.0000, 1.7500, 7.0042, 1.0000  # Página 2651
        ]
        
        coincidencias = sum(1 for v in muestra_conocida if v in puntuaciones_finales)
        print(f"Verificación muestra: {coincidencias}/{len(muestra_conocida)} coincidencias")
        
        if coincidencias >= len(muestra_conocida) * 0.8:  # 80% coincidencia
            print("✅ Extracción parece correcta")
            
            # GUARDAR DATOS REALES
            print(f"\n=== GUARDANDO 331 CANDIDATOS REALES ===")
            
            # TXT
            with open('informatica_107_331_candidatos.txt', 'w') as f:
                for p in puntuaciones_finales:
                    f.write(f"{p:.4f}\n")
            print("✅ informatica_107_331_candidatos.txt")
            
            # CSV
            try:
                import pandas as pd
                df = pd.DataFrame({'Puntuacion_Total': puntuaciones_finales})
                df.to_csv('informatica_107_331_candidatos.csv', index=False)
                print("✅ informatica_107_331_candidatos.csv")
            except:
                with open('informatica_107_331_candidatos.csv', 'w') as f:
                    f.write("Puntuacion_Total\n")
                    for p in puntuaciones_finales:
                        f.write(f"{p:.4f}\n")
                print("✅ informatica_107_331_candidatos.csv (manual)")
            
            # Código Python listo
            codigo = f"# Datos REALES Informática 107\n"
            codigo += f"# Extraído de páginas 2649-2697\n"
            codigo += f"# Total candidatos: {len(puntuaciones_finales)}\n\n"
            codigo += "puntuaciones_informatica_107 = [\n"
            
            for i, p in enumerate(puntuaciones_finales):
                if i % 10 == 0 and i > 0:
                    codigo += "\n"
                codigo += f"    {p:.4f},"
            
            codigo = codigo.rstrip(',') + "\n]\n"
            
            with open('informatica_107_datos_completos.py', 'w') as f:
                f.write(codigo)
            print("✅ informatica_107_datos_completos.py")
            
            # Estadísticas rápidas
            print(f"\n=== ESTADÍSTICAS RÁPIDAS ===")
            print(f"Media: {sum(puntuaciones_finales)/len(puntuaciones_finales):.4f}")
            
            altos = [p for p in puntuaciones_finales if p >= 9.0]
            print(f"Puntuaciones >= 9.0: {len(altos)}")
            
            perfectos = [p for p in puntuaciones_finales if p == 10.0]
            print(f"Puntuaciones = 10.0: {len(perfectos)}")
            
            print(f"\nTOP 10:")
            for i, p in enumerate(puntuaciones_finales[:10]):
                print(f"{i+1:2d}. {p:.4f}")
            
        else:
            print("⚠️ Pocas coincidencias con muestra - revisar extracción")
            
            # Mostrar muestra de lo extraído para diagnóstico
            print(f"Muestra extraída (primeros 10):")
            for p in puntuaciones_finales[:10]:
                print(f"  {p:.4f}")
    
    else:
        print("❌ No se extrajeron puntuaciones")
        
        # DIAGNÓSTICO
        print("\n=== DIAGNÓSTICO ===")
        print("Muestra de página 2649:")
        page_test = pdf.pages[2648]  # Página 2649
        texto_test = page_test.extract_text()
        
        if texto_test:
            lineas_test = texto_test.split('\n')[:15]
            for i, linea in enumerate(lineas_test):
                print(f"{i+1:2d}: {linea}")
        
    # Resumen por páginas
    print(f"\n=== RESUMEN POR PÁGINAS ===")
    total_encontrado = 0
    for pagina, count in estadisticas_paginas.items():
        print(f"Página {pagina}: {count} puntuaciones")
        total_encontrado += count
    
    print(f"Total encontrado: {total_encontrado}")
    
    if total_encontrado < 300:
        print("⚠️ Menos candidatos de lo esperado (331)")
    elif total_encontrado > 350:
        print("⚠️ Más candidatos de lo esperado - posibles duplicados")
    else:
        print("✅ Cantidad razonable de candidatos")

print(f"\n🎯 OBJETIVO: Extraer los 331 candidatos reales de Informática")
print("📁 Archivos que se generarán:")
print("- informatica_107_331_candidatos.txt")
print("- informatica_107_331_candidatos.csv")
print("- informatica_107_datos_completos.py")