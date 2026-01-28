import streamlit as st
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Finansal Hesap Makinesi",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# LANG DICTS
# =========================================================
TR = {
    "app_name": "Finansal Hesap Makinesi",
    "subheader": "Eczacıbaşı Sağlık Hazine Departmanı",
    "home": "🏠 Ana Menü",
    "mode_toggle": "🌙 Gece Modu",

    "m_rates": "Basit - Bileşik Faiz",
    "rt_what": "Ne Hesaplayalım?",
    "rt_days": "Gün Sayısı",
    "rt_base": "Baz Oran (%)",
    "opt_comp_rate": "Yıllık Bileşik Faiz (%)",
    "opt_simp_rate": "Yıllık Basit Faiz (%)",
    "rt_res": "Hesaplanan Oran",
    "calc": "HESAPLA",
}

LANGS = {"TR": TR}

# =========================================================
# HELPERS
# =========================================================
def T(k): 
    return LANGS[st.session_state.lang].get(k, k)

def qp_get(k, d):
    try:
        return st.query_params.get(k, d)
    except:
        return d

def qp_set(**kw):
    try:
        for k, v in kw.items():
            st.query_params[k] = v
    except:
        pass

def go(p):
    st.session_state.page = p
    qp_set(page=p)
    st.rerun()

# =========================================================
# STATE INIT
# =========================================================
if "page" not in st.session_state:
    st.session_state.page = qp_get("page", "home")

if "lang" not in st.session_state:
    st.session_state.lang = "TR"

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = (qp_get("dark", "0") == "1")

def on_dark():
    qp_set(dark="1" if st.session_state.dark_mode else "0")

is_dark = st.session_state.dark_mode

# =========================================================
# COLORS
# =========================================================
if is_dark:
    bg = "#0e1117"
    card = "#1f2430"
    text = "#ffffff"
    input_bg = "#121622"
    border = "#3b4252"
else:
    bg = "#ffffff"
    card = "#f6f7fb"
    text = "#111827"
    input_bg = "#ffffff"
    border = "#e5e7eb"

# =========================================================
# CSS (FINAL – TEMİZ)
# =========================================================
st.markdown(f"""
<style>
.stApp {{
  background:{bg};
  color:{text};
}}

.block-container {{
  padding-top:0.4rem;
  max-width:1240px;
}}

h1,h2,h3,p,label,span {{
  color:{text}!important;
  opacity:1!important;
}}

div[data-testid="stVerticalBlockBorderWrapper"] {{
  background:{card};
  border:1px solid {border};
  border-radius:14px;
}}

.stNumberInput input {{
  background:{input_bg};
  color:{text}!important;
  border:1px solid {border};
  border-radius:12px;
  font-weight:700;
}}

div[data-testid="stSelectbox"] div[data-baseweb="select"] {{
  background:{input_bg};
  border:1px solid {border};
  border-radius:12px;
}}

div[data-testid="stSelectbox"] div[data-baseweb="select"] * {{
  color:{text}!important;
  opacity:1!important;
}}

div[data-testid="stSelectbox"] svg {{
  fill:{text}!important;
}}

div[role="listbox"] * {{
  color:{text}!important;
}}

div.stButton > button {{
  background:{card};
  color:{text};
  border:1px solid {border};
  border-radius:12px;
  font-weight:700;
}}

div.stButton > button:hover {{
  border-color:#0d6efd;
  color:#0d6efd;
}}

/* ===== STICKY BAR ===== */
div[data-testid="stVerticalBlock"] > div:has(.topbar) {{
  position:sticky;
  top:64px;
  z-index:999;
  background:{card};
  border:1px solid {border};
  border-radius:14px;
  padding:0.25rem 0.6rem;
  margin-bottom:0.6rem;
}}

.topbar-title {{
  font-weight:900;
  font-size:1.05rem;
}}

/* ===== DARK MODE SWITCH (ONLY ONE) ===== */
div[data-testid="stCheckbox"] > label > div:first-child {{
  display:none!important;
}}

div[data-testid="stCheckbox"] input {{
  appearance:none;
  width:44px;
  height:24px;
  border-radius:999px;
  background:#e5e7eb;
  border:1px solid {border};
  position:relative;
  cursor:pointer;
}}

div[data-testid="stCheckbox"] input:checked {{
  background:#ef4444;
}}

div[data-testid="stCheckbox"] input::after {{
  content:"";
  position:absolute;
  top:2px;
  left:2px;
  width:20px;
  height:20px;
  border-radius:999px;
  background:#111827;
  transition:0.15s;
}}

div[data-testid="stCheckbox"] input:checked::after {{
  left:22px;
  background:white;
}}
</style>
""", unsafe_allow_html=True)

# =========================================================
# TOPBAR
# =========================================================
with st.container():
    st.markdown('<div class="topbar"></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([6,2,2])

    with c1:
        st.markdown(f"<div class='topbar-title'>{T('subheader')}</div>", unsafe_allow_html=True)

    with c2:
        st.checkbox(T("mode_toggle"), key="dark_mode", on_change=on_dark)

    with c3:
        st.selectbox("Dil / Language", ["🇹🇷 TR"], key="lang")

# =========================================================
# HOME
# =========================================================
if st.session_state.page == "home":
    st.title(T("app_name"))

    with st.container(border=True):
        if st.button(T("m_rates"), use_container_width=True):
            go("rates")

# =========================================================
# RATES
# =========================================================
elif st.session_state.page == "rates":
    st.title(T("m_rates"))
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox(T("rt_what"), [T("opt_comp_rate"), T("opt_simp_rate")])
        with c2:
            st.number_input(T("rt_days"), value=365)

        st.number_input(T("rt_base"), value=0.0)
        st.button(T("calc"))
