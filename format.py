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
    
    def clean_ammo_string(self, ammo_str):
        if not ammo_str or pd.isna(ammo_str):
            return None
        
        # 1. Eliminar ruido de codificación (â€¢, Â·, etc)
        # Reemplazamos cualquier cosa que no sea alfanumérica, espacios, puntos o guiones
        s = str(ammo_str).encode('ascii', 'ignore').decode('ascii')
        
        # 2. Si hay múltiples (separadas por puntos, comas o barras), tomar la primera
        # Esto soluciona casos como ".45 Round · .38 round"
        s = s.split('·')[0].split('•')[0].split('/')[0].split(',')[0]
        
        # 3. Limpiar términos molestos para el matcheo
        s = s.replace('(Ultracite)', '').replace('Ultracite', '').strip()
        
        return s

    def clean_data(self, value, col_name):
        if pd.isna(value): return None
        val_str = str(value).strip().replace('$', '').replace(' hexes', '')

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