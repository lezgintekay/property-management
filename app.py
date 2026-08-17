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
# VERİ YÜKLEME
# ---------------------------------------------------------

DATA_FILE = Path("data/emlak_portfoyleri.csv")


REQUIRED_COLUMNS = [
    "ilan_id",
    "portfoy_tipi",
    "ilan_turu",
    "mahalle",
    "oda_sayisi",
    "metrekare",
    "fiyat",
    "onceki_fiyat",
    "ilan_tarihi",
    "son_fiyat_guncelleme",
    "durum",
    "fiyat_m2",
    "ilan_yasi_gun",
    "fiyat_degisimi_yuzde",
    "portfoy_oncelik_skoru",
]


@st.cache_data
def load_data(file):
    df = pd.read_csv(file)

    return prepare_data(df)


def prepare_data(df):
    df = df.copy()

    # Tarih alanları
    df["ilan_tarihi"] = pd.to_datetime(
        df["ilan_tarihi"],
        errors="coerce",
    )

    df["son_fiyat_guncelleme"] = pd.to_datetime(
        df["son_fiyat_guncelleme"],
        errors="coerce",
    )

    # Sayısal alanlar
    numeric_columns = [
        "metrekare",
        "fiyat",
        "onceki_fiyat",
        "fiyat_m2",
        "ilan_yasi_gun",
        "fiyat_degisimi_yuzde",
        "portfoy_oncelik_skoru",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    return df


def validate_data(df):
    def get_priority_level(score):
        if score >= 70:
            return "🔴 Yüksek Öncelik"

    if score >= 40:
        return "🟡 Orta Öncelik"

    return "🟢 Düşük Öncelik"


def validate_data(df):
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    return missing_columns


def get_action_recommendation(row, neighborhood_avg):
    reasons = []

    age = int(row["ilan_yasi_gun"])
    price_change = float(row["fiyat_degisimi_yuzde"])
    price_m2 = float(row["fiyat_m2"])

    # İlan yaşı
    if age >= 120:
        reasons.append(
            f"İlan {age} gündür aktif."
        )
    elif age >= 60:
        reasons.append(
            f"İlan {age} gündür aktif."
        )

    # Fiyat güncellemesi
    if pd.isna(row["son_fiyat_guncelleme"]):
        reasons.append(
            "İlan için henüz fiyat güncellemesi yapılmamış."
        )

    # Fiyat değişimi
    if price_change <= -5:
        reasons.append(
            f"Fiyat daha önce %{abs(price_change):.1f} düşürülmüş."
        )

    # Mahalle ortalaması
    if neighborhood_avg > 0:
        ratio = price_m2 / neighborhood_avg

        if ratio >= 1.15:
            reasons.append(
                "Fiyat/m² mahalle ortalamasının belirgin şekilde üzerinde."
            )

        elif ratio >= 1.05:
            reasons.append(
                "Fiyat/m² mahalle ortalamasının üzerinde."
            )

    # Aksiyon
    if age >= 120 and price_m2 > neighborhood_avg:
        action = (
            "Mal sahibiyle fiyat revizyonu görüşülmesi "
            "önerilir."
        )

    elif age >= 90:
        action = (
            "Portföy sahibinden fiyat ve satış beklentisi "
            "tekrar değerlendirilmelidir."
        )

    elif price_change <= -5:
        action = (
            "Fiyat değişiminin ilan performansına etkisi "
            "kontrol edilmelidir."
        )

    else:
        action = (
            "Portföy mevcut koşullarda takip edilmeye "
            "devam edilebilir."
        )

    return reasons, action


def calculate_score_breakdown(row, df):
    """
    Seçilen portföyün öncelik skorunun
    hangi kriterlerden oluştuğunu hesaplar.
    """

    # 1. İlan yaşı — maksimum 40 puan
    age_score = min(
        max(
            row["ilan_yasi_gun"] / 180 * 40,
            0,
        ),
        40,
    )

    # 2. Fiyat değişimi — maksimum 30 puan
    price_change_score = min(
        max(
            -row["fiyat_degisimi_yuzde"] / 15 * 30,
            0,
        ),
        30,
    )

    # 3. Fiyat güncellemesi yok — 10 puan
    no_update_score = (
        10
        if pd.isna(row["son_fiyat_guncelleme"])
        else 0
    )

    # 4. Aynı mahalle + aynı ilan türü ortalaması
    comparison_df = df[
    (df["mahalle"] == row["mahalle"])
    & (
        df["ilan_turu"]
        == row["ilan_turu"]
    )
    & (
        df["portfoy_tipi"]
        == row["portfoy_tipi"]
    )
]

    neighborhood_avg = comparison_df[
        "fiyat_m2"
    ].mean()

    if neighborhood_avg > 0:
        price_ratio = (
            row["fiyat_m2"]
            / neighborhood_avg
        )

        expensive_score = min(
            max(
                (price_ratio - 1) * 100,
                0,
            ),
            20,
        )
    else:
        expensive_score = 0

    total_score = min(
        age_score
        + price_change_score
        + no_update_score
        + expensive_score,
        100,
    )

    return {
        "İlan yaşı": round(age_score, 1),
        "Fiyat değişimi": round(
            price_change_score,
            1,
        ),
        "Fiyat güncellemesi": round(
            no_update_score,
            1,
        ),
        "Bölge fiyat farkı": round(
            expensive_score,
            1,
        ),
        "Toplam": round(
            total_score,
            1,
        ),
    }

# ---------------------------------------------------------
# BAŞLIK
# ---------------------------------------------------------

st.title("🏠 Emlak Portföy Analizörü")

st.markdown(
    """
    Emlak portföyünüzü analiz edin, uzun süredir bekleyen
    ilanları ve fiyat değişimlerini kolayca takip edin.
    """
)


# ---------------------------------------------------------
# VERİ KAYNAĞI
# ---------------------------------------------------------

st.sidebar.header("📂 Veri Kaynağı")

data_source = st.sidebar.radio(
    "Veri kaynağını seçin",
    [
        "Demo verisi",
        "Kendi dosyamı yükle",
    ],
)


if data_source == "Demo verisi":

    df = load_data(DATA_FILE)

    st.sidebar.success(
        "500 adet örnek Tarsus portföyü kullanılıyor."
    )

else:

    uploaded_file = st.sidebar.file_uploader(
        "CSV dosyanızı yükleyin",
        type=["csv"],
        help=(
            "Emlak portföyünüzü CSV formatında yükleyin."
        ),
    )

    if uploaded_file is None:

        st.info(
            "👈 Analiz yapmak için sol menüden "
            "CSV dosyanızı yükleyin."
        )

        st.stop()

    try:
        uploaded_df = pd.read_csv(uploaded_file)

        missing_columns = validate_data(uploaded_df)

        if missing_columns:

            st.error(
                "Dosyanızda gerekli kolonlar bulunmuyor:"
            )

            st.code(
                "\n".join(missing_columns)
            )

            st.stop()

        df = prepare_data(uploaded_df)

        st.sidebar.success(
            f"{len(df):,} portföy yüklendi."
        )

    except Exception as error:

        st.error(
            f"Dosya okunurken hata oluştu: {error}"
        )

        st.stop()


# ---------------------------------------------------------
# SIDEBAR FİLTRELER
# ---------------------------------------------------------

st.sidebar.divider()

st.sidebar.header("🔎 Filtreler")


ilan_turu_options = [
    "Tümü"
] + sorted(
    df["ilan_turu"]
    .dropna()
    .unique()
    .tolist()
)

selected_ilan_turu = st.sidebar.selectbox(
    "İlan Türü",
    ilan_turu_options,
)


portfoy_options = [
    "Tümü"
] + sorted(
    df["portfoy_tipi"]
    .dropna()
    .unique()
    .tolist()
)

selected_portfoy = st.sidebar.selectbox(
    "Portföy Tipi",
    portfoy_options,
)


mahalle_options = [
    "Tümü"
] + sorted(
    df["mahalle"]
    .dropna()
    .unique()
    .tolist()
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
        filtered_df["ilan_turu"]
        == selected_ilan_turu
    ]


if selected_portfoy != "Tümü":

    filtered_df = filtered_df[
        filtered_df["portfoy_tipi"]
        == selected_portfoy
    ]


if selected_mahalle != "Tümü":

    filtered_df = filtered_df[
        filtered_df["mahalle"]
        == selected_mahalle
    ]
    
# ---------------------------------------------------------
# PORTFÖY SEÇİMİ
# ---------------------------------------------------------

st.sidebar.divider()

st.sidebar.header("🏠 Portföy Seç")

portfolio_options = (
    filtered_df["ilan_id"]
    .dropna()
    .tolist()
)

selected_listing_id = st.sidebar.selectbox(
    "İlan",
    portfolio_options,
)
# ---------------------------------------------------------
# PORTFÖY DETAYI
# ---------------------------------------------------------

selected_row = filtered_df[
    filtered_df["ilan_id"] == selected_listing_id
].iloc[0]

# ---------------------------------------------------------
# PİYASA KARŞILAŞTIRMASI
# ---------------------------------------------------------

similar_properties = df[
    (df["mahalle"] == selected_row["mahalle"])
    & (df["ilan_turu"] == selected_row["ilan_turu"])
    & (
        df["portfoy_tipi"]
        == selected_row["portfoy_tipi"]
    )
].copy()

market_avg_price_m2 = similar_properties[
    "fiyat_m2"
].mean()

selected_price_m2 = float(
    selected_row["fiyat_m2"]
)

if market_avg_price_m2 > 0:
    market_difference_percent = (
        (
            selected_price_m2
            - market_avg_price_m2
        )
        / market_avg_price_m2
        * 100
    )
else:
    market_difference_percent = 0


# ---------------------------------------------------------
# RİSK SEVİYESİ
# ---------------------------------------------------------

priority_score = float(
    selected_row["portfoy_oncelik_skoru"]
)

if priority_score >= 70:
    risk_level = "🔴 Yüksek"
    risk_text = (
        "Bu portföy yakın takip ve aksiyon gerektiriyor."
    )

elif priority_score >= 40:
    risk_level = "🟡 Orta"
    risk_text = (
        "Bu portföy düzenli takip edilmeli."
    )

else:
    risk_level = "🟢 Düşük"
    risk_text = (
        "Bu portföy için şu anda kritik bir durum görünmüyor."
    )


neighborhood_avg = (
    filtered_df[
        (filtered_df["mahalle"] == selected_row["mahalle"])
        & (
            filtered_df["ilan_turu"]
            == selected_row["ilan_turu"]
        )
    ]["fiyat_m2"]
    .mean()
)


reasons, action = get_action_recommendation(
    selected_row,
    neighborhood_avg,
)


st.subheader("🎯 Seçilen Portföy")


detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4)


