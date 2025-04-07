default_results = {
  404: dict(
    success=False,
    status=404
  ),
  200: dict(
    success=True,
    status=200
  ),
  408: dict(
    success=False,
    status=408
  )
}

def get_result(code, error=None, **kwargs):
  if code in default_results:
    result = default_results.get(code).copy()
    result["error"] = error
    result["data"] = dict(**kwargs)

    return result
  else:
    return kwargs