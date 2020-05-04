from app import create_app
import falcon
from falcon import testing
import pytest
from uuid import uuid4


@pytest.fixture
def client():
    return testing.TestClient(create_app())


def test_create_portainer(client):
    resp = client.simulate_post(
        "/portainer",
        json={
            "name": "test",
            "endpoint": "http://test.com",
            "username": "username",
            "password": "password",
        },
    )
    response_data = resp.json

    assert resp.status == falcon.HTTP_200
    assert "portainer_id" in response_data


def test_create_portainer_duplicate(client):
    resp = client.simulate_post(
        "/portainer",
        json={
            "name": "test",
            "endpoint": "http://test.com",
            "username": "username",
            "password": "password",
        },
    )

    assert resp.status == falcon.HTTP_501


def test_create_stack(client):
    name = str(uuid4())
    resp = client.simulate_post(
        "/portainer",
        json={
            "name": name,
            "endpoint": "http://test.com",
            "username": "username",
            "password": "password",
        },
    )
    response_data = resp.json

    resp = client.simulate_post(
        "/portainer/stack/create",
        json={
            "portainer_id": response_data["portainer_id"],
            "stack_name": "nginx",
        },
    )

    assert resp.status == falcon.HTTP_200


def test_create_stack_duplicate(client):
    name = str(uuid4())
    resp = client.simulate_post(
        "/portainer",
        json={
            "name": name,
            "endpoint": "http://test.com",
            "username": "username",
            "password": "password",
        },
    )
    response_data = resp.json

    resp = client.simulate_post(
        "/portainer/stack/create",
        json={
            "portainer_id": response_data["portainer_id"],
            "stack_name": "nginx",
        },
    )

    resp = client.simulate_post(
        "/portainer/stack/create",
        json={
            "portainer_id": response_data["portainer_id"],
            "stack_name": "nginx",
        },
    )

    assert resp.status == falcon.HTTP_501


def test_remove_stack(client):
    name = str(uuid4())
    resp = client.simulate_post(
        "/portainer",
        json={
            "name": name,
            "endpoint": "http://test.com",
            "username": "username",
            "password": "password",
        },
    )
    response_data = resp.json

    resp = client.simulate_post(
        "/portainer/stack/create",
        json={
            "portainer_id": response_data["portainer_id"],
            "stack_name": "nginx",
        },
    )

    resp = client.simulate_post(
        "/portainer/stack/remove",
        json={
            "portainer_id": response_data["portainer_id"],
            "stack_name": "nginx",
        },
    )

    assert resp.status == falcon.HTTP_200


def test_remove_stack_inexistent(client):
    name = str(uuid4())
    resp = client.simulate_post(
        "/portainer",
        json={
            "name": name,
            "endpoint": "http://test.com",
            "username": "username",
            "password": "password",
        },
    )
    response_data = resp.json

    resp = client.simulate_post(
        "/portainer/stack/remove",
        json={
            "portainer_id": response_data["portainer_id"],
            "stack_name": "nginx",
        },
    )

    assert resp.status == falcon.HTTP_501
