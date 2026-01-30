import duckdb

# Connexion DuckDB
con = duckdb.connect("bottleneck.duckdb")

print("🚀 Début des tests de qualité...")

# 1️⃣ Tests d’absence de doublons
for table, col in [("erp_clean", "product_id"), ("web_clean", "sku"), ("liaison_clean", "product_id")]:
    dup_check = con.execute(f"""
        SELECT {col} FROM {table} 
        GROUP BY {col} 
        HAVING COUNT(*) > 1
    """).fetchone()
    assert dup_check is None, f"❌ Doublons détectés dans {table}.{col}"

# 2️⃣ Tests d’absence de valeurs manquantes
tables_cols = {
    "erp_clean": ["product_id", "price", "stock_quantity", "stock_status"],
    "web_clean": ["sku", "total_sales", "post_title"],
    "liaison_clean": ["product_id"]  # id_web peut rester NULL
}
for table, cols in tables_cols.items():
    for col in cols:
        null_count = con.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL").fetchone()[0]
        assert null_count == 0, f"❌ Valeurs manquantes détectées dans {table}.{col}"

# 3️⃣ Tests de cohérence des jointures (après fusion, si nécessaire)
# Exemple : tous les produits de liaison_clean doivent exister dans erp_clean
join_test = con.execute("""
SELECT COUNT(*) 
FROM liaison_clean l
LEFT JOIN erp_clean e ON l.product_id = e.product_id
WHERE e.product_id IS NULL
""").fetchone()[0]
assert join_test == 0, "❌ Problème de cohérence dans les jointures"

print("✅ Tous les tests passés avec succès !")
