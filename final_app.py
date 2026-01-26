import streamlit as st

# --- SAYFA AYARLARI (APP GÖRÜNÜMÜ) ---
st.set_page_config(
    page_title="Finans Pro Global",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS İLE MODERN MOBİL TASARIM ---
st.markdown("""
<style>
    /* Gereksiz boşlukları al */
    .block-container {padding-top: 1rem; padding-bottom: 0rem;}
    
    /* Butonları Kart Gibi Yap */
    div.stButton > button:first-child {
        width: 100%;
        height: 4em;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        font-weight: 600;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.2s;
        color: #333;
    }
    div.stButton > button:hover {
        background-color: #f8f9fa;
        border-color: #007bff;
        color: #007bff;
        transform: translateY(-2px);
    }
    
    /* Metrik Kutuları */
    div[data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        color: #007bff;
    }
</style>
""", unsafe_allow_html=True)

# --- DİL SÖZLÜĞÜ (4 DİL) ---
TRANSLATIONS = {
    "TR": {
        "flag": "🇹🇷",
        "welcome": "Finansal Kontrol Merkezi",
        "subtitle": "Kişisel ve Kurumsal Finans Yönetimi",
        "menu_home": "🏠 Ana Menü",
        "menu_eurobond": "🌍 Eurobond Analizi",
        "menu_coming_soon": "🔜 Yakında",
        "lang_select": "Dil Seçimi",
        "eb_title": "Eurobond Vergi Analizi 2025",
        "eb_income": "Yıllık Toplam Kupon Geliri ($)",
        "eb_rate": "Ortalama Dolar Kuru",
        "eb_btn": "HESAPLA",
        "eb_result": "TL Karşılığı",
        "eb_safe": "✅ GÜVENLİ: {limit} TL sınırı aşılmadı. Beyan gerekmez.",
        "eb_risk": "⚠️ DİKKAT: {limit} TL sınırı aşıldı! Beyanname vermelisiniz.",
        "footer": "Eczacıbaşı & Sanofi Staj Projesi"
    },
    "EN": {
        "flag": "🇬🇧",
        "welcome": "Financial Control Center",
        "subtitle": "Personal & Corporate Finance Management",
        "menu_home": "🏠 Home Menu",
        "menu_eurobond": "🌍 Eurobond Analysis",
        "menu_coming_soon": "🔜 Coming Soon",
        "lang_select": "Language",
        "eb_title": "Eurobond Tax Analysis 2025",
        "eb_income": "Total Annual Coupon Income ($)",
        "eb_rate": "Avg. Exchange Rate",
        "eb_btn": "ANALYZE",
        "eb_result": "TRY Equivalent",
        "eb_safe": "✅ SAFE: Limit of {limit} TL not exceeded.",
        "eb_risk": "⚠️ WARNING: Limit of {limit} TL exceeded! Declaration required.",
        "footer": "Developed for Eczacıbaşı & Sanofi Internship"
    },
    "FR": {
        "flag": "🇫🇷",
        "welcome": "Centre de Contrôle Financier",
        "subtitle": "Gestion Financière Personnelle et Entreprise",
        "menu_home": "🏠 Menu Principal",
        "menu_eurobond": "🌍 Analyse Eurobond",
        "menu_coming_soon": "🔜 Bientôt",
        "lang_select": "Langue",
        "eb_title": "Analyse Fiscale Eurobond 2025",
        "eb_income": "Revenu Annuel Total ($)",
        "eb_rate": "Taux de Change Moyen",
        "eb_btn": "ANALYSER",
        "eb_result": "Équivalent TRY",
        "eb_safe": "✅ SÛR : Limite de {limit} TL non dépassée.",
        "eb_risk": "⚠️ ATTENTION : Limite de {limit} TL dépassée !",
        "footer": "Projet de Stage Eczacıbaşı & Sanofi"
    },
    "DE": {
        "flag": "🇩🇪",
        "welcome": "Finanzkontrollzentrum",
        "subtitle": "Persönliches & Unternehmensfinanzmanagement",
        "menu_home": "🏠 Hauptmenü",
        "menu_eurobond": "🌍 Eurobond-Analyse",
        "menu_coming_soon": "🔜 Bald",
        "lang_select": "Sprache",
        "eb_title": "Eurobond-Steueranalyse 2025",
        "eb_income": "Jährliche Kupon-Einnahmen ($)",
        "eb_rate": "Wechselkurs",
        "eb_btn": "ANALYSIEREN",
        "eb_result": "TRY-Gegenwert",
        "eb_safe": "✅ SICHER: Grenze von {limit} TL nicht überschritten.",
        "eb_risk": "⚠️ ACHTUNG: Grenze von {limit} TL überschritten!",
        "footer": "Eczacıbaşı & Sanofi Praktikumsprojekt"
    }
}

# --- OTURUM YÖNETİMİ ---
if 'lang' not in st.session_state:
    st.session_state.lang = "TR"
if 'page' not in st.session_state:
    st.session_state.page = "home"

def set_lang():
    selected_flag = st.session_state.lang_selector.split(" ")[0]
    for code, data in TRANSLATIONS.items():
        if data["flag"] == selected_flag:
            st.session_state.lang = code
            break

def go_to(page):
    st.session_state.page = page
    st.rerun()

def t(key):
    return TRANSLATIONS[st.session_state.lang][key]

# --- ÜST BAR (Dil Seçimi) ---
col1, col2 = st.columns([3, 1])
with col1:
    st.caption(t("footer"))
with col2:
    options = [f"{TRANSLATIONS[c]['flag']} {c}" for c in TRANSLATIONS.keys()]
    idx = list(TRANSLATIONS.keys()).index(st.session_state.lang)
    st.selectbox("", options, index=idx, key="lang_selector", on_change=set_lang, label_visibility="collapsed")

st.divider()

# --- SAYFA 1: ANA MENÜ ---
if st.session_state.page == "home":
    st.title(t("welcome"))
    st.markdown(f"*{t('subtitle')}*")
    st.write("")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button(f"{t('menu_eurobond')}\n➡️", use_container_width=True):
            go_to("eurobond")
        st.button(f"📊 {t('menu_coming_soon')}", disabled=True, use_container_width=True)
    with c2:
        st.button(f"💳 {t('menu_coming_soon')}", disabled=True, use_container_width=True)
        st.button(f"💰 {t('menu_coming_soon')}", disabled=True, use_container_width=True)

# --- SAYFA 2: EUROBOND ---
elif st.session_state.page == "eurobond":
    if st.button("⬅️ " + t("menu_home")):
        go_to("home")
    
    st.subheader(t("eb_title"))
    
    with st.container():
        gelir = st.number_input(t("eb_income"), value=6000.0, step=100.0)
        kur = st.number_input(t("eb_rate"), value=34.5, step=0.1)
    
    st.write("")
    if st.button(t("eb_btn"), type="primary", use_container_width=True):
        tl = gelir * kur
        sinir = 150000
        limit_txt = f"{sinir:,.0f}"
        
        st.metric(t("eb_result"), f"{tl:,.2f} ₺")
        
        if tl > sinir:
            st.error(t("eb_risk").format(limit=limit_txt))
        else:
            st.success(t("eb_safe").format(limit=limit_txt))
