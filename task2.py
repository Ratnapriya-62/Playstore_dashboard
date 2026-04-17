import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import pytz

df = pd.read_csv("Play Store Data.csv")

df["Installs"] = df["Installs"].astype(str).str.replace(",", "", regex=False)
df["Installs"] = df["Installs"].str.replace("+", "", regex=False)
df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")

df2 = df.dropna(subset=["Category", "Installs"]).copy()

df2 = df2[~df2["Category"].str.startswith(("A", "C", "G", "S"))]

# Installs > 1 million
df2 = df2[df2["Installs"] > 1000000]

top5 = (
    df2.groupby("Category")["Installs"]
    .sum()
    .nlargest(5)
    .index
)

df2 = df2[df2["Category"].isin(top5)]

countries = ["India", "United States", "Canada", "Germany", "Australia"]

df2["Country"] = np.random.choice(countries, size=len(df2))

map_data = (
    df2.groupby(["Country", "Category"])["Installs"]
    .sum()
    .reset_index()
)

fig = px.choropleth(
    map_data,
    locations="Country",
    locationmode="country names",
    color="Installs",
    hover_name="Category",
    title="Global Installs by Top 5 Categories"
)

ist = pytz.timezone("Asia/Kolkata")
current_hour = datetime.now(ist).hour

 if 18 <= current_hour < 20:
     fig.show()
 else:
     print("Chart only available between 6 PM and 8 PM IST")