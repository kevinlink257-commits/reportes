-- Índices para consultas por organización, tiempo, zona y ubicación.
-- Ejecutar en producción durante una ventana controlada; para tablas grandes
-- usar CREATE INDEX CONCURRENTLY fuera de una transacción.
CREATE EXTENSION IF NOT EXISTS btree_gist;

-- Combina el aislamiento por organización con el filtro espacial.
CREATE INDEX IF NOT EXISTS visits_org_location_gix
  ON visits USING GIST (organization_id, location)
  WHERE location IS NOT NULL;

-- Acelera filtros por rango temporal dentro de una organización.
CREATE INDEX IF NOT EXISTS visits_org_visited_at_idx
  ON visits (organization_id, visited_at DESC);

-- Acelera /api/v1/visits/in-zone, que usa LOWER(zone).
CREATE INDEX IF NOT EXISTS visits_org_zone_lower_idx
  ON visits (organization_id, lower(zone));
