import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="Finansal Hesap Makinesi",
    page_icon="E", # Eczacıbaşı'nın E'si gibi dursun
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. TASARIM & KURUMSAL CSS ---
st.markdown("""
<style>
    .block-container {padding-top: 1.5rem; padding-bottom: 3rem;}
    
    /* Tablo Başlıkları Gizle (Temiz Görünüm) */
    thead tr th:first-child {display:none}
    tbody th {display:none}
    
    /* Kurumsal Butonlar */
    div.stButton > button:first-child {
        width: 100%; height: 3.5em; border-radius: 8px; border: 1px solid #ced4da;
        font-weight: 600; background: #ffffff; color: #495057; transition: 0.2s;
    }
    div.stButton > button:hover {
        background: #e9ecef; border-color: #ff914d; color: #e85d04; /* Eczacıbaşı Turuncusuna atıf */
        transform: translateY(-2px);
    }
    
    /* Metrikler */
    div[data-testid="stMetricValue"] {font-size: 1.4rem !important; color: #212529;}
</style>
""", unsafe_allow_html=True)

# --- 3. ÇOKLU DİL SÖZLÜĞÜ (GERÇEK ÇEVİRİLER) ---

# TÜRKÇE
TR = {
    "header_title": "Eczacıbaşı Sağlık Hazine Departmanı",
    "app_name": "Finansal Hesap Makinesi",
    "welcome": "Hoş Geldiniz",
    "welcome_sub": "Finansal Analiz ve Hesaplama Modülleri",
    "lang_sel": "Dil / Language",
    "menu_nav": "Modül Seçimi",
    
    # Modül İsimleri
    "m_home": "🏠 Ana Sayfa",
    "m_invest": "Yatırım Getiri Oranı",
    "m_rates": "Basit - Bileşik Faiz",
    "m_single": "Tek Dönemlik Faiz",
    "m_comp_money": "Bileşik Faizle Para",
    "m_install": "Eşit Taksit (PMT)",
    "m_table": "Ödeme Tablosu",
    "m_euro": "Eurobond Analizi",
    "m_disc": "Erken Ödeme İskontosu", # Emoji kalktı
    
    # Ortak Kelimeler
    "calc": "HESAPLA", "res": "Sonuçlar", 
    "days_365": "Baz Gün (365/360)", "tax": "Vergi Oranı (%)",
    
    # Detaylar
    "inv_buy": "Alış Tutarı", "inv_sell": "Satış Tutarı", "inv_day": "Vade (gün)",
    "inv_r1": "Dönemsel Getiri", "inv_r2": "Yıllık Basit", "inv_r3": "Yıllık Bileşik",
    
    "rt_opt1": "Yıllık Bileşik Faiz (%)", "rt_opt2": "Yıllık Basit Faiz (%)",
    "rt_base": "Baz Oran (%)", "rt_days": "Gün Sayısı",
    
    "s_p": "Anapara", "s_r": "Faiz (%)", "s_d": "Gün", "s_res1": "Faiz Tutarı", "s_res2": "Vade Sonu Değer",
    
    "cm_opt1": "Anapara (PV)", "cm_opt2": "Vade Sonu (FV)", "cm_n": "Dönem",
    
    "pmt_loan": "Kredi Tutarı", "pmt_r": "Faiz (%)", "pmt_n": "Taksit Sayısı", 
    "pmt_res": "Taksit Tutarı",
    "tbl_col": ["Dönem", "Taksit", "Anapara", "Faiz", "Vergi", "Kalan"],
    
    "dc_rec": "Alacak Tutarı", "dc_day": "Erken Tahsilat Günü", "dc_rate": "Alternatif Getiri (%)",
    "dc_r1": "İskontolu Tutar", "dc_r2": "İskonto Tutarı",
    
    "eb_inc": "Kupon Geliri ($)", "eb_rate": "Dolar Kuru", "eb_res": "TL Değeri",
    "eb_warn": "Beyan Gerekir", "eb_ok": "Beyan Gerekmez"
}

