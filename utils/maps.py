import re

import pandas as pd

'''
map = {'first_language_speakers': 'L1', 'additional_language_speakers': 'L2'}
df.rename(columns=map)
'''

class Maps:
    def __init__(self):

        self.game_map = [
        {
            "title": "Fallout 2",
            "release_year": 1998,
            "studio": "Interplay"
        },
        {
            "title": "Fallout 3",
            "release_year": 2008,
            "studio": "Bethesda"
        },
        {
            "title": "Fallout New Vegas",
            "release_year": 2010,
            "studio": "Obsidian"
        },
        {
            "title": "Fallout 4",
            "release_year": 2015,
            "studio": "Bethesda"
        },
        {
            "title": "Fallout 76",
            "release_year": 2018,
            "studio": "Bethesda"
        }]

        self.weapon_type_map = {
            # --- PISTOLS ---
            'Pistols': 'Pistol',
            'Energy pistol name': 'Energy Pistol',
            'Laser Weapons': 'Energy Pistol',
            'Plasma Weapons': 'Energy Pistol',
            'Alien Blaster': 'Energy Pistol',

            # --- RIFLES ---
            'Rifles': 'Rifle',
            'Energy rifle name': 'Energy Rifle',
            'Laser rifle name': 'Energy Rifle',
            'Plasma rifle name': 'Energy Rifle',
            'Bows': 'Bows',

            # --- AUTOMÁTICAS / SMG ---
            'Submachine Guns': 'Submachine gun',
            'Submachine gun name': 'Submachine gun',
            'Smgs': 'Submachine gun',

            # --- ESCOPETAS ---
            'Shotguns': 'Shotgun',
            'Shotgun name': 'Shotgun',

            # --- PESADAS (HEAVY) ---
            'Heavy Weapons': 'Heavy Weapon',
            'Big Guns': 'Heavy Weapon',
            'Energy Heavy Weapons': 'Energy Heavy Weapon',
            'Area Of Effect': 'Explosive Heavy',
            'Direct Fire': 'Heavy Weapon',
            'Explosive Guns': 'Explosive Heavy',

            # --- MELEE / UNARMED ---
            'Bladed melee weapon name': 'Melee (Bladed)',
            'Blunt melee weapon name': 'Melee (Blunt)',
            'Fist melee weapon name': 'Unarmed',
            'Unarmed weapon name': 'Unarmed',
            'Melee Weapons': 'Melee',
            'One Handd Melee': 'Melee (1H)',
            'Two Handd Melee': 'Melee (2H)',

            # --- EXPLOSIVOS Y OTROS ---
            'Thrown Weapons': 'Explosive (Thrown)',
            'Explosives': 'Explosive',
            'Placed Traps': 'Trap',
            'Gamma Weapons': 'Radiation Weapon',
            'Non-Playable / Cut Content': 'Non-Playable / Cut Content',
        }

        self.ammo_type_map = {
            # --- ENERGÍA (MFC, SEC, FUSION) ---
            'Micro Fusion Cell': 'Microfusion Cell (MFC)',
            'Microfusion Cell': 'Microfusion Cell (MFC)',
            'MFC': 'Microfusion Cell (MFC)',
            'Small Energy Cell': 'Small Energy Cell (SEC)',
            'SEC': 'Small Energy Cell (SEC)',
            'Fusion cell': 'Fusion Cell',
            'Fusion core': 'Fusion Core',
            'Plasma cartridge': 'Plasma Cartridge',
            'Plasma Core': 'Plasma Core',
            'Alien blaster round': 'Alien Power Cell',
            'Alien Power Cell': 'Alien Power Cell',
            'Alien PC': 'Alien Power Cell',
            'Gamma round': 'Gamma Round',
            'MF breeder': 'Microfusion Breeder',

            # --- BALÍSTICA (Calibres con limpieza de ruido) ---
            '5.56mm': '5.56mm Round',
            '5.56': '5.56mm Round',
            '5mm': '5mm Round',
            '.308': '.308 Round',
            '0.308': '.308 Round',
            '.38': '.38 Round',
            '0.38': '.38 Round',
            '.44': '.44 Magnum Round',
            '0.44': '.44 Magnum Round',
            '.45': '.45 Round',
            '0.45': '.45 Round',
            '.50': '.50 Caliber Round',
            '10mm': '10mm Round',
            '9mm': '9mm Round',
            '7.62mm': '7.62mm Round',
            '7.62': '7.62mm Round',
            '12.7mm': '12.7mm Round',
            '.357': '.357 Magnum',
            '.223': '.223 Round',
            '.22LR': '.22 LR',
            '4.7mm caseless': '4.7mm Caseless',
            '2mm EC': '2mm Electromagnetic Cartridge',
            '2mm electromagnetic': '2mm Electromagnetic Cartridge',

            # --- ESCOPETAS Y PESADAS ---
            '12 gauge': '12 Gauge Shell',
            '20 gauge': '20 Gauge Shell',
            'Flamer fuel': 'Flamethrower Fuel',
            'Flamethrower fuel': 'Flamethrower Fuel',
            'Fuel': 'Flamethrower Fuel',
            'Mini Nuke': 'Mini Nuke',
            'Missile': 'Missile',
            'Rocket': 'Rocket',
            '40mm grenade': '40mm Grenade',

            # --- ESPECIALES ---
            'Railway spike': 'Railway Spike',
            'Harpoon': 'Harpoon',
            'Crossbow bolt': 'Crossbow Bolt',
            'Arrow': 'Arrow',
            'Syringer ammo': 'Syringer Ammo',
            'Dart': 'Dart',
            'Cannonball': 'Cannonball',
            'BB': 'BB Pellet',
            'Nails': 'Nails',

            # --- BASURA / FILTROS ---
            'Junk': 'Junk',
            'None': None,
            'nan': None,
            '-': None,
            '?': None
        }

        self.regex_stats_map = {
            # IDENTIFICACIÓN DE ARMA
            # Captura cualquier string que termine en 'name', 'weapon', o variantes complejas (ej: 'heavy weapon name')
            'weapon_name': re.compile(r'.*(weapon_name|weapon|name|pistol_name)$', re.IGNORECASE),

            'weapon_type': re.compile(r'.*(weapontype)$', re.IGNORECASE),
            
            # DURABILIDAD
            # Captura 'durability' sin importar si habla de 'shots', 'strikes' o 'attacks'
            'durability': re.compile(r'.*durability.*', re.IGNORECASE),
            
            # MUNICIÓN
            'ammo_name': re.compile(r'^(ammunition(_used)?|ammo)$', re.IGNORECASE),
            
            # DAÑO
            'damage': re.compile(r'.*damage.*', re.IGNORECASE),
            
            # PESO
            'weight': re.compile(r'.*weight.*', re.IGNORECASE),
            
            # ÁREA DE EFECTO
            'area_of_effect': re.compile(r'.*\baoe\b.*|.*area_of_effect.*', re.IGNORECASE),
            
            # VALOR / CHAPAS
            'caps_value': re.compile(r'.*(value|price|caps).*', re.IGNORECASE),
            
            # PUNTOS DE ACCIÓN (AP)
            'ap_cost': re.compile(r'.*(action_point|ap_cost).*', re.IGNORECASE),
            
            # CADENCIA DE FUEGO
            'fire_rate': re.compile(r'.*(speed|rate_of_fire|fire_rate|per_second).*', re.IGNORECASE),
            
            # PRECISIÓN / DISPERSIÓN
            'accuracy': re.compile(r'.*(spread|accuracy).*', re.IGNORECASE),
            
            # ALCANCE
            'weapon_range': re.compile(r'^range$', re.IGNORECASE),
            
            # MODOS DE DISPARO
            'shoot_modes': re.compile(r'.*mode.*', re.IGNORECASE),
            
            # CAPACIDAD DE CARGADOR
            'magazine_capacity': re.compile(r'.*magazine.*', re.IGNORECASE),
            
            # REQUISITOS
            'strength_required': re.compile(r'.*strength.*', re.IGNORECASE),
            'skill_required': re.compile(r'.*skill_required.*', re.IGNORECASE)
        }

    def get_unified_type(self, raw_type):
        """Devuelve el nombre estandarizado del tipo de arma."""
        return self.weapon_type_map.get(raw_type, raw_type)

    def get_unified_ammo(self, raw_ammo):
        if not raw_ammo or pd.isna(raw_ammo):
            return None
        
        # 1. Limpieza de caracteres extraños y normalización
        ammo_clean = str(raw_ammo).encode('ascii', 'ignore').decode('ascii') # Quita Â y â€¢
        ammo_clean = ammo_clean.split(',')[0]   # Quita ", 50 round magazine"
        ammo_clean = ammo_clean.split('(')[0]   # Quita "(Ultracite)"
        ammo_clean = ammo_clean.replace('Round', '').replace('ammo', '').strip()

        # 2. Búsqueda por coincidencia parcial (Substring)
        for key, standard in self.ammo_type_map.items():
            if key.lower() in ammo_clean.lower():
                return standard
                
        return None # Si no lo conocemos o es basura, no lo metemos a la DB
    
    def get_game_map(self):
        """Devuelve un DataFrame con la información de los juegos."""
        return pd.DataFrame(self.game_map)