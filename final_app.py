import streamlit as st

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Finans Pro Ultimate",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- TASARIM (MOBİL UYUMLU KARTLAR) ---
st.markdown("""
<style>
    .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    div.stButton > button:first-child {
        width: 100%; height: 3.8em; border-radius: 12px; border: 1px solid #e0e0e0;
        font-weight: 600; background-color: #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        color: #333; transition: all 0.2s;
    }
    div.stButton > button:hover {
        background-color: #f0f8ff; border-color: #007bff; color: #007bff; transform: translateY(-2px);
    }
    div[data-testid="stMetricValue"] { font-size: 1.5rem !important; color: #007bff; }
</style>
""", unsafe_allow_html=True)

# --- DİL SÖZLÜĞÜ (TÜM MODÜLLER İÇİN) ---
TRANSLATIONS = {
    "TR": {
        "flag": "🇹🇷", "home": "🏠 Ana Menü", "lang": "Dil / Language",
        "welcome": "Finansal Kontrol Merkezi", "sub": "Kişisel ve Kurumsal Finans Yönetimi",
        # Menü İsimleri
        "m_euro": "🌍 Eurobond Analizi", "m_credit": "💳 Kredi Hesapla",
        "m_deposit": "💰 Mevduat Getirisi", "m_invest": "📈 Yatırım Getirisi",
        # Eurobond
        "eb_t": "Eurobond Vergi Analizi 2025", "eb_i": "Yıllık Kupon Geliri ($)", 
        "eb_r": "Dolar Kuru", "eb_res": "TL Karşılığı", 
        "eb_ok": "✅ BEYAN GEREKMEZ ({limit} TL altı)", "eb_no": "⚠️ BEYAN GEREKİR ({limit} TL üstü)",
        # Kredi
        "cr_t": "Kredi Geri Ödeme Planı", "cr_amt": "Kredi Tutarı (TL)", 
        "cr_rate": "Aylık Faiz (%)", "cr_term": "Vade (Ay)", 
        "cr_res": "Aylık Taksit", "cr_tot": "Toplam Geri Ödeme",
        # Mevduat
        "dep_t": "Mevduat Faizi Hesapla", "dep_amt": "Ana Para (TL)",
        "dep_rate": "Yıllık Faiz (%)", "dep_days": "Gün Sayısı", "dep_stop": "Stopaj (%)",
        "dep_res": "Net Getiri", "dep_tot": "Vade Sonu Toplam",
        # Yatırım
        "inv_t": "Yatırım Getiri Analizi", "inv_buy": "Alış Fiyatı", "inv_sell": "Satış Fiyatı",
        "inv_days": "Elde Tutma Süresi (Gün)", "inv_res": "Basit Getiri", "inv_ann": "Yıllıklandırılmış Getiri",
        # Genel
        "calc": "HESAPLA", "back": "⬅️ Geri Dön", "footer": "Eczacıbaşı & Sanofi Staj Projesi"
    },
    "EN": {
        "flag": "🇬🇧", "home": "🏠 Home", "lang": "Language",
        "welcome": "Financial Control Center", "sub": "Personal & Corporate Finance Management",
        "m_euro": "🌍 Eurobond Analysis", "m_credit": "💳 Loan Calculator",
        "m_deposit": "💰 Deposit Return", "m_invest": "📈 Investment ROI",
        # Eurobond
        "eb_t": "Eurobond Tax Analysis 2025", "eb_i": "Annual Coupon Income ($)", 
        "eb_r": "Exchange Rate", "eb_res": "TRY Equivalent",
        "eb_ok": "✅ NO DECLARATION NEEDED (< {limit} TL)", "eb_no": "⚠️ DECLARATION REQUIRED (> {limit} TL)",
        # Credit
        "cr_t": "Loan Repayment Plan", "cr_amt": "Loan Amount", 
        "cr_rate": "Monthly Rate (%)", "cr_term": "Term (Months)", 
        "cr_res": "Monthly Payment", "cr_tot": "Total Repayment",
        # Deposit
        "dep_t": "Deposit Interest Calculator", "dep_amt": "Principal Amount",
        "dep_rate": "Annual Rate (%)", "dep_days": "Days", "dep_stop": "Withholding Tax (%)",
        "dep_res": "Net Return", "dep_tot": "Total at Maturity",
        # Investment
        "inv_t": "Investment Return Analysis", "inv_buy": "Buy Price", "inv_sell": "Sell Price",
        "inv_days": "Holding Period (Days)", "inv_res": "Simple Return", "inv_ann": "Annualized Return",
        "calc": "CALCULATE", "back": "⬅️ Back", "footer": "Eczacıbaşı & Sanofi Internship Project"
    },
    "FR": {
        "flag": "🇫🇷", "home": "🏠 Accueil", "lang": "Langue",
        "welcome": "Centre de Contrôle Financier", "sub": "Gestion Financière Personnelle et Entreprise",
        "m_euro": "🌍 Analyse Eurobond", "m_credit": "💳 Calcul Crédit",
        "m_deposit": "💰 Retour Dépôt", "m_invest": "📈 ROI Investissement",
        # Eurobond
        "eb_t": "Analyse Fiscale Eurobond 2025", "eb_i": "Revenu Annuel ($)", 
        "eb_r": "Taux de Change", "eb_res": "Équivalent TRY",
        "eb_ok": "✅ PAS DE DÉCLARATION (< {limit} TL)", "eb_no": "⚠️ DÉCLARATION REQUISE (> {limit} TL)",
        # Credit
        "cr_t": "Plan de Remboursement", "cr_amt": "Montant du Prêt", 
        "cr_rate": "Taux Mensuel (%)", "cr_term": "Durée (Mois)", 
        "cr_res": "Mensualité", "cr_tot": "Remboursement Total",
        # Deposit
        "dep_t": "Calcul Intérêts Dépôt", "dep_amt": "Montant Principal",
        "dep_rate": "Taux Annuel (%)", "dep_days": "Jours", "dep_stop": "Retenue à la source (%)",
        "dep_res": "Rendement Net", "dep_tot": "Total à l'échéance",
        # Investment
        "inv_t": "Analyse Retour Investissement", "inv_buy": "Prix Achat", "inv_sell": "Prix Vente",
        "inv_days": "Durée détention (Jours)", "inv_res": "Rendement Simple", "inv_ann": "Rendement Annualisé",
        "calc": "CALCULER", "back": "⬅️ Retour", "footer": "Projet de Stage Eczacıbaşı & Sanofi"
    },
    "DE": {
        "flag": "🇩🇪", "home": "🏠 Startseite", "lang": "Sprache",
        "welcome": "Finanzkontrollzentrum", "sub": "Persönliches & Unternehmensfinanzmanagement",
        "m_euro": "🌍 Eurobond-Analyse", "m_credit": "💳 Kreditrechner",
        "m_deposit": "💰 Einlagenrückgabe", "m_invest": "📈 Investitions-ROI",
        # Eurobond
        "eb_t": "Eurobond-Steueranalyse 2025", "eb_i": "Jährl. Kupon-Einkommen ($)", 
        "eb_r": "Wechselkurs", "eb_res": "TRY-Gegenwert",
        "eb_ok": "✅ KEINE ERKLÄRUNG NÖTIG (< {limit} TL)", "eb_no": "⚠️ ERKLÄRUNG ERFORDERLICH (> {limit} TL)",
        # Credit
        "cr_t": "Rückzahlungsplan", "cr_amt": "Kreditbetrag", 
        "cr_rate": "Monatl. Zinssatz (%)", "cr_term": "Laufzeit (Monate)", 
        "cr_res": "Monatliche Rate", "cr_tot": "Gesamtrückzahlung",
        # Deposit
        "dep_t": "Einlagenzinsrechner", "dep_amt": "Kapitalbetrag",
        "dep_rate": "Jährl. Zinssatz (%)", "dep_days": "Tage", "dep_stop": "Quellensteuer (%)",
        "dep_res": "Nettorendite", "dep_tot": "Gesamt bei Fälligkeit",
        # Investment
        "inv_t": "Investitionsrendite-Analyse", "inv_buy": "Kaufpreis", "inv_sell": "Verkaufspreis",
        "inv_days": "Haltedauer (Tage)", "inv_res": "Einfache Rendite", "inv_ann": "Annualisierte Rendite",
        "calc": "BERECHNEN", "back": "⬅️ Zurück", "footer": "Eczacıbaşı & Sanofi Praktikumsprojekt"
    }
}

