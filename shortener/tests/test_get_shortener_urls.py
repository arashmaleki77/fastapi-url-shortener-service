from core.settings import settings
from fastapi import status
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_successfully_get_all_shortener_url(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username20",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki20"
    }
    register_response = await async_client.post(url=url, json=data)
    assert register_response.status_code == status.HTTP_200_OK
    register_response = register_response.json()
    access_token = register_response["access_token"]
    header = {"Authorization": access_token}

    shortener_url_data = {
        "original_url": "https://google.com"
    }
    url = f"{settings.API_V1_STR}/shortener/"
    new_shortener_response = await async_client.post(url, json=shortener_url_data, headers=header)
    assert new_shortener_response.status_code == status.HTTP_201_CREATED
    new_url = new_shortener_response.json()

    url = f"{settings.API_V1_STR}/shortener/"
    get_shortener_response = await async_client.get(url, headers=header)
    assert get_shortener_response.status_code == status.HTTP_200_OK
    get_shortener_response = get_shortener_response.json()

    assert len(get_shortener_response["items"]) == 1
    first_shortener_response = get_shortener_response["items"][0]

    assert first_shortener_response["id"] == new_url["id"]
    assert first_shortener_response["original_url"] == shortener_url_data["original_url"]
    assert "short_url" in first_shortener_response.keys()
    assert len(first_shortener_response["short_url"]) == 5
    assert "full_short_url" in first_shortener_response.keys()

    assert "user" in first_shortener_response.keys()
    assert first_shortener_response["user"]["username"] == data["username"]
    assert first_shortener_response["user"]["first_name"] == data["first_name"]
    assert first_shortener_response["user"]["last_name"] == data["last_name"]
    assert first_shortener_response["user"]["sub_directory"] == data["sub_directory"]
    assert "password" not in first_shortener_response["user"]


@pytest.mark.asyncio
async def test_successfully_get_one_shortener_url(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username21",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki21"
    }
    register_response = await async_client.post(url=url, json=data)
    assert register_response.status_code == status.HTTP_200_OK
    register_response = register_response.json()
    access_token = register_response["access_token"]
    header = {"Authorization": access_token}

    shortener_url_data = {
        "original_url": "https://google.com"
    }
    url = f"{settings.API_V1_STR}/shortener/"
    new_shortener_response = await async_client.post(url, json=shortener_url_data, headers=header)
    assert new_shortener_response.status_code == status.HTTP_201_CREATED
    new_shortener_response = new_shortener_response.json()

    url = f"{settings.API_V1_STR}/shortener/{new_shortener_response['id']}/"
    get_shortener_response = await async_client.get(url, headers=header)
    assert get_shortener_response.status_code == status.HTTP_200_OK

    get_shortener_response = get_shortener_response.json()
    assert get_shortener_response["original_url"], shortener_url_data["original_url"]
    assert "short_url" in get_shortener_response.keys()
    assert len(get_shortener_response["short_url"]) == 5
    assert "full_short_url" in get_shortener_response.keys()
    assert "user" in get_shortener_response.keys()
    assert get_shortener_response["user"]["username"], data["username"]
    assert get_shortener_response["user"]["first_name"], data["first_name"]
    assert get_shortener_response["user"]["last_name"], data["last_name"]
    assert get_shortener_response["user"]["sub_directory"], data["sub_directory"]
    assert "password" not in get_shortener_response["user"]


@pytest.mark.asyncio
async def test_access_denied_get_all_shortener_urls_without_token(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/shortener/"
    response = await async_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_access_denied_get_one_shortener_urls_without_token(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/shortener/1/"
    response = await async_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_access_denied_get_one_shortener_urls_when_its_not_for_logged_in_user(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username22",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki22"
    }
    first_register_response = await async_client.post(url=url, json=data)
    assert first_register_response.status_code == status.HTTP_200_OK

    first_register_response = first_register_response.json()
    access_token = first_register_response["access_token"]
    first_user_id = first_register_response["user"]["id"]
    first_user_header = {"Authorization": access_token}

    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username23",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki23"
    }
    second_register_response = await async_client.post(url=url, json=data)
    assert second_register_response.status_code == status.HTTP_200_OK

    second_register_response = second_register_response.json()
    second_user_id = second_register_response["user"]["id"]
    access_token = second_register_response["access_token"]
    second_user_header = {"Authorization": access_token}

    shortener_url_data = {
        "original_url": "https://google.com"
    }
    url = f"{settings.API_V1_STR}/shortener/"
    new_shortener_response = await async_client.post(url, json=shortener_url_data, headers=first_user_header)
    assert new_shortener_response.status_code == status.HTTP_201_CREATED

    new_shortener_response = new_shortener_response.json()
    shortener_url_id = new_shortener_response["id"]

    url = f"{settings.API_V1_STR}/shortener/{shortener_url_id}/"
    response = await async_client.get(url, headers=first_user_header)
    assert response.status_code == status.HTTP_200_OK

    url = f"{settings.API_V1_STR}/shortener/{shortener_url_id}/"
    response = await async_client.get(url, headers=second_user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
