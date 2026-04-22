from pathlib import Path
import pandas as pd
import inspect

class Loader:
    def __init__(self, output_path="./output/fallout_weapons.sql"):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def create_relational_queries(self, data_dict):
        queries = []

        def escape(val):
            return str(val).replace("'", "''")

        def sql_val(val):
            if pd.isna(val) or val is None: return "NULL"
            return f"'{escape(val)}'"

        def sql_num(val):
            if pd.isna(val) or val is None: return "NULL"
            return val

        # 1. INSERT GAMES (Insert masivo)
        queries.append("\n-- ----------------------------\n-- SECCIÓN: JUEGOS\n-- ----------------------------")
        game_rows = [
            f"('{escape(r['title'])}', {sql_num(r['release_year'])}, '{escape(r['studio'])}')" 
            for _, r in data_dict['games'].iterrows()
        ]
        if game_rows:
            queries.append(f"INSERT INTO games (title, release_year, studio) VALUES \n    {',\n    '.join(game_rows)}\nON CONFLICT (title) DO NOTHING;")

        # 2. INSERT TYPES (Weapon & Ammo)
        queries.append("\n-- ----------------------------\n-- SECCIÓN: CATÁLOGOS\n-- ----------------------------")
        type_rows = [f"('{escape(t)}')" for t in data_dict['weapon_types']['type_name']]
        if type_rows:
            queries.append(f"INSERT INTO weapon_types (type_name) VALUES \n    {',\n    '.join(type_rows)}\nON CONFLICT (type_name) DO NOTHING;\n")

        ammo_rows = [f"('{escape(a)}')" for a in data_dict['ammo_types']['ammo_name'] if pd.notna(a)]
        if ammo_rows:
            queries.append(f"INSERT INTO ammo_types (ammo_name) VALUES \n    {',\n    '.join(ammo_rows)}\nON CONFLICT (ammo_name) DO NOTHING;")

        # 3. INSERT WEAPONS
        queries.append("\n-- ----------------------------\n-- SECCIÓN: ARMAS (CATÁLOGO ÚNICO)\n-- ----------------------------")
        for _, row in data_dict['weapons'].iterrows():
            queries.append(f"INSERT INTO weapons (name, base_type_id) \n    SELECT '{escape(row['name'])}', type_id \n    FROM weapon_types WHERE type_name = '{escape(row['type_name'])}' ON CONFLICT (name) DO NOTHING;\n")

# 4. INSERT STATS (Corregido para PostgreSQL)
        queries.append("\n-- ----------------------------\n-- SECCIÓN: ESTADÍSTICAS POR JUEGO\n-- ----------------------------")
        for _, row in data_dict['game_weapon_stats'].iterrows():
            # Usamos JOIN explícitos para evitar el error de sintaxis en el FROM
            query = f"""INSERT INTO game_weapon_stats (game_id, weapon_id, ammo_id, damage, weight, weapon_value, ap_cost, fire_rate, weapon_range, accuracy, magazine_capacity, strength_required)
SELECT 
    g.game_id, 
    w.weapon_id, 
    a.ammo_id, 
    {sql_num(row['damage'])}, 
    {sql_num(row['weight'])}, 
    {sql_num(row['value'])}, 
    {sql_num(row['ap_cost'])}, 
    {sql_num(row['fire_rate'])}, 
    {sql_num(row['range'])}, 
    {sql_num(row['accuracy'])}, 
    {sql_num(row['magazine_capacity'])}, 
    {sql_num(row['strength_required'])}
FROM games g
CROSS JOIN weapons w
LEFT JOIN ammo_types a ON a.ammo_name = {sql_val(row['ammo_name'])}
WHERE g.title = {sql_val(row['game_title'])} 
  AND w.name = {sql_val(row['weapon_name'])};\n"""
            queries.append(query)

        return queries

    def to_sql_file(self, data_dict):
        all_queries = self.create_relational_queries(data_dict)

        schema_postgres = inspect.cleandoc('''
            -- Limpieza de tablas existentes (orden inverso por llaves foráneas)
            DROP TABLE IF EXISTS game_weapon_stats CASCADE;
            DROP TABLE IF EXISTS weapons CASCADE;
            DROP TABLE IF EXISTS weapon_types CASCADE;
            DROP TABLE IF EXISTS ammo_types CASCADE;
            DROP TABLE IF EXISTS games CASCADE;

            -- Creación de Tablas
            CREATE TABLE games (
                game_id SERIAL PRIMARY KEY,
                title VARCHAR(255) UNIQUE NOT NULL,
                release_year INT,
                studio VARCHAR(100)
            );

            CREATE TABLE ammo_types (
                ammo_id SERIAL PRIMARY KEY,
                ammo_name VARCHAR(100) UNIQUE NOT NULL
            );

            CREATE TABLE weapon_types (
                type_id SERIAL PRIMARY KEY,
                type_name VARCHAR(100) UNIQUE NOT NULL
            );

            CREATE TABLE weapons (
                weapon_id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                base_type_id INT REFERENCES weapon_types(type_id) ON DELETE SET NULL
            );

            CREATE TABLE game_weapon_stats (
                stat_id SERIAL PRIMARY KEY,
                game_id INT REFERENCES games(game_id) ON DELETE CASCADE,
                weapon_id INT REFERENCES weapons(weapon_id) ON DELETE CASCADE,
                ammo_id INT REFERENCES ammo_types(ammo_id) ON DELETE SET NULL,
                damage DECIMAL,
                weight DECIMAL,
                weapon_value INT,
                ap_cost INT,
                fire_rate DECIMAL,
                weapon_range DECIMAL, -- Cambiado a DECIMAL por precisión
                accuracy DECIMAL,
                magazine_capacity INT,
                strength_required INT
            );
        ''')

        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write("-- Script generado para PostgreSQL\n")
            f.write("BEGIN;\n\n")
            f.write(schema_postgres)
            f.write("\n\n" + "\n".join(all_queries))
            f.write("\n\nCOMMIT;")
