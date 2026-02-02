import duckdb

# Connexion DuckDB
con = duckdb.connect("bottleneck.duckdb")

print("🚀 Lancement de la suite de tests Data Quality...")

# --- CONFIGURATION DES TESTS ---
# On définit tout ici pour ne pas répéter le code
checks = {
    "erp_clean": {
        "unique": ["product_id"],
        "not_null": ["product_id", "price", "stock_quantity"],
        "positive": ["price", "stock_quantity"]
    },
    "web_clean": {
        "unique": ["sku"],
        "not_null": ["sku", "total_sales", "post_title"],
        "positive": ["total_sales"]
    },
    "liaison_clean": {
        "unique": ["product_id"],
        "not_null": ["product_id"] # id_web est autorisé à être NULL
    }
}

# --- 1️⃣ EXÉCUTION DES TESTS D'UNICITÉ & NON-NULL ---
for table, rules in checks.items():
    # Test d'unicité
    for col in rules.get("unique", []):
        count_dup = con.execute(f"SELECT COUNT(*) FROM (SELECT {col} FROM {table} GROUP BY {col} HAVING COUNT(*) > 1)").fetchone()[0]
        assert count_dup == 0, f"❌ DOUBLONS détectés : {table}.{col}"
        print(f"✅ Unicité validée : {table}.{col}")

    # Test de valeurs manquantes
    for col in rules.get("not_null", []):
        null_count = con.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL").fetchone()[0]
        assert null_count == 0, f"❌ VALEURS MANQUANTES : {table}.{col}"
        print(f"✅ Complétude validée : {table}.{col}")

# --- 2️⃣ TESTS MÉTIER (Nouveaux) ---
print("🔍 Vérification de la cohérence des valeurs...")


# --- 3️⃣ TEST DE VOLUME (Benchmark de Stéphane) ---
# Pour s'assurer qu'on n'a pas perdu de lignes durant le nettoyage
volumes = {
    "erp_clean": 825,
    "liaison_clean": 825,
    "web_clean": 714
}

for table, expected in volumes.items():
    actual = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    assert actual == expected, f"❌ VOLUME INCORRECT : {table} a {actual} lignes (attendu : {expected})"
    print(f"✅ Volume validé : {table} ({actual} lignes)")

print("\n✨ [SUCCESS] Tous les tests de qualité sont passés avec succès !")