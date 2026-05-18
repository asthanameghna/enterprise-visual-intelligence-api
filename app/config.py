from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "enterprise-visual-intelligence-api"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    model_config = {"env_file": ".env"}


settings = Settings()
