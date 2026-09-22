# -*- coding: utf-8 -*-
"""
Génère 3 jeux de données volontairement imparfaits pour s'entraîner à la
collecte / nettoyage / stockage (Jours 1-3) et au monitoring de drift (Jour 9).

Sortie dans /home/claude/datasets/output/ :
  1. ecommerce_transactions_raw.csv
  2. customers_raw.csv
  3. reference_features.csv + production_week_features.csv (paire de drift)
"""
import numpy as np
import pandas as pd
from faker import Faker
import random
import os

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake = Faker("fr_FR")
Faker.seed(SEED)

OUT = "/home/claude/datasets/output"
os.makedirs(OUT, exist_ok=True)

# =====================================================================
# 1. ecommerce_transactions_raw.csv
# =====================================================================
N_TX = 3000

categories_clean = ["Electronique", "Mode", "Maison", "Sport", "Beaute", "Livres"]
# variantes sales volontaires d'une même catégorie
category_variants = {
    "Electronique": ["Electronique", "electronique ", "ELECTRONIQUE", "Électronique", "Electroniqe", "Ã‰lectronique"],
    "Mode": ["Mode", " mode", "MODE", "Modes"],
    "Maison": ["Maison", "maison", "MAISON ", "Maisons"],
    "Sport": ["Sport", "sport", "SPORT", "Sports"],
    "Beaute": ["Beaute", "beauté", "BEAUTE", "Beauté "],
    "Livres": ["Livres", "livres", "LIVRES", "Livre"],
}

country_variants = {
    "France": ["France", "FR", "fr", "FRANCE", "Francia"],
    "Belgique": ["Belgique", "BE", "be", "BELGIQUE"],
    "Suisse": ["Suisse", "CH", "ch", "SUISSE"],
    "Etats-Unis": ["Etats-Unis", "USA", "US", "United States", "États-Unis"],
    "Allemagne": ["Allemagne", "DE", "de", "GERMANY"],
}

payment_methods = ["carte_bancaire", "paypal", "virement", "cheque"]
null_like = ["", "N/A", "n/a", "null", "NULL", "-", "unknown", "?", "-999", None]

date_formats = [
    lambda d: d.strftime("%Y-%m-%d"),
    lambda d: d.strftime("%d/%m/%Y"),
    lambda d: d.strftime("%m-%d-%Y"),
    lambda d: d.strftime("%d-%b-%Y"),      # 03-Mar-2024
    lambda d: d.strftime("%Y/%m/%d %H:%M"),
]

rows = []
base_ids = list(range(100000, 100000 + int(N_TX * 0.95)))  # génère moins d'IDs uniques que de lignes -> doublons
for i in range(N_TX):
    tx_id = random.choice(base_ids) if random.random() < 0.06 else base_ids[i % len(base_ids)]
    cust_id = random.randint(5000, 5800)
    cat_key = random.choice(categories_clean)
    category = random.choice(category_variants[cat_key])

    # montant : parfois propre (float), parfois string sale, parfois aberrant
    base_amount = round(np.random.lognormal(mean=3.2, sigma=0.9), 2)
    r = random.random()
    if r < 0.05:
        amount = None  # valeur manquante réelle
    elif r < 0.10:
        amount = random.choice(null_like)  # valeur manquante déguisée
    elif r < 0.14:
        amount = f"{base_amount}€".replace(".", ",")     # "45,20€"
    elif r < 0.18:
        amount = f"${base_amount}"                        # "$45.20"
    elif r < 0.21:
        amount = -abs(base_amount)                        # montant négatif suspect
    elif r < 0.23:
        amount = round(base_amount * 500, 2)               # outlier extrême
    else:
        amount = base_amount

    country_key = random.choice(list(country_variants.keys()))
    country = random.choice(country_variants[country_key])

    payment = random.choice(payment_methods)
    if random.random() < 0.04:
        payment = random.choice(null_like)

    status = random.choice(["completed", "refunded", "pending", "failed", "Completed", "COMPLETED "])

    d = fake.date_time_between(start_date="-18M", end_date="now")
    date_fmt = random.choice(date_formats)
    tx_date = date_fmt(d)
    if random.random() < 0.03:
        tx_date = random.choice(null_like)

    # bruit d'encodage occasionnel sur le pays
    if random.random() < 0.02 and "é" in country.lower():
        country = country.encode("latin-1", errors="ignore").decode("utf-8", errors="ignore") or country

    rows.append({
        "transaction_id": tx_id,
        "customer_id": cust_id if random.random() > 0.02 else None,
        "product_category": category,
        "amount": amount,
        "currency": random.choice(["EUR", "eur", "USD", None]) if random.random() < 0.3 else "EUR",
        "transaction_date": tx_date,
        "country": country,
        "payment_method": payment,
        "status": status,
    })

df_tx = pd.DataFrame(rows)
# injecter quelques lignes 100% dupliquées
dup_rows = df_tx.sample(int(N_TX * 0.03), random_state=SEED)
df_tx = pd.concat([df_tx, dup_rows], ignore_index=True)
df_tx = df_tx.sample(frac=1, random_state=SEED).reset_index(drop=True)
df_tx.to_csv(os.path.join(OUT, "ecommerce_transactions_raw.csv"), index=False)

