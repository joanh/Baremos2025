import re

print("=== EXTRACTOR SIMPLE COLUMNA TOTAL ===")
print()
print("INSTRUCCIONES:")
print("1. Abre el PDF en páginas 2650-2697")
print("2. Selecciona SOLO la columna 'Total' de cada página")
print("3. Copia y pega aquí los valores")
print("4. Presiona Enter después de cada valor")
print("5. Escribe 'FIN' cuando termines")
print()
print("Formato esperado: x,xxxx (ejemplo: 7,3333)")
print("-" * 50)

puntuaciones_total = []
pagina_actual = 2650
contador_pagina = 0

while True:
    try:
        entrada = input(f"Valor {len(puntuaciones_total) + 1}: ")
        
        if entrada.upper() == 'FIN':
            break
        
        if entrada.upper() == 'PAGINA':
            pagina_actual += 1
            contador_pagina = 0
            print(f"\n--- PÁGINA {pagina_actual} ---")
            continue
        
        # Limpiar entrada
        entrada = entrada.strip().replace(' ', '').replace('\t', '')
        
        # Buscar patrón de puntuación
        match = re.match(r'^(\d{1,2}[,\.]\d{1,4})$', entrada)
        
        if match:
            # Normalizar formato
            puntuacion_str = match.group(1).replace(',', '.')
            puntuacion = float(puntuacion_str)
            
            if 0.0 <= puntuacion <= 10.0:
                puntuaciones_total.append(puntuacion)
                contador_pagina += 1
                print(f"✅ {puntuacion:.4f} (Total: {len(puntuaciones_total)}, Página: {contador_pagina})")
                
                # Aviso cada 7 valores (página completa)
                if contador_pagina == 7:
                    print(f"🎯 Página {pagina_actual} completa (7 valores)")
                    print("Escribe 'PAGINA' para siguiente página o continúa...")
                    
            else:
                print(f"❌ Valor fuera de rango (0-10): {puntuacion}")
        else:
            print(f"❌ Formato inválido. Usa: x,xxxx")
            print("Ejemplos válidos: 7,3333  2,4167  10,0000")
            
    except KeyboardInterrupt:
        print("\n⏹️ Proceso cancelado")
        break
    except Exception as e:
        print(f"❌ Error: {e}")

# ANÁLISIS DE LOS DATOS REALES
if puntuaciones_total:
    print(f"\n{'='*60}")
    print("=== ANÁLISIS DE DATOS REALES ===")
    print(f"{'='*60}")
    
    print(f"Total puntuaciones: {len(puntuaciones_total)}")
    print(f"Rango: {min(puntuaciones_total):.4f} - {max(puntuaciones_total):.4f}")
    
    if len(puntuaciones_total) >= 5:
        import statistics
        print(f"Media: {statistics.mean(puntuaciones_total):.4f}")
        print(f"Mediana: {statistics.median(puntuaciones_total):.4f}")
        
        # Valores altos
        print(f"\n=== VALORES ALTOS ===")
        for umbral in [8.0, 9.0, 9.5, 10.0]:
            altos = [p for p in puntuaciones_total if p >= umbral]
            porcentaje = (len(altos) / len(puntuaciones_total)) * 100
            print(f">= {umbral}: {len(altos)} ({porcentaje:.1f}%)")
            if altos and len(altos) <= 10:
                print(f"   Valores: {sorted(set(altos), reverse=True)}")
        
        # Distribución
        print(f"\n=== DISTRIBUCIÓN ===")
        rangos = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 11)]
        for min_r, max_r in rangos:
            count = sum(1 for p in puntuaciones_total if min_r <= p < max_r)
            if count > 0:
                porcentaje = (count / len(puntuaciones_total)) * 100
                print(f"{min_r}-{max_r}: {count:3d} ({porcentaje:5.1f}%)")
    
    # GUARDAR DATOS
    print(f"\n=== GUARDANDO DATOS REALES ===")
    
    # Archivo TXT ordenado
    puntuaciones_ordenadas = sorted(puntuaciones_total, reverse=True)
    with open('puntuaciones_REALES_manual.txt', 'w') as f:
        for p in puntuaciones_ordenadas:
            f.write(f"{p:.4f}\n")
    print("✅ Datos guardados en 'puntuaciones_REALES_manual.txt'")
    
    # CSV
    try:
        import pandas as pd
        df = pd.DataFrame({'Puntuacion_Total': puntuaciones_total})
        df.to_csv('puntuaciones_REALES_manual.csv', index=False)
        print("✅ CSV guardado en 'puntuaciones_REALES_manual.csv'")
    except ImportError:
        # CSV manual si no hay pandas
        with open('puntuaciones_REALES_manual.csv', 'w') as f:
            f.write("Puntuacion_Total\n")
            for p in puntuaciones_total:
                f.write(f"{p:.4f}\n")
        print("✅ CSV manual guardado en 'puntuaciones_REALES_manual.csv'")
    
    # Código Python para usar directamente
    codigo = "# Puntuaciones REALES Informática 107\n"
    codigo += "puntuaciones_reales = [\n"
    for i, p in enumerate(puntuaciones_ordenadas):
        if i % 10 == 0 and i > 0:
            codigo += "\n"
        codigo += f"    {p:.4f},"
    codigo = codigo.rstrip(',') + "\n]"
    
    with open('codigo_puntuaciones_reales.py', 'w') as f:
        f.write(codigo)
    print("✅ Código Python en 'codigo_puntuaciones_reales.py'")
    
    # TOP 20
    if len(puntuaciones_total) >= 20:
        print(f"\n=== TOP 20 ===")
        for i, p in enumerate(puntuaciones_ordenadas[:20]):
            print(f"{i+1:2d}. {p:.4f}")
    
    print(f"\n🎉 DATOS REALES PROCESADOS")
    print(f"🏆 Máximo: {max(puntuaciones_total):.4f}")
    print(f"📊 Total: {len(puntuaciones_total)} candidatos")
    
    # Estimación de progreso
    if len(puntuaciones_total) < 300:
        restantes = 320 - len(puntuaciones_total)  # Estimado total
        print(f"📋 Faltan ~{restantes} valores por extraer")
    
else:
    print("❌ No se introdujeron datos")

print("\n" + "="*60)
print("Archivos generados:")
print("- puntuaciones_REALES_manual.txt")
print("- puntuaciones_REALES_manual.csv") 
print("- codigo_puntuaciones_reales.py")