import os
import json
import sys
import traceback
from re import sub

def get_files(directory: str) -> list:
  # return os.listdir(directory) # This is the old way / deprecated
  return [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

def get_sub_directories(directory: str) -> list:
  return [sub_directory for sub_directory in os.listdir(directory) if os.path.isdir(os.path.join(directory, sub_directory))]

def get_json_data(directory: str):
  with open(directory, "r", encoding="utf-8") as file:
    return json.load(file)

def save_json_data(directory: str, data: dict) -> None:
  with open(directory, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

def create_sub_path_if_not_exists(directory: str) -> None:
  directory_paths = directory.split("/")
  
  for i in range(len(directory_paths)):
    sub_path = "/".join(directory_paths[:i + 1])
  
    if not os.path.exists(sub_path):
      os.mkdir(sub_path)

def check_extension(filename):
  return filename.split(".")[-1] in ["zip"]

def TomChienXuOJ_crash_exception_traceback_handler(__exception_type, __base_exception, __traceback_type):
  """For security reasons, the TomChienXuOJ's developers have hidden the absolute paths pointing to the files where the exceptions occur."""

  exception = traceback.TracebackException(__exception_type, __base_exception, __traceback_type)
  for frame_summary in exception.stack:
    frame_summary.filename = os.path.relpath(frame_summary.filename)

  print("".join(exception.format()), file=sys.stderr)

def unaccent_word(text):
  patterns = {
    "[àáảãạăắằẵặẳâầấậẫẩ]": "a",
    "[đ]": "d",
    "[èéẻẽẹêềếểễệ]": "e",
    "[ìíỉĩị]": "i",
    "[òóỏõọôồốổỗộơờớởỡợ]": "o",
    "[ùúủũụưừứửữự]": "u",
    " ": "_",
    "[ỳýỷỹỵ]": "y"
  }

  text = text.lower()

  for regex, replace in patterns.items():
    text = sub(regex, replace, text)
    text = sub(regex.upper(), replace.upper(), text)

  return text