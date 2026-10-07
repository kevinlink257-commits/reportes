from __future__ import annotations

import hashlib
import hmac
import os
import secrets
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any

import psycopg
from psycopg.types.json import Jsonb
from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://colserlog:colserlog@localhost:5432/colserlog")
CORS_ORIGINS = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:8080,https://kevinlink257-commits.github.io").split(",") if x.strip()]
DEV_AUTH = os.getenv("DEV_AUTH", "false").lower() == "true"
PBKDF2_ITERATIONS = 310_000

app = FastAPI(title="Colserlog API", version="1.0.0", docs_url="/docs")
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@contextmanager
def db():
    with psycopg.connect(DATABASE_URL) as conn:
        yield conn


def current_user(request: Request) -> dict[str, Any]:
    """Temporary development identity; production must use OIDC/SSO middleware."""
    if DEV_AUTH:
        return {"sub": request.headers.get("x-dev-user", "local-dev"), "role": request.headers.get("x-dev-role", "admin"), "organization_id": request.headers.get("x-dev-org", "00000000-0000-0000-0000-000000000001")}
    # The production deployment should validate the Bearer token with the configured OIDC JWKS.
    # Failing closed prevents accidental exposure of the API.
    auth = request.headers.get("authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token OIDC requerido")
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Configura OIDC_JWKS_URL antes de usar autenticación productiva")


def require_roles(*roles: str):
    def dependency(user=Depends(current_user)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Permiso insuficiente")
        return user
    return dependency


def hash_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, PBKDF2_ITERATIONS)
    return digest.hex(), salt.hex()


def verify_password(password: str, expected_hash: str, salt_hex: str) -> bool:
    calculated, _ = hash_password(password, bytes.fromhex(salt_hex))
    return hmac.compare_digest(calculated, expected_hash)


class ProfilePatch(BaseModel):
    display_name: str = Field(min_length=3, max_length=80)


class PasswordChange(BaseModel):
    current_password: str = Field(min_length=1)
    new_password: str = Field(min_length=8, max_length=128)


class GuideSearchResult(BaseModel):
    code: str
    address: str | None = None
    zone: str | None = None
    price: float = 0
    score: int


class GPSPoint(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    accuracy_m: float | None = Field(default=None, ge=0, le=100000)


class VisitCreate(BaseModel):
    code: str = Field(min_length=12, max_length=12, pattern=r"^[0-9]{12}$")
    status: str = Field(min_length=1, max_length=80)
    description: str | None = Field(default=None, max_length=2000)
    zone: str | None = Field(default=None, max_length=160)
    price: float = Field(default=0, ge=0)
    visited_at: datetime | None = None
    gps: GPSPoint | None = None


@app.get("/health")
def health():
    with db() as conn:
        conn.execute("SELECT 1")
    return {"status": "ok", "service": "colserlog-api", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/api/v1/guides/search", response_model=list[GuideSearchResult])
def search_guides(digits: str = Query(min_length=2, max_length=12, pattern=r"^[0-9]+$"), user=Depends(current_user)):
    with db() as conn:
        rows = conn.execute("""
            SELECT code, address, zone, price,
              CASE WHEN code=%s THEN 10000 WHEN code LIKE %s THEN 7000+char_length(%s)*100 WHEN position(%s in code)>0 THEN 4000+char_length(%s)*100 ELSE 0 END AS score
            FROM guides
            WHERE organization_id=%s AND status='available' AND (code=%s OR code LIKE %s OR position(%s in code)>0)
            ORDER BY score DESC, code LIMIT 20
        """, (digits, digits+'%', digits, digits, digits, user["organization_id"], digits, digits+'%', digits)).fetchall()
    return [GuideSearchResult(code=r[0], address=r[1], zone=r[2], price=float(r[3] or 0), score=r[4]) for r in rows]


@app.post("/api/v1/visits", status_code=status.HTTP_201_CREATED)
def create_visit(body: VisitCreate, user=Depends(require_roles("admin", "supervisor", "repartidor"))):
    visited_at = body.visited_at or datetime.now(timezone.utc)
    with db() as conn:
        guide = conn.execute(
            "SELECT id, price FROM guides WHERE organization_id=%s AND code=%s",
            (user["organization_id"], body.code),
        ).fetchone()
        if not guide:
            raise HTTPException(404, "Guía no encontrada en la organización")
        account = conn.execute("SELECT id FROM users WHERE sso_subject=%s", (user["sub"],)).fetchone()
        gps = body.gps
        row = conn.execute(
            """INSERT INTO visits
              (organization_id, guide_id, user_id, status, description, zone, price,
               visited_at, location, gps_accuracy_m)
              VALUES (%s,%s,%s,%s,%s,%s,%s,%s,
                CASE WHEN %s IS NULL OR %s IS NULL THEN NULL
                     ELSE ST_SetSRID(ST_MakePoint(%s,%s),4326)::geography END,
                %s)
              RETURNING id, visited_at, ST_Y(location::geometry), ST_X(location::geometry), gps_accuracy_m""",
            (
                user["organization_id"], guide[0], account[0] if account else None,
                body.status, body.description, body.zone,
                body.price or float(guide[1] or 0), visited_at,
                gps.lng if gps else None, gps.lat if gps else None,
                gps.lng if gps else None, gps.lat if gps else None,
                gps.accuracy_m if gps else None,
            ),
        ).fetchone()
    return {
        "id": str(row[0]),
        "code": body.code,
        "visited_at": row[1].isoformat(),
        "gps": {"lat": row[2], "lng": row[3], "accuracy_m": row[4]} if row[2] is not None else None,
    }


@app.get("/api/v1/profile")
def profile(user=Depends(current_user)):
    with db() as conn:
        row = conn.execute("SELECT display_name, email, role FROM users WHERE sso_subject=%s", (user["sub"],)).fetchone()
    if not row:
        raise HTTPException(404, "Perfil no encontrado")
    return {"display_name": row[0], "email": row[1], "role": row[2]}


@app.patch("/api/v1/profile")
def update_profile(body: ProfilePatch, user=Depends(current_user)):
    with db() as conn:
        conn.execute("UPDATE users SET display_name=%s WHERE sso_subject=%s", (body.display_name.strip(), user["sub"]))
    return {"ok": True, "display_name": body.display_name.strip()}


@app.post("/api/v1/profile/password")
def change_password(body: PasswordChange, user=Depends(current_user)):
    if not any(c.isupper() for c in body.new_password) or not any(c.islower() for c in body.new_password) or not any(c.isdigit() for c in body.new_password):
        raise HTTPException(400, "La nueva contraseña debe incluir mayúscula, minúscula y número")
    with db() as conn:
        row = conn.execute("SELECT password_hash, password_salt FROM users WHERE sso_subject=%s", (user["sub"],)).fetchone()
        if not row or not verify_password(body.current_password, row[0], row[1]):
            raise HTTPException(400, "La contraseña actual no coincide")
        digest, salt = hash_password(body.new_password)
        conn.execute("UPDATE users SET password_hash=%s, password_salt=%s WHERE sso_subject=%s", (digest, salt, user["sub"]))
    return {"ok": True}


@app.get("/api/v1/telemetry/ping")
def telemetry_ping(request: Request, user=Depends(current_user)):
    with db() as conn:
        conn.execute("INSERT INTO telemetry_events (organization_id, user_subject, event_name, metadata) VALUES (%s,%s,%s,%s)", (user["organization_id"], user["sub"], "api_ping", Jsonb({"user_agent": request.headers.get("user-agent", "")})))
    return {"ok": True}
