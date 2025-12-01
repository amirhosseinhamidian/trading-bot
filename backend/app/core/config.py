from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Trading Bot Backend"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql+psycopg://user:password@localhost:5432/trading_bot"
    # حتماً مقدار واقعی رو توی .env ست کن

    class Config:
        env_file = ".env"


settings = Settings()
