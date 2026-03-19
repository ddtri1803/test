from __future__ import annotations

from fastapi import Depends, FastAPI, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.security import SecurityError, auth_manager
from app.db.session import SessionLocal
from app.services.auth_service import AuthService

app = FastAPI(title="Secure FTP Manager API")
auth_service = AuthService()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/auth/login")
def login(payload: dict, db: Session = Depends(get_db)):
    try:
        user, token = auth_service.login(db, payload["username"], payload["password"])
        return {"user_id": user.id, "token": token}
    except SecurityError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


@app.get("/auth/verify")
def verify_token(authorization: str = Header(default="")):
    token = authorization.removeprefix("Bearer ")
    try:
        return auth_manager.decode_token(token)
    except SecurityError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
