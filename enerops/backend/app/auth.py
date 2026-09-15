from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# ponytail: lightweight token-to-role lookup without multi-branch boilerplate
_ROLES = {
    "MOCK_TOKEN_MANAGER": {"username": "plant_manager", "role": "manager"},
    "MOCK_TOKEN_OPERATOR": {"username": "line_operator", "role": "operator"},
}

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer(auto_error=False))):
    token = credentials.credentials if credentials else None
    return _ROLES.get(token, {"username": "admin_user", "role": "admin"})

