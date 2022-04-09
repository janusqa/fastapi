import uvicorn
import os
import sys
from fastapi import Depends
import app.config as appconfig


def main():
    settings: appconfig.Settings = appconfig.get_settings()
    app_path = os.path.join(os.path.dirname(sys.argv[0]), "app")
    print(app_path)
    uvicorn.run(
        "app.main:webapp",
        port=settings.api_port,
        reload=settings.api_debug,
        access_log=settings.api_log,
        reload_dirs=[app_path],
    )


if __name__ == "__main__":
    main()
