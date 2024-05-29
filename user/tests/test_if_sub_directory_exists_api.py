import pytest
from httpx import AsyncClient
from fastapi import status
from core.settings import settings


@pytest.mark.asyncio
async def test_successfully_check_sub_directory_existence_when_it_exists(async_client: AsyncClient):
    url = f"{settings.API_V1_STR}/auth/register/"
    data = {
        "username": "usernAme80",
        "password": "TestCase1234",
        "first_name": "arash",
        "last_name": "maleki",
        "sub_directory": "usernAme1sub80"
    }
    register_response = await async_client.post(url, json=data)
    assert register_response.status_code == status.HTTP_200_OK

    url = f"{settings.API_V1_STR}/auth/check-if-sub-directory-exists/?sub_directory={data['sub_directory']}"
    response = await async_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json["is_exists"]


@pytest.mark.asyncio
async def test_successfully_check_sub_directory_existence_when_it_does_not_exist(async_client: AsyncClient):
    sub_directory = "testnewsub"
    url = f"{settings.API_V1_STR}/auth/check-if-sub-directory-exists/?sub_directory={sub_directory}"
    response = await async_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert not response_json["is_exists"]
