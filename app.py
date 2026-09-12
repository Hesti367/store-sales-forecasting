from datetime import datetime, timedelta
import os

import joblib
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="Store Sales Forecasting",
    page_icon="🌷",
    layout="wide"
)


# =========================================================
# FUNGSI FORMAT ANGKA (RUPIAH / INDONESIA FORMAT)
# =========================================================

def format_idr(val):
    """Mengubah format 1,463,084 menjadi 1.463.084 (Titik untuk ribuan)"""
    return f"{val:,.0f}".replace(",", ".")


# =========================================================
# CSS (FIX OVERFLOW, HEADER CUT-OFF & FULL CONTAINER)
# =========================================================

st.markdown(
    """
    <style>

    * { font-family: "Segoe UI", "Inter", sans-serif; }

    /* Fix Background & Streamlit Header agar Menyatu Sempurna */
    .stApp { background-color: #faf9ff; }
    
    header[data-testid="stHeader"] {
        background: transparent !important;
        background-color: transparent !important;
        z-index: 1;
    }
    
    section[data-testid="stSidebar"] { background-color: #f3f0ff; }

    /* Beri jarak padding atas yang pas agar Hero Box TIDAK KEPOTONG */
    div.block-container { 
        padding-top: 3.5rem !important; 
        padding-bottom: 2rem !important; 
        max-width: 95% !important;
    }

    .main-title { font-size: 32px; font-weight: 800; color: #3f3a56; margin-bottom: 4px; }
    .main-subtitle { font-size: 14px; color: #817b91; margin-bottom: 25px; }

    /* ===== HERO BOX (UTUH, BERSIH, LEBIH RAPI) ===== */
    .hero-box {
        background: linear-gradient(135deg, #eee9ff 0%, #f8f3ff 50%, #eaf6ff 100%);
        border: 1.5px solid #cbbdf0;
        border-radius: 20px;
        padding: 28px 32px;
        margin-top: 10px;
        margin-bottom: 26px;
        box-shadow: 0 6px 20px rgba(120, 105, 189, 0.08);
        width: 100%;
        box-sizing: border-box;
    }
    .hero-small { color: #7869bd; font-size: 11px; font-weight: 700; letter-spacing: 1.5px; }
    .hero-title { color: #39334e; font-size: 29px; font-weight: 800; margin-top: 8px; margin-bottom: 6px; }
    .hero-text { color: #777184; font-size: 13.5px; line-height: 1.7; margin-top: 6px; max-width: 700px; }

    /* ===== SECTION HEADER ===== */
    h3 { color: #3f3a56 !important; font-weight: 800 !important; margin-top: 10px !important; }

    /* ===== KPI CARDS ===== */
    .kpi {
        border-radius: 16px;
        padding: 20px 18px;
        min-height: 118px;
        border: 1.5px solid #d4cbf0;
        background-color: white;
        box-shadow: 0 4px 12px rgba(63, 58, 86, 0.05);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .kpi:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(63, 58, 86, 0.1); }

    .kpi-purple { background-color: #f4f1ff; border-color: #d2c8f5; }
    .kpi-blue { background-color: #edf7ff; border-color: #cbe3f7; }
    .kpi-green { background-color: #edf9f2; border-color: #cae8d7; }
    .kpi-orange { background-color: #fff5e9; border-color: #f7dfc5; }

    .kpi-icon {
        font-size: 19px;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 10px;
        border: 1px solid rgba(0,0,0,0.05);
    }
    .kpi-label { color: #837da0; font-size: 10.5px; font-weight: 700; letter-spacing: 0.4px; margin-top: 12px; }
    .kpi-value { color: #37324a; font-size: 22px; font-weight: 800; margin-top: 5px; }

    /* ===== PREDICTION BOX ===== */
    .prediction-box {
        background: linear-gradient(180deg, #ffffff, #fbf9ff);
        border: 1.5px solid #cbbdf0;
        border-radius: 20px;
        padding: 28px;
        min-height: 260px;
        box-shadow: 0 4px 15px rgba(117, 100, 207, 0.06);
    }
    .prediction-label { color: #8f88a3; font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }
    .prediction-date { color: #46405c; font-size: 18px; font-weight: 700; margin-top: 8px; }
    .prediction-value { color: #7564cf; font-size: 44px; font-weight: 800; margin-top: 16px; line-height: 1; }
    .prediction-unit { color: #a29bb3; font-size: 11.5px; margin-top: 4px; }
    .prediction-info {
        color: #776f8c;
        font-size: 11.5px;
        line-height: 1.8;
        margin-top: 22px;
        padding-top: 18px;
        border-top: 1.5px dashed #dfd7f2;
    }

    /* ===== INSIGHT CARDS ===== */
    .insight {
        background-color: white;
        border: 1.5px solid #dcd4f2;
        border-radius: 16px;
        padding: 17px;
        min-height: 112px;
        box-shadow: 0 4px 12px rgba(63, 58, 86, 0.04);
    }
    .insight-title { color: #9a94a6; font-size: 10px; font-weight: 700; letter-spacing: 0.4px; text-transform: uppercase; }
    .insight-value { color: #3d3750; font-size: 19px; font-weight: 800; margin-top: 9px; }
    .insight-text { color: #a39dad; font-size: 10.5px; margin-top: 4px; }

    /* ===== INFO BOX CARA KERJA ===== */
    .how-it-works-card {
        background: linear-gradient(135deg, #f7f4ff 0%, #f0f4ff 50%, #faf8ff 100%);
        border: 1.5px solid #c8bceb;
        border-radius: 20px;
        padding: 24px 28px;
        margin-top: 25px;
        margin-bottom: 25px;
        box-shadow: 0 6px 18px rgba(117, 100, 207, 0.06);
    }
    .how-it-works-header {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 15px;
        font-weight: 800;
        color: #3f3a56;
        margin-bottom: 12px;
    }
    .how-it-works-icon {
        background-color: rgba(255, 255, 255, 0.9);
        color: #7564cf;
        padding: 6px 10px;
        border-radius: 10px;
        font-size: 14px;
        border: 1px solid #d4cbf0;
        box-shadow: 0 2px 6px rgba(117, 100, 207, 0.08);
    }
    .how-it-works-body {
        color: #615a78;
        font-size: 13px;
        line-height: 1.8;
    }
    .date-badge {
        background-color: rgba(255, 255, 255, 0.9);
        color: #6250b4;
        padding: 3px 10px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 12px;
        border: 1px solid #cbbdf0;
    }
    .steps-container {
        display: flex;
        gap: 14px;
        margin-top: 16px;
        flex-wrap: wrap;
    }
    .step-item {
        background-color: rgba(255, 255, 255, 0.85);
        border: 1.5px solid #d8cfede0;
        border-radius: 14px;
        padding: 12px 16px;
        font-size: 12px;
        color: #554e6b;
        flex: 1;
        min-width: 200px;
    }

    /* ===== TABS & TAB CONTENT ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
        padding-bottom: 5px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border: 1.5px solid #d4cbf0 !important;
        border-radius: 14px 14px 0px 0px !important;
        padding: 10px 22px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        color: #79728b !important;
        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f6f3ff !important;
        color: #6250b4 !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7564cf, #6552c4) !important;
        color: #ffffff !important;
        border-color: #6552c4 !important;
        box-shadow: 0 4px 14px rgba(117, 100, 207, 0.25) !important;
    }

    .tab-content-box {
        background: linear-gradient(135deg, #fbf9ff 0%, #f4f6fe 50%, #f9f7ff 100%);
        border: 1.5px solid #cbbdf0;
        border-radius: 0px 20px 20px 20px;
        padding: 26px;
        margin-top: -5px;
        box-shadow: 0 6px 18px rgba(117, 100, 207, 0.05);
    }

    /* STYLING DATAFRAME / TABEL STREAMLIT */
    div[data-testid="stDataFrame"] {
        border: 1.5px solid #d4cbf0;
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(117, 100, 207, 0.03);
        background-color: white;
    }
    
    div[data-testid="stDataFrame"] header {
        background-color: #f2edfe !important;
        color: #4a3e7d !important;
        font-weight: 700 !important;
    }

    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        color: #b5aebe;
        font-size: 10.5px;
        letter-spacing: 0.3px;
        margin-top: 34px;
        margin-bottom: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FEATURE MODEL
# =========================================================

FEATURE_NAMES = [
    "year", "month", "day", "day_of_week", "day_of_year", "week_of_year",
    "lag_1", "lag_7", "lag_14", "lag_28",
    "rolling_mean_7", "rolling_mean_14", "rolling_mean_28"
]


# =========================================================
# LOAD MODEL
# =========================================================

MODEL_FILENAMES = ["model.pkl", "random_forest_final.pkl"]


def find_model_path():
    for name in MODEL_FILENAMES:
        if os.path.exists(name):
            return name
    return None


@st.cache_resource
def load_model():
    path = find_model_path()
    return joblib.load(path)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    df = pd.read_csv("sales_history.csv")

    df.columns = df.columns.str.strip()

    if "date" not in df.columns or "sales" not in df.columns:
        raise ValueError("Kolom 'date' atau 'sales' tidak ditemukan.")

    df["Date"] = pd.to_datetime(df["date"], errors="coerce")
    df["Value"] = pd.to_numeric(df["sales"], errors="coerce")

    df = df.dropna(subset=["Date", "Value"])
    df = df.sort_values("Date").reset_index(drop=True)

    if df.empty:
        raise ValueError("Dataset tidak memiliki data yang valid.")

    return df


# =========================================================
# NAMA HARI & BULAN INDONESIA
# =========================================================

DAYS_ID = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

MONTHS_ID = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]


def format_date_id(date):
    return f"{DAYS_ID[date.weekday()]}, {date.day} {MONTHS_ID[date.month - 1]} {date.year}"


# =========================================================
# DATE FEATURES
# =========================================================

def extract_date_features(date):
    return {
        "year": date.year,
        "month": date.month,
        "day": date.day,
        "day_of_week": date.dayofweek,
        "day_of_year": date.dayofyear,
        "week_of_year": int(date.isocalendar().week)
    }


# =========================================================
# DYNAMIC FORECAST
# =========================================================

def predict_dynamic_until_date(model, history, target_date):
    result = history.copy()
    last_date = result["Date"].max()

    if target_date <= last_date:
        return result

    current_date = last_date + timedelta(days=1)

    while current_date <= target_date:
        values = result["Value"]

        features = extract_date_features(current_date)

        features["lag_1"] = values.iloc[-1]
        features["lag_7"] = values.iloc[-7] if len(values) >= 7 else values.iloc[-1]
        features["lag_14"] = values.iloc[-14] if len(values) >= 14 else values.iloc[-1]
        features["lag_28"] = values.iloc[-28] if len(values) >= 28 else values.iloc[-1]

        features["rolling_mean_7"] = values.iloc[-7:].mean() if len(values) >= 7 else values.mean()
        features["rolling_mean_14"] = values.iloc[-14:].mean() if len(values) >= 14 else values.mean()
        features["rolling_mean_28"] = values.iloc[-28:].mean() if len(values) >= 28 else values.mean()

        X = pd.DataFrame([features])[FEATURE_NAMES]

        prediction = model.predict(X)[0]
        prediction = max(0, float(prediction))

        new_data = pd.DataFrame({"Date": [current_date], "Value": [prediction]})
        result = pd.concat([result, new_data], ignore_index=True)

        current_date += timedelta(days=1)

    return result


# =========================================================
# MAIN
# =========================================================

def main():

    if find_model_path() is None or not os.path.exists("sales_history.csv"):
        st.error("❌ File model atau dataset tidak ditemukan.")
        st.stop()

    try:
        model = load_model()
        df = load_data()
    except Exception as error:
        st.error(f"Gagal membaca model atau dataset: {error}")
        st.stop()

    # =====================================================
    # SIDEBAR
    # =====================================================

    with st.sidebar:
        st.markdown(
            """
            <div style="background-color:white; padding:18px; border-radius:18px;
                        border:1.5px solid #d4cbf0; margin-bottom:20px;">
                <div style="font-size:25px; margin-bottom:7px;">🌷</div>
                <div style="font-size:18px; font-weight:800; color:#3f3a56;">Store Sales</div>
                <div style="font-size:11px; color:#8b8596; margin-top:4px;">Intelligent Forecasting</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### 🤖 Model")
        st.success("Random Forest Tuned")

        st.markdown("### 📅 Pilih Tanggal")
        mode = st.radio("Metode", ["Kalender", "Ketik tanggal"])

        last_date = df["Date"].max()
        MAX_HORIZON_DAYS = 90
        max_allowed_date = (last_date + timedelta(days=MAX_HORIZON_DAYS)).date()

        if mode == "Kalender":
            selected_date = st.date_input(
                "Tanggal target",
                value=(last_date + timedelta(days=30)).date(),
                min_value=(last_date + timedelta(days=1)).date(),
                max_value=max_allowed_date
            )
        else:
            date_input = st.text_input(
                "Masukkan tanggal",
                value=(last_date + timedelta(days=30)).strftime("%Y-%m-%d"),
                placeholder="YYYY-MM-DD"
            )

            try:
                selected_date = datetime.strptime(date_input, "%Y-%m-%d").date()
            except ValueError:
                st.warning("Gunakan format YYYY-MM-DD")
                st.stop()

            if selected_date > max_allowed_date:
                st.error(
                    f"⚠️ Horizon terlalu jauh! Tanggal target maksimal "
                    f"adalah {max_allowed_date.strftime('%d-%m-%Y')} ({MAX_HORIZON_DAYS} hari dari data terakhir)."
                )
                st.stop()
            elif selected_date <= last_date.date():
                st.error(f"⚠️ Pilihlah tanggal setelah data terakhir ({last_date.strftime('%d-%m-%Y')}).")
                st.stop()

        target_date = pd.Timestamp(selected_date)

        st.markdown("### 📊 Dataset")
        st.info(
            f"**Jumlah data:** {len(df):,}  \n"
            f"**Data awal:** {df['Date'].min().strftime('%d-%m-%Y')}  \n"
            f"**Data terakhir:** {last_date.strftime('%d-%m-%Y')}"
        )

    # =====================================================
    # FORECAST
    # =====================================================

    forecast_df = predict_dynamic_until_date(model, df, target_date)
    target_data = forecast_df[forecast_df["Date"] == target_date]

    if target_data.empty:
        st.error("Prediksi tidak ditemukan.")
        st.stop()

    prediction = float(target_data["Value"].iloc[0])
    average_sales = float(df["Value"].mean())
    highest_value = float(forecast_df["Value"].max())
    lowest_value = float(forecast_df["Value"].min())
    highest_date = forecast_df.loc[forecast_df["Value"].idxmax(), "Date"]
    lowest_date = forecast_df.loc[forecast_df["Value"].idxmin(), "Date"]

    horizon = (target_date - last_date).days

    deviation = ((prediction - average_sales) / average_sales) * 100 if average_sales != 0 else 0

    # =====================================================
    # HERO
    # =====================================================

    st.markdown(
        """
        <div class="hero-box">
            <div class="hero-small">✦ AI FORECASTING SYSTEM</div>
            <div class="hero-title">Store Sales Forecasting</div>
            <div class="hero-text">
                Dashboard prediksi penjualan menggunakan
                Random Forest Tuned dengan fitur waktu,
                lag historis, dan rolling average.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # KPI OVERVIEW
    # =====================================================

    st.subheader("📌 Forecast Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="kpi kpi-purple">
                <div class="kpi-icon">📅</div>
                <div class="kpi-label">TANGGAL TARGET</div>
                <div class="kpi-value">{target_date.strftime("%d %b %Y")}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi kpi-blue">
                <div class="kpi-icon">📈</div>
                <div class="kpi-label">PREDIKSI PENJUALAN</div>
                <div class="kpi-value">{format_idr(prediction)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi kpi-green">
                <div class="kpi-icon">📊</div>
                <div class="kpi-label">RATA-RATA DATA</div>
                <div class="kpi-value">{format_idr(average_sales)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="kpi kpi-orange">
                <div class="kpi-icon">⏱️</div>
                <div class="kpi-label">HORIZON</div>
                <div class="kpi-value">{horizon} hari</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # =====================================================
    # HASIL PREDIKSI
    # =====================================================

    left, right = st.columns([1.35, 1])

    with left:
        st.markdown(
            f"""
            <div class="prediction-box">
                <div class="prediction-label">Estimasi Penjualan</div>
                <div class="prediction-date">{format_date_id(target_date)}</div>
                <div class="prediction-value">{format_idr(prediction)}</div>
                <div class="prediction-unit">estimasi nilai penjualan</div>
                <div class="prediction-info">
                    Model melakukan <b>dynamic forecasting</b>.
                    Prediksi hari sebelumnya digunakan
                    kembali sebagai input untuk prediksi
                    hari berikutnya hingga mencapai
                    tanggal target.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        row1_col1, row1_col2 = st.columns(2)

        with row1_col1:
            st.markdown(
                f"""
                <div class="insight">
                    <div class="insight-title">Nilai Tertinggi</div>
                    <div class="insight-value">{format_idr(highest_value)}</div>
                    <div class="insight-text">{highest_date.strftime("%d %b %Y")}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with row1_col2:
            st.markdown(
                f"""
                <div class="insight">
                    <div class="insight-title">Nilai Terendah</div>
                    <div class="insight-value">{format_idr(lowest_value)}</div>
                    <div class="insight-text">{lowest_date.strftime("%d %b %Y")}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        row2_col1, row2_col2 = st.columns(2)

        with row2_col1:
            sign = "+" if deviation >= 0 else ""

            st.markdown(
                f"""
                <div class="insight">
                    <div class="insight-title">Deviasi</div>
                    <div class="insight-value">{sign}{deviation:.1f}%</div>
                    <div class="insight-text">dibanding rata-rata data</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with row2_col2:
            st.markdown(
                """
                <div class="insight">
                    <div class="insight-title">Algoritma</div>
                    <div class="insight-value">Random Forest</div>
                    <div class="insight-text">Tuned Model</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    # =====================================================
    # CHART
    # =====================================================

    st.subheader("📈 Sales Forecast Trend")

    historical = forecast_df[forecast_df["Date"] <= last_date]
    future = forecast_df[forecast_df["Date"] > last_date]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=historical["Date"],
            y=historical["Value"],
            mode="lines",
            name="Data",
            line=dict(color="#8b7cf6", width=3)
        )
    )

    if not future.empty:
        fig.add_trace(
            go.Scatter(
                x=future["Date"],
                y=future["Value"],
                mode="lines",
                name="Forecast",
                line=dict(color="#69aee8", width=3, dash="dash")
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[target_date],
            y=[prediction],
            mode="markers",
            name="Target",
            marker=dict(size=12, color="#ef8299")
        )
    )

    fig.add_hline(
        y=average_sales,
        line_dash="dot",
        line_color="#75b99a",
        annotation_text="Rata-rata"
    )

    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=25, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        hovermode="x unified",
        xaxis=dict(title="Tanggal", showgrid=False),
        yaxis=dict(title="Penjualan", gridcolor="#f0edf5"),
        legend=dict(orientation="h", y=1.08, x=0)
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # =====================================================
    # INFO BOX: CARA KERJA FORECASTING
    # =====================================================

    start_date_str = last_date.strftime("%d-%m-%Y")
    target_date_str = target_date.strftime("%d-%m-%Y")

    st.markdown(
        f"""
        <div class="how-it-works-card">
            <div class="how-it-works-header">
                <span class="how-it-works-icon">💡</span>
                <span>Cara Kerja Forecasting</span>
            </div>
            <div class="how-it-works-body">
                Sistem memulai prediksi dari data terakhir yaitu 
                <span class="date-badge">📅 {start_date_str}</span>. 
                Model kemudian menghasilkan prediksi untuk hari berikutnya. 
                Nilai tersebut digunakan kembali sebagai data input (secara <i>recursive/dynamic</i>) 
                untuk memprediksi hari selanjutnya hingga mencapai tanggal target 
                <span class="date-badge">🎯 {target_date_str}</span>.
            </div>
            <div class="steps-container">
                <div class="step-item">
                    <b>1. Data Terakhir</b><br>
                    Mengambil lag & rolling mean dari <b>{start_date_str}</b>
                </div>
                <div class="step-item">
                    <b>2. Dynamic Iteration</b><br>
                    Prediksi t+1 dimasukkan kembali sebagai fitur t+2
                </div>
                <div class="step-item">
                    <b>3. Target Final</b><br>
                    Hasil akhir diperoleh pada <b>{target_date_str}</b>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # TABS: DETAIL & MODEL FEATURES
    # =====================================================

    tab1, tab2 = st.tabs(["📋 Detail Forecast", "🧠 Model & Features"])

    with tab1:
        st.markdown(
            """
            <div class="tab-content-box">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                    <span style="font-size:18px;">📊</span>
                    <span style="font-size:16px; font-weight:800; color:#3f3a56;">Detail Hasil Prediksi Harian</span>
                </div>
                <div style="font-size:12px; color:#857e95; margin-bottom:18px;">
                    Menampilkan rincian hasil prediksi harian dari awal periode forecast hingga tanggal target.
                </div>
            """,
            unsafe_allow_html=True
        )

        detail = forecast_df.copy()
        detail = detail[(detail["Date"] > last_date) & (detail["Date"] <= target_date)]

        detail["Tanggal"] = detail["Date"].dt.strftime("%d-%m-%Y")
        detail["Penjualan (Forecast)"] = detail["Value"].apply(format_idr)

        detail = detail[["Tanggal", "Penjualan (Forecast)"]]

        st.dataframe(detail, use_container_width=True, hide_index=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown(
            """
            <div class="tab-content-box">
            """,
            unsafe_allow_html=True
        )
        
        col_m1, col_m2 = st.columns(2)

        with col_m1:
            st.markdown(
                """
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                    <span style="font-size:17px;">🤖</span>
                    <span style="font-size:15px; font-weight:800; color:#3f3a56;">Konfigurasi Model</span>
                </div>
                <div style="font-size:12px; color:#857e95; margin-bottom:14px;">
                    Parameter terbaik Random Forest Tuned.
                </div>
                """,
                unsafe_allow_html=True
            )
            
            model_info = pd.DataFrame({
                "Parameter": [
                    "n_estimators", "max_depth", "min_samples_leaf",
                    "min_samples_split", "random_state"
                ],
                "Nilai Parameter": [200, 10, 2, 5, 42]
            })

            st.dataframe(model_info, use_container_width=True, hide_index=True)

        with col_m2:
            st.markdown(
                """
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                    <span style="font-size:17px;">⚙️</span>
                    <span style="font-size:15px; font-weight:800; color:#3f3a56;">Fitur Model (Features)</span>
                </div>
                <div style="font-size:12px; color:#857e95; margin-bottom:14px;">
                    Fitur temporal, lag, dan rolling average.
                </div>
                """,
                unsafe_allow_html=True
            )

            feature_df = pd.DataFrame({
                "Kelompok Fitur": [
                    "Kalender", "Kalender", "Kalender", "Kalender", "Kalender", "Kalender",
                    "Lag Historis", "Lag Historis", "Lag Historis", "Lag Historis",
                    "Rolling Average", "Rolling Average", "Rolling Average"
                ],
                "Nama Fitur": FEATURE_NAMES
            })

            st.dataframe(feature_df, use_container_width=True, hide_index=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown(
        """
        <div class="footer">
            Store Sales Forecasting Dashboard
            · Streamlit
            · Random Forest Tuned
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":
    main()