from pydantic_settings import (
    BaseSettings,
)


class ProjectSettings(BaseSettings):
    """Класс настроек проекта."""

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    ENGINE: str
    TYPE: str

    PATH_TO_APP: str
    APP_NAME: str

    TEST_URL: str

    DEFAULT_URL_PREFIX_V1: str
    DEFAULT_TAG_V1: str

    USERS_PREFIX: str
    USERS_TAG: str

    @property
    def get_database_url(cls) -> str:
        """Формирует из возвращает Database URL."""

        database_url = f'{cls.ENGINE}+{cls.TYPE}://{cls.DB_USER}:{cls.DB_PASS}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}'

        return database_url

    class Config:
        env_file = '.env'


settings = ProjectSettings()
