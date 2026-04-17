import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
import re

df = pd.read_csv("Play Store Data.csv")

df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")

df["Installs"] = df["Installs"].astype(str).str.replace(",", "", regex=False)
df["Installs"] = df["Installs"].str.replace("+", "", regex=False)
df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")

df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors="coerce")

def clean_size(size):
    if pd.isna(size):
        return None
    size = str(size).strip()
    if size == "Varies with device":
        return None
    if size.endswith("M"):
        try:
            return float(size.replace("M", ""))
        except:
            return None
    if size.endswith("k"):
        try:
            return float(size.replace("k", "")) / 1024
        except:
            return None
    return None

df["Size_MB"] = df["Size"].apply(clean_size)

df = df.dropna(subset=["App", "Category", "Rating", "Reviews", "Installs", "Last Updated", "Size_MB"])

# Rating >= 4.2
df = df[df["Rating"] >= 4.2]

# Reviews > 1000
df = df[df["Reviews"] > 1000]

# Size between 20 and 80 MB
df = df[(df["Size_MB"] >= 20) & (df["Size_MB"] <= 80)]

# Category starts with T or P
df = df[df["Category"].str.startswith(("T", "P"))]

# App name should not contain any number
df = df[~df["App"].str.contains(r"\d", regex=True, na=False)]

df["Month"] = df["Last Updated"].dt.to_period("M").astype(str)

grouped = (
    df.groupby(["Month", "Category"])["Installs"]
    .sum()
    .reset_index()
)

# Sort months properly
grouped["Month"] = pd.to_datetime(grouped["Month"])
grouped = grouped.sort_values("Month")

grouped["Cumulative_Installs"] = grouped.groupby("Category")["Installs"].cumsum()

grouped["Category"] = grouped["Category"].replace({
    "TRAVEL_AND_LOCAL": "Voyage et Local",
    "PRODUCTIVITY": "Productividad",
    "PHOTOGRAPHY": "写真"
})

monthly_total = (
    grouped.groupby("Month")["Installs"]
    .sum()
    .reset_index()
)

monthly_total["Growth"] = monthly_total["Installs"].pct_change()

highlight_months = monthly_total[monthly_total["Growth"] > 0.25]["Month"]

fig = px.area(
    grouped,
    x="Month",
    y="Cumulative_Installs",
    color="Category",
    title="Cumulative Installs Over Time by App Category"
)

# Highlight high-growth months
for month in highlight_months:
    fig.add_vrect(
        x0=month,
        x1=month,
        fillcolor="red",
        opacity=0.15,
        line_width=0
    )

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Cumulative Installs",
    template="plotly_white"
)

ist = pytz.timezone("Asia/Kolkata")
current_hour = datetime.now(ist).hour

if 16 <= current_hour < 18:
     fig.show()
 else:
     print("Task 6 chart should only be visible between 4 PM IST and 6 PM IST.")