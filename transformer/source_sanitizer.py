import re
from pathlib import Path

class SourceSanitizer:
    def __init__(self):
        self.root_folder = Path("./archive/")

    def _is_line_empty(self, line: str) -> bool:
        line_clean = line.strip()
        return not line_clean or bool(re.match(r'^[,\s]*$', line_clean))

    def sanitize_all_sources(self):
        print("🚀 Iniciando fase Pre-Extract: Remoción de registros vacíos y fix de Encoding...")
        
        csv_files = list(self.root_folder.glob("**/*.csv"))
        if not csv_files:
            print("⚠️ No se encontraron archivos CSV en ./archive/")
            return

        for file_path in csv_files:
            lines = []
            # Intentamos leer primero en UTF-8 (con BOM) y si falla, caemos en Latin-1
            try:
                with open(file_path, "r", encoding="utf-8-sig") as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="iso-8859-1") as f:
                    lines = f.readlines()

            sanitized_lines = []
            for line in lines:
                if not self._is_line_empty(line):
                    sanitized_lines.append(line)

            # Reescribimos SIEMPRE en utf-8 limpio para estandarizar todo el proyecto
            with open(file_path, "w", encoding="utf-8-sig", errors="ignore") as f:
                f.writelines(sanitized_lines)
                
        print(f"✅ Pre-Extract completado con éxito. {len(csv_files)} fuentes normalizadas en UTF-8.")