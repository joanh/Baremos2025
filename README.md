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
│   ├── informatica_107/    # Informática (107) - IMPLEMENTADO
│   │   ├── scripts/        # Scripts específicos de Informática
│   │   ├── data/          # PDFs y archivos de entrada
│   │   ├── output/        # Resultados generados
│   │   ├── config.yaml    # Configuración específica
│   │   └── README.md      # Documentación detallada
│   └── matematicas_008/    # Matemáticas (008) - IMPLEMENTADO
│       ├── scripts/        # Scripts específicos de Matemáticas
│       ├── data/          # PDFs y archivos de entrada
│       ├── output/        # Resultados generados
│       ├── config.yaml    # Configuración específica
│       └── README.md      # Documentación detallada
├── img/                    # Gráficos generados para documentación
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
   # Para Informática (107)
   cd especialidades/informatica_107
   
   # Para Matemáticas (008)
   cd especialidades/matematicas_008
   ```

2. **Colocar el PDF en data/:**

   ```bash
   # Para Informática
   cp ../../data/rh03_257_2025_590_12_baremo_prov.pdf data/baremo_informatica_107_2025.pdf
   
   # Para Matemáticas
   cp ../../data/rh03_257_2025_590_12_baremo_prov.pdf data/baremo_matematicas_008_2025.pdf
   ```

3. **Ejecutar extractor específico:**

   ```bash
   cd scripts
   # Para Informática
   python extractor_informatica.py
   
   # Para Matemáticas
   python extractor_matematicas_CORREGIDO.py
   ```

4. **Generar visualización:**

   ```bash
   # Para Informática
   python visualizador_informatica.py
   
   # Para Matemáticas
   python visualizador_matematicas_CORREGIDO.py
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

- **✅ Informática (107)** - Páginas 2649-2697 - 338 candidatos - **COMPLETADO**
  - 📁 `especialidades/informatica_107/`
  - 🔧 Extractor + Visualizador funcionales
  - 📊 Validación exitosa contra datos conocidos
  - 🎨 Gráficos profesionales generados

- **✅ Matemáticas (008)** - Páginas 662-924 - 1,808 candidatos - **COMPLETADO**
  - 📁 `especialidades/matematicas_008/`
  - 🔧 Extractor + Visualizador funcionales
  - 📊 Extracción exitosa (263 páginas procesadas)
  - 🎨 Gráficos profesionales generados

- **✅ Física y Química (010)** - Páginas 925-1062 - 947 candidatos - **COMPLETADO**
  - 📁 `especialidades/fisica_quimica_010/`
  - 🔧 Extractor + Visualizador funcionales
  - 📊 Extracción exitosa (138 páginas procesadas)
  - 🎨 Gráficos profesionales generados

- **🔧 Lengua y Literatura** - Configurable - **PLANIFICADO**

## 🔧 Requisitos

```bash
pip install -r requirements.txt
```

## 📈 Ejemplo de Resultados

### Informática (107)
![Análisis Informática 2025](img/baremo_informatica_107_2025.png)

### Matemáticas (008)
![Análisis Matemáticas 2025](img/baremo_matematicas_008_2025.png)

### Física y Química (010)
![Análisis Física y Química 2025](img/baremo_fisica_quimica_010_2025.png)

### Datos Extraídos

#### Informática (107)
- **📊 338 candidatos** extraídos en orden del PDF
- **📈 Estadísticas**: Media 4.31, Mediana 4.06, σ 2.43
- **📋 Formatos**: CSV, TXT, Python list
- **🎨 Gráficos**: Distribución + análisis por rangos

#### Matemáticas (008)
- **📊 1,808 candidatos** extraídos en orden del PDF
- **📈 Estadísticas**: Media 4.68, Mediana 4.70, σ 2.74
- **📋 Formatos**: CSV, TXT, Python list
- **🎨 Gráficos**: Distribución + análisis por rangos

#### Física y Química (010)
- **📊 947 candidatos** extraídos en orden del PDF
- **📈 Estadísticas**: Media 4.97, Mediana 5.00, σ 2.72
- **📋 Formatos**: CSV, TXT, Python list
- **🎨 Gráficos**: Distribución + análisis por rangos

## 🤝 Contribuir

Este proyecto está en desarrollo activo. Contribuciones bienvenidas:

1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Commit de cambios
4. Push y crear Pull Request

## ⚖️ Aviso Legal

- Los datos utilizados son **públicos** y oficiales
- Este proyecto es **educativo** y no tiene fines comerciales
- No se garantiza la exactitud de los resultados
- Verificar siempre con fuentes oficiales

## ✍️ Autor

**@joanh** - Análisis y visualización de datos de oposiciones  
Asistente: Claude Sonnet 4.0

---
*📅 Última actualización: Julio 2025*
