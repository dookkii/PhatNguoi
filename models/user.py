from flask_login import UserMixin
from arrow import utcnow
from sqlalchemy.sql import expression

from pages import database

class User(database.Model, UserMixin):
  id = database.Column(database.Integer, primary_key=True)
  email = database.Column(database.String, unique=True, nullable=False)
  password = database.Column(database.String, nullable=True)
  name = database.Column(database.String, nullable=True)
  active = database.Column(database.Boolean, default=expression.true())
  oauth2_token = database.Column(database.Text)
  avatar_url = database.Column(database.Text)
  created_at = database.Column(database.DateTime, default=utcnow().datetime)
  last_login = database.Column(database.DateTime)
  last_ip = database.Column(database.String)
  premium = database.Column(database.Boolean, default=expression.false())
  number_plate = database.Column(database.String)
  vehicle_type = database.Column(database.Integer)
  
  api_key = database.Column(database.String, unique=True)
  api_key_created_at = database.Column(database.DateTime, default=utcnow().datetime)
  api_key_reset_count = database.Column(database.Integer, default=0)
  api_key_usage_count = database.Column(database.Integer, default=0)