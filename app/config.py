from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    jose_secret_key: str
    jose_algorithm: str
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()