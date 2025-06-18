from flask import request
from flask import render_template
from flask import redirect
from flask_login import current_user

from settings import USE_RECAPTCHA

default_keyword_arguments = {
  "USE_RECAPTCHA": USE_RECAPTCHA,
  "current_user": current_user,
}

def TomChienXuOJ_render_template(*args, **kwargs):
  return render_template(*args, **default_keyword_arguments, **kwargs)

def TomChienXuOJ_redirect(location, code=302, *args, **kwargs):
  href = request.args.get("next") or location
  return redirect(href, code, *args, **kwargs)

def get_request_public_ip():
  x_real_ip = request.headers.get("X-Real-IP")
  
  if x_real_ip:
    return x_real_ip.strip()
  else:
    x_forwarded_for_ips = request.headers.get("X-Forwarded-For").split(",")
    n = len(x_forwarded_for_ips)
    
    if n >= 2:
      return x_forwarded_for_ips[1].strip()
    elif n == 1:
      return x_forwarded_for_ips[0].strip()
    else:
      return request.remote_addr.strip()