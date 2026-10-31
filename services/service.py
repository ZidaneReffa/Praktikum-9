class PrediksiService:
    """Menangani validasi dan aturan prediksi kelulusan."""

    BATAS_IPK_MINIMAL = 3.0
    BATAS_SKS_MINIMAL = 140

    def validasi_data(
        self,
        nama: str,
        ipk: float,
        sks: int
    ) -> str | None:

        if not nama or not nama.strip():
            return "Nama mahasiswa tidak boleh kosong."

        if not 0.0 <= ipk <= 4.0:
            return "IPK harus berada di antara 0,00 sampai 4,00."

        if sks < 0:
            return "Total SKS tidak boleh bernilai negatif."

        return None

    def tentukan_kelulusan(
        self,
        ipk: float,
        sks: int
    ) -> str:

        if (
            ipk >= self.BATAS_IPK_MINIMAL
            and sks >= self.BATAS_SKS_MINIMAL
        ):
            return "Lulus Tepat Waktu"

        return "Tidak Lulus"