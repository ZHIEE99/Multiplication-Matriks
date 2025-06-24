# --- SELURUH KODE DALAM SATU BLOK UNTUK GOOGLE COLAB ---

# 1. Instalasi Library yang Dibutuhkan
# Menginstal Streamlit, NumPy, dan pyngrok. `--quiet` untuk output yang lebih bersih.
!pip install streamlit numpy pyngrok --quiet

# 2. Menulis Kode Aplikasi Streamlit ke dalam File
# Baris '%%writefile' adalah magic command Colab yang menyimpan kode di bawahnya
# ke dalam file bernama 'matrix_calculator_app.py'.
# Pastikan nama file ini konsisten dengan yang digunakan di langkah 4.
%%writefile matrix_calculator_app.py
import streamlit as st
import numpy as np

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(
    page_title="Kalkulator Perkalian Matriks Cantik",
    layout="wide", # Menggunakan layout 'wide' agar lebih luas
    initial_sidebar_state="expanded", # Sidebar terlihat saat aplikasi pertama kali dibuka
    menu_items={
        'About': "Kalkulator perkalian matriks interaktif dan menarik dengan tampilan yang dipercantik.",
        'Report a bug': "Silakan laporkan bug melalui GitHub issues atau forum Streamlit.",
        'Get help': "Kunjungi dokumentasi Streamlit atau forum untuk bantuan lebih lanjut.",
    }
)

# --- Gaya CSS Kustom untuk Mempercantik Tampilan ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f4f4f4; /* Latar belakang aplikasi */
    }
    .st-header {
        background-color: #e1f5fe; /* Warna latar belakang header */
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Efek bayangan */
    }
    .st-subheader {
        color: #1e88e5; /* Warna subheader */
        margin-top: 1rem;
        font-weight: bold;
    }
    .matrix-input-container {
        border: 1px solid #dcdcdc; /* Border untuk kotak input matriks */
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        background-color: #ffffff; /* Latar belakang input matriks */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .result-container {
        background-color: #e8f5e9; /* Latar belakang container hasil */
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 2rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .calculate-button {
        background-color: #4caf50; /* Warna tombol hitung */
        color: white;
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1.1rem;
        margin-top: 1.5rem;
        transition: background-color 0.3s ease;
    }
    .calculate-button:hover {
        background-color: #43a047; /* Warna tombol saat di-hover */
    }
    .error-message {
        color: #f44336; /* Warna teks error */
        padding: 0.75rem;
        background-color: #ffebee; /* Latar belakang error */
        border-radius: 3px;
        margin-top: 1rem;
        border: 1px solid #ef9a9a;
    }
    .success-message {
        color: #2e7d32; /* Warna teks sukses */
        padding: 0.75rem;
        background-color: #e8f5e9; /* Latar belakang sukses */
        border-radius: 3px;
        margin-top: 1rem;
        border: 1px solid #a5d6a7;
    }
    .stNumberInput > div > div > input {
        text-align: center !important; /* Agar input angka di tengah */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Fungsi Perkalian Matriks ---
def multiply_matrices(matrix_a, matrix_b):
    """Mengalikan dua matriks menggunakan NumPy."""
    try:
        result = np.dot(matrix_a, matrix_b)
        return result
    except ValueError as e:
        # Menangani error jika dimensi matriks tidak cocok
        st.error(f"<div class='error-message'>Error dalam perkalian matriks: {e}. Pastikan dimensi sesuai.</div>", unsafe_allow_html=True)
        return None

# --- Fungsi untuk Mendapatkan Input Matriks dari Pengguna ---
def get_matrix_input(label, key_prefix):
    """
    Mendapatkan input matriks dari pengguna dengan tampilan yang lebih baik.
    Memungkinkan pengguna menentukan jumlah baris dan kolom secara dinamis.
    """
    st.markdown(f"<div class='matrix-input-container'>", unsafe_allow_html=True)
    st.subheader(f"✨ {label} ✨")

    # Input untuk dimensi matriks (baris dan kolom)
    cols_dim = st.columns(2)
    rows = cols_dim[-2].number_input(f"Jumlah Baris {label}", min_value=1, value=2, step=1, key=f"rows_{key_prefix}", help=f"Tentukan jumlah baris untuk {label}")
    cols = cols_dim[-1].number_input(f"Jumlah Kolom {label}", min_value=1, value=2, step=1, key=f"cols_{key_prefix}", help=f"Tentukan jumlah kolom untuk {label}")

    matrix = []
    st.write(f"Masukkan elemen untuk {label} (Baris {int(rows)} x Kolom {int(cols)}):")

    # Input elemen matriks menggunakan kolom Streamlit
    for r in range(int(rows)):
        cols_input = st.columns(int(cols)) # Membuat kolom sebanyak jumlah kolom matriks
        row_values = []
        for c in range(int(cols)):
            try:
                # Menggunakan label_visibility="collapsed" agar label tidak terlihat dan layout lebih rapi
                value = cols_input[-int(cols) + c].number_input(
                    f"B{r+1}, K{c+1}", # Label internal untuk setiap input
                    key=f"matrix_{key_prefix}_{r}_{c}",
                    value=0.0, # Nilai default
                    step=0.1, # Langkah perubahan nilai
                    label_visibility="collapsed" # Menyembunyikan label
                )
                row_values.append(float(value))
            except ValueError:
                st.warning(f"⚠️ Masukkan angka valid untuk {label} - Baris {r+1}, Kolom {c+1}")
                st.markdown("</div>", unsafe_allow_html=True) # Tutup container jika ada warning
                return None
        matrix.append(row_values)
    st.markdown("</div>", unsafe_allow_html=True) # Tutup container matriks
    return np.array(matrix) if matrix else None

# --- Fungsi untuk Menampilkan Matriks (Tidak digunakan langsung di sini, tapi bisa untuk debugging) ---
def display_matrix(label, matrix):
    """Menampilkan matriks dengan label yang indah menggunakan st.dataframe."""
    st.markdown(f"<h4 style='color: #29b6f6; text-align: center;'>{label}</h4>", unsafe_allow_html=True)
    st.dataframe(matrix) # st.dataframe memberikan tampilan tabel yang rapi

# --- Bagian Utama Aplikasi Streamlit ---

# Judul aplikasi dengan gaya khusus
st.markdown(
    "<div class='st-header'><h1><span style='color:#3f51b5;'>🧮</span> Kalkulator Perkalian Matriks <span style='color:#3f51b5;'>🧮</span></h1></div>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; font-size: 1.1em;'>Masukkan dimensi dan elemen untuk dua matriks di bawah ini, lalu klik 'Hitung'.</p>",
    unsafe_allow_html=True
)
st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True) # Garis pemisah

# Dua kolom untuk input Matriks A dan Matriks B
col_a, col_b = st.columns(2)

with col_a:
    matrix_a_input = get_matrix_input("Matriks A", "A")

with col_b:
    matrix_b_input = get_matrix_input("Matriks B", "B")

st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True) # Garis pemisah

