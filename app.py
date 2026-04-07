import streamlit as st
import pandas as pd
import requests
import io
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────
GITHUB_RAW_DEFAULT = "https://raw.githubusercontent.com/SEU_ORG/SEU_REPO/main/data/alerta_aceleracao.csv"

st.set_page_config(
    page_title="Farol · Aceleração PAX",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# ESTILOS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500&display=swap');

:root {
  --bg:      #080a0f;
  --bg2:     #0e1118;
  --surf:    #111520;
  --surf2:   #161b28;
  --bdr:     #1d2335;
  --bdr2:    #252c40;
  --txt:     #dde3f0;
  --muted:   #4a5370;
  --muted2:  #6b7590;
  --red:     #ff3b55;
  --orange:  #ff7a2f;
  --yellow:  #ffd23f;
  --green:   #20e89a;
  --blue:    #3d8bff;
}

*,*::before,*::after{box-sizing:border-box;}

html,body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
section[data-testid="stMain"]>div{
  background:var(--bg)!important;
  color:var(--txt)!important;
  font-family:'IBM Plex Sans',sans-serif!important;
}
[data-testid="stSidebar"]{
  background:var(--bg2)!important;
  border-right:1px solid var(--bdr)!important;
}
[data-testid="stSidebar"] *{color:var(--txt)!important;}
.block-container{padding:1.5rem 2rem!important;max-width:100%!important;}
hr{border-color:var(--bdr)!important;}

[data-testid="stTextInput"] input{
  background:var(--surf)!important;border-color:var(--bdr2)!important;
  color:var(--txt)!important;font-family:'IBM Plex Sans',sans-serif!important;
}
[data-testid="stButton"]>button{
  background:var(--surf2)!important;border:1px solid var(--bdr2)!important;
  color:var(--txt)!important;font-family:'IBM Plex Mono',monospace!important;
  font-size:.74rem!important;letter-spacing:.4px!important;
}
[data-testid="stButton"]>button:hover{border-color:var(--blue)!important;color:var(--blue)!important;}
[data-testid="stButton"]>button[kind="primary"]{
  background:rgba(61,139,255,.15)!important;
  border-color:var(--blue)!important;
  color:var(--blue)!important;
}

/* HEADER */
.farol-header{
  display:flex;align-items:center;justify-content:space-between;
  padding-bottom:1.2rem;margin-bottom:1.4rem;border-bottom:1px solid var(--bdr);
}
.farol-title{
  font-family:'Syne',sans-serif;font-size:1.55rem;font-weight:800;
  letter-spacing:-.5px;color:var(--txt);margin:0;line-height:1;
}
.farol-sub{font-family:'IBM Plex Mono',monospace;font-size:.68rem;color:var(--muted2);margin-top:4px;letter-spacing:.5px;}
.upill{
  display:inline-flex;align-items:center;gap:7px;
  background:var(--surf);border:1px solid var(--bdr2);border-radius:20px;
  padding:5px 14px;font-family:'IBM Plex Mono',monospace;font-size:.68rem;color:var(--muted2);
}
.dot{width:7px;height:7px;border-radius:50%;background:var(--green);display:inline-block;animation:pulse 2.5s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}

/* KPI */
.kpi-strip{display:grid;grid-template-columns:repeat(7,1fr);gap:10px;margin-bottom:1.6rem;}
.kpi{
  background:var(--surf);border:1px solid var(--bdr);border-top:3px solid var(--bdr);
  border-radius:8px;padding:12px 14px 10px;transition:transform .15s;
}
.kpi:hover{transform:translateY(-2px);}
.kpi-lbl{font-family:'IBM Plex Mono',monospace;font-size:.61rem;color:var(--muted2);text-transform:uppercase;letter-spacing:1.2px;margin-bottom:6px;}
.kpi-val{font-family:'Syne',sans-serif;font-size:1.85rem;font-weight:700;line-height:1;color:var(--txt);}
.c-red{border-top-color:var(--red)!important;}
.c-ora{border-top-color:var(--orange)!important;}
.c-red2{border-top-color:#ff6b6b!important;}
.c-grn{border-top-color:var(--green)!important;}
.c-yel{border-top-color:var(--yellow)!important;}
.c-blu{border-top-color:var(--blue)!important;}
.c-mut{border-top-color:var(--bdr2)!important;}

/* CHART */
.chart-wrap{
  background:var(--surf);border:1px solid var(--bdr);border-radius:10px;
  padding:20px 24px;margin-bottom:1.5rem;
}
.chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:28px;}
.chart-col-title{
  font-family:'Syne',sans-serif;font-size:.92rem;font-weight:700;
  margin-bottom:14px;letter-spacing:-.3px;
}
.hbar-row{display:flex;align-items:center;gap:10px;margin-bottom:7px;}
.hbar-lbl{
  font-family:'IBM Plex Mono',monospace;font-size:.68rem;color:var(--muted2);
  width:80px;text-align:right;flex-shrink:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.hbar-track{flex:1;height:22px;background:var(--bdr);border-radius:4px;overflow:hidden;}
.hbar-fill{height:100%;border-radius:4px;display:flex;align-items:center;}
.hbar-val{font-family:'IBM Plex Mono',monospace;font-size:.68rem;font-weight:600;padding-left:8px;color:#fff;white-space:nowrap;}

/* CHIPS */
.chip-bar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:.8rem;}

/* TABLE */
.tbl-wrap{overflow-x:auto;border:1px solid var(--bdr);border-radius:10px;margin-bottom:1.5rem;}
.tbl{width:100%;border-collapse:collapse;font-size:.79rem;}
.tbl thead tr{background:var(--surf2);}
.tbl th{
  padding:10px 13px;border-bottom:1px solid var(--bdr2);
  font-family:'IBM Plex Mono',monospace;font-size:.6rem;font-weight:500;
  color:var(--muted2);text-transform:uppercase;letter-spacing:1px;
  text-align:left;white-space:nowrap;
}
.tbl td{padding:9px 13px;border-bottom:1px solid var(--bdr);vertical-align:middle;white-space:nowrap;}
.tbl tbody tr:hover td{background:rgba(255,255,255,.025);}
.tbl tbody tr:last-child td{border-bottom:none;}
.grp-sep td{
  background:var(--surf2)!important;padding:5px 13px!important;
  font-family:'IBM Plex Mono',monospace!important;font-size:.6rem!important;
  color:var(--muted2)!important;letter-spacing:1px!important;
  text-transform:uppercase!important;border-bottom:1px solid var(--bdr2)!important;
}

/* cells */
.rname{font-family:'Syne',sans-serif;font-weight:700;font-size:.88rem;letter-spacing:-.3px;color:var(--txt);}
.rsub{font-family:'IBM Plex Mono',monospace;font-size:.6rem;color:var(--muted);}

.badge{display:inline-block;padding:2px 9px;border-radius:20px;font-family:'IBM Plex Mono',monospace;font-size:.62rem;font-weight:500;white-space:nowrap;}
.b-urg{background:rgba(255,59,85,.12);color:var(--red);border:1px solid rgba(255,59,85,.3);}
.b-atn{background:rgba(255,122,47,.12);color:var(--orange);border:1px solid rgba(255,122,47,.3);}
.b-lot{background:rgba(255,107,107,.12);color:#ff6b6b;border:1px solid rgba(255,107,107,.3);}
.b-opp{background:rgba(32,232,154,.12);color:var(--green);border:1px solid rgba(32,232,154,.3);}
.b-mon{background:rgba(255,210,63,.12);color:var(--yellow);border:1px solid rgba(255,210,63,.3);}
.b-des{background:rgba(61,139,255,.12);color:var(--blue);border:1px solid rgba(61,139,255,.3);}
.b-nor{background:rgba(74,83,112,.12);color:var(--muted2);border:1px solid rgba(74,83,112,.3);}

.spark{display:inline-flex;gap:3px;align-items:flex-end;height:24px;vertical-align:middle;}
.sb{width:7px;border-radius:2px 2px 0 0;background:var(--muted);opacity:.4;}
.su{background:var(--green);opacity:.9;}
.sd{background:var(--red);opacity:.9;}
.sl{opacity:1!important;}

.occ-row{display:flex;align-items:center;gap:7px;}
.occ-track{width:52px;height:5px;background:var(--bdr2);border-radius:3px;}
.occ-fill{height:100%;border-radius:3px;}
.om{font-family:'IBM Plex Mono',monospace;font-size:.74rem;}

.ng{font-family:'IBM Plex Mono',monospace;color:var(--green);font-size:.78rem;}
.nr{font-family:'IBM Plex Mono',monospace;color:var(--red);font-size:.78rem;}
.nm{font-family:'IBM Plex Mono',monospace;color:var(--muted2);font-size:.78rem;}
.nt{font-family:'IBM Plex Mono',monospace;color:var(--txt);font-size:.78rem;}
.no{font-family:'IBM Plex Mono',monospace;color:var(--orange);font-size:.78rem;}

/* FOOTER */
.footer{
  display:flex;justify-content:space-between;align-items:center;
  padding-top:1rem;border-top:1px solid var(--bdr);margin-top:.5rem;
}
.ftxt{font-family:'IBM Plex Mono',monospace;font-size:.63rem;color:var(--muted);}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────────────────────────────────────
SINAL_ORDER = {
    "🚨 ABAIXO FORECAST + DESACEL - URGENTE": 1,
    "⚠️ ABAIXO FORECAST - PROXIMA VIAGEM":    2,
    "🔴 LOTANDO - REVISAR PREÇO":              3,
    "🟢 ACELERANDO - OPORTUNIDADE":            4,
    "🟡 ACELERANDO - MONITORAR":               5,
    "🔵 DESACELERANDO":                        6,
    "⚪ NORMAL":                               7,
}
SINAL_META = {
    "🚨 ABAIXO FORECAST + DESACEL - URGENTE": {"short":"URGENTE",      "badge":"b-urg","color":"var(--red)",   "kpi":"c-red"},
    "⚠️ ABAIXO FORECAST - PROXIMA VIAGEM":    {"short":"ATENÇÃO",      "badge":"b-atn","color":"var(--orange)","kpi":"c-ora"},
    "🔴 LOTANDO - REVISAR PREÇO":              {"short":"LOTANDO",      "badge":"b-lot","color":"#ff6b6b",      "kpi":"c-red2"},
    "🟢 ACELERANDO - OPORTUNIDADE":            {"short":"OPORTUNIDADE", "badge":"b-opp","color":"var(--green)", "kpi":"c-grn"},
    "🟡 ACELERANDO - MONITORAR":               {"short":"MONITORAR",    "badge":"b-mon","color":"var(--yellow)","kpi":"c-yel"},
    "🔵 DESACELERANDO":                        {"short":"DESACEL.",     "badge":"b-des","color":"var(--blue)",  "kpi":"c-blu"},
    "⚪ NORMAL":                               {"short":"NORMAL",       "badge":"b-nor","color":"var(--muted2)","kpi":"c-mut"},
}

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data(url: str) -> pd.DataFrame:
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        df = pd.read_csv(io.StringIO(r.text))
        df.columns = df.columns.str.strip()
        int_cols = ["pax","capacidade_atual","assentos_disponiveis",
                    "pax_d1","pax_d2","pax_d3","pax_d4","pax_d5",
                    "pax_hoje_parcial","predict_consenso","pax_faltam_forecast",
                    "predict_time_series","predict_eixo_sentido"]
        float_cols = ["occ_atual","tkm_comp","aceleracao_pct","aceleracao_abs",
                      "tendencia_linear","pct_atingimento_forecast","media_d2_d5","load_factor_atual"]
        for c in int_cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
        for c in float_cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")
        if "data" in df.columns:
            df["data"] = pd.to_datetime(df["data"])
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS HTML
# ─────────────────────────────────────────────────────────────────────────────
def badge_html(sinal):
    m = SINAL_META.get(sinal, SINAL_META["⚪ NORMAL"])
    return f'<span class="badge {m["badge"]}">{m["short"]}</span>'

def occ_html(v):
    try:
        pct = min(float(v)*100, 100)
        col = "#ff3b55" if pct>=90 else ("#ffd23f" if pct>=70 else "#20e89a")
        return (f'<div class="occ-row">'
                f'<div class="occ-track"><div class="occ-fill" style="width:{pct:.0f}%;background:{col}"></div></div>'
                f'<span class="om">{pct:.0f}%</span></div>')
    except:
        return "—"

def spark_html(d5, d4, d3, d2, d1):
    vals = [float(x) if str(x) not in ("nan","") else 0 for x in [d5,d4,d3,d2,d1]]
    mx = max(vals) if max(vals)>0 else 1
    up = vals[-1] >= (sum(vals[:-1])/max(len(vals)-1,1))
    bars=""
    for i,v in enumerate(vals):
        h = max(int((v/mx)*22),2)
        last = i==4
        cls = ("su sl" if up else "sd sl") if last else "sb"
        bars += f'<div class="{cls}" style="height:{h}px" title="{v:.0f}"></div>'
    return f'<div class="spark">{bars}</div>'

def acel_html(pct):
    try:
        v=float(pct)
        if v>30:  return f'<span class="ng">+{v:.0f}%</span>'
        if v<-30: return f'<span class="nr">{v:.0f}%</span>'
        return f'<span class="nm">{v:.0f}%</span>'
    except:
        return '<span class="nm">—</span>'

def fc_html(pct, faltam):
    try:
        v=float(pct)
        cls="nr" if v<50 else ("no" if v<80 else "ng")
        ft = f'<br><span class="nm" style="font-size:.63rem">faltam {int(faltam)}</span>' if str(faltam) not in ("nan","") else ""
        return f'<span class="{cls}">{v:.0f}%</span>{ft}'
    except:
        return "—"

def tend_html(v):
    try:
        f=float(v)
        if f>0.5:  return f'<span class="ng">↑ {f:.1f}</span>'
        if f<-0.5: return f'<span class="nr">↓ {f:.1f}</span>'
        return f'<span class="nm">→ {f:.1f}</span>'
    except:
        return '<span class="nm">—</span>'

def mono_html(v, prefix="", suffix="", dec=0):
    try:
        if str(v) in ("nan",""):
            return '<span class="nm">—</span>'
        return f'<span class="nt">{prefix}{float(v):,.{dec}f}{suffix}</span>'
    except:
        return '<span class="nm">—</span>'

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuração")
    github_url = st.text_input("URL do CSV (GitHub Raw)", value=GITHUB_RAW_DEFAULT)
    if st.button("↻ Recarregar dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.divider()
    st.markdown("### 🔍 Filtros")

    df_raw = load_data(github_url)
    if df_raw.empty:
        st.warning("Nenhum dado. Verifique a URL.")
        st.stop()

    datas_disp = sorted(df_raw["data"].dt.date.unique()) if "data" in df_raw.columns else []
    datas_sel = st.multiselect(
        "Data de viagem", options=datas_disp, default=datas_disp,
        format_func=lambda d: d.strftime("%d/%m/%Y"),
    )
    ant_min, ant_max = int(df_raw["antecedencia"].min()), int(df_raw["antecedencia"].max())
    ant_range = st.slider("Antecedência (dias)", ant_min, ant_max, (ant_min, ant_max))
    rota_busca = st.text_input("Buscar rota", placeholder="ex: SAO-RIO")
    hide_normal = st.checkbox("Ocultar ⚪ NORMAL", value=True)
    st.divider()
    st.markdown(
        '<span style="font-family:\'IBM Plex Mono\',monospace;font-size:.63rem;color:#4a5370">'
        'D1=ontem · D5=5 dias atrás<br>Acel=D1 vs média D2–D5</span>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# FILTROS BASE
# ─────────────────────────────────────────────────────────────────────────────
df_base = df_raw.copy()
if datas_sel:
    df_base = df_base[df_base["data"].dt.date.isin(datas_sel)]
df_base = df_base[df_base["antecedencia"].between(ant_range[0], ant_range[1])]
if rota_busca:
    df_base = df_base[df_base["sentido"].str.upper().str.contains(rota_busca.upper(), na=False)]
if hide_normal:
    df_base = df_base[df_base["sinal"] != "⚪ NORMAL"]

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
agora = datetime.now().strftime("%d/%m %H:%M")
st.markdown(f"""
<div class="farol-header">
  <div>
    <div class="farol-title">🚦 FAROL · ACELERAÇÃO PAX</div>
    <div class="farol-sub">MONITORAMENTO DE RESERVAS POR ROTA &nbsp;·&nbsp; {len(df_base)} ROTAS VISÍVEIS</div>
  </div>
  <div class="upill"><span class="dot"></span>atualizado {agora}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# KPI STRIP
# ─────────────────────────────────────────────────────────────────────────────
def cnt_kw(kw): return int(df_raw["sinal"].str.contains(kw, na=False).sum())

kpis = [
    ("c-red",  "🚨 URGENTE",      cnt_kw("URGENTE")),
    ("c-ora",  "⚠️ ATENÇÃO",      cnt_kw("PROXIMA")),
    ("c-red2", "🔴 LOTANDO",      cnt_kw("LOTANDO")),
    ("c-grn",  "🟢 OPORTUNIDADE", cnt_kw("OPORTUNIDADE")),
    ("c-yel",  "🟡 MONITORAR",    cnt_kw("MONITORAR")),
    ("c-blu",  "🔵 DESACEL.",     cnt_kw("DESACEL")),
    ("c-mut",  "TOTAL ROTAS",     len(df_raw)),
]
strip = '<div class="kpi-strip">'
for cls, lbl, val in kpis:
    strip += f'<div class="kpi {cls}"><div class="kpi-lbl">{lbl}</div><div class="kpi-val">{val}</div></div>'
strip += '</div>'
st.markdown(strip, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# GRÁFICO — Top acelerações / desacelerações
# ─────────────────────────────────────────────────────────────────────────────
if "aceleracao_pct" in df_base.columns and not df_base.empty:
    df_ch = df_base.dropna(subset=["aceleracao_pct"]).copy()
    if "media_d2_d5" in df_ch.columns:
        df_ch = df_ch[df_ch["media_d2_d5"] >= 2]

    top_up   = df_ch.nlargest(8,  "aceleracao_pct")
    top_down = df_ch.nsmallest(8, "aceleracao_pct")
    max_abs  = max(
        top_up["aceleracao_pct"].abs().max()   if not top_up.empty   else 1,
        top_down["aceleracao_pct"].abs().max() if not top_down.empty else 1,
    )

    def hbar(row, color):
        pct_w = min(abs(float(row["aceleracao_pct"])) / max_abs * 100, 100)
        v     = float(row["aceleracao_pct"])
        sign  = "+" if v > 0 else ""
        dt    = pd.to_datetime(row["data"]).strftime("%d/%m") if pd.notna(row["data"]) else ""
        return (f'<div class="hbar-row">'
                f'<div class="hbar-lbl">{row["sentido"]}<br>'
                f'<span style="font-size:.57rem;color:var(--muted)">{dt}</span></div>'
                f'<div class="hbar-track">'
                f'<div class="hbar-fill" style="width:{pct_w:.1f}%;background:{color}">'
                f'<span class="hbar-val">{sign}{v:.0f}%</span></div></div></div>')

    chart = '<div class="chart-wrap"><div class="chart-grid">'
    chart += '<div><div class="chart-col-title" style="color:var(--green)">↑ Maiores Acelerações</div>'
    for _, r in top_up.iterrows():
        chart += hbar(r, "#20e89a")
    chart += '</div>'
    chart += '<div><div class="chart-col-title" style="color:var(--red)">↓ Maiores Desacelerações</div>'
    for _, r in top_down.iterrows():
        chart += hbar(r, "#ff3b55")
    chart += '</div></div></div>'
    st.markdown(chart, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CHIPS DE SINAL (filtro rápido inline)
# ─────────────────────────────────────────────────────────────────────────────
sinais_pres = sorted(df_base["sinal"].dropna().unique(), key=lambda s: SINAL_ORDER.get(s, 99))

if "chips" not in st.session_state:
    st.session_state.chips = set(sinais_pres)
st.session_state.chips = st.session_state.chips.intersection(sinais_pres)
if not st.session_state.chips:
    st.session_state.chips = set(sinais_pres)

n = len(sinais_pres)
chip_cols = st.columns(n + 1)
for i, sinal in enumerate(sinais_pres):
    m    = SINAL_META.get(sinal, SINAL_META["⚪ NORMAL"])
    ativo = sinal in st.session_state.chips
    cnt_s = int((df_base["sinal"] == sinal).sum())
    with chip_cols[i]:
        if st.button(
            f"{m['short']} ({cnt_s})",
            key=f"chip_{i}",
            use_container_width=True,
            type="primary" if ativo else "secondary",
        ):
            if ativo and len(st.session_state.chips) > 1:
                st.session_state.chips.discard(sinal)
            else:
                st.session_state.chips.add(sinal)
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# TABELA PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
df_view = df_base[df_base["sinal"].isin(st.session_state.chips)].copy()
df_view = df_view.sort_values("sinal", key=lambda s: s.map(lambda x: SINAL_ORDER.get(x, 99)))

if df_view.empty:
    st.info("Nenhuma rota com os filtros selecionados.")
    st.stop()

has_d5 = "pax_d5" in df_view.columns
rows = ""
cur  = None

for _, row in df_view.iterrows():
    if row["sinal"] != cur:
        cur = row["sinal"]
        m   = SINAL_META.get(cur, SINAL_META["⚪ NORMAL"])
        cnt_g = int((df_view["sinal"] == cur).sum())
        rows += f'<tr class="grp-sep"><td colspan="13" style="color:{m["color"]}!important">● {cur} &nbsp;·&nbsp; {cnt_g} rota{"s" if cnt_g>1 else ""}</td></tr>'

    dt  = row["data"].strftime("%d/%m") if pd.notna(row.get("data")) else "—"
    d5  = row.get("pax_d5", 0) if has_d5 else 0

    rows += f"""<tr>
      <td><div><span class="rname">{row.get('sentido','—')}</span><br>
          <span class="rsub">{row.get('rota_principal','')}</span></div></td>
      <td><span class="nt">{dt}</span></td>
      <td>{mono_html(row.get('antecedencia'), suffix='d')}</td>
      <td>{occ_html(row.get('occ_atual',0))}</td>
      <td>{mono_html(row.get('pax'))}</td>
      <td>{mono_html(row.get('assentos_disponiveis'))}</td>
      <td>{fc_html(row.get('pct_atingimento_forecast'), row.get('pax_faltam_forecast'))}</td>
      <td>{spark_html(d5, row.get('pax_d4',0), row.get('pax_d3',0), row.get('pax_d2',0), row.get('pax_d1',0))}</td>
      <td>{acel_html(row.get('aceleracao_pct'))}</td>
      <td>{tend_html(row.get('tendencia_linear'))}</td>
      <td>{mono_html(row.get('tkm_comp'), prefix='R$', dec=0)}</td>
      <td>{mono_html(row.get('predict_consenso'))}</td>
      <td>{badge_html(str(row.get('sinal','⚪ NORMAL')))}</td>
    </tr>"""

tabela = f"""
<div class="tbl-wrap">
<table class="tbl">
  <thead><tr>
    <th>Rota</th><th>Data</th><th>Antec.</th><th>Ocupação</th>
    <th>PAX</th><th>Assentos liv.</th><th>Forecast %</th>
    <th>D5→D1</th><th>Acel. %</th><th>Tendência</th>
    <th>Ticket</th><th>Predict</th><th>Sinal</th>
  </tr></thead>
  <tbody>{rows}</tbody>
</table>
</div>
"""
st.markdown(tabela, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# RODAPÉ
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <span class="ftxt">{len(df_view)} rotas exibidas &nbsp;·&nbsp; {len(df_raw)} total carregadas</span>
  <span class="ftxt">D1=ontem completo &nbsp;·&nbsp; Acel=D1 vs média D2–D5 &nbsp;·&nbsp; sem viés de horário</span>
</div>
""", unsafe_allow_html=True)
