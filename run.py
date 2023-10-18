import asyncio
from http import client
from hypercorn.config import Config
from hypercorn.asyncio import serve
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
import logging

from app.main import app
from app.db.init_db import init_db
from app.db.session import SessionLocal

# Debugging
debug_config = {
    "debug": True,
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60  # 1 minute
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    logger.info("Creating initial data")
    try:
        init_db()
        logger.info("Initial data created")
        start_app()
    except Exception as e:
        logger.error(e)
        raise e

def start_app() -> None:
    logger.info("Starting app")
    # uvicorn.run("app", host="127.0.0.1", port=8000, log_level="info",  reload=True)

    # asyncio.run(serve(app,Config().from_mapping(debug_config)))
    asyncio.run(serve(app,Config()))
    

if __name__ == "__main__":
    init()