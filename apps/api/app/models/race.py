import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, SmallInteger, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class WeekendType(str, Enum):
    standard = "standard"
    sprint = "sprint"

class SessionType(str, Enum):
    qualifying = "qualifying"
    sprint_qualifying = "sprint_qualifying"
    sprint = "sprint"
    race = "race"


class SessionStatus(str, Enum):
    upcoming = "upcoming"
    live = "live"
    completed = "completed"

class Race(Base):
    __tablename__ = "races"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    season: Mapped[int] = mapped_column(SmallInteger)
    round: Mapped[int] = mapped_column(SmallInteger)
    name: Mapped[str] = mapped_column(String(100))
    circuit_name: Mapped[str] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(100))
    country_code: Mapped[str] = mapped_column(String(3))
    weekend_type: Mapped[WeekendType] = mapped_column(default=WeekendType.standard)
    openf1_meeting_key: Mapped[str | None] = mapped_column(String(50), nullable=True)

    sessions: Mapped[list["RaceSession"]] = relationship("RaceSession", back_populates="race")
    
    def __repr__(self) -> str:
        return f"<Race {self.name}>"

class RaceSession(Base):
    __tablename__ = "race_sessions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    race_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("races.id"))
    type: Mapped[SessionType]
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[SessionStatus] = mapped_column(default=SessionStatus.upcoming)
    openf1_session_key: Mapped[str | None] = mapped_column(String(50), nullable=True)

    Race: Mapped["Race"] = relationship("Race", back_populates="sessions")
    predictions: Mapped[list["Prediction"]] = relationship("Prediction", back_populates="session")
    results: Mapped[list["RaceResult"]] = relationship("RaceResult", back_populates="session")

    def __repr__(self) -> str:
        return f"<RaceSession {self.type} {self.starts_at}>"

