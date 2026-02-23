from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BAKONG_DEV_TOKEN: str = ""
    BAKONG_BANK_ACCOUNT: str = ""
    API_SECRET: str = ""
    BAKONG_MERCHANT_NAME: str = "moy_soriya@bkrt"
    BAKONG_MERCHANT_CITY: str = "Phnom Penh"
    BAKONG_APP_NAME: str = "Room Rental"
    BAKONG_APP_ICON_URL: str = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQb17OLPVxDbgiMnuuXiy3uJoJaUQRsGB6y8Q&s"
    BAKONG_CALLBACK_URL: str = "http://localhost:3000/payment/success"
    BAKONG_PHONE_NUMBER: str = "85566455124"
    BAKONG_DEFAULT_CURRENCY: str = "USD"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()