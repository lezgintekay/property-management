from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


# ---------------------------------------------------------
# SAYFA AYARLARI
# ---------------------------------------------------------

st.set_page_config(
    page_title="Emlak Portföy Analizörü",
    page_icon="🏠",
    layout="wide",
)

st.markdown(
    """
    <style>

    /* =====================================================
                MATERIAL 3 — LIGHT THEME
       ===================================================== */

    :root {
        --surface: #FFFFFF;
        --surface-container: #F7F9FC;
        --surface-container-high: #EEF0F4;

        --primary: #3F51B5;
        --primary-container: #E8EAF6;

        --on-surface: #1A1B20;
        --on-surface-variant: #5F6368;

        --outline: #E1E3E8;

        --success: #2E7D32;
        --warning: #B26A00;
        --error: #BA1A1A;
    }

    /* -----------------------------------------------------
                            APP
       ----------------------------------------------------- */

    [data-testid="stAppViewContainer"] {
        background: var(--surface-container);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1440px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* -----------------------------------------------------
                            SIDEBAR
       ----------------------------------------------------- */

    [data-testid="stSidebar"] {
        background: var(--surface);
        border-right: 1px solid var(--outline);
    }

    [data-testid="stSidebar"] * {
        color: var(--on-surface);
    }

/* -----------------------------------------------------
                    TYPOGRAPHY
   ----------------------------------------------------- */

h1,
h2,
h3 {
    color: var(--on-surface) !important;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}

h1 {
    font-size: 2rem !important;
    font-weight: 600 !important;
    line-height: 1.2 !important;
}

h2 {
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    line-height: 1.3 !important;
}

h3 {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    line-height: 1.4 !important;
}

p {
    color: var(--on-surface-variant);
    line-height: 1.55;
}

label {
    color: var(--on-surface-variant) !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
}

    /* -----------------------------------------------------
                            METRIC CARDS
       ----------------------------------------------------- */

    [data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid var(--outline);
        border-radius: 16px;
        padding: 1rem;
    }

    /* -----------------------------------------------------
                    CUSTOM MATERIAL CARDS
   ----------------------------------------------------- */

.material-card {
    background: var(--surface);
    border: 1px solid var(--outline);
    border-radius: 16px;
    padding: 1.1rem 1.2rem;
    min-height: 105px;
    box-sizing: border-box;
    transition: box-shadow 0.2s ease;
}

.kpi-card {
    min-height: 100px;
    padding: 1rem 1.1rem;
}

.kpi-card .card-value {
    font-size: 1.65rem;
}

.material-card:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* -----------------------------------------------------
                    RISK STATUS
   ----------------------------------------------------- */

.risk-status {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin-top: 0.35rem;
}

.risk-dot {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}

.risk-low {
    background: #7CB342;
}

.risk-medium {
    background: #F9A825;
}

.risk-high {
    background: #D32F2F;
}

.risk-value {
    color: var(--on-surface);
    font-size: 1.55rem;
    font-weight: 500;
    line-height: 1.25;
}

.card-label {
    color: var(--on-surface-variant);
    font-size: 0.82rem;
    font-weight: 500;
    margin-bottom: 0.45rem;
}

.card-value {
    color: var(--on-surface);
    font-size: 1.55rem;
    font-weight: 600;
    line-height: 1.25;
    letter-spacing: -0.015em;
}

.property-meta {
    margin-top: 0.9rem;
    margin-bottom: 1.5rem;
    color: var(--on-surface-variant);
    font-size: 0.95rem;
    line-height: 1.7;
}

.property-meta strong {
    color: var(--on-surface);
    font-weight: 600;
}

    [data-testid="stMetricLabel"] {
        color: var(--on-surface-variant) !important;
    }

    [data-testid="stMetricValue"] {
        color: var(--on-surface) !important;
    }

    /* -----------------------------------------------------
                            BUTTONS
       ----------------------------------------------------- */

    .stButton > button {
        border-radius: 999px;
        border: 1px solid var(--outline);
        background: var(--surface);
        color: var(--on-surface);
        font-weight: 500;
        min-height: 42px;
    }

    .stButton > button:hover {
        border-color: var(--primary);
        color: var(--primary);
    }

    /* -----------------------------------------------------
                            SELECTBOX
       ----------------------------------------------------- */

    [data-baseweb="select"] > div {
        border-radius: 12px;
        border-color: var(--outline);
        background: var(--surface);
    }

    /* -----------------------------------------------------
                            EXPANDER
       ----------------------------------------------------- */

    [data-testid="stExpander"] {
        border: 1px solid var(--outline);
        border-radius: 16px;
        background: var(--surface);
    }

    /* -----------------------------------------------------
                            DATAFRAME
       ----------------------------------------------------- */

    [data-testid="stDataFrame"] {
        border: 1px solid var(--outline);
        border-radius: 16px;
        overflow: hidden;
    }

    /* -----------------------------------------------------
                    TABLE CARD TYPOGRAPHY
       ----------------------------------------------------- */

    .table-card-title {
        color: var(--on-surface);
        font-size: 1.05rem;
        font-weight: 650;
        line-height: 1.3;
        margin: 0 0 0.2rem 0;
        letter-spacing: -0.01em;
    }

    .table-card-description {
        color: var(--on-surface-variant);
        font-size: 0.78rem;
        font-weight: 400;
        line-height: 1.35;
        margin: 0 0 0.55rem 0;
    }


    /* -----------------------------------------------------
                            FILE UPLOADER
       ----------------------------------------------------- */

    [data-testid="stFileUploader"] {
        background: var(--surface);
        border: 1px solid var(--outline);
        border-radius: 16px;
        padding: 0.5rem;
    }

    /* -----------------------------------------------------
                            MATERIAL ALERTS
   ----------------------------------------------------- */

.material-alert {
    border-radius: 12px;
    padding: 0.85rem 1rem;
    margin: 0.5rem 0;
    border: 1px solid transparent;
    font-size: 0.92rem;
    line-height: 1.5;
    box-sizing: border-box;
}

.material-alert.warning {
    background: #FFFBE6;
    border-color: #F0E7A8;
    color: #5F5B22;
}

.material-alert.success {
    background: #E8F5E9;
    border-color: #C8E6C9;
    color: #245B2A;
}

.material-alert.info {
    background: #E8F1FB;
    border-color: #C7DCF5;
    color: #28527A;
}

/* Streamlit başlıklarının otomatik anchor ikonlarını gizle */
[data-testid="stHeadingWithActionElements"] a {
    display: none !important;
}

        /* =====================================================
                        SIDEBAR CONTROLS — LIGHT
       ===================================================== */

    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #DADCE0 !important;
        color: #1A1B20 !important;
        border-radius: 10px !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] input {
        color: #1A1B20 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] span {
        color: #1A1B20 !important;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label {
        color: #1A1B20 !important;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background: #FFFFFF !important;
    }

    /* Sidebar başlıkları */

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-size: 1rem !important;
        font-weight: 600 !important;
    }

    /* =====================================================
                SIDEBAR SELECTBOX — MATERIAL LIGHT
   ===================================================== */

[data-testid="stSidebar"] [data-baseweb="select"] {
    background: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #DADCE0 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] [role="button"] {
    background-color: #FFFFFF !important;
    color: #1A1B20 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] [role="button"] * {
    background-color: transparent !important;
    color: #1A1B20 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] input {
    background-color: #FFFFFF !important;
    color: #1A1B20 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] svg {
    fill: #5F6368 !important;
}

[data-testid="stSidebar"] [data-baseweb="popover"] {
    background-color: #FFFFFF !important;
}

[data-testid="stSidebar"] [role="listbox"] {
    background-color: #FFFFFF !important;
    border: 1px solid #DADCE0 !important;
}

[data-testid="stSidebar"] [role="option"] {
    background-color: #FFFFFF !important;
    color: #1A1B20 !important;
}

[data-testid="stSidebar"] [role="option"]:hover {
    background-color: #F1F3F4 !important;
}

    </style>
    """,
    unsafe_allow_html=True,
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
    "ilan_tarihi",
]