detail_col1.metric(
    "İlan",
    selected_row["ilan_id"],
)


detail_col2.metric(
    "Fiyat",
    f"{selected_row['fiyat']:,.0f} TL",
)


detail_col3.metric(
    "Alan",
    f"{selected_row['metrekare']:,.0f} m²",
)


detail_col4.metric(
    "Öncelik",
    f"{selected_row['portfoy_oncelik_skoru']:.1f}/100",
)


st.markdown(
    f"""
    **{selected_row['mahalle']}**
    
    {selected_row['portfoy_tipi']} ·
    {selected_row['ilan_turu']} ·
    {selected_row['oda_sayisi']}
    """
)


detail_left, detail_right = st.columns(2)


with detail_left:

    st.markdown("### ⚠️ Dikkat Gerektiren Noktalar")

    if reasons:

        for reason in reasons:
            st.warning(reason)

    else:

        st.success(
            "Bu portföy için belirgin bir risk tespit edilmedi."
        )


with detail_right:

    st.markdown("### 💡 Önerilen Aksiyon")

    st.info(action)


# ---------------------------------------------------------
# KARAR MERKEZİ
# ---------------------------------------------------------

st.subheader("🎯 Karar Merkezi")

decision_col1, decision_col2, decision_col3 = st.columns(3)


