from typing import List, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    TEST_DB_HOST: str
    TEST_DB_PORT: str
    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASS: str

    @property
    def TEST_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    TOKEN_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    
    MIN_PASSWORD_LENGTH: int
    MAX_PASSWORD_LENGTH: int
    
    MIN_USERNAME_LENGTH: int
    MAX_USERNAME_LENGTH: int
    
    PASSWORD_HASH_NAME: str
    PASSWORD_HASH_ITERATIONS: int
    PASSWORD_SALT_SEPARATOR: str
    
    CORS_ORIGINS: List[str]
    CORS_HEADERS: List[str]
    CORS_METHODS: List[str]
    CORS_CREDENTIALS: bool
    
    ROOT_DIR: str
    UPLOAD_DIR: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings: Settings = Settings()