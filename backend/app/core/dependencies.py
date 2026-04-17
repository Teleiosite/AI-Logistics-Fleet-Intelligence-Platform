from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import InvalidTokenError, decode_access_token

bearer_scheme = HTTPBearer(auto_error=True)


@dataclass
class AuthContext:
    email: str
    company_id: str
    role: str


ROLE_PERMISSIONS: dict[str, set[str]] = {
    "super_admin": {"*"},
    "company_admin": {"*"},
    "transport_admin": {"read", "write", "approve"},
    "logistics_manager": {"read", "write"},
    "finance_officer": {"read", "write", "approve"},
    "driver": {"read", "write_own"},
    "auditor": {"read"},
}


def get_auth_context(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> AuthContext:
    try:
        payload = decode_access_token(credentials.credentials)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    return AuthContext(email=payload["sub"], company_id=payload["company_id"], role=payload["role"])


def require_permissions(*permissions: str):
    def dependency(auth: AuthContext = Depends(get_auth_context)) -> AuthContext:
        allowed = ROLE_PERMISSIONS.get(auth.role, set())
        if "*" in allowed:
            return auth
        if not set(permissions).issubset(allowed):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return auth

    return dependency
