import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#  Configuration globale de la page
st.set_page_config(
    page_title="Analyse Qualité du Vin Blanc",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded",
)

#  CSS personnalisé
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Fond général */
.stApp {
    background-color: #F7F3EE;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1A1A2E;
}
section[data-testid="stSidebar"] * {
    color: #E8E0D5 !important;
}
section[data-testid="stSidebar"] .stRadio label {
    font-size: 15px;
    padding: 6px 0;
}

/* Titres */
h1 {
    font-family: 'DM Serif Display', serif !important;
    color: #1A1A2E !important;
    letter-spacing: -0.5px;
}
h2, h3 {
    font-family: 'DM Serif Display', serif !important;
    color: #2C3E50 !important;
}

/* Carte métrique */
div[data-testid="metric-container"] {
    background: white;
    border-radius: 12px;
    padding: 18px 20px;
    border-left: 4px solid #C8956C;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
div[data-testid="metric-container"] label {
    color: #2563EB !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #1A1A2E !important;
    font-size: 28px !important;
    font-weight: 600 !important;
}

/* Séparateur */
hr {
    border: none;
    border-top: 1px solid #E5DDD5;
    margin: 20px 0;
}

/* Boîte d'info */
.insight-box {
    background: white;
    border-radius: 12px;
    padding: 16px 20px;
    border-left: 4px solid #4A90D9;
    margin: 12px 0;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    color: #2C3E50;
    font-size: 14px;
    line-height: 1.6;
}
.insight-box.warning {
    border-left-color: #E67E22;
}
.insight-box.success {
    border-left-color: #27AE60;
}

/* Header page */
.page-header {
    background: linear-gradient(135deg, #1A1A2E 0%, #2C3E50 100%);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 28px;
    color: white;
}
.page-header h1 {
    color: white !important;
    margin: 0 0 6px 0;
    font-size: 28px;
}
.page-header p {
    color: #B0C4D8;
    margin: 0;
    font-size: 14px;
}

/* Selectbox */
div[data-baseweb="select"] {
    border-radius: 8px !important;
}

/* Tableau */
.dataframe {
    border-radius: 10px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

#  Chargement des données
df = pd.read_csv("juice_clean.csv")

FEATURES = [c for c in df.columns if c not in ["quality", "quality_label"]]

# Palette couleurs qualité
QUALITY_COLORS = {
    3: "#E74C3C", 4: "#E67E22", 5: "#F1C40F",
    6: "#2ECC71", 7: "#27AE60", 8: "#1ABC9C", 9: "#16A085"
}
CAT_COLORS = {
    "Faible (≤4)": "#E74C3C",
    "Moyen (5-6)": "#F1C40F",
    "Excellent (≥7)": "#27AE60"
}

PLOTLY_TEMPLATE = "plotly_white"

LABELS_FR = {
    "fixed acidity": "Acidité fixe",
    "volatile acidity": "Acidité volatile",
    "citric acid": "Acide citrique",
    "residual sugar": "Sucre résiduel",
    "chlorides": "Chlorures",
    "free sulfur dioxide": "SO₂ libre",
    "total sulfur dioxide": "SO₂ total",
    "density": "Densité",
    "pH": "pH",
    "sulphates": "Sulfates",
    "alcohol": "Alcool",
    "quality": "Qualité"
}

def label(col):
    return LABELS_FR.get(col, col)


#  Métriques globales (accessibles sur toutes les pages)
pct_excellent = (df["quality"] >= 7).sum() / len(df) * 100
pct_faible    = (df["quality"] <= 4).sum() / len(df) * 100


#  Sidebar Navigation
with st.sidebar:
    st.markdown("## 🍷 Vin Blanc")
    st.markdown("**Analyse Qualité**")
    st.markdown("---")
    page = st.radio(
        "Navigation",
        options=[
            "🏠 Vue d'ensemble",
            "📊 Distribution Qualité",
            "🔬 Analyse par Variable",
            "🔗 Corrélations",
            "📈 Profils de Qualité",
        ],
        label_visibility="collapsed"
    )


#  PAGE 1 - VUE D'ENSEMBLE
if page == "🏠 Vue d'ensemble":

    st.markdown("""
    <div class='page-header'>
        <h1>🍷 Tableau de Bord - Qualité du Vin Blanc</h1>
        <p>Analyse exploratoire du dataset juice 3961 échantillons</p>
    </div>
    """, unsafe_allow_html=True)

    # -- KPIs
    q_mean = df["quality"].mean()
    q_mode = int(df["quality"].mode()[0])
    q_min = int(df["quality"].min())
    q_max = int(df["quality"].max())

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Vins analysés", f"{len(df):,}")
    c2.metric("Note moyenne", f"{q_mean:.2f} / 10")
    c3.metric("Note la + fréquente", str(q_mode))
    c4.metric("Vins Excellents (≥7)", f"{pct_excellent:.1f}%")
    c5.metric("Vins Faibles (≤4)", f"{pct_faible:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.3, 1])

    with col_left:
        # Distribution rapide des notes
        vc = df["quality"].value_counts().sort_index().reset_index()
        vc.columns = ["Note", "Nombre"]
        vc["Couleur"] = vc["Note"].map(QUALITY_COLORS)
        fig = px.bar(
            vc, x="Note", y="Nombre", color="Note",
            color_discrete_map=QUALITY_COLORS,
            title="Répartition des notes de qualité",
            labels={"Note": "Note de qualité", "Nombre": "Nombre de vins"},
            template=PLOTLY_TEMPLATE, text="Nombre"
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(showlegend=False, plot_bgcolor="white",
                          title_font_size=15, height=340,
                          margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        # Camembert catégories
        cat_counts = df["quality_label"].value_counts()
        fig2 = px.pie(
            values=cat_counts.values,
            names=cat_counts.index.tolist(),
            title="Catégories de qualité",
            color=cat_counts.index.tolist(),
            color_discrete_map=CAT_COLORS,
            hole=0.45,
            template=PLOTLY_TEMPLATE
        )
        fig2.update_traces(textposition="outside", textinfo="percent+label",
                           pull=[0.03, 0.03, 0.07])
        fig2.update_layout(showlegend=False, height=340,
                           title_font_size=15,
                           margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # -- Aperçu du dataset
    st.subheader("Aperçu des données")
    st.dataframe(df.drop(columns=["quality_label"]).head(10), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -- Stats descriptives
    st.subheader("Statistiques descriptives")
    stats = df[FEATURES + ["quality"]].describe().T.round(3)
    stats.columns = ["Nb obs.", "Moyenne", "Écart-type", "Min", "Q1", "Médiane", "Q3", "Max"]
    stats.index = [label(i) for i in stats.index]
    st.dataframe(stats, use_container_width=True)

    st.markdown("""
    <div class='insight-box success'>
    <b>Résumé :</b> Le jeu de données ne contient aucune valeur manquante. La majorité des vins obtiennent une note de 5 ou 6 (plus de 70 % des observations). 
    Les notes extrêmes (3, 4, 8, 9) sont très peu représentées. La variable <b>alcool</b> est la plus fortement corrélée avec la qualité.
    </div>
    """, unsafe_allow_html=True)


#  PAGE 2 - DISTRIBUTION QUALITÉ
elif page == "📊 Distribution Qualité":

    st.markdown("""
    <div class='page-header'>
        <h1>📊 Distribution de la Qualité</h1>
        <p>Comment les notes de qualité se distribuent-elles dans le dataset ?</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        vc = df["quality"].value_counts().sort_index().reset_index()
        vc.columns = ["Note", "Nombre"]
        vc["Pct"] = (vc["Nombre"] / vc["Nombre"].sum() * 100).round(1)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=vc["Note"], y=vc["Nombre"],
            marker_color=[QUALITY_COLORS[n] for n in vc["Note"]],
            text=[f"{p}%" for p in vc["Pct"]],
            textposition="outside"
        ))
        fig.update_layout(
            title="Nombre de vins par note de qualité",
            xaxis_title="Note de qualité",
            yaxis_title="Nombre de vins",
            template=PLOTLY_TEMPLATE, height=380,
            plot_bgcolor="white",
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        cat_counts = df["quality_label"].value_counts()
        fig2 = go.Figure(go.Pie(
            labels=cat_counts.index.tolist(),
            values=cat_counts.values,
            marker_colors=[CAT_COLORS[c] for c in cat_counts.index],
            hole=0.5,
            textinfo="percent+label",
            pull=[0.04, 0.04, 0.08]
        ))
        fig2.update_layout(
            title="Répartition Faible / Moyen / Excellent",
            template=PLOTLY_TEMPLATE, height=380,
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("Distribution cumulée")

    cumulative = vc.copy()
    cumulative["Cumulé"] = cumulative["Nombre"].cumsum()
    cumulative["Pct_cum"] = (cumulative["Cumulé"] / len(df) * 100).round(1)

    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(go.Bar(
        x=cumulative["Note"], y=cumulative["Nombre"],
        name="Nb vins", marker_color="#4A90D9", opacity=0.7
    ), secondary_y=False)
    fig3.add_trace(go.Scatter(
        x=cumulative["Note"], y=cumulative["Pct_cum"],
        name="% cumulé", line=dict(color="#E67E22", width=3),
        mode="lines+markers", marker=dict(size=8)
    ), secondary_y=True)
    fig3.update_layout(
        title="Distribution + courbe cumulative",
        template=PLOTLY_TEMPLATE, height=380,
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=50, b=20)
    )
    fig3.update_yaxes(title_text="Nombre de vins", secondary_y=False)
    fig3.update_yaxes(title_text="Pourcentage cumulé (%)", secondary_y=True)
    st.plotly_chart(fig3, use_container_width=True)

    n_56 = int(vc.loc[vc['Note'].isin([5, 6]), 'Nombre'].sum())
    pct_56 = round(n_56 / len(df) * 100)
    st.markdown(f"""
    <div class='insight-box'>
    <b>Observation :</b> {n_56:,} vins ({pct_56}%) ont une note de 5 ou 6.
    Les vins excellents (&ge;7) représentent <b>{pct_excellent:.1f}%</b> du dataset,
    et les vins faibles (&le;4) seulement <b>{pct_faible:.1f}%</b>.
    Le dataset est donc <b>déséquilibré</b> : la classe médiane est sur-représentée.
    </div>
    """, unsafe_allow_html=True)

#  PAGE 3 - ANALYSE PAR VARIABLE
elif page == "🔬 Analyse par Variable":

    st.markdown("""
    <div class='page-header'>
        <h1>🔬 Analyse par Variable</h1>
        <p>Explorez la distribution et le comportement de chaque variable physico-chimique</p>
    </div>
    """, unsafe_allow_html=True)

    col_sel, _ = st.columns([1, 2])
    with col_sel:
        var_choisie = st.selectbox(
            "Choisir une variable",
            options=FEATURES,
            format_func=label
        )

    st.markdown("---")

    # Statistiques rapides de la variable choisie
    s = df[var_choisie]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Moyenne", f"{s.mean():.3f}")
    c2.metric("Médiane", f"{s.median():.3f}")
    c3.metric("Écart-type", f"{s.std():.3f}")
    c4.metric("Plage", f"[{s.min():.2f} ; {s.max():.2f}]")

    st.markdown("<br>", unsafe_allow_html=True)

    col_hist, col_box = st.columns(2)

    with col_hist:
        fig = px.histogram(
            df, x=var_choisie, nbins=50,
            color_discrete_sequence=["#4A90D9"],
            title=f"Distribution - {label(var_choisie)}",
            labels={var_choisie: label(var_choisie)},
            template=PLOTLY_TEMPLATE, opacity=0.85
        )
        fig.add_vline(x=s.mean(), line_dash="dash", line_color="#E74C3C",
                      annotation_text=f"Moy: {s.mean():.2f}", annotation_position="top right")
        fig.add_vline(x=s.median(), line_dash="dot", line_color="#E67E22",
                      annotation_text=f"Méd: {s.median():.2f}", annotation_position="top left")
        fig.update_layout(height=360, plot_bgcolor="white",
                          margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_box:
        fig2 = px.box(
            df, x="quality", y=var_choisie,
            color="quality", color_discrete_map=QUALITY_COLORS,
            title=f"{label(var_choisie)} selon la note de qualité",
            labels={"quality": "Note", var_choisie: label(var_choisie)},
            template=PLOTLY_TEMPLATE
        )
        fig2.update_layout(showlegend=False, height=360, plot_bgcolor="white",
                           margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # Moyenne de la variable par note - graphique linéaire
    means = df.groupby("quality")[var_choisie].mean().reset_index()
    fig3 = px.line(
        means, x="quality", y=var_choisie,
        markers=True,
        title=f"Moyenne de {label(var_choisie)} par note de qualité",
        labels={"quality": "Note de qualité", var_choisie: f"Moyenne - {label(var_choisie)}"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=["#C8956C"]
    )
    fig3.update_traces(line_width=3, marker_size=10)
    fig3.update_layout(height=320, plot_bgcolor="white",
                       margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig3, use_container_width=True)

    # Détection outliers IQR
    Q1 = s.quantile(0.25)
    Q3 = s.quantile(0.75)
    IQR = Q3 - Q1
    n_out = ((s < Q1 - 1.5 * IQR) | (s > Q3 + 1.5 * IQR)).sum()
    pct_out = n_out / len(df) * 100

    corr_val = df[[var_choisie, "quality"]].corr().iloc[0, 1]
    direction = "positive" if corr_val > 0 else "négative"
    force = "forte" if abs(corr_val) > 0.3 else ("modérée" if abs(corr_val) > 0.15 else "faible")

    st.markdown(f"""
    <div class='insight-box'>
    <b>{label(var_choisie)}</b> - Corrélation avec la qualité : <b>r = {corr_val:.3f}</b> ({force}, {direction}).
    Outliers détectés (méthode IQR) : <b>{n_out}</b> valeurs ({pct_out:.1f}% du dataset).
    </div>
    """, unsafe_allow_html=True)


#  PAGE 4 - CORRÉLATIONS
elif page == "🔗 Corrélations":

    st.markdown("""
    <div class='page-header'>
        <h1>🔗 Analyse des Corrélations</h1>
        <p>Quelles variables physico-chimiques influencent le plus la qualité du vin ?</p>
    </div>
    """, unsafe_allow_html=True)

    corr = df[FEATURES + ["quality"]].corr()
    corr_quality = corr["quality"].drop("quality").sort_values(key=abs, ascending=False)

    col_heat, col_bar = st.columns([1.4, 1])

    with col_heat:
        # Masque triangle supérieur
        mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
        corr_masked = corr.copy()
        corr_masked[mask] = None
        cols_fr = [label(c) for c in corr.columns]
        fig = px.imshow(
            corr_masked,
            x=cols_fr, y=cols_fr,
            color_continuous_scale="RdBu_r",
            zmin=-1, zmax=1,
            title="Matrice de corrélation (Pearson)",
            text_auto=".2f",
            template=PLOTLY_TEMPLATE, aspect="auto"
        )
        fig.update_layout(height=500, margin=dict(l=20, r=20, t=50, b=20),
                          coloraxis_colorbar=dict(title="r", thickness=15))
        fig.update_traces(textfont_size=10)
        st.plotly_chart(fig, use_container_width=True)

    with col_bar:
        colors = ["#27AE60" if v > 0 else "#E74C3C" for v in corr_quality.values]
        fig2 = go.Figure(go.Bar(
            x=corr_quality.values,
            y=[label(c) for c in corr_quality.index],
            orientation="h",
            marker_color=colors,
            text=[f"{v:.3f}" for v in corr_quality.values],
            textposition="outside"
        ))
        fig2.add_vline(x=0, line_color="black", line_width=1)
        fig2.update_layout(
            title="Corrélation avec la Qualité",
            xaxis_title="Coefficient r",
            template=PLOTLY_TEMPLATE,
            height=500, plot_bgcolor="white",
            margin=dict(l=20, r=100, t=50, b=20),
            xaxis=dict(range=[-0.55, 0.55])
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("Top corrélations inter-variables")

    # Tableau des paires les plus corrélées (hors qualité, hors diagonale)
    corr_no_quality = df[FEATURES].corr()
    pairs = []
    for i, c1 in enumerate(FEATURES):
        for j, c2 in enumerate(FEATURES):
            if j > i:
                pairs.append({
                    "Variable 1": label(c1),
                    "Variable 2": label(c2),
                    "Corrélation": round(corr_no_quality.loc[c1, c2], 3)
                })
    pairs_df = pd.DataFrame(pairs).sort_values("Corrélation", key=abs, ascending=False).head(10)
    pairs_df["Direction"] = pairs_df["Corrélation"].apply(lambda x: "🟢 Positive" if x > 0 else "🔴 Négative")
    st.dataframe(pairs_df.reset_index(drop=True), use_container_width=True)

    st.markdown(f"""
    <div class='insight-box success'>
    <b>Variable la plus influente :</b> <b>Alcool</b> (r = {corr_quality['alcohol']:.3f}) - corrélation positive la plus forte avec la qualité.  
    <b>Densité</b> (r = {corr_quality['density']:.3f}) - plus la densité est faible, meilleure est la qualité.  
    <b>Alcool et Densité</b> sont elles-mêmes fortement corrélées entre elles (r ≈ {corr_no_quality.loc['alcohol','density']:.2f}).
    </div>
    """, unsafe_allow_html=True)


#  PAGE 5 - PROFILS DE QUALITÉ
elif page == "📈 Profils de Qualité":

    st.markdown("""
    <div class='page-header'>
        <h1>📈 Profils de Qualité</h1>
        <p>Comment les caractéristiques du vin varient-elles selon la note de qualité ?</p>
    </div>
    """, unsafe_allow_html=True)

    # -- Sélecteur de variables
    vars_dispo = FEATURES
    vars_sel = st.multiselect(
        "Choisir les variables à comparer (1 à 4)",
        options=vars_dispo,
        default=["alcohol", "density", "volatile acidity", "chlorides"],
        format_func=label,
        max_selections=4
    )

    if not vars_sel:
        st.warning("Sélectionnez au moins une variable.")
        st.stop()

    st.markdown("---")

    # -- Boxplots groupés côte à côte
    n = len(vars_sel)
    ncols = 2
    nrows = (n + 1) // 2

    fig = make_subplots(rows=nrows, cols=ncols,
                        subplot_titles=[label(v) for v in vars_sel])
    for idx, var in enumerate(vars_sel):
        row = idx // ncols + 1
        col = idx % ncols + 1
        for note in sorted(df["quality"].unique()):
            vals = df[df["quality"] == note][var]
            fig.add_trace(go.Box(
                y=vals, name=f"Note {note}",
                marker_color=QUALITY_COLORS.get(note, "#888888"),
                showlegend=(idx == 0),
                legendgroup=str(note)
            ), row=row, col=col)

    fig.update_layout(
        title="Distribution des variables par note de qualité",
        template=PLOTLY_TEMPLATE,
        height=280 * nrows + 80,
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=70, b=20),
        boxmode="group"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # -- Courbes des moyennes par note
    means_df = df.groupby("quality")[vars_sel].mean().reset_index()

    fig2 = go.Figure()
    colors_line = ["#C8956C", "#4A90D9", "#27AE60", "#E74C3C"]
    for i, var in enumerate(vars_sel):
        fig2.add_trace(go.Scatter(
            x=means_df["quality"], y=means_df[var],
            name=label(var), mode="lines+markers",
            line=dict(color=colors_line[i % len(colors_line)], width=3),
            marker=dict(size=9)
        ))
    fig2.update_layout(
        title="Évolution des moyennes par note de qualité",
        xaxis_title="Note de qualité",
        yaxis_title="Valeur moyenne",
        template=PLOTLY_TEMPLATE, height=380, plot_bgcolor="white",
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")


    # -- Tableau des moyennes par catégorie
    st.subheader("Tableau des moyennes par catégorie")
    tbl = df.groupby("quality_label")[FEATURES].mean().round(3)
    tbl.index = tbl.index.astype(str)
    tbl.columns = [label(c) for c in tbl.columns]
    st.dataframe(tbl, use_container_width=True)
