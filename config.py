from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # API
    PROJECT_NAME: str = "Caspian Pollution Monitor"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # File Upload
    UPLOAD_DIR: str = "app/static/uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: str = ".jpg,.jpeg,.png,.webp"

    @property
    def ALLOWED_EXTENSIONS_SET(self) -> set:
        return set(self.ALLOWED_EXTENSIONS.split(','))

    # Rate Limiting
    RATE_LIMIT_POINTS: int = 5
    RATE_LIMIT_ENABLED: bool = True

    # Geo
    CASPIAN_MIN_LAT: float = 36.5
    CASPIAN_MAX_LAT: float = 47.5
    CASPIAN_MIN_LON: float = 46.5
    CASPIAN_MAX_LON: float = 54.5

    # CORS
    CORS_ORIGINS: str = "http://localhost,http://localhost:8000"

    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(',')]

    # MinIO/S3 (optional)
    MINIO_ENDPOINT: Optional[str] = None
    MINIO_ACCESS_KEY: Optional[str] = None
    MINIO_SECRET_KEY: Optional[str] = None
    MINIO_BUCKET: str = "pollution-images"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()