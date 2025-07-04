# Informática 107 - Análisis de Baremo 📊

Extracción y análisis específico para la especialidad de **Informática (código 107)**.

## 📋 Información de la Especialidad

- **Código**: 107
- **Nombre**: Informática
- **Descripción**: Profesores de Enseñanza Secundaria - Informática
- **Páginas en PDF**: 2649 - 2697
- **Candidatos esperados**: 343
- **Fecha de publicación**: 1 de julio de 2025

## 🏗️ Estructura

```
informatica_107/
├── scripts/
│   ├── extractor_informatica.py    # Extractor principal
│   ├── visualizador_informatica.py # Generador de gráficos
│   └── validador_informatica.py    # Validación de datos
├── data/
│   └── baremo_informatica_107_2025.pdf  # PDF original (colocar aquí)
├── output/
│   ├── puntuaciones_informatica_107.csv
│   ├── lista_informatica_107.txt
│   ├── lista_informatica_107.py
│   ├── baremo_informatica_107_2025.png
│   └── estadisticas_informatica_107.txt
├── config.yaml                     # Configuración específica
└── README.md                       # Esta documentación
```

## 🚀 Uso

### 1. Preparar Datos
```bash
# Copiar el PDF original a la carpeta data/
cp ../../data/rh03_257_2025_590_12_baremo_prov.pdf data/baremo_informatica_107_2025.pdf
```

### 2. Extraer Datos
```bash
cd scripts
python extractor_informatica.py
```

### 3. Generar Visualización
```bash
python visualizador_informatica.py
```

### 4. Validar Resultados
```bash
python validador_informatica.py
```

## 📊 Resultados Esperados

- **343 candidatos** extraídos en orden del PDF
- **Puntuaciones** en formato CSV, TXT y Python
- **Gráfico profesional** con estadísticas
- **Validación** contra datos conocidos

## 🔧 Configuración

Todos los parámetros se configuran en `config.yaml`:

- Rutas de archivos
- Rangos de páginas
- Patrones de extracción
- Configuración de visualización
- Parámetros de validación

## ✅ Validación

Para validar que la extracción es correcta:

1. **Número total**: Debe ser exactamente 343 candidatos
2. **Orden preservado**: Debe mantener el orden exacto del PDF
3. **Rangos válidos**: Puntuaciones entre 0.0 y 15.0
4. **Consistencia**: Comparar con extracciones anteriores

## 📈 Salidas Generadas

### Archivos de Datos
- `puntuaciones_informatica_107.csv` - Datos tabulados
- `lista_informatica_107.txt` - Lista legible
- `lista_informatica_107.py` - Array de Python
- `estadisticas_informatica_107.txt` - Resumen estadístico

### Visualización
- `baremo_informatica_107_2025.png` - Gráfico profesional con:
  - Histograma de distribución
  - Estadísticas principales
  - Firma @joanh
  - Formato consistente

## 🚨 Troubleshooting

### Errores Comunes

1. **PDF no encontrado**
   - Verificar que el archivo esté en `data/`
   - Comprobar el nombre exacto del archivo

2. **Números de página incorrectos**
   - Verificar configuración en `config.yaml`
   - Comprobar que el PDF tenga las páginas esperadas

3. **Candidatos faltantes**
   - Revisar patrones de extracción
   - Verificar formato del PDF

### Logs y Depuración

El script muestra información detallada durante la ejecución:
- Número de candidatos extraídos
- Páginas procesadas
- Errores encontrados
- Estadísticas finales

## 📝 Notas

- **Orden preservado**: Los candidatos se mantienen en el orden exacto del PDF oficial
- **Sin modificaciones**: No se aplica ningún ordenamiento o filtrado
- **Trazabilidad completa**: Cada candidato mantiene su posición original
- **Reproducible**: Los resultados deben ser idénticos en cada ejecución

---

**Autor**: @joanh  
**Asistente**: Claude Sonnet 4.0  
**Fecha**: Julio 2025
