# Fallout Weapons Relational ETL ☢️

Un pipeline profesional de **Extracción, Transformación y Carga (ETL)** que convierte el "caos de datos" de la franquicia Fallout (archivos .csv inconsistentes) en una base de datos relacional robusta y normalizada para **PostgreSQL**.

## 🚀 Resumen del Proyecto
Este proyecto soluciona el problema de la fragmentación de datos en la saga Fallout. Cada juego utiliza convenciones distintas (ej: "Weight" vs "Lbs"), pero este pipeline unifica más de 50 columnas diferentes en un esquema relacional de 3ª Forma Normal (3NF).

### ✨ Características Principales:
* **Normalización Agresiva:** Separa los datos en tablas maestras (`games`, `ammo_types`, `weapon_types`) para eliminar la redundancia.
* **Limpieza Profunda (Data Sanitization):** Elimina artefactos de encoding (como `Â²`), limpia caracteres especiales de Fallout 76 y estandariza nombres de munición.
* **Mapeo Inteligente:** Unifica más de 40 variantes de encabezados (ej: `pistol_name`, `rifle_name` -> `weapon_name`).
* **PostgreSQL Ready:** Salida optimizada para PostgreSQL con soporte de transacciones (`BEGIN/COMMIT`), `SERIAL` types y manejo de conflictos (`ON CONFLICT DO NOTHING`).

## 🛠️ Tech Stack
* **Python 3.x**
* **Pandas:** Motor principal de transformación de datos.
* **PostgreSQL:** Destino de la base de datos relacional.
* **Docker:** (Opcional) Recomendado para correr la DB.

## 🗄️ Modelo Relacional
El pipeline genera un script SQL con la siguiente estructura:

* `games`: Información de los títulos (Fallout 2, 3, 4, NV, 76).
* `weapon_types`: Categorías unificadas (Melee, Pistols, Heavy Weapons, etc.).
* `ammo_types`: Catálogo estandarizado de munición (ej: "Microfusion Cell (MFC)").
* `weapons`: Catálogo único de armas vinculadas a su tipo base.
* `game_weapon_stats`: La tabla de hechos que contiene el daño, peso y valor de cada arma por juego.



## ⚙️ Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   [git clone [https://github.com/Dicocha/Fallout-Games-Weapons-Collection-Database](https://github.com/Dicocha/fallout-etl.git)](https://github.com/Dicocha/Fallout-Games-Weapons-Collection-Database.git)
   cd fallout-etl
