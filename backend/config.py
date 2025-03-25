from os import environ
from typing import Union

from pydantic_settings import BaseSettings

TESTING = bool(environ.get("TESTING", True))


class ProjectSettings(BaseSettings):
    """Класс настроек проекта."""

    RUN_MODE: str

    POSTGR_TYPE: str
    POSTGR_ENGINE: str
    POSTGR_DB_HOST: str
    POSTGR_DB_PORT: int
    POSTGR_DB_USER: str
    POSTGR_DB_PASS: str
    POSTGR_DB_NAME: str

    REDIS_HOSTNAME: str
    REDIS_PORT: int

    EMAIL_HOST: str
    EMAIL_PORT: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRES_IN: int

    PATH_TO_APP: str
    APP_NAME: str

    TEST_URL: str

    DEFAULT_URL_PREFIX_V1: str
    DEFAULT_TAG_V1: str

    USERS_PREFIX: str
    USERS_TAG: str

    @property
    def get_database_url(self) -> str:
        """Формирует и возвращает Database URL."""

        database_url = (
            f'{self.POSTGR_ENGINE}+{self.POSTGR_TYPE}://{self.POSTGR_DB_USER}:{self.POSTGR_DB_PASS}@'
            f'{self.POSTGR_DB_HOST}:{self.POSTGR_DB_PORT}/{self.POSTGR_DB_NAME}'
        )

        return database_url

    @property
    def get_redis_host_and_port(self) -> dict[str, Union[str, int]]:
        return {'host': self.REDIS_HOSTNAME, 'port': self.REDIS_PORT}

    @property
    def get_auth_data(self) -> dict[str, str]:
        return {"secret_key": settings.JWT_SECRET_KEY, "algorithm": settings.JWT_ALGORITHM}

    class Config:
        env_file = '.test_env' if TESTING else '.env'


settings = ProjectSettings()
