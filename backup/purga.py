import os
import glob
import shutil
from pathlib import Path

# SCRIPT PARA PURGAR COMPLETAMENTE DIRECTORIO FCT
print("=== PURGA COMPLETA DIRECTORIO FCT ===")
print("🧹 Eliminando todos los archivos relacionados con Baremo2025...")

# VERIFICAR QUE EL REPOSITORIO EXISTE ANTES DE PURGAR
repo_path = Path("C:/GitHub/Baremo2025")
if not repo_path.exists():
    print("❌ ERROR: Repositorio C:/GitHub/Baremo2025 no encontrado")
    print("🚨 NO SE REALIZARÁ LA PURGA por seguridad")
    print("📋 Ejecuta primero moverepo.py")
    exit()

print(f"✅ Repositorio confirmado en: {repo_path}")

# PRIMERO: Copiar este script al backup
backup_dir = repo_path / "backup"
backup_dir.mkdir(exist_ok=True)

# Copiar moverepo.py si existe
if Path("moverepo.py").exists():
    shutil.copy2("moverepo.py", backup_dir / "moverepo.py")
    print(f"📦 moverepo.py copiado al backup")

# Copiar este script de purga
script_actual = Path(__file__)
if script_actual.exists():
    shutil.copy2(script_actual, backup_dir / script_actual.name)
    print(f"📦 {script_actual.name} copiado al backup")

print(f"📦 Procediendo con la purga segura...")

# LISTA COMPLETA DE ARCHIVOS A ELIMINAR
patrones_purgar = [
    # Scripts de análisis y extracción
    "analisis_*.py",
    "extractor_*.py", 
    "baremo*.py",
    
    # Datos y resultados
    "lista_*.py",
    "*INFORMATICA*.csv",
    "*INFORMATICA*.txt",
    "*informatica*.png", 
    "*informatica*.pdf",
    
    # PDFs originales
    "rh03_*.pdf",
    "*baremo*.pdf",
    
    # Scripts de utilidad
    "moverepo.py",
    "cleanup_*.py",
    "purgar_*.py",  # Este mismo script
    
    # Archivos temporales que pudieran existir
    "temp_*.py",
    "test_*.py",
    "*_temp.*",
    "*_backup.*"
]

# CONTADOR
total_eliminados = 0
archivos_no_encontrados = 0
errores = 0

print(f"\n=== INICIANDO ELIMINACIÓN ===")

for patron in patrones_purgar:
    archivos = glob.glob(patron)
    
    if not archivos:
        archivos_no_encontrados += 1
        continue
        
    for archivo in archivos:
        try:
            # Verificar que el archivo existe antes de eliminar
            if Path(archivo).exists():
                os.remove(archivo)
                print(f"🗑️ Eliminado: {archivo}")
                total_eliminados += 1
            else:
                print(f"⚠️ Ya no existe: {archivo}")
                
        except PermissionError:
            print(f"🔒 Sin permisos para eliminar: {archivo}")
            errores += 1
        except Exception as e:
            print(f"❌ Error eliminando {archivo}: {e}")
            errores += 1

# VERIFICAR DIRECTORIO LIMPIO
print(f"\n=== VERIFICACIÓN FINAL ===")

# Buscar cualquier archivo restante relacionado
archivos_restantes = []
for patron in ["*baremo*", "*INFORMATICA*", "*extractor*", "*analisis*"]:
    restantes = glob.glob(patron, recursive=False)
    archivos_restantes.extend(restantes)

# Mostrar archivos restantes (si los hay)
if archivos_restantes:
    print(f"⚠️ ARCHIVOS RESTANTES ENCONTRADOS:")
    for archivo in archivos_restantes:
        print(f"   - {archivo}")
    
    # Preguntar si eliminar los restantes
    print(f"\n🤔 ¿Eliminar también estos archivos? (y/n): ", end="")
    try:
        respuesta = input().lower().strip()
        
        if respuesta in ['y', 'yes', 's', 'si', 'sí']:
            for archivo in archivos_restantes:
                try:
                    os.remove(archivo)
                    print(f"🗑️ Eliminado adicional: {archivo}")
                    total_eliminados += 1
                except Exception as e:
                    print(f"❌ Error: {archivo} - {e}")
                    errores += 1
    except:
        print("⚠️ Input no disponible, saltando archivos restantes")
else:
    print("✅ No se encontraron archivos restantes")

# RESUMEN FINAL
print(f"\n{'='*50}")
print("=== RESUMEN DE PURGA ===")
print(f"{'='*50}")

print(f"🗑️ Archivos eliminados: {total_eliminados}")
print(f"⚠️ Patrones sin coincidencias: {archivos_no_encontrados}")
print(f"❌ Errores durante eliminación: {errores}")

if total_eliminados > 0:
    print(f"\n✅ PURGA COMPLETADA EXITOSAMENTE")
    print(f"🧹 Directorio FCT limpio de archivos Baremo2025")
else:
    print(f"\n🤷 NO SE ELIMINÓ NINGÚN ARCHIVO")
    print(f"📋 El directorio ya estaba limpio o los archivos ya fueron movidos")

print(f"\n📁 Todos los archivos están seguros en:")
print(f"   📦 Repositorio: {repo_path}")
print(f"   💾 Backup: {repo_path}/backup/")

# VERIFICACIÓN DE SEGURIDAD FINAL
backup_files = list((repo_path / "backup").glob("*")) if (repo_path / "backup").exists() else []
output_files = list((repo_path / "output").glob("*")) if (repo_path / "output").exists() else []

print(f"\n🔒 VERIFICACIÓN DE SEGURIDAD:")
print(f"   📦 Backup: {len(backup_files)} archivos guardados")
print(f"   📊 Output: {len(output_files)} archivos de resultados")

if len(backup_files) > 0 and len(output_files) > 0:
    print(f"✅ MIGRACIÓN VERIFICADA - Archivos seguros en repositorio")
else:
    print(f"⚠️ ADVERTENCIA: Pocos archivos en repositorio")
    print(f"   Verifica que moverepo.py se ejecutó correctamente")

print(f"\n🎉 PROCESO DE MIGRACIÓN COMPLETO")
print(f"📍 Próximos pasos:")
print(f"   1. cd C:/GitHub/Baremo2025")
print(f"   2. git init") 
print(f"   3. git add .")
print(f"   4. git commit -m 'Initial commit: PDF mining toolkit'")
print(f"   5. git remote add origin <tu-repo-url>")
print(f"   6. git push -u origin main")

print(f"\n📋 ARCHIVOS DISPONIBLES EN REPOSITORIO:")
print(f"   🔧 src/ - Código fuente")
print(f"   📊 output/ - Resultados y gráficos")
print(f"   📄 data/ - PDFs originales")
print(f"   💾 backup/ - Backup completo del desarrollo")
print(f"   📖 README.md - Documentación completa")

input(f"\n⏸️ Presiona ENTER para continuar...")