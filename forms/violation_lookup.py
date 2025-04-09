from flask_wtf import FlaskForm
from flask_wtf import RecaptchaField
from wtforms import StringField
from wtforms import SelectField
from wtforms import SubmitField
from wtforms.validators import DataRequired

class ViolationLookupForm(FlaskForm):
  number_plate = StringField("Biển số xe", validators=[DataRequired()])
  vehicle_type = SelectField("Loại xe", choices=[
    ("1", "Xe ô tô"),
    ("2", "Xe máy"),
    ("3", "Xe đạp điện")
  ], validators=[DataRequired()])
  submit = SubmitField("TRA CỨU")

class ViolationLookupFormWithRecaptcha(ViolationLookupForm):
  recaptcha = RecaptchaField("reCAPTCHA")