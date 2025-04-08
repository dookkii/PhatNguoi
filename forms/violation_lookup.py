from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SelectField
from wtforms.validators import DataRequired

class ViolationLookupForm(FlaskForm):
  number_plate = StringField("Biển số xe", validators=[DataRequired()])
  vehicle_type = SelectField("Loại xe", choices=[
    ("1", "Xe ô tô"),
    ("2", "Xe máy"),
    ("3", "Xe đạp điện")
  ], validators=[DataRequired()])