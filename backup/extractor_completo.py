import os
import re
from collections import Counter

print("=== EXTRACTOR ESPECÍFICO COLUMNA TOTAL ===")

# Verificar si pdfplumber está disponible
try:
    import pdfplumber
    print("✅ pdfplumber disponible")
    PDFPLUMBER_OK = True
except ImportError:
    print("❌ pdfplumber no disponible")
    print("Ejecuta: python -m pip install pdfplumber")
    PDFPLUMBER_OK = False

# Verificar archivo PDF
pdf_file = "rh03_257_2025_590_12_baremo_prov.pdf"
if os.path.exists(pdf_file):
    print(f"✅ PDF encontrado: {pdf_file}")
    PDF_OK = True
else:
    print(f"❌ PDF no encontrado: {pdf_file}")
    PDF_OK = False

if PDFPLUMBER_OK and PDF_OK:
    print("\n🎯 EXTRAYENDO SOLO COLUMNA 'TOTAL' DE INFORMÁTICA...")
    
    # PÁGINAS ESPECÍFICAS DE INFORMÁTICA (2650-2697)
    pagina_inicio = 2649  # Índice 0-based (página 2650)
    pagina_fin = 2697     # Página 2697 incluida
    
    with pdfplumber.open(pdf_file) as pdf:
        print(f"PDF abierto: {len(pdf.pages)} páginas totales")
        print(f"Extrayendo SOLO columna Total de páginas {pagina_inicio + 1} a {pagina_fin}")
        
        puntuaciones_total = []
        puntuaciones_por_pagina = {}
        
        # Procesar solo las páginas de Informática
        for num_pagina in range(pagina_inicio, min(pagina_fin, len(pdf.pages))):
            page = pdf.pages[num_pagina]
            puntuaciones_pagina = []
            
            print(f"\n--- Procesando página {num_pagina + 1} ---")
            
            # MÉTODO 1: Buscar estructura de tabla específica
            try:
                tables = page.extract_tables()
                print(f"  Tablas encontradas: {len(tables)}")
                
                for j, table in enumerate(tables):
                    if table and len(table) > 0:
                        print(f"    Analizando tabla {j+1}: {len(table)} filas")
                        
                        # Buscar fila de cabecera con "Total"
                        header_row_idx = None
                        total_col_idx = None
                        
                        for row_idx, row in enumerate(table[:5]):  # Buscar en primeras 5 filas
                            if row:
                                for col_idx, cell in enumerate(row):
                                    if cell and isinstance(cell, str) and 'TOTAL' in cell.upper():
                                        header_row_idx = row_idx
                                        total_col_idx = col_idx
                                        print(f"      ✅ Columna 'Total' encontrada en fila {row_idx}, columna {col_idx}")
                                        break
                                if total_col_idx is not None:
                                    break
                        
                        # Si encontramos la columna Total, extraer sus valores
                        if total_col_idx is not None:
                            print(f"      Extrayendo datos de columna {total_col_idx}...")
                            
                            for row_idx in range(header_row_idx + 1, len(table)):
                                row = table[row_idx]
                                if row and len(row) > total_col_idx:
                                    cell = row[total_col_idx]
                                    if cell and isinstance(cell, str):
                                        # Buscar número en esta celda específica
                                        matches = re.findall(r'\b(\d{1,2},\d{4})\b', cell)
                                        for match in matches:
                                            try:
                                                valor = float(match.replace(',', '.'))
                                                if 0.0 <= valor <= 10.0:
                                                    puntuaciones_pagina.append(valor)
                                                    print(f"        Total: {valor:.4f}")
                                            except:
                                                pass
                        else:
                            print(f"      ❌ No se encontró columna 'Total' en tabla {j+1}")
                            
                            # Fallback: buscar patrón de línea con DNI seguido de puntuaciones
                            print(f"      🔍 Buscando patrón alternativo...")
                            
                            for row_idx, row in enumerate(table):
                                if row:
                                    row_text = ' '.join([str(cell) for cell in row if cell])
                                    
                                    # Buscar patrón: DNI (****xxxx*) seguido de puntuaciones
                                    # El último número suele ser el Total
                                    if '****' in row_text and '*' in row_text:
                                        numeros = re.findall(r'\b(\d{1,2},\d{4})\b', row_text)
                                        if numeros:
                                            # Tomar el último número (suele ser Total)
                                            ultimo_numero = numeros[-1]
                                            try:
                                                valor = float(ultimo_numero.replace(',', '.'))
                                                if 0.0 <= valor <= 10.0:
                                                    puntuaciones_pagina.append(valor)
                                                    print(f"        Total (patrón): {valor:.4f}")
                                            except:
                                                pass
                            
            except Exception as e:
                print(f"  Error extrayendo tablas: {e}")
            
            # MÉTODO 2: Buscar en texto con patrones específicos
            try:
                texto = page.extract_text()
                if texto:
                    print(f"  🔍 Analizando texto para patrones específicos...")
                    
                    # Dividir en líneas
                    lines = texto.split('\n')
                    
                    # Buscar líneas que contengan DNI y extraer el último número
                    for line in lines:
                        if '****' in line and line.count('*') >= 4:
                            # Esta línea contiene un DNI, buscar números
                            numeros = re.findall(r'\b(\d{1,2},\d{4})\b', line)
                            if numeros:
                                # El último número en una línea con DNI suele ser Total
                                ultimo_numero = numeros[-1]
                                try:
                                    valor = float(ultimo_numero.replace(',', '.'))
                                    if 0.0 <= valor <= 10.0:
                                        puntuaciones_pagina.append(valor)
                                        print(f"        Total (línea DNI): {valor:.4f}")
                                except:
                                    pass
                    
                    # También buscar líneas que terminen con un número (posible Total)
                    for line in lines:
                        line_clean = line.strip()
                        if line_clean:
                            # Buscar línea que termine con patrón x,xxxx
                            match = re.search(r'\b(\d{1,2},\d{4})\s*$', line_clean)
                            if match:
                                try:
                                    valor = float(match.group(1).replace(',', '.'))
                                    if 0.0 <= valor <= 10.0:
                                        puntuaciones_pagina.append(valor)
                                        print(f"        Total (fin línea): {valor:.4f}")
                                except:
                                    pass
                    
            except Exception as e:
                print(f"  Error analizando texto: {e}")
            
            # Eliminar duplicados de esta página
            puntuaciones_pagina_unicas = list(set(puntuaciones_pagina))
            puntuaciones_por_pagina[num_pagina + 1] = puntuaciones_pagina_unicas
            puntuaciones_total.extend(puntuaciones_pagina_unicas)
            
            print(f"  ✅ Puntuaciones Total en esta página: {len(puntuaciones_pagina_unicas)}")
            if len(puntuaciones_pagina_unicas) <= 10:
                print(f"  Valores: {sorted(puntuaciones_pagina_unicas, reverse=True)}")
            
            # VALIDACIÓN: Deberían ser ~7 por página
            if len(puntuaciones_pagina_unicas) > 15:
                print(f"  ⚠️ ADVERTENCIA: Demasiadas puntuaciones ({len(puntuaciones_pagina_unicas)})")
                print(f"     Posiblemente capturando otras columnas")
            elif len(puntuaciones_pagina_unicas) < 3:
                print(f"  ⚠️ ADVERTENCIA: Muy pocas puntuaciones ({len(puntuaciones_pagina_unicas)})")
                print(f"     Posiblemente no capturando todas")
        
        # ANÁLISIS FINAL
        print(f"\n{'='*60}")
        print("=== ANÁLISIS ESPECÍFICO COLUMNA TOTAL ===")
        print(f"{'='*60}")
        
        # Eliminar duplicados globales
        puntuaciones_unicas = list(set(puntuaciones_total))
        
        print(f"Páginas procesadas: {pagina_fin - pagina_inicio}")
        print(f"Total puntuaciones extraídas: {len(puntuaciones_total)}")
        print(f"Puntuaciones únicas: {len(puntuaciones_unicas)}")
        print(f"Promedio por página: {len(puntuaciones_total) / (pagina_fin - pagina_inicio):.1f}")
        
        # Verificar si estamos cerca de los ~7 por página esperados
        esperado_total = (pagina_fin - pagina_inicio) * 7
        if len(puntuaciones_unicas) < esperado_total * 0.5:
            print(f"⚠️ ADVERTENCIA: Solo {len(puntuaciones_unicas)} puntuaciones de ~{esperado_total} esperadas")
            print("   Posiblemente no estamos capturando toda la columna Total")
        elif len(puntuaciones_unicas) > esperado_total * 1.5:
            print(f"⚠️ ADVERTENCIA: {len(puntuaciones_unicas)} puntuaciones, más de ~{esperado_total} esperadas")
            print("   Posiblemente capturando otras columnas además de Total")
        else:
            print(f"✅ Cantidad razonable de puntuaciones para columna Total")
        
        if len(puntuaciones_unicas) >= 10:
            puntuaciones_ordenadas = sorted(puntuaciones_unicas, reverse=True)
            
            print(f"Rango: {min(puntuaciones_unicas):.4f} - {max(puntuaciones_unicas):.4f}")
            print(f"Media: {sum(puntuaciones_unicas)/len(puntuaciones_unicas):.4f}")
            
            # Comparar con muestra conocida
            valores_conocidos = [2.4167, 7.3333, 3.6500, 5.2084, 2.5000, 4.3333, 5.7500, 
                               1.8000, 6.8500, 8.0000, 5.0000, 7.5833, 7.5000, 6.3750,
                               1.9167, 2.2500, 10.0000, 1.0000, 1.7500, 7.0042, 1.0000]
            
            print(f"\n=== VERIFICACIÓN CON MUESTRA CONOCIDA ===")
            coincidencias = 0
            for valor in valores_conocidos:
                if valor in puntuaciones_unicas:
                    coincidencias += 1
            
            print(f"Coincidencias con muestra manual: {coincidencias}/{len(valores_conocidos)}")
            
            if coincidencias >= len(valores_conocidos) * 0.8:
                print("✅ Buena coincidencia - datos probablemente correctos")
            else:
                print("⚠️ Pocas coincidencias - revisar método de extracción")
            
            # GUARDAR SOLO SI PARECE CORRECTO
            if coincidencias >= len(valores_conocidos) * 0.5:
                print(f"\n=== GUARDANDO RESULTADOS VALIDADOS ===")
                
                # Archivo con puntuaciones de columna Total únicamente
                with open('puntuaciones_TOTAL_informatica.txt', 'w') as f:
                    for p in puntuaciones_ordenadas:
                        f.write(f"{p:.4f}\n")
                print("✅ Puntuaciones Total guardadas en 'puntuaciones_TOTAL_informatica.txt'")
                
                # CSV validado
                import pandas as pd
                df = pd.DataFrame({'Puntuacion_Total': puntuaciones_unicas})
                df.to_csv('puntuaciones_TOTAL_informatica.csv', index=False)
                print("✅ CSV validado guardado en 'puntuaciones_TOTAL_informatica.csv'")
                
                print(f"\n🎉 EXTRACCIÓN VALIDADA COMPLETADA")
                print(f"🏆 Puntuación máxima: {max(puntuaciones_unicas):.4f}")
                print(f"📊 Total candidatos: {len(puntuaciones_unicas)}")
                
            else:
                print(f"\n❌ Datos no validados - no se guardan archivos")
                print("Revisar método de extracción")

else:
    print("\n⚠️ No se pueden extraer datos automáticamente")