# Bike Sharing Analytics Dashboard 🚲

Proyek analisis data dan dan dashboard interaktif menggunakan dataset **Bike Sharing** untuk mengevaluasi pola penyewaan sepeda berdasarkan musim, cuaca, jam sibuk hari kerja dan hari libur, serta segmentasi permintaan harian.

## Struktur Direktori
- `Dashboard/` : Berisi kode utama aplikasi Streamlit (`dashboard.py`) beserta dataset bersih (`day_clean.csv` dan `hour_clean.csv`).
- `data/` : Berisi dataset mentah awal (`day.csv` dan `hour.csv`).
- `Proyek_Analisis_Data.ipynb` : Jupyter Notebook yang berisi proses *Data Wrangling*, *Exploratory Data Analysis (EDA)*, dan visualisasi data.
- `requirements.txt` : Daftar dependensi library Python yang dibutuhkan.
- `url.txt` : Tautan publik dashboard yang telah di-*deploy* ke Streamlit Community Claud.

---

## Dependensi Utama ('requirement.txt')

Proyek ini dikembangkan menggunakan **Python 3.13.15** dengan spesifikasi pustaka berikut :

- `streamlit==1.67.0`
- `pandas==3.1.1`
- `matplotlib==3.11.2`
- `seaborn==0.13.2`

---

## Setup Environment - Anaconda

Buka terminal atau Anaconda Prompt pada direktori utama proyek (`submission Proyek Analisis Data`), lalu jalankan perintah berikut :

```bash
conda create --name main-ds python=3.13
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

Pastikan sudah berada di dalam direktori utama proyek (`Submission Proyek Analisis Data`), lalu buat dan aktifkan *virtual environment* :

**macOS / Linux :**
```bash
python3 -m vene venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows :**
```bash
python3 -m vene venv
source venv/Scripts/activate
pip install -r requirements.txt
```

## Run Streamlit App

Setelah seluruh dependensi terinstall dan *environment* aktif, jalankan dashboard dari direktori utama proyek (`Submission Proyek Analisis Data`)

```bash
streamlit run Dashboard/dashboard.py
```