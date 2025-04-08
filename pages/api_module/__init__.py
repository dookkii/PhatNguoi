from .. import api
from .delayed_fine import PhatNguoi

api.add_resource(PhatNguoi, "/phatnguoi/<bien_so_xe>/<loai_xe>")