COLUMN_ALIASES = {
    "ilan_id": [
        "ilan_id",
        "ilan no",
        "ilan_no",
        "ilan numarası",
        "ilan numarasi",
        "ilan kodu",
        "ilan_kodu",
        "id",
    ],

    "portfoy_tipi": [
        "portfoy_tipi",
        "portföy tipi",
        "portfoy tipi",
        "tip",
        "emlak tipi",
        "gayrimenkul tipi",
        "tür",
        "tur",
    ],

    "ilan_turu": [
        "ilan_turu",
        "ilan türü",
        "ilan turu",
        "işlem türü",
        "islem turu",
        "satış/kiralık",
        "satis/kiralik",
        "satis_kiralik",
    ],

    "mahalle": [
        "mahalle",
        "mahalle adı",
        "mahalle adi",
        "semt",
        "bölge",
        "bolge",
    ],

    "oda_sayisi": [
        "oda_sayisi",
        "oda sayısı",
        "oda sayisi",
        "oda",
        "oda tipi",
        "oda tipi",
    ],

    "metrekare": [
        "metrekare",
        "m²",
        "m2",
        "m² net",
        "m2 net",
        "alan",
        "alan m2",
        "alan (m2)",
    ],

    "fiyat": [
        "fiyat",
        "satış fiyatı",
        "satis fiyati",
        "satış fiyat",
        "satis fiyat",
        "kira",
        "kira fiyatı",
        "kira fiyati",
        "bedel",
    ],

    "onceki_fiyat": [
        "onceki_fiyat",
        "önceki fiyat",
        "onceki fiyat",
        "eski fiyat",
        "eski fiyatı",
        "eski fiyati",
    ],

    "ilan_tarihi": [
        "ilan_tarihi",
        "ilan tarihi",
        "yayın tarihi",
        "yayin tarihi",
        "oluşturulma tarihi",
        "olusturulma tarihi",
    ],

    "son_fiyat_guncelleme": [
        "son_fiyat_guncelleme",
        "son fiyat güncelleme",
        "son fiyat güncellemesi",
        "fiyat güncelleme tarihi",
        "fiyat güncelleme",
    ],

    "durum": [
        "durum",
        "ilan durumu",
        "aktiflik",
        "aktif/pasif",
        "aktif pasif",
    ],
}

