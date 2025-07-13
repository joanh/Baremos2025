# Biología y Geología (008) - Baremo 2025 🧬

Extracción y análisis de datos para la especialidad de **Biología y Geología** (código 008) del baremo provisional de oposiciones 2025 de la Comunidad de Madrid.

## 📊 Información de la Especialidad

- **Código**: 008
- **Nombre**: Biología y Geología  
- **Nivel**: Profesores de Enseñanza Secundaria
- **Total candidatos**: 1,275
- **Páginas**: 1063-1237 (175 páginas)
- **Fuente**: [Baremo Provisional CM](https://www.comunidad.madrid/sites/default/files/doc/educacion/rh03/rh03_257_2025_590_12_baremo_prov.pdf)

## 🚀 Uso

### 1. Extraer datos

```bash
cd scripts
python extractor_biologia_geologia.py
```

### 2. Generar visualización

```bash
python visualizador_biologia_geologia.py
```

## 📈 Resultados de la Extracción

- **Total candidatos**: 1,275
- **Puntuación máxima**: 10.0000
- **Puntuación mínima**: 0.0000  
- **Puntuación media**: 5.2447
- **Desviación estándar**: 2.6891

### Distribución por rangos

- **0-2 puntos**: 178 candidatos (14.0%)
- **2-4 puntos**: 267 candidatos (20.9%)
- **4-6 puntos**: 302 candidatos (23.7%)
- **6-8 puntos**: 374 candidatos (29.3%)
- **8-10 puntos**: 154 candidatos (12.1%)

![Gráfico Biología y Geología](../../img/baremo_biologia_geologia_008_2025.png)

## 📁 Estructura

```
biologia_geologia_008/
├── scripts/
│   ├── analisis_forense_biologia.py     # Buscar páginas de Biología
│   ├── extractor_biologia_geologia.py   # Extractor específico
│   └── visualizador_biologia_geologia.py # Gráficos profesionales
├── data/
│   └── baremo_biologia_geologia_008_2025.pdf  # PDF específico (opcional)
├── output/                               # Resultados generados
├── config.yaml                          # Configuración de la especialidad
└── README.md                            # Este archivo
```

## ⚙️ Configuración

El archivo `config.yaml` contiene:
- Páginas del PDF a procesar (1063-1237)
- Patrones de extracción específicos
- Configuración de visualización
- Metadatos de la especialidad

## 🎯 Archivos Generados

- `puntuaciones_biologia_geologia_008.csv` - Datos en formato CSV
- `puntuaciones_biologia_geologia_008.txt` - Lista legible
- `lista_biologia_geologia_008.py` - Array de Python
- `estadisticas_biologia_geologia_008.txt` - Estadísticas básicas
- `baremo_biologia_geologia_008_2025.png/pdf` - Gráficos profesionales

## 📈 Ejemplo de Resultados

Una vez ejecutado correctamente, se generarán:
- Histograma de distribución de puntuaciones con curva normal
- Gráfico de barras por rangos de puntuación
- Estadísticas descriptivas completas (media, mediana, desviación)
- Análisis de normalidad y distribución

## 🔧 Requisitos

```bash
pip install pdfplumber pandas matplotlib numpy scipy pyyaml
```

## ✍️ Autor

**@joanh** - Análisis y visualización de datos de oposiciones  
Asistente: Claude Sonnet 4.0
