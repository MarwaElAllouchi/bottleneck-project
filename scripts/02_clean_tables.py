import duckdb

# Connexion DuckDB
con = duckdb.connect("bottleneck.duckdb")

print("🚀 Début nettoyage des tables...")

# --- Nettoyage ERP ---
con.execute("""
CREATE OR REPLACE TABLE erp_clean AS
SELECT DISTINCT 
    CAST(product_id AS INTEGER) AS product_id,
    TRY_CAST(REPLACE(CAST(price AS VARCHAR), ',', '.') AS DOUBLE) AS price,
    stock_quantity, 
    stock_status, 
    onsale_web
FROM erp 
WHERE product_id IS NOT NULL;
""")

# --- Nettoyage LIAISON ---
con.execute("""
CREATE OR REPLACE TABLE liaison_clean AS
SELECT DISTINCT 
    CAST(product_id AS INTEGER) AS product_id,
    id_web
FROM liaison 
WHERE product_id IS NOT NULL; -- id_web peut rester NULL
""")

# --- Nettoyage WEB ---
# Étape 1 : supprimer les lignes vides
con.execute("""
CREATE OR REPLACE TABLE web_cleaned_temp AS
SELECT * FROM web 
WHERE sku IS NOT NULL;
""")
count_web_cleaned=con.execute("SELECT COUNT(*) FROM web_cleaned_temp").fetchone()[0]
# Étape 2 : dédoublonnage et filtrage des produits
con.execute("""
CREATE OR REPLACE TABLE web_clean AS
SELECT DISTINCT 
    sku, 
    CAST(total_sales AS DOUBLE) AS total_sales, 
    post_title,
    post_type
FROM web_cleaned_temp 
WHERE post_type = 'product';
""")

# --- Affichage des volumes pour vérification ---
count_erp = con.execute("SELECT COUNT(*) FROM erp_clean").fetchone()[0]
count_web = con.execute("SELECT COUNT(*) FROM web_clean").fetchone()[0]
count_liaison = con.execute("SELECT COUNT(*) FROM liaison_clean").fetchone()[0]

print("✅ Tables nettoyées avec succès !")
print(f"📊 ERP clean : {count_erp} lignes")
print(f"📊 Web validé : Aprés Nettoyage ({count_web_cleaned}) et Dédoublonnage ({count_web}) lignes (Attendu: 714)")
print(f"📊 Liaison clean : {count_liaison} lignes")
