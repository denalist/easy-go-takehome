from fastapi.testclient import TestClient
from src.inference import app

client = TestClient(app)


def valid_payload():
    return {
        "age": 35,
        "gender_code": 1,
        "location": 123,
        "subscription_type_code": 1,
        "tenure_months": 12,
        "income_bracket_code": 0,
        "event_created_at_ts": 1693478400.0,
        "transaction_value": 150.75,
        "channel_code": 0,
    }


def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_infer_success_returns_probability_and_flag():
    r = client.post("/infer", json=valid_payload())
    assert r.status_code == 200
    data = r.json()
    assert set(data.keys()) == {"fraud_flag", "fraud_probability"}
    assert isinstance(data["fraud_flag"], bool)
    assert 0.0 <= float(data["fraud_probability"]) <= 1.0


def test_infer_422_on_missing_field():
    payload = valid_payload()
    payload.pop("age")
    r = client.post("/infer", json=payload)
    assert r.status_code == 422


def test_infer_422_on_bad_enum():
    payload = valid_payload()
    payload["gender_code"] = 99  # must be 0/1/2
    r = client.post("/infer", json=payload)
    assert r.status_code == 422