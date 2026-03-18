# Fallout Games Weapons Collection Database ☢️

A professional ETL (Extract, Transform, Load) pipeline that converts messy, inconsistent weapon data from the Fallout franchise into a clean, unified Relational SQL database.

## 🚀 Project Overview
This project automates the transition from flat `.csv` files (found in game archives) to a structured SQL format. It handles the "data wild west" of the Fallout series, where different games use different naming conventions for the same attributes (e.g., "Weight" vs "Weapon weight (lbs)").

### Key Features:
* **Data Unification:** Collapses over 40+ different column headers into a standardized schema (e.g., `ammo_type`, `magazine_capacity`, `ap_cost`).
* **Automatic Normalization:** Generates a relational structure with a dedicated `weapon_type` lookup and individual game tables.
* **Data Sanitization:** Cleans encoding artifacts (like `Â²`), strips units (like `lbs` or `hp`), and handles SQL reserved words using bracketed identifiers `[]`.
* **Professional SQL Output:** Generates a complete `.sql` script with `CREATE TABLE` schemas and `INSERT` statements ready for SQLite, PostgreSQL, or SQL Server.

## 🛠️ The Tech Stack
* **Language:** Python 3.x
* **Data Library:** Pandas (for heavy-duty data transformation)
* **Regex:** Advanced pattern matching for column mapping and string cleaning.
* **Database:** SQL (Standard Relational Schema).

## 🗄️ Database Schema
The generated database includes tables for:
* `fallout_2`
* `fallout_3`
* `fallout_4`
* `fallout_76`
* `fallout_new_vegas`
* `weapon_type` (Categorical metadata)

### Example Standardized Columns:
| Standard Column | Source Variations Found |
| :--- | :--- |
| `weapon_name` | `Name`, `Pistol name`, `Weapon`, `Rifle name` |
| `ap_cost` | `Action point cost`, `AP`, `Cost` |
| `magazine_capacity` | `Magazine`, `Capacity`, `Shots per reload` |
| `value` | `Caps`, `Selling Price`, `Value` |

## ⚙️ How to Run
1. Place your game CSV datasets in the `./archive/` folder.
2. Run the pipeline:
   ```bash
   python main.py
