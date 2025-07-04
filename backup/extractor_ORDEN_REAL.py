import pdfplumber
import re

print("=== EXTRACTOR ORDEN REAL - 343 CANDIDATOS ===")
print("Mantiene el orden exacto del PDF")

with pdfplumber.open("rh03_257_2025_590_12_baremo_prov.pdf") as pdf:
    
    candidatos = []  # Lista ordenada como en el PDF
    
    print("Extrayendo candidatos en orden del PDF...")
    
    for num_pagina in range(2648, 2697):  # 2649 a 2697
        page = pdf.pages[num_pagina]
        
        try:
            texto = page.extract_text()
            if texto:
                lineas = texto.split('\n')
                
                for linea in lineas:
                    if linea.startswith('****') and '*' in linea[4:]:
                        numeros = re.findall(r'\b(\d{1,2},\d{4})\b', linea)
                        
                        if numeros:
                            primer_numero = numeros[0]
                            try:
                                valor = float(primer_numero.replace(',', '.'))
                                if 0.0 <= valor <= 10.0:
                                    candidatos.append(valor)
                                    print(f"{len(candidatos):3d}. {valor:.4f}")
                            except:
                                pass
        
        except Exception as e:
            print(f"Error página {num_pagina + 1}: {e}")
    
    # GUARDAR EN ORDEN REAL
    print(f"\n{'='*50}")
    print("=== GUARDANDO LISTA ORDENADA ===")
    print(f"{'='*50}")
    
    print(f"Total candidatos: {len(candidatos)}")
    
    # TXT con orden del PDF
    with open('INFORMATICA_107_ORDEN_PDF.txt', 'w') as f:
        for i, puntuacion in enumerate(candidatos):
            f.write(f"{i+1:3d}. {puntuacion:.4f}\n")
    print("💾 Guardado: INFORMATICA_107_ORDEN_PDF.txt")
    
    # CSV con orden del PDF
    with open('INFORMATICA_107_ORDEN_PDF.csv', 'w') as f:
        f.write("Posicion,Puntuacion_Total\n")
        for i, puntuacion in enumerate(candidatos):
            f.write(f"{i+1},{puntuacion:.4f}\n")
    print("💾 Guardado: INFORMATICA_107_ORDEN_PDF.csv")
    
    # Lista Python directa
    with open('lista_informatica_107.py', 'w') as f:
        f.write("# Lista completa Informática 107 - ORDEN DEL PDF\n")
        f.write(f"# Total: {len(candidatos)} candidatos\n\n")
        f.write("puntuaciones_informatica = [\n")
        for i, puntuacion in enumerate(candidatos):
            f.write(f"    {puntuacion:.4f},  # {i+1:3d}\n")
        f.write("]\n")
    print("💾 Guardado: lista_informatica_107.py")
    
    # ESTADÍSTICAS SIN ALTERAR EL ORDEN
    print(f"\n=== ESTADÍSTICAS (SIN CAMBIAR ORDEN) ===")
    print(f"📊 Total candidatos: {len(candidatos)}")
    print(f"🏆 Puntuación máxima: {max(candidatos):.4f}")
    print(f"📉 Puntuación mínima: {min(candidatos):.4f}")
    print(f"📈 Media: {sum(candidatos)/len(candidatos):.4f}")
    
    # Contar valores únicos SIN alterar la lista
    valores_unicos = len(set(candidatos))
    print(f"🎯 Puntuaciones diferentes: {valores_unicos}")
    print(f"🔄 Candidatos con misma nota: {len(candidatos) - valores_unicos}")
    
    # Primeros y últimos 10
    print(f"\n=== PRIMEROS 10 (orden PDF) ===")
    for i in range(min(10, len(candidatos))):
        print(f"{i+1:3d}. {candidatos[i]:.4f}")
    
    print(f"\n=== ÚLTIMOS 10 (orden PDF) ===")
    inicio = max(0, len(candidatos) - 10)
    for i in range(inicio, len(candidatos)):
        print(f"{i+1:3d}. {candidatos[i]:.4f}")
    
    print(f"\n🎉 ¡EXTRACCIÓN COMPLETA!")
    print(f"✅ {len(candidatos)} candidatos en orden del PDF")
    print(f"📁 Archivos con orden REAL generados")

print("\n📋 CANDIDATOS EN ORDEN DEL PDF - SIN MODIFICACIONES")