with decision_col1:

    st.markdown("### 📊 Piyasa Durumu")

    st.metric(
        "İlan Fiyatı / m²",
        f"{selected_price_m2:,.0f} TL",
    )

    st.metric(
        "Benzer Portföy Ortalaması",
        f"{market_avg_price_m2:,.0f} TL",
    )

    if market_difference_percent > 0:

        st.warning(
            f"İlan, benzer portföylere göre "
            f"%{market_difference_percent:.1f} daha yüksek."
        )

    elif market_difference_percent < 0:

        st.success(
            f"İlan, benzer portföylere göre "
            f"%{abs(market_difference_percent):.1f} daha düşük."
        )

    else:

        st.info(
            "İlan fiyatı benzer portföylerin ortalamasına yakın."
        )


with decision_col2:

    st.markdown("### ⚠️ Risk Özeti")

    st.metric(
        "Risk Seviyesi",
        risk_level,
    )

    st.caption(risk_text)

    st.caption(
        f"{len(similar_properties)} benzer "
        f"portföy üzerinden karşılaştırıldı."
    )

    st.caption(
        f"İlan yaşı: "
        f"{int(selected_row['ilan_yasi_gun'])} gün"
    )

    st.caption(
        f"Fiyat değişimi: "
        f"{selected_row['fiyat_degisimi_yuzde']:+.1f}%"
    )


