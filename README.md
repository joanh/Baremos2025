# Baremo2025 - Análisis de Oposiciones 📊

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
![Work in Progress](https://img.shields.io/badge/status-work%20in%20progress-orange.svg)
[![PDFPlumber](https://img.shields.io/badge/pdfplumber-0.7%2B-green.svg)](https://github.com/jsvine/pdfplumber)
[![Pandas](https://img.shields.io/badge/pandas-1.3%2B-150458.svg)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/matplotlib-3.5%2B-11557c.svg)](https://matplotlib.org/)
[![NumPy](https://img.shields.io/badge/numpy-1.21%2B-013243.svg)](https://numpy.org/)
[![Claude](https://img.shields.io/badge/AI_Assistant-Claude_Sonnet_4.0-8A2BE2.svg)](https://www.anthropic.com/claude)

Herramientas para extraer y analizar datos de baremos de oposiciones desde PDFs oficiales.

## 🎯 Características

- **Análisis forense de PDFs** complejos con múltiples especialidades
- **Extracción automatizada** de puntuaciones manteniendo el orden original  
- **Visualización profesional** con gráficos estadísticos
- **Generalizable** para cualquier especialidad de oposiciones

## 🪧 Datos Públicos

Los datos tratados en este repositorio son públicos y fueron publicados el 1 de julio de 2025:

👉 [Baremo Provisional - Comunidad de Madrid](https://www.comunidad.madrid/sites/default/files/doc/educacion/rh03/rh03_257_2025_590_12_baremo_prov.pdf)

Una copia del PDF original se puede encontrar en `./data`

## 📁 Estructura

```
Baremo2025/
├── src/                    # Scripts comunes y herramientas generales
│   ├── analisis_forense_pdf.py    # Análisis de estructura PDF
│   ├── extractor_ORDEN_REAL.py    # Extractor original (legacy)
│   └── baremo2025.py              # Visualización general
├── especialidades/         # Directorios independientes por especialidad
│   └── informatica_107/    # Informática (107) - IMPLEMENTADO
│       ├── scripts/        # Scripts específicos de Informática
│       ├── data/          # PDFs y archivos de entrada
│       ├── output/        # Resultados generados
│       ├── config.yaml    # Configuración específica
│       └── README.md      # Documentación detallada
├── data/                   # PDFs originales comunes
├── output/                 # Resultados globales (legacy)
├── config/                 # Configuración global
├── backup/                 # Archivos de desarrollo
├── docs/                   # Documentación general
└── examples/              # Ejemplos de uso
```

## 🚀 Uso Rápido

### Método Recomendado (Especialidades Independientes)

1. **Navegar a la especialidad deseada:**
   ```bash
   cd especialidades/informatica_107
   ```

2. **Colocar el PDF en data/:**
   ```bash
   cp ../../data/rh03_257_2025_590_12_baremo_prov.pdf data/baremo_informatica_107_2025.pdf
   ```

3. **Ejecutar extractor específico:**
   ```bash
   cd scripts
   python extractor_informatica.py
   ```

### Método Legacy (Scripts Globales)

1. **Analizar estructura del PDF:**
   ```bash
   python src/analisis_forense_pdf.py
   ```

2. **Extraer datos:**
   ```bash  
   python src/extractor_ORDEN_REAL.py
   ```

3. **Generar visualización:**
   ```bash
   python src/baremo2025.py
   ```

## 📊 Especialidades Disponibles

- **✅ Informática (107)** - Páginas 2649-2697 - 343 candidatos - **IMPLEMENTADO**
  - 📁 `especialidades/informatica_107/`
  - 🔧 Scripts específicos y configuración dedicada
  - 📊 Validación contra datos conocidos
- **🔧 Matemáticas (008)** - Configurable - **PLANIFICADO**
- **🔧 Física y Química (010)** - Configurable - **PLANIFICADO**
- **🔧 Lengua y Literatura** - Configurable - **PLANIFICADO**

## 🔧 Requisitos

```bash
pip install -r requirements.txt
```

## 📈 Ejemplo de Resultados

![Análisis Informática 2025](output/baremo_informatica_107_2025.png)

### Datos Extraídos

- **📊 343 candidatos** de Informática en orden del PDF
- **📈 Estadísticas completas** (media, mediana, percentiles)
- **📋 Múltiples formatos** (CSV, TXT, Python list)
- **🎨 Gráficos profesionales** con firma @joanh

## 🤝 Contribuir

1. Fork del repositorio
2. Crear rama para tu especialidad
3. Añadir configuración para nuevas especialidades
4. Pull request

## 📝 Licencia

MIT License

## ✍️ Autor

**@joanh** - Análisis y visualización de datos de oposiciones

### Metodología

Este proyecto demuestra cómo realizar **minería de datos en PDFs complejos**:

1. **🔍 Análisis forense** para entender la estructura
2. **⚙️ Extracción precisa** manteniendo el orden original
3. **📊 Visualización profesional** con estadísticas

---
⭐ Si te resulta útil, ¡dale una estrella al repo!
