import uuid

from sqlalchemy import ForeignKey, SmallInteger, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100))
    short_name: Mapped[str] = mapped_column(String(50))
    season: Mapped[int] = mapped_column(SmallInteger)
    color: Mapped[str] = mapped_column(String(7))  # Hex color code

    driver_seasons: Mapped[list["DriverSeason"]] = relationship("DriverSeason", back_populates="team"
                                                                )
    def __repr__(self) -> str:
        return f"<Team {self.name}>"
    
class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    code: Mapped[str] = mapped_column(String(3))
    nationality: Mapped[str] = mapped_column(String(3))

    seasons: Mapped[list["DriverSeason"]] = relationship("DriverSeason", back_populates="driver")
    
    def __repr__(self) -> str:
        return f"<Driver {self.first_name} {self.last_name}>"

class DriverSeason(Base):
    __tablename__ = "driver_seasons"

    __table_args__ = (
        UniqueConstraint("driver_id", "season", name="uq_driver_season"),
        UniqueConstraint("team_id", "number", name="uq_season_number") 
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    driver_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("drivers.id"))
    team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("teams.id"))
    season: Mapped[int] = mapped_column(SmallInteger)
    number: Mapped[int] = mapped_column(SmallInteger)
    is_active: Mapped[bool] = mapped_column(default=True)

    driver: Mapped["Driver"] = relationship("Driver", back_populates="seasons")
    team: Mapped["Team"] = relationship("Team", back_populates="driver_seasons")

    prediction_items: Mapped[list["PredictionItem"]] = relationship("PredictionItem", back_populates="driver_season")
    race_results: Mapped[list["RaceResult"]] = relationship("RaceResult", back_populates="driver_season")

    def __repr__(self) -> str:
        return f"<DriverSeason {self.number} {self.driver.first_name} {self.driver.last_name} - {self.team.name} ({self.season})>"
    