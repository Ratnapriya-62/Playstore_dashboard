import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

#loding_dataset
df = pd.read_csv("Play Store Data.csv")

#cleanning important columns
df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
#converting rating into numeric
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

df["Installs"] = df["Installs"].astype(str).str.replace(",","", regex=False)
df["Installs"] = df["Installs"].str.replace("+","",regex=False)
df["Installs"] = pd.to_numeric(df["Installs"],errors="coerce")

df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors="coerce")

#function to clean the size 
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
            return float(size.replace("k", ""))
        except: 
            return None

df["Size_MB"] = df["Size"].apply(clean_size)
#drop rows with missing required value
df = df.dropna(subset=["Category", "Rating",])
#apply row-level filters
#Rating >=4.0
df = df[df["Rating"] >=4.0]
#Filter for size
df = df[df["Size_MB"] >= 10]
#Month filter
df = df[df["Last Updated"].dt.month ==1]

#Finding the top 10 categories
top_10_categories = (
    df.groupby("Category")["Installs"]
    .sum()
    .nlargest(10)
    .index
)
df_top = df[df["Category"].isin(top_10_categories)].copy()

grouped = (
    df_top.groupby("Category")
    .agg(
        Average_Rating=("Rating","mean"),
        Total_Reviews=("Reviews", "sum")
    )
    .reset_index()
)
grouped = grouped[grouped["Average_Rating"] >= 4.0]

grouped = grouped.sort_values(by="Total_Reviews", ascending=False)

print("\nFinal grouped data:\n")
print(grouped)

fig = go.Figure()

fig.add_trace(go.Bar(
    x=grouped["Category"],
    y=grouped["Average_Rating"],
    name="Average Rating"
))

fig.update_layout(
    title="Top 10 App Categories: Average Rating Vs Total Reviews",
    xaxis_title= "Category",
    yaxis_title="Values",
    barmode="group",
    xaxis_tickangle= -45,
    template="plotly_white"
)

ist = pytz.timezone("Asia/Kolkata")
current_time = datetime.now(ist)
current_hour = current_time.hour

print("\nCurrent IST hour:", current_hour)

if 15<= current_hour <17:
    fig.show()
else:
    print("Task 1 chart should be visible between 3P.M. IST and 5 P.M. IST.")