@st.cache_data
def load_data(file):
    df = pd.read_csv(file)

    return prepare_data(df)


def normalize_column_name(name):
    return (
        str(name)
        .strip()
        .lower()
        .replace("_", " ")
        .replace("-", " ")
    )


def map_columns(df):
    df = df.copy()

    normalized_columns = {
        normalize_column_name(column): column
        for column in df.columns
    }

    rename_map = {}

    for target_column, aliases in COLUMN_ALIASES.items():

        for alias in aliases:

            normalized_alias = normalize_column_name(alias)

            if normalized_alias in normalized_columns:
                original_column = normalized_columns[
                    normalized_alias
                ]

                rename_map[original_column] = target_column
                break

    df = df.rename(columns=rename_map)

    return df

def prepare_data(df):
    df = df.copy()

    # -----------------------------------------------------
    # KOLONLARI TANIMA
    # -----------------------------------------------------

    df = map_columns(df)

    # -----------------------------------------------------
    # OPSİYONEL ALANLAR
    # -----------------------------------------------------

    if "onceki_fiyat" not in df.columns:
        df["onceki_fiyat"] = df["fiyat"]

    if "son_fiyat_guncelleme" not in df.columns:
        df["son_fiyat_guncelleme"] = pd.NaT

    if "durum" not in df.columns:
        df["durum"] = "Aktif"

    # -----------------------------------------------------
    # TARİHLER
    # -----------------------------------------------------

    df["ilan_tarihi"] = pd.to_datetime(
        df["ilan_tarihi"],
        errors="coerce",
    )

    df["son_fiyat_guncelleme"] = pd.to_datetime(
        df["son_fiyat_guncelleme"],
        errors="coerce",
    )

    # -----------------------------------------------------
    # SAYISAL ALANLAR
    # -----------------------------------------------------

    numeric_columns = [
        "metrekare",
        "fiyat",
        "onceki_fiyat",
    ]

    for column in numeric_columns:
        df[column] = (
            df[column]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.replace("TL", "", regex=False)
            .str.strip()
        )

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # -----------------------------------------------------
    # HESAPLANAN ALANLAR
    # -----------------------------------------------------

    df["fiyat_m2"] = (
    df["fiyat"]
    .div(df["metrekare"])
    .where(df["metrekare"] > 0)
    .round(2)
)
    today = pd.Timestamp.today().normalize()

    df["ilan_yasi_gun"] = (
        today - df["ilan_tarihi"]
    ).dt.days.clip(lower=0)

    df["fiyat_degisimi_yuzde"] = (
        (
            df["fiyat"]
            - df["onceki_fiyat"]
        )
        / df["onceki_fiyat"]
        * 100
    ).replace(
        [float("inf"), -float("inf")],
        0,
    )

    df["fiyat_degisimi_yuzde"] = (
        df["fiyat_degisimi_yuzde"]
        .fillna(0)
        .round(2)
    )

    # -----------------------------------------------------
    # ÖNCELİK SKORU
    # -----------------------------------------------------

    df["portfoy_oncelik_skoru"] = (
        calculate_priority_score(df)
    )

    return df


