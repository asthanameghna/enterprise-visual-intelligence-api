from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "enterprise-visual-intelligence-api"


settings = Settings()