with decision_col3:

    st.markdown("### 💡 Önerilen Aksiyon")

    st.info(action)

    if priority_score >= 70:

        st.warning(
            "Bu portföy için aksiyon öncelikli."
        )

    elif priority_score >= 40:

        st.info(
            "Portföyü takip listesinde tutun."
        )

    else:

        st.success(
            "Şimdilik rutin takip yeterli."
        )

st.divider()

# ---------------------------------------------------------
# SKOR AÇIKLAMASI
# ---------------------------------------------------------

score_breakdown = calculate_score_breakdown(
    selected_row,
    df,
)

with st.expander("📊 Öncelik skoru nasıl hesaplanıyor?"):

    st.markdown(
        """
        Öncelik skoru, portföyün emlakçı tarafından
        tekrar değerlendirilme ihtiyacını ölçmek için
        dört farklı kriter kullanır.
        """
    )

    score_col1, score_col2 = st.columns(2)

    with score_col1:

        st.metric(
            "İlan yaşı",
            f"+{score_breakdown['İlan yaşı']} puan",
        )

        st.caption(
            "İlan 180 güne yaklaştıkça "
            "öncelik puanı artar. Maksimum 40 puan."
        )

        st.metric(
            "Fiyat değişimi",
            f"+{score_breakdown['Fiyat değişimi']} puan",
        )

        st.caption(
            "Fiyat indirimi yapılmışsa öncelik artar. "
            "Maksimum 30 puan."
        )

    with score_col2:

        st.metric(
            "Fiyat güncellemesi",
            f"+{score_breakdown['Fiyat güncellemesi']} puan",
        )

        st.caption(
            "Uzun süredir fiyat güncellenmeyen "
            "portföylere 10 puan eklenir."
        )

        st.metric(
            "Bölge fiyat farkı",
            f"+{score_breakdown['Bölge fiyat farkı']} puan",
        )

        st.caption(
            "Aynı mahalle ve ilan türündeki ortalamaya "
            "göre yüksek fiyatlı portföylere maksimum "
            "20 puan eklenir."
        )

    st.divider()

    st.metric(
        "Hesaplanan toplam skor",
        f"{score_breakdown['Toplam']} / 100",
    )