# İNGİLİZCE (Treasury Terminology)
EN = {
    "header_title": "Eczacıbaşı Healthcare Treasury Dept.",
    "app_name": "Financial Calculator",
    "welcome": "Welcome",
    "welcome_sub": "Financial Analysis & Calculation Modules",
    "lang_sel": "Language",
    "menu_nav": "Module Selection",
    
    "m_home": "🏠 Home",
    "m_invest": "Investment ROI",
    "m_rates": "Simple vs Compound",
    "m_single": "Single Period Interest",
    "m_comp_money": "TVM (PV/FV)",
    "m_install": "Loan Payment (PMT)",
    "m_table": "Amortization Table",
    "m_euro": "Eurobond Analysis",
    "m_disc": "Early Payment Discount",
    
    "calc": "CALCULATE", "res": "Results", 
    "days_365": "Day Count (365/360)", "tax": "Tax Rate (%)",
    
    "inv_buy": "Purchase Price", "inv_sell": "Sell Price", "inv_day": "Tenor (days)",
    "inv_r1": "Periodic Return", "inv_r2": "Annual Simple", "inv_r3": "Annual Compound",
    
    "rt_opt1": "Annual Compound Rate (%)", "rt_opt2": "Annual Simple Rate (%)",
    "rt_base": "Base Rate (%)", "rt_days": "Days",
    
    "s_p": "Principal", "s_r": "Interest Rate (%)", "s_d": "Days", "s_res1": "Interest Amount", "s_res2": "Future Value",
    
    "cm_opt1": "Principal (PV)", "cm_opt2": "Future Value (FV)", "cm_n": "Periods",
    
    "pmt_loan": "Loan Amount", "pmt_r": "Rate (%)", "pmt_n": "Installments", 
    "pmt_res": "Monthly Payment",
    "tbl_col": ["Period", "Payment", "Principal", "Interest", "Tax", "Balance"],
    
    "dc_rec": "Receivable Amount", "dc_day": "Days Early", "dc_rate": "Opp. Cost (%)",
    "dc_r1": "Net Payable", "dc_r2": "Discount Amount",
    
    "eb_inc": "Coupon Income ($)", "eb_rate": "FX Rate", "eb_res": "TRY Value",
    "eb_warn": "Declaration Required", "eb_ok": "No Declaration Needed"
}

# FRANSIZCA (Sanofi Connection)
FR = {
    "header_title": "Dépt. Trésorerie Santé Eczacıbaşı",
    "app_name": "Calculatrice Financière",
    "welcome": "Bienvenue",
    "welcome_sub": "Modules d'Analyse Financière",
    "lang_sel": "Langue",
    "menu_nav": "Sélection du Module",
    
    "m_home": "🏠 Accueil",
    "m_invest": "ROI Investissement",
    "m_rates": "Intérêts Simples/Composés",
    "m_single": "Intérêt Période Unique",
    "m_comp_money": "Valeur Temps (VA/VC)",
    "m_install": "Remboursement (PMT)",
    "m_table": "Tableau d'Amortissement",
    "m_euro": "Analyse Eurobond",
    "m_disc": "Escompte Paiement Anticipé",
    
    "calc": "CALCULER", "res": "Résultats", 
    "days_365": "Base Jours (365/360)", "tax": "Taux Taxe (%)",
    
    "inv_buy": "Prix Achat", "inv_sell": "Prix Vente", "inv_day": "Durée (jours)",
    "inv_r1": "Rendement Périodique", "inv_r2": "Annuel Simple", "inv_r3": "Annuel Composé",
    
    "rt_opt1": "Taux Annuel Composé", "rt_opt2": "Taux Annuel Simple",
    "rt_base": "Taux de Base", "rt_days": "Jours",
    
    "s_p": "Principal", "s_r": "Taux (%)", "s_d": "Jours", "s_res1": "Montant Intérêts", "s_res2": "Valeur Finale",
    
    "cm_opt1": "Valeur Actuelle (VA)", "cm_opt2": "Valeur Future (VC)", "cm_n": "Périodes",
    
    "pmt_loan": "Montant Prêt", "pmt_r": "Taux (%)", "pmt_n": "Échéances", 
    "pmt_res": "Mensualité",
    "tbl_col": ["Période", "Paiement", "Principal", "Intérêts", "Taxe", "Solde"],
    
    "dc_rec": "Montant Créance", "dc_day": "Jours Anticipés", "dc_rate": "Taux Opportunité",
    "dc_r1": "Net à Payer", "dc_r2": "Montant Escompte",
    
    "eb_inc": "Revenu Coupon ($)", "eb_rate": "Taux Change", "eb_res": "Valeur TRY",
    "eb_warn": "Déclaration Requise", "eb_ok": "Pas de Déclaration"
}

