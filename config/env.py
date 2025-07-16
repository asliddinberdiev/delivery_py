import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    # app
    app_name: str = os.getenv("APP_NAME", "Delivery")
    app_is_dev: bool = bool(os.getenv("APP_IS_DEV", True))
    app_log_level: str = os.getenv("APP_LOG_LEVEL", "INFO")
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", 8888))

    # auth
    auth_secret_key: str = os.getenv("AUTH_SECRET_KEY", "secret_key")

    # postgres
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", 5432))
    postgres_user: str = os.getenv("POSTGRES_USER", "database_user")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "database_password")
    postgres_db: str = os.getenv("POSTGRES_DATABASE", "database_name")

    def get_postgres_url(self) -> str:
        return f"{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}?sslmode=disable"

cfg = Config()
