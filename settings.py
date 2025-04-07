DOMAIN = "localhost"
SERVER_NAME = "localhost"
PORT = 80
DEBUG_STATUS = True
USE_SSL_CONTEXT_ON_MAIN_SERVER = False
SSL_CONTEXT = ("server.pem", "server-key.pem")
SSL_CONTEXT_TO_USE = SSL_CONTEXT if USE_SSL_CONTEXT_ON_MAIN_SERVER else None
USE_EVAL_EXECUTIONS = False
ALLOWED_HOST = [
  "0.0.0.0"
]
DATABASE_FILENAME = "database"

API_VERSION = 1
RESTFUL_JSON_SETTINGS = {
  "ensure_ascii": False
}

# TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSERACT_CMD = None
CAPTCHA_IMAGE_PATH = "img/captcha.png"
CUSTOM_SESSION_HEADER = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}
# TomChienXu Note: You can change this to whatever you want.
# This will be used as soon as the session is initialized.
# STATIC_SESSION_COOKIE_PHPSESSID = "a4ipsbe4jfv5qu8avhgb5o0ut3"
STATIC_SESSION_COOKIE_PHPSESSID = "doilucnolaskibididopdopyesyes"
DEFAULT_DATA_SOURCE = "Cổng thông tin điện tử Cục CSGT"
DEFAULT_VEHICLE_NUMBER_PLATE = "30K13784"
DEFAULT_VEHICLE_TYPE = "1"

SAVE_LAST_CAPTCHA_IMAGE = False
SOLVE_CAPTCHA_MANUALLY = False
DELAY_AFTER_WRONG_CAPTCHA = 0.5
MAX_CAPTCHA_ATTEMPTS = 10

IP_CLIENT = "9.9.9.91"
C_URL = "https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html"
CAPTCHA_URL = "https://www.csgt.vn/lib/captcha/captcha.class.php"
POST_DATA_URL = "https://www.csgt.vn/?mod=contact&task=tracuu_post&ajax"