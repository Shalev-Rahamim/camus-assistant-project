"""Admin API routes - Login and Dashboard only."""

import logging
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from api.admin.auth import (
    authenticate_admin,
    create_access_token,
    verify_admin,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from db.database import get_db
from db.models import AdminUser

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["Admin"])


# ========== Authentication & Dashboard ==========


class LoginRequest(BaseModel):
    """Schema for admin login request."""

    username: str = Field(..., description="Admin username")
    password: str = Field(..., description="Admin password")


class LoginResponse(BaseModel):
    """Schema for admin login response."""

    success: bool
    message: str
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=LoginResponse)
async def admin_login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Admin login endpoint - verifies username/password and returns JWT token."""
    try:
        user = await authenticate_admin(db, credentials.username, credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        return LoginResponse(
            success=True,
            message="Login successful",
            access_token=access_token,
            token_type="bearer",
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login",
        )


@router.get("/dashboard", response_model=Dict[str, Any])
async def admin_dashboard(current_user: AdminUser = Depends(verify_admin)):
    """Admin dashboard endpoint - returns available options for admin panel."""
    return {
        "title": "Admin Dashboard",
        "description": "Campus Elad Software - Admin Panel",
        "options": [],
    }
