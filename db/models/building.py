from sqlalchemy import Column, Float, Integer, String

from db.base import Base


class Building(Base):
    """Represents a building with address and coordinates."""
    __tablename__ = "buildings"

    id: int = Column(Integer, primary_key=True, index=True)
    address: str = Column(String, nullable=False)
    latitude: float = Column(Float, nullable=False)
    longitude: float = Column(Float, nullable=False)
