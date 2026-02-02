import duckdb

con = duckdb.connect("bottleneck.duckdb")

print("🧪 Lancement des tests de cohérence du CA...")

df = con.execute("SELECT * FROM ca_results").df()

# Test 1 : nombre de produits
nb_lignes = len(df)
assert nb_lignes == 714, f"❌ Nombre de lignes incorrect : {nb_lignes} au lieu de 714"

# Test 2 : CA global
ca_global = df["ca_produit"].sum()
expected_ca = 70568.60
assert abs(ca_global - expected_ca) < 0.01, f"❌ CA global incorrect : {ca_global}€ au lieu de {expected_ca}€"

# Test 3 : pas de CA négatif
assert (df["ca_produit"] >= 0).all(), "❌ CA négatif détecté"

print("✅ Tous les tests du CA sont validés")
print(f"   - Nombre de produits : {nb_lignes}")
print(f"   - CA global : {ca_global:,.2f} €")
