from pathlib import Path
from transformer import Transformer
from loader import Loader
from extractor import Extractor

def main():
    # 1. Inicialización
    extractor = Extractor()
    transformer = Transformer()
    loader = Loader()

    # 2. Ejecución del ETL
    print("🚀 Iniciando proceso ETL...")
    
    # Simulación de descarga si no existe la carpeta
    archive_path = Path("./archive")
    if not archive_path.exists():
        print("📥 Descargando dataset...")
        extractor.download() 
    else:
        print("📂 Usando archivos locales de './archive'...")

    print("🛠️ Transformando y Normalizando datos...")
    data_dict = transformer.extract_and_transform()

    # 3. Carga
    print("💾 Generando script SQL Relacional...")
    loader.to_sql_file(data_dict)
    #loader.view_data(data_dict) # Descomenta para ver los DataFrames limpios en un txt
    
    print("\n✅ Proceso completado con éxito.")
    print(f"📍 Tu base de datos está lista en: {loader.output_path}")

if __name__ == "__main__":
    main()