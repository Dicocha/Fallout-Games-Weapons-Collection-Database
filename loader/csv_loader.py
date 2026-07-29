import asyncio
from pathlib import Path
from pandas import DataFrame
from loader.base import BaseLoader

class CSVLoader(BaseLoader):
    """Estrategia para guardar en archivos CSV planos locales para Power BI"""
    
    def _sync_write(self, df: DataFrame) -> None:
        # Obtenemos el título de la columna de manera segura
        game_title = df['game_title'].iloc[0] if 'game_title' in df.columns else "unknown_game"
        
        # Normalizamos el nombre para el archivo físico (ej: "Fallout New Vegas" -> "fallout_new_vegas")
        file_name = game_title.lower().replace(" ", "_")
        
        output_path = Path(f"./output/csv/{file_name}.csv")

        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"💾 Generando el archivo CSV: {game_title} -> {output_path.name}")

    async def load(self, df: DataFrame) -> None:
        if df.empty: return
        # Mandamos la escritura síncrona a un hilo asíncrono
        await asyncio.to_thread(self._sync_write, df)