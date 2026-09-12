# Store Sales Forecasting

Project ini merupakan implementasi machine learning untuk melakukan forecasting penjualan berdasarkan data historis penjualan. Sistem dikembangkan untuk membantu memperkirakan jumlah penjualan pada tanggal yang akan datang.

Aplikasi dibuat dalam bentuk web sehingga pengguna cukup memilih tanggal target, kemudian sistem akan melakukan prediksi penjualan hingga tanggal tersebut.

## Live Demo

https://store-sales-forecasting-hesti.streamlit.app/

## 1. Latar Belakang

Data penjualan dapat digunakan untuk melihat pola penjualan dari waktu ke waktu dan membantu memperkirakan penjualan pada periode berikutnya.

Pada project ini dilakukan pengolahan data penjualan, eksplorasi data, feature engineering, pemodelan machine learning, evaluasi model, hingga deployment model ke dalam aplikasi web.

Forecasting dilakukan secara bertahap dari hari ke hari. Setiap hasil prediksi digunakan kembali sebagai bagian dari input untuk melakukan prediksi pada hari berikutnya.

## 2. Tujuan

Project ini bertujuan untuk:

* melakukan analisis terhadap data historis penjualan;
* melakukan preprocessing dan penggabungan beberapa sumber data;
* membuat fitur yang dapat digunakan untuk forecasting;
* membandingkan beberapa model machine learning;
* melakukan hyperparameter tuning pada Random Forest;
* membuat sistem forecasting penjualan berdasarkan tanggal target;
* melakukan deployment model dalam bentuk aplikasi web.

## 3. Dataset

Dataset yang digunakan merupakan dataset Store Sales yang terdiri dari beberapa file:

* `train.csv` — data utama penjualan
* `stores.csv` — informasi toko
* `oil.csv` — data harga minyak
* `holidays.csv` — informasi hari libur
* `transactions.csv` — data transaksi

Ukuran data yang digunakan:

| Dataset      | Jumlah Data |
| ------------ | ----------: |
| Train        |   3.000.888 |
| Stores       |          54 |
| Oil          |       1.218 |
| Holidays     |         350 |
| Transactions |      83.488 |

Data kemudian digabungkan berdasarkan informasi tanggal dan store untuk menghasilkan dataset yang digunakan dalam proses modeling.

## 4. Metodologi

Tahapan yang dilakukan dalam project ini adalah:

### 4.1 Data Preprocessing

Tahapan preprocessing meliputi:

* membaca dataset;
* pengecekan missing value;
* pengecekan tipe data;
* konversi kolom tanggal;
* penggabungan beberapa dataset;
* penanganan data yang diperlukan untuk proses forecasting.

### 4.2 Exploratory Data Analysis

EDA dilakukan untuk memahami karakteristik data, antara lain:

* pola penjualan berdasarkan waktu;
* distribusi penjualan;
* hubungan penjualan dengan variabel lain;
* pola harian dan periode tertentu;
* kondisi missing value;
* perkembangan penjualan dari waktu ke waktu.

### 4.3 Feature Engineering

Beberapa fitur dibuat berdasarkan data historis, seperti:

* fitur tanggal;
* fitur hari, bulan, dan tahun;
* lag penjualan;
* rolling mean;
* fitur yang berasal dari data store;
* fitur tambahan dari dataset pendukung.

Lag dan rolling mean digunakan untuk menangkap pola penjualan sebelumnya.

## 5. Model yang Digunakan

Beberapa model diuji dan dibandingkan dalam project ini:

1. Naive Forecasting
2. Linear Regression
3. Ridge Regression
4. Random Forest
5. Random Forest Tuned

### Naive Forecasting

Naive Forecasting digunakan sebagai baseline.

Prediksi dibuat berdasarkan nilai penjualan sebelumnya sehingga dapat digunakan sebagai pembanding awal untuk melihat apakah model machine learning memberikan hasil yang lebih baik.

### Linear Regression

Linear Regression digunakan sebagai model regresi dasar untuk melihat hubungan antara fitur yang digunakan dengan nilai penjualan.

### Ridge Regression

Ridge Regression merupakan pengembangan dari Linear Regression dengan tambahan regularisasi untuk membantu mengurangi pengaruh koefisien yang terlalu besar.

### Random Forest

Random Forest digunakan karena mampu menangani hubungan non-linear antara fitur dan target penjualan.

### Random Forest Tuned

Random Forest kemudian dilakukan hyperparameter tuning untuk mencari kombinasi parameter yang memberikan performa lebih baik.

## 6. Evaluasi Model

Evaluasi dilakukan menggunakan:

* MAE (Mean Absolute Error)
* RMSE (Root Mean Squared Error)
* R² Score

MAE menunjukkan rata-rata selisih absolut antara hasil prediksi dan nilai aktual.

RMSE memberikan penalti lebih besar terhadap kesalahan prediksi yang besar.

R² menunjukkan seberapa besar variasi target yang dapat dijelaskan oleh model.

### Hasil Linear Regression

| Dataset |       MAE |       RMSE |     R² |
| ------- | --------: | ---------: | -----: |
| Test    | 91.968,13 | 156.933,65 | 0,3512 |

