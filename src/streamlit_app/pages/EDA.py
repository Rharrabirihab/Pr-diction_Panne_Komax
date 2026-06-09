import base64
from io import BytesIO
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st



def image_to_base64(image) -> str:

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def get_repo_root() -> Path:
    # src/streamlit_app/pages/EDA.py -> src/streamlit_app/pages -> src/streamlit_app -> src -> repo_root
    return Path(__file__).resolve().parents[3]


def load_logo_base64() -> str:
    try:
        from PIL import Image

        assets_dir = Path(__file__).resolve().parent.parent / "assets"
        logo_path = assets_dir / "ESTILOGO.png"
        if not logo_path.exists():
            return ""
        return image_to_base64(Image.open(logo_path))
    except Exception:
        return ""


logo_base64 = load_logo_base64()

st.markdown(
    """
    <style>
    .logo-img { border-radius: 15px; height: 90px; margin-right: 1.5rem; }
    header {
        background-color: #F0F1F5;
        border-radius: 15px;
        display: flex;
        align-items: center;
        padding: 1rem 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
    header h2 {
        font-size: 1.8rem;
        font-weight: bold;
        color: #AF9979;
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <header>
        {f'<img src="data:image/png;base64,{logo_base64}" class="logo-img">' if logo_base64 else ''}
        <h2>EDA Komax — Pannes & Maintenance</h2>
    </header>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data() -> pd.DataFrame:
    repo_root = get_repo_root()

    candidate_paths = [
        repo_root / "data" / "processed" / "trainFinal.csv",
        repo_root / "data" / "processed" / "testFinal.csv",
        repo_root / "data" / "raw" / "komax_cleandata.csv",
        repo_root / "data" / "data.csv",
    ]

    last_err = None
    for p in candidate_paths:
        try:
            if p.exists():
                return pd.read_csv(p)
        except Exception as e:
            last_err = e

    raise FileNotFoundError(f"Impossible de charger le dataset EDA. Dernière erreur: {last_err}")


df = load_data()

st.markdown(
    "🔎 Cette page explore les variables du dataset pour comprendre les tendances avant l’entraînement."
)

with st.expander("Aperçu du dataset", expanded=True):
    st.dataframe(df.head(50), use_container_width=True)


# --- detect columns ---
possible_targets = ["failure", "Type Of Failure", "Type Of Failure_label", "Machine_label", "target", "y"]
target_col = next((c for c in possible_targets if c in df.columns), None)

num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
cat_cols = [c for c in df.columns if c not in num_cols]

st.divider()

st.subheader("🎯 Distribution de la variable cible")
if target_col is None:
    st.info("Aucune colonne cible reconnue automatiquement. Colonnes disponibles :")
    st.write(list(df.columns))
else:
    vc = df[target_col].value_counts()

    # Nettoyage/compat Plotly: assurer un vrai champ pour l'axe X
    vc_df = (
        vc.reset_index()
        .rename(columns={"index": target_col, target_col: target_col, 0: "count"})
    )
    # selon version pandas, la colonne count peut avoir un nom différent
    if "count" not in vc_df.columns:
        # fallback sur la dernière colonne numérique
        num_like = [c for c in vc_df.columns if c != target_col]
        if num_like:
            vc_df = vc_df.rename(columns={num_like[0]: "count"})

    fig = px.bar(
        vc_df,
        x=target_col,
        y="count",
        title=f"Nombre d'observations par {target_col}",
        color="count",
        color_continuous_scale="sunsetdark",
    )
    fig.update_layout(xaxis_title=target_col, yaxis_title="Nombre d'observations")
    st.plotly_chart(fig, use_container_width=True)


st.divider()

st.subheader("🔗 Corrélations (variables numériques vs cible)")
if target_col is None or target_col not in num_cols:
    st.info("La cible n'est pas numérique (ou non trouvée) : corrélations ignorées.")
else:
    corr = df[num_cols].corr(numeric_only=True)[target_col].sort_values(ascending=False)
    corr_top = corr.dropna().head(15)
    fig_corr = px.bar(
        corr_top.reset_index(name="corr"),
        x="index",
        y="corr",
        title="Corrélations les plus fortes avec la cible",
        color="corr",
        color_continuous_scale="tealgrn",
    )
    fig_corr.update_layout(xaxis_title="Variable", yaxis_title="Corrélation")
    st.plotly_chart(fig_corr, use_container_width=True)


st.divider()

st.subheader("📈 Impact d'une variable numérique (binné)")
if target_col is None or not num_cols:
    st.info("Impossible de construire le graphe : cible ou variables numériques manquantes.")
else:
    x_var = st.selectbox("Choisissez une variable numérique :", num_cols, index=0)

    # binning for readability
    binned = pd.cut(df[x_var], bins=12)
    stats = (
        pd.DataFrame({"bin": binned, "target": df[target_col]})
        .groupby("bin", observed=True)["target"]
        .mean()
        .reset_index()
    )

    fig_impact = px.line(
        stats,
        x="bin",
        y="target",
        markers=True,
        title=f"Tendance moyenne de {target_col} selon {x_var} (binné)",
    )
    fig_impact.update_layout(xaxis_title=x_var, yaxis_title=f"Moyenne de {target_col}")
    st.plotly_chart(fig_impact, use_container_width=True)


st.divider()

st.subheader("🖼️ Visualisations issues des notebooks")
repo_root = get_repo_root()

candidate_images = [repo_root / "notebooks" / "valeurs_manquantes.png"]

found_any = False
for img_path in candidate_images:
    if img_path.exists():
        found_any = True
        st.image(str(img_path), caption=img_path.name, use_container_width=True)

if not found_any:
    st.warning("Aucune image n'a été trouvée automatiquement dans notebooks/.")

st.markdown(
    """
    <hr>
    📊 Une fois l’exploration terminée, passez à l’onglet **Prediction**.
    """,
    unsafe_allow_html=True,
)

