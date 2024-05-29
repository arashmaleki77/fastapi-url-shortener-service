from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from redis_client import cache
from shortener.crud.shortener import (
    get_long_url_by_shortener_url, create_shortener_url, get_shortener_url_by_id, get_shortener_urls_by_user_id
)
from shortener.schemas.shortener import ShortenerUrlSchema, CreateShortenerUrlSchema
from user.crud.user import get_user_by_sub_directory
from user.dependencies import get_current_user
from user.schemas.user import UserSchema
from fastapi.responses import RedirectResponse
from utils.pagination import PaginatedResponse, PaginationManager


shortener_router = APIRouter(prefix="/shortener", tags=["shortener"])


@shortener_router.get("/", response_model=PaginatedResponse[ShortenerUrlSchema])
async def get_all_shortener_urls(
        request: Request,
        current_user: UserSchema = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, le=25),
):
    urls = await get_shortener_urls_by_user_id(db=db, user_id=current_user.id)
    return PaginationManager(
        query=urls, page=page, page_size=page_size, request=request, schema=ShortenerUrlSchema
    ).paginate()


@shortener_router.get("/{pk}/", response_model=ShortenerUrlSchema)
async def get_one_shortener_urls(
        pk: int,
        current_user: UserSchema = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    url = await get_shortener_url_by_id(db=db, pk=pk, user_id=current_user.id)
    if url is None or url.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
    return url


@shortener_router.post("/", response_model=ShortenerUrlSchema, status_code=status.HTTP_201_CREATED)
async def create_shortener_urls(
        new_url: CreateShortenerUrlSchema,
        current_user: UserSchema = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    new_shortener_url = await create_shortener_url(db=db, user_id=current_user.id, original_url=new_url.original_url)
    return new_shortener_url


@shortener_router.get("/redirect/{sub_directory}/{short_url}/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_into_original_url(
        sub_directory: str,
        short_url: str,
        db: AsyncSession = Depends(get_db)
):
    cache_key = f"{sub_directory}/{short_url}"
    original_url = cache.get(cache_key)
    if original_url:
        return RedirectResponse(url=original_url.decode("utf-8"), status_code=status.HTTP_307_TEMPORARY_REDIRECT)

    db_user = await get_user_by_sub_directory(db=db, sub_directory=sub_directory)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")

    current_shortener_url = await get_long_url_by_shortener_url(db=db, user_id=db_user.id, short_url=short_url)
    if not current_shortener_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")

    cache.set(cache_key, str(current_shortener_url.original_url), ex=10)

    return RedirectResponse(url=current_shortener_url.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
