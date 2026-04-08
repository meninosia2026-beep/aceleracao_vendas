import streamlit as st
import pandas as pd
import requests
import io
import base64
import json
from datetime import datetime

GITHUB_RAW_ACEL  = "https://raw.githubusercontent.com/meninosia2026-beep/aceleracao_vendas/main/data/alerta_aceleracao.csv"
GITHUB_RAW_CURVA = "https://raw.githubusercontent.com/meninosia2026-beep/aceleracao_vendas/main/data/curva_feriado.csv"

st.set_page_config(page_title="Farol PAX", page_icon="🚦", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');
:root {
  --bg:#fff;--bg2:#f7f6f3;--bg3:#eeede9;--bdr:#e2e1dc;--bdr2:#d0cfc9;
  --txt:#1a1a18;--txt2:#3d3d38;--muted:#8c8c84;--muted2:#b8b8b0;
  --accent:#f11075;--green:#2d6a4f;--green-lt:#d8f3dc;
  --red:#c0392b;--red-lt:#fde8e8;--orange:#d35400;--blue:#2c3e7a;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,[data-testid="stAppViewContainer"],[data-testid="stAppViewBlockContainer"],
section[data-testid="stMain"]>div{background:var(--bg)!important;color:var(--txt)!important;font-family:'Inter',sans-serif!important;}
[data-testid="stSidebar"]{background:var(--bg2)!important;border-right:1px solid var(--bdr)!important;}
[data-testid="stSidebar"] *{color:var(--txt)!important;font-family:'Inter',sans-serif!important;}
.block-container{padding:2rem 2.5rem!important;max-width:100%!important;}
hr{border:none;border-top:1px solid var(--bdr)!important;margin:1rem 0;}
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:var(--bg2);}
::-webkit-scrollbar-thumb{background:var(--bdr2);border-radius:2px;}
[data-testid="stTextInput"] input{background:var(--bg)!important;border:1px solid var(--bdr2)!important;border-radius:4px!important;color:var(--txt)!important;font-family:'Inter',sans-serif!important;font-size:.83rem!important;}
[data-testid="stTextInput"] input:focus{border-color:var(--accent)!important;outline:none!important;box-shadow:none!important;}
[data-testid="stButton"]>button{background:var(--bg)!important;border:1px solid var(--bdr2)!important;color:var(--muted)!important;font-family:'Inter',sans-serif!important;font-size:.75rem!important;font-weight:500!important;border-radius:20px!important;padding:4px 14px!important;line-height:1.4!important;transition:all .12s!important;white-space:nowrap!important;}
[data-testid="stButton"]>button:hover{border-color:var(--accent)!important;color:var(--accent)!important;background:rgba(241,16,117,.04)!important;}
[data-testid="stButton"]>button[kind="primary"]{background:rgba(241,16,117,.08)!important;color:var(--accent)!important;border-color:var(--accent)!important;font-weight:600!important;}
[data-testid="stSidebar"] [data-testid="stButton"]>button{border-radius:4px!important;color:var(--txt2)!important;}
[data-testid="stSidebar"] [data-testid="stButton"]>button:hover{border-color:var(--accent)!important;color:var(--accent)!important;background:var(--bg)!important;}
[data-testid="stMultiSelect"] [data-baseweb="select"]>div{background:var(--bg)!important;border:1px solid var(--bdr2)!important;border-radius:4px!important;min-height:36px!important;box-shadow:none!important;}
[data-testid="stMultiSelect"] [data-baseweb="select"]>div:focus-within{border-color:var(--accent)!important;box-shadow:none!important;}
[data-baseweb="tag"]{background:var(--bg3)!important;border:1px solid var(--bdr2)!important;border-radius:3px!important;padding:1px 6px!important;height:22px!important;}
[data-baseweb="tag"] span:first-child{color:var(--txt2)!important;font-size:.72rem!important;font-weight:600!important;}
[data-baseweb="popover"] [data-baseweb="menu"]{background:var(--bg)!important;border:1px solid var(--bdr2)!important;border-radius:4px!important;box-shadow:0 4px 16px rgba(0,0,0,.08)!important;}
[data-baseweb="option"]{background:var(--bg)!important;font-size:.78rem!important;color:var(--txt2)!important;padding:7px 12px!important;}
[data-baseweb="option"]:hover,[aria-selected="true"][data-baseweb="option"]{background:var(--bg2)!important;}
[data-testid="stSlider"] [role="slider"]{background:var(--accent)!important;border:2px solid #fff!important;box-shadow:0 1px 6px rgba(241,16,117,.25)!important;width:14px!important;height:14px!important;}
[data-testid="stSlider"] [data-testid="stTickBarMin"],[data-testid="stSlider"] [data-testid="stTickBarMax"]{font-size:.7rem!important;color:var(--muted)!important;}
[data-testid="stCheckbox"] label{font-size:.82rem!important;color:var(--txt2)!important;font-weight:500!important;display:flex!important;flex-direction:row!important;align-items:center!important;gap:8px!important;white-space:nowrap!important;}
[data-testid="stCheckbox"] [data-baseweb="checkbox"] div{border-color:var(--bdr2)!important;border-radius:3px!important;background:var(--bg)!important;width:16px!important;height:16px!important;flex-shrink:0!important;}
[data-testid="stCheckbox"] [aria-checked="true"] div{background:var(--accent)!important;border-color:var(--accent)!important;}
[data-testid="stTabs"] [data-baseweb="tab-list"]{background:transparent!important;border-bottom:1px solid var(--bdr)!important;gap:0!important;}
[data-testid="stTabs"] [data-baseweb="tab"]{background:transparent!important;color:var(--muted)!important;font-family:'Inter',sans-serif!important;font-size:.85rem!important;font-weight:500!important;border:none!important;border-bottom:2px solid transparent!important;padding:8px 18px 10px!important;margin-bottom:-1px!important;}
[data-testid="stTabs"] [data-baseweb="tab"]:hover{color:var(--txt)!important;}
[data-testid="stTabs"] [aria-selected="true"][data-baseweb="tab"]{color:var(--txt)!important;border-bottom-color:var(--accent)!important;font-weight:600!important;}
[data-testid="stTabs"] [data-baseweb="tab-highlight"]{display:none!important;}
[data-testid="stTabs"] [data-baseweb="tab-border"]{display:none!important;}
.pg-header{display:flex;align-items:flex-start;justify-content:space-between;padding-bottom:1.4rem;margin-bottom:1.8rem;border-bottom:1px solid var(--bdr);}
.pg-title{font-family:'Libre Baskerville',serif;font-size:2rem;font-weight:700;letter-spacing:-.5px;color:var(--txt);line-height:1.1;margin-bottom:5px;}
.pg-sub{font-size:.82rem;color:var(--muted);}
.upill{display:inline-flex;align-items:center;gap:7px;font-size:.72rem;color:var(--muted);white-space:nowrap;margin-top:4px;}
.dot{width:7px;height:7px;border-radius:50%;background:var(--green);display:inline-block;animation:pulse 2.5s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.kpi-strip{display:grid;gap:0;border:1px solid var(--bdr);border-radius:6px;overflow:hidden;margin-bottom:2rem;}
.kpi{padding:14px 18px 12px;border-right:1px solid var(--bdr);background:var(--bg);}
.kpi:last-child{border-right:none;}
.kpi-lbl{font-size:.63rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:1px;margin-bottom:7px;display:flex;align-items:center;gap:5px;}
.kpi-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0;}
.kpi-val{font-family:'Libre Baskerville',serif;font-size:2rem;font-weight:700;line-height:1;color:var(--txt);}
.kpi-val.zero{color:var(--muted2);}
.c-red{border-top:3px solid var(--red)!important;}.c-ora{border-top:3px solid var(--orange)!important;}
.c-red2{border-top:3px solid #ef4444!important;}.c-grn{border-top:3px solid var(--green)!important;}
.c-yel{border-top:3px solid #b7950b!important;}.c-blu{border-top:3px solid var(--blue)!important;}
.c-mut{border-top:3px solid var(--bdr2)!important;}
.chart-section{margin-bottom:2rem;}
.section-title{font-family:'Libre Baskerville',serif;font-size:1.05rem;font-weight:700;color:var(--txt);margin-bottom:3px;}
.section-sub{font-size:.76rem;color:var(--muted);margin-bottom:1rem;}
.chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:28px;}
.chart-col{background:var(--bg2);border:1px solid var(--bdr);border-radius:6px;padding:18px 20px;}
.chart-col-title{font-size:.68rem;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:var(--muted);margin-bottom:12px;display:flex;align-items:center;gap:8px;}
.chart-col-title span{display:inline-block;width:8px;height:8px;border-radius:50%;}
.hbar-row{display:flex;align-items:center;gap:10px;margin-bottom:7px;}
.hbar-lbl{font-size:.72rem;font-weight:500;color:var(--txt2);width:80px;text-align:right;flex-shrink:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.hbar-date{font-size:.6rem;color:var(--muted);display:block;font-weight:400;}
.hbar-track{flex:1;height:20px;background:var(--bg3);border-radius:3px;overflow:hidden;}
.hbar-fill{height:100%;border-radius:3px;display:flex;align-items:center;}
.hbar-val{font-size:.68rem;font-weight:600;padding-left:8px;color:#fff;white-space:nowrap;}
.sort-info{font-size:.68rem;color:var(--muted);padding:6px 0 10px;display:flex;align-items:center;gap:6px;}
.sort-tag{display:inline-flex;align-items:center;gap:4px;background:var(--bg3);border:1px solid var(--bdr2);border-radius:3px;padding:1px 7px;font-size:.65rem;font-weight:600;color:var(--txt2);}
.tbl-wrap{overflow-x:auto;border:1px solid var(--bdr);border-radius:6px;margin-bottom:1.2rem;}
.tbl{width:100%;border-collapse:collapse;font-size:.79rem;}
.tbl thead tr{background:var(--bg2);}
.tbl th{padding:10px 13px;border-bottom:1px solid var(--bdr2);font-size:.61rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:1px;text-align:left;white-space:nowrap;}
.tbl th.sort-active{color:var(--txt);}
.tbl th.sort-active::after{content:' ↓';color:var(--accent);}
.tbl td{padding:9px 13px;border-bottom:1px solid var(--bdr);vertical-align:middle;white-space:nowrap;}
.tbl tbody tr:hover td{background:var(--bg2);}
.tbl tbody tr:last-child td{border-bottom:none;}
.tbl tbody tr.top-row td{background:#fafaf8;}
.grp-sep td{background:var(--bg2)!important;padding:6px 13px!important;font-size:.63rem!important;font-weight:600!important;color:var(--muted)!important;letter-spacing:.8px!important;text-transform:uppercase!important;border-top:1px solid var(--bdr2)!important;border-bottom:1px solid var(--bdr2)!important;}
.rname{font-weight:600;font-size:.85rem;color:var(--txt);}
.rsub{font-size:.62rem;color:var(--muted);}
.badge{display:inline-block;padding:2px 8px;border-radius:3px;font-size:.63rem;font-weight:600;white-space:nowrap;text-transform:uppercase;background:var(--bg3);color:var(--txt2);border:1px solid var(--bdr2);}
.b-urg{background:var(--red-lt);color:var(--red);border-color:#f5c6c6;}
.b-atn{background:#fef3e2;color:var(--orange);border-color:#f5d9b0;}
.b-opp{background:var(--green-lt);color:var(--green);border-color:#95d5b2;}
.spark{display:inline-flex;gap:2px;align-items:flex-end;height:22px;vertical-align:middle;}
.sb{width:6px;border-radius:1px 1px 0 0;background:var(--bdr2);}
.su{background:#74c69d;}.sd{background:#f5a0a0;}
.su.sl{background:var(--green);}.sd.sl{background:var(--red);}
.occ-row{display:flex;align-items:center;gap:7px;}
.occ-track{width:48px;height:4px;background:var(--bg3);border-radius:2px;}
.occ-fill{height:100%;border-radius:2px;}
.om{font-size:.77rem;font-weight:600;}
.ng{color:var(--green);font-size:.79rem;font-weight:600;}
.nr{color:var(--red);font-size:.79rem;font-weight:600;}
.nm{color:var(--muted);font-size:.79rem;}
.nt{color:var(--txt2);font-size:.79rem;}
.no{color:var(--orange);font-size:.79rem;font-weight:600;}
.sinal-tag{display:inline-flex;align-items:center;gap:5px;font-size:.71rem;font-weight:500;color:var(--txt2);}
.sinal-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0;}
.score-wrap{display:flex;align-items:center;gap:5px;}
.score-track{width:38px;height:3px;background:var(--bg3);border-radius:2px;}
.score-fill{height:100%;border-radius:2px;background:var(--accent);}
.score-val{font-size:.67rem;color:var(--muted);}
.sb-label{font-size:.63rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:1px;margin:.8rem 0 .3rem;}
.footer{display:flex;justify-content:space-between;align-items:center;padding-top:1rem;border-top:1px solid var(--bdr);margin-top:.5rem;}
.ftxt{font-size:.67rem;color:var(--muted);}
/* banner de acionamento */
.acion-banner{display:flex;align-items:center;justify-content:space-between;
  background:#f0fdf4;border:1px solid #bbf7d0;border-radius:6px;
  padding:10px 16px;margin:1rem 0 .5rem;}
.acion-banner-warn{background:#fff7ed;border-color:#fed7aa;}
.acion-txt{font-size:.82rem;color:#2d6a4f;font-weight:600;}
.acion-txt-warn{color:#92400e;}
</style>
""", unsafe_allow_html=True)

# ── CONSTANTES ────────────────────────────────────────────────────────────────
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
    "🚨 ABAIXO FORECAST + DESACEL - URGENTE": {"short":"Urgente",      "badge":"b-urg","dot":"#c0392b"},
    "⚠️ ABAIXO FORECAST - PROXIMA VIAGEM":    {"short":"Atenção",      "badge":"b-atn","dot":"#d35400"},
    "🔴 LOTANDO - REVISAR PREÇO":              {"short":"Lotando",      "badge":"",     "dot":"#e74c3c"},
    "🟢 ACELERANDO - OPORTUNIDADE":            {"short":"Oportunidade", "badge":"b-opp","dot":"#2d6a4f"},
    "🟡 ACELERANDO - MONITORAR":               {"short":"Monitorar",    "badge":"",     "dot":"#b7950b"},
    "🔵 DESACELERANDO":                        {"short":"Desacel.",     "badge":"",     "dot":"#2c3e7a"},
    "⚪ NORMAL":                               {"short":"Normal",       "badge":"",     "dot":"#b8b8b0"},
}

# ── LOAD ──────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data(url: str) -> pd.DataFrame:
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        df = pd.read_csv(io.StringIO(r.text))
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

def prep_acel(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return df
    df = df.copy()
    int_cols   = ["pax","capacidade_atual","assentos_disponiveis","pax_d1","pax_d2","pax_d3","pax_d4","pax_d5",
                  "pax_hoje_parcial","predict_consenso","pax_faltam_forecast","predict_time_series","predict_eixo_sentido"]
    float_cols = ["occ_atual","tkm_comp","aceleracao_pct","aceleracao_abs","tendencia_linear",
                  "pct_atingimento_forecast","media_d2_d5","load_factor_atual"]
    for c in int_cols:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
    for c in float_cols:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce")
    if "data" in df.columns: df["data"] = pd.to_datetime(df["data"])
    return df

def prep_curva(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return df
    df = df.copy()
    float_cols = ["occ_atual","lf_pascoa_2026","lf_atual","ratio","tkm_comp",
                  "preco_base","preco_est_draft","preco_praticado","mult_final","price_cc",
                  "tkm_atual","mult_flutuacao","preco_com_flutuacao"]
    for c in float_cols:
        if c in df.columns: df[c] = pd.to_numeric(df[c].replace("null", None), errors="coerce")
    for c in ["pax","capacidade_atual","vagas_restantes","antecedencia"]:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
    if "data" in df.columns: df["data"] = pd.to_datetime(df["data"])
    return df

# ── SCORE ─────────────────────────────────────────────────────────────────────
def calcular_score(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    fc        = df["pct_atingimento_forecast"].fillna(0).clip(0, 150) / 150
    occ       = df["occ_atual"].fillna(0).clip(0, 1)
    acel      = df["aceleracao_pct"].fillna(0).clip(-100, 200)
    a_min, a_max = acel.min(), acel.max()
    acel_norm = (acel - a_min) / (a_max - a_min + 1e-9)
    df["_score"] = (0.45 * occ) + (0.35 * fc) + (0.20 * acel_norm)
    return df

# ── HELPERS HTML ──────────────────────────────────────────────────────────────
def sinal_tag(sinal):
    m = SINAL_META.get(sinal, SINAL_META["⚪ NORMAL"])
    if m["badge"]: return f'<span class="badge {m["badge"]}">{m["short"]}</span>'
    return f'<span class="sinal-tag"><span class="sinal-dot" style="background:{m["dot"]}"></span>{m["short"]}</span>'

def occ_html(v):
    try:
        pct = min(float(v)*100, 100)
        col = "#c0392b" if pct>=90 else ("#d35400" if pct>=70 else "#2d6a4f")
        return (f'<div class="occ-row"><div class="occ-track">'
                f'<div class="occ-fill" style="width:{pct:.0f}%;background:{col}"></div></div>'
                f'<span class="om" style="color:{col}">{pct:.0f}%</span></div>')
    except: return "—"

def spark_html(d5, d4, d3, d2, d1):
    vals = [float(x) if str(x) not in ("nan","") else 0 for x in [d5,d4,d3,d2,d1]]
    mx   = max(vals) if max(vals)>0 else 1
    up   = vals[-1] >= (sum(vals[:-1])/max(len(vals)-1,1))
    bars = ""
    for i,v in enumerate(vals):
        h = max(int((v/mx)*20), 2)
        last = (i==4)
        cls  = ("su sl" if up else "sd sl") if last else ("su" if up else "sd")
        bars += f'<div class="sb {cls}" style="height:{h}px" title="D{5-i}: {v:.0f}"></div>'
    return f'<div class="spark">{bars}</div>'

def acel_html(pct):
    try:
        v = float(pct)
        if v>30:  return f'<span class="ng">+{v:.0f}%</span>'
        if v<-30: return f'<span class="nr">{v:.0f}%</span>'
        return f'<span class="nm">{v:.0f}%</span>'
    except: return '<span class="nm">—</span>'

def fc_html(pct, faltam):
    try:
        v   = float(pct)
        cls = "nr" if v<50 else ("no" if v<80 else "ng")
        ft  = (f'<br><span class="nm" style="font-size:.62rem">faltam {int(faltam)}</span>'
               if str(faltam) not in ("nan","") else "")
        return f'<span class="{cls}">{v:.0f}%</span>{ft}'
    except: return "—"

def tend_html(v):
    try:
        f = float(v)
        if f>0.5:  return f'<span class="ng">↑ {f:.1f}</span>'
        if f<-0.5: return f'<span class="nr">↓ {f:.1f}</span>'
        return f'<span class="nm">→ {f:.1f}</span>'
    except: return '<span class="nm">—</span>'

def mono_html(v, prefix="", suffix="", dec=0):
    try:
        if str(v) in ("nan",""): return '<span class="nm">—</span>'
        return f'<span class="nt">{prefix}{float(v):,.{dec}f}{suffix}</span>'
    except: return '<span class="nm">—</span>'

def score_bar(score):
    try:
        pct = min(float(score)*100, 100)
        return (f'<div class="score-wrap"><div class="score-track">'
                f'<div class="score-fill" style="width:{pct:.0f}%"></div></div>'
                f'<span class="score-val">{pct:.0f}</span></div>')
    except: return "—"

def lf_bar(v, ref=None):
    try:
        pct   = min(float(v)*100, 100)
        ref_f = float(ref) if ref is not None and str(ref) not in ("nan","") else None
        col   = "#2d6a4f" if (ref_f is None or float(v) >= ref_f) else "#c0392b"
        return (f'<div class="occ-row"><div class="occ-track" style="width:52px">'
                f'<div class="occ-fill" style="width:{pct:.0f}%;background:{col}"></div></div>'
                f'<span class="om" style="color:{col}">{float(v):.0%}</span></div>')
    except: return "—"

def ratio_html(v):
    try:
        f = float(v)
        if f>=1.2: return f'<span class="ng" style="font-weight:700">{f:.2f}x</span>'
        if f>=1.0: return f'<span class="ng">{f:.2f}x</span>'
        if f>=0.8: return f'<span class="no">{f:.2f}x</span>'
        return f'<span class="nr">{f:.2f}x</span>'
    except: return "—"

def turno_badge(t):
    cores = {"MANHA":"#f97316","TARDE":"#2563eb","NOITE":"#7c3aed","MADRUGADA":"#374151"}
    cor   = cores.get(str(t).upper(), "#8c8c84")
    return (f'<span style="display:inline-block;padding:1px 7px;border-radius:3px;'
            f'font-size:.61rem;font-weight:600;background:{cor}18;color:{cor};'
            f'border:1px solid {cor}33">{t}</span>')

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="padding:14px 0 6px"><div class="sb-label">Aceleração PAX · URL</div></div>',
                unsafe_allow_html=True)
    url_acel = st.text_input("", value=GITHUB_RAW_ACEL, label_visibility="collapsed", key="url_acel")
    st.markdown('<div class="sb-label" style="margin-top:8px">Curva de Feriado · URL</div>', unsafe_allow_html=True)
    url_curva = st.text_input("", value=GITHUB_RAW_CURVA, label_visibility="collapsed", key="url_curva")

    if st.button("↻  Recarregar dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    df_acel_raw  = prep_acel(load_data(url_acel))
    df_curva_raw = prep_curva(load_data(url_curva))

    st.markdown('<div style="margin-top:18px;padding-top:18px;border-top:1px solid #e2e1dc">'
                '<div style="font-size:.7rem;font-weight:700;color:#8c8c84;letter-spacing:1.5px;'
                'text-transform:uppercase;margin-bottom:12px">Filtros · Aceleração</div></div>',
                unsafe_allow_html=True)
    datas_disp = sorted(df_acel_raw["data"].dt.date.unique()) if not df_acel_raw.empty else []
    st.markdown('<div class="sb-label">Data de viagem</div>', unsafe_allow_html=True)
    datas_sel  = st.multiselect("", options=datas_disp, default=datas_disp,
                                format_func=lambda d: d.strftime("%d/%m/%Y"),
                                label_visibility="collapsed", key="datas_acel")
    st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-label">Antecedência (dias)</div>', unsafe_allow_html=True)
    if not df_acel_raw.empty:
        ant_min = int(df_acel_raw["antecedencia"].min())
        ant_max = int(df_acel_raw["antecedencia"].max())
    else:
        ant_min, ant_max = 0, 30
    ant_range = st.slider("", ant_min, ant_max, (ant_min, ant_max), label_visibility="collapsed")
    st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-label">Buscar rota</div>', unsafe_allow_html=True)
    rota_busca  = st.text_input("", placeholder="ex: SAO-RIO", label_visibility="collapsed", key="rota_acel")
    hide_normal = st.checkbox("Ocultar rotas Normais", value=True)

    st.markdown(
        '<div style="margin-top:18px;padding-top:16px;border-top:1px solid #e2e1dc">'
        '<div style="font-size:.7rem;font-weight:700;color:#8c8c84;letter-spacing:1.5px;'
        'text-transform:uppercase;margin-bottom:10px">Legenda</div>'
        '<div style="font-size:.7rem;color:#8c8c84">'
        '<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #eeede9">'
        '<span>D1</span><span style="color:#3d3d38;font-weight:500">ontem completo</span></div>'
        '<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #eeede9">'
        '<span>D5</span><span style="color:#3d3d38;font-weight:500">5 dias atrás</span></div>'
        '<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #eeede9">'
        '<span>Acel</span><span style="color:#3d3d38;font-weight:500">D1 vs média D2–D5</span></div>'
        '<div style="display:flex;justify-content:space-between;padding:4px 0">'
        '<span>Score</span><span style="color:#3d3d38;font-weight:500">45% occ · 35% fc · 20% acel</span></div>'
        '</div></div>',
        unsafe_allow_html=True,
    )

# ── FILTRAR ACELERAÇÃO ────────────────────────────────────────────────────────
df_base = df_acel_raw.copy() if not df_acel_raw.empty else pd.DataFrame()
if not df_base.empty:
    if datas_sel:
        df_base = df_base[df_base["data"].dt.date.isin(datas_sel)]
    df_base = df_base[df_base["antecedencia"].between(ant_range[0], ant_range[1])]
    if rota_busca:
        df_base = df_base[df_base["sentido"].str.upper().str.contains(rota_busca.upper(), na=False)]
    if hide_normal:
        df_base = df_base[df_base["sinal"] != "⚪ NORMAL"]

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🚦  Aceleração PAX", "📈  Curva de Feriado"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — ACELERAÇÃO PAX
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    st.markdown(f"""
    <div class="pg-header">
      <div>
        <div class="pg-title">Farol de Aceleração PAX</div>
        <div class="pg-sub">Monitoramento de velocidade de reservas por rota · {len(df_base)} rotas visíveis</div>
      </div>
      <div class="upill"><span class="dot"></span>Atualizado em {agora} · via Databricks</div>
    </div>
    """, unsafe_allow_html=True)

    if df_acel_raw.empty:
        st.info("Nenhum dado de aceleração. Verifique a URL na sidebar.")
    else:
        def cnt_kw(kw): return int(df_acel_raw["sinal"].str.contains(kw, na=False).sum())
        kpis = [
            ("URGENTE",      cnt_kw("URGENTE"),      "#c0392b", "c-red"),
            ("ATENÇÃO",      cnt_kw("PROXIMA"),       "#d35400", "c-ora"),
            ("LOTANDO",      cnt_kw("LOTANDO"),       "#e74c3c", "c-red2"),
            ("OPORTUNIDADE", cnt_kw("OPORTUNIDADE"), "#2d6a4f", "c-grn"),
            ("MONITORAR",    cnt_kw("MONITORAR"),     "#b7950b", "c-yel"),
            ("DESACEL.",     cnt_kw("DESACEL"),       "#2c3e7a", "c-blu"),
            ("TOTAL ROTAS",  len(df_acel_raw),        "#b8b8b0", "c-mut"),
        ]
        strip = '<div class="kpi-strip" style="grid-template-columns:repeat(7,1fr)">'
        for lbl, val, dot, cls in kpis:
            zc = " zero" if val == 0 else ""
            strip += (f'<div class="kpi {cls}"><div class="kpi-lbl">'
                      f'<span class="kpi-dot" style="background:{dot}"></span>{lbl}</div>'
                      f'<div class="kpi-val{zc}">{val}</div></div>')
        strip += '</div>'
        st.markdown(strip, unsafe_allow_html=True)

        if "aceleracao_pct" in df_base.columns and not df_base.empty:
            df_ch = df_base.dropna(subset=["aceleracao_pct"]).copy()
            if "media_d2_d5" in df_ch.columns:
                df_ch = df_ch[df_ch["media_d2_d5"] >= 5]
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
                        f'<div style="width:80px;text-align:right;flex-shrink:0">'
                        f'<span class="hbar-lbl">{row["sentido"]}</span>'
                        f'<span class="hbar-date">{dt}</span></div>'
                        f'<div class="hbar-track">'
                        f'<div class="hbar-fill" style="width:{pct_w:.1f}%;background:{color}">'
                        f'<span class="hbar-val">{sign}{v:.0f}%</span></div></div></div>')
            st.markdown(f"""
            <div class="chart-section">
              <div class="section-title">Maiores variações de aceleração</div>
              <div class="section-sub">D1 vs média D2–D5 · mínimo 5 reservas/dia · aceleração limitada a 200%</div>
              <div class="chart-grid">
                <div class="chart-col">
                  <div class="chart-col-title"><span style="background:#2d6a4f"></span>Acelerando</div>
                  {''.join(hbar(r, "#2d6a4f") for _, r in top_up.iterrows())}
                </div>
                <div class="chart-col">
                  <div class="chart-col-title"><span style="background:#c0392b"></span>Desacelerando</div>
                  {''.join(hbar(r, "#c0392b") for _, r in top_down.iterrows())}
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        sinais_pres = sorted(df_base["sinal"].dropna().unique(), key=lambda s: SINAL_ORDER.get(s, 99))
        if "chips" not in st.session_state:
            st.session_state.chips = set(sinais_pres)
        st.session_state.chips = st.session_state.chips.intersection(sinais_pres)
        if not st.session_state.chips:
            st.session_state.chips = set(sinais_pres)

        st.markdown('<div style="border-top:1px solid #e2e1dc;padding-top:12px;margin-bottom:6px"></div>',
                    unsafe_allow_html=True)
        chip_cols = st.columns(len(sinais_pres))
        for i, sinal in enumerate(sinais_pres):
            m     = SINAL_META.get(sinal, SINAL_META["⚪ NORMAL"])
            ativo = sinal in st.session_state.chips
            cnt_s = int((df_base["sinal"] == sinal).sum())
            with chip_cols[i]:
                label = f'● {m["short"]} {cnt_s}' if ativo else f'○ {m["short"]} {cnt_s}'
                if st.button(label, key=f"chip_{i}", use_container_width=True,
                             type="primary" if ativo else "secondary"):
                    if ativo and len(st.session_state.chips) > 1:
                        st.session_state.chips.discard(sinal)
                    else:
                        st.session_state.chips.add(sinal)
                    st.rerun()

        df_view = df_base[df_base["sinal"].isin(st.session_state.chips)].copy()
        df_view = calcular_score(df_view)
        df_view["_sinal_ord"] = df_view["sinal"].map(lambda x: SINAL_ORDER.get(x, 99))
        df_view = df_view.sort_values(["_sinal_ord", "_score"], ascending=[True, False])

        if df_view.empty:
            st.info("Nenhuma rota com os filtros selecionados.")
        else:
            st.markdown("""
            <div class="sort-info">Ordenado por &nbsp;
              <span class="sort-tag">▼ Ocupação</span>
              <span class="sort-tag">▼ Forecast %</span>
              <span class="sort-tag">▼ Aceleração</span>
              &nbsp; dentro de cada grupo · score ponderado 45 / 35 / 20
            </div>""", unsafe_allow_html=True)

            has_d5 = "pax_d5" in df_view.columns
            rows   = ""
            cur    = None
            rank   = {}
            for _, row in df_view.iterrows():
                sinal = row["sinal"]
                if sinal != cur:
                    cur = sinal; rank[cur] = 0
                    m   = SINAL_META.get(cur, SINAL_META["⚪ NORMAL"])
                    cnt_g = int((df_view["sinal"] == cur).sum())
                    rows += (f'<tr class="grp-sep"><td colspan="14">'
                             f'<span style="display:inline-flex;align-items:center;gap:6px">'
                             f'<span style="width:6px;height:6px;border-radius:50%;background:{m["dot"]};display:inline-block"></span>'
                             f'{cur} &nbsp;·&nbsp; {cnt_g} rota{"s" if cnt_g>1 else ""}'
                             f'</span></td></tr>')
                rank[cur] += 1
                top_cls = " top-row" if rank[cur] <= 3 else ""
                dt  = row["data"].strftime("%d/%m") if pd.notna(row.get("data")) else "—"
                d5  = row.get("pax_d5", 0) if has_d5 else 0
                rows += f"""<tr class="{top_cls}">
                  <td><span style="font-size:.58rem;color:var(--muted2);font-weight:600;margin-right:5px">#{rank[cur]}</span>
                      <span class="rname">{row.get('sentido','—')}</span><br>
                      <span class="rsub">{row.get('rota_principal','')}</span></td>
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
                  <td>{score_bar(row.get('_score',0))}</td>
                  <td>{sinal_tag(str(row.get('sinal','⚪ NORMAL')))}</td>
                </tr>"""

            st.markdown(f"""
            <div class="tbl-wrap"><table class="tbl">
              <thead><tr>
                <th>Rota</th><th>Data</th><th>Antec.</th>
                <th class="sort-active">Ocupação</th>
                <th>PAX</th><th>Assentos liv.</th>
                <th class="sort-active">Forecast %</th>
                <th>D5→D1</th><th class="sort-active">Acel. %</th>
                <th>Tendência</th><th>Ticket</th><th>Predict</th>
                <th class="sort-active">Score</th><th>Sinal</th>
              </tr></thead>
              <tbody>{rows}</tbody>
            </table></div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="footer">
              <span class="ftxt"><strong style="color:var(--txt)">{len(df_view)}</strong> rotas · {len(df_acel_raw)} total</span>
              <span class="ftxt">D1 = ontem completo · Acel = D1 vs média D2–D5 · sem viés de horário</span>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CURVA DE FERIADO + EDITOR DE PRICING
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    agora2 = datetime.now().strftime("%d/%m/%Y %H:%M")
    st.markdown(f"""
    <div class="pg-header">
      <div>
        <div class="pg-title">Curva de Feriado</div>
        <div class="pg-sub">Comparativo de load factor · edite o preço desejado diretamente na tabela</div>
      </div>
      <div class="upill"><span class="dot"></span>Atualizado em {agora2} · via Databricks</div>
    </div>
    """, unsafe_allow_html=True)

    if df_curva_raw.empty:
        st.info("Nenhum dado de curva. Verifique a URL na sidebar.")
    else:
        df_c = df_curva_raw.copy()

        # ── KPIs ──────────────────────────────────────────────────────────────
        lf_med  = df_c["lf_atual"].mean()
        lf_ref  = df_c["lf_pascoa_2026"].mean()
        rat_med = df_c["ratio"].mean()
        acima   = int((df_c["ratio"] >= 1).sum())
        abaixo  = int((df_c["ratio"] < 1).sum())
        rat_cls = "c-grn" if rat_med >= 1 else "c-red"
        rat_dot = "#2d6a4f" if rat_med >= 1 else "#c0392b"

        st.markdown(f"""
        <div class="kpi-strip" style="grid-template-columns:repeat(5,1fr)">
          <div class="kpi c-grn"><div class="kpi-lbl"><span class="kpi-dot" style="background:#2d6a4f"></span>LF Atual médio</div>
            <div class="kpi-val">{lf_med:.0%}</div></div>
          <div class="kpi c-blu"><div class="kpi-lbl"><span class="kpi-dot" style="background:#2c3e7a"></span>LF Referência</div>
            <div class="kpi-val">{lf_ref:.0%}</div></div>
          <div class="kpi {rat_cls}"><div class="kpi-lbl"><span class="kpi-dot" style="background:{rat_dot}"></span>Ratio médio</div>
            <div class="kpi-val">{rat_med:.2f}</div></div>
          <div class="kpi c-grn"><div class="kpi-lbl"><span class="kpi-dot" style="background:#2d6a4f"></span>Acima da ref.</div>
            <div class="kpi-val">{acima}</div></div>
          <div class="kpi c-red"><div class="kpi-lbl"><span class="kpi-dot" style="background:#c0392b"></span>Abaixo da ref.</div>
            <div class="kpi-val">{abaixo}</div></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Gráfico ───────────────────────────────────────────────────────────
        df_chart = (df_c.groupby("sentido")
                    .agg(lf_atual=("lf_atual","mean"), lf_ref=("lf_pascoa_2026","mean"),
                         ratio=("ratio","mean"), occ=("occ_atual","mean"))
                    .reset_index().sort_values("occ", ascending=False).head(12))
        max_lf = max(df_chart["lf_atual"].max(), df_chart["lf_ref"].max(), 0.01)
        chart_rows = ""
        for _, r in df_chart.iterrows():
            lf_a  = float(r["lf_atual"]) if pd.notna(r["lf_atual"]) else 0
            lf_r  = float(r["lf_ref"])   if pd.notna(r["lf_ref"])   else 0
            rat   = float(r["ratio"])    if pd.notna(r["ratio"])    else 0
            w_a   = min(lf_a / max_lf * 100, 100)
            w_r   = min(lf_r / max_lf * 100, 100)
            col_a = "#2d6a4f" if lf_a >= lf_r else "#c0392b"
            rat_c = "ng" if rat >= 1 else "nr"
            chart_rows += (
                f'<div class="hbar-row">'
                f'<div style="width:80px;text-align:right;flex-shrink:0"><span class="hbar-lbl">{r["sentido"]}</span></div>'
                f'<div style="flex:1;display:flex;flex-direction:column;gap:3px">'
                f'<div class="hbar-track" style="height:13px">'
                f'<div class="hbar-fill" style="width:{w_a:.1f}%;background:{col_a}">'
                f'<span class="hbar-val" style="font-size:.6rem">{lf_a:.0%}</span></div></div>'
                f'<div class="hbar-track" style="height:13px;background:#e8e8ed">'
                f'<div class="hbar-fill" style="width:{w_r:.1f}%;background:#9ab8d4">'
                f'<span class="hbar-val" style="font-size:.6rem;color:#1a1a18">{lf_r:.0%}</span></div></div>'
                f'</div>'
                f'<div style="width:44px;text-align:right;flex-shrink:0">'
                f'<span class="{rat_c}" style="font-size:.76rem">{rat:.2f}x</span></div></div>'
            )
        st.markdown(f"""
        <div class="chart-section">
          <div class="section-title">LF Atual vs Referência — top rotas por ocupação</div>
          <div class="section-sub">
            <span style="display:inline-flex;align-items:center;gap:5px;margin-right:14px">
              <span style="width:10px;height:3px;background:#2d6a4f;border-radius:2px;display:inline-block"></span>LF Atual
            </span>
            <span style="display:inline-flex;align-items:center;gap:5px">
              <span style="width:10px;height:3px;background:#9ab8d4;border-radius:2px;display:inline-block"></span>LF Referência (Páscoa)
            </span>
          </div>
          <div class="chart-col" style="margin-top:12px;max-width:700px">{chart_rows}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Filtros ───────────────────────────────────────────────────────────
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            datas_c     = sorted(df_c["data"].dt.date.unique())
            datas_c_sel = st.multiselect("Data", options=datas_c, default=datas_c,
                                         format_func=lambda d: d.strftime("%d/%m"), key="datas_curva")
        with col_f2:
            turnos_c   = sorted(df_c["turno"].dropna().unique())
            turnos_sel = st.multiselect("Turno", options=turnos_c, default=turnos_c, key="turnos_curva")
        with col_f3:
            rota_c = st.text_input("Buscar rota", placeholder="ex: BHZ-RIO", key="rota_curva")

        df_cv = df_c.copy()
        if datas_c_sel: df_cv = df_cv[df_cv["data"].dt.date.isin(datas_c_sel)]
        if turnos_sel:  df_cv = df_cv[df_cv["turno"].isin(turnos_sel)]
        if rota_c:      df_cv = df_cv[df_cv["sentido"].str.upper().str.contains(rota_c.upper(), na=False)]
        df_cv = df_cv.sort_values(["occ_atual","ratio"], ascending=[False, False]).reset_index(drop=True)

        # ── EDITOR DE PRICING ────────────────────────────────────────────────
        st.markdown("""
        <div style="margin:1.2rem 0 .4rem">
          <div class="section-title" style="font-size:.95rem">Editor de Pricing</div>
          <div class="section-sub">
            Preencha <strong>✏️ Preço novo</strong> nas linhas que deseja alterar.
            O mult é calculado automaticamente. Linhas sem preço novo são ignoradas.
            Use o botão <strong>Reset</strong> para limpar todas as edições.
          </div>
        </div>
        """, unsafe_allow_html=True)

        # chave de versão — mudar força recriação do editor
        if "editor_version" not in st.session_state:
            st.session_state.editor_version = 0

        # monta df para o editor com TODAS as colunas relevantes
        cols_editor = [
            "data", "turno", "rota_principal", "sentido",
            "occ_atual", "pax", "vagas_restantes",
            "lf_atual", "lf_pascoa_2026", "ratio",
            "tkm_atual", "tkm_comp", "price_cc",
            "preco_praticado", "preco_com_flutuacao",
            "mult_final", "mult_flutuacao",
            "antecedencia",
        ]
        cols_presentes = [c for c in cols_editor if c in df_cv.columns]
        df_editor = df_cv[cols_presentes].copy()

        # formata colunas de exibição
        df_editor["data_fmt"] = pd.to_datetime(df_editor["data"]).dt.strftime("%d/%m/%Y")
        if "occ_atual"       in df_editor.columns: df_editor["occ_pct"]  = (df_editor["occ_atual"]       * 100).round(1).astype(str) + "%"
        if "lf_atual"        in df_editor.columns: df_editor["lf_a_fmt"] = (df_editor["lf_atual"]        * 100).round(1).astype(str) + "%"
        if "lf_pascoa_2026"  in df_editor.columns: df_editor["lf_r_fmt"] = (df_editor["lf_pascoa_2026"]  * 100).round(1).astype(str) + "%"
        if "ratio"           in df_editor.columns: df_editor["ratio_fmt"]= df_editor["ratio"].round(3).astype(str) + "x"

        # coluna editável — preço novo (começa None)
        df_editor["✏️ Preço novo"] = None

        # colunas que aparecem no editor (ordem visual)
        show_cols = (
            ["data_fmt","turno","rota_principal","sentido","antecedencia",
             "occ_pct","pax","vagas_restantes",
             "lf_a_fmt","lf_r_fmt","ratio_fmt",
             "tkm_atual","tkm_comp","price_cc",
             "preco_praticado","preco_com_flutuacao",
             "mult_final","mult_flutuacao",
             "✏️ Preço novo"]
        )
        show_cols = [c for c in show_cols if c in df_editor.columns]
        df_show   = df_editor[show_cols].copy()

        col_config = {
            "data_fmt":            st.column_config.TextColumn("Data",            disabled=True),
            "turno":               st.column_config.TextColumn("Turno",           disabled=True),
            "rota_principal":      st.column_config.TextColumn("Rota principal",  disabled=True),
            "sentido":             st.column_config.TextColumn("Sentido",         disabled=True),
            "antecedencia":        st.column_config.NumberColumn("Antec.",        disabled=True),
            "occ_pct":             st.column_config.TextColumn("Occ",             disabled=True),
            "pax":                 st.column_config.NumberColumn("PAX",           disabled=True),
            "vagas_restantes":     st.column_config.NumberColumn("Vagas rest.",   disabled=True),
            "lf_a_fmt":            st.column_config.TextColumn("LF Atual",        disabled=True),
            "lf_r_fmt":            st.column_config.TextColumn("LF Ref",          disabled=True),
            "ratio_fmt":           st.column_config.TextColumn("Ratio",           disabled=True),
            "tkm_atual":           st.column_config.NumberColumn("TKM Atual",     disabled=True, format="R$ %.0f"),
            "tkm_comp":            st.column_config.NumberColumn("TKM Comp",      disabled=True, format="R$ %.0f"),
            "price_cc":            st.column_config.NumberColumn("Price CC",      disabled=True, format="R$ %.0f"),
            "preco_praticado":     st.column_config.NumberColumn("Preço prat.",   disabled=True, format="R$ %.2f"),
            "preco_com_flutuacao": st.column_config.NumberColumn("Preço c/ flut.",disabled=True, format="R$ %.2f"),
            "mult_final":          st.column_config.NumberColumn("Mult Final",    disabled=True, format="%.3fx"),
            "mult_flutuacao":      st.column_config.NumberColumn("Mult Flut.",    disabled=True, format="%.3fx"),
            "✏️ Preço novo": st.column_config.NumberColumn(
                "✏️ Preço novo",
                help="Digite o preço desejado — mult será calculado automaticamente",
                min_value=0.0,
                format="R$ %.2f",
            ),
        }

        edited = st.data_editor(
            df_show,
            use_container_width=True,
            hide_index=True,
            column_config=col_config,
            num_rows="fixed",
            key=f"pricing_editor_{st.session_state.editor_version}",
        )

        # ── PREVIEW DO ACIONAMENTO ────────────────────────────────────────────
        df_editado = edited[edited["✏️ Preço novo"].notna()].copy()

        if not df_editado.empty:
            # recupera preco_praticado original pelo índice
            df_editado["_preco_prat"] = df_cv.loc[df_editado.index, "preco_praticado"].values
            df_editado["mult_novo"]   = (df_editado["✏️ Preço novo"] / df_editado["_preco_prat"]).round(6)

            df_acionamento = pd.DataFrame({
                "data":            pd.to_datetime(df_editado["data_fmt"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d"),
                "turno":           df_editado["turno"].values,
                "rota_principal":  df_editado["rota_principal"].values,
                "sentido":         df_editado["sentido"].values,
                "preco_praticado": df_editado["_preco_prat"].values,
                "preco_novo":      df_editado["✏️ Preço novo"].values,
                "mult":            df_editado["mult_novo"].values,
            })

            n_edit = len(df_acionamento)
            st.markdown(f"""
            <div class="acion-banner">
              <span class="acion-txt">✅ {n_edit} linha{"s" if n_edit>1 else ""} com preço editado · pronto para enviar</span>
            </div>
            """, unsafe_allow_html=True)

            st.dataframe(df_acionamento, use_container_width=True, hide_index=True)

            # botões de ação
            col_b1, col_b2, col_b3, _ = st.columns([1, 1, 1, 3])

            with col_b1:
                csv_bytes = df_acionamento.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇ Baixar CSV",
                    data=csv_bytes,
                    file_name=f"pricing_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            with col_b2:
                if st.button("🚀 Enviar pro GitHub", use_container_width=True,
                             type="primary", key="push_pricing"):
                    gh_token = st.session_state.get("gh_token_pricing", "")
                    if not gh_token:
                        st.warning("Cole seu token no campo abaixo.")
                    else:
                        repo   = "meninosia2026-beep/aceleracao_vendas"
                        branch = "main"
                        path   = f"data/pricing_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
                        url_gh = f"https://api.github.com/repos/{repo}/contents/{path}"
                        hdrs   = {"Authorization": f"token {gh_token}", "Accept": "application/vnd.github.v3+json"}
                        enc    = base64.b64encode(csv_bytes).decode("utf-8")
                        r_gh   = requests.put(url_gh, headers=hdrs,
                                              data=json.dumps({"message": f"pricing: {path}",
                                                               "content": enc, "branch": branch}))
                        if r_gh.status_code in (200, 201):
                            st.success(f"✅ Enviado: {path}")
                        else:
                            st.error(f"Erro {r_gh.status_code}: {r_gh.json().get('message')}")

            with col_b3:
                if st.button("🔄 Reset edições", use_container_width=True, key="reset_pricing"):
                    st.session_state.editor_version += 1
                    st.rerun()

            with st.expander("🔑 GitHub Token para envio"):
                st.text_input("Token", type="password", key="gh_token_pricing",
                              help="Necessário só para 'Enviar pro GitHub'. Fica apenas na sessão.")

        else:
            # sem edições — mostra botão de reset só se houve edição anterior
            st.markdown("""
            <div style="margin-top:.8rem;padding:10px 16px;background:var(--bg2);
                        border:1px solid var(--bdr);border-radius:6px">
              <span style="font-size:.82rem;color:var(--muted)">
                Preencha <strong>✏️ Preço novo</strong> nas linhas que deseja alterar para gerar o acionamento.
              </span>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🔄 Reset edições", key="reset_pricing_empty"):
                st.session_state.editor_version += 1
                st.rerun()

        st.markdown(f"""
        <div class="footer">
          <span class="ftxt"><strong style="color:var(--txt)">{len(df_cv)}</strong> linhas · {len(df_curva_raw)} total</span>
          <span class="ftxt">mult = preço novo / preço praticado · só linhas editadas entram no acionamento</span>
        </div>""", unsafe_allow_html=True)
