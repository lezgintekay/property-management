from pathlib import Path

import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# SAYFA AYARLARI
# ---------------------------------------------------------

st.set_page_config(
    page_title="Emlak Portföy Analizörü",
    page_icon="🏠",
    layout="wide",
)


# ---------------------------------------------------------
# VERİYİ YÜKLE
# ---------------------------------------------------------

DATA_FILE = Path("data/emlak_portfoyleri.csv")


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)

    df["ilan_tarihi"] = pd.to_datetime(df["ilan_tarihi"])
    df["son_fiyat_guncelleme"] = pd.to_datetime(
        df["son_fiyat_guncelleme"]
    )

    return df


df = load_data()


# ---------------------------------------------------------
# BAŞLIK
# ---------------------------------------------------------

st.title("🏠 Emlak Portföy Analizörü")

st.markdown(
    """
    Portföylerinizi analiz edin, uzun süredir bekleyen
    ilanları ve fiyat değişimlerini kolayca takip edin.
    """
)


# ---------------------------------------------------------
# SIDEBAR FİLTRELER
# ---------------------------------------------------------

st.sidebar.header("🔎 Filtreler")

ilan_turu_options = ["Tümü"] + sorted(
    df["ilan_turu"].unique().tolist()
)

selected_ilan_turu = st.sidebar.selectbox(
    "İlan Türü",
    ilan_turu_options,
)

portfoy_options = ["Tümü"] + sorted(
    df["portfoy_tipi"].unique().tolist()
)

selected_portfoy = st.sidebar.selectbox(
    "Portföy Tipi",
    portfoy_options,
)

mahalle_options = ["Tümü"] + sorted(
    df["mahalle"].unique().tolist()
)

selected_mahalle = st.sidebar.selectbox(
    "Mahalle",
    mahalle_options,
)


# ---------------------------------------------------------
# FİLTRELEME
# ---------------------------------------------------------

filtered_df = df.copy()

if selected_ilan_turu != "Tümü":
    filtered_df = filtered_df[
        filtered_df["ilan_turu"] == selected_ilan_turu
    ]

if selected_portfoy != "Tümü":
    filtered_df = filtered_df[
        filtered_df["portfoy_tipi"] == selected_portfoy
    ]

if selected_mahalle != "Tümü":
    filtered_df = filtered_df[
        filtered_df["mahalle"] == selected_mahalle
    ]


# ---------------------------------------------------------
# KPI HESAPLARI
# ---------------------------------------------------------

total_listings = len(filtered_df)

sale_count = len(
    filtered_df[
        filtered_df["ilan_turu"] == "Satılık"
    ]
)

rent_count = len(
    filtered_df[
        filtered_df["ilan_turu"] == "Kiralık"
    ]
)

old_listing_count = len(
    filtered_df[
        filtered_df["ilan_yasi_gun"] >= 60
    ]
)

price_drop_count = len(
    filtered_df[
        filtered_df["fiyat_degisimi_yuzde"] < 0
    ]
)


# ---------------------------------------------------------
# KPI KARTLARI
# ---------------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Toplam Portföy",
    f"{total_listings:,}",
)

col2.metric(
    "Satılık",
    f"{sale_count:,}",
)

col3.metric(
    "Kiralık",
    f"{rent_count:,}",
)

col4.metric(
    "60+ Günlük",
    f"{old_listing_count:,}",
)

col5.metric(
    "Fiyatı Düşen",
    f"{price_drop_count:,}",
)


st.divider()


# ---------------------------------------------------------
# MAHALLE ANALİZİ
# ---------------------------------------------------------

st.subheader("📊 Mahalle Bazlı Analiz")

sale_df = filtered_df[
    filtered_df["ilan_turu"] == "Satılık"
].copy()

