from io import BytesIO
from bs4 import BeautifulSoup
from PIL import Image
from time import sleep
from datetime import datetime

from settings import CAPTCHA_URL
from settings import SAVE_LAST_CAPTCHA_IMAGE
from settings import CAPTCHA_IMAGE_PATH
from settings import DEFAULT_DATA_SOURCE
from settings import DEFAULT_VEHICLE_NUMBER_PLATE
from settings import DEFAULT_VEHICLE_TYPE
from settings import IP_CLIENT
from settings import C_URL
from settings import POST_DATA_URL
from settings import SOLVE_CAPTCHA_MANUALLY
from settings import DELAY_AFTER_WRONG_CAPTCHA
from settings import MAX_CAPTCHA_ATTEMPTS
from helpers import unaccent_word
from helpers.custom_session import get_new_session
from handlers.image_to_text import image_to_string  

class ViolationDataPostSession:
  def __init__(self, vehicle_data=None, phpsessid=None):
    self.vehicle_data = vehicle_data or {}
    self.session = get_new_session(phpsessid)
    self.captcha = None
    self.solved_captcha = False
    self.response = None
    self.violations = []

  def post_solve_session_captcha(self, solve_manually=None):
    captcha_post = self.session.post(CAPTCHA_URL)

    with BytesIO(captcha_post.content) as raw_file:
      with Image.open(raw_file) as image:
        if SAVE_LAST_CAPTCHA_IMAGE:
          image.save(CAPTCHA_IMAGE_PATH)

        if solve_manually:
          captcha = input("Enter CAPTCHA manually: ")
        else:
          captcha = image_to_string(image)
        
    self.captcha = captcha.lower().replace(".", "").strip()

  def post_vehicle_data(self):
    data = {
      "BienKS": self.vehicle_data.get("BienKS", DEFAULT_VEHICLE_NUMBER_PLATE),
      "Xe": self.vehicle_data.get("Xe", DEFAULT_VEHICLE_TYPE),
      "captcha": self.captcha,
      "ipClient": IP_CLIENT,
      "cUrl": C_URL
    }

    response = self.session.post(POST_DATA_URL, data=data)
    response_text = response.text.strip()

    if response_text != "404":
      self.solved_captcha = True
      self.response = response

  def handle_data(self):
    if not self.solved_captcha or self.response is None:
      return

    result = self.response.json()

    if not result.get("success") == "true":
      raise Exception("Something is wrong with the parent website!")

    web_response = self.session.get(result.get("href"))
    soup = BeautifulSoup(web_response.content, "html.parser")
    
    data = soup.find("div", id="bodyPrint123")

    if data.get_text(strip=True) == "Không tìm thấy kết quả !":
      return
    
    sections = data.find_all(["div", "hr"], recursive=False)

    violations = []
    current_violation = {}

    for element in sections:
      if element.name == "hr":
        if current_violation:
          violations.append(current_violation)
          current_violation = {}
      else:
        label = element.find("label", class_="control-label")
        value = element.find("div", class_="col-md-9")

        if label and value:
          key = label.get_text(strip=True).replace(":", "").strip()
          val = value.get_text(strip=True)

          special_key = "Nơi giải quyết vụ việc"
          if label and special_key in label.get_text(strip=True):
            addresses = []
            for sibling in element.find_next_siblings(["div", "hr"]):
              if sibling.name == "hr":
                break
              if "form-group" in sibling.attrs["class"]:
                addresses.append(sibling.get_text(strip=True))

            current_violation[unaccent_word(special_key)] = addresses
          else:
            current_violation[unaccent_word(key)] = val

    # TomChienXu Note: Should never reach here, since every violation ends with a <hr>.
    if current_violation:
      violations.append(current_violation)

    self.violations = violations

# TomChienXu Note: This function uses time.sleep() to wait for retrying to solve
# in case the captcha is wrong. It is strongly recommended to call this function
# in a separate thread to avoid blocking the main thread, as time.sleep() can 
# cause delays in the program's execution.
def safely_get_violations(bien_so_xe, loai_xe):
  bien_so_xe = bien_so_xe.strip()
  loai_xe = {
    "1": 1,
    "2": 2,
    "3": 3,
    "oto": 1,
    "xemay": 2,
    "xedap": 3,
  }.get(loai_xe.strip(), 1)

  session = ViolationDataPostSession(dict(BienKS=bien_so_xe, Xe=loai_xe))
  
  for index in range(MAX_CAPTCHA_ATTEMPTS):
    session.post_solve_session_captcha(SOLVE_CAPTCHA_MANUALLY)

    session_time = datetime.now()
    session.post_vehicle_data()

    if session.solved_captcha:
      print(f"({index + 1}) Captcha solved:", session.captcha)
      break
    
    sleep(DELAY_AFTER_WRONG_CAPTCHA)
    print(f"({index + 1}) Wrong Captcha:", session.captcha)
  else:
    print("Captcha failed after maximum attempts.")
  
  session.handle_data()
  return dict(
    time=session_time.strftime("%d-%m-%Y %H:%M:%S"),
    source=DEFAULT_DATA_SOURCE,
    number_plate=bien_so_xe,
    vehicle_type=loai_xe,
    violations=session.violations if session.solved_captcha else None
  )