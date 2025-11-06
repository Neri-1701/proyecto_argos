import os
import sys
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
venv_path = root / ".venv"

# --- Validar versión de Python ---
if not sys.version.startswith("3.12"):
    print("Este proyecto requiere Python 3.12.x")
    sys.exit(1)

def run(cmd):
    print(f"→ {cmd}")
    subprocess.run(cmd, shell=True, check=True)

print(f"\nConfigurando entorno virtual en {venv_path}")

# 1️⃣ Crear entorno si no existe
if not venv_path.exists():
    run(f'"{sys.executable}" -m venv "{venv_path}"')

else:
    print("Entorno virtual ya existente.\n")

# 2️⃣ Instalar dependencias base
pip = venv_path / "Scripts" / "pip.exe"
run(f"{pip} install --upgrade pip")
run(f"{pip} install pandas numpy matplotlib seaborn jupyter ipykernel python-dotenv")

# 3️⃣ Registrar kernel Jupyter
python = venv_path / "Scripts" / "python.exe"
run(f"{python} -m ipykernel install --user --name=argos_env --display-name 'Python (ARGOS)'")

# 4️⃣ Crear estructura base
folders = [
    "data/external", "data/interim", "data/processed/familias",
    "notebooks", "src/data", "src/models", "src/utils",
    "reports/figures", "tests", "docs", "plantillas"
]
for f in folders:
    p = root / f
    p.mkdir(parents=True, exist_ok=True)
    (p / ".gitkeep").touch(exist_ok=True)

print("\nARGOS listo para usar con Python 3.12.\n")
