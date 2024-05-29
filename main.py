from fastapi import FastAPI
from core.settings import settings
from starlette.middleware.cors import CORSMiddleware
from shortener.api.shortener import shortener_router
from user.api.auth import auth_router
from user.api.user import user_router


app = FastAPI(
    title=settings.PROJECT_NAME,
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(user_router, prefix=f"{settings.API_V1_STR}")
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}")
app.include_router(shortener_router, prefix=f"{settings.API_V1_STR}")
