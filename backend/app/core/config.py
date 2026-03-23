from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Task & Knowledge Management System"
    API_V1_PREFIX: str = "/api/v1"

    SECRET_KEY: str = "change-this-to-a-long-random-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "root"
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_DB: str = "ai_task_knowledge"

    UPLOAD_DIR: str = "uploads"
    CHROMA_DIR: str = "chroma_store"

    SEARCH_DISTANCE_THRESHOLD: float = 0.65

    GEMINI_ENABLED: bool = False
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-3-flash-preview"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
        )


settings = Settings()