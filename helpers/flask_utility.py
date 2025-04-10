from flask import request
from flask import render_template
from flask import redirect

from settings import USE_RECAPTCHA

default_keyword_arguments = {
  "USE_RECAPTCHA": USE_RECAPTCHA
}

def TomChienXuOJ_render_template(*args, **kwargs):
  return render_template(*args, **default_keyword_arguments, **kwargs)

def TomChienXuOJ_redirect(location, code=302, *args, **kwargs):
  href = request.args.get("next") or location
  return redirect(href, code, *args, **kwargs)