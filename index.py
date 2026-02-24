# import os
# from datetime import datetime
# from bakong_khqr import KHQR

# MERCHANT_BANK = os.getenv("MERCHANT_BANK")
# MERCHANT_NAME = os.getenv("MERCHANT_NAME")
# MERCHANT_CITY = os.getenv("MERCHANT_CITY")
# STORE_LABEL = os.getenv("STORE_LABEL")
# PHONE_NUMBER = os.getenv("PHONE_NUMBER")
# TERMINAL_LABEL = os.getenv("TERMINAL_LABEL")

# CURRENCY = "USD"


# def _require_env(value: str | None, name: str) -> str:
#     if not value or not str(value).strip():
#         raise ValueError(f"Missing {name} in environment")
#     return value.strip()


# def generate_bill_no(order_id: str) -> str:
#     short_id = order_id.replace("-", "").replace("_", "")[:6].upper()
#     date_part = datetime.utcnow().strftime("%y%m%d")
#     return f"INV{date_part}{short_id}"[:25]


# def create_khqr(amount_usd: float, bill_no: str) -> str:
#     bank_account = _require_env(MERCHANT_BANK, "MERCHANT_BANK")
#     merchant_name = _require_env(MERCHANT_NAME, "MERCHANT_NAME")
#     merchant_city = _require_env(MERCHANT_CITY, "MERCHANT_CITY")

#     if amount_usd <= 0:
#         raise ValueError("amount_usd must be > 0")

#     khqr = KHQR()
#     qr_string = khqr.create_qr(
#         bank_account=bank_account,
#         merchant_name=merchant_name,
#         merchant_city=merchant_city,
#         amount=round(float(amount_usd), 2),
#         currency=CURRENCY,
#         bill_number=bill_no,
#         store_label=(STORE_LABEL or "").strip() or None,
#         phone_number=(PHONE_NUMBER or "").strip() or None,
#         terminal_label=(TERMINAL_LABEL or "").strip() or None,
#     )

#     if not qr_string or len(qr_string) < 10:
#         raise ValueError("Failed to generate KHQR payload")

#     return qr_string
