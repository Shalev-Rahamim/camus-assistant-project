"""Admin API module for CRUD operations."""

from api.admin import schemas
from api.admin import crud
from api.admin.routes import router

__all__ = ["schemas", "crud", "router"]