# Tombol untuk menghitung perkalian
if st.button("✨ Hitung Hasil Perkalian ✨", key="calculate_button", type="primary", use_container_width=True):
    if matrix_a_input is not None and matrix_b_input is not None:
        # Mendapatkan dimensi matriks untuk validasi
        # numpy.shape mengembalikan tuple (rows, cols) atau (rows,) untuk 1D array
        # kita perlu memastikan penanganan untuk kasus 1D array atau skalar
        cols_a = matrix_a_input.shape[-1] if matrix_a_input.ndim > 1 else matrix_a_input.size if matrix_a_input.ndim == 1 else 1
        rows_b = matrix_b_input.shape[-2] if matrix_b_input.ndim > 1 else matrix_b_input.size if matrix_b_input.ndim == 1 else 1

        if cols_a != rows_b:
            # Pesan error jika dimensi tidak cocok
            st.error(
                "<div class='error-message'>⚠️ Jumlah **kolom Matriks A** harus sama dengan jumlah **baris Matriks B** untuk melakukan perkalian. Silakan sesuaikan dimensinya.</div>",
                unsafe_allow_html=True
            )
        else:
            # Melakukan perkalian matriks jika valid
            result_matrix = multiply_matrices(matrix_a_input, matrix_b_input)
            if result_matrix is not None:
                # Menampilkan hasil
                st.markdown("<hr style='border: 2px solid #4caf50; border-radius: 5px;'>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='result-container'><h3><span style='color:#2e7d32;'>✅</span> Hasil Perkalian Matriks (A × B) <span style='color:#2e7d32;'>✅</span></h3></div>",
                    unsafe_allow_html=True
                )
                st.dataframe(result_matrix) # Tampilan tabel untuk hasil
                st.balloons() # Efek balon untuk merayakan keberhasilan
    else:
        # Pesan peringatan jika input belum lengkap
        st.warning("🔔 Mohon lengkapi semua input matriks dengan angka sebelum menghitung.")

st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True) # Garis pemisah bawah
st.markdown(
    "<p style='text-align: center; color: #757575; font-size: 0.9em;'>Dibuat dengan ❤️ oleh program Python untuk Streamlit</p>",
    unsafe_allow_html=True
)


# 3. Konfigurasi Ngrok dan Menjalankan Streamlit
# --- PENTING: GANTI 'YOUR_NGROK_AUTHTOKEN' DENGAN TOKEN ASLI ANDA ---
# Anda bisa mendapatkan token dari https://dashboard.ngrok.com/auth/your-authtoken setelah mendaftar.
# Ini hanya perlu dilakukan sekali per sesi Colab atau jika token belum diatur.
# Baris ini dikomentari secara default, HILANGKAN KOMENTAR (#) jika Anda perlu mengaturnya.
# !ngrok config add-authtoken YOUR_NGROK_AUTHTOKEN

# Menjalankan aplikasi Streamlit di background.
# 'matrix_calculator_app.py' harus sesuai dengan nama file yang disimpan di langkah 2.
# '&>/dev/null &' menyembunyikan output Streamlit di Colab dan menjalankannya di latar belakang.
!streamlit run matrix_calculator_app.py &>/dev/null &

# Mengimpor pyngrok dan menghubungkan ke aplikasi Streamlit untuk mendapatkan URL publik.
# Port default Streamlit adalah 8501.
from pyngrok import ngrok
public_url = ngrok.connect(addr="8501", proto="http")
print("Aplikasi Kalkulator Perkalian Matriks Anda bisa diakses di link berikut:")
print(public_url)
