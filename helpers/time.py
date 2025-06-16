from arrow import get

from settings import TIMEZONE

def datetime_to_arrow(datetime):
  return get(datetime).floor("second").to(TIMEZONE)