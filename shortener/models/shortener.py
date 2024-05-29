from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, UniqueConstraint, Index, func
from sqlalchemy.orm import relationship
from core.database import Base


class ShortenerURL(Base):
    __tablename__ = "shortener_url"
    __table_args__ = (
        UniqueConstraint("short_url", "user_id", name="unique_short_url_user_id"),
        Index("index_short_url_user_id", "short_url", "user_id")
    )

    id = Column(Integer, primary_key=True, index=True)
    short_url = Column(String(5), nullable=False, index=True)
    original_url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    user = relationship("User")
