from app.db import base  # noqa: F401
from app.db.session import engine
from app.db.base_class import Base

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
def init_db() -> None:
    Base.metadata.create_all(bind=engine)
