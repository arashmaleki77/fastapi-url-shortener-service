from core.settings import settings
from fastapi import status
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_successfully_redirect_shortener_url(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username31",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki31"
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
    assert new_shortener_response["original_url"] == shortener_url_data["original_url"]
    assert "short_url" in new_shortener_response.keys()
    assert len(new_shortener_response["short_url"]) == 5
    assert "full_short_url" in new_shortener_response.keys()
    assert "user" in new_shortener_response.keys()
    assert new_shortener_response["user"]["username"] == data["username"]
    assert new_shortener_response["user"]["first_name"] == data["first_name"]
    assert new_shortener_response["user"]["last_name"] == data["last_name"]
    assert new_shortener_response["user"]["sub_directory"] == data["sub_directory"]
    assert "password" not in new_shortener_response.keys()

    redirect_shortener_url = f"{settings.API_V1_STR}/shortener/redirect/{data['sub_directory']}/{new_shortener_response['short_url']}/"
    redirect_shortener_response = await async_client.get(redirect_shortener_url, follow_redirects=False)
    assert redirect_shortener_response.status_code == status.HTTP_307_TEMPORARY_REDIRECT


@pytest.mark.asyncio
async def test_failed_redirect_into_wrong_sub_directory_and_short_url(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/shortener/redirect/fake_sub_directory/test1/"
    response = await async_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_failed_redirect_into_wrong_sub_directory(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username32",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki32"
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
    assert new_shortener_response["original_url"] == shortener_url_data["original_url"]
    assert "short_url" in new_shortener_response.keys()
    assert len(new_shortener_response["short_url"]) == 5
    assert "full_short_url" in new_shortener_response.keys()
    assert "user" in new_shortener_response.keys()
    assert new_shortener_response["user"]["username"] == data["username"]
    assert new_shortener_response["user"]["first_name"] == data["first_name"]
    assert new_shortener_response["user"]["last_name"] == data["last_name"]
    assert new_shortener_response["user"]["sub_directory"] == data["sub_directory"]
    assert "password" not in new_shortener_response.keys()

    redirect_shortener_url = f"{settings.API_V1_STR}/shortener/redirect/fake_sub_directory/{new_shortener_response['short_url']}/"
    redirect_shortener_response = await async_client.get(redirect_shortener_url, follow_redirects=False)
    assert redirect_shortener_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_failed_redirect_into_wrong_short_url(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "new_username34",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "maleki34"
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
    assert new_shortener_response["original_url"] == shortener_url_data["original_url"]
    assert "short_url" in new_shortener_response.keys()
    assert len(new_shortener_response["short_url"]) == 5
    assert "full_short_url" in new_shortener_response.keys()
    assert "user" in new_shortener_response.keys()
    assert new_shortener_response["user"]["username"] == data["username"]
    assert new_shortener_response["user"]["first_name"] == data["first_name"]
    assert new_shortener_response["user"]["last_name"] == data["last_name"]
    assert new_shortener_response["user"]["sub_directory"] == data["sub_directory"]
    assert "password" not in new_shortener_response.keys()

    redirect_shortener_url = f"{settings.API_V1_STR}/shortener/redirect/{data['sub_directory']}/test5/"
    redirect_shortener_response = await async_client.get(redirect_shortener_url, follow_redirects=False)
    assert redirect_shortener_response.status_code == status.HTTP_404_NOT_FOUND
