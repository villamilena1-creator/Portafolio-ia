import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="PortafolioIA — Optimización con IA",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 1.5rem 2rem 0rem; }
  div[data-testid="stTabs"] button { font-size:14px; font-weight:600; padding:10px 18px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
  <span style="font-size:26px;font-weight:900;color:#E8EDF5;letter-spacing:-1px">
    Portafolio<span style="color:#3B82F6">IA</span>
  </span>
  <span style="font-size:11px;color:#06B6D4;background:rgba(6,182,212,0.1);
    border:1px solid rgba(6,182,212,0.25);padding:3px 10px;border-radius:20px;
    font-family:monospace;letter-spacing:1px">MARKOWITZ</span>
  <span style="font-size:11px;color:#4A6280;font-family:monospace;margin-left:auto">
    15 activos · 6 clases · datos sintéticos
  </span>
</div>
<hr style="border:none;border-top:1px solid #1E2D45;margin-bottom:16px">
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🤖  Diagnóstico de Perfil", "📊  Dashboard · Calculadora · Activos"])

PERFILES = {
    "conservador": {
        "label":"Conservador","emoji":"🟡",
        "ret":10.8,"vol":8.3,"sharpe":0.63,"mc_p50":186,"mc_prob":91.2,
        "desc":"Tu prioridad es **preservar el capital**. Horizonte corto (< 3 años). Baja tolerancia a pérdidas.",
        "pesos":{"TES Colombia 2030":35,"Bono Corp. Col.":25,"US Treasury 10Y":15,
                 "FIC Inmobiliario Col.":10,"SPDR S&P 500":8,"SPDR Gold":5,"Bancolombia":2}
    },
    "moderado": {
        "label":"Moderado","emoji":"🔵",
        "ret":12.4,"vol":14.4,"sharpe":0.48,"mc_p50":219,"mc_prob":87.6,
        "desc":"Buscas **equilibrio entre crecimiento y seguridad**. Horizonte 3-7 años. Tolerancia media.",
        "pesos":{"SPDR S&P 500":20,"Bancolombia":12,"Grupo Nutresa":10,
                 "TES Colombia 2030":18,"Bono Corp. Col.":12,"FIC Inmobiliario Col.":10,
                 "Invesco QQQ":8,"SPDR Gold":6,"ISA":4}
    },
    "agresivo": {
        "label":"Agresivo","emoji":"🟣",
        "ret":20.9,"vol":29.3,"sharpe":0.53,"mc_p50":426,"mc_prob":79.3,
        "desc":"Buscas **maximizar retornos** asumiendo alta volatilidad. Horizonte > 7 años.",
        "pesos":{"Invesco QQQ":22,"Ecopetrol":12,"SPDR S&P 500":15,
                 "Bitcoin":10,"Ethereum":6,"Grupo Nutresa":8,
                 "Bancolombia":8,"Bono Corp. Col.":8,"VNQ REIT USA":7,"VWO Emergentes":4}
    }
}

PREGUNTAS = [
    {"q":"⏱️ ¿Cuánto tiempo planeas mantener tu inversión sin tocarla?",
     "opts":["Menos de 1 año","Entre 1 y 3 años","Entre 3 y 7 años","Más de 7 años"],
     "pts":[0,1,2,3]},
    {"q":"📉 Si tu portafolio cae un 20% en un mes, ¿qué harías?",
     "opts":["Vendo todo para no perder más","Espero a que se recupere",
             "Analizo antes de decidir","Compro más, es una oportunidad"],
     "pts":[0,1,2,3]},
    {"q":"💰 ¿Qué porcentaje de tus ingresos mensuales puedes destinar a inversión?",
     "opts":["Menos del 5%","Entre el 5% y 15%","Más del 15%"],
     "pts":[0,1,3]},
    {"q":"📚 ¿Cuál es tu experiencia previa en inversiones?",
     "opts":["Ninguna, apenas empiezo","Básica, conozco algunos productos",
             "Intermedia, he invertido antes","Avanzada, manejo portafolios"],
     "pts":[0,1,2,3]},
    {"q":"🚨 ¿Necesitas disponer de este dinero en los próximos 12 meses?",
     "opts":["Sí, es posible que lo necesite","Tal vez, no estoy seguro",
             "No, es dinero que puedo dejar invertido"],
     "pts":[0,1,3]},
]

# ── TAB 1: WIZARD NATIVO STREAMLIT ───────────────────────────
with tab1:
    if "step" not in st.session_state:
        st.session_state.step      = 0
        st.session_state.score     = 0
        st.session_state.respuestas = []

    step  = st.session_state.step
    total = len(PREGUNTAS)

    st.progress(step / total, text=f"Pregunta {min(step+1, total)} de {total}")
    st.markdown("")

    if step < total:
        p = PREGUNTAS[step]
        st.markdown(f"### {p['q']}")
        st.markdown("")
        ncols = min(len(p["opts"]), 2)
        cols  = st.columns(ncols)
        for i, opt in enumerate(p["opts"]):
            with cols[i % ncols]:
                if st.button(opt, key=f"opt_{step}_{i}", use_container_width=True):
                    st.session_state.score += p["pts"][i]
                    st.session_state.respuestas.append(opt)
                    st.session_state.step  += 1
                    st.rerun()

        if st.session_state.respuestas:
            st.markdown("---")
            st.markdown("**Tus respuestas anteriores:**")
            for j, r in enumerate(st.session_state.respuestas):
                st.markdown(f"- {PREGUNTAS[j]['q']}  \n  ✅ *{r}*")
    else:
        score = st.session_state.score
        pkey  = "conservador" if score<=4 else "moderado" if score<=9 else "agresivo"
        p     = PERFILES[pkey]

        st.markdown(f"## {p['emoji']} Tu perfil es: **{p['label']}**")
        st.markdown(p["desc"])
        st.markdown("")

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Retorno Anual Esp.", f"{p['ret']}%")
        c2.metric("Volatilidad Anual",  f"{p['vol']}%")
        c3.metric("Sharpe Ratio",       f"{p['sharpe']}")
        c4.metric("Monte Carlo P50",    f"${p['mc_p50']}M COP")

        st.markdown("")
        st.markdown("### 📊 Asignación Sugerida del Portafolio")
        for activo, pct in p["pesos"].items():
            ca, cb = st.columns([3,1])
            with ca:
                st.progress(pct/100, text=activo)
            with cb:
                st.markdown(
                    f"<p style='text-align:right;font-weight:700;padding-top:6px'>{pct}%</p>",
                    unsafe_allow_html=True
                )

        st.markdown("")
        with st.expander("📋 Ver todas tus respuestas"):
            for j, r in enumerate(st.session_state.respuestas):
                st.markdown(f"**{PREGUNTAS[j]['q']}**  \n✅ {r}")

        st.markdown("")
        if st.button("↺  Repetir diagnóstico"):
            st.session_state.step      = 0
            st.session_state.score     = 0
            st.session_state.respuestas = []
            st.rerun()

# ── TAB 2: DASHBOARD HTML ────────────────────────────────────
with tab2:
    with open("portafolio_ia.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # Ocultar pestaña Agente y abrir directo en Dashboard
    html_content = (html_content
        .replace('class="page active" id="page-agent"',
                 'class="page" id="page-agent"')
        .replace('class="page" id="page-dashboard"',
                 'class="page active" id="page-dashboard"')
        .replace('class="nav-tab active" onclick="goTab(\'agent\',this)"',
                 'class="nav-tab" onclick="goTab(\'agent\',this)"')
        .replace('class="nav-tab" onclick="goTab(\'dashboard\',this)"',
                 'class="nav-tab active" onclick="goTab(\'dashboard\',this)"')
    )

    components.html(html_content, height=960, scrolling=True)
