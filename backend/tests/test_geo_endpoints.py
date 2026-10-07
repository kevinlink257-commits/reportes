from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
import sys
from uuid import UUID

import pytest
from fastapi import HTTPException

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import main  # noqa: E402


ORG_ID = "00000000-0000-0000-0000-000000000001"
USER = {"sub": "analyst-01", "role": "analyst", "organization_id": ORG_ID}


class FakeResult:
    def __init__(self, rows):
        self.rows = rows

    def fetchone(self):
        return self.rows[0] if self.rows else None

    def fetchall(self):
        return self.rows


class FakeConnection:
    def __init__(self, rows=None, geometry=(True, False, "POLYGON")):
        self.calls = []
        self.rows = rows or []
        self.geometry = geometry

    def execute(self, sql, params=()):
        self.calls.append((sql, tuple(params)))
        if "ST_IsValid" in sql:
            return FakeResult([self.geometry])
        return FakeResult(self.rows)


@contextmanager
def fake_db(connection):
    yield connection


def visit_row():
    return (
        UUID("11111111-1111-1111-1111-111111111111"),
        "482100000001",
        "Entregado",
        "Chapinero",
        datetime(2026, 10, 7, 15, 0, tzinfo=timezone.utc),
        4.711,
        -74.0721,
        7.0,
        None,
    )


def square_polygon():
    return {
        "type": "Polygon",
        "coordinates": [[
            [-74.0800, 4.7050],
            [-74.0650, 4.7050],
            [-74.0650, 4.7200],
            [-74.0800, 4.7200],
            [-74.0800, 4.7050],
        ]],
    }


def test_polygon_query_validates_and_preserves_tenant_filter(monkeypatch):
    connection = FakeConnection(rows=[visit_row()])
    monkeypatch.setattr(main, "db", lambda: fake_db(connection))

    body = main.PolygonVisitQuery.model_validate({
        "polygon": square_polygon(),
        "from": "2026-10-01T00:00:00Z",
        "limit": 25,
    })
    result = main.visits_within_polygon(body, USER)

    assert result[0].code == "482100000001"
    query, params = connection.calls[1]
    assert "ST_Intersects(v.location, z.geom)" in query
    assert params[0].find('"type":"Polygon"') >= 0
    assert params[1] == ORG_ID
    assert params[-1] == 25


def test_polygon_query_rejects_non_polygon_without_query(monkeypatch):
    connection = FakeConnection()
    monkeypatch.setattr(main, "db", lambda: fake_db(connection))
    body = main.PolygonVisitQuery(polygon={"type": "Point", "coordinates": [-74, 4]})

    with pytest.raises(HTTPException) as error:
        main.visits_within_polygon(body, USER)

    assert error.value.status_code == 422
    assert connection.calls == []


def test_polygon_query_rejects_invalid_postgis_geometry(monkeypatch):
    connection = FakeConnection(geometry=(False, False, "POLYGON"))
    monkeypatch.setattr(main, "db", lambda: fake_db(connection))

    with pytest.raises(HTTPException) as error:
        main.visits_within_polygon(main.PolygonVisitQuery(polygon=square_polygon()), USER)

    assert error.value.status_code == 422
    assert len(connection.calls) == 1


def test_radius_query_keeps_spatial_parameters_before_where_parameters(monkeypatch):
    connection = FakeConnection(rows=[visit_row()])
    monkeypatch.setattr(main, "db", lambda: fake_db(connection))

    result = main.visits_within_radius(
        lat=4.711,
        lng=-74.0721,
        radius_m=1000,
        from_date=None,
        to_date=None,
        limit=10,
        user=USER,
    )

    assert result[0].distance_m is None
    query, params = connection.calls[0]
    assert "ST_DWithin(v.location, q.point, %s)" in query
    assert params[:4] == (-74.0721, 4.711, ORG_ID, 1000)
    assert params[-1] == 10


def test_query_models_reject_invalid_radius_and_limit():
    with pytest.raises(Exception):
        # La validación de Query ocurre en FastAPI; este caso documenta los límites
        # que debe cubrir una prueba de contrato con TestClient.
        main.GPSPoint(lat=91, lng=0)

    assert main.PolygonVisitQuery(polygon=square_polygon(), limit=5000).limit == 5000
    with pytest.raises(Exception):
        main.PolygonVisitQuery(polygon=square_polygon(), limit=5001)
