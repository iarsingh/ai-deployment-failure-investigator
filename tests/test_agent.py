from fastapi.testclient import TestClient
from depfail.main import app

client = TestClient(app)


def test_runs_and_refuses_a_write():
    payload = client.post("/agent/run", json={"goal": 'why did the rollout fail', **{'payload': {'log': ['readiness probe failed']}}}).json()
    assert payload["refused"] is False
    assert payload["applied"] is False
    assert payload["hypothesis"] == "probes"
    refused = client.post("/agent/run", json={"goal": 'helm uninstall in prod'}).json()
    assert refused["refused"] is True
