import duckdb
import os

con = duckdb.connect("bottleneck.duckdb")

print("🧪 Tests statistiques et export final...")

# --- Recharger les DataFrames depuis DuckDB ---
vins_premium = con.execute("SELECT * FROM vins_premium_data").df()
vins_ordinaires = con.execute("SELECT * FROM vins_ordinaires_data").df()
ca_df = con.execute("SELECT * FROM ca_results").df()  # CA par produit

# --- Tests Z-score ---
# Test A : nombre de vins premium
nb_premium = len(vins_premium)
assert nb_premium == 30, f"❌ {nb_premium} vins premium détectés au lieu de 30"

# Test B : cohérence logique
mean_price = (vins_premium['price'].mean() + vins_ordinaires['price'].mean()) / 2
assert vins_premium['price'].min() > mean_price, "❌ Un vin premium a un prix inférieur à la moyenne"

# Test C : intégrité
total_check = len(vins_premium) + len(vins_ordinaires)
assert total_check == 714, f"❌ Total incorrect : {total_check} au lieu de 714"

print(f"✅ Tests statistiques validés !")
print(f"   - Vins Premium : {nb_premium}")
print(f"   - Vins Ordinaires : {len(vins_ordinaires)}")

# --- Export final uniquement après validation ---
os.makedirs('exports', exist_ok=True)
# Export Excel pour les responsables produits

vins_premium.to_csv('exports/vins_premium.csv', index=False)
vins_ordinaires.to_csv('exports/vins_ordinaires.csv', index=False)
ca_df.to_excel('exports/ca_par_produit.xlsx', index=False)  # <-- ajouté

print("📂 Exports terminés dans 'exports/'")

