import streamlit as st

import pandas as pd

st.title("Analyse des données")

df = pd.read_csv("data\data.csv")

st.write(df.head(20))

st.bar_chart(df["failure"].value_counts())