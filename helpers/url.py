from urllib.parse import urlparse
from urllib.parse import urlunparse

def clean_google_avatar_image_url(url):
  parsed = urlparse(url)
  clean_path = parsed.path.split("=")[0]
  clean_url = urlunparse(parsed._replace(path=clean_path, query="", fragment=""))

  return clean_url