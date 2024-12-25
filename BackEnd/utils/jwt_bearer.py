from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from BackEnd.utils.jwt_handler import decode_jwt_token
from BackEnd.models import User
from BackEnd.database.database import Session as SessionLocal
from sqlalchemy.orm import Session


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: Optional[HTTPAuthorizationCredentials] = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = decode_jwt_token(jwtoken)
            print(payload.user_id)
            if payload:
                db: Session = SessionLocal()
                user = db.query(User).filter(User.id == payload.user_id).first()
                if user:
                    isTokenValid = True
        except:
            isTokenValid = False
        return isTokenValid
