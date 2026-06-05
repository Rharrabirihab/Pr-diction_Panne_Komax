import streamlit as st

# Thin wrapper so `streamlit run streamlit_app.py` works from the repo root.
# It delegates to the real app located in `src/streamlit_app/`.

from src.streamlit_app.app import main as _main

if __name__ == "__main__":
    _main()