# ---------------------------------------------------------
# KPI
# ---------------------------------------------------------

total_listings = len(filtered_df)

sale_count = len(
    filtered_df[
        filtered_df["ilan_turu"]
        == "Satılık"
    ]
)

rent_count = len(
    filtered_df[
        filtered_df["ilan_turu"]
        == "Kiralık"
    ]
)

old_listing_count = len(
    filtered_df[
        filtered_df["ilan_yasi_gun"]
        >= 60
    ]
)

price_drop_count = len(
    filtered_df[
        filtered_df["fiyat_degisimi_yuzde"]
        < 0
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

st.subheader("📊 Mahalle Bazlı Satılık Fiyat Analizi")


sale_df = filtered_df[
    filtered_df["ilan_turu"]
    == "Satılık"
].copy()


if not sale_df.empty:

    neighborhood_analysis = (
        sale_df
        .groupby("mahalle")
        .agg(
            ortalama_fiyat_m2=(
                "fiyat_m2",
                "mean",
            ),
            portfoy_sayisi=(
                "ilan_id",
                "count",
            ),
        )
        .reset_index()
        .sort_values(
            "ortalama_fiyat_m2",
            ascending=False,
        )
    )

    neighborhood_analysis[
        "ortalama_fiyat_m2"
    ] = (
        neighborhood_analysis[
            "ortalama_fiyat_m2"
        ]
        .round(0)
    )

    st.bar_chart(
        neighborhood_analysis.set_index(
            "mahalle"
        )["ortalama_fiyat_m2"]
    )

else:

    st.info(
        "Mahalle analizi için satılık "
        "portföy bulunamadı."
    )


# ---------------------------------------------------------
# İKİ SÜTUN
# ---------------------------------------------------------

left_col, right_col = st.columns(2)


# ---------------------------------------------------------
# ÖNCELİKLİ PORTFÖYLER
# ---------------------------------------------------------

with left_col:

    st.subheader(
        "🔥 Öncelikli Portföyler"
    )

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
        .map(
            lambda x:
            f"{x:,.0f} TL"
        )
    )

    priority_display[
        "portfoy_oncelik_skoru"
    ] = (
        priority_display[
            "portfoy_oncelik_skoru"
        ]
        .map(
            lambda x:
            f"{x:.1f}"
        )
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

    st.subheader(
        "⏳ Uzun Süredir Bekleyenler"
    )

    old_df = (
        filtered_df[
            filtered_df[
                "ilan_yasi_gun"
            ] >= 60
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
        .map(
            lambda x:
            f"{x:,.0f} TL"
        )
    )

    st.dataframe(
        old_display,
        hide_index=True,
        width="stretch",
    )


st.divider()


# ---------------------------------------------------------
# FİYAT DEĞİŞİMLERİ
# ---------------------------------------------------------

st.subheader(
    "📉 Fiyatı Değişen Portföyler"
)


price_changed = (
    filtered_df[
        filtered_df[
            "fiyat_degisimi_yuzde"
        ] != 0
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
        .map(
            lambda x:
            f"{x:,.0f} TL"
        )
    )

    price_display["onceki_fiyat"] = (
        price_display["onceki_fiyat"]
        .map(
            lambda x:
            f"{x:,.0f} TL"
        )
    )

    price_display[
        "fiyat_degisimi_yuzde"
    ] = (
        price_display[
            "fiyat_degisimi_yuzde"
        ]
        .map(
            lambda x:
            f"{x:+.2f}%"
        )
    )

    st.dataframe(
        price_display,
        hide_index=True,
        width="stretch",
    )

else:

    st.info(
        "Filtrelere uygun fiyat değişikliği "
        "bulunamadı."
    )


# ---------------------------------------------------------
# TÜM PORTFÖYLER
# ---------------------------------------------------------

with st.expander(
    "📋 Tüm Filtrelenmiş Portföyleri Gör"
):

    st.dataframe(
        filtered_df,
        hide_index=True,
        width="stretch",
    )