from pydantic import BaseSettings


class Settings(BaseSettings):
    BAKONG_DEV_TOKEN: str = ""
    BAKONG_BANK_ACCOUNT: str = ""
    API_SECRET: str = ""
    BAKONG_APP_ICON_URL: str = ""
    BAKONG_CALLBACK_URL: str = ""

    BAKONG_MERCHANT_NAME: str = "SORIYA MOY"
    BAKONG_MERCHANT_CITY: str = "Phnom Penh"
    BAKONG_APP_NAME: str = "Room Rental"
    BAKONG_PHONE_NUMBER: str = "85566455124"
    BAKONG_DEFAULT_CURRENCY: str = "USD"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()