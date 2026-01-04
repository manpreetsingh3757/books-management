from pydantic_settings  import BaseSettings

class Settings(BaseSettings):
    PROJECT_TITLE: str
    PROJECT_VERSION: str
    API_VERSION: str
    database_url: str
    database_url_sync: str
    production: bool
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ai_model_key: str
    ai_model: str
    
    class Config:
        env_file = ".env"

settings = Settings()