# ALMANCA (Global Standart)
DE = {
    "header_title": "Eczacıbaşı Gesundheits-Schatzamt",
    "app_name": "Finanzrechner",
    "welcome": "Willkommen",
    "welcome_sub": "Finanzanalyse-Module",
    "lang_sel": "Sprache",
    "menu_nav": "Modulauswahl",
    
    "m_home": "🏠 Startseite",
    "m_invest": "Investitionsrendite (ROI)",
    "m_rates": "Einfache / Zinseszinsen",
    "m_single": "Einmalige Zinsen",
    "m_comp_money": "Zeitwert des Geldes",
    "m_install": "Kreditrate (PMT)",
    "m_table": "Tilgungsplan",
    "m_euro": "Eurobond-Analyse",
    "m_disc": "Skonto / Frühzahlung",
    
    "calc": "BERECHNEN", "res": "Ergebnisse", 
    "days_365": "Zinstage (365/360)", "tax": "Steuersatz (%)",
    
    "inv_buy": "Kaufpreis", "inv_sell": "Verkaufspreis", "inv_day": "Laufzeit (Tage)",
    "inv_r1": "Periodenrendite", "inv_r2": "Jährlich Einfach", "inv_r3": "Jährlich Effektiv",
    
    "rt_opt1": "Effektivzinssatz (%)", "rt_opt2": "Nominalzinssatz (%)",
    "rt_base": "Basiszinssatz", "rt_days": "Tage",
    
    "s_p": "Kapital", "s_r": "Zinssatz (%)", "s_d": "Tage", "s_res1": "Zinsbetrag", "s_res2": "Endwert",
    
    "cm_opt1": "Barwert (PV)", "cm_opt2": "Endwert (FV)", "cm_n": "Perioden",
    
    "pmt_loan": "Kreditbetrag", "pmt_r": "Zins (%)", "pmt_n": "Raten", 
    "pmt_res": "Monatsrate",
    "tbl_col": ["Periode", "Rate", "Tilgung", "Zins", "Steuer", "Restschuld"],
    
    "dc_rec": "Forderungsbetrag", "dc_day": "Tage früher", "dc_rate": "Alternativzins",
    "dc_r1": "Zahlungsbetrag", "dc_r2": "Skontobetrag",
    
    "eb_inc": "Kupon-Einkommen ($)", "eb_rate": "Wechselkurs", "eb_res": "TRY Wert",
    "eb_warn": "Erklärung erforderlich", "eb_ok": "Keine Erklärung"
}

LANGS = {"TR": TR, "EN": EN, "FR": FR, "DE": DE}

# --- 4. SİSTEM FONKSİYONLARI ---
if 'lang' not in st.session_state: st.session_state.lang = "TR"
if 'page' not in st.session_state: st.session_state.page = "home"

def T(k): return LANGS[st.session_state.lang].get(k, k)
def go(p): st.session_state.page = p; st.rerun()

