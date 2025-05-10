from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    mongo_uri: str = Field(..., env="MONGO_URI")
    db_name: str = Field(..., env="DB_NAME")
    google_api_key: str = Field(..., env="GOOGLE_API_KEY")
    rss_feeds: str = Field(..., env="RSS_FEEDS")
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")

    class Config:
        """Configurations for Pydantic settings."""

        env_file = ".env"  # Load variables from a .env file if present
        env_file_encoding = "utf-8"


settings = Settings()
