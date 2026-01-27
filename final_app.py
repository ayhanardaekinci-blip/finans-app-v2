import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="Finansal Hesap Makinesi",
    page_icon="E",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. TASARIM & OKUNABİLİRLİK (CSS) ---
st.markdown("""
<style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem;}
    
    /* Tablo Başlıkları Gizle */
    thead tr th:first-child {display:none}
    tbody th {display:none}
    
    /* Kart Butonlar */
    div.stButton > button:first-child {
        width: 100%; height: 5em; border-radius: 12px; border: 1px solid #ced4da;
        font-weight: 700; background: #ffffff; color: #495057; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: 0.2s;
    }
    div.stButton > button:hover {
        background: #f8f9fa; border-color: #ff914d; color: #e85d04; 
        transform: translateY(-3px); box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    
    /* Metrik Değerleri (Rakamlar) - DAHA OKUNAKLI */
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem !important; 
        color: #0d6efd !important; /* Parlak Mavi */
        font-weight: bold;
    }
    
    /* Metrik Etiketleri (Başlıklar) */
    div[data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        color: #495057 !important; /* Koyu Gri (Açık modda net) */
        font-weight: 600;
    }
    
    /* Koyu Mod Uyumu İçin Zorlama */
    @media (prefers-color-scheme: dark) {
        div[data-testid="stMetricLabel"] { color: #e0e0e0 !important; } /* Koyu modda beyaz */
        div[data-testid="stMetricValue"] { color: #4dabf7 !important; } /* Koyu modda açık mavi */
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DİL SÖZLÜKLERİ ---

# --- TÜRKÇE (TR) ---
TR = {
    "header": "Eczacıbaşı Sağlık Hazine Departmanı",
    "app_name": "Finansal Hesap Makinesi",
    "home": "🏠 Ana Menü",
    "info_sel": "Hesaplama modülünü seçiniz:", 
    
    # MODÜLLER
    "m_invest": "Yatırım Getiri Oranı",
    "m_rates": "Basit - Bileşik Faiz Oranı",
    "m_single": "Tek Dönemlik Faiz Tutarı",
    "m_comp": "Bileşik Faizle Para Hesaplamaları",
    "m_install": "Kredi / Taksit Hesaplama", # Birleştirildi
    "m_table": "Ödeme Tablosu Oluştur",
    "m_disc": "İskontolu Alacak Hesaplama",
    
    # ORTAK
    "calc": "HESAPLA", "days_365": "Yıldaki Gün (365/360)", "tax": "Vergi Oranı (%)",
    
    # KREDİ SEÇENEKLERİ (YENİ)
    "cr_type": "Ödeme Planı Türü",
    "cr_opt1": "Eşit Taksitli (Standart)",
    "cr_opt2": "Eşit Anaparalı (Azalan Taksit)",
    
    # DETAYLAR
    "inv_buy": "Alış Tutarı", "inv_sell": "Satış Tutarı", "inv_day": "Vade (gün)",
    "inv_r1": "Dönemsel Getiri (%)", "inv_r2": "Yıllık Basit Getiri (%)", "inv_r3": "Yıllık Bileşik Getiri (%)",

    "rt_what": "Ne Hesaplayalım?", 
    "rt_opt1": "Yıllık Bileşik Faiz Oranı (%)", "rt_opt2": "Yıllık Basit Faiz Oranı (%)",
    "rt_base": "Yıllık Basit Faiz Oranı (%)", "rt_days": "Gün Sayısı",
    "rt_res": "Hesaplanan Oran",
    
    "s_p": "Anapara", "s_r": "Faiz Oranı (% Yıllık)", "s_d": "Vade (gün)",
    "s_note": "Mevduatta (-), Kredide (+) giriniz.",
    "s_r1": "Faiz Tutarı", "s_r2": "Vade Sonu Değer",
    
    "cm_what": "Ne Hesaplanacak?",
    "cm_opt1": "Anapara (PV)", "cm_opt2": "Vade Sonu Değer (FV)",
    "cm_r": "Dönemsel Faiz Oranı (%)", "cm_n": "Dönem Sayısı", "cm_res": "Faiz Tutarı",
    
    "pmt_what": "Ne Hesaplanacak?",
    "pmt_loan": "Kredi Tutarı", "pmt_r": "Dönemsel Faiz Oranı (%)", "pmt_n": "Taksit Sayısı",
    "pmt_kkdf": "KKDF (%)", "pmt_bsmv": "BSMV (%)",
    "pmt_res": "İlk Taksit Tutarı", # Değişti
    "pmt_res_total": "Toplam Geri Ödeme",
    "tbl_cols": ["Dönem", "Taksit", "Anapara", "Faiz", "KKDF", "BSMV", "Kalan"],

    "dc_rec": "Alacak Tutarı", "dc_day": "Erken Tahsilat Günü", "dc_rate": "Alternatif Mevduat Faizi (%)",
    "dc_r1": "İskontolu Tutar (Ele Geçen)", "dc_r2": "Yapılan İskonto Tutarı"
}

# --- İNGİLİZCE (EN) ---
EN = {
    "header": "Eczacıbaşı Healthcare Treasury Dept.",
    "app_name": "Financial Calculator",
    "home": "🏠 Home Menu",
    "info_sel": "Select calculation module:", 
    
    "m_invest": "Investment ROI", "m_rates": "Simple vs Compound Rates",
    "m_single": "Single Period Interest", "m_comp": "TVM Calculations (PV/FV)",
    "m_install": "Loan / Installment Calc",
    "m_table": "Amortization Table",
    "m_disc": "Discounted Receivables",
    
    "calc": "CALCULATE", "days_365": "Day Count (365/360)", "tax": "Tax Rate (%)",
    
    "cr_type": "Payment Plan Type",
    "cr_opt1": "Equal Installments (Annuity)",
    "cr_opt2": "Equal Principal (Decreasing)",
    
    "inv_buy": "Purchase Price", "inv_sell": "Sell Price", "inv_day": "Tenor (days)",
    "inv_r1": "Periodic Return (%)", "inv_r2": "Annual Simple Return (%)", "inv_r3": "Annual Compound Return (%)",

    "rt_what": "Calculate What?", 
    "rt_opt1": "Annual Compound Rate (%)", "rt_opt2": "Annual Simple Rate (%)",
    "rt_base": "Annual Simple Rate (%)", "rt_days": "Days", "rt_res": "Result Rate",
    
    "s_p": "Principal", "s_r": "Interest Rate (% p.a.)", "s_d": "Tenor (days)",
    "s_note": "Deposit (-), Loan (+)",
    "s_r1": "Interest Amount", "s_r2": "Future Value",
    
    "cm_what": "Calculate What?",
    "cm_opt1": "Principal (PV)", "cm_opt2": "Future Value (FV)",
    "cm_r": "Periodic Interest Rate (%)", "cm_n": "Number of Periods", "cm_res": "Interest Amount",
    
    "pmt_what": "Calculate What?",
    "pmt_loan": "Loan Amount", "pmt_r": "Periodic Rate (%)", "pmt_n": "Installments",
    "pmt_kkdf": "KKDF (%)", "pmt_bsmv": "BSMV (%)",
    "pmt_res": "First Payment Amount",
    "pmt_res_total": "Total Repayment",
    "tbl_cols": ["Period", "Payment", "Principal", "Interest", "KKDF", "BSMV", "Balance"],

    "dc_rec": "Receivable Amount", "dc_day": "Days Early", "dc_rate": "Opportunity Cost (%)",
    "dc_r1": "Net Payable Amount", "dc_r2": "Discount Amount"
}

# --- FRANSIZCA (FR) ---
FR = {
    "header": "Dépt. Trésorerie Santé Eczacıbaşı",
    "app_name": "Calculatrice Financière",
    "home": "🏠 Menu Principal",
    "info_sel": "Sélectionnez le module de calcul :",
    
    "m_invest": "ROI Investissement", "m_rates": "Taux Simples vs Composés",
    "m_single": "Intérêt Période Unique", "m_comp": "Calculs TVM (VA/VC)",
    "m_install": "Calcul de Prêt",
    "m_table": "Tableau d'Amortissement",
    "m_disc": "Créances Escomptées",
    
    "calc": "CALCULER", "days_365": "Base Jours (365/360)", "tax": "Taux Taxe (%)",
    
    "cr_type": "Type de Plan",
    "cr_opt1": "Mensualités Constantes",
    "cr_opt2": "Amortissement Constant",

    "inv_buy": "Prix Achat", "inv_sell": "Prix Vente", "inv_day": "Durée (jours)",
    "inv_r1": "Rendement Périodique", "inv_r2": "Annuel Simple", "inv_r3": "Annuel Composé",

    "rt_what": "Que Calculer?", 
    "rt_opt1": "Taux Annuel Composé (%)", "rt_opt2": "Taux Annuel Simple (%)",
    "rt_base": "Taux Simple (%)", "rt_days": "Jours", "rt_res": "Taux Résultant",
    
    "s_p": "Principal", "s_r": "Taux Intérêt (%)", "s_d": "Jours",
    "s_note": "Dépôt (-), Prêt (+)",
    "s_r1": "Montant Intérêts", "s_r2": "Valeur Future",
    
    "cm_what": "Que Calculer?",
    "cm_opt1": "Valeur Actuelle (VA)", "cm_opt2": "Valeur Future (VC)",
    "cm_r": "Taux Périodique (%)", "cm_n": "Périodes", "cm_res": "Montant Intérêts",
    
    "pmt_what": "Que Calculer?",
    "pmt_loan": "Montant Prêt", "pmt_r": "Taux Périodique (%)", "pmt_n": "Échéances",
    "pmt_kkdf": "KKDF (%)", "pmt_bsmv": "BSMV (%)",
    "pmt_res": "Premier Paiement",
    "pmt_res_total": "Remboursement Total",
    "tbl_cols": ["Période", "Paiement", "Principal", "Intérêts", "KKDF", "BSMV", "Solde"],

    "dc_rec": "Montant Créance", "dc_day": "Jours Anticipés", "dc_rate": "Coût Opportunité (%)",
    "dc_r1": "Net à Payer", "dc_r2": "Montant Escompte"
}

# --- ALMANCA (DE) ---
DE = {
    "header": "Eczacıbaşı Gesundheits-Schatzamt",
    "app_name": "Finanzrechner",
    "home": "🏠 Hauptmenü",
    "info_sel": "Bitte Berechnungsmodul wählen:",
    
    "m_invest": "Investitions-ROI", "m_rates": "Einfache vs Zinseszinsen",
    "m_single": "Einmalige Zinszahlung", "m_comp": "Zeitwert des Geldes (Barwert)",
    "m_install": "Kreditrechner",
    "m_table": "Tilgungsplan",
    "m_disc": "Forderungsdiskontierung",
    
    "calc": "BERECHNEN", "days_365": "Zinstage (365/360)", "tax": "Steuersatz (%)",
    
    "cr_type": "Tilgungsplanart",
    "cr_opt1": "Gleiche Raten (Annuität)",
    "cr_opt2": "Gleiche Tilgung (Ratentilgung)",

    "inv_buy": "Kaufpreis", "inv_sell": "Verkaufspreis", "inv_day": "Laufzeit (Tage)",
    "inv_r1": "Periodenrendite", "inv_r2": "Jährlich Einfach", "inv_r3": "Jährlich Effektiv",

    "rt_what": "Was berechnen?", 
    "rt_opt1": "Effektivzinssatz (%)", "rt_opt2": "Nominalzinssatz (%)",
    "rt_base": "Nominalzins (%)", "rt_days": "Tage", "rt_res": "Ergebnis",
    
    "s_p": "Kapital", "s_r": "Zinssatz (%)", "s_d": "Tage",
    "s_note": "Einlage (-), Kredit (+)",
    "s_r1": "Zinsbetrag", "s_r2": "Endwert",
    
    "cm_what": "Was berechnen?",
    "cm_opt1": "Barwert (PV)", "cm_opt2": "Endwert (FV)",
    "cm_r": "Periodischer Zins (%)", "cm_n": "Perioden", "cm_res": "Zinsbetrag",
    
    "pmt_what": "Was berechnen?",
    "pmt_loan": "Kreditbetrag", "pmt_r": "Periodischer Zins (%)", "pmt_n": "Raten",
    "pmt_kkdf": "KKDF (%)", "pmt_bsmv": "BSMV (%)",
    "pmt_res": "Erste Rate",
    "pmt_res_total": "Gesamtrückzahlung",
    "tbl_cols": ["Periode", "Rate", "Tilgung", "Zins", "KKDF", "BSMV", "Restschuld"],

    "dc_rec": "Forderungsbetrag", "dc_day": "Tage früher", "dc_rate": "Alternativzins (%)",
    "dc_r1": "Auszahlungsbetrag", "dc_r2": "Skontobetrag"
}

LANGS = {"TR": TR, "EN": EN, "FR": FR, "DE": DE}

# --- 4. SİSTEM & FONKSİYONLAR ---
if 'lang' not in st.session_state: st.session_state.lang = "TR"
if 'page' not in st.session_state: st.session_state.page = "home"

def T(k): return LANGS[st.session_state.lang].get(k, k)
def go(p): st.session_state.page = p; st.rerun()

def update_lang():
    st.session_state.lang = st.session_state.l_sel.split(" ")[1]

# --- YAN MENÜ ---
with st.sidebar:
    st.title(T("app_name"))
    st.caption(T("header"))
    
    st.selectbox(
        "Dil / Language", 
        ["🇹🇷 TR", "🇬🇧 EN", "🇫🇷 FR", "🇩🇪 DE"], 
        key="l_sel", 
        on_change=update_lang
    )
    
    st.divider()
    if st.button(T("home")): go("home")

# --- SAYFALAR ---

# 0. ANA SAYFA
if st.session_state.page == "home":
    st.title(T("header"))
    st.info(T("info_sel"))
    
    # Grid Düzeni
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(f"📈 {T('m_invest')}", use_container_width=True): go("invest")
        if st.button(f"💰 {T('m_comp')}", use_container_width=True): go("comp")
    with c2:
        if st.button(f"🔄 {T('m_rates')}", use_container_width=True): go("rates")
        if st.button(f"💳 {T('m_install')}", use_container_width=True): go("install")
    with c3:
        if st.button(f"📅 {T('m_single')}", use_container_width=True): go("single")
        if st.button(f"📋 {T('m_table')}", use_container_width=True): go("table")
        if st.button(f"⚡ {T('m_disc')}", use_container_width=True): go("disc")

# 1. YATIRIM GETİRİSİ
elif st.session_state.page == "invest":
    st.subheader(T("m_invest"))
    st.divider()
    with st.container(border=True):
        buy = st.number_input(T("inv_buy"), value=0.0, format="%.4f")
        sell = st.number_input(T("inv_sell"), value=0.0, format="%.4f")
        days = st.number_input(T("inv_day"), value=30, step=1)
        
        if st.button(T("calc"), type="primary"):
            if buy > 0 and days > 0:
                per = (sell - buy) / buy
                ann_s = per * (365/days)
                ann_c = ((1 + per)**(365/days)) - 1
                c1, c2, c3 = st.columns(3)
                c1.metric(T("inv_r1"), f"%{per*100:,.2f}")
                c2.metric(T("inv_r2"), f"%{ann_s*100:,.2f}")
                c3.metric(T("inv_r3"), f"%{ann_c*100:,.2f}")

# 2. FAİZ ORANI DÖNÜŞÜM
elif st.session_state.page == "rates":
    st.subheader(T("m_rates"))
    st.divider()
    with st.container(border=True):
        mode = st.selectbox(T("rt_what"), [T("rt_opt1"), T("rt_opt2")])
        days = st.number_input(T("rt_days"), value=365)
        base = st.number_input(T("rt_base"), value=0.0)
        
        if st.button(T("calc"), type="primary"):
            r = base / 100
            if days > 0:
                if mode == T("rt_opt1"): res = ((1 + r * (days/365))**(365/days)) - 1
                else: res = (((1 + r)**(days/365)) - 1) * (365/days)
                st.metric(T("rt_res"), f"%{res*100:,.2f}")

# 3. TEK DÖNEMLİK FAİZ
elif st.session_state.page == "single":
    st.subheader(T("m_single"))
    st.divider()
    with st.container(border=True):
        c1, c2 = st.columns(2)
        p = c1.number_input(T("s_p"), value=0.0, step=1000.0)
        r = c1.number_input(T("s_r"), value=0.0)
        d = c2.number_input(T("s_d"), value=32)
        tax = c2.number_input(T("tax"), value=0.0, help=T("s_note"))
        day_base = st.selectbox(T("days_365"), [365, 360])
        
        if st.button(T("calc"), type="primary"):
            gross = (p * r * d) / (day_base * 100)
            net = gross * (1 - tax/100)
            m1, m2 = st.columns(2)
            m1.metric(T("s_r1"), f"{net:,.2f}")
            m2.metric(T("s_r2"), f"{p+net:,.2f}")

# 4. BİLEŞİK FAİZLE PARA
elif st.session_state.page == "comp":
    st.subheader(T("m_comp"))
    st.divider()
    with st.container(border=True):
        target = st.selectbox(T("cm_what"), [T("cm_opt1"), T("cm_opt2")])
        
        if target == T("cm_opt1"): 
            val = st.number_input(T("cm_opt2"), value=0.0) # FV gir
        else: 
            val = st.number_input(T("cm_opt1"), value=0.0) # PV gir

        r = st.number_input(T("cm_r"), value=0.0)
        n = st.number_input(T("cm_n"), value=1)
        tax = st.number_input(T("tax"), value=0.0)
        
        if st.button(T("calc"), type="primary"):
            net_r = (r/100) * (1 - tax/100)
            if target == T("cm_opt1"): # PV bul
                res = val / ((1 + net_r)**n)
                lbl = T("cm_opt1")
            else: # FV bul
                res = val * ((1 + net_r)**n)
                lbl = T("cm_opt2")
            
            c1, c2 = st.columns(2)
            c1.metric(lbl, f"{res:,.2f}")
            c2.metric(T("cm_res"), f"{abs(val-res):,.2f}")

# 5. KREDİ VE TABLO (BİRLEŞTİRİLMİŞ MANTIK)
elif st.session_state.page in ["install", "table"]:
    st.subheader(T("m_install") if st.session_state.page=="install" else T("m_table"))
    st.divider()
    with st.container(border=True):
        # Ödeme Planı Seçimi (YENİ)
        plan_type = st.radio(T("cr_type"), [T("cr_opt1"), T("cr_opt2")], horizontal=True)
        st.write("")
        
        c1, c2, c3 = st.columns(3)
        loan = c1.number_input(T("pmt_loan"), value=100000.0)
        rate = c2.number_input(T("pmt_r"), value=1.20)
        n = c3.number_input(T("pmt_n"), value=12)
        
        c4, c5 = st.columns(2)
        kkdf = c4.number_input("KKDF (%)", value=15.0)
        bsmv = c5.number_input("BSMV (%)", value=5.0)
        
        if st.button(T("calc"), type="primary"):
            if n > 0:
                sch = []
                bal = loan
                total_pay = 0
                
                # SEÇENEK 1: EŞİT TAKSİT (Annuity)
                if plan_type == T("cr_opt1"):
                    gross = (rate/100) * (1 + (kkdf+bsmv)/100)
                    if gross > 0: pmt = loan * (gross * (1+gross)**n) / ((1+gross)**n - 1)
                    else: pmt = loan / n
                    
                    first_pmt = pmt
                    
                    for i in range(1, int(n)+1):
                        inte = bal * (rate/100)
                        t_kkdf = inte * (kkdf/100)
                        t_bsmv = inte * (bsmv/100)
                        princ = pmt - (inte + t_kkdf + t_bsmv)
                        bal -= princ
                        total_pay += pmt
                        sch.append([i, pmt, princ, inte, t_kkdf, t_bsmv, max(0, bal)])

                # SEÇENEK 2: EŞİT ANAPARA (Decreasing)
                else:
                    fixed_princ = loan / n
                    first_pmt = 0
                    
                    for i in range(1, int(n)+1):
                        inte = bal * (rate/100)
                        t_kkdf = inte * (kk
