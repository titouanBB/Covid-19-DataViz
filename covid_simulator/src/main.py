import streamlit as st
import pandas as pd
import plotly.express as px

# === Charger les données Johns Hopkins ===
url_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/" \
                "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
url_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/" \
             "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

df_confirmed = pd.read_csv(url_confirmed)
df_deaths = pd.read_csv(url_deaths)

# On prend la dernière date disponible
latest_date = df_confirmed.columns[-1]

# Sommes par pays
confirmed_latest = df_confirmed.groupby("Country/Region")[latest_date].sum().reset_index()
deaths_latest = df_deaths.groupby("Country/Region")[latest_date].sum().reset_index()

# Merge cas + morts
data_latest = confirmed_latest.merge(deaths_latest, on="Country/Region", suffixes=("_confirmed", "_deaths"))

# === Sidebar navigation ===
st.sidebar.title("COVID-19 Dashboard")
page = st.sidebar.radio("Aller à :", ["Courbes globales", "Carte interactive"])

# === Page 1 : courbes ===
if page == "Courbes globales":
    st.title("📈 Évolution COVID-19 par pays")

    countries = st.multiselect("Choisis les pays :", ["France", "Germany", "Italy", "United Kingdom", "US"], default=["France","US"])

    df_grouped = df_confirmed.drop(columns=["Province/State", "Lat", "Long"]) \
                             .groupby("Country/Region").sum()
    df_grouped = df_grouped.T
    df_grouped.index = pd.to_datetime(df_grouped.index, errors="coerce")

    fig = px.line(df_grouped[countries],
                  labels={"value": "Cas confirmés", "index": "Date", "variable": "Pays"},
                  title="Évolution des cas confirmés COVID-19")
    st.plotly_chart(fig, use_container_width=True)

# === Page 2 : carte interactive ===
elif page == "Carte interactive":
    st.title("🌍 Carte mondiale COVID-19")

    # Carte colorée par cas confirmés
    fig_map = px.choropleth(
        data_latest,
        locations="Country/Region",
        locationmode="country names",
        color=f"{latest_date}_confirmed",
        hover_name="Country/Region",
        hover_data=[f"{latest_date}_confirmed", f"{latest_date}_deaths"],
        title=f"Situation au {latest_date}"
    )

    # 🔹 Agrandir la carte (plein écran + suppression des marges)
    fig_map.update_layout(
        height=800,  # augmente la hauteur (par défaut ~450)
        margin=dict(l=0, r=0, t=50, b=0)
    )

    st.plotly_chart(fig_map, use_container_width=True)

    # Choix d'un pays
    selected_country = st.selectbox("Détails pour un pays :", data_latest["Country/Region"].unique())

    # Extraire évolution dans le temps
    confirmed_country = df_confirmed[df_confirmed["Country/Region"] == selected_country].drop(columns=["Province/State","Lat","Long"]).sum()
    deaths_country = df_deaths[df_deaths["Country/Region"] == selected_country].drop(columns=["Province/State","Lat","Long"]).sum()

    confirmed_country = confirmed_country[1:]  # enlever nom pays
    deaths_country = deaths_country[1:]

    df_country = pd.DataFrame({
        "Date": pd.to_datetime(confirmed_country.index, errors="coerce"),
        "Confirmés": confirmed_country.values,
        "Morts": deaths_country.values
    })

    st.subheader(f"📊 Détails pour {selected_country}")
    fig_detail = px.line(df_country, x="Date", y=["Confirmés", "Morts"], title=f"Évolution COVID-19 - {selected_country}")
    st.plotly_chart(fig_detail, use_container_width=True)
