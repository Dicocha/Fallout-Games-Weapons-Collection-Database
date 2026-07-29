# transformer/transformer.py
from pathlib import Path
import re
import pandas as pd
from utils.format import Format
from utils.maps import Maps

class Transformer:
    def __init__(self):
        self.maps = Maps()
        self.format = Format()

    def sort_columns(self, df):
        cols = df.columns.tolist()
        for col in ['weapon_name', 'game_title']:
            if col in cols:
                cols.insert(0, cols.pop(cols.index(col)))
        return df[cols]

    def clean_and_unify(self, df):
        new_df = df.copy()

        # 1. Eliminamos de golpe filas y columnas vacías (Tu excelente práctica)
        new_df.dropna(axis=1, how='all', inplace=True)
        new_df.dropna(axis=0, how='all', inplace=True)
        
        # 2. Mapeo dinámico usando Expresiones Regulares
        mapping = {}
        pipeline_reserved_cols = ['game_title', 'weapon_type']

        for col in new_df.columns:
            if col in pipeline_reserved_cols:
                mapping[col] = col
                continue

            col_normalized = self.format.to_snake_case(col)
            target_name = None
            
            for standard_name, regex_pattern in self.maps.regex_stats_map.items():
                if regex_pattern.match(col_normalized):
                    target_name = standard_name
                    break
            
            mapping[col] = target_name if target_name else col_normalized

        new_df = new_df.rename(columns=mapping)

        # Si había desfases remanentes de otras columnas unnamed, hacemos el fillna de seguridad
        if 'weapon_name' in new_df.columns:
            unnamed_candidate_cols = [c for c in new_df.columns if str(c).startswith('unnamed_')]
            for unnamed_col in unnamed_candidate_cols:
                new_df['weapon_name'] = new_df['weapon_name'].fillna(new_df[unnamed_col])

        junk_patterns = [r'unnamed_']
        cols_to_drop = [
            c for c in new_df.columns 
            if any(re.search(pattern, str(c).lower()) for pattern in junk_patterns)
        ]
        new_df = new_df.drop(columns=cols_to_drop, errors='ignore')

        if new_df.columns.duplicated().any():
            new_df = new_df.T.groupby(level=0).first().T
        
        return new_df

    def apply_cell_cleaning(self, df):
        """
        NUEVO MÉTODO: Aplica la función clean_data de format.py en bloque
        para limpiar los textos y convertirlos a flotantes/ints donde corresponda.
        """
        cleaned_df = df.copy()
        
        # Iteramos sobre las columnas para aplicar la vectorización de Pandas (Series.apply)
        for col in cleaned_df.columns:
            if col in ['game_title', 'weapon_type', 'upgrades', 'shoot_modes', 'components']:
                continue  # No limpiamos estas columnas de contexto
            
            # Mandamos el valor de la celda y el nombre de la columna a tu utilidad clean_data
            cleaned_df[col] = cleaned_df[col].apply(lambda val: self.format.clean_data(val, col))
            
            # Si limpiamos la columna de munición, le pasamos también tu limpiador especializado
            if col == 'ammo_name':
                cleaned_df[col] = cleaned_df[col].apply(self.format.clean_ammo_string)
                
        return cleaned_df