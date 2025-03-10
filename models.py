from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class DbMovie(Base):
    __tablename__ = 'movie'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30))
    details: Mapped[str] = mapped_column(String(300))
    image_url: Mapped[str] = mapped_column(String(100))
