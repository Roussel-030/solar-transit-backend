import logging

from sqlalchemy import text
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.session import SessionLocal

import crud
import schemas
from models.users import UserRole

from core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 3  # 3 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        db = SessionLocal()
        # Try to create session to check if DB is awake
        db.execute(text('Select 1'))
        admin = crud.users.get_by_username(db=db, username=settings.DEFAULT_USER_ADMIN)
        if not admin:
            user_in = schemas.UsersCreate(username=settings.DEFAULT_USER_ADMIN, password=settings.DEFAULT_PASSWORD,
                                          role=UserRole.ADMIN)
            crud.users.create(db=db, obj_in=user_in)
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Connecting to the mysql")
    init()
    logger.info("Mysql connected")


if __name__ == "__main__":
    main()
