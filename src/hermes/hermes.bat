@echo off
setlocal enabledelayedexpansion

echo Creando estructura de Hermes en src\hermes ...
echo.

REM ================================
REM   Carpetas principales
REM ================================
mkdir src\hermes
mkdir src\hermes\core
mkdir src\hermes\gui
mkdir src\hermes\io
mkdir src\hermes\resources
mkdir src\hermes\utils

REM ================================
REM   Archivos base
REM ================================
type nul > src\hermes\__init__.py
type nul > src\hermes\main.py
type nul > src\hermes\config.py

type nul > src\hermes\core\__init__.py
type nul > src\hermes\core\dimensions.py
type nul > src\hermes\core\allocation.py
type nul > src\hermes\core\standards.py
type nul > src\hermes\core\validators.py

type nul > src\hermes\gui\__init__.py
type nul > src\hermes\gui\app.py
type nul > src\hermes\gui\main_window.py
type nul > src\hermes\gui\styles.py
type nul > src\hermes\gui\dialogs.py

type nul > src\hermes\io\__init__.py
type nul > src\hermes\io\excel_loader.py
type nul > src\hermes\io\exporters.py
type nul > src\hermes\io\resource_path.py

type nul > src\hermes\utils\__init__.py
type nul > src\hermes\utils\threading_utils.py
type nul > src\hermes\utils\logging_utils.py

echo Estructura creada con exito.
pause
