# Matemáticas (008) - Baremo 2025 📐

Extracción y análisis de datos para la especialidad de **Matemáticas** (código 008) del baremo provisional de oposiciones 2025 de la Comunidad de Madrid.

## 📊 Información de la Especialidad

- **Código**: 008
- **Nombre**: Matemáticas  
- **Nivel**: Profesores de Enseñanza Secundaria
- **Total candidatos**: 1,808
- **Páginas**: 662-924 (263 páginas)
- **Fuente**: [Baremo Provisional CM](https://www.comunidad.madrid/sites/default/files/doc/educacion/rh03/rh03_257_2025_590_12_baremo_prov.pdf)

## 🚀 Uso

### 1. Extraer datos

```bash
cd scripts
python extractor_matematicas_CORREGIDO.py
```

### 2. Generar visualización

```bash
python visualizador_matematicas_CORREGIDO.py
```

## 📈 Resultados de la Extracción

- **Total candidatos**: 1,808
- **Puntuación máxima**: 10.0000
- **Puntuación mínima**: 0.0000  
- **Puntuación media**: 4.6811
- **Desviación estándar**: 2.7438

### Distribución por rangos

- **0-2 puntos**: 363 candidatos (20.1%)
- **2-4 puntos**: 419 candidatos (23.2%)
- **4-6 puntos**: 329 candidatos (18.2%)
- **6-8 puntos**: 421 candidatos (23.3%)
- **8-10 puntos**: 251 candidatos (13.9%)

![Gráfico Matemáticas](../../img/baremo_matematicas_008_2025.png)

## 📁 Estructura

```
matematicas_008/
├── scripts/
│   ├── analisis_forense_matematicas.py  # Buscar páginas de Matemáticas
│   ├── extractor_matematicas.py         # Extractor específico
│   └── visualizador_matematicas.py      # Gráficos profesionales
├── data/
│   └── baremo_matematicas_008_2025.pdf  # PDF específico (opcional)
├── output/                               # Resultados generados
├── config.yaml                          # Configuración de la especialidad
└── README.md                            # Este archivo
```

## ⚙️ Configuración

El archivo `config.yaml` contiene:
- Páginas del PDF a procesar
- Patrones de extracción específicos
- Configuración de visualización
- Metadatos de la especialidad

## 🎯 Archivos Generados

- `puntuaciones_matematicas_008.csv` - Datos en formato CSV
- `puntuaciones_matematicas_008.txt` - Lista legible
- `lista_matematicas_008.py` - Array de Python
- `estadisticas_matematicas_008.txt` - Estadísticas básicas
- `baremo_matematicas_008_2025.png/pdf` - Gráficos profesionales

## 📈 Ejemplo de Resultados

Una vez ejecutado correctamente, se generarán:
- Histograma de distribución de puntuaciones
- Gráfico de barras por rangos
- Estadísticas descriptivas completas
- Análisis de normalidad

## 🔧 Requisitos

```bash
pip install pdfplumber pandas matplotlib numpy scipy pyyaml
```

## ✍️ Autor

**@joanh** - Análisis y visualización de datos de oposiciones  
Asistente: Claude Sonnet 4.0
