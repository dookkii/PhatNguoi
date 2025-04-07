from flask_restful import Resource

from helpers.api_result import get_result
from helpers.custom_thread import TomChienXuOJThread
from handlers.violation import safely_get_violations

from .. import api

class API_Violation(Resource):
  def get(self, bien_so_xe, loai_xe):
    thread = TomChienXuOJThread(target=safely_get_violations, args=(bien_so_xe, loai_xe))
    thread.start()
    result = thread.join(timeout=10)

    if thread.is_alive():
      thread.join()

    # TomChienXu Note: Timeout
    if result is None:
      return get_result(408, "Timed out. (Network error, connection issue, or CSGT.vn is down/inaccessible)")

    # TomChienXu Note: Max Captcha Attempts reached
    if result.get("violations") is None:
      return get_result(408, "Max Captcha attempts reached.", **result)
    else:
      return get_result(200, **result)

api.add_resource(API_Violation, "/phatnguoi/<bien_so_xe>/<loai_xe>", endpoint="api.phatnguoi", subdomain="api")