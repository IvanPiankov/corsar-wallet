from dotenv import load_dotenv
from environs import Env

load_dotenv()
env = Env()

SECONDS_IN_MINUTES = 60
SECONDS_IN_HOURS = SECONDS_IN_MINUTES * 60
SECONDS_IN_DAY = SECONDS_IN_HOURS * 24


class Settings:
    PG_HOST = env.str("PG_HOST")
    PG_PORT = env.int("PG_PORT", 5432)
    PG_USER = env.str("PG_USER")
    PG_PASSWORD = env.str("PG_PASSWORD")
    PG_DB = env.str("PG_DB")
    PG_MIGRATE_URL = "postgresql://" f"{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

    ACCESS_TOKEN_EXPIRE_MINUTES = SECONDS_IN_MINUTES * 30
    REFRESH_TOKEN_EXPIRE_MINUTES = SECONDS_IN_DAY * 7
    ALGORITHM = "HS256"
    JWT_SECRET_KEY = env.str('JWT_SECRET_KEY')  # jwk secret for generate jwt
    JWT_REFRESH_SECRET_KEY = env.str('JWT_REFRESH_SECRET_KEY')  # jkk for refresh token

    @classmethod
    def get_pg_url(cls) -> str:
        return (
            f"postgresql+asyncpg://:@?dsn=postgresql://:@{cls.PG_HOST}/"
            f"{cls.PG_DB}&port={cls.PG_PORT}&user={cls.PG_USER}&password={cls.PG_PASSWORD}"
        )
