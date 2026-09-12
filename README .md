# 🌷 Store Sales Forecasting System

Aplikasi web berbasis Artificial Intelligence (AI) untuk memprediksi penjualan toko secara *dynamic forecasting* menggunakan algoritma **Random Forest (Tuned)**.

---

## 📌 Latar Belakang & Urgensi Bisnis
Prediksi penjualan yang akurat sangat penting untuk manajemen persediaan (*inventory management*) dan perencanaan operasional toko. Proyek ini bertujuan untuk membantu pemilik usaha memprediksi estimasi penjualan di masa depan sehingga dapat mencegah kerugian akibat stok habis (*understocking*) maupun penumpukan barang (*overstocking*).

---

## 🛠️ Metodologi & Fitur
- **Algoritma Utama:** Random Forest Regressor (Tuned)
- **Fitur Temporal:** Tahun, Bulan, Hari, Day of Week, Day of Year, Week of Year.
- **Fitur Historis (Lag & Rolling):** `lag_1`, `lag_7`, `lag_14`, `lag_28`, serta `rolling_mean_7`, `14`, `28`.
- **Pendekatan Forecasting:** *Recursive / Dynamic Forecasting* (prediksi hari sebelumnya digunakan kembali sebagai data input untuk prediksi hari berikutnya).

---

## 🚀 Cara Menjalankan Aplikasi Secara Lokal

1. **Clone Repositori ini:**
   ```bash
   git clone [https://github.com/USERNAME-KAMU/store-sales-forecasting.git](https://github.com/USERNAME-KAMU/store-sales-forecasting.git)
   cd store-sales-forecasting