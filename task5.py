import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

apps = pd.read_csv("Play Store Data.csv")

try:
    reviews = pd.read_csv("User Reviews.csv")
except:
    reviews = None

apps["Installs"] = apps["Installs"].astype(str).str.replace(",", "", regex=False)
apps["Installs"] = apps["Installs"].str.replace("+", "", regex=False)
apps["Installs"] = pd.to_numeric(apps["Installs"], errors="coerce")

apps["Reviews"] = pd.to_numeric(apps["Reviews"], errors="coerce")
apps["Rating"] = pd.to_numeric(apps["Rating"], errors="coerce")

# Size clean
def clean_size(size):
    if pd.isna(size):
        return None
    size = str(size)
    if size.endswith("M"):
        return float(size.replace("M", ""))
    if size.endswith("k"):
        return float(size.replace("k", "")) / 1024
    return None

apps["Size_MB"] = apps["Size"].apply(clean_size)

apps = apps.dropna(subset=["Rating", "Reviews", "Installs", "Size_MB"])

apps = apps[apps["Rating"] > 3.5]
apps = apps[apps["Reviews"] > 500]
apps = apps[apps["Installs"] > 50000]

# App name filter
apps = apps[~apps["App"].str.contains("S", case=False, na=False)]

# Category filter
allowed = ["GAME", "BEAUTY", "BUSINESS", "COMICS", "COMMUNICATION",
           "DATING", "ENTERTAINMENT", "SOCIAL", "EVENTS"]

apps = apps[apps["Category"].str.upper().isin(allowed)]

if reviews is not None:
    reviews = reviews.dropna(subset=["App", "Sentiment_Subjectivity"])
    reviews = reviews.groupby("App")["Sentiment_Subjectivity"].mean().reset_index()

    apps = apps.merge(reviews, on="App", how="left")

    apps = apps[apps["Sentiment_Subjectivity"] > 0.5]

apps["Category"] = apps["Category"].replace({
    "BEAUTY": "सौंदर्य",
    "BUSINESS": "வணிகம்",
    "DATING": "Dating (German)"
})

fig = px.scatter(
    apps,
    x="Size_MB",
    y="Rating",
    size="Installs",
    color="Category",
    title="App Size vs Rating (Bubble Chart)",
    hover_name="App"
)

# Highlight GAME in pink
fig.update_traces(marker=dict(color="pink"), selector=dict(name="GAME"))

ist = pytz.timezone("Asia/Kolkata")
hour = datetime.now(ist).hour
if 17 <= hour < 19:
     fig.show()
 else:
     print("Chart only available between 5 PM and 7 PM IST")