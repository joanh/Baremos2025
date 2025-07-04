import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import requests
import PyPDF2
import io
import re

print("Descargando y procesando el PDF...")

try:
    # Descargar el PDF
    url = "https://www.comunidad.madrid/sites/default/files/doc/educacion/rh03/rh03_257_2025_590_12_baremo_prov.pdf"
    response = requests.get(url)
    pdf_file = io.BytesIO(response.content)

    # Leer el PDF y extraer texto
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    print("PDF descargado correctamente.")

    # Buscar la sección de INFORMÁTICA (especialidad 107)
    informatica_section = re.search(r'ESPECIALIDAD: 107 - INFORMATICA.*?(?=ESPECIALIDAD:|CUERPO:|$)', text, re.DOTALL)

    if informatica_section:
        section_text = informatica_section.group(0)
        print("Sección de Informática encontrada.")
        
        # Extraer líneas con datos de candidatos
        lines = section_text.split('\n')
        datos = []
        
        for line in lines:
            # Buscar líneas que contengan puntuaciones
            if re.search(r'\d{8}[A-Z]\s+.*?\s+\d+[.,]\d+\s+\d+[.,]\d+\s+\d+[.,]\d+', line):
                parts = line.strip().split()
                if len(parts) >= 3:
                    try:
                        # La puntuación total suele ser la última columna numérica
                        total = float(parts[-1].replace(',', '.'))
                        nombre_completo = ' '.join(parts[1:-3])  # Nombre entre DNI y puntuaciones
                        datos.append({
                            'DNI': parts[0],
                            'Nombre': nombre_completo,
                            'Puntuacion_Total': total
                        })
                    except Exception as e:
                        continue

        # Crear DataFrame
        df = pd.DataFrame(datos)
        
        if len(df) > 0:
            print(f"\n=== DATOS EXTRAÍDOS ===")
            print(f"Total candidatos: {len(df)}")
            
            # Guardar CSV
            df.to_csv('baremos_informatica_107.csv', index=False, encoding='utf-8')
            print("✅ Datos guardados en 'baremos_informatica_107.csv'")
            
            # Mostrar primeros registros
            print("\n=== PRIMEROS 5 CANDIDATOS ===")
            print(df.head().to_string(index=False))
            
            # Buscar a José Ángel Heras
            heras = df[df['Nombre'].str.contains('HERAS.*JOSE.*ANGEL', case=False, na=False)]
            if len(heras) > 0:
                print(f"\n🎯 ¡ENCONTRADO! {heras.iloc[0]['Nombre']}")
                print(f"Puntuación: {heras.iloc[0]['Puntuacion_Total']}")
            else:
                print("\n❌ No se encontró a José Ángel Heras")
                # Buscar solo por HERAS
                solo_heras = df[df['Nombre'].str.contains('HERAS', case=False, na=False)]
                if len(solo_heras) > 0:
                    print("Candidatos con apellido HERAS encontrados:")
                    print(solo_heras[['Nombre', 'Puntuacion_Total']].to_string(index=False))
            
            # Estadísticas básicas
            puntuaciones = df['Puntuacion_Total']
            print(f"\n=== ESTADÍSTICAS BÁSICAS ===")
            print(f"Puntuación máxima: {puntuaciones.max():.3f}")
            print(f"Puntuación mínima: {puntuaciones.min():.3f}")
            print(f"Media: {puntuaciones.mean():.3f}")
            print(f"Mediana: {puntuaciones.median():.3f}")
            print(f"Desviación estándar: {puntuaciones.std():.3f}")
            
            # Distribución de frecuencias
            print(f"\n=== DISTRIBUCIÓN DE FRECUENCIAS ===")
            bins = np.arange(0, puntuaciones.max() + 0.5, 0.5)
            hist, bin_edges = np.histogram(puntuaciones, bins=bins)
            
            freq_df = pd.DataFrame({
                'Rango': [f"{bin_edges[i]:.1f}-{bin_edges[i+1]:.1f}" for i in range(len(hist))],
                'Frecuencia': hist,
                'Porcentaje': (hist / len(puntuaciones) * 100).round(1)
            })
            freq_df = freq_df[freq_df['Frecuencia'] > 0]  # Solo rangos con datos
            print(freq_df.to_string(index=False))
            
            # Posición de José Ángel (1.850)
            tu_puntuacion = 1.850
            mejor_que = (puntuaciones < tu_puntuacion).sum()
            percentil = (mejor_que / len(puntuaciones)) * 100
            posicion = len(puntuaciones) - mejor_que
            
            print(f"\n=== TU POSICIÓN (puntuación: {tu_puntuacion}) ===")
            print(f"Posición: {posicion} de {len(puntuaciones)}")
            print(f"Mejor que {mejor_que} candidatos ({percentil:.1f}%)")
            print(f"Percentil: {percentil:.1f}")
            
            # Generar curva gaussiana
            plt.figure(figsize=(12, 8))
            
            # Histograma
            plt.subplot(2, 1, 1)
            plt.hist(puntuaciones, bins=20, alpha=0.7, color='lightblue', edgecolor='black')
            plt.axvline(tu_puntuacion, color='red', linestyle='--', linewidth=2, label=f'Tu puntuación: {tu_puntuacion}')
            plt.axvline(puntuaciones.mean(), color='green', linestyle='-', linewidth=2, label=f'Media: {puntuaciones.mean():.3f}')
            plt.xlabel('Puntuación Total')
            plt.ylabel('Frecuencia')
            plt.title('Distribución de Puntuaciones - Informática (Especialidad 107)')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Curva gaussiana
            plt.subplot(2, 1, 2)
            x = np.linspace(puntuaciones.min(), puntuaciones.max(), 100)
            y = stats.norm.pdf(x, puntuaciones.mean(), puntuaciones.std())
            plt.plot(x, y, 'b-', linewidth=2, label='Distribución normal')
            plt.axvline(tu_puntuacion, color='red', linestyle='--', linewidth=2, label=f'Tu puntuación: {tu_puntuacion}')
            plt.axvline(puntuaciones.mean(), color='green', linestyle='-', linewidth=2, label=f'Media: {puntuaciones.mean():.3f}')
            plt.xlabel('Puntuación Total')
            plt.ylabel('Densidad de Probabilidad')
            plt.title('Curva Gaussiana de Puntuaciones')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('distribucion_informatica_107.png', dpi=300, bbox_inches='tight')
            print("\n✅ Gráfico guardado como 'distribucion_informatica_107.png'")
            
            # Guardar estadísticas en archivo
            with open('estadisticas_informatica_107.txt', 'w', encoding='utf-8') as f:
                f.write("=== ANÁLISIS BAREMO INFORMÁTICA 107 ===\n")
                f.write(f"Total candidatos: {len(df)}\n")
                f.write(f"Puntuación máxima: {puntuaciones.max():.3f}\n")
                f.write(f"Puntuación mínima: {puntuaciones.min():.3f}\n")
                f.write(f"Media: {puntuaciones.mean():.3f}\n")
                f.write(f"Mediana: {puntuaciones.median():.3f}\n")
                f.write(f"Desviación estándar: {puntuaciones.std():.3f}\n\n")
                f.write(f"=== POSICIÓN JOSÉ ÁNGEL HERAS (1.850) ===\n")
                f.write(f"Posición: {posicion} de {len(puntuaciones)}\n")
                f.write(f"Percentil: {percentil:.1f}\n")
                f.write(f"Mejor que {mejor_que} candidatos ({percentil:.1f}%)\n")
            
            print("✅ Estadísticas guardadas en 'estadisticas_informatica_107.txt'")
            print("\n🎉 ANÁLISIS COMPLETADO")
            
        else:
            print("❌ No se pudieron extraer datos.")
            print("Mostrando muestra del texto encontrado:")
            print(section_text[:500])
    else:
        print("❌ No se encontró la sección de Informática en el PDF")

except Exception as e:
    print(f"❌ Error: {e}")