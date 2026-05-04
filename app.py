import streamlit as st
import streamlit.components.v1 as components

# ── Configuración de la página ──────────────────────────────
st.set_page_config(
    page_title="PortafolioIA — Optimización con IA",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Ocultar menú y footer de Streamlit ──────────────────────
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
    </style>
""", unsafe_allow_html=True)

# ── Cargar y mostrar el HTML ─────────────────────────────────
with open("portafolio_ia.html", "r", encoding="utf-8") as f:
    html_content = f.read()

components.html(html_content, height=900, scrolling=True)