# --- SİSTEM ---
if 'lang' not in st.session_state: st.session_state.lang = "TR"
if 'page' not in st.session_state: st.session_state.page = "home"

def set_lang():
    sel = st.session_state.lang_selector.split(" ")[0]
    for c, d in TRANSLATIONS.items():
        if d["flag"] == sel: st.session_state.lang = c; break
def go(p): st.session_state.page = p; st.rerun()
def t(k): return TRANSLATIONS[st.session_state.lang][k]

# --- ÜST BAR ---
c1, c2 = st.columns([3, 1.5])
with c1: st.caption(t("footer"))
with c2:
    opts = [f"{TRANSLATIONS[c]['flag']} {c}" for c in TRANSLATIONS]
    idx = list(TRANSLATIONS).index(st.session_state.lang)
    st.selectbox("", opts, index=idx, key="lang_selector", on_change=set_lang, label_visibility="collapsed")
st.divider()

# --- SAYFA 1: ANA MENÜ ---
if st.session_state.page == "home":
    st.title(t("welcome"))
    st.markdown(f"*{t('sub')}*")
    st.write("")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"{t('m_euro')}\n➡️", use_container_width=True): go("euro")
        if st.button(f"{t('m_deposit')}\n➡️", use_container_width=True): go("dep")
    with col2:
        if st.button(f"{t('m_credit')}\n➡️", use_container_width=True): go("cred")
        if st.button(f"{t('m_invest')}\n➡️", use_container_width=True): go("inv")

