import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

df = pd.read_csv("Play Store Data.csv")

df["Installs"] = df["Installs"].astype(str).str.replace(",", "", regex=False)
df["Installs"] = df["Installs"].str.replace("+", "", regex=False)
df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")

# Reviews clean
df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")

# Date clean
df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors="coerce")
df = df.dropna(subset=["Installs", "Reviews", "Last Updated", "Category", "App"])
df = df[df["Reviews"] > 500]
# Category starts with E, C, B
df = df[df["Category"].str.startswith(("E", "C", "B"))]
# App name filters
df = df[~df["App"].str.lower().str.startswith(("x", "y", "z"))]
df = df[~df["App"].str.contains("S", case=False, na=False)]
df["Category"] = df["Category"].replace({
    "Beauty": "सौंदर्य",
    "Business": "வணிகம்",
    "Dating": "Dating (German)"
})

df["Month"] = df["Last Updated"].dt.to_period("M").astype(str)
grouped = df.groupby(["Month", "Category"])["Installs"].sum().reset_index()
grouped["Growth"] = grouped.groupby("Category")["Installs"].pct_change()
fig = px.line(
    grouped,
    x="Month",
    y="Installs",
    color="Category",
    title="Installs Trend Over Time"
)

high_growth = grouped[grouped["Growth"] > 0.2]

fig.add_scatter(
    x=high_growth["Month"],
    y=high_growth["Installs"],
    mode="markers",
    marker=dict(size=10, color="red"),
    name="High Growth (>20%)"
)

ist = pytz.timezone("Asia/Kolkata")
hour = datetime.now(ist).hour
if 18 <= hour < 21:
     fig.show()
 else:
     print("Chart only available between 6 PM and 9 PM IST")