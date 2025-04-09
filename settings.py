HOST = ""
SERVER_NAME = ""
PORT = 80
DEBUG_STATUS = False
USE_SSL_CONTEXT_ON_MAIN_SERVER = False
SSL_CONTEXT = ("server.pem", "server-key.pem")
SSL_CONTEXT_TO_USE = SSL_CONTEXT if USE_SSL_CONTEXT_ON_MAIN_SERVER else None
USE_EVAL_EXECUTIONS = False
ALLOWED_HOSTS = []
DATABASE_FILENAME = "database"

API_VERSION = 1
RESTFUL_JSON_SETTINGS = {
  "ensure_ascii": False
}

SUBDOMAIN_API = "api"
SUBDOMAIN_MAIN_PAGE = None

USE_RECAPTCHA = True
RECAPTCHA_PARAMETERS = {
  "hl": "en",
  "render": "onload"
}
RECAPTCHA_DATA_ATTRS = {
  "theme": "dark"
}
RECAPTCHA_SCRIPT = "https://www.google.com/recaptcha/api.js"
RECAPTCHA_DIV_CLASS = "g-recaptcha"
RECAPTCHA_VERIFY_SERVER = "https://www.google.com/recaptcha/api/siteverify"

TESSERACT_CMD = None
CAPTCHA_IMAGE_PATH = ""
CUSTOM_SESSION_HEADER = {}
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

# TomChienXu Note: local_settings.py loader.
try:
  from os import path

  with open(path.join(
    path.dirname(__file__),
    "local_settings.py"
  )) as file:
    exec(file.read(), globals())

except IOError:
  pass