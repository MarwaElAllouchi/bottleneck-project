import duckdb
import pandas as pd

con = duckdb.connect("bottleneck.duckdb")

print("💰 Calcul du chiffre d'affaires par produit et global...")

df = con.execute("SELECT * FROM final_data").df()

# Calcul CA par produit
df["ca_produit"] = df["price"] * df["total_sales"]

# Sauvegarde intermédiaire
con.execute("CREATE OR REPLACE TABLE ca_results AS SELECT * FROM df")

ca_global = df["ca_produit"].sum()
print(f"✅ CA calculé : {ca_global:,.2f} €")
