import duckdb
import pandas as pd
import os

# Connexion DuckDB
con = duckdb.connect("bottleneck.duckdb")

print("📊 Début de la fusion ")
# --- 1. Jointure des données ---
# On utilise INNER JOIN car on ne veut que les produits qui ont une correspondance web complète
# (liaison + infos web) pour calculer le CA.
fusion_query = """
SELECT 
    e.product_id, 
    w.sku, 
    w.post_title, 
    e.price, 
    w.total_sales
    FROM erp_clean e
INNER JOIN liaison_clean l ON e.product_id = l.product_id
INNER JOIN web_clean w ON l.id_web = w.sku
"""

fusion_df = con.execute(fusion_query).df()

# Sauvegarde dans DuckDB pour le script suivant
con.execute("CREATE OR REPLACE TABLE final_data AS SELECT * FROM fusion_df")

print(f"✅ Fusion terminée : {len(fusion_df)} lignes")
