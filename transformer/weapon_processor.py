from typing import List
from pandas import DataFrame
from transformer.transformer import Transformer

class WeaponProcessor:
    def __init__(self):
        self.transformer = Transformer()

    async def process_extracted_data(self, list_of_dfs: List[DataFrame]) -> List[DataFrame]:
        """
        Recibe los DataFrames crudos de cualquier fuente, los limpia por separado
        y regresa la lista de DataFrames completamente pulidos.
        """ 
        if not list_of_dfs:
            print("⚠️ No se recibieron datos para procesar.")
            return []

        print(f"Procesando y puliendo {len(list_of_dfs)} datasets de juegos...")

        # 1 y 2. Limpieza estructural y mapeo por cada DataFrame
        dfs_cleaned = [self.transformer.clean_and_unify(df) for df in list_of_dfs]

        # 3. Sanitización de celdas (Texto a números, etc.)
        dfs_sanitiged = [self.transformer.apply_cell_cleaning(df) for df in dfs_cleaned]

        # 4. Ordenamiento estricto de columnas principales
        dfs_final = [self.transformer.sort_columns(df) for df in dfs_sanitiged]

        return dfs_final