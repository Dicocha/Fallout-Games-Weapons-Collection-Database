from pathlib import Path

import pandas as pd
import re

class Transformer:
    def __init__(self):
        self.root_folder = Path("./archive/")
        self.unify_map = {
            'name': 'weapon_name',
            'weapon': 'weapon_name',
            'damage': 'damage',
            'weight': 'weight',
            'value': 'value',
            'caps': 'value',
            'selling price': 'value',
            'cost': 'ap_cost',
            'action point': 'ap_cost',
            'ammo': 'ammo_type',
            'ammunition': 'ammo_type',
            'range': 'range',
            'fire rate': 'fire_rate',
            'rate of fire': 'fire_rate',
            'accuracy': 'accuracy',
            'magazine': 'magazine_capacity',
            'capacity': 'magazine_capacity',
            'skill': 'skill_required',
            'strength': 'strength_required',
            'multiplier': 'critical_chance_multiplier',
            'special': 'special',
            'upgrades': 'upgrades',
            'components': 'components',
            'modes': 'attack_modes',
            'speed': 'fire_rate'
        }

    def to_snake_case(self, text):
        """Strictly follows Object snake_case convention."""
        if not text: return "Unnamed"
        # Remove parentheses and non-alphanumeric, then underscore
        text = re.sub(r'\(.*?\)', '', str(text)) 
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text.lower().strip().replace(" ", "_")

    def clean_data_string(self, value):
        if pd.isna(value):
            return None

        val_str = str(value).strip()

        if val_str.lower() in ['nan', 'none', '', 'null']:
            return None

        val_str = val_str.encode("ascii", "ignore").decode("ascii")

        # Extrae número si existe
        match = re.search(r'[-+]?\d*\.?\d+', val_str)
        if match:
            return match.group()

        return val_str

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
                
                for key, standard in self.unify_map.items():
                    if key in col_lower: # Substring match
                        target_name = standard
                        break
                
                # If no match in dict, just snake_case the original name
                mapping[col] = target_name if target_name else self.to_snake_case(col)

            new_df = new_df.rename(columns=mapping)

            # 3. IMPORTANT: Collapse duplicates
            # If the file had "Rifle name" AND "Pistol name", they are both "weapon_name" now.
            # This line merges them so you don't have two 'weapon_name' columns.
            new_df = new_df.loc[:, ~new_df.columns.duplicated()]

            return new_df

    def extract_and_transform(self):
        tables = {}
        for folder in sorted(self.root_folder.iterdir()):
            if folder.is_dir():
                game_table_name = self.to_snake_case(folder.name.replace("_dataset", ""))
                weapon_dfs = []

                for file_path in folder.glob("*.csv"):
                    df = pd.read_csv(file_path, encoding="ISO-8859-1")
                    df = self.clean_and_unify(df)
                    
                    # Add your specific string-based metadata
                    df['game_name'] = game_table_name
                    df['weapon_type'] = file_path.stem.replace("_", " ").title()
                    
                    # Clean the data cells
                    for col in df.columns:
                        if col not in ['game_name', 'weapon_type']:
                            # Correct: Pass the function reference, NOT the function call with ()
                            df[col] = df[col].apply(self.clean_data_string)
                    
                    weapon_dfs.append(df)

                if weapon_dfs:
                    final_df = pd.concat(weapon_dfs, ignore_index=True)
                    # Force 'id' to be the first column
                    final_df.index.name = 'id'
                    tables[game_table_name] = final_df.reset_index()

        return tables