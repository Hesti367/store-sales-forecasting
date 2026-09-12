# 🌷 Store Sales Forecasting System

Aplikasi web berbasis Artificial Intelligence (AI) untuk memprediksi penjualan toko secara *dynamic forecasting* menggunakan algoritma **Random Forest (Tuned)**.

🔗 **Live Demo Application:** [https://NAMA-APP-KAMU.streamlit.app](https://NAMA-APP-KAMU.streamlit.app)

---

## 📌 Latar Belakang & Urgensi Bisnis
Prediksi penjualan yang akurat sangat penting untuk manajemen persediaan (*inventory management*) dan perencanaan operasional toko. Proyek ini bertujuan untuk membantu pemilik usaha memprediksi estimasi penjualan di masa depan sehingga dapat mencegah kerugian akibat stok habis (*understocking*) maupun penumpukan barang (*overstocking*).

---

## 🛠️ Metodologi & Fitur
- **Algoritma Utama:** Random Forest Regressor (Tuned)
- **Fitur Temporal:** Tahun, Bulan, Hari, Day of Week, Day of Year, Week of Year.
- **Fitur Historis (Lag & Rolling):** `lag_1`, `lag_7`, `lag_14`, `lag_28`, serta `rolling_mean_7`, `14`, `28`.
- **Pendekatan Forecasting:** *Recursive / Dynamic Forecasting* (dibatasi hingga horizon 90 hari untuk menjaga stabilitas akurasi dan mencegah akumulasi error).

---

## 📊 Performa & Evaluasi Model
Model dievaluasi menggunakan data uji dan menghasilkan metrik utama sebagai berikut:
- **MAE (Mean Absolute Error):** [Isi angka MAE kamu, misal: 12.5]
- **RMSE (Root Mean Squared Error):** [Isi angka RMSE kamu, misal: 18.2]
- **R² Score:** [Isi angka R2 kamu, misal: 0.89]

---

## 📁 Struktur Repositori
```text
.
├── app.py                 # File utama dashboard Streamlit
├── model.pkl              # File model Machine Learning yang telah dilatih
├── sales_history.csv      # Dataset riwayat penjualan
├── requirements.txt       # Daftar library Python yang dibutuhkan
└── README.md              # Dokumentasi proyek
