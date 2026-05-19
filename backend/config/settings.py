from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str
    tavily_api_key: str

    class Config:
        # Path is relative to the working directory when uvicorn starts (backend/),
        # so "../.env" resolves to the project root where the .env file lives.
        env_file = "../.env"


settings = Settings()  # type: ignore
