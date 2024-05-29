from core.settings import settings
from fastapi import status
import pytest
from httpx import AsyncClient
from shortener.models.shortener import ShortenerURL
from shortener.utils import generate_short_url
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_successfully_create_shortener_url(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username11",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki11"
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
    assert new_shortener_response["original_url"], shortener_url_data["original_url"]
    assert "short_url" in new_shortener_response.keys()
    assert len(new_shortener_response["short_url"]) == 5
    assert "full_short_url" in new_shortener_response.keys()
    assert "user" in new_shortener_response.keys()
    assert new_shortener_response["user"]["username"], data["username"]
    assert new_shortener_response["user"]["first_name"], data["first_name"]
    assert new_shortener_response["user"]["last_name"], data["last_name"]
    assert new_shortener_response["user"]["sub_directory"], data["sub_directory"]
    assert "password" not in new_shortener_response["user"]


@pytest.mark.asyncio
async def test_successfully_create_shortener_url_for_each_user_with_the_same_short_url(
        async_client: AsyncClient,
        async_session: AsyncSession
):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username13",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki13"
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    first_user_id: int = response["user"]["id"]

    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username14",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki14"
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    second_user_id: int = response["user"]["id"]

    short_url = generate_short_url()

    first_shortener_url = ShortenerURL(
        short_url=short_url,
        user_id=first_user_id,
        original_url="https://google.com"
    )

    async_session.add(first_shortener_url)
    await async_session.commit()
    await async_session.refresh(first_shortener_url)

    second_shortener_url = ShortenerURL(
        short_url=short_url,
        user_id=second_user_id,
        original_url="https://google.com"
    )
    async_session.add(second_shortener_url)
    await async_session.commit()
    await async_session.refresh(second_shortener_url)

    assert first_shortener_url.id != second_shortener_url.id
    assert first_shortener_url.user_id != second_shortener_url.user_id
    assert first_shortener_url.short_url == second_shortener_url.short_url


@pytest.mark.asyncio
async def test_failed_create_shortener_url_with_invalid_url(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username12",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki12"
    }
    response = await async_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    access_token = response["access_token"]
    header = {"Authorization": access_token}

    shortener_url_data = {
        "original_url": "fake string"
    }
    url = f"{settings.API_V1_STR}/shortener/"
    response = await async_client.post(url, json=shortener_url_data, headers=header)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_access_denied_to_create_shortener_url_without_token(async_client: AsyncClient):
    shortener_url_data = {
        "original_url": "https://google.com"
    }
    url = f"{settings.API_V1_STR}/shortener/"
    response = await async_client.post(url, json=shortener_url_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
