"""
backend/database/init_db.py

Database initialization for FitTrack.

Two things need to happen before the app can use MySQL:

  1. The `fittrack` database itself has to exist on the MySQL server.
     SQLAlchemy's create_all() only creates TABLES -- it assumes the
     database already exists -- so we connect without a database
     selected and issue CREATE DATABASE IF NOT EXISTS ourselves.

  2. Every table (all 14 models) has to be created via
     Base.metadata.create_all(). That requires every model class to
     already be imported (so it's registered on Base.metadata) --
     `import backend.models` guarantees that.

Run with:
    python -m backend.database.init_db

(run from the fittrack/ project root, with a MySQL server reachable
at the host/port/credentials configured in .env)
"""

import pymysql

from backend.config import settings
from backend.database.session import Base, engine

import backend.models  # noqa: F401  (imported for its side effect)


def create_database_if_not_exists() -> None:
    connection = pymysql.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{settings.db_name}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        connection.commit()
    finally:
        connection.close()


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def init_db() -> None:
    create_database_if_not_exists()
    create_tables()


if __name__ == "__main__":
    init_db()
    print(f"FitTrack database '{settings.db_name}' and all tables are ready.")