# --- SAYFA 2: EUROBOND ---
elif st.session_state.page == "euro":
    if st.button(t("back")): go("home")
    st.subheader(t("eb_t"))
    
    inc = st.number_input(t("eb_i"), value=6000.0, step=100.0)
    rate = st.number_input(t("eb_r"), value=34.5, step=0.1)
    
    if st.button(t("calc"), type="primary", use_container_width=True):
        res = inc * rate
        limit = 150000
        st.metric(t("eb_res"), f"{res:,.2f} ₺")
        if res > limit: st.error(t("eb_no").format(limit=f"{limit:,}"))
        else: st.success(t("eb_ok").format(limit=f"{limit:,}"))

# --- SAYFA 3: KREDİ ---
elif st.session_state.page == "cred":
    if st.button(t("back")): go("home")
    st.subheader(t("cr_t"))
    
    amt = st.number_input(t("cr_amt"), value=100000.0, step=1000.0)
    rate = st.number_input(t("cr_rate"), value=3.5, step=0.1)
    term = st.number_input(t("cr_term"), value=12, step=1)
    
    if st.button(t("calc"), type="primary", use_container_width=True):
        i = rate / 100
        if i == 0: pmt = amt / term
        else: pmt = amt * (i * (1 + i)**term) / ((1 + i)**term - 1)
        
        c1, c2 = st.columns(2)
        c1.metric(t("cr_res"), f"{pmt:,.2f} ₺")
        c2.metric(t("cr_tot"), f"{pmt*term:,.2f} ₺")

# --- SAYFA 4: MEVDUAT ---
elif st.session_state.page == "dep":
    if st.button(t("back")): go("home")
    st.subheader(t("dep_t"))
    
    amt = st.number_input(t("dep_amt"), value=100000.0, step=1000.0)
    rate = st.number_input(t("dep_rate"), value=45.0, step=0.5)
    days = st.number_input(t("dep_days"), value=32, step=1)
    stop = st.number_input(t("dep_stop"), value=5.0, step=1.0)
    
    if st.button(t("calc"), type="primary", use_container_width=True):
        gross = (amt * rate * days) / 36500
        net = gross * (1 - stop/100)
        c1, c2 = st.columns(2)
        c1.metric(t("dep_res"), f"{net:,.2f} ₺")
        c2.metric(t("dep_tot"), f"{amt+net:,.2f} ₺")

# --- SAYFA 5: YATIRIM ---
elif st.session_state.page == "inv":
    if st.button(t("back")): go("home")
    st.subheader(t("inv_t"))
    
    buy = st.number_input(t("inv_buy"), value=100.0, step=1.0)
    sell = st.number_input(t("inv_sell"), value=120.0, step=1.0)
    days = st.number_input(t("inv_days"), value=90, step=1)
    
    if st.button(t("calc"), type="primary", use_container_width=True):
        simple = (sell - buy) / buy
        if days > 0: ann = (1 + simple)**(365/days) - 1
        else: ann = 0
        
        c1, c2 = st.columns(2)
        c1.metric(t("inv_res"), f"%{simple*100:.2f}")
        c2.metric(t("inv_ann"), f"%{ann*100:.2f}")
