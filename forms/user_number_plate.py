from flask_wtf import RecaptchaField
from .violation_lookup import ViolationLookupForm

class UserNumberPlate(ViolationLookupForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.submit.label.text = "LƯU LẠI BIỂN SỐ XE CỦA TÔI"

class UserNumberPlateWithRecaptcha(UserNumberPlate):
  recaptcha = RecaptchaField("reCAPTCHA")