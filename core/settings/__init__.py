import os

from decouple import config

from .base import BASE_DIR


ENVIRONMENT = config("ENVIRONMENT", "dev")

if ENVIRONMENT == "dev":
    from .development import *  # noqa
elif ENVIRONMENT == "prod":
    from .production import *  # noqa
elif ENVIRONMENT == "stage":
    from .base import *  # noqa
else:
    raise ValueError("Invalid environment specified.")
