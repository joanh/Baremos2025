import os
import shutil
import glob
from pathlib import Path

# SCRIPT PARA CREAR REPOSITORIO BAREMO2025 COMPLETO
print("=== CREANDO REPOSITORIO BAREMO2025 COMPLETO ===")

# Crear estructura del repositorio
repo_path = Path("C:/GitHub/Baremo2025")
repo_path.mkdir(parents=True, exist_ok=True)

# Crear subdirectorios incluido backup
dirs = ['src', 'data', 'output', 'docs', 'examples', 'config', 'backup']
for dir_name in dirs:
    (repo_path / dir_name).mkdir(exist_ok=True)
    print(f"📁 Creado: {dir_name}/")

print(f"\n=== MOVIENDO ARCHIVOS PRINCIPALES ===")

# 1. Mover PDF original a data/
pdf_files = glob.glob("*.pdf")
for pdf_file in pdf_files:
    if "baremo" in pdf_file.lower() or "rh03" in pdf_file:
        src = Path(pdf_file)
        dst = repo_path / "data" / pdf_file
        shutil.copy2(src, dst)
        print(f"✅ PDF movido: {pdf_file} → data/")

# 2. Archivos principales a src/
archivos_src = [
    'analisis_forense_pdf.py',
    'extractor_ORDEN_REAL.py', 
    'extractor_DEFINITIVO.py',
    'extractor_FINAL_CORREGIDO.py',
    'baremo2025.py'  # Este archivo DEBE existir
]

print(f"\n=== VERIFICANDO ARCHIVOS PRINCIPALES ===")

# Verificar qué archivos existen realmente
archivos_existentes = []
archivos_faltantes = []

for archivo in archivos_src:
    if Path(archivo).exists():
        archivos_existentes.append(archivo)
        dst = repo_path / "src" / archivo
        shutil.copy2(archivo, dst)
        print(f"✅ Código movido: {archivo} → src/")
    else:
        archivos_faltantes.append(archivo)
        print(f"❌ NO ENCONTRADO: {archivo}")

