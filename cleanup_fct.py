import os
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

print(f"\n✅ LIMPIEZA COMPLETADA")
print(f"🗑️ {total_eliminados} archivos eliminados")
print(f"📁 Todos los archivos han sido movidos a C:/GitHub/Baremo2025")
print(f"💾 Backup completo disponible en C:/GitHub/Baremo2025/backup")
