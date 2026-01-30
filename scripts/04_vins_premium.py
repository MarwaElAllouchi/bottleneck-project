import duckdb
import pandas as pd
import os

# Connexion à la base de données DuckDB
con = duckdb.connect("bottleneck.duckdb")

print("📊 Début de l'analyse statistique (Z-score)...")

# --- 1. Récupération des données fusionnées ---
df = con.execute("SELECT * FROM final_data").df()

# --- 2. Calcul du Z-score ---
# Formule : z = (prix - moyenne) / écart-type
mean_price = df['price'].mean()
std_price = df['price'].std()

df['z_score'] = (df['price'] - mean_price) / std_price

# --- 3. Identification des segments ---
# Stéphane définit un vin premium par un z-score > 2
vins_premium = df[df['z_score'] > 2].copy()
vins_ordinaires = df[df['z_score'] <= 2].copy()

# --- 4. Tests Nominaux (Qualité de l'analyse) ---

# Test A : Nombre de vins premium (Doit être de 30)
nb_premium = len(vins_premium)
assert nb_premium == 30, f"❌ Erreur Statistique : {nb_premium} vins premium détectés au lieu de 30"

# Test B : Cohérence logique
# Un vin premium doit avoir un prix strictement supérieur à la moyenne
assert vins_premium['price'].min() > mean_price, "❌ Erreur : Un vin premium a un prix inférieur à la moyenne"

# Test C : Intégrité des données
# On vérifie que la somme des deux listes égale le total initial (714)
total_check = len(vins_premium) + len(vins_ordinaires)
assert total_check == 714, f"❌ Erreur d'intégrité : total de {total_check} au lieu de 714"

print(f"✅ Tests statistiques validés !")
print(f"   - Prix moyen : {mean_price:.2f} €")
print(f"   - Vins Premium détectés : {nb_premium}")
print(f"   - Vins Ordinaires détectés : {len(vins_ordinaires)}")

# --- 5. Exports des fichiers pour Maria et Laure ---

os.makedirs('exports', exist_ok=True)

# Export des vins premium pour Laure
vins_premium.to_csv('exports/vins_premium.csv', index=False)

# Export des vins ordinaires pour Maria
vins_ordinaires.to_csv('exports/vins_ordinaires.csv', index=False)

print("📂 Fichiers CSV exportés avec succès dans le dossier 'exports/'.")