# Si falta baremo2025.py, buscarlo con otros nombres
if 'baremo2025.py' in archivos_faltantes:
    print(f"\n🔍 BUSCANDO ARCHIVO BAREMO2025...")
    
    # Buscar variaciones del nombre
    posibles_nombres = [
        'baremo*.py',
        '*baremo*.py', 
        '*2025*.py',
        '*visualiz*.py'
    ]
    
    encontrado = False
    for patron in posibles_nombres:
        archivos = glob.glob(patron)
        for archivo in archivos:
            if 'baremo' in archivo.lower() or '2025' in archivo:
                print(f"📍 Encontrado archivo similar: {archivo}")
                dst = repo_path / "src" / archivo
                shutil.copy2(archivo, dst)
                print(f"✅ Movido: {archivo} → src/")
                encontrado = True
                break
        if encontrado:
            break
    
    if not encontrado:
        print(f"⚠️ ARCHIVO BAREMO2025.PY NO ENCONTRADO")
        print(f"💡 Creando archivo básico de visualización...")
        
        # Crear archivo baremo2025.py básico
        baremo_basico = '''import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.colors as mcolors

# ANÁLISIS BAREMO INFORMÁTICA 107 - 2025
print("=== ANÁLISIS BAREMO INFORMÁTICA 107 - 2025 ===")

# Cargar datos reales
try:
    with open('lista_informatica_107.py', 'r') as f:
        exec(f.read())
    datos = puntuaciones_informatica
    print(f"✅ Datos cargados: {len(datos)} candidatos")
except:
    print("❌ Archivo lista_informatica_107.py no encontrado")
    print("Ejecuta primero extractor_ORDEN_REAL.py")
    exit()

# Convertir a numpy array
puntuaciones = np.array(datos)

print(f"📊 Total candidatos: {len(puntuaciones)}")
print(f"🏆 Puntuación máxima: {np.max(puntuaciones):.4f}")
print(f"📉 Puntuación mínima: {np.min(puntuaciones):.4f}")
print(f"📈 Media: {np.mean(puntuaciones):.4f}")
print(f"📊 Mediana: {np.median(puntuaciones):.4f}")
print(f"📐 Desviación estándar: {np.std(puntuaciones):.4f}")

# Análisis por rangos
rangos = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10)]
rangos_counts = []
rangos_porcentajes = []

for min_r, max_r in rangos:
    count = np.sum((puntuaciones >= min_r) & (puntuaciones < max_r))
    porcentaje = (count / len(puntuaciones)) * 100
    rangos_counts.append(count)
    rangos_porcentajes.append(porcentaje)

# CREAR GRÁFICOS
plt.style.use('default')
plt.rcParams['font.size'] = 12

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('ANÁLISIS BAREMO INFORMÁTICA 107 - CONVOCATORIA 2025', 
             fontsize=16, fontweight='bold', y=0.95)

# 1. HISTOGRAMA
ax1.hist(puntuaciones, bins=25, alpha=0.7, color='steelblue', 
         edgecolor='black', linewidth=1)

# Curva normal
mu, sigma = stats.norm.fit(puntuaciones)
x = np.linspace(0, 10, 100)
y_normal = stats.norm.pdf(x, mu, sigma)
scale_factor = len(puntuaciones) * (10 / 25)
y_normal_scaled = y_normal * scale_factor
ax1.plot(x, y_normal_scaled, 'red', linewidth=3, 
         label=f'Distribución Normal\\nμ={mu:.2f}, σ={sigma:.2f}')

ax1.set_xlabel('Puntuación (0-10)', fontweight='bold')
ax1.set_ylabel('Número de Candidatos', fontweight='bold')
ax1.set_title('Distribución de Puntuaciones', fontweight='bold', pad=20)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 10)

# 2. GRÁFICO DE BARRAS CON GRADIENTE
rangos_nombres = ['0-2', '2-4', '4-6', '6-8', '8-10']
norm = mcolors.Normalize(vmin=min(rangos_porcentajes), vmax=max(rangos_porcentajes))
colormap = plt.cm.RdYlBu_r

bars = ax2.bar(rangos_nombres, rangos_counts, 
               color=[colormap(norm(p)) for p in rangos_porcentajes],
               edgecolor='black', linewidth=1.5, alpha=0.8)

ax2.set_xlabel('Rango de Puntuaciones', fontweight='bold')
ax2.set_ylabel('Número de Candidatos', fontweight='bold')
ax2.set_title('Distribución por Rangos de Puntuación', fontweight='bold', pad=20)
ax2.grid(True, alpha=0.3, axis='y')

# Valores en barras
for bar, count, porcentaje in zip(bars, rangos_counts, rangos_porcentajes):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + max(rangos_counts)*0.01,
             f'{count}\\n({porcentaje:.1f}%)',
             ha='center', va='bottom', fontweight='bold', fontsize=10)

# FIRMA DEL AUTOR
fig.text(0.99, 0.01, '@joanh', fontsize=10, color='gray', alpha=0.7, 
         ha='right', va='bottom', style='italic', weight='bold')

plt.tight_layout()

# GUARDAR
plt.savefig('baremo_informatica_107_2025.png', dpi=300, bbox_inches='tight')
plt.savefig('baremo_informatica_107_2025.pdf', bbox_inches='tight')
print(f"\\n💾 Gráficos guardados:")
print("   - baremo_informatica_107_2025.png")
print("   - baremo_informatica_107_2025.pdf")

plt.show()

print(f"\\n🎉 ANÁLISIS COMPLETADO")
print(f"✍️ Análisis realizado por @joanh")
'''
        
        # Crear el archivo en src/
        with open(repo_path / "src" / "baremo2025.py", "w", encoding="utf-8") as f:
            f.write(baremo_basico)
        print(f"✅ Creado: src/baremo2025.py")

# Mostrar resumen de archivos encontrados
print(f"\n📋 RESUMEN ARCHIVOS PRINCIPALES:")
print(f"✅ Encontrados: {len(archivos_existentes)}")
for archivo in archivos_existentes:
    print(f"   - {archivo}")

if archivos_faltantes:
    print(f"❌ Faltantes: {len(archivos_faltantes)}")
    for archivo in archivos_faltantes:
        print(f"   - {archivo}")

