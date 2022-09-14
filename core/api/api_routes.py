from core.api.mortgage_api.mortgage_api import *
from core.server.api import calculate


controllers = (
    # ----------------------------------------Calculate deposit--------------------------------------------
    {"path": "/calculate", "endpoint": calculate, "methods": ["POST"]},
    # ----------------------------------------USER---------------------------------------------------------
    # {"path": "/users", "endpoint": create_user, "methods": ["POST"], "response_model": schemas.User},
    # {"path": "/users/", "endpoint": read_users, "methods": ["GET"], "response_model": list[schemas.User]},
    # ----------------------------------------BANK---------------------------------------------------------
    {"path": "/banks", "endpoint": create_bank, "methods": ["POST"], "response_model": schemas.Bank},
    {"path": "/banks", "endpoint": read_banks, "methods": ["GET"], "response_model": list[schemas.Bank]},
    {"path": "/banks/{bank_id}", "endpoint": read_bank, "methods": ["GET"], "response_model": schemas.Bank},
    {"path": "/banks/{bank_id}", "endpoint": patch_bank, "methods": ["PATCH"], "response_model": schemas.Bank},
)

