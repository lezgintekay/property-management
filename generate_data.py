import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# AYARLAR
# ---------------------------------------------------------

NUMBER_OF_LISTINGS = 500
OUTPUT_FILE = Path("data/emlak_portfoyleri.csv")

random.seed(42)


# ---------------------------------------------------------
# TARSUS MAHALLELERİ
# ---------------------------------------------------------

NEIGHBORHOODS = {
    "Yeni Mahalle": 34000,
    "Gaziler": 33800,
    "Şahin": 30000,
    "Bahçe": 28500,
    "Akşemsettin": 27000,
    "Yeşil Mahalle": 25000,
    "Mithatpaşa": 24500,
    "Kızılmurat": 23000,
    "Reşadiye": 22000,
    "Eski Yol": 20500,
}

PROPERTY_TYPES = {
    "Daire": {
        "weight": 70,
        "rooms": ["1+1", "2+1", "3+1", "4+1"],
    },
    "Müstakil Ev": {
        "weight": 10,
        "rooms": ["2+1", "3+1", "4+1", "5+1"],
    },
    "Villa": {
        "weight": 5,
        "rooms": ["3+1", "4+1", "5+1"],
    },
    "Dükkan": {
        "weight": 10,
        "rooms": ["1+0", "2+0", "3+0"],
    },
    "Ofis": {
        "weight": 5,
        "rooms": ["1+0", "2+0", "3+0"],
    },
}

LISTING_STATUS = ["Satılık", "Kiralık"]


# ---------------------------------------------------------
# YARDIMCI FONKSİYONLAR
# ---------------------------------------------------------

def choose_property_type():
    types = list(PROPERTY_TYPES.keys())
    weights = [PROPERTY_TYPES[item]["weight"] for item in types]

    return random.choices(types, weights=weights, k=1)[0]


def choose_area(property_type):
    if property_type == "Daire":
        return random.randint(55, 220)

    if property_type == "Müstakil Ev":
        return random.randint(100, 300)

    if property_type == "Villa":
        return random.randint(160, 400)

    if property_type == "Dükkan":
        return random.randint(40, 250)

    return random.randint(30, 180)


def calculate_price(neighborhood, property_type, area, listing_type):
    base_price_m2 = NEIGHBORHOODS[neighborhood]

    if property_type == "Dükkan":
        base_price_m2 *= 1.15
    elif property_type == "Ofis":
        base_price_m2 *= 1.05
    elif property_type == "Villa":
        base_price_m2 *= 1.10

    if listing_type == "Kiralık":
        # Aylık kira
        monthly_rent = (
            base_price_m2
            * area
            * random.uniform(0.0025, 0.0045)
        )

        return round(monthly_rent / 100) * 100

    # Satılık fiyat
    price = base_price_m2 * area

    price *= random.uniform(0.85, 1.20)

    return round(price / 1000) * 1000


def generate_listing(listing_number):
    neighborhood = random.choice(list(NEIGHBORHOODS.keys()))
    property_type = choose_property_type()
    listing_type = random.choice(LISTING_STATUS)

    area = choose_area(property_type)
    rooms = random.choice(PROPERTY_TYPES[property_type]["rooms"])

    price = calculate_price(
        neighborhood=neighborhood,
        property_type=property_type,
        area=area,
        listing_type=listing_type,
    )

    today = datetime.now()

    # İlanların bir kısmı yeni, bir kısmı uzun süredir aktif.
    listing_age_days = random.randint(1, 180)

    listing_date = today - timedelta(days=listing_age_days)

    # Son fiyat değişikliği bazen hiç yapılmamış olsun.
    if random.random() < 0.35:
        last_price_update = None
        previous_price = price
    else:
        update_days_ago = random.randint(1, min(listing_age_days, 90))

        last_price_update = today - timedelta(days=update_days_ago)

        # Fiyat değişiminin çoğu düşüş olsun.
        if random.random() < 0.70:
            previous_price = round(
                price * random.uniform(1.03, 1.15) / 1000
            ) * 1000
        else:
            previous_price = round(
                price * random.uniform(0.90, 0.98) / 1000
            ) * 1000

    status = "Aktif"

    return {
        "ilan_id": f"TRS-{listing_number:05d}",
        "portfoy_tipi": property_type,
        "ilan_turu": listing_type,
        "mahalle": neighborhood,
        "oda_sayisi": rooms,
        "metrekare": area,
        "fiyat": price,
        "onceki_fiyat": previous_price,
        "ilan_tarihi": listing_date.date(),
        "son_fiyat_guncelleme": (
            last_price_update.date()
            if last_price_update
            else None
        ),
        "durum": status,
    }


# ---------------------------------------------------------
# VERİ ÜRET
# ---------------------------------------------------------

def main():
    listings = [
        generate_listing(i)
        for i in range(1, NUMBER_OF_LISTINGS + 1)
    ]

    df = pd.DataFrame(listings)

    # Tarih kolonlarını standartlaştır.
    df["ilan_tarihi"] = pd.to_datetime(df["ilan_tarihi"])
    df["son_fiyat_guncelleme"] = pd.to_datetime(
        df["son_fiyat_guncelleme"]
    )

    # Fiyat / m²
    df["fiyat_m2"] = (
    df["fiyat"] / df["metrekare"]
).round(2)

    # İlan yaşı
    today = pd.Timestamp.today().normalize()

    df["ilan_yasi_gun"] = (
        today - df["ilan_tarihi"]
    ).dt.days

    # Fiyat değişim yüzdesi
    df["fiyat_degisimi_yuzde"] = (
        (df["fiyat"] - df["onceki_fiyat"])
        / df["onceki_fiyat"]
        * 100
    ).round(2)

    # Öncelik skoru
    df["portfoy_oncelik_skoru"] = calculate_priority_score(df)

    # CSV'ye yaz.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig",
    )

    print()
    print("✅ Veri başarıyla oluşturuldu.")
    print(f"📁 Dosya: {OUTPUT_FILE}")
    print(f"🏠 Portföy sayısı: {len(df)}")
    print()
    print("İlk 5 kayıt:")
    print(df.head().to_string(index=False))


# ---------------------------------------------------------
# ÖNCELİK SKORU
# ---------------------------------------------------------

def calculate_priority_score(df):
    score = pd.Series(0.0, index=df.index)

    # 1. İlan yaşı
    score += (
        df["ilan_yasi_gun"].clip(upper=120) / 120 * 40
    )

    # 2. Fiyat değişimi
    price_change = df["fiyat_degisimi_yuzde"]

    # Fiyatı düşen ilanlara daha yüksek öncelik
    score += (
        -price_change
    ).clip(lower=0, upper=30)

    # 3. Uzun süredir fiyatı değişmeyen ilanlar
    no_update = df["son_fiyat_guncelleme"].isna()

    score += no_update.astype(int) * 10

    # 0-100 arasında tut
    return score.clip(lower=0, upper=100).round(1)


if __name__ == "__main__":
    main()