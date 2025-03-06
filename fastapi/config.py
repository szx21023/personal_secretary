from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # db config
    MONGODB_SETTINGS: dict = {
        "host": "127.0.0.1",
        "port": 27017,
        "db_name": "personal_sercretary",
        "username": "",
        "password": "",
        "ssl": False,
        "ssl_ca_certs": "",
        "retryWrites": False
    }

    # swagger docs config
    DOCS_URL: str|None = '/docs'
    REDOC_URL: str|None = '/redoc'
    OPENAPI_URL: str|None = '/openapi.json'

    # aws config
    AWS_ACCESS_KEY_ID: str = ''
    AWS_SECRET_KEY: str = ''
    AWS_REGION: str = ''
    AWS_LOGGROUP_NAME: str = ''

    # line config
    LINE_CHANNEL_ACCESS_TOKEN: str = ''
    LINE_CHANNEL_SECRET: str = ''

    # cron config
    CRON_DAILY_EVENT_EVERYDAY_REMINDING: str = '00 00 * * *'
    CRON_DAILY_EVENT_DELAY: str = '* * * * *'

    model_config = SettingsConfigDict(env_file=".env")
