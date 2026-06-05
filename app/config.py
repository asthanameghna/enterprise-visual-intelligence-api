from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "enterprise-visual-intelligence-api"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/visual_intelligence"

    model_config = {"env_file": ".env"}


settings = Settings()