# --- YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/eb/Eczacibasi_Holding_logo.svg", width=50) # Logo varsa güzel olur yoksa E ikon kalır
    st.title(T("app_name"))
    st.caption(T("header_title"))
    
    st.divider()
    
    # Dil Seçimi
    sel = st.selectbox(T("lang_sel"), ["🇹🇷 TR", "🇬🇧 EN", "🇫🇷 FR", "🇩🇪 DE"], key="l_sel")
    st.session_state.lang = sel.split(" ")[1]
    
    st.divider()
    st.subheader(T("menu_nav"))
    
    if st.button(T("m_home")): go("home")
    if st.button(T("m_disc")): go("disc")
    if st.button(T("m_euro")): go("euro")
    if st.button(T("m_invest")): go("invest")
    if st.button(T("m_rates")): go("rates")
    if st.button(T("m_single")): go("single")
    if st.button(T("m_comp_money")): go("comp_money")
    if st.button(T("m_install")): go("install")
    if st.button(T("m_table")): go("table")

# --- SAYFA İÇERİKLERİ ---

# 0. ANA SAYFA (Temiz & Kurumsal)
if st.session_state.page == "home":
    st.title(T("header_title"))
    st.header(T("welcome"))
    st.write(T("welcome_sub"))
    st.divider()
    st.info("👈 " + T("menu_nav"))

# 1. YATIRIM GETİRİ ORANI
elif st.session_state.page == "invest":
    st.subheader(T("m_invest"))
    with st.container(border=True):
        buy = st.number_input(T("inv_buy"), value=0.0, format="%.4f")
        sell = st.number_input(T("inv_sell"), value=0.0, format="%.4f")
        days = st.number_input(T("inv_day"), value=30, step=1)
        
        if st.button(T("calc"), type="primary"):
            if buy > 0 and days > 0:
                period_ret = (sell - buy) / buy
                ann_simple = period_ret * (365/days)
                ann_comp = ((1 + period_ret)**(365/days)) - 1
                c1, c2, c3 = st.columns(3)
                c1.metric(T("inv_r1"), f"%{period_ret*100:,.2f}")
                c2.metric(T("inv_r2"), f"%{ann_simple*100:,.2f}")
                c3.metric(T("inv_r3"), f"%{ann_comp*100:,.2f}")

# 2. BASİT - BİLEŞİK FAİZ ORANI
elif st.session_state.page == "rates":
    st.subheader(T("m_rates"))
    with st.container(border=True):
        mode = st.selectbox("", [T("rt_opt1"), T("rt_opt2")])
        days = st.number_input(T("rt_days"), value=365)
        rate_in = st.number_input(T("rt_base"), value=0.0)
        
        if st.button(T("calc")):
            r = rate_in / 100
            if days > 0:
                if mode == T("rt_opt1"): 
                    res = ((1 + r * (days/365))**(365/days)) - 1
                else: 
                    res = (((1 + r)**(days/365)) - 1) * (365/days)
                st.metric(T("res"), f"%{res*100:,.2f}")

# 3. TEK DÖNEMLİK FAİZ
elif st.session_state.page == "single":
    st.subheader(T("m_single"))
    with st.container(border=True):
        c1, c2 = st.columns(2)
        p = c1.number_input(T("s_p"), value=0.0, step=1000.0)
        r = c1.number_input(T("s_r"), value=0.0)
        d = c2.number_input(T("s_d"), value=30)
        tax = c2.number_input(T("tax"), value=0.0)
        base = st.selectbox(T("days_365"), [365, 360])
        
        if st.button(T("calc"), type="primary"):
            gross = (p * r * d) / (base * 100)
            net = gross * (1 - tax/100)
            total = p + net
            m1, m2 = st.columns(2)
            m1.metric(T("s_res1"), f"{net:,.2f}")
            m2.metric(T("s_res2"), f"{total:,.2f}")

