import asyncio

import kagglehub
import pandas as pd
from pandas import DataFrame
from typing import List
from pathlib import Path
from utils.format import Format

class KaggleExtractor:
    def __init__(self):
        self.handle = "wassimouledmohamed/fallout-new-vegas-weapons-dataset"
        self.local_path = Path("./archive")
        self.format = Format()

    def download(self):
        # This downloads the dataset and returns the local path to the folder
        kagglehub.dataset_download(self.handle, output_dir=self.local_path)
        print("Download complete. Dataset is available at:", self.local_path)

    def _sync_process_folder(self, folder: Path) -> DataFrame:
        """Lee los CSVs de una carpeta, les pone el título del juego y guarda un backup por juego."""
        dfs_of_folder = [] # MEJORA: Guardamos los dataframes en una lista primero
        game_title = self.format.format_file_name(folder.name)

        for file_path in folder.glob("*.csv"):
            
            try:
                temp_df = pd.read_csv(file_path, encoding="ISO-8859-1")

            except Exception as e:
                print(f"⚠️ Error leyendo {file_path.name} del juego {game_title}: {e}")
                continue

            temp_df.columns = temp_df.columns.str.lower().str.strip()

            # Agregamos las columnas de contexto
            temp_df['weapon_type'] = file_path.stem  # Ej: "pistols", "rifles"
            temp_df['game_title'] = game_title # Ej: "fallout_new_vegas"

            dfs_of_folder.append(temp_df)

        # --- OPTIMIZACIÓN DE CONCAT ---
        # En lugar de hacer pd.concat en cada iteración del bucle (que es lento y causa errores de indexación),
        # hacemos un único concat global de todos los archivos de esta carpeta al final.
        if dfs_of_folder:
            df = pd.concat(dfs_of_folder, ignore_index=True)
        else:
            df = pd.DataFrame()

        return df

    async def process_folder(self, folder: Path) -> List[DataFrame]:
        return await asyncio.to_thread(self._sync_process_folder, folder)

    async def extract(self) -> List[DataFrame]:
        """Cumple con la interfaz de extracción regresando la lista de DataFrames crudos"""
        folders = [folder for folder in self.local_path.iterdir() if folder.is_dir()]
        print(f"Iniciando extracción asíncrona de {len(folders)} carpetas de Kaggle...")
        all_dfs = await asyncio.gather(*(self.process_folder(folder) for folder in folders))
        return all_dfs