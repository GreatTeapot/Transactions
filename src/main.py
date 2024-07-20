from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.auth.router import router as auth_router
from src.payment.api.router import all_routers
app = FastAPI(
    title="Payment",

)

app.mount("/static", StaticFiles(directory="src/static"), name="static")


origins = [
    "http://localhost:3000",
]

app.include_router(auth_router)
for i in all_routers:
    app.include_router(i)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

#
# @app.on_event("startup")
# async def startup_event():
#     redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

