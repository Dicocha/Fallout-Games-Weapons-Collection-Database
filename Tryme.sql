-- 1. El "Top 10" de Daño (Uniendo Armas y Juegos)

-- Esta consulta te dirá cuáles son las armas más letales de toda la franquicia y en qué juego aparecen.

SELECT 
    g.title AS juego, 
    w.name AS arma, 
    s.damage AS daño, 
    wt.type_name AS categoria
FROM game_weapon_stats s
JOIN games g ON s.game_id = g.game_id
JOIN weapons w ON s.weapon_id = w.weapon_id
JOIN weapon_types wt ON w.base_type_id = wt.type_id
WHERE s.damage IS NOT NULL
ORDER BY s.damage DESC
LIMIT 10;

-- 2. Comparativa de un Arma a través de los Años

-- ¿Quieres ver cómo ha cambiado la mítica 10mm Pistol (o cualquier otra) en cada entrega de la saga?

SELECT 
    g.title AS juego, 
    g.release_year AS año,
    s.damage AS daño, 
    s.weight AS peso,
    s.magazine_capacity AS cargador
FROM game_weapon_stats s
JOIN games g ON s.game_id = g.game_id
JOIN weapons w ON s.weapon_id = w.weapon_id
WHERE w.name ILIKE '%10mm Pistol%'
ORDER BY g.release_year;

-- 3. Conteo de Armas por Tipo

-- Para verificar si el mapa de weapon_types funcionó y cuántas armas logramos categorizar en cada grupo.

SELECT 
    wt.type_name, 
    COUNT(w.weapon_id) AS total_armas
FROM weapon_types wt
LEFT JOIN weapons w ON wt.type_id = w.base_type_id
GROUP BY wt.type_name
ORDER BY total_armas DESC;

-- 4. Análisis de Munición (Eficacia del mapa de Ammo)

-- Esta query te permite ver qué municiones son las más comunes y cuál es el daño promedio de las armas que las usan. Aquí verás si tu unificación de "Microfusion Cell (MFC)" funcionó bien.

SELECT 
    a.ammo_name, 
    COUNT(s.stat_id) AS cantidad_armas,
    ROUND(AVG(s.damage), 2) AS daño_promedio
FROM ammo_types a
JOIN game_weapon_stats s ON a.ammo_id = s.ammo_id
GROUP BY a.ammo_name
HAVING COUNT(s.stat_id) > 5
ORDER BY daño_promedio DESC;

-- 5. Armas "Peso Pluma" pero Letales

-- Ideal para encontrar armas eficientes (daño > 50 y peso < 5).

SELECT 
    w.name, 
    s.damage, 
    s.weight, 
    g.title
FROM game_weapon_stats s
JOIN weapons w ON s.weapon_id = w.weapon_id
JOIN games g ON s.game_id = g.game_id
WHERE s.damage > 50 AND s.weight < 5
ORDER BY s.damage DESC;

-- 6. ¿Cómo verificar si hay errores de datos?

-- Si quieres ver si alguna limpieza falló, ejecuta esta query para encontrar estadísticas que quedaron "huérfanas" de munición o nombre:

-- Buscar estadísticas que no tienen munición asignada (posible error en el mapa)
SELECT 
    g.title, 
    w.name, 
    ats.stat_id,
    ats.damage, 
    ats.weight, 
    ats.weapon_value, 
    ats.ap_cost, 
    ats.fire_rate, 
    ats.weapon_range, 
    ats.accuracy, 
    ats.magazine_capacity, 
    ats.strength_required
FROM 
    game_weapon_stats ats
JOIN 
    games g ON ats.game_id = g.game_id
JOIN 
    weapons w ON ats.weapon_id = w.weapon_id
WHERE 
    ats.damage IS NULL 
    OR ats.weight IS NULL 
    OR ats.weapon_value IS NULL 
    OR ats.ap_cost IS NULL 
    OR ats.fire_rate IS NULL 
    OR ats.weapon_range IS NULL 
    OR ats.accuracy IS NULL 
    OR ats.magazine_capacity IS NULL 
    OR ats.strength_required IS NULL;
