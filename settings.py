from environs import Env

env = Env()


class Settings:
    PG_HOST = env.str("PG_HOST")
    PG_PORT = env.int("PG_PORT", 5432)
    PG_USER = env.str("PG_USER")
    PG_PASSWORD = env.str("PG_PASSWORD")
    PG_DB = env.str("PG_DB")