# 3. Resultados finales a output/
archivos_output = [
    'lista_informatica_107.py',
    'INFORMATICA_107_ORDEN_PDF.csv',
    'INFORMATICA_107_ORDEN_PDF.txt',
    'INFORMATICA_107_EXTRACCION.csv',
    'INFORMATICA_107_EXTRACCION.txt',
    'INFORMATICA_107_DATOS_REALES.csv',
    'INFORMATICA_107_DATOS_REALES.txt'
]

# Buscar todos los archivos de resultados (incluyendo variaciones)
patrones_output = [
    'lista_informatica_*.py',
    'INFORMATICA_*_*.csv', 
    'INFORMATICA_*_*.txt',
    'baremo_informatica_*.png',
    'baremo_informatica_*.pdf'
]

for patron in patrones_output:
    for archivo in glob.glob(patron):
        dst = repo_path / "output" / archivo
        shutil.copy2(archivo, dst)
        print(f"✅ Resultado movido: {archivo} → output/")

# 4. MOVER TODO A BACKUP (incluyendo versiones intermedias)
print(f"\n=== CREANDO BACKUP COMPLETO ===")

# Todos los archivos relacionados con el análisis
patrones_backup = [
    'extractor_*.py',
    'analisis_*.py', 
    'baremo*.py',
    'lista_*.py',
    '*INFORMATICA*.csv',
    '*INFORMATICA*.txt', 
    '*informatica*.png',
    '*informatica*.pdf',
    'moverepo.py'
]

archivos_backup = set()  # Usar set para evitar duplicados

for patron in patrones_backup:
    for archivo in glob.glob(patron):
        archivos_backup.add(archivo)

for archivo in archivos_backup:
    if Path(archivo).exists():
        dst = repo_path / "backup" / archivo
        shutil.copy2(archivo, dst)
        print(f"📦 Backup: {archivo} → backup/")

print(f"\n=== CREANDO ARCHIVOS DEL REPOSITORIO ===")

# README.md
readme_content = '''# Baremo2025 - Análisis de Oposiciones 📊

Herramientas para extraer y analizar datos de baremos de oposiciones desde PDFs oficiales.

## 🎯 Características

- **Análisis forense de PDFs** complejos con múltiples especialidades
- **Extracción automatizada** de puntuaciones manteniendo el orden original  
- **Visualización profesional** con gráficos estadísticos
- **Generalizable** para cualquier especialidad de oposiciones

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

## 📊 Especialidades Disponibles

- **✅ Informática (107)** - Páginas 2649-2697 - 343 candidatos
- **🔧 Matemáticas** - Configurable
- **🔧 Física y Química** - Configurable  
- **🔧 Lengua y Literatura** - Configurable

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
'''

