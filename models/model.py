from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Mahasiswa(Base):
    """Representasi tabel mahasiswa pada database."""

    __tablename__ = "mahasiswa"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(150), nullable=False)
    ipk = Column(Float, nullable=False)
    sks = Column(Integer, nullable=False)
    status_kelulusan = Column(String(50), nullable=False)
    tanggal_prediksi = Column(
        DateTime,
        default=datetime.now,
        nullable=False
    )