def validate_data(df):
    df = map_columns(df)

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    return missing_columns

def validate_data_quality(df):
    issues = {}

    invalid_price = (
        df["fiyat"].isna()
        | (df["fiyat"] <= 0)
    )

    invalid_area = (
        df["metrekare"].isna()
        | (df["metrekare"] <= 0)
    )

    invalid_date = df["ilan_tarihi"].isna()

    if invalid_price.sum() > 0:
        issues["Geçersiz fiyat"] = int(
            invalid_price.sum()
        )

    if invalid_area.sum() > 0:
        issues["Geçersiz metrekare"] = int(
            invalid_area.sum()
        )

    if invalid_date.sum() > 0:
        issues["Geçersiz ilan tarihi"] = int(
            invalid_date.sum()
        )

    return issues


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

def calculate_priority_score(df):
    score = pd.Series(
        0.0,
        index=df.index,
    )

    # İlan yaşı — maksimum 40
    age_score = (
        df["ilan_yasi_gun"]
        / 180
        * 40
    ).clip(
        lower=0,
        upper=40,
    )

    score += age_score

    # Fiyat değişimi — maksimum 30
    price_change_score = (
        -df["fiyat_degisimi_yuzde"]
        / 15
        * 30
    ).clip(
        lower=0,
        upper=30,
    )

    score += price_change_score

    # Fiyat güncellemesi yok — 10
    no_update = (
        df["son_fiyat_guncelleme"]
        .isna()
    )

    score += (
        no_update.astype(int) * 10
    )

    # Aynı mahalle + ilan türü + portföy tipi
    neighborhood_avg = (
        df.groupby(
            [
                "mahalle",
                "ilan_turu",
                "portfoy_tipi",
            ]
        )["fiyat_m2"]
        .transform("mean")
    )

    price_ratio = (
        df["fiyat_m2"]
        / neighborhood_avg
    )

    expensive_score = (
        (price_ratio - 1) * 100
    ).clip(
        lower=0,
        upper=20,
    )

    score += expensive_score

    return score.clip(
        lower=0,
        upper=100,
    ).round(1)


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

