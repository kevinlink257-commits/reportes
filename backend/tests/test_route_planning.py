from contextlib import contextmanager

from app import main


USER = {"sub": "driver-01", "role": "repartidor", "organization_id": "org-1"}


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeClient:
    response_payload = []
    requests = []

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def get(self, url, params=None):
        self.requests.append((url, params))
        return FakeResponse(self.response_payload)


def test_geocode_uses_complete_query_and_returns_coordinates(monkeypatch):
    FakeClient.response_payload = [{
        "lat": "4.7110",
        "lon": "-74.0721",
        "display_name": "Calle 93B, Bogotá",
        "address": {"city": "Bogotá"},
    }]
    FakeClient.requests = []
    monkeypatch.setattr(main.httpx, "Client", FakeClient)

    result = main._geocode_address("Calle 93B # 13-45, Bogotá, Colombia")

    assert result["lat"] == 4.711
    assert result["lng"] == -74.0721
    assert FakeClient.requests[0][1]["format"] == "jsonv2"
    assert FakeClient.requests[0][1]["countrycodes"] == "co"


def test_daily_route_returns_osrm_optimized_order(monkeypatch):
    FakeClient.response_payload = {
        "code": "Ok",
        "waypoints": [
            {"waypoint_index": 0},
            {"waypoint_index": 2},
            {"waypoint_index": 1},
        ],
        "trips": [{
            "distance": 4200,
            "duration": 900,
            "geometry": {"type": "LineString", "coordinates": []},
            "legs": [],
        }],
    }
    FakeClient.requests = []
    monkeypatch.setattr(main.httpx, "Client", FakeClient)
    monkeypatch.setattr(main, "_resolve_point", lambda point: {"lat": 4.70, "lng": -74.07, "source": "gps"})
    monkeypatch.setattr(
        main,
        "_resolve_visit_stop",
        lambda stop, user: {"visit_id": str(stop.visit_id), "lat": 4.71, "lng": -74.07, "label": stop.label},
    )

    body = main.DailyRouteRequest.model_validate({
        "start": {"gps": {"lat": 4.70, "lng": -74.07}},
        "stops": [
            {"visit_id": "11111111-1111-1111-1111-111111111111", "label": "A"},
            {"visit_id": "22222222-2222-2222-2222-222222222222", "label": "B"},
        ],
        "return_to_start": True,
    })
    result = main.plan_daily_route(body, USER)

    assert result["distance_m"] == 4200
    assert [stop["label"] for stop in result["stops"]] == ["B", "A"]
    route_url, params = FakeClient.requests[0]
    assert "/trip/v1/driving/" in route_url
    assert params["roundtrip"] == "true"
