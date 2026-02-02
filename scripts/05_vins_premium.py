import duckdb
import pandas as pd

con = duckdb.connect("bottleneck.duckdb")

print("📊 Calcul du Z-score des prix des vins...")

# Charger les données avec prix
df = con.execute("SELECT * FROM final_data").df()

# Calcul Z-score
mean_price = df['price'].mean()
std_price = df['price'].std()
df['z_score'] = (df['price'] - mean_price) / std_price

# Créer vins premium / ordinaires
vins_premium = df[df['z_score'] > 2].copy()
vins_ordinaires = df[df['z_score'] <= 2].copy()

# Sauvegarde intermédiaire dans DuckDB pour test/export
con.execute("CREATE OR REPLACE TABLE vins_premium_data AS SELECT * FROM vins_premium")
con.execute("CREATE OR REPLACE TABLE vins_ordinaires_data AS SELECT * FROM vins_ordinaires")

print(f"✅ Z-score calculé : {len(vins_premium)} vins premium et {len(vins_ordinaires)} vins ordinaires")
