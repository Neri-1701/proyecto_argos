# Archivo Histórico de ARGOS

## Propósito del directorio `archive/`

El directorio `archive/` conserva implementaciones previas, prototipos,
versiones descontinuadas y artefactos técnicos que formaron parte de la
evolución del sistema ARGOS, pero que ya no representan la arquitectura
actual. Su función es exclusivamente histórica y referencial.

Nada dentro de este directorio debe considerarse productivo ni
mantenerse en uso dentro del flujo de desarrollo vigente.

------------------------------------------------------------------------

## Estructura general

Cada subcarpeta en `archive/` agrupa un componente o módulo en su
versión previa a la integración formal del sistema.

Ejemplo:

    archive/
    └── hermes_all_in_one/
        ├── hermes_AIO_v0.1.0.py
        ├── notas_migracion.md
        └── screenshots/

------------------------------------------------------------------------

## Hermes All-in-One

La carpeta `hermes_all_in_one/` almacena la primera versión completa y
funcional de Hermes, implementada como un único script monolítico. Esta
versión incluía en un solo archivo:

-   extracción de dimensiones (diámetro y longitud),
-   procesamiento de DataFrames,
-   reglas de asignación de inventario,
-   interfaz gráfica con Tkinter,
-   exportación a Excel,
-   manejo simultáneo de inventario y Visiflex.

------------------------------------------------------------------------

## Lineamientos de uso

1.  No importar código desde `archive/` hacia `src/`.
2.  No modificar ni refactorizar contenido dentro de este directorio.
3.  No agregar nuevas funciones aquí; sólo material histórico.
4.  Si surge una versión experimental que luego se reemplaza, debe
    archivarse aquí.
5.  Este directorio no forma parte de distribuciones finales ni
    empaquetados.

------------------------------------------------------------------------

## Estado actual

-   `hermes_all_in_one/` contiene Hermes v0.2.0 en su versión monolítica
    original.

    Hermes v0.2.1 agrega un message box para que el usuario diga que busca en específico y este busque inteligentemente en inventario.
