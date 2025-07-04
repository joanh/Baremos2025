#!/usr/bin/env python3
"""
Extractor de puntuaciones para Lengua Castellana y Literatura (011) - Baremo 2025
Procesa páginas 2-10 del PDF oficial del baremo provisional
"""

import sys
import os
import yaml
import pandas as pd
import pdfplumber
import re
from pathlib import Path

def cargar_configuracion():
    """Carga la configuración desde config.yaml"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def extraer_puntuaciones_pagina(page):
    """Extrae puntuaciones de una página usando múltiples métodos"""
    puntuaciones = []
    
    try:
        # Método 1: Extraer texto completo y buscar puntuaciones
        text = page.extract_text()
        if text:
            # Buscar todas las puntuaciones válidas con formato decimal
            matches = re.findall(r'\b\d+[,\.]\d{4}\b', text)
            for match in matches:
                try:
                    puntuacion = float(match.replace(',', '.'))
                    if 0.0 <= puntuacion <= 10.0:
                        puntuaciones.append(puntuacion)
                except ValueError:
                    continue
        
        # Método 2: Extraer tablas si existen
        if not puntuaciones:
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    for row in table:
                        if row and len(row) > 0:
                            # Buscar en todas las celdas
                            for cell in row:
                                if cell and isinstance(cell, str):
                                    matches = re.findall(r'\b\d+[,\.]\d{4}\b', cell)
                                    for match in matches:
                                        try:
                                            puntuacion = float(match.replace(',', '.'))
                                            if 0.0 <= puntuacion <= 10.0:
                                                puntuaciones.append(puntuacion)
                                        except ValueError:
                                            continue
                            
    except Exception as e:
        print(f"Error procesando página: {e}")
    
    return puntuaciones

def validar_pagina(puntuaciones_extraidas, puntuaciones_esperadas, numero_pagina):
    """Valida que las puntuaciones extraídas coincidan con las esperadas"""
    coincidencias = 0
    total_esperadas = len(puntuaciones_esperadas)
    
    print(f"\n=== VALIDACIÓN PÁGINA {numero_pagina} ===")
    print(f"Puntuaciones esperadas: {puntuaciones_esperadas}")
    print(f"Puntuaciones extraídas (primeras {len(puntuaciones_esperadas)}): {puntuaciones_extraidas[:len(puntuaciones_esperadas)]}")
    
    for i, esperada in enumerate(puntuaciones_esperadas):
        if i < len(puntuaciones_extraidas):
            extraida = puntuaciones_extraidas[i]
            if abs(extraida - esperada) < 0.0001:
                coincidencias += 1
                print(f"✓ Posición {i+1}: {extraida} == {esperada}")
            else:
                print(f"✗ Posición {i+1}: {extraida} != {esperada}")
        else:
            print(f"✗ Posición {i+1}: No encontrada")
    
    porcentaje = (coincidencias / total_esperadas) * 100
    print(f"Resultado: {coincidencias}/{total_esperadas} coincidencias ({porcentaje:.1f}%)")
    
    return porcentaje >= 50.0  # Consideramos válido si coincide al menos el 50%

def main():
    """Función principal de extracción"""
    print("🎭 EXTRACTOR LENGUA CASTELLANA Y LITERATURA (011) - BAREMO 2025")
    print("=" * 70)
    
    # Cargar configuración
    config = cargar_configuracion()
    
    # Configurar rutas
    pdf_path = Path(__file__).parent.parent / config['pdf']['archivo']
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    print(f"📄 PDF: {pdf_path}")
    print(f"📊 Páginas: {config['pdf']['pagina_inicio']}-{config['pdf']['pagina_fin']}")
    print(f"📁 Salida: {output_dir}")
    
    if not pdf_path.exists():
        print(f"❌ ERROR: No se encuentra el PDF en {pdf_path}")
        return False
    
    todas_puntuaciones = []
    paginas_procesadas = 0
    errores = 0
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"\n📖 Procesando PDF... Total páginas: {len(pdf.pages)}")
            
            for i in range(config['pdf']['pagina_inicio'] - 1, config['pdf']['pagina_fin']):
                if i >= len(pdf.pages):
                    print(f"⚠️ Página {i+1} fuera de rango")
                    break
                
                pagina_actual = i + 1
                puntuaciones_pagina = extraer_puntuaciones_pagina(pdf.pages[i])
                
                if puntuaciones_pagina:
                    todas_puntuaciones.extend(puntuaciones_pagina)
                    print(f"📄 Página {pagina_actual}: {len(puntuaciones_pagina)} puntuaciones")
                    
                    # Validar páginas clave
                    if pagina_actual == config['validacion']['pagina_inicial']['numero']:
                        validar_pagina(
                            puntuaciones_pagina,
                            config['validacion']['pagina_inicial']['puntuaciones_esperadas'],
                            pagina_actual
                        )
                    elif pagina_actual == config['validacion']['pagina_final']['numero']:
                        validar_pagina(
                            puntuaciones_pagina,
                            config['validacion']['pagina_final']['puntuaciones_esperadas'],
                            pagina_actual
                        )
                        
                    paginas_procesadas += 1
                else:
                    errores += 1
                    if errores <= 5:  # Solo mostrar los primeros 5 errores
                        print(f"❌ Página {pagina_actual}: Sin puntuaciones")
    
    except Exception as e:
        print(f"❌ ERROR procesando PDF: {e}")
        return False
    
    print(f"\n📊 RESUMEN DE EXTRACCIÓN")
    print("=" * 50)
    print(f"Total candidatos encontrados: {len(todas_puntuaciones)}")
    print(f"Páginas procesadas: {paginas_procesadas}")
    print(f"Páginas con errores: {errores}")
    
    if not todas_puntuaciones:
        print("❌ No se encontraron puntuaciones válidas")
        return False
    
    # Estadísticas básicas
    df = pd.DataFrame({'Total': todas_puntuaciones})
    print(f"\n📈 ESTADÍSTICAS")
    print("-" * 30)
    print(f"Puntuación máxima: {df['Total'].max():.4f}")
    print(f"Puntuación mínima: {df['Total'].min():.4f}")
    print(f"Puntuación media: {df['Total'].mean():.4f}")
    print(f"Desviación estándar: {df['Total'].std():.4f}")
    
    # Guardar resultados
    try:
        # CSV
        csv_path = output_dir / "puntuaciones_lengua_literatura_011.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"✅ CSV guardado: {csv_path}")
        
        # TXT (lista legible)
        txt_path = output_dir / "puntuaciones_lengua_literatura_011.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("# Puntuaciones Lengua Castellana y Literatura (011) - Baremo 2025\n")
            f.write(f"# Total candidatos: {len(todas_puntuaciones)}\n\n")
            for i, puntuacion in enumerate(todas_puntuaciones, 1):
                f.write(f"{i:4d}: {puntuacion:.4f}\n")
        print(f"✅ TXT guardado: {txt_path}")
        
        # Python array
        py_path = output_dir / "lista_lengua_literatura_011.py"
        with open(py_path, 'w', encoding='utf-8') as f:
            f.write("#!/usr/bin/env python3\n")
            f.write('"""\n')
            f.write("Puntuaciones de Lengua Castellana y Literatura (011) - Baremo 2025\n")
            f.write(f"Total candidatos: {len(todas_puntuaciones)}\n")
            f.write('"""\n\n')
            f.write("puntuaciones_lengua_literatura_011 = [\n")
            for puntuacion in todas_puntuaciones:
                f.write(f"    {puntuacion:.4f},\n")
            f.write("]\n")
        print(f"✅ Python guardado: {py_path}")
        
        # Estadísticas detalladas
        stats_path = output_dir / "estadisticas_lengua_literatura_011.txt"
        with open(stats_path, 'w', encoding='utf-8') as f:
            f.write("ESTADÍSTICAS LENGUA CASTELLANA Y LITERATURA (011) - BAREMO 2025\n")
            f.write("=" * 65 + "\n\n")
            f.write(f"Total candidatos: {len(todas_puntuaciones)}\n")
            f.write(f"Páginas procesadas: {config['pdf']['pagina_inicio']}-{config['pdf']['pagina_fin']}\n\n")
            f.write("ESTADÍSTICAS DESCRIPTIVAS:\n")
            f.write("-" * 30 + "\n")
            f.write(f"Puntuación máxima: {df['Total'].max():.4f}\n")
            f.write(f"Puntuación mínima: {df['Total'].min():.4f}\n")
            f.write(f"Puntuación media: {df['Total'].mean():.4f}\n")
            f.write(f"Mediana: {df['Total'].median():.4f}\n")
            f.write(f"Desviación estándar: {df['Total'].std():.4f}\n")
            f.write(f"Percentil 25: {df['Total'].quantile(0.25):.4f}\n")
            f.write(f"Percentil 75: {df['Total'].quantile(0.75):.4f}\n")
            
            # Distribución por rangos
            rangos = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10)]
            f.write(f"\nDISTRIBUCIÓN POR RANGOS:\n")
            f.write("-" * 25 + "\n")
            for inicio, fin in rangos:
                count = len(df[(df['Total'] >= inicio) & (df['Total'] < fin)])
                porcentaje = (count / len(df)) * 100
                f.write(f"{inicio}-{fin} puntos: {count} candidatos ({porcentaje:.1f}%)\n")
            
            # Último rango (incluye 10.0)
            count_10 = len(df[df['Total'] == 10.0])
            if count_10 > 0:
                porcentaje_10 = (count_10 / len(df)) * 100
                f.write(f"10.0 puntos exactos: {count_10} candidatos ({porcentaje_10:.1f}%)\n")
        
        print(f"✅ Estadísticas guardadas: {stats_path}")
        
    except Exception as e:
        print(f"❌ ERROR guardando archivos: {e}")
        return False
    
    print(f"\n🎉 EXTRACCIÓN COMPLETADA")
    print(f"✅ {len(todas_puntuaciones)} candidatos procesados correctamente")
    print(f"📁 Archivos generados en: {output_dir}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
            
            # Buscar tabla estructurada primero
            tables = page.extract_tables()
            puntuaciones_tabla = []
            
            for table in tables:
                if table:
                    for row in table:
                        if row:
                            for cell in row:
                                if cell and isinstance(cell, str):
                                    # Buscar columna "Total" o puntuaciones
                                    if "Total" in cell or re.match(r'^\d+[.,]\d{4}$', cell.strip()):
                                        puntos = self._extraer_numero(cell)
                                        if puntos is not None and self._validar_puntuacion(puntos):
                                            puntuaciones_tabla.append(puntos)
            
            if puntuaciones_tabla:
                return puntuaciones_tabla
            
            # Si no hay tablas, buscar en texto plano
            patron = self.config['extraccion']['patron_puntuacion']
            matches = re.findall(patron, texto)
            
            puntuaciones_texto = []
            for match in matches:
                puntos = self._extraer_numero(match)
                if puntos is not None and self._validar_puntuacion(puntos):
                    puntuaciones_texto.append(puntos)
            
            return puntuaciones_texto
            
        except Exception as e:
            logger.warning(f"Error extrayendo página: {e}")
            return []
    
    def _extraer_numero(self, texto: str) -> float:
        """Extraer número de una cadena de texto."""
        try:
            # Limpiar y normalizar
            numero_str = texto.strip().replace(',', '.')
            
            # Extraer solo la parte numérica
            match = re.search(r'\d+\.?\d*', numero_str)
            if match:
                return float(match.group())
            return None
        except:
            return None
    
    def _validar_pagina(self, numero_pagina: int, puntuaciones: List[float]) -> bool:
        """Validar puntuaciones de una página contra valores esperados."""
        config_val = self.config.get('validacion', {})
        
        if numero_pagina == config_val.get('pagina_inicial', {}).get('numero'):
            esperadas = config_val['pagina_inicial']['puntuaciones_esperadas']
            encontradas = set(round(p, 4) for p in puntuaciones[:len(esperadas)])
            esperadas_set = set(esperadas)
            coincidencias = len(encontradas & esperadas_set)
            total = len(esperadas)
            
            logger.info(f"📋 Página {numero_pagina} (inicial): {coincidencias}/{total} coincidencias")
            logger.info(f"   Esperadas: {esperadas[:5]}...")
            logger.info(f"   Encontradas: {sorted(list(encontradas))[:5]}...")
            return coincidencias >= total * 0.8  # 80% de coincidencias
            
        elif numero_pagina == config_val.get('pagina_final', {}).get('numero'):
            esperadas = config_val['pagina_final']['puntuaciones_esperadas']
            encontradas = set(round(p, 4) for p in puntuaciones[-len(esperadas):])
            esperadas_set = set(esperadas)
            coincidencias = len(encontradas & esperadas_set)
            total = len(esperadas)
            
            logger.info(f"📋 Página {numero_pagina} (final): {coincidencias}/{total} coincidencias")
            logger.info(f"   Esperadas: {esperadas}")
            logger.info(f"   Encontradas: {sorted(list(encontradas))}")
            return coincidencias >= total * 0.8  # 80% de coincidencias
            
        return True
    
    def extraer_datos(self) -> pd.DataFrame:
        """Extraer todos los datos del PDF."""
        pdf_path = self.config['pdf']['archivo']
        pagina_inicio = self.config['pdf']['pagina_inicio']
        pagina_fin = self.config['pdf']['pagina_fin']
        
        logger.info(f"🚀 Iniciando extracción para Lengua Castellana y Literatura (011)")
        logger.info(f"📄 PDF: {pdf_path}")
        logger.info(f"📄 Páginas: {pagina_inicio}-{pagina_fin} ({pagina_fin - pagina_inicio + 1} páginas)")
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_paginas = len(pdf.pages)
                logger.info(f"📄 Total páginas en PDF: {total_paginas}")
                
                if pagina_fin > total_paginas:
                    logger.warning(f"⚠️ Página final ({pagina_fin}) mayor que total ({total_paginas})")
                    pagina_fin = total_paginas
                
                # Procesar páginas
                for num_pagina in range(pagina_inicio - 1, min(pagina_fin, total_paginas)):
                    try:
                        page = pdf.pages[num_pagina]
                        puntuaciones_pagina = self._extraer_puntuaciones_pagina(page)
                        
                        if puntuaciones_pagina:
                            # Validar páginas clave
                            if num_pagina + 1 in [pagina_inicio, pagina_fin]:
                                self._validar_pagina(num_pagina + 1, puntuaciones_pagina)
                            
                            self.puntuaciones.extend(puntuaciones_pagina)
                            logger.info(f"📄 Página {num_pagina + 1}: {len(puntuaciones_pagina)} puntuaciones")
                        else:
                            logger.warning(f"⚠️ Página {num_pagina + 1}: Sin puntuaciones encontradas")
                            
                    except Exception as e:
                        logger.error(f"❌ Error en página {num_pagina + 1}: {e}")
                        continue
                
                logger.info(f"✅ Extracción completada: {len(self.puntuaciones)} puntuaciones totales")
                
                # Crear DataFrame
                df = pd.DataFrame({
                    'Puntuacion': self.puntuaciones
                })
                
                return df
                
        except Exception as e:
            logger.error(f"❌ Error abriendo PDF: {e}")
            sys.exit(1)
    
    def guardar_resultados(self, df: pd.DataFrame):
        """Guardar resultados en múltiples formatos."""
        if df.empty:
            logger.warning("⚠️ No hay datos para guardar")
            return
        
        # Crear directorio output si no existe
        os.makedirs("../output", exist_ok=True)
        
        especialidad = self.config['especialidad']['codigo']
        
        # 1. CSV
        csv_path = f"../output/puntuaciones_lengua_literatura_{especialidad}.csv"
        df.to_csv(csv_path, index=False)
        logger.info(f"💾 CSV guardado: {csv_path}")
        
        # 2. TXT (lista legible)
        txt_path = f"../output/puntuaciones_lengua_literatura_{especialidad}.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"Puntuaciones Lengua Castellana y Literatura ({especialidad}) - Baremo 2025\n")
            f.write("=" * 60 + "\n\n")
            for i, puntuacion in enumerate(df['Puntuacion'], 1):
                f.write(f"{i:4d}: {puntuacion:.4f}\n")
        logger.info(f"💾 TXT guardado: {txt_path}")
        
        # 3. Array de Python
        py_path = f"../output/lista_lengua_literatura_{especialidad}.py"
        with open(py_path, 'w', encoding='utf-8') as f:
            f.write("# Lista de puntuaciones - Lengua Castellana y Literatura (011)\n")
            f.write("# Generado automáticamente\n\n")
            f.write("puntuaciones_lengua_literatura = [\n")
            for puntuacion in df['Puntuacion']:
                f.write(f"    {puntuacion:.4f},\n")
            f.write("]\n\n")
            f.write(f"# Total candidatos: {len(df)}\n")
            f.write(f"# Puntuación máxima: {df['Puntuacion'].max():.4f}\n")
            f.write(f"# Puntuación mínima: {df['Puntuacion'].min():.4f}\n")
            f.write(f"# Puntuación media: {df['Puntuacion'].mean():.4f}\n")
        logger.info(f"💾 Python guardado: {py_path}")
        
        # 4. Estadísticas
        stats_path = f"../output/estadisticas_lengua_literatura_{especialidad}.txt"
        with open(stats_path, 'w', encoding='utf-8') as f:
            f.write("ESTADÍSTICAS - LENGUA CASTELLANA Y LITERATURA (011)\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total candidatos: {len(df)}\n")
            f.write(f"Puntuación máxima: {df['Puntuacion'].max():.4f}\n")
            f.write(f"Puntuación mínima: {df['Puntuacion'].min():.4f}\n")
            f.write(f"Puntuación media: {df['Puntuacion'].mean():.4f}\n")
            f.write(f"Desviación estándar: {df['Puntuacion'].std():.4f}\n")
            f.write(f"Mediana: {df['Puntuacion'].median():.4f}\n")
            
            # Distribución por rangos
            f.write(f"\nDISTRIBUCIÓN POR RANGOS:\n")
            f.write(f"-" * 25 + "\n")
            rangos = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10)]
            for min_r, max_r in rangos:
                count = len(df[(df['Puntuacion'] >= min_r) & (df['Puntuacion'] < max_r)])
                porcentaje = (count / len(df)) * 100
                f.write(f"{min_r}-{max_r} puntos: {count} candidatos ({porcentaje:.1f}%)\n")
        
        logger.info(f"💾 Estadísticas guardadas: {stats_path}")
        
        # Mostrar resumen
        logger.info("\n" + "="*50)
        logger.info("📊 RESUMEN DE LA EXTRACCIÓN")
        logger.info("="*50)
        logger.info(f"Especialidad: Lengua Castellana y Literatura ({especialidad})")
        logger.info(f"Total candidatos: {len(df)}")
        logger.info(f"Puntuación máxima: {df['Puntuacion'].max():.4f}")
        logger.info(f"Puntuación mínima: {df['Puntuacion'].min():.4f}")
        logger.info(f"Puntuación media: {df['Puntuacion'].mean():.4f}")
        logger.info(f"Desviación estándar: {df['Puntuacion'].std():.4f}")
        logger.info("="*50)

def main():
    """Función principal."""
    print("🚀 Extractor de Lengua Castellana y Literatura (011) - Baremo 2025")
    print("="*60)
    
    try:
        # Crear extractor
        extractor = ExtractorLenguaLiteratura()
        
        # Extraer datos
        df = extractor.extraer_datos()
        
        if df.empty:
            logger.error("❌ No se encontraron datos válidos")
            sys.exit(1)
        
        # Guardar resultados
        extractor.guardar_resultados(df)
        
        print("\n✅ Extracción completada exitosamente")
        print("📁 Revisa la carpeta 'output' para los resultados")
        
    except KeyboardInterrupt:
        print("\n⚠️ Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
