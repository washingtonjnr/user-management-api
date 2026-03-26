from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    jwt_secret_key: str = Field(...)
    jwt_access_token_expires: int = Field(1)

    db_password: str = Field(...)
    database_url: str = Field(...)
    db_track_modifications: bool = False

    title: str = Field("Managements Users")
    version: str = Field("1.0.0")

    openapi_version: str = "3.0.3"
    openapi_url_prefix: str = "/"
    openapi_swagger_ui_path: str = "/docs"
    openapi_swagger_ui_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    dummy_url: str = Field(...)

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="APP_", case_sensitive=False, extra="ignore"
    )


settings = Settings()
