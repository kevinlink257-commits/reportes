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
- `GET/PATCH /api/v1/profile`
- `POST /api/v1/profile/password`
- `GET /api/v1/telemetry/ping`

El modo `DEV_AUTH=true` únicamente sirve para desarrollo local y usa `X-Dev-User`, `X-Dev-Role` y `X-Dev-Org`. Antes de publicar se debe activar la validación OIDC/JWKS y desactivar `DEV_AUTH`.

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
