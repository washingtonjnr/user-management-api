from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from api.infra.db.models.base_model import Base


class UserModel(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    role: Mapped[str] = mapped_column(String, nullable=False)