### Hasil Ridge Regression

| Dataset |       MAE |       RMSE |     R² |
| ------- | --------: | ---------: | -----: |
| Test    | 90.428,22 | 155.790,07 | 0,3549 |

### Hasil Random Forest Tuned

| Dataset    |       MAE |       RMSE |     R² |
| ---------- | --------: | ---------: | -----: |
| Train      | 23.095,53 |  43.258,98 | 0,9568 |
| Validation | 56.684,67 |  93.714,98 | 0,6983 |
| Test       | 91.562,15 | 148.935,71 | 0,3994 |

Hasil Random Forest Tuned menunjukkan bahwa performa pada data train cukup tinggi, sedangkan performa pada data test lebih rendah. Hal ini menunjukkan adanya perbedaan performa antara data training dan data yang belum pernah dilihat model sehingga perlu diperhatikan dalam interpretasi hasil forecasting.

## 7. Forecasting Dinamis

Sistem menggunakan pendekatan recursive/dynamic forecasting, yaitu model melakukan prediksi secara bertahap dari hari ke hari.

Pengguna memilih tanggal target yang ingin diprediksi. Sistem kemudian menghitung jarak antara tanggal terakhir pada data historis dengan tanggal target tersebut.

Forecasting dibatasi maksimal 90 hari dari tanggal terakhir pada data historis. Batas ini digunakan agar periode prediksi tetap berada pada rentang forecasting yang ditentukan dalam project.

Proses forecasting dilakukan sebagai berikut:

Pengguna memilih tanggal target.
Sistem menghitung jumlah hari yang perlu diprediksi.
Model memprediksi penjualan untuk satu hari.
Hasil prediksi digunakan sebagai bagian dari data historis untuk prediksi berikutnya.
Fitur lag dan rolling mean diperbarui setiap langkah.
Proses diulangi sampai mencapai tanggal target.

Dengan demikian, model tidak langsung memprediksi seluruh periode sekaligus, tetapi memprediksi hari demi hari hingga mencapai tanggal target.

Contohnya, jika tanggal terakhir pada data adalah 31 Desember dan pengguna memilih tanggal target 30 hari setelahnya, maka sistem akan melakukan forecasting selama 30 hari secara bertahap.

Tanggal target yang dipilih tidak boleh lebih dari 90 hari dari tanggal terakhir data yang tersedia.
## 8. Fitur Aplikasi

Aplikasi web menyediakan fitur utama:

* pemilihan tanggal target;
* forecasting penjualan hingga tanggal target;
* prediksi dilakukan secara bertahap per hari;
* menampilkan hasil prediksi;
* visualisasi hasil forecasting;
* informasi periode forecasting.

Pengguna tidak perlu memasukkan store secara manual karena proses forecasting menggunakan data dan fitur yang telah disiapkan oleh sistem.

## 9. Teknologi yang Digunakan

Project ini menggunakan beberapa teknologi berikut:

* Python
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Seaborn
* Streamlit
* Joblib

## 10. Menjalankan Project

### 10.1 Clone Repository

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY
```

### 10.2 Membuat Virtual Environment

Windows:

```bash
python -m venv venv
```

Aktifkan environment:

```bash
venv\Scripts\activate
```

### 10.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 10.4 Menjalankan Aplikasi

Jika file aplikasi bernama `app.py`:

```bash
streamlit run app.py
```

Setelah itu aplikasi dapat dibuka melalui alamat yang diberikan oleh Streamlit.

## 11. Deployment

Aplikasi dideploy menggunakan Streamlit Community Cloud.

File utama yang diperlukan untuk deployment meliputi:

* source code aplikasi;
* model yang sudah dilatih;
* `requirements.txt`;
* dataset atau file pendukung yang diperlukan aplikasi.

Setelah repository terhubung dengan Streamlit, aplikasi dapat dijalankan melalui URL publik.

## 12. Kesimpulan

Project ini menghasilkan sistem forecasting penjualan berbasis machine learning yang dapat digunakan untuk memperkirakan penjualan pada tanggal yang akan datang.

Beberapa model telah dibandingkan, mulai dari Naive Forecasting sebagai baseline hingga Random Forest dengan hyperparameter tuning.

Berdasarkan hasil pengujian yang tersedia, Random Forest Tuned menghasilkan nilai Test RMSE sebesar 148.935,71 dan R² sebesar 0,3994. Sementara itu, Ridge Regression menghasilkan Test MAE sebesar 90.428,22.

Hasil tersebut menunjukkan bahwa model masih memiliki ruang untuk dikembangkan, terutama dalam meningkatkan kemampuan generalisasi terhadap data yang belum pernah dilihat model.

Aplikasi deployment memungkinkan proses forecasting dilakukan dengan lebih sederhana karena pengguna cukup menentukan tanggal target, kemudian sistem melakukan prediksi secara bertahap hingga tanggal tersebut.

## 13. Author

Hesti Sisila Wati

Universitas Sriwijaya
Fakultas Ilmu Komputer
Jurusan Sistem Komputer
