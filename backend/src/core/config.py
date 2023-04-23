from dotenv import find_dotenv
from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    PROJECT_NAME: str = "peppermint"
    API_VERSION_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_HOST: str

    POSTGRES_DSN: PostgresDsn
    POSTGRES_PASSWORD: str

    USERS_OPEN_REGISTRATION: bool = False

    UPLOAD_DIR: str

    # email/smtp settings
    EMAILS_ENABLED: bool
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int
    EMAIL_TEMPLATES_DIR: str
    EMAILS_FROM_NAME: str
    EMAILS_FROM_EMAIL: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    class Config:
        env_file = find_dotenv(usecwd=True)


settings = Settings()
