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
  submit_my_number_plate = SubmitField("TRA CỨU BIỂN SỐ CỦA TÔI")
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    self.is_my_plate = False
    
  def validate_on_submit(self, extra_validators=None):
    if self.is_my_plate:
      self.number_plate.validators = []
      
    return super().validate_on_submit(extra_validators)

class ViolationLookupFormWithRecaptcha(ViolationLookupForm):
  recaptcha = RecaptchaField("reCAPTCHA")