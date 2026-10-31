from sqlalchemy.orm import Session

from models.model import Mahasiswa


class MahasiswaRepository:
    """Mengelola penyimpanan dan pengambilan data mahasiswa."""

    def __init__(self, db_session: Session):
        self.db = db_session

    def simpan_data(
        self,
        nama: str,
        ipk: float,
        sks: int,
        status: str,
    ) -> Mahasiswa:

        data_baru = Mahasiswa(
            nama=nama,
            ipk=ipk,
            sks=sks,
            status_kelulusan=status,
        )

        try:
            self.db.add(data_baru)
            self.db.commit()
            self.db.refresh(data_baru)

            return data_baru

        except Exception:
            self.db.rollback()
            raise

    def ambil_semua_data(self) -> list[Mahasiswa]:

        return (
            self.db.query(Mahasiswa)
            .order_by(
                Mahasiswa.tanggal_prediksi.desc(),
                Mahasiswa.id.desc()
            )
            .all()
        )