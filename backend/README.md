# Colserlog API

Base ejecutable para la migración de Firebase a **FastAPI + PostgreSQL + PostGIS**.

## Ejecutar localmente

```bash
docker compose up --build
curl http://localhost:8000/health
```

La documentación queda en `http://localhost:8000/docs`.

## Endpoints incluidos

- `GET /health`
- `GET /api/v1/guides/search?digits=4821`
- `POST /api/v1/visits` — guarda una visita y su ubicación GPS en PostGIS.
- `GET /api/v1/visits/within-radius?lat=4.711&lng=-74.0721&radius_m=1000` — visitas dentro de un radio en metros.
- `GET /api/v1/visits/in-zone?zone=Chapinero` — visitas cuyo campo operativo `zone` coincide.
- `GET/PATCH /api/v1/profile`
- `POST /api/v1/profile/password`
- `GET /api/v1/telemetry/ping`

`DEV_AUTH` está desactivado en `docker-compose.yml`. La API ahora exige un Bearer JWT OIDC válido. Configura antes de arrancar:

```bash
export OIDC_JWKS_URL=https://idp.example.com/.well-known/jwks.json
export OIDC_ISSUER=https://idp.example.com/
export OIDC_AUDIENCE=colserlog-api
docker compose up --build
```

El token debe contener `sub`, `organization_id` (o `org_id`) y opcionalmente `role`. Si falta la configuración OIDC, la API responde `503` de forma segura.

La API es el nuevo punto de control para roles, duplicados, búsqueda de guías, visitas, contraseñas y telemetría. El frontend está preparado para continuar operando offline mientras se conecta progresivamente a estos endpoints.

### Ejemplo de registro con GPS

```bash
curl -X POST http://localhost:8000/api/v1/visits \
  -H 'Content-Type: application/json' \
  -H 'X-Dev-User: repartidor-01' \
  -H 'X-Dev-Role: repartidor' \
  -H 'X-Dev-Org: 00000000-0000-0000-0000-000000000001' \
  -d '{
    "code": "482100000001",
    "status": "Entregado",
    "description": "Recibido por el cliente",
    "zone": "Chapinero",
    "price": 50000,
    "gps": {"lat": 4.711, "lng": -74.0721, "accuracy_m": 7}
  }'
```

El endpoint valida los rangos de coordenadas, busca la guía dentro de la organización autenticada y ejecuta `ST_SetSRID(ST_MakePoint(lng, lat),4326)::geography`. En producción se debe desactivar `DEV_AUTH`, configurar OIDC/SSO y usar HTTPS.

### Consultas espaciales

El endpoint de radio usa `ST_DWithin` —que aprovecha el índice GiST de `visits.location`— y devuelve la distancia real en metros con `ST_Distance`:

```bash
curl -G 'https://api.example.com/api/v1/visits/within-radius' \
  -H "Authorization: Bearer $TOKEN" \
  --data-urlencode 'lat=4.711' \
  --data-urlencode 'lng=-74.0721' \
  --data-urlencode 'radius_m=1000' \
  --data-urlencode 'from=2026-10-01T00:00:00Z' \
  --data-urlencode 'limit=100'
```

Para una zona operativa guardada como texto:

```bash
curl -G 'https://api.example.com/api/v1/visits/in-zone' \
  -H "Authorization: Bearer $TOKEN" \
  --data-urlencode 'zone=Chapinero'
```

Si necesitas límites geográficos reales —por ejemplo un polígono de localidad— crea una tabla `zones` con `geometry(MultiPolygon,4326)` y consulta:

```sql
SELECT v.id, g.code, v.status,
       ST_Distance(v.location, z.geom::geography) AS distance_m
FROM visits v
JOIN guides g ON g.id = v.guide_id
JOIN zones z ON z.organization_id = v.organization_id
WHERE z.code = $1
  AND ST_Intersects(v.location::geometry, z.geom);
```
