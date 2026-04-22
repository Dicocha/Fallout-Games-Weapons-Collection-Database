from pathlib import Path
import pandas as pd

from format import Format
from maps import Maps


class Transformer:
    def __init__(self):
        self.root_folder = Path("./archive/")
        self.root_folder.parent.mkdir(parents=True, exist_ok=True)
        self.maps = Maps()
        self.format = Format()

    def clean_and_unify(self, df):
            new_df = df.copy()

            # 1. Drop junk
            junk = ['Unnamed', 'Form ID', 'CODE']
            cols_to_drop = [c for c in new_df.columns if any(p.lower() in c.lower() for p in junk)]
            new_df = new_df.drop(columns=cols_to_drop, errors='ignore')

            # 2. Map Columns (Search for substrings in the dictionary keys)
            mapping = {}
            for col in new_df.columns:
                target_name = None
                col_lower = col.lower()
                
                for key, standard in self.maps.stats_map.items(): # Usando la instancia de Maps
                    if key in col_lower:
                        target_name = standard
                        break
                
                # If no match in dict, just snake_case the original name
                mapping[col] = target_name if target_name else self.format.to_snake_case(col)

            new_df = new_df.rename(columns=mapping)

            # 3. IMPORTANT: Collapse duplicates
            # If the file had "Rifle name" AND "Pistol name", they are both "weapon_name" now.
            # This line merges them so you don't have two 'weapon_name' columns.
            new_df = new_df.loc[:, ~new_df.columns.duplicated()]

            return new_df

    def extract_and_transform(self):
            # Inicializamos listas para acumular datos
            games_list = self.maps.get_game_map()
            ammo_list = []
            types_list = []
            weapons_list = []
            stats_list = []

            for folder in sorted(self.root_folder.iterdir()):
                if folder.is_dir():
                    # Obtenemos el título del juego del nombre de la carpeta
                    game_title = folder.name.replace("_dataset", "").replace("_", " ").title()
                    game_title = "Fallout New Vegas" if game_title == "Fallout Newvegas" else game_title # Corrección específica para New Vegas

                    for file_path in folder.glob("*.csv"):
                        df = pd.read_csv(file_path, encoding="ISO-8859-1")
                        
                        # 1. Unificamos columnas (ej: 'pistol_name' -> 'weapon_name')
                        df = self.clean_and_unify(df)
                        
                        # 2. Identificar el tipo de arma por el nombre del archivo
                        w_type = file_path.stem.replace("_", " ").title()
                        w_type = self.maps.get_unified_type(w_type)
                        types_list.append({'type_name': w_type})

                        for _, row in df.iterrows():
                            # 3. Extraer y Limpiar Nombre del Arma
                            w_name = row.get('weapon_name') # Usamos el nombre unificado
                            
                            # Limpieza profunda (caracteres raros, espacios, etc.)
                            if pd.notna(w_name):
                                w_name = self.format.deep_clean_text(str(w_name))
                            
                            # Saltar si el nombre es nulo o quedó vacío tras la limpieza
                            if not w_name or str(w_name).lower() == 'nan':
                                continue

                            # 4. Extraer y Limpiar Munición
                            raw_ammo = row.get('ammo_type')
                            # Aplicamos unificación (ej: "MFC" -> "Microfusion Cell (MFC)")
                            ammo = self.maps.get_unified_ammo(raw_ammo)
                            
                            if pd.notna(ammo):
                                ammo_list.append({'ammo_name': str(ammo)})

                            # 5. Guardar relación Arma-Tipo
                            weapons_list.append({'name': w_name, 'type_name': w_type})
                            
                            # 6. Captura de métricas (Stats)
                            stats_list.append({
                                'game_title': game_title,
                                'weapon_name': w_name,
                                'ammo_name': ammo,
                                'damage': self.format.clean_data(row.get('damage'), 'damage'),
                                'weight': self.format.clean_data(row.get('weight'), 'weight'),
                                'value': self.format.clean_data(row.get('value'), 'value'),
                                'ap_cost': self.format.clean_data(row.get('ap_cost'), 'ap_cost'),
                                'fire_rate': self.format.clean_data(row.get('fire_rate'), 'fire_rate'),
                                'range': self.format.clean_data(row.get('range'), 'range'),
                                'accuracy': self.format.clean_data(row.get('accuracy'), 'accuracy'),
                                'magazine_capacity': self.format.clean_data(row.get('magazine_capacity'), 'magazine_capacity'),
                                'strength_required': self.format.clean_data(row.get('strength_required'), 'strength_required')
                            })

            # Retornamos el diccionario final para el Loader
            return {
                'games': pd.DataFrame(games_list).drop_duplicates(),
                'ammo_types': pd.DataFrame(ammo_list).drop_duplicates(),
                'weapon_types': pd.DataFrame(types_list).drop_duplicates(),
                'weapons': pd.DataFrame(weapons_list).drop_duplicates(subset=['name']),
                'game_weapon_stats': pd.DataFrame(stats_list),
            }