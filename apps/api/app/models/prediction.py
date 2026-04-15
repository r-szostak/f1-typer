import uuid
from datetime import datetime

from app.core.database import Base

from sqlalchemy import ForeignKey, SmallInteger, UniqueConstraint, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.api.app.models.driver import DriverSeason
from apps.api.app.models.user import User


class Prediction(Base): 
    __tablename__ = "predictions"

    __table__args__ = (
        UniqueConstraint("user_id", "session_id", name="uq_prediction_user_session"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id"))
    score: Mapped[int] = mapped_column(SmallInteger, default=0)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="predictions")
    session: Mapped["RaceSession"] = relationship("RaceSession", back_populates="predictions")
    items: Mapped[list["PredictionItem"]] = relationship("PredictionItem", back_populates="prediction", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Prediction User {self.user_id} - Session {self.session_id}>"
    
class PredictionItem(Base):
    __tablename__ = "prediction_items"

    __table_args__ = (
        UniqueConstraint("prediction_id", "position", name= "uq_item_position"),
        UniqueConstraint("prediction_id", "driver_season_id", name="uq_item_driver")
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    prediction_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("predictions.id"))
    driver_season_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("driver_seasons.id"))
    position: Mapped[int] = mapped_column(SmallInteger)

    prediction: Mapped["Prediction"] = relationship("Prediction", back_populates="items")
    driver_season: Mapped["DriverSeason"] = relationship("DriverSeason", back_populates="prediction_items")
