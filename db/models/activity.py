from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Activity(Base):
    """Represents an activity (supports up to 3 levels of nesting)."""
    __tablename__ = "activities"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False)
    parent_id: int | None = Column(
        Integer, ForeignKey("activities.id"), nullable=True)

    parent: Mapped["Activity"] = relationship(
        "Activity", remote_side=[id], backref="children")
