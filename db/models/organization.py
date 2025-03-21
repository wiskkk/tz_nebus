from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, relationship

from db.base import Base

# Association table for many-to-many relationship
organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey(
        "organizations.id"), primary_key=True),
    Column("activity_id", Integer, ForeignKey(
        "activities.id"), primary_key=True),
)


class Organization(Base):
    """Represents an organization with phones, building, and activities."""
    __tablename__ = "organizations"

    id: int = Column(Integer, primary_key=True, index=True)
    inn: str = Column(String, nullable=False)
    name: str = Column(String, nullable=False)
    phones: str = Column(String, nullable=False)  # Comma-separated numbers
    building_id: int = Column(
        Integer, ForeignKey("buildings.id"), nullable=False)

    building: Mapped["Building"] = relationship("Building")
    activities: Mapped[list["Activity"]] = relationship(
        "Activity", secondary=organization_activity, backref="organizations")
