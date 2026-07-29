import pandas as pd
import re

class Format:
    def __init__(self):
        # Patrón RegEx que detecta la "basura" de encoding típica (Ã, Â, â, €, ¦, etc.)
        # Preserva letras, números, espacios, guiones, puntos, comillas simples y paréntesis normales.
        self.encoding_trash_pattern = re.compile(r'[ÃÂâ€¢¹²³µµ½¼¾æøåêíóúáéíóúñÑçÇ]|âµ|Â·|â\x80¢', re.IGNORECASE)

    def format_file_name(self, name):
        game_title = name.replace("_dataset", "").replace("_", " ").title()
        game_title = "Fallout New Vegas" if game_title == "Fallout Newvegas" else game_title
        return game_title

    def deep_clean_text(self, text):
            """Aplica una lista blanca estricta para eliminar Mojibake y basura de encoding."""
            if not text or pd.isna(text): 
                return None
            
            text_str = str(text)

            # 1. Filtro de Lista Blanca (Whitelist):
            # Mantiene letras a-z, A-Z, números 0-9, caracteres latinos (á, é, í, ó, ú, ñ, etc.),
            # espacios y puntuación básica: . , - _ ( ) / + % ' "
            cleaned_text = re.sub(r'[^a-zA-Z0-9ñÑüÜ\s\.\,\-\_\(\)\/\+\%\'\"]', '', text_str)

            # 2. Si el resultado solo contiene símbolos sueltos o quedó en blanco, retornamos None
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
            
            return cleaned_text if cleaned_text else None

    def to_snake_case(self, text):
        if not text: return "Unnamed"
        text = re.sub(r'\(.*?\)', '', str(text)) 
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text.lower().strip().replace(" ", "_")
    
    def clean_ammo_string(self, ammo_str):
        if not ammo_str or pd.isna(ammo_str): 
            return None
            
        # 1. PASO CLAVE: Primero limpiamos el Mojibake con la Whitelist
        cleaned = self.deep_clean_text(ammo_str)
        if not cleaned: 
            return None

        # 2. Reemplazamos separadores raros que hayan sobrevivido o espacios múltiples
        # Si la munición era "2mm ... Ultracite", ahora será "2mm Ultracite" o "2mm / Ultracite"
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()

        # 3. Hacemos el corte seguro si tiene separadores explícitos (como / o ,)
        cleaned = cleaned.split('/')[0].split(',')[0]

        return cleaned.strip()

    def clean_data(self, value, col_name):
        if pd.isna(value): 
            return None
        
        #Tratamiento especial para munición
        if col_name == 'ammo_name':
            return self.clean_ammo_string(value)

        # Tratar el resto de columnas de texto
        if col_name in ['weapon_name', 'notes', 'special', 'special_effect']:
            return self.deep_clean_text(value)

        val_str = str(value).strip().replace('$', '')
        
        # Limpiamos basura de números antes de castear
        val_str = re.sub(r'[^a-zA-Z0-9\.\,\-\/\+]', '', val_str)

        if val_str.lower() in ['n/a', 'none', 'null', 'nan', 'unknown', 'varies', '?', '']:
            return None
        
        numeric_cols = ['damage', 'weight', 'weapon_range', 'accuracy', 'caps_value', 'ap_cost', 'fire_rate', 'magazine_capacity']
        
        if col_name in numeric_cols:
            if '/' in val_str:
                parts = [float(x) for x in re.findall(r'[-+]?\d*\.?\d+', val_str)]
                return max(parts) if parts else None

            match = re.search(r'[-+]?\d*\.?\d+', val_str)
            return float(match.group()) if match else None
        
        return val_str.strip()