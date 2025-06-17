from secrets import choice
from string import ascii_letters
from string import digits

def generate_api_key(length=32, prefix="", suffix=""):
  characters = ascii_letters + digits
  
  random_part = "".join(choice(characters) for _ in range(length))
  
  api_key = f"{prefix}{random_part}{suffix}"
  return api_key