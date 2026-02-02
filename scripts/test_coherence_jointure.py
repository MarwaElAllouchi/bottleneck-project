import duckdb

# Connexion DuckDB
con = duckdb.connect("bottleneck.duckdb")


print("🧪 Début des tests de cohérence..")

# 1️⃣ Tests de cohérence des jointures (après fusion, si nécessaire)
# Exemple : tous les produits de liaison_clean doivent exister dans erp_clean
join_test = con.execute("""
SELECT COUNT(*) 
FROM liaison_clean l
LEFT JOIN erp_clean e ON l.product_id = e.product_id
WHERE e.product_id IS NULL
""").fetchone()[0]
assert join_test == 0, "❌ Problème de cohérence dans les jointures"


# --- Test A : Nombre de lignes ---
fusion_df = con.execute("SELECT * FROM final_data").df()
nb_lignes = len(fusion_df)
assert nb_lignes == 714, f"❌ Erreur jointure : {nb_lignes} lignes au lieu de 714"

# --- Test C : Prix négatifs ou nuls ---
negative_prices = fusion_df[fusion_df['price'] <= 0]
assert len(negative_prices) == 0, "❌ Des prix négatifs ou nuls détectés"

print("✅ Tous les tests de coherences sont validés !")
print(f"   - Nombre de fusion validé : {nb_lignes}")