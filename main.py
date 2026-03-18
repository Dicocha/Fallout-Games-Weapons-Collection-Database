from transformer import Transformer
from loader import Loader
from extractor import Extractor
from pathlib import Path

def main():
    # 1. Initialize
    extractor = Extractor()
    transformer = Transformer()
    loader = Loader()

    # 2. Run ETL
    print("Starting ETL Process...")
    print("Downloading dataset...")
    if not Path("./archive").exists():
        extractor.download()

    print("Transforming data...")
    df = transformer.extract_and_transform()

    # 3. Load
    print("Loading data into SQL file...")
    loader.to_sql_file(df)

if __name__ == "__main__":
    main()