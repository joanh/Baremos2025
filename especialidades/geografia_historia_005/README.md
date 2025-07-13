# Geografía e Historia (005) - Baremo 2025 🗺️

Extracción y análisis de datos para la especialidad de **Geografía e Historia** (código 005) del baremo provisional de oposiciones 2025 de la Comunidad de Madrid.

## 📊 Información de la Especialidad

- **Código**: 005
- **Nombre**: Geografía e Historia  
- **Nivel**: Profesores de Enseñanza Secundaria
- **Total candidatos**: 2,112
- **Páginas**: 360-661 (302 páginas)
- **Fuente**: [Baremo Provisional CM](https://www.comunidad.madrid/sites/default/files/doc/educacion/rh03/rh03_257_2025_590_12_baremo_prov.pdf)

## 🚀 Uso

### 1. Extraer datos

```bash
cd scripts
python extractor_geografia_historia.py
```

### 2. Generar visualización

```bash
python visualizador_geografia_historia.py
```

## 📈 Resultados de la Extracción

- **Total candidatos**: 2,112
- **Puntuación máxima**: 10.0000
- **Puntuación mínima**: 0.0000  
- **Puntuación media**: 4.9876
- **Desviación estándar**: 2.6432

### Distribución por rangos

- **0-2 puntos**: 297 candidatos (14.1%)
- **2-4 puntos**: 481 candidatos (22.8%)
- **4-6 puntos**: 437 candidatos (20.7%)
- **6-8 puntos**: 564 candidatos (26.7%)
- **8-10 puntos**: 333 candidatos (15.8%)

![Gráfico Geografía e Historia](../../img/baremo_geografia_e_historia_005_2025.png)

## 📁 Estructura

```
geografia_historia_005/
├── scripts/
│   ├── analisis_forense_geografia.py    # Buscar páginas de Geografía
│   ├── extractor_geografia_historia.py  # Extractor específico
│   └── visualizador_geografia_historia.py # Gráficos profesionales
├── data/
│   └── baremo_geografia_historia_005_2025.pdf  # PDF específico (opcional)
├── output/                               # Resultados generados
├── config.yaml                          # Configuración de la especialidad
└── README.md                            # Este archivo
```

## ⚙️ Configuración

El archivo `config.yaml` contiene:

- Páginas del PDF a procesar (360-661)
- Patrones de extracción específicos
- Configuración de visualización
- Metadatos de la especialidad

## 🎯 Archivos Generados

- `puntuaciones_geografia_historia_005.csv` - Datos en formato CSV
- `puntuaciones_geografia_historia_005.txt` - Lista legible
- `lista_geografia_historia_005.py` - Array de Python
- `estadisticas_geografia_historia_005.txt` - Estadísticas básicas
- `baremo_geografia_e_historia_005_2025.png/pdf` - Gráficos profesionales

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
