from io import BytesIO
from time import sleep
from requests import Session
from requests.cookies import cookiejar_from_dict
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from PIL import Image
from pytesseract import pytesseract
import ssl

from settings import *

# TomChienXu Note: If you don't add Tesseract's path into your computer's environment, you
#                  could provide it here.
pytesseract.tesseract_cmd = TESSERACT_CMD

class TLSAdapter(HTTPAdapter):
  def init_poolmanager(self, *args, **kwargs):
    context = ssl.create_default_context()
    context.set_ciphers("DEFAULT:@SECLEVEL=1")
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    kwargs["ssl_context"] = context
    return super().init_poolmanager(*args, **kwargs)

def get_new_session(phpsessid=None):
  new_session = Session()
  new_session.mount("https://", TLSAdapter())
  new_session.headers = CUSTOM_SESSION_HEADER

  if phpsessid is not None:
    new_session.cookies = cookiejar_from_dict(dict(PHPSESSID=phpsessid))
  print("Session cookie PHPSESSID:", repr(new_session.cookies.get_dict()))

  return new_session

def solve_captcha(session, solve_manually):
  captcha_post = session.post(CAPTCHA_URL)

  with BytesIO(captcha_post.content) as raw_file:
    with Image.open(raw_file) as image:
      if SAVE_LAST_CAPTCHA_IMAGE:
        image.save("img.png")

      if solve_manually:
        captcha = input("Enter CAPTCHA manually: ")
      else:
        captcha = pytesseract.image_to_string(image)
      
      captcha = captcha.lower().replace(".", "").strip()
      print("Solved CAPTCHA:", repr(captcha))

  return captcha

def post_vehicle_data(session, captcha, vehicle_data=None):
  data = {
    "BienKS": vehicle_data.get("BienKS", "30K13784"),
    "Xe": vehicle_data.get("Xe", "30K13784"),
    "captcha": captcha,
    "ipClient": IP_CLIENT,
    "cUrl": C_URL
  }

  response = session.post(POST_DATA_URL, data=data)
  response_text = response.text.strip()
  print("Response:", repr(response_text))

  if response_text == "404":
    return None
  else:
    return response

def get_data(session, response):
  try:
    result = response.json()

    if not result.get("success") == "true":
      raise RuntimeError("Something is wrong?")

    web_response = session.get(result.get("href"))
    soup = BeautifulSoup(web_response.content, "html.parser")
    
    data = soup.find("div", id="bodyPrint123")

    if data.get_text(strip=True) == "Không tìm thấy kết quả !":
      print("Không tìm thấy kết quả !")
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

            current_violation[special_key] = addresses
          else:
            current_violation[key] = val

    # TomChienXu Note: Should never reach here, since every violation ends with a <hr>
    if current_violation:
      violations.append(current_violation)

    for index, violation in enumerate(violations):
      print(f"Violation {index + 1}:")
      for key, value in violation.items():
        print(f"{key}: {value}")
      print("\n" + "="*50 + "\n")
  except:
    print("Nuhuh")


def main():
  session = get_new_session()

  bien_so_xe = input("Nhập biển số xe: ")
  loai_xe = input("Nhập loại xe: ")

  while True:
    captcha = solve_captcha(session, SOLVE_CAPTCHA_MANUALLY)
    "30K13784"
    response = post_vehicle_data(session, captcha, dict(BienKS=bien_so_xe, Xe=loai_xe))

    if response is not None:
      print("Done!")
      print("Session cookie PHPSESSID after process:", repr(session.cookies.get_dict()))
      print("----------------")
      break

    sleep(2)

  get_data(session, response)

if __name__ == "__main__":
  main()
