import pandas as pd

class Maps:
    def __init__(self):

        self.game_map = [{
            "title": "Fallout 1",
            "release_year": 1997,
            "studio": "Interplay"
        },
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
            'Pistols': 'Pistols',
            'Energy Pistols': 'Pistols',
            'Laser Pistols': 'Pistols',
            'Plasma Pistols': 'Pistols',
            
            'Rifles': 'Rifles',
            'Energy Rifles': 'Rifles',
            'Laser Rifles': 'Rifles',
            'Plasma Rifles': 'Rifles',
            'Pipe Weapons': 'Rifles', # Generalmente se clasifican aquí
            
            'Sub Machine Guns': 'Submachine Guns',
            'Submachine Guns': 'Submachine Guns',
            
            'Shotguns': 'Shotguns',
            
            'Big Guns': 'Heavy Weapons',
            'Heavy Weapons': 'Heavy Weapons',
            'Heavy Guns': 'Heavy Weapons',
            'Large Weapons': 'Heavy Weapons',
            
            'Melee Weapons': 'Melee Weapons',
            'One Handed Melee': 'Melee Weapons',
            'Two Handed Melee': 'Melee Weapons',
            'Bladed Melee': 'Melee Weapons',
            'Blunt Melee': 'Melee Weapons',
            
            'Unarmed': 'Unarmed',
            'Unarmed Weapons': 'Unarmed',
            
            'Explosives': 'Explosives',
            'Thrown Explosives': 'Explosives',
            'Placed Explosives': 'Explosives',
            'Projectile Explosives': 'Explosives',
            
            'Cut Content': 'Non-Playable / Cut Content',
            'Unused Weapons': 'Non-Playable / Cut Content',
            'Npc Weapons': 'Non-Playable / Cut Content'
        }

        self.ammo_type_map = {
            # --- MICROFUSION / ENERGY CELLS ---
            "Microfusion Cell": "Microfusion Cell (MFC)",
            "Micro Fusion Cell": "Microfusion Cell (MFC)",
            "MFC": "Microfusion Cell (MFC)",
            "Small Energy Cell": "Small Energy Cell (SEC)",
            "SEC": "Small Energy Cell (SEC)",
            "Energy cell": "Small Energy Cell (SEC)",
            "Fusion cell": "Fusion Cell (FC)",
            "Worn fusion cell": "Fusion Cell (FC)",
            "Plasma cartridge": "Plasma Cartridge (PC)",
            "Plasma Core": "Plasma Core",
            "Fusion Core": "Fusion Core",
            "Electron Charge Pack": "Electron Charge Pack (ECP)",
            "ECP": "Electron Charge Pack (ECP)",
            "MF breeder": "Microfusion Breeder (MFB)",
            "Microfusion breeder": "Microfusion Breeder (MFB)",
            "Alien Power Cell": "Alien Power Cell (APC)",
            "Alien PC": "Alien Power Cell (APC)",
            "Alien power module": "Alien Power Cell (APC)",

            # --- BALÍSTICA (CON UNIFICACIÓN DE CALIBRES) ---
            "10mm": "10mm Round",
            "9mm": "9mm Round",
            "5.56": "5.56mm Round",
            "5mm": "5mm Round",
            "7.62": "7.62mm Round",
            ".308": "0.308 Round",
            "0.308": "0.308 Round",
            ".38": "0.38 Round",
            "0.38": "0.38 Round",
            ".44": "0.44 Magnum Round",
            "0.44": "0.44 Magnum Round",
            ".45": "0.45 Auto Round",
            "0.45": "0.45 Auto Round",
            ".357": "0.357 Magnum Round",
            ".50 caliber": "0.50 Caliber Round",
            ".50 MG": "0.50 Machine Gun Round (.50 MG)",
            "12.7mm": "12.7mm Round",
            ".22LR": "0.22 Long Rifle Round (.22LR)",
            ".223": "0.223 Round",
            "14mm": "14mm Round",
            "2mm EC": "2mm Electromagnetic Cartridge (2mm EC)",
            "2mm electromagnetic": "2mm Electromagnetic Cartridge (2mm EC)",

            # --- ESCOPETAS Y PESADAS ---
            "12 gauge": "12 Gauge Shell",
            "12 ga": "12 Gauge Shell",
            "20 gauge": "20 Gauge Shell",
            "20 ga": "20 Gauge Shell",
            "Flamethrower fuel": "Flamethrower Fuel",
            "Flamer fuel": "Flamethrower Fuel",
            "Fuel": "Flamethrower Fuel",
            "Missile": "Missile",
            "Mini nuke": "Mini Nuke",
            "Rocket": "Rocket",
            "40mm grenade": "40mm Grenade Round",
            "25mm grenade": "25mm Grenade Round",

            # --- ESPECIALES / ARCHIVO ---
            "Railway spike": "Railway Spike",
            "Harpoon": "Harpoon",
            "Gamma round": "Gamma Round",
            "Alien blaster round": "Alien Blaster Round",
            "Syringer ammo": "Syringer Ammo",
            "Dart": "Dart",
            "BB": "BB Pellet",
            "Nail": "Nails",
            "Flare": "Flare",
            "Cannonball": "Cannonball",
            "Cryo cell": "Cryo Cell",
            
            # --- FILTROS DE BASURA (Retornan None para ser ignorados) ---
            "None": None,
            "nan": None,
            "-": None,
            "?": None,
            "Junk": "Junk / Scrap",
            "Most junk": "Junk / Scrap",
            "Squirt of water": "Water / Liquid"
        }

        self.stats_map = {
            # NOMBRES DE ARMA (Todas estas variaciones -> weapon_name)
            'weapon_name': 'weapon_name',
            'pistol_name': 'weapon_name',
            'rifle_name': 'weapon_name',
            'shotgun_name': 'weapon_name',
            'submachine_gun_name': 'weapon_name',
            'heavy_weapon_name': 'weapon_name',
            'energy_pistol_name': 'weapon_name',
            'energy_rifle_name': 'weapon_name',
            'laser_weapon_name': 'weapon_name',
            'plasma_weapon_name': 'weapon_name',
            'big_gun_name': 'weapon_name', # Detectará 'area_of_effect_big_gun_name' por substring
            'melee_weapon_name': 'weapon_name', # Detectará bladed, blunt, etc.
            'unarmed_weapon_name': 'weapon_name',
            'thrown_explosive': 'weapon_name',
            'placed_explosive': 'weapon_name',
            'placed_trap_name': 'weapon_name',
            'weapon': 'weapon_name',
            'name': 'weapon_name',

            # ESTADÍSTICAS BÁSICAS
            'damage': 'damage',
            'weight': 'weight',
            'caps': 'value',
            'selling_caps': 'value',
            'value': 'value',
            'ap_cost': 'ap_cost',
            'action_point': 'ap_cost',
            'ammo_type': 'ammo_type',
            'ammunition': 'ammo_type',
            'ammo': 'ammo_type',
            
            # MÁQUINAS Y ESTADO
            'fire_rate': 'fire_rate',
            'attacks_per_second': 'fire_rate',
            'magazine_capacity': 'magazine_capacity',
            'capacity': 'magazine_capacity',
            'accuracy': 'accuracy',
            'weapon_spread': 'accuracy', # El spread es lo opuesto a la precisión, pero se mapea aquí
            'range': 'range',
            'scope': 'range',
            
            # REQUISITOS Y OTROS
            'strength_required': 'strength_required',
            'skill_required': 'skill_required',
            'critical_chance_multiplier': 'critical_chance_multiplier',
            'durability': 'durability', # Capturará 'weapon_durability_in_shots...'
            'components': 'components',
            'upgrades': 'upgrades',
            'special': 'special',
            'attack_modes': 'attack_modes'
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