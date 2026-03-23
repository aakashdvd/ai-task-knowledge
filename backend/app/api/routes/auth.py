from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user, get_db, require_admin
from app.core.security import create_access_token, verify_password
from app.models import User
from app.schemas.auth import LoginRequest, TokenResponse, UserOut
from app.services.logging_service import create_activity_log

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    stmt = (
        select(User)
        .options(joinedload(User.role))
        .where(User.email == payload.email)
    )
    user = db.execute(stmt).scalars().first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(subject=str(user.id), role=user.role.name)

    create_activity_log(
        db=db,
        user_id=user.id,
        action="LOGIN",
        entity_type="user",
        entity_id=user.id,
        details={"email": user.email},
    )
    db.commit()

    return TokenResponse(
        access_token=access_token,
        user=user,
    )


@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/admin-check")
def admin_check(_: User = Depends(require_admin)):
    return {"message": "Admin access confirmed"}