import random
import string
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from bakong_khqr import KHQR
from app.config import settings


app = FastAPI(title="KHQR Payment Service")


# =========================
# Request Models
# =========================

class PaymentRequest(BaseModel):
    amount: float
    booking_id: str   # ASP.NET should send this


class PaymentStatusRequest(BaseModel):
    md5: str


# =========================
# Utility Functions
# =========================

def get_khqr_instance() -> KHQR:
    if not settings.BAKONG_DEV_TOKEN:
        raise HTTPException(status_code=500, detail="BAKONG_DEV_TOKEN not configured")
    return KHQR(settings.BAKONG_DEV_TOKEN)


def verify_api_key(x_api_key: str):
    if x_api_key != settings.API_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")


# =========================
# Generate QR Endpoint
# =========================

@app.post("/generate_qr")
def generate_qr(
    request: PaymentRequest,
    x_api_key: str = Header(...)
):
    verify_api_key(x_api_key)

    khqr = get_khqr_instance()

    try:
        qr_string = khqr.create_qr(
            bank_account=settings.BAKONG_BANK_ACCOUNT,
            merchant_name=settings.BAKONG_MERCHANT_NAME,
            merchant_city=settings.BAKONG_MERCHANT_CITY,
            amount=request.amount,
            currency=settings.BAKONG_DEFAULT_CURRENCY,
            store_label=settings.BAKONG_APP_NAME,
            phone_number=settings.BAKONG_PHONE_NUMBER,
            bill_number=request.booking_id,
            terminal_label="FastAPI-Server",
            static=False,
        )

        deeplink = khqr.generate_deeplink(
            qr_string,
            callback=settings.BAKONG_CALLBACK_URL,
            appIconUrl=settings.BAKONG_APP_ICON_URL,
            appName=settings.BAKONG_APP_NAME,
        )

        md5 = khqr.generate_md5(qr_string)

        return {
            "success": True,
            "qr_string": qr_string,
            "deeplink": deeplink,
            "md5": md5,
            "bill_number": request.booking_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# Check Payment Endpoint
# =========================

@app.post("/check_payment_status")
def check_payment_status(
    request: PaymentStatusRequest,
    x_api_key: str = Header(...)
):
    verify_api_key(x_api_key)

    khqr = get_khqr_instance()

    try:
        status = khqr.check_payment(request.md5)

        return {
            "success": True,
            "status": status,
            "is_paid": status == "PAID"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))