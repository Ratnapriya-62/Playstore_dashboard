import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz

st.set_page_config(page_title="Play Store Dashboard", layout="wide")

st.title("📊 Play Store Data Analysis Dashboard")

df = pd.read_csv("Play Store Data.csv")

try:
    reviews = pd.read_csv("User Reviews.csv")
except:
    reviews = None

df["Installs"] = df["Installs"].astype(str).str.replace(",", "", regex=False)
df["Installs"] = df["Installs"].str.replace("+", "", regex=False)
df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")

df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors="coerce")

def clean_size(size):
    if pd.isna(size):
        return None
    size = str(size)
    if size.endswith("M"):
        return float(size.replace("M", ""))
    if size.endswith("k"):
        return float(size.replace("k", "")) / 1024
    return None

df["Size_MB"] = df["Size"].apply(clean_size)

ist = pytz.timezone("Asia/Kolkata")
current_hour = datetime.now(ist).hour

st.subheader("Task 1: Grouped Bar Chart")

if 15 <= current_hour < 17:
    t1 = df.dropna(subset=["Category", "Rating", "Reviews", "Installs", "Size_MB", "Last Updated"])
    t1 = t1[(t1["Rating"] >= 4) & (t1["Size_MB"] >= 10) & (t1["Last Updated"].dt.month == 1)]

    top10 = t1.groupby("Category")["Installs"].sum().nlargest(10).index
    t1 = t1[t1["Category"].isin(top10)]

    grouped = t1.groupby("Category").agg(
        Avg_Rating=("Rating", "mean"),
        Total_Reviews=("Reviews", "sum")
    ).reset_index()

    fig1 = go.Figure()
    fig1.add_bar(x=grouped["Category"], y=grouped["Avg_Rating"], name="Rating")
    fig1.add_bar(x=grouped["Category"], y=grouped["Total_Reviews"], name="Reviews")

    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("Available between 3 PM – 5 PM")

st.subheader("Task 2: Choropleth Map")

if 18 <= current_hour < 20:
    t2 = df.dropna(subset=["Category", "Installs"])
    t2 = t2[~t2["Category"].str.startswith(("A", "C", "G", "S"))]
    t2 = t2[t2["Installs"] > 1000000]

    top5 = t2.groupby("Category")["Installs"].sum().nlargest(5).index
    t2 = t2[t2["Category"].isin(top5)]

    countries = ["India", "USA", "UK", "Germany", "Canada"]
    t2["Country"] = np.random.choice(countries, len(t2))

    map_data = t2.groupby(["Country", "Category"])["Installs"].sum().reset_index()

    fig2 = px.choropleth(
        map_data,
        locations="Country",
        locationmode="country names",
        color="Installs",
        hover_name="Category"
    )

    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Available between 6 PM – 8 PM")

st.subheader("Task 3: Dual Axis Chart")

if 13 <= current_hour < 14:
    t3 = df.dropna(subset=["Installs", "Size_MB"])

    t3["Revenue"] = t3["Installs"] * t3["Price"]

    t3 = t3[(t3["Installs"] > 10000) &
            (t3["Revenue"] > 10000) &
            (t3["Size_MB"] > 15) &
            (t3["Content Rating"] == "Everyone")]

    t3 = t3[t3["App"].str.len() <= 30]

    top3 = t3.groupby("Category")["Installs"].sum().nlargest(3).index
    t3 = t3[t3["Category"].isin(top3)]

    grouped = t3.groupby("Type").agg(
        Installs=("Installs", "mean"),
        Revenue=("Revenue", "mean")
    ).reset_index()

    fig3 = go.Figure()
    fig3.add_bar(x=grouped["Type"], y=grouped["Installs"], name="Installs")
    fig3.add_scatter(x=grouped["Type"], y=grouped["Revenue"], yaxis="y2", name="Revenue")

    fig3.update_layout(yaxis2=dict(overlaying='y', side='right'))

    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Available between 1 PM – 2 PM")

st.subheader("Task 4: Time Series")

if 18 <= current_hour < 21:
    t4 = df.dropna(subset=["Installs", "Reviews", "Last Updated"])
    t4 = t4[t4["Reviews"] > 500]
    t4 = t4[t4["Category"].str.startswith(("E", "C", "B"))]
    t4["Month"] = t4["Last Updated"].dt.to_period("M").astype(str)

    grouped = t4.groupby(["Month", "Category"])["Installs"].sum().reset_index()

    fig4 = px.line(grouped, x="Month", y="Installs", color="Category")

    st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("Available between 6 PM – 9 PM")


st.subheader("Task 5: Bubble Chart")

if 17 <= current_hour < 19:
    t5 = df.dropna(subset=["Rating", "Reviews", "Installs", "Size_MB"])
    t5 = t5[(t5["Rating"] > 3.5) &
            (t5["Reviews"] > 500) &
            (t5["Installs"] > 50000)]

    fig5 = px.scatter(
        t5,
        x="Size_MB",
        y="Rating",
        size="Installs",
        color="Category"
    )

    st.plotly_chart(fig5, use_container_width=True)
else:
    st.info("Available between 5 PM – 7 PM")

st.subheader("Task 6: Stacked Area Chart")

if 16 <= current_hour < 18:
    t6 = df.dropna(subset=["Installs", "Last Updated", "Size_MB"])

    t6 = t6[(t6["Rating"] >= 4.2) &
            (t6["Reviews"] > 1000) &
            (t6["Size_MB"].between(20, 80))]

    t6 = t6[t6["Category"].str.startswith(("T", "P"))]

    t6["Month"] = t6["Last Updated"].dt.to_period("M").astype(str)

    grouped = t6.groupby(["Month", "Category"])["Installs"].sum().reset_index()

    fig6 = px.area(grouped, x="Month", y="Installs", color="Category")

    st.plotly_chart(fig6, use_container_width=True)
else:
    st.info("Available between 4 PM – 6 PM")