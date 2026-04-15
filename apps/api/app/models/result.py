import uuid
from datetime import datetime
from enum import Enum

from app.core.database import Base

from sqlalchemy import Boolean, ForeignKey, UniqueConstraint, SmallInteger, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.api.app.models.driver import DriverSeason
from apps.api.app.models.race import RaceSession
from apps.api.app.models.user import User

class ResultScore(str, Enum): 
    openf1 = "openf1"
    manual = "manual"

class RaceResult(Base):
    __tablename__ = "race_results"

    __table_args__ = (
        UniqueConstraint("session_id", "position", name="uq_result_session_position"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id"))
    driver_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("drivers.id"))
    position: Mapped[int] = mapped_column(SmallInteger)
    dnf: Mapped[bool] = mapped_column(Boolean, default=False)
    source: Mapped[ResultScore] = mapped_column(default=ResultScore.openf1)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    session: Mapped["RaceSession"] = relationship("RaceSession", back_populates="results")
    driver_season: Mapped["DriverSeason"] = relationship("DriverSeason", back_populates="race_results")
    

class SeasonScore(Base):
    __tablename__ = "season_scores"
    __table_args__ = (
        UniqueConstraint("user_id", "season", name="uq_season_score"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    season: Mapped[int] = mapped_column(SmallInteger)
    total_score: Mapped[int] = mapped_column(default=0)

    user: Mapped["User"] = relationship("User", back_populates="season_scores")