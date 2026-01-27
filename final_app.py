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

# --- 2. TASARIM & CSS ---
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
    /* Metrikler */
    div[data-testid="stMetricValue"] {font-size: 1.3rem !important; color: #212529;}
</style>
""", unsafe_allow_html=True)

# --- 3. DİL SÖZLÜKLERİ ---

# --- TÜRKÇE (TR) ---
TR = {
    "header": "Eczacıbaşı Sağlık Hazine Departmanı",
    "app_name": "Finansal Hesap Makinesi",
    "home": "🏠 Ana Menü",
    "info_sel": "Hesaplama modülünü seçiniz:", # EKLENDİ (Artık çevriliyor)
    
    # MODÜLLER
    "m_invest": "Yatırım Getiri Oranı",
    "m_rates": "Basit - Bileşik Faiz Oranı",
    "m_single": "Tek Dönemlik Faiz Tutarı",
    "m_comp": "Bileşik Faizle Para Hesaplamaları",
    "m_install": "Eşit Taksit (PMT)",
    "m_table": "Eşit Taksit Ödeme Tablosu",
    "m_cost": "Komisyon Dahil Maliyet",
    "m_disc": "İskontolu Alacak Hesaplama",
    
    # ORTAK
    "calc": "HESAPLA", "days_365": "Yıldaki Gün (365/360)", "tax": "Vergi Oranı (%)",
    
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
    "pmt_res": "Taksit Tutarı",
    "tbl_cols": ["Dönem", "Taksit", "Anapara", "Faiz", "KKDF", "BSMV", "Kalan"],
    
    "c_n": "Taksit Sayısı", "c_r": "Dönemsel Kredi Oranı (%)", 
    "c_tax": "Vergi Oranı (KKDF+BSMV)", "c_comm": "Komisyon/Masraf Oranı (%)",
    "c_res1": "Gerçek Aylık Maliyet", "c_res2": "Yıllık Basit Maliyet", "c_res3": "Yıllık Bileşik Maliyet",

    "dc_rec": "Alacak Tutarı", "dc_day": "Erken Tahsilat Günü", "dc_rate": "Alternatif Mevduat Faizi (%)",
    "dc_r1": "İskontolu Tutar (Ele Geçen)", "dc_r2": "Yapılan İskonto Tutarı"
}

# --- İNGİLİZCE (EN) ---
EN = {
    "header": "Eczacıbaşı Healthcare Treasury Dept.",
    "app_name": "Financial Calculator",
    "home": "🏠 Home Menu",
    "info_sel": "Select calculation module:", # EKLENDİ
    
    "m_invest": "Investment ROI", "m_rates": "Simple vs Compound Rates",
    "m_single": "Single Period Interest", "m_comp": "TVM Calculations (PV/FV)",
    "m_install": "Equal Installments (PMT)", "m_table": "Amortization Table",
    "m_cost": "Cost with Commission", "m_disc": "Discounted Receivables",
    
    "calc": "CALCULATE", "days_365": "Day Count (365/360)", "tax": "Tax Rate (%)",
    
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
    "pmt_res": "Installment Amount",
    "tbl_cols": ["Period", "Payment", "Principal", "Interest", "KKDF", "BSMV", "Balance"],
    
    "c_n": "Installments", "c_r": "Periodic Loan Rate (%)", 
    "c_tax": "Tax Rate (KKDF+BSMV)", "c_comm": "Commission Rate (%)",
    "c_res1": "Monthly Effective Cost", "c_res2": "Annual Simple Cost", "c_res3": "Annual Compound Cost",

    "dc_rec": "Receivable Amount", "dc_day": "Days Early", "dc_rate": "Opportunity Cost (%)",
    "dc_r1": "Net Payable Amount", "dc_r2": "Discount Amount"
}

# --- FRANSIZCA (FR) ---
FR = {
    "header": "Dépt. Trésorerie Santé Eczacıbaşı",
    "app_name": "Calculatrice Financière",
    "home": "🏠 Menu Principal",
    "info_sel": "Sélectionnez le module de calcul :", # EKLENDİ
    
    "m_invest": "ROI Investissement", "m_rates": "Taux Simples vs Composés",
    "m_single": "Intérêt Période Unique", "m_comp": "Calculs TVM (VA/VC)",
    "m_install": "Mensualités (PMT)", "m_table": "Tableau d'Amortissement",
    "m_cost": "Coût avec Commission", "m_disc": "Créances Escomptées",
    
    "calc": "CALCULER", "days_365": "Base Jours (365/360)", "tax": "Taux Taxe (%)",
    
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
    "pmt_res": "Mensualité",
    "tbl_cols": ["Période", "Paiement", "Principal", "Intérêts", "KKDF", "BSMV", "Solde"],
    
    "c_n": "Échéances", "c_r": "Taux Périodique (%)", 
    "c_tax": "Taxe (KKDF+BSMV)", "c_comm": "Commission (%)",
    "c_res1": "Coût Mensuel Effectif", "c_res2": "Coût Annuel Simple", "c_res3": "Coût Annuel Composé",

    "dc_rec": "Montant Créance", "dc_day": "Jours Anticipés", "dc_rate": "Coût Opportunité (%)",
    "dc_r1": "Net à Payer", "dc_r2": "Montant Escompte"
}

# --- ALMANCA (DE) ---
DE = {
    "header": "Eczacıbaşı Gesundheits-Schatzamt",
    "app_name": "Finanzrechner",
    "home": "🏠 Hauptmenü",
    "info_sel": "Bitte Berechnungsmodul wählen:", # EKLENDİ
    
    "m_invest": "Investitions-ROI", "m_rates": "Einfache vs Zinseszinsen",
    "m_single": "Einmalige Zinszahlung", "m_comp": "Zeitwert des Geldes (Barwert)",
    "m_install": "Ratenzahlung (PMT)", "m_table": "Tilgungsplan",
    "m_cost": "Kosten inkl. Provision", "m_disc": "Forderungsdiskontierung",
    
    "calc": "BERECHNEN", "days_365": "Zinstage (365/360)", "tax": "Steuersatz (%)",
    
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
    
    "pmt_what
