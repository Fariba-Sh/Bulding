SECRET_KEY = "DLOHNCFDSHCHSDGBHSVHJubguishhcsbvgfyusggT!@@!@@55565656r56454r"


SQLALCHEMY_DATABASE_URI = "sqlite:///Building1.db"


ADMIN_USERNAME = 'fari_sh_aqw'

ADMIN_PASSWORD = 'hdejkfnfeujrfeufcbcb67644'


ZARINPAL_MERCHANT_ID = "00000000-0000-0000-0000-000000000000"

ZARINPAL_REQUEST_URL = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZARINPAL_VERIFY_URL = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZARINPAL_STARTPAY_URL = "https://sandbox.zarinpal.com/pg/StartPay/{authority}"

ZARINPAL_CALLBACK_URL = "http://127.0.0.1:8086/user/payment/verify"