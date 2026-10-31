import os

import pandas as pd
import streamlit as st

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.model import Base
from repositories.repository import MahasiswaRepository
from services.service import PrediksiService


# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="Sistem Prediksi Kelulusan",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==========================================
# 2. CUSTOM CSS
# ==========================================

CUSTOM_CSS = """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #172D55;
    --blue: #2563EB;
    --page: #F5F7FB;
    --border: #E2E8F0;
    --text: #142746;
    --muted: #64748B;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--page);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1440px;
    padding: 1.6rem 2rem 3rem 2rem;
}

/* HEADER */

.hero {
    display: flex;
    align-items: center;
    gap: 24px;
    min-height: 150px;
    padding: 28px 42px;
    margin-bottom: 24px;
    color: white;
    background: linear-gradient(
        110deg,
        #172D55 0%,
        #203D70 100%
    );
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(23,45,85,0.12);
}

.hero-icon {
    flex: 0 0 110px;
    text-align: center;
    font-size: 66px;
    line-height: 1;
}

.hero h1 {
    color: white;
    font-size: clamp(1.8rem, 3vw, 2.65rem);
    font-weight: 800;
    line-height: 1.2;
    margin: 0 0 8px 0;
}

.hero p {
    color: #E8EEF9;
    font-size: 1.08rem;
    margin: 0;
}

/* JUDUL SECTION */

.section-heading {
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--text);
    font-size: 1.45rem;
    font-weight: 750;
    margin: 0 0 18px 0;
}

.section-icon {
    font-size: 1.55rem;
}

/* CARD */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: white;
    border: 1px solid var(--border);
    border-radius: 16px;
    box-shadow: 0 2px 8px rgba(31,55,90,0.035);
}

/* INPUT */

div[data-testid="stTextInput"] label,
div[data-testid="stNumberInput"] label {
    color: var(--text);
    font-weight: 650;
    font-size: 0.98rem;
}

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    min-height: 48px;
    border-radius: 10px;
    border-color: #C9D4E5;
    color: var(--text);
    background: white;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {
    border-color: var(--blue);
    box-shadow: 0 0 0 1px var(--blue);
}

/* BUTTON */

div.stButton > button,
div[data-testid="stFormSubmitButton"] > button {
    min-height: 50px;
    color: white;
    background: linear-gradient(
        90deg,
        #2F75E5,
        #245FC2
    );
    border: 0;
    border-radius: 10px;
    font-size: 1.03rem;
    font-weight: 700;
    transition: all 0.2s ease;
}

div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    color: white;
    background: #174EA6;
    border: 0;
    box-shadow: 0 5px 14px rgba(37,99,235,0.2);
}

/* HASIL PREDIKSI */

.result-box {
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 20px 24px;
    border-radius: 12px;
    border: 1px solid;
}

.result-success {
    color: #087A34;
    background: #E7F7ED;
    border-color: #C5EBD2;
}

.result-fail {
    color: #B42318;
    background: #FFF0EF;
    border-color: #F7CDCA;
}

.result-neutral {
    color: #475569;
    background: #F1F5F9;
    border-color: #E2E8F0;
}

.result-icon {
    flex: 0 0 58px;
    width: 58px;
    height: 58px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    color: white;
    background: #16A34A;
    font-size: 32px;
    font-weight: 800;
}

.result-fail .result-icon {
    background: #DC2626;
}

.result-neutral .result-icon {
    color: #475569;
    background: #E2E8F0;
}

.result-label {
    font-size: 0.9rem;
    font-weight: 750;
    letter-spacing: 0.02em;
    margin-bottom: 4px;
}

.result-status {
    font-size: clamp(1.3rem, 2.5vw, 1.8rem);
    line-height: 1.25;
    font-weight: 800;
    margin-bottom: 4px;
}

.result-description {
    color: #263449;
    font-size: 0.98rem;
}

/* TABEL */

.history-note {
    color: var(--muted);
    font-size: 0.9rem;
    margin-top: 4px;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
}

/* RESPONSIVE */

@media (max-width: 700px) {

    .block-container {
        padding: 1rem 0.8rem 2rem 0.8rem;
    }

    .hero {
        padding: 22px;
        gap: 12px;
    }

    .hero-icon {
        flex-basis: 55px;
        font-size: 42px;
    }

    .hero p {
        font-size: 0.9rem;
    }

}

</style>
"""

st.markdown(
    CUSTOM_CSS,
    unsafe_allow_html=True
)


# ==========================================
# 3. INISIALISASI DATABASE
# ==========================================

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///data_prediksi.db"
)


@st.cache_resource
def inisialisasi_database(database_url: str):

    connect_args = (
        {"check_same_thread": False}
        if database_url.startswith("sqlite")
        else {}
    )

    engine = create_engine(
        database_url,
        connect_args=connect_args
    )

    Base.metadata.create_all(bind=engine)

    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False
    )


SessionLocal = inisialisasi_database(DATABASE_URL)

service = PrediksiService()


# ==========================================
# 4. HEADER APLIKASI
# ==========================================

