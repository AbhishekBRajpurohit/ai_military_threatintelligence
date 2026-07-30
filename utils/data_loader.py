import pandas as pd
import streamlit as st
from config import DATA_PATH


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, encoding="latin-1", low_memory=False)

    df["nkill"] = df["nkill"].fillna(0)
    df["nwound"] = df["nwound"].fillna(0)

    for col in ["country_txt", "region_txt", "attacktype1_txt",
                "weaptype1_txt", "targtype1_txt", "gname", "city"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    return df


@st.cache_data
def load_geo_data():
    """Subset with valid coordinates, for map pages."""
    df = load_data()
    return df.dropna(subset=["latitude", "longitude"])