# 4. BİLEŞİK FAİZLE PARA
elif st.session_state.page == "comp_money":
    st.subheader(T("m_comp_money"))
    with st.container(border=True):
        target = st.selectbox("", [T("cm_opt1"), T("cm_opt2")])
        if target == T("cm_opt1"):
            fv = st.number_input("FV", value=0.0)
            r = st.number_input(T("s_r"), value=0.0)
            n = st.number_input(T("cm_n"), value=1)
            if st.button(T("calc")):
                pv = fv / ((1 + r/100)**n)
                st.metric(T("cm_opt1"), f"{pv:,.2f}")
        else:
            pv = st.number_input("PV", value=0.0)
            r = st.number_input(T("s_r"), value=0.0)
            n = st.number_input(T("cm_n"), value=1)
            if st.button(T("calc")):
                fv = pv * ((1 + r/100)**n)
                st.metric(T("cm_opt2"), f"{fv:,.2f}")

# 5. EŞİT TAKSİT VE TABLO
elif st.session_state.page in ["install", "table"]:
    st.subheader(T("m_install") if st.session_state.page == "install" else T("m_table"))
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        loan = c1.number_input(T("pmt_loan"), value=0.0)
        rate = c2.number_input(T("pmt_r"), value=0.0)
        n = c3.number_input(T("pmt_n"), value=12)
        
        c4, c5 = st.columns(2)
        kkdf = c4.number_input("KKDF (%)", value=0.0)
        bsmv = c5.number_input("BSMV (%)", value=0.0)
        
        gross_rate = (rate / 100) * (1 + (kkdf+bsmv)/100)
        
        if st.button(T("calc"), type="primary"):
            if n > 0:
                if gross_rate == 0: pmt = loan / n
                else: pmt = loan * (gross_rate * (1 + gross_rate)**n) / ((1 + gross_rate)**n - 1)
                
                st.metric(T("pmt_res"), f"{pmt:,.2f}")
                
                if st.session_state.page == "table":
                    st.write("---")
                    schedule = []
                    bal = loan
                    for i in range(1, int(n) + 1):
                        int_raw = bal * (rate/100)
                        tax_load = int_raw * ((kkdf+bsmv)/100)
                        princ = pmt - (int_raw + tax_load)
                        bal -= princ
                        schedule.append([i, pmt, princ, int_raw, tax_load, max(0, bal)])
                    
                    df = pd.DataFrame(schedule, columns=T("tbl_col"))
                    st.dataframe(df.style.format("{:,.2f}"), use_container_width=True, hide_index=True)

# 6. İSKONTO (YENİLENMİŞ)
elif st.session_state.page == "disc":
    st.subheader(T("m_disc"))
    with st.container(border=True):
        receiv = st.number_input(T("dc_rec"), value=0.0)
        days = st.number_input(T("dc_day"), value=0)
        r_alt = st.number_input(T("dc_rate"), value=0.0)
        
        if st.button(T("calc"), type="primary"):
            r = r_alt / 100
            if days > 0:
                pv = receiv / ((1 + r)**(days/365))
                disc_amt = receiv - pv
                c1, c2 = st.columns(2)
                c1.metric(T("dc_r1"), f"{pv:,.2f}")
                c2.metric(T("dc_r2"), f"{disc_amt:,.2f}", delta=f"-{disc_amt:,.2f}")

# 7. EUROBOND
elif st.session_state.page == "euro":
    st.subheader(T("m_euro"))
    with st.container(border=True):
        inc = st.number_input(T("eb_inc"), value=0.0)
        fx = st.number_input(T("eb_rate"), value=0.0)
        if st.button(T("calc"), type="primary"):
            res = inc * fx
            st.metric(T("eb_res"), f"{res:,.2f} ₺")
            if res > 150000: st.error(T("eb_warn"))
            else: st.success(T("eb_ok"))
