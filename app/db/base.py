from sqlmodel import SQLModel

#   Importar todos los modelos aqui para que Alembic los detecte
from app.models.user import User # noqa: F401

__all__ = ["SQLModel"]