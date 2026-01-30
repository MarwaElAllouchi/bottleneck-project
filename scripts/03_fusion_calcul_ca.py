import duckdb
import pandas as pd
import os

# Connexion DuckDB
con = duckdb.connect("bottleneck.duckdb")

print("📊 Début de la fusion et des calculs financiers...")

# --- 1. Jointure des données ---
# On utilise INNER JOIN car on ne veut que les produits qui ont une correspondance web complète
# (liaison + infos web) pour calculer le CA.
fusion_query = """
SELECT 
    e.product_id, 
    w.sku, 
    w.post_title, 
    e.price, 
    w.total_sales, 
    (e.price * w.total_sales) AS ca_produit
FROM erp_clean e
INNER JOIN liaison_clean l ON e.product_id = l.product_id
INNER JOIN web_clean w ON l.id_web = w.sku
"""

fusion_df = con.execute(fusion_query).df()

# --- 2. Tests de cohérence demandés par Laurent ---

# Test A : Nombre de lignes fusionnées (Doit être de 714)
nb_lignes = len(fusion_df)
assert nb_lignes == 714, f"❌ Erreur de jointure : {nb_lignes} lignes au lieu de 714"

# Test B : Cohérence du Chiffre d'Affaires total
ca_total = fusion_df['ca_produit'].sum()
expected_ca = 70568.60
# On tolère une micro-marge d'erreur de 0.01 pour les arrondis flottants
assert abs(ca_total - expected_ca) < 0.01, f"❌ Erreur CA Total : {ca_total}€ au lieu de {expected_ca}€"

# Test C : Absence de prix aberrants ou négatifs
negative_prices = fusion_df[fusion_df['price'] <= 0]
assert len(negative_prices) == 0, "❌ Erreur : Des prix négatifs ou nuls ont été détectés"

print(f"✅ Tests financiers validés !")
print(f"   - Nombre de produits réconciliés : {nb_lignes}")
print(f"   - Chiffre d'Affaires global : {ca_total:,.2f} €")

# --- 3. Sauvegarde et Export ---

# Création du dossier exports s'il n'existe pas
os.makedirs('exports', exist_ok=True)

# Export Excel pour les responsables produits
fusion_df.to_excel('exports/rapport_ca_final.xlsx', index=False)

# On enregistre la table finale dans DuckDB pour le script suivant (Z-score)
con.execute("CREATE OR REPLACE TABLE final_data AS SELECT * FROM fusion_df")

print("📂 Rapport exporté ")