hero_html = """
<div class="hero">
<div class="hero-icon">🎓</div>
<div>
<h1>Sistem Prediksi Kelulusan</h1>
<p>Masukkan data mahasiswa untuk memprediksi status kelulusan.</p>
</div>
</div>
"""

st.markdown(
    hero_html,
    unsafe_allow_html=True
)


# ==========================================
# 5. FORM INPUT DAN PROSES PREDIKSI
# ==========================================

with SessionLocal() as db_session:

    repository = MahasiswaRepository(db_session)

    with st.container(border=True):

        st.markdown(
            """
            <div class="section-heading">
                <span class="section-icon">📝</span>
                Form Data Mahasiswa
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.form(
            "form_prediksi",
            clear_on_submit=False
        ):

            nama = st.text_input(
                "Nama Mahasiswa",
                placeholder="Masukkan nama mahasiswa",
                max_chars=150
            )

            kolom_ipk, kolom_sks = st.columns(2)

            with kolom_ipk:

                ipk = st.number_input(
                    "IPK (0.0 – 4.0)",
                    min_value=0.0,
                    max_value=4.0,
                    value=0.0,
                    step=0.01,
                    format="%.2f"
                )

            with kolom_sks:

                sks = st.number_input(
                    "Total SKS",
                    min_value=0,
                    max_value=250,
                    value=0,
                    step=1
                )

            tombol_proses = st.form_submit_button(
                "▶  Prediksi & Simpan",
                use_container_width=True,
                type="primary"
            )

    # ======================================
    # 6. PROSES PREDIKSI
    # ======================================

    if tombol_proses:

        pesan_error = service.validasi_data(
            nama,
            ipk,
            sks
        )

        if pesan_error:

            st.session_state.pop(
                "hasil_prediksi",
                None
            )

            st.warning(pesan_error)

        else:

            status = service.tentukan_kelulusan(
                ipk,
                sks
            )

            try:

                repository.simpan_data(
                    nama=nama.strip(),
                    ipk=float(ipk),
                    sks=int(sks),
                    status=status
                )

                st.session_state["hasil_prediksi"] = {
                    "nama": nama.strip(),
                    "ipk": float(ipk),
                    "sks": int(sks),
                    "status": status
                }

                st.success(
                    "Prediksi berhasil dihitung dan data berhasil disimpan."
                )

            except Exception as error:

                st.error(
                    f"Data gagal disimpan ke database: {error}"
                )

   # ==========================================
    # 7. HASIL PREDIKSI
# ==========================================

with st.container(border=True):

    st.markdown(
        """
<div class="section-heading">
<span class="section-icon">📊</span>
Hasil Prediksi
</div>
        """,
        unsafe_allow_html=True
    )

    hasil = st.session_state.get("hasil_prediksi")

    if hasil:

        lulus = hasil["status"] == "Lulus Tepat Waktu"

        kelas_hasil = (
            "result-success" if lulus else "result-fail"
        )

        ikon_hasil = "✓" if lulus else "✕"

        result_html = f"""
<div class="result-box {kelas_hasil}">
<div class="result-icon">{ikon_hasil}</div>
<div>
<div class="result-label">STATUS KELULUSAN</div>
<div class="result-status">{hasil['status']}</div>
<div class="result-description">
Berdasarkan IPK {hasil['ipk']:.2f} dan total SKS {hasil['sks']}.
</div>
</div>
</div>
"""

        st.markdown(
            result_html,
            unsafe_allow_html=True
        )

    else:

        result_html = """
<div class="result-box result-neutral">
<div class="result-icon">ⓘ</div>
<div>
<div class="result-label">STATUS KELULUSAN</div>
<div class="result-status">Belum ada prediksi</div>
<div class="result-description">
Isi form data mahasiswa, lalu tekan tombol Prediksi & Simpan.
</div>
</div>
</div>
"""

        st.markdown(
            result_html,
            unsafe_allow_html=True
        )
    # ======================================
    # 8. RIWAYAT PREDIKSI
    # ======================================

    with st.container(border=True):

        st.markdown(
            """
            <div class="section-heading">
                <span class="section-icon">🕘</span>
                Riwayat Prediksi
            </div>
            """,
            unsafe_allow_html=True
        )

        data_mahasiswa = repository.ambil_semua_data()

        if data_mahasiswa:

            daftar_riwayat = [

                {
                    "No": nomor,
                    "Nama": data.nama,
                    "IPK": f"{data.ipk:.2f}",
                    "SKS": data.sks,
                    "Status": data.status_kelulusan,
                    "Tanggal": data.tanggal_prediksi.strftime(
                        "%d/%m/%Y %H:%M"
                    )
                }

                for nomor, data in enumerate(
                    data_mahasiswa,
                    start=1
                )

            ]

            df_riwayat = pd.DataFrame(
                daftar_riwayat
            )

            st.dataframe(
                df_riwayat,
                use_container_width=True,
                hide_index=True
            )

            st.markdown(
                f"""
                <div class="history-note">
                    Total data tersimpan:
                    {len(data_mahasiswa)} mahasiswa.
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.info(
                "Belum ada riwayat prediksi. "
                "Data akan muncul setelah Anda menyimpan prediksi pertama."
            )