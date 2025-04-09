from flask_wtf.recaptcha import validators

validators.RECAPTCHA_ERROR_CODES = {
  "missing-input-secret": "Thiếu tham số bí mật.",
  "invalid-input-secret": "Tham số bí mật không hợp lệ hoặc sai phương thức.",
  "missing-input-response": "Không nhận được tín hiệu trả lời từ reCAPTCHA.",
  "invalid-input-response": "Tín hiệu trả lời từ reCAPTCHA không hợp lệ hoặc sai phương thức.",
}