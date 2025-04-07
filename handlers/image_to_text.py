import pytesseract
from pytesseract import pytesseract

from settings import TESSERACT_CMD

# TomChienXu Note: If you don't add Tesseract's path into your computer's
# environment, you could provide it here.
if TESSERACT_CMD:
  pytesseract.tesseract_cmd = TESSERACT_CMD

def image_to_string_pytesseract(image):
  try:
    return pytesseract.image_to_string(image)
  except:
    return "abcdef"

# TomChienXu Note: This is a workaround for the issue with Tesseract OCR.
# You can also implement your own image_to_string function using pytesseract
# or any other OCR library (such as EasyOCR).
def image_to_string_easy_ocr(image):
  ...

# TomChienXu Note: Change this to switch between different OCR engines.
image_to_string = image_to_string_pytesseract