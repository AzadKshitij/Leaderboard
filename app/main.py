from fastapi import FastAPI, status
import logging
from starlette.middleware.cors import CORSMiddleware
from app.core.config import config
from app.api.api import api_router
from app.logger import logger

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S"
                    )

logger.debug("Creating GameLitics app instance")

app = FastAPI(
    title=config.get("PROJECT_NAME")
)
app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in config.get("BACKEND_CORS_ORIGINS")],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

app.include_router(api_router) # , prefix=settings.API_V1_STR)

@app.get("/healthcheck", status_code=status.HTTP_200_OK)
def root():
    return {"message": "Root of the app"}
