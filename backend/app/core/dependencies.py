from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.authorization import has_permission
from app.core.security import InvalidTokenError, decode_access_token

bearer_scheme = HTTPBearer(auto_error=True)


@dataclass
class AuthContext:
    email: str
    company_id: str
    role: str


def get_auth_context(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> AuthContext:
    try:
        payload = decode_access_token(credentials.credentials)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    return AuthContext(email=payload["sub"], company_id=payload["company_id"], role=payload["role"])


def require_permission(resource: str, action: str):
    def dependency(auth: AuthContext = Depends(get_auth_context)) -> AuthContext:
        if not has_permission(auth.role, resource, action):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return auth

    return dependency


def require_permissions(action: str):
    """Backward-compatible alias retained for branches still using old dependency names.

    Defaults to the `system` resource to simplify conflict resolution when merging
    branches that still import `require_permissions("read"|"write")`.
    """

    return require_permission("system", action)
