import os
import uvicorn
from core.config import IS_DEBUG, HOST, PORT
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

if __name__ == "__main__":

    app = "core.app:app"

    uvicorn.run(app, host=HOST, port=PORT, log_level=IS_DEBUG and "debug" or "info",
                reload=IS_DEBUG, log_config='./config.ini', use_colors=True, reload_dirs=['app'])
