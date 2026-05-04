import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="PortafolioIA",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
  #MainMenu, footer, header {visibility:hidden;}
  .block-container {padding:1.5rem 2rem 2rem;}
  .stProgress > div > div {background:linear-gradient(90deg,#3B82F6,#06B6D4);}
  div[data-testid="metric-container"] {
    background:#0D1421;border:1px solid #1E2D45;
    border-radius:10px;padding:14px;
  }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:12px;margin-bottom:4px">
  <span style="font-size:28px;font-weight:900;letter-spacing:-1px">
    Portafolio<span style="color:#3B82F6">IA</span>
  </span>
  <span style="font-size:11px;color:#06B6D4;background:rgba(6,182,212,0.1);
    border:1px solid rgba(6,182,212,0.25);padding:3px 10px;border-radius:20px;
    font-family:monospace">MARKOWITZ · MONTE CARLO</span>
</div>
<hr style="border:none;border-top:1px solid #1E2D45;margin-bottom:8px">
""", unsafe_allow_html=True)

# ── Datos ─────────────────────────────────────────────────────
ACTIVOS = pd.DataFrame([
  dict(id="ECO",  nombre="Ecopetrol",           clase="Acciones BVC", ret=14.2, vol=28.0, div=6.8,  beta=1.32, sharpe=0.31),
  dict(id="GRU",  nombre="Grupo Nutresa",        clase="Acciones BVC", ret=11.8, vol=19.0, div=3.2,  beta=0.81, sharpe=0.67),
  dict(id="BAR",  nombre="Bancolombia Pref.",    clase="Acciones BVC", ret=13.2, vol=22.0, div=5.5,  beta=0.95, sharpe=0.35),
  dict(id="ISA",  nombre="ISA",                  clase="Acciones BVC", ret=10.9, vol=16.0, div=4.1,  beta=0.72, sharpe=0.31),
  dict(id="SPY",  nombre="SPDR S&P 500",         clase="ETFs",         ret=12.6, vol=17.0, div=1.3,  beta=1.00, sharpe=0.42),
  dict(id="QQQ",  nombre="Invesco QQQ (Nasdaq)", clase="ETFs",         ret=18.9, vol=24.0, div=0.6,  beta=1.18, sharpe=0.58),
  dict(id="VWO",  nombre="Vanguard Emergentes",  clase="ETFs",         ret=9.8,  vol=21.0, div=2.8,  beta=1.05, sharpe=0.23),
  dict(id="GLD",  nombre="SPDR Gold",            clase="ETFs",         ret=8.3,  vol=14.0, div=0.0,  beta=-0.02,sharpe=0.21),
  dict(id="TES",  nombre="TES Colombia 2030",    clase="Bonos",        ret=11.8, vol=6.0,  div=11.8, beta=-0.10,sharpe=1.05),
  dict(id="COB",  nombre="Bono Corp. Col.",       clase="Bonos",        ret=13.4, vol=8.0,  div=13.4, beta=0.05, sharpe=0.74),
  dict(id="UST",  nombre="US Treasury 10Y",      clase="Bonos",        ret=4.3,  vol=5.0,  div=4.3,  beta=-0.15,sharpe=-0.24),
  dict(id="BTC",  nombre="Bitcoin",              clase="Criptomonedas",ret=61.2, vol=72.0, div=0.0,  beta=1.45, sharpe=0.78),
  dict(id="ETH",  nombre="Ethereum",             clase="Criptomonedas",ret=49.8, vol=81.0, div=0.0,  beta=1.52, sharpe=0.55),
  dict(id="FIR",  nombre="FIC Inmobiliario Col.",clase="Finca Raíz",   ret=9.7,  vol=10.0, div=7.2,  beta=0.48, sharpe=0.42),
  dict(id="VNQ",  nombre="VNQ REIT USA",         clase="Finca Raíz",   ret=8.8,  vol=18.0, div=3.8,  beta=0.82, sharpe=0.18),
])

PERFILES = {
  "conservador": dict(
    label="Conservador", emoji="🟡", color="#F59E0B",
    ret=10.8, vol=8.3, sharpe=0.63, mc_p10=134, mc_p50=186, mc_p90=264, prob=91.2,
    desc="Preservar el capital. Horizonte < 3 años. Baja tolerancia a pérdidas.",
    pesos={"TES Colombia 2030":35,"Bono Corp. Col.":25,"US Treasury 10Y":15,
           "FIC Inmobiliario Col.":10,"SPDR S&P 500":8,"SPDR Gold":5,"Bancolombia Pref.":2}
  ),
  "moderado": dict(
    label="Moderado", emoji="🔵", color="#3B82F6",
    ret=12.4, vol=14.4, sharpe=0.48, mc_p10=128, mc_p50=219, mc_p90=412, prob=87.6,
    desc="Equilibrio entre crecimiento y seguridad. Horizonte 3-7 años.",
    pesos={"SPDR S&P 500":20,"Bancolombia Pref.":12,"Grupo Nutresa":10,
           "TES Colombia 2030":18,"Bono Corp. Col.":12,"FIC Inmobiliario Col.":10,
           "Invesco QQQ (Nasdaq)":8,"SPDR Gold":6,"ISA":4}
  ),
  "agresivo": dict(
    label="Agresivo", emoji="🟣", color="#8B5CF6",
    ret=20.9, vol=29.3, sharpe=0.53, mc_p10=87, mc_p50=426, mc_p90=1820, prob=79.3,
    desc="Maximizar retornos con alta volatilidad. Horizonte > 7 años.",
    pesos={"Invesco QQQ (Nasdaq)":22,"Ecopetrol":12,"SPDR S&P 500":15,
           "Bitcoin":10,"Ethereum":6,"Grupo Nutresa":8,
           "Bancolombia Pref.":8,"Bono Corp. Col.":8,"VNQ REIT USA":7,"Vanguard Emergentes":4}
  )
}

PREGUNTAS = [
  dict(q="⏱️ ¿Cuánto tiempo planeas mantener tu inversión sin tocarla?",
       opts=["Menos de 1 año","Entre 1 y 3 años","Entre 3 y 7 años","Más de 7 años"],
       pts=[0,1,2,3]),
  dict(q="📉 Si tu portafolio cae un 20% en un mes, ¿qué harías?",
       opts=["Vendo todo para no perder más","Espero a que se recupere",
             "Analizo antes de decidir","Compro más, es una oportunidad"],
       pts=[0,1,2,3]),
  dict(q="💰 ¿Qué % de tus ingresos mensuales puedes destinar a inversión?",
       opts=["Menos del 5%","Entre el 5% y 15%","Más del 15%"],
       pts=[0,1,3]),
  dict(q="📚 ¿Cuál es tu experiencia previa en inversiones?",
       opts=["Ninguna, apenas empiezo","Básica, conozco algunos productos",
             "Intermedia, he invertido antes","Avanzada, manejo portafolios"],
       pts=[0,1,2,3]),
  dict(q="🚨 ¿Necesitas disponer de este dinero en los próximos 12 meses?",
       opts=["Sí, es posible que lo necesite","Tal vez, no estoy seguro",
             "No, es dinero que puedo dejar invertido"],
       pts=[0,1,3]),
]

# ── Tabs ──────────────────────────────────────────────────────
t1, t2, t3, t4 = st.tabs([
    "🤖 Diagnóstico de Perfil",
    "📊 Dashboard de Mercado",
    "🧮 Calculadora",
    "📦 Universo de Activos"
])

# ════════════════════════════════
# TAB 1 — WIZARD
# ════════════════════════════════
with t1:
    if "wstep" not in st.session_state:
        st.session_state.wstep = 0
        st.session_state.wscore = 0
        st.session_state.wresp = []

    step = st.session_state.wstep

    st.progress(step / len(PREGUNTAS),
                text=f"Pregunta {min(step+1, len(PREGUNTAS))} de {len(PREGUNTAS)}")
    st.markdown("")

    if step < len(PREGUNTAS):
        p = PREGUNTAS[step]
        st.markdown(f"### {p['q']}")
        st.markdown("")
        cols = st.columns(2)
        for i, opt in enumerate(p["opts"]):
            if cols[i % 2].button(opt, key=f"w{step}_{i}", use_container_width=True):
                st.session_state.wscore += p["pts"][i]
                st.session_state.wresp.append(opt)
                st.session_state.wstep += 1
                st.rerun()

        if st.session_state.wresp:
            st.markdown("---")
            for j, r in enumerate(st.session_state.wresp):
                st.markdown(f"**{PREGUNTAS[j]['q']}**  \n✅ *{r}*")

    else:
        sc   = st.session_state.wscore
        pkey = "conservador" if sc<=4 else "moderado" if sc<=9 else "agresivo"
        p    = PERFILES[pkey]

        st.success(f"{p['emoji']} **Tu perfil es: {p['label']}** — {p['desc']}")
        st.markdown("")

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Retorno Anual",    f"{p['ret']}%")
        c2.metric("Volatilidad",      f"{p['vol']}%")
        c3.metric("Sharpe Ratio",     str(p['sharpe']))
        c4.metric("P50 Monte Carlo",  f"${p['mc_p50']}M COP")

        st.markdown("### 📊 Asignación Sugerida")
        fig = go.Figure(go.Bar(
            x=list(p["pesos"].values()),
            y=list(p["pesos"].keys()),
            orientation="h",
            marker_color=p["color"],
            text=[f"{v}%" for v in p["pesos"].values()],
            textposition="outside"
        ))
        fig.update_layout(
            height=320, margin=dict(l=0,r=40,t=10,b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#E8EDF5", xaxis=dict(showgrid=False,visible=False),
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🎲 Simulación Monte Carlo (10 años · $100M COP)")
        fig2 = go.Figure()
        fig2.add_bar(name="P10 Pesimista",  x=["Escenario"], y=[p["mc_p10"]],  marker_color="#EF4444")
        fig2.add_bar(name="P50 Esperado",   x=["Escenario"], y=[p["mc_p50"]],  marker_color=p["color"])
        fig2.add_bar(name="P90 Optimista",  x=["Escenario"], y=[p["mc_p90"]],  marker_color="#10B981")
        fig2.update_layout(
            height=260, barmode="group",
            margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#E8EDF5", yaxis_title="Valor ($M COP)",
            legend=dict(orientation="h", y=-0.2)
        )
        st.plotly_chart(fig2, use_container_width=True)

        with st.expander("📋 Ver tus respuestas"):
            for j, r in enumerate(st.session_state.wresp):
                st.markdown(f"**{PREGUNTAS[j]['q']}**  \n✅ {r}")

        if st.button("↺ Repetir diagnóstico"):
            st.session_state.wstep = 0
            st.session_state.wscore = 0
            st.session_state.wresp = []
            st.rerun()

# ════════════════════════════════
# TAB 2 — DASHBOARD
# ════════════════════════════════
with t2:
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Activos disponibles", "15", "6 clases")
    c2.metric("Mejor retorno",  "61.2%", "Bitcoin")
    c3.metric("Menor volatilidad", "5.0%", "US Treasury")
    c4.metric("Mejor Sharpe", "1.05", "TES Colombia")
    st.markdown("")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("##### 📊 Retorno vs Volatilidad")
        fig = px.scatter(ACTIVOS, x="vol", y="ret", color="clase", size=[15]*15,
                         hover_name="nombre", text="id",
                         color_discrete_map={
                           "Acciones BVC":"#1D4ED8","ETFs":"#0891B2",
                           "Bonos":"#059669","Criptomonedas":"#9333EA","Finca Raíz":"#B45309"
                         })
        fig.update_traces(textposition="top center", textfont_size=9)
        fig.update_layout(height=340, margin=dict(l=0,r=0,t=10,b=0),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(13,20,33,1)",
                          font_color="#E8EDF5",
                          xaxis=dict(title="Volatilidad (%)", gridcolor="#1E2D45"),
                          yaxis=dict(title="Retorno (%)", gridcolor="#1E2D45"),
                          legend=dict(font_size=11))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("##### 📐 Frontera Eficiente (Markowitz)")
        vols = np.linspace(5, 80, 60)
        rets = 5.5 + (vols/80)*18 + np.sin(vols/8)*1.2
        fig2 = go.Figure()
        fig2.add_scatter(x=vols, y=rets, mode="lines", name="Frontera Eficiente",
                         line=dict(color="#3B82F6", width=2.5))
        for pkey, pd_ in PERFILES.items():
            fig2.add_scatter(x=[pd_["vol"]], y=[pd_["ret"]],
                             mode="markers+text", name=pd_["label"],
                             marker=dict(size=12, color=pd_["color"]),
                             text=[pd_["label"]], textposition="top center",
                             textfont=dict(size=11))
        fig2.update_layout(height=340, margin=dict(l=0,r=0,t=10,b=0),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(13,20,33,1)",
                           font_color="#E8EDF5",
                           xaxis=dict(title="Volatilidad (%)", gridcolor="#1E2D45"),
                           yaxis=dict(title="Retorno (%)", gridcolor="#1E2D45"),
                           legend=dict(font_size=11))
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown("##### 💰 Asignación Perfil Moderado")
        pm = PERFILES["moderado"]
        fig3 = go.Figure(go.Pie(
            labels=list(pm["pesos"].keys()),
            values=list(pm["pesos"].values()),
            hole=0.45, textinfo="label+percent"
        ))
        fig3.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0),
                           paper_bgcolor="rgba(0,0,0,0)", font_color="#E8EDF5",
                           showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        st.markdown("##### 🎲 Monte Carlo P50 — $100M COP · 10 años")
        mc_df = pd.DataFrame([
            dict(Perfil="Conservador", Escenario="P10", Valor=134),
            dict(Perfil="Conservador", Escenario="P50", Valor=186),
            dict(Perfil="Conservador", Escenario="P90", Valor=264),
            dict(Perfil="Moderado",    Escenario="P10", Valor=128),
            dict(Perfil="Moderado",    Escenario="P50", Valor=219),
            dict(Perfil="Moderado",    Escenario="P90", Valor=412),
            dict(Perfil="Agresivo",    Escenario="P10", Valor=87),
            dict(Perfil="Agresivo",    Escenario="P50", Valor=426),
            dict(Perfil="Agresivo",    Escenario="P90", Valor=1820),
        ])
        fig4 = px.bar(mc_df, x="Perfil", y="Valor", color="Escenario", barmode="group",
                      color_discrete_map={"P10":"#EF4444","P50":"#3B82F6","P90":"#10B981"})
        fig4.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(13,20,33,1)",
                           font_color="#E8EDF5", yaxis_title="Valor ($M COP)",
                           xaxis=dict(gridcolor="#1E2D45"), yaxis=dict(gridcolor="#1E2D45"),
                           legend=dict(font_size=11))
        st.plotly_chart(fig4, use_container_width=True)

# ════════════════════════════════
# TAB 3 — CALCULADORA
# ════════════════════════════════
with t3:
    col_form, col_res = st.columns([1,2])
    with col_form:
        st.markdown("##### ⚙️ Parámetros")
        perfil_sel = st.selectbox("Perfil de Riesgo",
                                  ["🟡 Conservador","🔵 Moderado","🟣 Agresivo"])
        capital    = st.number_input("Capital Inicial (COP)", 1_000_000, 5_000_000_000,
                                     50_000_000, step=1_000_000,
                                     format="%d")
        horizonte  = st.slider("Horizonte (años)", 1, 30, 10)
        aporte_m   = st.number_input("Aportación Mensual (COP)", 0, 50_000_000,
                                     500_000, step=100_000, format="%d")
        calcular   = st.button("⚡ Calcular Proyección", use_container_width=True)

    with col_res:
        if calcular:
            pkey = perfil_sel.split()[-1].lower()
            p    = PERFILES[pkey]
            r    = p["ret"] / 100

            # Proyección año a año
            vals = [capital]
            for _ in range(horizonte):
                vals.append(vals[-1] * (1+r) + aporte_m*12)

            final = vals[-1]
            st.success(f"**Valor proyectado: ${final/1e6:,.1f}M COP** en {horizonte} años")

            cc1,cc2,cc3 = st.columns(3)
            cc1.metric("Retorno Anual", f"{p['ret']}%")
            cc2.metric("Volatilidad",   f"{p['vol']}%")
            cc3.metric("Sharpe",        str(p["sharpe"]))

            st.markdown("")
            st.markdown("##### 📈 Trayectoria del Capital")
            fig = go.Figure()
            fig.add_scatter(
                x=list(range(horizonte+1)),
                y=[v/1e6 for v in vals],
                mode="lines+markers",
                line=dict(color=p["color"], width=2.5),
                marker=dict(size=5),
                fill="tozeroy",
                fillcolor=p["color"].replace(")", ",0.1)").replace("rgb","rgba") if "rgb" in p["color"] else p["color"]+"22",
                name="Valor esperado"
            )
            fig.update_layout(
                height=300, margin=dict(l=0,r=0,t=10,b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(13,20,33,1)",
                font_color="#E8EDF5",
                xaxis=dict(title="Año", gridcolor="#1E2D45"),
                yaxis=dict(title="Valor ($M COP)", gridcolor="#1E2D45"),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("👈 Configura los parámetros y haz clic en **Calcular Proyección**")

# ════════════════════════════════
# TAB 4 — UNIVERSO DE ACTIVOS
# ════════════════════════════════
with t4:
    clase_filter = st.selectbox("Filtrar por clase",
                                ["Todas"] + sorted(ACTIVOS["clase"].unique().tolist()))
    df_show = ACTIVOS if clase_filter=="Todas" else ACTIVOS[ACTIVOS["clase"]==clase_filter]

    st.markdown(f"**{len(df_show)} activos** · datos sintéticos")
    st.dataframe(
        df_show.rename(columns={
            "id":"ID","nombre":"Nombre","clase":"Clase","ret":"Retorno %",
            "vol":"Volatilidad %","div":"Dividendo %","beta":"Beta","sharpe":"Sharpe"
        }).set_index("ID"),
        use_container_width=True,
        height=460,
        column_config={
            "Retorno %":    st.column_config.ProgressColumn("Retorno %",    min_value=0, max_value=65),
            "Volatilidad %":st.column_config.ProgressColumn("Volatilidad %",min_value=0, max_value=85),
            "Sharpe":       st.column_config.NumberColumn("Sharpe", format="%.2f"),
        }
    )
