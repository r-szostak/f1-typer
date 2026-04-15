import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(default=UserRole.user)
    is_verified: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime]= mapped_column(DateTime(timezone=True), server_default=func.now())

    predictions: Mapped[list["Prediction"]] = relationship("Prediction", back_populates="user")
    season_scores: Mapped[list["SeasonScore"]] = relationship("SeasonScore", back_populates="user")

    def __repr__(self) -> str:
        return f"<User {self.email}>"
    