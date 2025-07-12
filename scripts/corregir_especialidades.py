#!/usr/bin/env python3
"""
Script de corrección para especialidades con rangos incorrectos
Corrige las puntuaciones > 10.0 y regenera estadísticas y visualizaciones
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os
import sys

def corregir_puntuaciones(puntuaciones):
    """Corrige puntuaciones limitándolas al rango 0.0-10.0"""
    puntuaciones_corregidas = np.array(puntuaciones)
    
    # Limitar al rango válido
    puntuaciones_corregidas = np.clip(puntuaciones_corregidas, 0.0, 10.0)
    
    return puntuaciones_corregidas.tolist()

def generar_estadisticas(puntuaciones, nombre_especialidad):
    """Genera estadísticas descriptivas"""
    puntuaciones = np.array(puntuaciones)
    
    estadisticas = {
        'total_candidatos': len(puntuaciones),
        'media': np.mean(puntuaciones),
        'mediana': np.median(puntuaciones),
        'desviacion': np.std(puntuaciones),
        'minimo': np.min(puntuaciones),
        'maximo': np.max(puntuaciones),
        'q1': np.percentile(puntuaciones, 25),
        'q3': np.percentile(puntuaciones, 75)
    }
    
    print(f"\n📊 {nombre_especialidad} - Estadísticas Corregidas:")
    print(f"• Candidatos: {estadisticas['total_candidatos']:,}")
    print(f"• Media: {estadisticas['media']:.2f} puntos")
    print(f"• Mediana: {estadisticas['mediana']:.2f} puntos")
    print(f"• Desviación estándar: {estadisticas['desviacion']:.2f}")
    print(f"• Rango: {estadisticas['minimo']:.2f} - {estadisticas['maximo']:.2f} puntos")
    
    return estadisticas

def generar_visualizacion(puntuaciones, nombre_especialidad, codigo, output_dir):
    """Genera la visualización corregida"""
    
    # Configurar estilo
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Crear figura con subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle(f'Análisis de Puntuaciones - {nombre_especialidad} ({codigo})', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Histograma con curva normal
    ax1.hist(puntuaciones, bins=20, density=True, alpha=0.7, color='skyblue', edgecolor='black')
    
    # Curva normal teórica
    mu, sigma = np.mean(puntuaciones), np.std(puntuaciones)
    x = np.linspace(0, 10, 100)
    y = ((1/(sigma * np.sqrt(2*np.pi))) * np.exp(-0.5*((x-mu)/sigma)**2))
    ax1.plot(x, y, 'r-', linewidth=2, label=f'Normal (μ={mu:.2f}, σ={sigma:.2f})')
    
    ax1.set_xlabel('Puntuación')
    ax1.set_ylabel('Densidad')
    ax1.set_title('Distribución de Puntuaciones')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 10)
    
    # Gráfico de barras por rangos
    rangos = ['0-2', '2-4', '4-6', '6-8', '8-10']
    conteos = [
        sum(1 for p in puntuaciones if 0 <= p < 2),
        sum(1 for p in puntuaciones if 2 <= p < 4),
        sum(1 for p in puntuaciones if 4 <= p < 6),
        sum(1 for p in puntuaciones if 6 <= p < 8),
        sum(1 for p in puntuaciones if 8 <= p <= 10)
    ]
    
    colores = ['#ff7f7f', '#ffbf7f', '#ffff7f', '#7fff7f', '#7f7fff']
    bars = ax2.bar(rangos, conteos, color=colores, edgecolor='black', alpha=0.8)
    
    # Añadir valores en las barras
    for bar, count in zip(bars, conteos):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + len(puntuaciones)*0.01,
                f'{count}\n({count/len(puntuaciones)*100:.1f}%)',
                ha='center', va='bottom', fontweight='bold')
    
    ax2.set_xlabel('Rango de Puntuaciones')
    ax2.set_ylabel('Número de Candidatos')
    ax2.set_title('Distribución por Rangos')
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    # Guardar imagen
    output_path = output_dir / f"baremo_{nombre_especialidad.lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')}_{codigo}_2025.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Visualización guardada: {output_path}")
    
    # También guardar en img/ del proyecto principal
    img_dir = Path(__file__).parent.parent / "img"
    img_dir.mkdir(exist_ok=True)
    img_path = img_dir / f"baremo_{nombre_especialidad.lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')}_{codigo}_2025.png"
    plt.savefig(img_path, dpi=300, bbox_inches='tight')
    
    plt.close()

def corregir_especialidad(especialidad_dir, nombre_especialidad, codigo):
    """Corrige una especialidad completa"""
    
    print(f"\n🔧 Corrigiendo {nombre_especialidad} ({codigo})...")
    
    # Buscar archivo de puntuaciones
    output_dir = especialidad_dir / "output"
    
    # Buscar archivos CSV con puntuaciones
    csv_files = list(output_dir.glob("*.csv"))
    
    if not csv_files:
        print(f"❌ No se encontraron archivos CSV en {output_dir}")
        return False
    
    # Tomar el archivo más probable (buscar el que tenga "puntuaciones" en el nombre)
    puntuaciones_file = None
    for csv_file in csv_files:
        if 'puntuaciones' in csv_file.name.lower():
            puntuaciones_file = csv_file
            break
    
    if not puntuaciones_file:
        puntuaciones_file = csv_files[0]  # Tomar el primero si no encuentra ninguno específico
    
    print(f"📁 Procesando archivo: {puntuaciones_file}")
    
    # Leer puntuaciones
    try:
        df = pd.read_csv(puntuaciones_file)
        
        # Buscar columna de puntuaciones (puede tener diferentes nombres)
        puntuacion_col = None
        for col in df.columns:
            if any(keyword in col.lower() for keyword in ['puntuacion', 'total', 'nota']):
                puntuacion_col = col
                break
        
        if puntuacion_col is None:
            # Si no encuentra por nombre, usar la última columna (suele ser la puntuación)
            puntuacion_col = df.columns[-1]
        
        print(f"📊 Usando columna: {puntuacion_col}")
        
        puntuaciones_originales = df[puntuacion_col].tolist()
        print(f"📈 Puntuaciones originales: {len(puntuaciones_originales)} candidatos")
        print(f"📊 Rango original: {min(puntuaciones_originales):.2f} - {max(puntuaciones_originales):.2f}")
        
        # Corregir puntuaciones
        puntuaciones_corregidas = corregir_puntuaciones(puntuaciones_originales)
        
        # Contar cuántas se corrigieron
        valores_corregidos = sum(1 for orig, corr in zip(puntuaciones_originales, puntuaciones_corregidas) if orig != corr)
        print(f"🔧 Valores corregidos: {valores_corregidos}")
        
        # Actualizar DataFrame
        df[puntuacion_col] = puntuaciones_corregidas
        
        # Guardar CSV corregido
        csv_corregido = output_dir / f"puntuaciones_{nombre_especialidad.lower().replace(' ', '_')}_{codigo}_corregidas.csv"
        df.to_csv(csv_corregido, index=False)
        print(f"💾 CSV corregido guardado: {csv_corregido}")
        
        # Generar estadísticas
        estadisticas = generar_estadisticas(puntuaciones_corregidas, nombre_especialidad)
        
        # Generar visualización
        generar_visualizacion(puntuaciones_corregidas, nombre_especialidad, codigo, output_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Error procesando {puntuaciones_file}: {e}")
        return False

def main():
    """Función principal"""
    
    print("🚀 Iniciando corrección de especialidades con rangos incorrectos...")
    
    # Especialidades a corregir
    especialidades = [
        ("lengua_literatura_004", "Lengua y Literatura", "004"),
        ("matematicas_006", "Matemáticas", "006"),
        ("fisica_quimica_007", "Física y Química", "007"),
        ("informatica_107", "Informática", "107")
    ]
    
    especialidades_dir = Path(__file__).parent.parent / "especialidades"
    
    resultados = []
    
    for dir_name, nombre, codigo in especialidades:
        especialidad_dir = especialidades_dir / dir_name
        
        if not especialidad_dir.exists():
            print(f"❌ No existe directorio: {especialidad_dir}")
            resultados.append(False)
            continue
        
        resultado = corregir_especialidad(especialidad_dir, nombre, codigo)
        resultados.append(resultado)
    
    # Resumen final
    print(f"\n📋 Resumen de correcciones:")
    for i, (dir_name, nombre, codigo) in enumerate(especialidades):
        estado = "✅ Completado" if resultados[i] else "❌ Falló"
        print(f"• {nombre} ({codigo}): {estado}")
    
    exitosos = sum(resultados)
    print(f"\n🎯 Total: {exitosos}/{len(especialidades)} especialidades corregidas")
    
    if exitosos == len(especialidades):
        print("\n🎉 ¡Todas las especialidades han sido corregidas exitosamente!")
        print("📝 Recuerda actualizar los README de cada especialidad con las nuevas estadísticas.")
    else:
        print("\n⚠️  Algunas especialidades requieren revisión manual.")

if __name__ == "__main__":
    main()
