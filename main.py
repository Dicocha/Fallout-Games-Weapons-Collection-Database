import asyncio
from loader import csv_loader
from transformer.source_sanitizer import SourceSanitizer  # Nuevo Módulo
from extractor.kaggle_extractor import KaggleExtractor
from transformer.weapon_processor import WeaponProcessor
from loader.csv_loader import CSVLoader

async def main():
    
    # 0. FASE PRE-EXTRACT (Limpia los CSV corruptos de raíz)
    sanitizer = SourceSanitizer()
    sanitizer.sanitize_all_sources()
    
    # 1. Extracción Pura (Ahora lee archivos perfectos sin comas dobles)
    extractor = KaggleExtractor()
    raw_dataframes = await extractor.extract()
    
    # 2. Transformación Pura (Mapeo por RegEx + Sanitización de celdas)
    processor = WeaponProcessor()
    processed_dfs = await processor.process_extracted_data(raw_dataframes)
    
    # 4. Carga Pura Paralela
    csv_loader = CSVLoader()
    await asyncio.gather(*(csv_loader.load(df) for df in processed_dfs))
    
    print("🎉 ¡Pipeline finalizado con éxito!")

if __name__ == "__main__":
    asyncio.run(main())