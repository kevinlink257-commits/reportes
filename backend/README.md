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
- `GET/PATCH /api/v1/profile`
- `POST /api/v1/profile/password`
- `GET /api/v1/telemetry/ping`

El modo `DEV_AUTH=true` únicamente sirve para desarrollo local y usa `X-Dev-User`, `X-Dev-Role` y `X-Dev-Org`. Antes de publicar se debe activar la validación OIDC/JWKS y desactivar `DEV_AUTH`.

La API es el nuevo punto de control para roles, duplicados, búsqueda de guías, contraseñas y telemetría. El frontend está preparado para continuar operando offline mientras se conecta progresivamente a estos endpoints.
