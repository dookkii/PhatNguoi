from settings import *
from helpers import *
from pages import app

from pathlib import Path
from dotenv import set_key

def run_application():
  deploy_kwargs = {
    "host": HOST,
    "port": PORT,
    "debug": DEBUG_STATUS,
    "ssl_context": SSL_CONTEXT_TO_USE,
    "use_evalex": USE_EVAL_EXECUTIONS
  }
  
  app.run(**deploy_kwargs)

if __name__ == "__main__":
  env_path = Path(".env")
  try:
    env_path.touch(exist_ok=False)
    set_key(env_path, "SECRET_KEY", "6969696969")
  except FileExistsError:
    pass
  except Exception as error:
    print(error.__traceback__)

  run_application()