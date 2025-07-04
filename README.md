# Baremo2025 - Análisis de Oposiciones 📊

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-black.svg)](https://github.com/psf/black)
[![PDF Processing](https://img.shields.io/badge/PDF-Processing-red.svg)](https://github.com/jmcarpenter2/pdfplumber)
[![Data Science](https://img.shields.io/badge/Data-Science-orange.svg)](https://pandas.pydata.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-purple.svg)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-blue.svg)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-blue.svg)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-lightblue.svg)](https://seaborn.pydata.org/)
[![GitHub](https://img.shields.io/github/stars/joanh/Baremos2025?style=social)](https://github.com/joanh/Baremos2025)
[![Forks](https://img.shields.io/github/forks/joanh/Baremos2025?style=social)](https://github.com/joanh/Baremos2025)
[![Issues](https://img.shields.io/github/issues/joanh/Baremos2025)](https://github.com/joanh/Baremos2025/issues)
[![Last Commit](https://img.shields.io/github/last-commit/joanh/Baremos2025)](https://github.com/joanh/Baremos2025)
[![Education](https://img.shields.io/badge/Purpose-Education-brightgreen.svg)](https://github.com/joanh/Baremos2025)

Herramientas Python para extraer y analizar datos de baremos de oposiciones desde PDFs oficiales de la Comunidad de Madrid.

## 📊 Gráficos y Estadísticas

### 🎯 Acceso Directo a Resultados

| Especialidad | Candidatos | Gráfico | Estadísticas | Datos |
|--------------|------------|---------|-------------|-------|
| **Informática (107)** | 343 | [📈 Ver Gráfico](img/baremo_informatica_107_2025.png) | Media: 6.84, σ: 2.44 | [📁 Datos](especialidades/informatica_107/output/) |
| **Matemáticas (008)** | 1,829 | [📈 Ver Gráfico](img/baremo_matematicas_008_2025.png) | Media: 5.07, σ: 2.61 | [📁 Datos](especialidades/matematicas_008/output/) |
| **Física y Química (010)** | 962 | [📈 Ver Gráfico](img/baremo_fisica_quimica_010_2025.png) | Media: 5.09, σ: 2.62 | [📁 Datos](especialidades/fisica_quimica_010/output/) |
| **Lengua y Literatura (004)** | 1,727 | [📈 Ver Gráfico](img/baremo_lengua_literatura_004_2025.png) | Media: 5.06, σ: 2.62 | [📁 Datos](especialidades/lengua_literatura_004/output/) |

### 📈 Vista Previa de Resultados

![Análisis Informática 2025](img/baremo_informatica_107_2025.png)

*Ejemplo: Distribución de puntuaciones de Informática (107) - 343 candidatos*

## 🎯 Características

- **Análisis forense de PDFs** complejos con múltiples especialidades
- **Extracción automatizada** de puntuaciones manteniendo el orden original  
- **Visualización profesional** con gráficos estadísticos usando matplotlib y seaborn
- **Arquitectura modular** - Cada especialidad es totalmente independiente
- **Datos verificables** - Validación automática con puntuaciones de control
- **Múltiples formatos** - CSV, TXT, Python lists, gráficos PNG/PDF

## 📁 Estructura

```
Baremo2025/
├── src/                    # Código fuente
│   ├── analisis_forense_pdf.py    # Análisis de estructura PDF
│   ├── extractor_ORDEN_REAL.py    # Extractor en orden del PDF
│   └── baremo2025.py              # Visualización y estadísticas
├── data/                   # PDFs originales
├── output/                 # Resultados generados
├── config/                 # Configuración de especialidades
├── backup/                 # Archivos de desarrollo
├── docs/                   # Documentación
└── examples/              # Ejemplos de uso
```

## 🚀 Uso Rápido

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

## 📊 Especialidades Implementadas

### ✅ **Completamente Funcionales**

| Especialidad | Código | Candidatos | Estado | Documentación |
|--------------|--------|------------|--------|---------------|
| **Informática** | 107 | 343 | ✅ Completo | [📖 README](especialidades/informatica_107/README.md) |
| **Matemáticas** | 008 | 1,829 | ✅ Completo | [📖 README](especialidades/matematicas_008/README.md) |
| **Física y Química** | 010 | 962 | ✅ Completo | [📖 README](especialidades/fisica_quimica_010/README.md) |
| **Lengua y Literatura** | 004 | 1,727 | ✅ Completo | [📖 README](especialidades/lengua_literatura_004/README.md) |

**Total candidatos analizados: 4,861** 📊

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