# =====================================================================
# 2. customers_raw.csv
# =====================================================================
N_CUST = 1500

loyalty_tiers = ["bronze", "argent", "or", "platine"]

def messy_phone():
    r = random.random()
    n = fake.msisdn()[-9:]
    if r < 0.2:
        return f"+33{n}"
    elif r < 0.4:
        return f"0033{n}"
    elif r < 0.6:
        return f"0{n[:9]}".replace(n[:9], "0" + n[1:])
    elif r < 0.75:
        return f"{n[0:2]}.{n[2:4]}.{n[4:6]}.{n[6:8]}.{n[8:9]}0"
    else:
        return random.choice(null_like)

def messy_email(name):
    base = name.lower().replace(" ", ".").replace("'", "")
    r = random.random()
    if r < 0.08:
        return base + "gmail.com"          # arobase manquant
    elif r < 0.14:
        return base + "@ gmail.com"        # espace parasite
    elif r < 0.20:
        return random.choice(null_like)
    else:
        return base + "@" + random.choice(["gmail.com", "yahoo.fr", "outlook.com", "hotmail.fr"])

rows2 = []
names_pool = []
for i in range(N_CUST):
    cust_id = 5000 + i
    name = fake.name()
    names_pool.append(name)

    birth = fake.date_of_birth(minimum_age=16, maximum_age=90)
    r = random.random()
    if r < 0.03:
        birth_str = "2031-01-15"          # date de naissance dans le futur
    elif r < 0.06:
        birth_str = "1899-05-20"          # âge absurde (125+ ans)
    else:
        birth_str = birth.strftime(random.choice(["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]))

    country_key = random.choice(list(country_variants.keys()))
    country = random.choice(country_variants[country_key])

    tier = random.choice(loyalty_tiers)
    if random.random() < 0.10:
        tier = random.choice(null_like + ["VIP", "gold", "GOLD"])  # catégories hors référentiel

    rows2.append({
        "customer_id": cust_id,
        "full_name": name if random.random() > 0.02 else f"  {name.upper()}  ",
        "email": messy_email(name),
        "phone": messy_phone(),
        "birth_date": birth_str,
        "country": country,
        "signup_date": fake.date_between(start_date="-5y", end_date="today").strftime(
            random.choice(["%Y-%m-%d", "%d/%m/%Y"])),
        "loyalty_tier": tier,
    })

# injecter des quasi-doublons (même personne, nom légèrement différent / re-signup)
for _ in range(int(N_CUST * 0.05)):
    src = random.choice(rows2).copy()
    variant_name = src["full_name"].strip()
    variant_name = variant_name.replace("é", "e").replace("è", "e")
    if random.random() < 0.5:
        variant_name = variant_name + " "
    src["customer_id"] = max(r["customer_id"] for r in rows2) + 1
    src["full_name"] = variant_name
    rows2.append(src)

df_cust = pd.DataFrame(rows2)
df_cust.to_csv(os.path.join(OUT, "customers_raw.csv"), index=False)

# =====================================================================
# 3. Paire de drift : reference_features.csv / production_week_features.csv
#    (pour Feast / Evidently — Jours 2 et 9)
# =====================================================================
N_FEAT = 2000

def make_features(n, drift=False, week_label="ref"):
    customer_id = np.arange(6000, 6000 + n)
    avg_basket_30d = np.random.gamma(shape=2.0, scale=25 if not drift else 40, size=n)  # drift = panier moyen qui gonfle
    recency_days = np.random.exponential(scale=15, size=n)
    nb_orders_90d = np.random.poisson(lam=3 if not drift else 1.2, size=n)  # drift = moins de commandes (désengagement)

    cats = ["Electronique", "Mode", "Maison", "Sport", "Beaute", "Livres"]
    if drift:
        cats = cats + ["Jardin"]  # nouvelle catégorie jamais vue en référence -> unseen category en prod
        weights = [0.15, 0.15, 0.15, 0.1, 0.1, 0.1, 0.25]
    else:
        weights = [0.25, 0.2, 0.2, 0.15, 0.1, 0.1]
    category_pref = np.random.choice(cats, size=n, p=weights)

    df = pd.DataFrame({
        "customer_id": customer_id,
        "avg_basket_30d": np.round(avg_basket_30d, 2),
        "recency_days": np.round(recency_days, 1),
        "nb_orders_90d": nb_orders_90d,
        "category_pref": category_pref,
        "week": week_label,
    })

    # taux de valeurs manquantes plus élevé en prod (dérive de collecte)
    missing_rate = 0.02 if not drift else 0.12
    mask = np.random.random(n) < missing_rate
    df.loc[mask, "recency_days"] = np.nan

    return df

df_ref = make_features(N_FEAT, drift=False, week_label="reference_S-8_a_S-1")
df_prod = make_features(N_FEAT, drift=True, week_label="production_semaine_courante")

df_ref.to_csv(os.path.join(OUT, "reference_features.csv"), index=False)
df_prod.to_csv(os.path.join(OUT, "production_week_features.csv"), index=False)

print("Fichiers générés :")
for f in sorted(os.listdir(OUT)):
    path = os.path.join(OUT, f)
    print(f" - {f} ({os.path.getsize(path)/1024:.1f} Ko, {sum(1 for _ in open(path, encoding='utf-8', errors='ignore'))-1} lignes)")
