import pandas as pd
import re

class Format:
    def __init__(self):
        pass

    def deep_clean_text(self, text):
        """Elimina artefactos de encoding y normaliza separadores de munición."""
        if not text or pd.isna(text): return None
        
        # 1. Corregir artefactos comunes de encoding mal interpretado
        text = str(text).replace('Â', '').replace('â€¢', '·').replace('Â·', '·').replace('²', '').replace('¹', '').replace('³', '').replace('âµ', '').replace('â', '').replace('µ', '')
        
        # 2. Eliminar caracteres no deseados pero mantener puntos y decimales
        # Esto limpia cosas como 'RoundÂ Â·' -> 'Round ·'
        text = re.sub(r'[^\w\s\.\·\(\)\-]', '', text)
        
        # 3. Normalizar espacios múltiples
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()

    def to_snake_case(self, text):
        """Strictly follows Object snake_case convention."""
        if not text: return "Unnamed"
        # Remove parentheses and non-alphanumeric, then underscore
        text = re.sub(r'\(.*?\)', '', str(text)) 
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text.lower().strip().replace(" ", "_")

    def clean_data(self, value, col_name):
        if pd.isna(value): return None
        val_str = str(value).strip()

        if val_str.lower() in ['n/a', 'none', 'null', 'nan', 'unknown', 'varies', '?']:
            return None
        
        # Lista de columnas que DEBEN ser números
        numeric_cols = ['damage', 'weight', 'range', 'accuracy', 'value', 'ap_cost', 'fire_rate', 'magazine_capacity']
        
        if col_name in numeric_cols:
            # Extraer solo el número (ej: "10 lbs" -> 10)
            match = re.search(r'[-+]?\d*\.?\d+', val_str)
            return float(match.group()) if match else None
        
        # Para nombres, mantenemos el texto pero escapamos comillas para SQL
        return val_str.replace("'", "''")