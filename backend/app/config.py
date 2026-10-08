from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Adizz"
    app_version: str = "1.0.0"
    database_url: str = (
        "postgresql://adizz:adizz_password@localhost:5432/adizz"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()