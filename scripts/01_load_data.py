import duckdb
import pandas as pd

# Connexion à DuckDB
con = duckdb.connect('bottleneck.duckdb')

# Paramètres génériques
FILES = {
    'erp': 'data/Fichier_erp.xlsx',
    'web': 'data/Fichier_web.xlsx',
    'liaison': 'data/fichier_liaison.xlsx'
}

# Lire Excel avec pandas et injecter dans DuckDB
for table_name, file_path in FILES.items():
    df = pd.read_excel(file_path)
    con.register(table_name + "_df", df)  # enregistre le DataFrame temporaire
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM {table_name}_df;")

print("✅ Tables brutes chargées avec succès via pandas !")