st.title("Emlak Portföy Analizörü")
st.caption(
    "Portföyünüzü analiz edin, piyasa koşullarını karşılaştırın "
    "ve aksiyon gerektiren ilanları belirleyin."
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

        mapped_df = map_columns(uploaded_df)

        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if column not in mapped_df.columns
        ]

        if missing_columns:

            st.error(
                "Dosyanızdaki bazı temel alanlar tanınamadı:"
            )

            st.code(
                "\n".join(missing_columns)
            )

            st.info(
                "Gerekli temel alanları ekleyip dosyayı tekrar yükleyin."
            )

            st.stop()

        df = prepare_data(mapped_df)

        data_quality_issues = validate_data_quality(df)

        if data_quality_issues:

            st.error(
                "Yüklenen dosyada analiz için düzeltilmesi gereken "
                "veriler bulundu."
            )

            for issue, count in data_quality_issues.items():

                st.warning(
                    f"{issue}: {count:,} kayıt"
                )

            st.info(
                "Lütfen dosyanızı düzelttikten sonra tekrar yükleyin."
            )

            st.stop()

        st.sidebar.success(
            f"{len(df):,} portföy yüklendi."
        )

    except Exception as exc:

        st.error(
            "CSV dosyası okunurken bir hata oluştu. "
            "Lütfen dosya formatını kontrol edip tekrar deneyin."
        )

        st.exception(exc)
        st.stop()


# ---------------------------------------------------------
# SIDEBAR FİLTRELER
# ---------------------------------------------------------

st.sidebar.divider()

st.sidebar.header("Filtreler")


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

st.sidebar.caption(
    f"{len(filtered_df):,} portföy bulundu."
)

# ---------------------------------------------------------
# PORTFÖY SEÇİMİ
# ---------------------------------------------------------

if filtered_df.empty:
    st.info(
        "Seçtiğiniz filtrelere uygun portföy bulunamadı. "
        "Lütfen filtreleri değiştirerek tekrar deneyin."
    )
    st.stop()

st.sidebar.divider()

st.sidebar.header("Portföy Seç")

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
    risk_level = "Yüksek"
    risk_text = (
        "Bu portföy yakın takip ve aksiyon gerektiriyor."
    )

elif priority_score >= 40:
    risk_level = "Orta"
    risk_text = (
        "Bu portföy düzenli takip edilmeli."
    )

else:
    risk_level = "Düşük"
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

st.subheader("Seçilen Portföy")


# ---------------------------------------------------------
# PORTFÖY BİLGİ KARTLARI
# ---------------------------------------------------------

detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4)