with open(repo_path / "README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)
print("✅ Creado: README.md")

# requirements.txt
requirements = '''pdfplumber>=0.7.0
numpy>=1.21.0
matplotlib>=3.5.0
scipy>=1.7.0
pandas>=1.3.0
PyYAML>=6.0
'''

with open(repo_path / "requirements.txt", "w") as f:
    f.write(requirements)
print("✅ Creado: requirements.txt")

# Configuración de especialidades
especialidades_config = '''especialidades:
  INFORMATICA:
    codigo: "107"
    nombre: "INFORMATICA" 
    pagina_inicio: 2649
    pagina_fin: 2697
    candidatos_por_pagina: 7
    descripcion: "Profesores de Enseñanza Secundaria - Informática"
    total_candidatos: 343
  
  MATEMATICAS:
    codigo: "008"
    nombre: "MATEMATICAS"
    pagina_inicio: null  # Configurar según PDF
    pagina_fin: null     # Configurar según PDF
    candidatos_por_pagina: 7
    descripcion: "Profesores de Enseñanza Secundaria - Matemáticas"
  
  FISICA_QUIMICA:
    codigo: "010" 
    nombre: "FISICA_QUIMICA"
    pagina_inicio: null  # Configurar según PDF
    pagina_fin: null     # Configurar según PDF
    candidatos_por_pagina: 7
    descripcion: "Profesores de Enseñanza Secundaria - Física y Química"

# Configuración general
configuracion:
  patron_dni: "^\\*\\*\\*\\*.*\\*"
  patron_numeros: "\\b(\\d{1,2},\\d{4})\\b"
  rango_puntuaciones: [0.0, 10.0]
  pdf_original: "rh03_257_2025_590_12_baremo_prov.pdf"
'''

with open(repo_path / "config" / "especialidades.yaml", "w", encoding="utf-8") as f:
    f.write(especialidades_config)
print("✅ Creado: config/especialidades.yaml")

# .gitignore
gitignore = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Data files - MANTENER PDFs EN REPO PARA REFERENCIA
# *.pdf (comentado para incluir PDFs de ejemplo)

# Output temporales
output/temp_*
output/*.tmp

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Backup temporal
backup/temp_*
'''

with open(repo_path / ".gitignore", "w") as f:
    f.write(gitignore)
print("✅ Creado: .gitignore")

# Script de limpieza COMPLETA del directorio actual
cleanup_script = '''import os
import glob

# SCRIPT PARA LIMPIAR COMPLETAMENTE DIRECTORIO FCT
print("=== LIMPIEZA COMPLETA DIRECTORIO FCT ===")

# Todos los archivos relacionados con baremos
patrones_limpiar = [
    "analisis_*.py",
    "extractor_*.py", 
    "baremo*.py",
    "lista_*.py",
    "*INFORMATICA*.csv",
    "*INFORMATICA*.txt",
    "*informatica*.png", 
    "*informatica*.pdf",
    "rh03_*.pdf",
    "*baremo*.pdf",
    "moverepo.py"
]

total_eliminados = 0

for patron in patrones_limpiar:
    archivos = glob.glob(patron)
    for archivo in archivos:
        try:
            os.remove(archivo)
            print(f"🗑️ Eliminado: {archivo}")
            total_eliminados += 1
        except Exception as e:
            print(f"⚠️ No se pudo eliminar {archivo}: {e}")

print(f"\\n✅ LIMPIEZA COMPLETADA")
print(f"🗑️ {total_eliminados} archivos eliminados")
print(f"📁 Todos los archivos han sido movidos a C:/GitHub/Baremo2025")
print(f"💾 Backup completo disponible en C:/GitHub/Baremo2025/backup")
'''

with open(repo_path / "cleanup_fct.py", "w", encoding="utf-8") as f:
    f.write(cleanup_script)
print("✅ Creado: cleanup_fct.py")

# Crear documentación básica
docs_content = '''# Metodología de Extracción

## Proceso de Análisis Forense

1. **Identificación de estructura** del PDF
2. **Localización de patrones** de datos
3. **Extracción precisa** manteniendo orden
4. **Validación** con datos conocidos
5. **Visualización** profesional

## Archivos por Especialidad

### Informática (107)
- **Páginas**: 2649-2697
- **Candidatos**: 343
- **Patrón**: `****XXXX* NOMBRE, TOTAL ...`

### Añadir Nueva Especialidad

1. Editar `config/especialidades.yaml`
2. Ejecutar análisis forense
3. Configurar páginas de inicio/fin
4. Ejecutar extractor
5. Generar visualización
'''

with open(repo_path / "docs" / "metodologia.md", "w", encoding="utf-8") as f:
    f.write(docs_content)
print("✅ Creado: docs/metodologia.md")

print(f"\n🎉 REPOSITORIO COMPLETO CREADO")
print(f"📁 Ubicación: {repo_path}")
print(f"💾 PDF original incluido en data/")
print(f"📊 Resultados finales en output/") 
print(f"📦 Backup completo en backup/")
print(f"\n🔄 Pasos siguientes:")
print(f"1. cd {repo_path}")
print(f"2. git init")
print(f"3. git add .")
print(f"4. git commit -m 'Initial commit: Baremo2025 - PDF mining toolkit'")
print(f"5. Ejecutar cleanup_fct.py para limpiar directorio FCT")

# Mostrar resumen de archivos
print(f"\n📋 RESUMEN DE ARCHIVOS MOVIDOS:")
print(f"   📄 PDFs: {len(glob.glob('*.pdf'))} archivos")
print(f"   🐍 Scripts: {len(glob.glob('*extractor*.py')) + len(glob.glob('baremo*.py'))} archivos")
print(f"   📊 Resultados: {len(glob.glob('*INFORMATICA*'))} archivos")
print(f"   💾 Total backup: {len(archivos_backup)} archivos")
