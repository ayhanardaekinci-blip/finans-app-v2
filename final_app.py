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
    
    /* Metrik Değerleri (Rakamlar) - TÜRKÇE FORMAT İÇİN DAHA OKUNAKLI */
    div[data-testid="stMetricValue"] {
        font-size: 1.6rem !important; 
        color: #0d6efd !important; /* Parlak Mavi */
        font-weight: bold;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        font-weight: 600;
        color: #495057 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- TÜRKÇE SAYI FORMATLAYICI ---
def fmt_tr(value):
    """
    Sayayı 1.234,56 formatına çevirir (TR Standardı).
    """
    try:
        # Önce standart format (1,234.56)
        s = f"{float(value):,.2f}"
        # Karakterleri değiştir: Virgülü X yap, Noktayı Virgül yap, X'i Nokta yap
        return s.replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return str(value)

# --- 3. DİL SÖZLÜKLERİ ---

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
    "m_install": "Kredi / Taksit Hesaplama",
    "m_table": "Ödeme Tablosu Oluştur",
    "m_disc": "İskontolu Alacak Hesaplama",
    
    # ORTAK
    "calc": "HESAPLA", "days_365": "Yıldaki Gün (365/360)", "tax": "Vergi Oranı (%)",
    
    # KREDİ SEÇENEKLERİ
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
    "pmt_res": "İlk Taksit Tutarı",
    "pmt_res_total": "Toplam Geri Ödeme",
    "tbl_cols": ["Dönem", "Taksit", "Anapara", "Faiz", "KKDF", "BSMV", "Kalan"],

    "dc_rec": "Alacak Tutarı", "dc_day": "Erken Tahsilat Günü", "dc_rate": "Alternatif Mevduat Faizi (%)",
    "dc_r1": "İskontolu Tutar (Ele Geçen)", "dc_r2": "Yapılan İskonto Tutarı"
}

# (Diğer diller TR kopyası olarak kalıyor, metinler TR görünebilir ama yapı çalışır)
EN = TR.copy(); FR = TR.copy(); DE = TR.copy()
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
    
    st.selectbox("Dil / Language", ["🇹🇷 TR", "🇬🇧 EN", "🇫🇷 FR", "🇩🇪 DE"], key="l_sel", on_change=update_lang)
    
    st.divider()
    if st.button(T("home")): go("home")

# --- SAYFALAR ---

# 0. ANA SAYFA
if st.session_state.page == "home":
    st.title(T("header"))
    st.info(T("info_sel"))
    
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
                c1.metric(T("inv_r1"), f"%{fmt_tr(per*100)}")
                c2.metric(T("inv_r2"), f"%{fmt_tr(ann_s*100)}")
                c3.metric(T("inv_r3"), f"%{fmt_tr(ann_c*100)}")

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
                st.metric(T("rt_res"), f"%{fmt_tr(res*100)}")

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
            m1.metric(T("s_r1"), f"{fmt_tr(net)} ₺")
            m2.metric(T("s_r2"), f"{fmt_tr(p+net)} ₺")

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
            c1.metric(lbl, f"{fmt_tr(res)} ₺")
            c2.metric(T("cm_res"), f"{fmt_tr(abs(val-res))} ₺")

# 5. KREDİ VE TABLO (MATEMATİK DÜZELTİLDİ)
elif st.session_state.page in ["install", "table"]:
    st.subheader(T("m_install") if st.session_state.page=="install" else T("m_table"))
    st.divider()
    with st.container(border=True):
        plan_type = st.radio(T("cr_type"), [T("cr_opt1"), T("cr_opt2")], horizontal=True)
        st.write("")
        
        c1, c2, c3 = st.columns(3)
        loan = c1.number_input(T("pmt_loan"), value=100000.0, step=1000.0)
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
                first_pmt_display = 0
                
                # VERGİ DAHİL ORAN
                gross_rate = (rate/100) * (1 + (kkdf+bsmv)/100)

                # SEÇENEK 1: EŞİT TAKSİT (Annuity) - PMT Sabit
                if plan_type == T("cr_opt1"):
                    if gross_rate > 0: 
                        pmt = loan * (gross_rate * (1+gross_rate)**n) / ((1+gross_rate)**n - 1)
                    else: 
                        pmt = loan / n
                    
                    first_pmt_display = pmt
                    
                    for i in range(1, int(n)+1):
                        # Faiz Hesabı (Vergisiz faiz üzerinden yapılır, sonra vergi eklenir)
                        # Bankacılıkta faiz = Kalan Anapara * Faiz Oranı
                        # Vergiler = Faiz * Vergi Oranları
                        
                        raw_int = bal * (rate/100)
                        tax_k = raw_int * (kkdf/100)
                        tax_b = raw_int * (bsmv/100)
                        total_int_load = raw_int + tax_k + tax_b
                        
                        princ = pmt - total_int_load
                        bal -= princ
                        total_pay += pmt
                        sch.append([i, fmt_tr(pmt), fmt_tr(princ), fmt_tr(raw_int), fmt_tr(tax_k), fmt_tr(tax_b), fmt_tr(max(0, bal))])

                # SEÇENEK 2: EŞİT ANAPARA (Decreasing) - Anapara Sabit, Taksit Azalır
                else:
                    fixed_princ = loan / n # Her ay düşecek sabit anapara
                    
                    for i in range(1, int(n)+1):
                        raw_int = bal * (rate/100)
                        tax_k = raw_int * (kkdf/100)
                        tax_b = raw_int * (bsmv/100)
                        total_int_load = raw_int + tax_k + tax_b
                        
                        curr_pmt = fixed_princ + total_int_load # Taksit = Sabit Anapara + O ayın faizi
                        
                        if i == 1: first_pmt_display = curr_pmt # İlk taksiti kaydet
                        
                        bal -= fixed_princ
                        total_pay += curr_pmt
                        sch.append([i, fmt_tr(curr_pmt), fmt_tr(fixed_princ), fmt_tr(raw_int), fmt_tr(tax_k), fmt_tr(tax_b), fmt_tr(max(0, bal))])

                m1, m2 = st.columns(2)
                m1.metric(T("pmt_res"), f"{fmt_tr(first_pmt_display)} ₺")
                m2.metric(T("pmt_res_total"), f"{fmt_tr(total_pay)} ₺")
                
                if st.session_state.page == "table":
                    st.write("---")
                    df = pd.DataFrame(sch, columns=T("tbl_cols"))
                    # Tabloyu göster (string formatlı olduğu için direk basıyoruz)
                    st.dataframe(df, use_container_width=True, hide_index=True)

# 6. İSKONTOLU ALACAK
elif st.session_state.page == "disc":
    st.subheader(T("m_disc"))
    st.divider()
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
                c1.metric(T("dc_r1"), f"{fmt_tr(pv)} ₺")
                c2.metric(T("dc_r2"), f"{fmt_tr(disc_amt)} ₺", delta=f"-{fmt_tr(disc_amt)} ₺")