with detail_col1:
    st.markdown(
        f"""
        <div class="material-card">
            <div class="card-label">İlan</div>
            <div class="card-value">{selected_row["ilan_id"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with detail_col2:
    st.markdown(
        f"""
        <div class="material-card">
            <div class="card-label">Fiyat</div>
            <div class="card-value">
                {selected_row["fiyat"]:,.0f} TL
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with detail_col3:
    st.markdown(
        f"""
        <div class="material-card">
            <div class="card-label">Alan</div>
            <div class="card-value">
                {selected_row["metrekare"]:,.0f} m²
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with detail_col4:
    st.markdown(
        f"""
        <div class="material-card">
            <div class="card-label">Öncelik</div>
            <div class="card-value">
                {selected_row["portfoy_oncelik_skoru"]:.1f}/100
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    f"""
    <div class="property-meta">
        <strong>{selected_row["mahalle"]}</strong>
        <br>
        {selected_row["portfoy_tipi"]} ·
        {selected_row["ilan_turu"]} ·
        {selected_row["oda_sayisi"]}
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# DİKKAT / AKSİYON
# ---------------------------------------------------------

st.markdown("### Dikkat Gerektiren Noktalar")

if reasons:

    for reason in reasons:
        st.markdown(
            f"""
            <div class="material-alert warning">
                {reason}
            </div>
            """,
            unsafe_allow_html=True,
        )

else:

    st.markdown(
        """
        <div class="material-alert success">
            Bu portföy için belirgin bir risk tespit edilmedi.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# KARAR MERKEZİ
# ---------------------------------------------------------

st.subheader("Karar Merkezi")

decision_col1, decision_col2, decision_col3 = st.columns(3)


with decision_col1:

    st.markdown("### Piyasa Durumu")

    st.markdown(
        f"""
        <div class="material-card">
            <div class="card-label">İlan Fiyatı / m²</div>
            <div class="card-value">
                {selected_price_m2:,.0f} TL
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="material-card">
            <div class="card-label">
                Benzer Portföy Ortalaması
            </div>
            <div class="card-value">
                {market_avg_price_m2:,.0f} TL
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if market_difference_percent > 0:

        market_message = (
            f"İlan, benzer portföylere göre "
            f"%{market_difference_percent:.1f} daha yüksek."
        )

        market_class = "warning"

    elif market_difference_percent < 0:

        market_message = (
            f"İlan, benzer portföylere göre "
            f"%{abs(market_difference_percent):.1f} daha düşük."
        )

        market_class = "success"

    else:

        market_message = (
            "İlan fiyatı benzer portföylerin "
            "ortalamasına yakın."
        )

        market_class = "info"

    st.markdown(
        f"""
        <div class="material-alert {market_class}">
            {market_message}
        </div>
        """,
        unsafe_allow_html=True,
    )


with decision_col2:

    st.markdown("### Risk Özeti")

    risk_class = {
        "Düşük": "risk-low",
        "Orta": "risk-medium",
        "Yüksek": "risk-high",
    }[risk_level]

    risk_card = f"""
<div class="material-card">
    <div class="card-label">Risk Seviyesi</div>
    <div class="risk-status">
        <span class="risk-dot {risk_class}"></span>
        <span class="risk-value">{risk_level}</span>
    </div>
</div>
"""

    st.markdown(
        risk_card,
        unsafe_allow_html=True,
    )

    st.caption(risk_text)

    st.caption(
        f"{len(similar_properties)} benzer "
        f"portföy üzerinden karşılaştırıldı."
    )

    st.caption(
        f"İlan yaşı: "
        f"{selected_row['ilan_yasi_gun']} gün"
    )

    st.caption(
        f"Fiyat değişimi: "
        f"{selected_row['fiyat_degisimi_yuzde']:.1f}%"
    )



with decision_col3:

    st.markdown("### Önerilen Aksiyon")

    st.markdown(
        f"""
        <div class="material-alert info">
            {action}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if priority_score >= 70:

        follow_up_message = (
            "Bu portföy için aksiyon öncelikli."
        )

        follow_up_class = "warning"

    elif priority_score >= 40:

        follow_up_message = (
            "Portföyü takip listesinde tutun."
        )

        follow_up_class = "info"

    else:

        follow_up_message = (
            "Şimdilik rutin takip yeterli."
        )

        follow_up_class = "success"

    st.markdown(
        f"""
        <div class="material-alert {follow_up_class}">
            {follow_up_message}
        </div>
        """,
        unsafe_allow_html=True,
    )


st.divider()

# ---------------------------------------------------------
# SKOR AÇIKLAMASI
# ---------------------------------------------------------

score_breakdown = calculate_score_breakdown(
    selected_row,
    df,
)

with st.expander("Öncelik skoru nasıl hesaplanıyor?"):

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

kpi_data = [
    ("Toplam Portföy", total_listings),
    ("Satılık", sale_count),
    ("Kiralık", rent_count),
    ("60+ Günlük", old_listing_count),
    ("Fiyatı Düşen", price_drop_count),
]

kpi_columns = st.columns(5)

for column, (label, value) in zip(
    kpi_columns,
    kpi_data,
):
    with column:
        st.markdown(
            f"""
            <div class="material-card kpi-card">
                <div class="card-label">{label}</div>
                <div class="card-value">{value:,}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()


# ---------------------------------------------------------
# MAHALLE ANALİZİ
# ---------------------------------------------------------

st.subheader("Mahalle Bazlı Satılık Fiyat Analizi")


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

    fig = px.bar(
        neighborhood_analysis,
        x="mahalle",
        y="ortalama_fiyat_m2",
        labels={
            "mahalle": "Mahalle",
            "ortalama_fiyat_m2": "Ortalama Fiyat / m²",
        },
    )

    fig.update_traces(
        marker_color="#3F51B5",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Ortalama: %{y:,.0f} TL/m²"
            "<extra></extra>"
        ),
    )
    fig.update_layout(
        height=380,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            color="#1A1B20",
            size=13,
        ),
        xaxis=dict(
            title=None,
            showgrid=False,
            linecolor="#E1E3E8",
        ),
        yaxis=dict(
            title=None,
            showgrid=True,
            gridcolor="#EEF0F4",
            zeroline=False,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
        },
    )



else:

    st.info(
        "Mahalle analizi için satılık "
        "portföy bulunamadı."
    )


# ---------------------------------------------------------
# İKİ SÜTUN
# ---------------------------------------------------------

left_col, right_col = st.columns(
    [1, 1],
    gap="medium",
)


# ---------------------------------------------------------
# ÖNCELİKLİ PORTFÖYLER
# ---------------------------------------------------------

with left_col:

    with st.container(border=True):

        st.markdown(
            '<div class="table-card-title">'
            'Öncelikli Portföyler'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="table-card-description">'
            'En yüksek öncelik skoruna sahip 10 portföy.'
            '</div>',
            unsafe_allow_html=True,
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

        # -------------------------------------------------
        # TABLO FORMATLARI
        # -------------------------------------------------

        priority_display["fiyat"] = (
            priority_display["fiyat"]
            .map(lambda x: f"{x:,.0f} TL")
        )

        # -------------------------------------------------
        # ÖNCELİK RENKLENDİRME
        # -------------------------------------------------

        def priority_style(value):

            value = float(value)

            if value >= 70:
                return (
                    "color: #BA1A1A; "
                    "background-color: #FDECEC; "
                    "font-weight: 700;"
                )

            elif value >= 40:
                return (
                    "color: #B26A00; "
                    "background-color: #FFF8E1; "
                    "font-weight: 700;"
                )

            return (
                "color: #2E7D32; "
                "background-color: #E8F5E9; "
                "font-weight: 700;"
            )

        priority_styled = (
            priority_display.style
            .format(
                {
                    "portfoy_oncelik_skoru": "{:.1f}",
                }
            )
            .map(
                priority_style,
                subset=["portfoy_oncelik_skoru"],
            )
        )

        st.dataframe(
            priority_styled,
            hide_index=True,
            width="stretch",
            column_config={
                "ilan_id": st.column_config.TextColumn(
                    "İlan",
                    width="small",
                ),
                "mahalle": st.column_config.TextColumn(
                    "Mahalle",
                    width="small",
                ),
                "ilan_turu": st.column_config.TextColumn(
                    "Tür",
                    width="small",
                ),
                "fiyat": st.column_config.TextColumn(
                    "Fiyat",
                    width="small",
                ),
                "ilan_yasi_gun": st.column_config.NumberColumn(
                    "İlan Yaşı",
                    format="%d gün",
                    width="small",
                ),
                "portfoy_oncelik_skoru": st.column_config.NumberColumn(
                    "Öncelik",
                    format="%.1f",
                    width="small",
                ),
            },
        )

        st.caption(
            "Öncelik skoru 0–100 arasında hesaplanır. "
            "Skor yükseldikçe portföyün tekrar değerlendirilme "
            "önceliği artar."
        )


# ---------------------------------------------------------
# UZUN SÜREDİR BEKLEYENLER
# ---------------------------------------------------------

with right_col:

    with st.container(border=True):

        st.markdown(
            '<div class="table-card-title">'
            'Uzun Süredir Bekleyenler'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="table-card-description">'
            '60 günden uzun süredir yayında olan 10 portföy.'
            '</div>',
            unsafe_allow_html=True,
        )

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
            column_config={
                "ilan_id": st.column_config.TextColumn(
                    "İlan",
                    width="small",
                ),
                "mahalle": st.column_config.TextColumn(
                    "Mahalle",
                    width="small",
                ),
                "ilan_turu": st.column_config.TextColumn(
                    "Tür",
                    width="small",
                ),
                "fiyat": st.column_config.TextColumn(
                    "Fiyat",
                    width="small",
                ),
                "ilan_yasi_gun": st.column_config.NumberColumn(
                    "İlan Yaşı",
                    format="%d gün",
                    width="small",
                ),
            },
        )

        st.caption(
            "Bu portföyler uzun süredir yayında olduğu için "
            "fiyat, talep ve mal sahibi beklentilerinin "
            "yeniden değerlendirilmesi önerilir."
        )


st.divider()


# ---------------------------------------------------------
# FİYAT DEĞİŞİMLERİ
# ---------------------------------------------------------

with st.container(border=True):

    st.markdown(
        '<div class="table-card-title">'
        'Fiyatı Değişen Portföyler'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="table-card-description">'
        'Fiyatında değişiklik yapılan son 15 portföy.'
        '</div>',
        unsafe_allow_html=True,
    )

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

        # -------------------------------------------------
        # FİYAT FORMATLARI
        # -------------------------------------------------

        price_display["fiyat"] = (
            price_display["fiyat"]
            .map(lambda x: f"{x:,.0f} TL")
        )

        price_display["onceki_fiyat"] = (
            price_display["onceki_fiyat"]
            .map(lambda x: f"{x:,.0f} TL")
        )

        # -------------------------------------------------
        # FİYAT DEĞİŞİMİ RENKLENDİRME
        # -------------------------------------------------

        def price_change_style(value):

            value = float(value)

            if value < 0:
                return (
                    "color: #BA1A1A; "
                    "background-color: #FDECEC; "
                    "font-weight: 700;"
                )

            elif value > 0:
                return (
                    "color: #2E7D32; "
                    "background-color: #E8F5E9; "
                    "font-weight: 700;"
                )

            return (
                "color: #5F6368; "
                "background-color: #F1F3F4; "
                "font-weight: 600;"
            )

        price_styled = (
            price_display.style
            .format(
                {
                    "fiyat_degisimi_yuzde": "{:+.2f}%",
                }
            )
            .map(
                price_change_style,
                subset=["fiyat_degisimi_yuzde"],
            )
        )

        st.dataframe(
            price_styled,
            hide_index=True,
            width="stretch",
            column_config={
                "ilan_id": st.column_config.TextColumn(
                    "İlan",
                    width="small",
                ),
                "mahalle": st.column_config.TextColumn(
                    "Mahalle",
                    width="medium",
                ),
                "ilan_turu": st.column_config.TextColumn(
                    "Tür",
                    width="small",
                ),
                "fiyat": st.column_config.TextColumn(
                    "Güncel Fiyat",
                    width="medium",
                ),
                "onceki_fiyat": st.column_config.TextColumn(
                    "Önceki Fiyat",
                    width="medium",
                ),
                "fiyat_degisimi_yuzde": st.column_config.NumberColumn(
                    "Fiyat Değişimi (%)",
                    format="%+.2f%%",
                    width="medium",
                ),
            },
        )

        st.caption(
            "Kırmızı değerler fiyat indirimi, yeşil değerler "
            "fiyat artışı anlamına gelir."
        )

    else:

        st.info(
            "Filtrelere uygun fiyat değişikliği bulunamadı."
        )


# ---------------------------------------------------------
# TÜM PORTFÖYLER
# ---------------------------------------------------------

with st.expander(
    "Tüm Filtrelenmiş Portföyleri Gör"
):

    st.dataframe(
        filtered_df,
        hide_index=True,
        width="stretch",
    )