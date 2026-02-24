from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from decimal import Decimal, ROUND_HALF_UP
from bakong_khqr import KHQR
from app.config import settings  # adjust if inside app folder

app = FastAPI()


class PaymentRequest(BaseModel):
    booking_id: str = Field(..., min_length=1)
    amount: Decimal = Field(..., gt=0)


def verify_api_key(x_api_key: str):
    if x_api_key != settings.API_SECRET:
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.post("/generate_qr")
def generate_qr(request: PaymentRequest, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)

    try:
        khqr = KHQR()

        amount = Decimal(str(request.amount)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        qr_string = khqr.create_qr(
            bank_account=settings.BAKONG_BANK_ACCOUNT,
            merchant_name=settings.BAKONG_MERCHANT_NAME,
            merchant_city=settings.BAKONG_MERCHANT_CITY,
            amount=float(amount),
            currency=settings.BAKONG_DEFAULT_CURRENCY,
            bill_number=str(request.booking_id),
            store_label=settings.BAKONG_APP_NAME,
            phone_number=settings.BAKONG_PHONE_NUMBER,
            terminal_label=f"BOOKING_{request.booking_id}",
            static=False
        )

        return {"success": True, "qr_string": qr_string}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))