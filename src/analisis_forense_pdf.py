import pdfplumber
import re

print("=== ANÁLISIS FORENSE DEL PDF ===")
print("Analizando estructura real de las páginas de Informática...")

with pdfplumber.open("rh03_257_2025_590_12_baremo_prov.pdf") as pdf:
    
    # Analizar las primeras 3 páginas que conocemos (2649, 2650, 2651)
    paginas_test = [2648, 2649, 2650]  # índices 0-based
    
    for i, num_pagina in enumerate(paginas_test):
        page = pdf.pages[num_pagina]
        print(f"\n{'='*60}")
        print(f"PÁGINA {num_pagina + 1} (conocemos: página {2649 + i})")
        print(f"{'='*60}")
        
        # 1. ANÁLISIS DE TABLAS
        print("\n1. ESTRUCTURA DE TABLAS:")
        tables = page.extract_tables()
        print(f"   Número de tablas: {len(tables)}")
        
        for j, table in enumerate(tables):
            if table:
                print(f"\n   Tabla {j+1}:")
                print(f"     Filas: {len(table)}")
                print(f"     Columnas: {len(table[0]) if table else 0}")
                
                # Mostrar primera fila (headers)
                if table and len(table) > 0:
                    print(f"     Header: {table[0]}")
                
                # Mostrar primeras 2 filas de datos
                for row_idx in range(min(3, len(table))):
                    if table[row_idx]:
                        print(f"     Fila {row_idx}: {table[row_idx]}")
        
        # 2. ANÁLISIS DE TEXTO CRUDO
        print(f"\n2. TEXTO CRUDO (primeras 20 líneas):")
        texto = page.extract_text()
        if texto:
            lineas = texto.split('\n')
            for idx, linea in enumerate(lineas[:20]):
                if linea.strip():
                    print(f"   {idx+1:2d}: {linea}")
        
        # 3. BÚSQUEDA DE PATRONES NUMÉRICOS
        print(f"\n3. PATRONES NUMÉRICOS ENCONTRADOS:")
        if texto:
            # Buscar todos los números x,xxxx
            numeros = re.findall(r'\b(\d{1,2},\d{4})\b', texto)
            print(f"   Números formato x,xxxx: {len(numeros)}")
            if numeros:
                print(f"   Primeros 10: {numeros[:10]}")
                print(f"   Últimos 10: {numeros[-10:]}")
        
        # 4. BÚSQUEDA DE LÍNEAS CON DNI
        print(f"\n4. LÍNEAS CON DNI (asteriscos):")
        if texto:
            lineas_dni = [linea for linea in texto.split('\n') if '****' in linea]
            print(f"   Líneas con DNI: {len(lineas_dni)}")
            for idx, linea in enumerate(lineas_dni[:3]):
                print(f"   DNI {idx+1}: {linea}")
                # Extraer números de esta línea
                nums_en_linea = re.findall(r'\b(\d{1,2},\d{4})\b', linea)
                print(f"           Números: {nums_en_linea}")
        
        # 5. COORDENADAS Y POSICIONAMIENTO
        print(f"\n5. ANÁLISIS DE COORDENADAS:")
        chars = page.chars
        if chars:
            # Buscar caracteres que forman números conocidos
            valores_conocidos = ['2,4167', '7,3333', '3,6500'] if i == 0 else \
                              ['1,8000', '6,8500', '8,0000'] if i == 1 else \
                              ['1,9167', '2,2500', '10,0000']
            
            for valor in valores_conocidos:
                print(f"   Buscando '{valor}':")
                posiciones = []
                for char in chars:
                    if valor.replace(',', '.') in str(char.get('text', '')):
                        posiciones.append((char.get('x0'), char.get('y0')))
                
                if posiciones:
                    print(f"     Encontrado en posiciones: {posiciones[:3]}")
    
    # 6. ANÁLISIS COMPARATIVO
    print(f"\n{'='*60}")
    print("6. ANÁLISIS COMPARATIVO ENTRE PÁGINAS")
    print(f"{'='*60}")
    
    # Comparar estructuras
    for i, num_pagina in enumerate(paginas_test):
        page = pdf.pages[num_pagina]
        tables = page.extract_tables()
        texto = page.extract_text()
        
        lineas_dni = len([l for l in texto.split('\n') if '****' in l]) if texto else 0
        numeros_total = len(re.findall(r'\b(\d{1,2},\d{4})\b', texto)) if texto else 0
        
        print(f"Página {num_pagina + 1}: {len(tables)} tablas, {lineas_dni} DNIs, {numeros_total} números")

print(f"\n{'='*60}")
print("7. ESTRATEGIA BASADA EN ANÁLISIS")
print(f"{'='*60}")
print("Basándome en este análisis, implementaré el extractor óptimo...")