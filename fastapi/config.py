from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # db config
    MONGODB_SETTINGS: dict = {
        "host": "ps-mongodb",
        "port": 27017,
        "db_name": "personal_sercretary",
        "username": "root",
        "password": "example",
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
    LINE_CHANNEL_ACCESS_TOKEN: str = 'VVsvv/tgNZq7y4hM8+Ggd2/+cdR21TdeMglwAIiPAhlNjyx+M+uEQlRQ5ZFJE8bMInrpSqJSI3Bg2p+RIO5wGlqnhLZ2pw+jVZaxe0AZU5uZqfZbCczYYYZtIiuO8M9MxmR8sG6m1Psl6yiCmoiTrQdB04t89/1O/w1cDnyilFU='
    LINE_CHANNEL_SECRET: str = '260ca420b318a7cb3838ddf2fd56217d'

    model_config = SettingsConfigDict(env_file=".env")