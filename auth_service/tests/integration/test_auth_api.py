import pytest

pytestmark = pytest.mark.anyio

async def register_user(client, email: str, password: str):
    return await client.post(
        "/auth/register",
        json={"email": email, "password": password},
    )

async def login_user(client, email: str, password: str):
    return await client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

async def get_me(client, token: str | None = None):
    headers = {}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"

    return await client.get("/auth/me", headers=headers)

@pytest.mark.integration
async def test_full_auth_flow_register_login_me(client):
    email = "user@example.com"
    password = "secret123"

    register_response = await register_user(client, email, password)
    assert register_response.status_code == 201

    register_data = register_response.json()
    assert register_data["email"] == email
    assert "id" in register_data
    assert "created_at" in register_data

    login_response = await login_user(client, email, password)
    assert login_response.status_code == 200

    login_data = login_response.json()
    assert login_data["token_type"] == "bearer"
    assert login_data["access_token"]

    me_response = await get_me(client, login_data["access_token"])
    assert me_response.status_code == 200

    me_data = me_response.json()
    assert me_data["email"] == email
    assert me_data["id"] == register_data["id"]
    assert "created_at" in me_data

@pytest.mark.integration
async def test_duplicate_registration_returns_409(client):
    email = "user@example.com"
    password = "secret123"

    first_response = await register_user(client, email, password)
    assert first_response.status_code == 201

    second_response = await register_user(client, email, password)
    assert second_response.status_code == 409
    assert "detail" in second_response.json()

@pytest.mark.integration
async def test_login_with_wrong_password_returns_401(client):
    email = "user@example.com"
    password = "secret123"

    register_response = await register_user(client, email, password)
    assert register_response.status_code == 201

    login_response = await login_user(client, email, "wrong-password")
    assert login_response.status_code == 401
    assert "detail" in login_response.json()

@pytest.mark.integration
async def test_me_without_token_returns_401(client):
    response = await get_me(client)
    assert response.status_code == 401
    assert "detail" in response.json()

@pytest.mark.integration
async def test_me_with_invalid_token_returns_401(client):
    response = await get_me(client, "invalid-token")
    assert response.status_code == 401
    assert "detail" in response.json()