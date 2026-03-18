from pathlib import Path
import pandas as pd

class Loader:
    def __init__(self, output_path="./output/fallout_weapons.sql"):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        # Standard SQL Reserved words often found in your data: 
        # range, value, special, group, order, table, connection
    
    def create_queries(self, tables_dict):
        schema_queries = []
        data_queries = []

        # Sort keys to maintain a consistent output order
        sorted_tables = sorted(tables_dict.keys())

        for table_name in sorted_tables:
            df = tables_dict[table_name]
            
            # 1. SCHEMA DEFINITION
            cols_list = []
            for col in df.columns:
                # Wrap column names in [] to avoid reserved word errors (e.g., [range])
                if col.lower() == 'id':
                    cols_list.append(f"    [{col}] INTEGER PRIMARY KEY")
                else:
                    cols_list.append(f"    [{col}] TEXT")
            
            cols_def = ",\n".join(cols_list)
            # Wrap table names in [] as well
            schema_queries.append(f"-- Table Structure for [{table_name}]\n"
                                 f"CREATE TABLE IF NOT EXISTS [{table_name}] (\n{cols_def}\n);\n")
            
            # 2. DATA INSERTIONS
            # Build the column list once for this table
            col_names_str = ", ".join([f"[{c}]" for c in df.columns])
            
            data_queries.append(f"-- Data for [{table_name}]")
            for _, row in df.iterrows():
                values = []
                for val in row:
                    if pd.isnull(val) or str(val).lower() == 'nan':
                        values.append("NULL")
                    else:
                        # Escape single quotes and convert to string
                        clean_val = str(val).replace("'", "''")
                        values.append(f"'{clean_val}'")
                
                query = f"\nINSERT INTO [{table_name}] ({col_names_str}) VALUES ({', '.join(values)});"
                data_queries.append(query)
            
            # Add a separator between tables
            data_queries.append("") 

        return schema_queries, data_queries

    def to_sql_file(self, tables_dict):
        schemas, data = self.create_queries(tables_dict)
        
        with open(self.output_path, "w", encoding="utf-8") as f:
            # Metadata Header
            f.write("/*\n" + "="*50 + "\n")
            f.write("   FALLOUT FRANCHISE WEAPONS DATABASE\n")
            f.write(f"   Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n*/\n\n")
            
            f.write("PRAGMA foreign_keys = ON;\n\n") # Enable FKs for SQLite compatibility
            
            f.write("-- 1. SCHEMAS\n")
            f.write("-" * 20 + "\n")
            f.write("\n".join(schemas))
            
            f.write("\n\n-- 2. DATA INSERTIONS\n")
            f.write("-" * 20 + "\n")
            f.write("\n".join(data))
                
        print(f"✅ Professional SQL script generated at: {self.output_path}")