if not sale_df.empty:

    neighborhood_analysis = (
        sale_df
        .groupby("mahalle")
        .agg(
            ortalama_fiyat_m2=("fiyat_m2", "mean"),
            portfoy_sayisi=("ilan_id", "count"),
        )
        .reset_index()
        .sort_values(
            "ortalama_fiyat_m2",
            ascending=False,
        )
    )

    neighborhood_analysis[
        "ortalama_fiyat_m2"
    ] = neighborhood_analysis[
        "ortalama_fiyat_m2"
    ].round(0)

    st.bar_chart(
        neighborhood_analysis.set_index("mahalle")[
            "ortalama_fiyat_m2"
        ]
    )

else:
    st.info("Mahalle analizi için satılık portföy bulunamadı.")


# ---------------------------------------------------------
# İKİ SÜTUNLU ANALİZ
# ---------------------------------------------------------

left_col, right_col = st.columns(2)


# ---------------------------------------------------------
# ÖNCELİKLİ PORTFÖYLER
# ---------------------------------------------------------

with left_col:

    st.subheader("🔥 Öncelikli Portföyler")

    priority_df = (
        filtered_df
        .sort_values(
            "portfoy_oncelik_skoru",
            ascending=False,
        )
        .head(10)
        .copy()
    )

    priority_display = priority_df[
        [
            "ilan_id",
            "mahalle",
            "ilan_turu",
            "fiyat",
            "ilan_yasi_gun",
            "portfoy_oncelik_skoru",
        ]
    ].copy()

    priority_display["fiyat"] = (
        priority_display["fiyat"]
        .map(lambda x: f"{x:,.0f} TL")
    )

    priority_display["portfoy_oncelik_skoru"] = (
        priority_display["portfoy_oncelik_skoru"]
        .map(lambda x: f"{x:.1f}")
    )

    st.dataframe(
        priority_display,
        hide_index=True,
        width="stretch",
    )


# ---------------------------------------------------------
# ESKİ İLANLAR
# ---------------------------------------------------------

with right_col:

    st.subheader("⏳ Uzun Süredir Bekleyenler")

    old_df = (
        filtered_df[
            filtered_df["ilan_yasi_gun"] >= 60
        ]
        .sort_values(
            "ilan_yasi_gun",
            ascending=False,
        )
        .head(10)
        .copy()
    )

    old_display = old_df[
        [
            "ilan_id",
            "mahalle",
            "ilan_turu",
            "fiyat",
            "ilan_yasi_gun",
        ]
    ].copy()

    old_display["fiyat"] = (
        old_display["fiyat"]
        .map(lambda x: f"{x:,.0f} TL")
    )

    st.dataframe(
        old_display,
        hide_index=True,
        width="stretch",
    )


st.divider()


# ---------------------------------------------------------
# FİYATI DÜŞEN PORTFÖYLER
# ---------------------------------------------------------

st.subheader("📉 Fiyatı Değişen Portföyler")

price_changed = (
    filtered_df[
        filtered_df["fiyat_degisimi_yuzde"] != 0
    ]
    .sort_values(
        "fiyat_degisimi_yuzde"
    )
    .head(15)
    .copy()
)

if not price_changed.empty:

    price_display = price_changed[
        [
            "ilan_id",
            "mahalle",
            "ilan_turu",
            "fiyat",
            "onceki_fiyat",
            "fiyat_degisimi_yuzde",
        ]
    ].copy()

    price_display["fiyat"] = (
        price_display["fiyat"]
        .map(lambda x: f"{x:,.0f} TL")
    )

    price_display["onceki_fiyat"] = (
        price_display["onceki_fiyat"]
        .map(lambda x: f"{x:,.0f} TL")
    )

    price_display["fiyat_degisimi_yuzde"] = (
        price_display["fiyat_degisimi_yuzde"]
        .map(lambda x: f"{x:+.2f}%")
    )

    st.dataframe(
        price_display,
        hide_index=True,
        width="stretch",
    )

else:
    st.info("Filtrelere uygun fiyat değişikliği bulunamadı.")


# ---------------------------------------------------------
# TÜM PORTFÖYLER
# ---------------------------------------------------------

with st.expander("📋 Tüm Filtrelenmiş Portföyleri Gör"):

    st.dataframe(
        filtered_df,
        hide_index=True,
        width="stretch",
    )