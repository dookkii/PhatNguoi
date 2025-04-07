from requests import Session
from requests.cookies import cookiejar_from_dict
from requests.adapters import HTTPAdapter
import ssl

from settings import CUSTOM_SESSION_HEADER


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

  return new_session