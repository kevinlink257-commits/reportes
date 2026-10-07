from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app import main


ORG_ID = str(uuid4())
USER = {"sub": "integration-user", "role": "analyst", "organization_id": ORG_ID}
GUIDE_ID = str(uuid4())


@pytest.fixture(scope="session", autouse=True)
def seed_database():
    """Inserta datos aislados; el workflow usa una base PostGIS efímera."""
    with main.db() as conn:
        conn.execute(
            """INSERT INTO guides (id, organization_id, code, zone, price, status)
               VALUES (%s, %s, %s, %s, %s, 'available')""",
            (GUIDE_ID, ORG_ID, "482100000001", "Chapinero", 50000),
        )
        conn.execute(
            """INSERT INTO visits
               (organization_id, guide_id, status, zone, visited_at, location, gps_accuracy_m)
               VALUES (%s, %s, 'Entregado', 'Chapinero', %s,
                       ST_SetSRID(ST_MakePoint(-74.0721, 4.7110), 4326)::geography, 7)""",
            (ORG_ID, GUIDE_ID, datetime.now(timezone.utc)),
        )
    yield
    with main.db() as conn:
        conn.execute("DELETE FROM visits WHERE organization_id=%s", (ORG_ID,))
        conn.execute("DELETE FROM guides WHERE organization_id=%s", (ORG_ID,))


@pytest.mark.integration
def test_radius_query_uses_real_postgis():
    result = main.visits_within_radius(
        lat=4.7110,
        lng=-74.0721,
        radius_m=100,
        from_date=None,
        to_date=None,
        limit=10,
        user=USER,
    )

    assert len(result) == 1
    assert result[0].code == "482100000001"
    assert result[0].distance_m is not None
    assert result[0].distance_m < 1


@pytest.mark.integration
def test_polygon_query_uses_real_postgis():
    body = main.PolygonVisitQuery(
        polygon={
            "type": "Polygon",
            "coordinates": [[
                [-74.0800, 4.7050],
                [-74.0650, 4.7050],
                [-74.0650, 4.7200],
                [-74.0800, 4.7200],
                [-74.0800, 4.7050],
            ]],
        },
        limit=10,
    )

    result = main.visits_within_polygon(body, USER)

    assert len(result) == 1
    assert result[0].code == "482100000001"
    assert result[0].lat == pytest.approx(4.7110, abs=0.0001)
    assert result[0].lng == pytest.approx(-74.0721, abs=0.0001)
