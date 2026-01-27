import streamlit as st
import pandas as pd
import numpy as np

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="Finansal Hesap Makinesi",
    page_icon="E",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. DİL SÖZLÜKLERİ (EN BAŞA ALINDI - HATA DÜZELTİLDİ) ---
TR = {
    "header": "Eczacıbaşı Sağlık Hazine Departmanı",
    "app_name": "Finansal Hesap Makinesi",
    "home": "🏠 Ana Menü",
    "info_sel": "Hesaplama modülünü seçiniz:", 
    "m_invest": "Yatırım Getiri Oranı", "m_rates": "Basit - Bileşik Faiz Oranı",
    "m_single": "Tek Dönemlik Faiz Tutarı", "m_comp": "Bileşik Faizle Para Hesaplamaları",
    "m_install": "Kredi / Taksit Hesaplama", "m_table": "Ödeme Tablosu Oluştur",
    "m_disc": "⚡ İskontolu Alacak Hesaplama",
    "calc": "HESAPLA", "days_365": "Yıldaki Gün (365/360)", "tax": "Vergi Oranı (%)",
    "cr_type": "Ödeme Planı Türü", "cr_opt1": "Eşit Taksitli (Standart)", "cr_opt2": "Eşit Anaparalı (Azalan Taksit)",
    "inv_buy": "Alış Tutarı", "inv_sell": "Satış Tutarı", "inv_day": "Vade (gün)",
    "inv_r1": "Dönemsel Getiri (%)", "inv_r2": "Yıllık Basit Getiri (%)", "inv_r3": "Yıllık Bileşik Getiri (%)",
    "rt_what": "Ne Hesaplayalım?", "rt_opt1": "Yıllık Bileşik Faiz Oranı (%)", "rt_opt2": "Yıllık Basit Faiz Oranı (%)",
    "rt_base": "Yıllık Basit Faiz Oranı (%)", "rt_days": "Gün Sayısı", "rt_res": "Hesaplanan Oran",
    "s_p": "Anapara", "s_r": "Faiz Oranı (% Yıllık)", "s_d": "Vade (gün)", "s_note": "Mevduatta (-), Kredide (+) giriniz.",
    "s_r1": "Faiz Tutarı", "s_r2": "Vade Sonu Değer",
    "cm_what": "Ne Hesaplanacak?", "cm_opt1": "Anapara (PV)", "cm_opt2": "Vade Sonu Değer (FV)",
    "cm_r": "Dönemsel Faiz Oranı (%)", "cm_n": "Dönem Sayısı", "cm_res": "Faiz Tutarı",
    "pmt_what": "Ne Hesaplanacak?", "pmt_loan": "Kredi Tutarı", "pmt_r": "Dönemsel Faiz Oranı (%)", "pmt_n": "Taksit Sayısı",
    "pmt_kkdf": "KKDF (%)", "pmt_bsmv": "BSMV (%)", "pmt_res": "İlk Taksit Tutarı", "pmt_res_total": "Toplam Geri Ödeme",
    "tbl_cols": ["Dönem", "Taksit", "Anapara", "Faiz", "KKDF", "BSMV", "Kalan"],
    "dc_rec": "Alacak Tutarı", "dc_day": "Erken Tahsilat Günü", "dc_rate": "Alternatif Mevduat Faizi (%)",
    "dc_r1": "İskontolu Tutar (Ele Geçen)", "dc_r2": "Yapılan İskonto Tutarı"
}
EN = TR.copy(); FR = TR.copy(); DE = TR.copy()
# Dil ayarları (Gerekirse burayı detaylandırabilirsin)
EN["app_name"] = "Financial Calculator"; EN["home"] = "🏠 Home Menu"
FR["app_name"] = "Calculatrice Financière"; DE["app_name"] = "Finanzrechner"

LANGS = {"TR": TR, "EN": EN, "FR": FR, "DE": DE}

# --- 3. FONKSİYONLAR ---
def fmt(value):
    if value is None: return "0,00"
    try:
        s = "{:,.2f}".format(float(value))
        return s.replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "0,00"

def update_lang():
    st.session_state.lang = st.session_state.l_sel.split(" ")[1]

# --- 4. SİSTEM BAŞLANGICI ---
if 'lang' not in st.session_state: st.session_state.lang = "TR"
if 'page' not in st.session_state: st.session_state.page = "home"

def T(k):
    return LANGS[st.session_state.lang].get(k, k)

def go(p): st.session_state.page = p; st.rerun()

# --- 5. YAN MENÜ & TEMA SEÇİMİ ---
with st.sidebar:
    st.title(T("app_name"))
    st.caption("Eczacıbaşı Sağlık Hazine Departmanı")
    
    # Dil Seçimi
    st.selectbox("Dil / Language", ["🇹🇷 TR", "🇬🇧 EN", "🇫🇷 FR", "🇩🇪 DE"], key="l_sel", on_change=update_lang)
    
    st.write("") 
    
    # GECE MODU ANAHTARI
    is_dark = st.toggle("🌙 Gece Modu / Dark Mode", value=False)
    
    st.divider()
    if st.button("🏠 " + ("Ana Menü" if st.session_state.lang == "TR" else "Home")): go("home")

# --- 6. DİNAMİK CSS (RENK VE KONTRAST) ---
if is_dark:
    # --- GECE MODU ---
    bg_color = "#0e1117"
    card_bg = "#262730"
    text_color = "#ffffff"
    metric_color = "#4dabf7"  # Parlak Açık Mavi
    input_bg = "#262730"
    input_text = "#ffffff"
    btn_border = "#495057"
else:
    # --- GÜNDÜZ MODU (DEFAULT) ---
    bg_color = "#f8f9fa"
    card_bg = "#ffffff"
    text_color = "#000000"
    metric_color = "#0d25cf"  # Koyu Lacivert
    input_bg = "#ffffff"
    input_text = "#000000"
    btn_border = "#ced4da"

st.markdown(f"""
<style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .block-container {{padding-top: 2rem; padding-bottom: 3rem;}}
    
    /* Tablo Gizlemeleri */
    thead tr th:first-child {{display:none}}
    tbody th {{display:none}}
    
    /* Butonlar */
    div.stButton > button:first-child {{
        width: 100%; height: 4.5em; border-radius: 10px; 
        border: 1px solid {btn_border};
        font-weight: 700; 
        background: {card_bg}; 
        color: {text_color}; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.05); transition: 0.2s;
    }}
    div.stButton > button:hover {{
        background: {input_bg}; border-color: #0d6efd; color: #0d6efd; 
        transform: translateY(-2px);
    }}
    
    /* Girdi Kutuları */
    .stNumberInput input {{
        color: {input_text} !important;
        font-weight: 800 !important;
        background-color: {input_bg} !important;
        border: 1px solid {btn_border} !important;
        font-size: 1.1rem !important;
    }}
    input[type=number]::-webkit-inner-spin-button, 
    input[type=number]::-webkit-outer-spin-button {{ 
        -webkit-appearance: none; margin: 0; 
    }}
    
    /* Sonuç Rakamları */
    div[data-testid="stMetricValue"] {{
        font-size: 1.7rem !important; 
        color: {metric_color} !important; 
        font-weight: 800 !important;
    }}
    div[data-testid="stMetricLabel"] {{
        font-size: 1rem !important;
        font-weight: 600;
        color: {text_color} !important;
        opacity: 0.9;
    }}
</style>
""", unsafe_allow_html=True)

# --- 7. SAYFALAR ---

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
    
    st.write("") 
    ec1, ec2, ec3 = st.columns([1, 2, 1])
    with ec2:
        if st.button(f"{T('m_disc')}", use_container_width=True): go("disc")

elif st.session_state.page == "invest":
    st.subheader(T("m_invest"))
    st.divider()
    with st.container(border=True):
        buy = st.number_input(T("inv_buy"), value=0.0, format="%.2f")
        sell = st.number_input(T("inv_sell"), value=0.0, format="%.2f")
        days = st.number_input(T("inv_day"), value=30, step=1)
        
        if st.button(T("calc"), type="primary"):
            if buy > 0 and days > 0:
                per = (sell - buy) / buy
                ann_s = per * (365/days)
                ann_c = ((1 + per)**(365/days)) - 1
                c1, c2, c3 = st.columns(3)
                c1.metric(T("inv_r1"), f"%{fmt(per*100)}")
                c2.metric(T("inv_r2"), f"%{fmt(ann_s*100)}")
                c3.metric(T("inv_r3"), f"%{fmt(ann_c*100)}")

elif st.session_state.page == "rates":
    st.subheader(T("m_rates"))
    st.divider()
    with st.container(border=True):
        mode = st.selectbox(T("rt_what"), [T("rt_opt1"), T("rt_opt2")])
        days = st.number_input(T("rt_days"), value=365)
        base = st.number_input(T("rt_base"), value=0.0, format="%.2f")
        if st.button(T("calc"), type="primary"):
            r = base / 100
            if days > 0:
                if mode == T("rt_opt1"): res = ((1 + r * (days/365))**(365/days)) - 1
                else: res = (((1 + r)**(days/365)) - 1) * (365/days)
                st.metric(T("rt_res"), f"%{fmt(res*100)}")

elif st.session_state.page == "single":
    st.subheader(T("m_single"))
    st.divider()
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1: p = st.number_input(T("s_p"), value=0.0, step=1000.0, format="%.2f")
        r = c1.number_input(T("s_r"), value=0.0, format="%.2f")
        d = c2.number_input(T("s_d"), value=32)
        tax = c2.number_input(T("tax"), value=0.0, format="%.2f", help=T("s_note"))
        day_base = st.selectbox(T("days_365"), [365, 360])
        if st.button(T("calc"), type="primary"):
            gross = (p * r * d) / (day_base * 100)
            net = gross * (1 - tax/100)
            m1, m2 = st.columns(2)
            m1.metric(T("s_r1"), f"{fmt(net)} ₺")
            m2.metric(T("s_r2"), f"{fmt(p+net)} ₺")

elif st.session_state.page == "comp":
    st.subheader(T("m_comp"))
    st.divider()
    with st.container(border=True):
        target = st.selectbox(T("cm_what"), [T("cm_opt1"), T("cm_opt2")])
        label = T("cm_opt2") if target == T("cm_opt1") else T("cm_opt1")
        val = st.number_input(label, value=0.0, step=1000.0, format="%.2f")
        r = st.number_input(T("cm_r"), value=0.0, format="%.2f")
        n = st.number_input(T("cm_n"), value=1)
        tax = st.number_input(T("tax"), value=0.0, format="%.2f")
        if st.button(T("calc"), type="primary"):
            net_r = (r/100) * (1 - tax/100)
            if target == T("cm_opt1"): 
                res = val / ((1 + net_r)**n); lbl = T("cm_opt1")
            else: 
                res = val * ((1 + net_r)**n); lbl = T("cm_opt2")
            c1, c2 = st.columns(2)
            c1.metric(lbl, f"{fmt(res)} ₺")
            c2.metric(T("cm_res"), f"{fmt(abs(val-res))} ₺")

elif st.session_state.page in ["install", "table"]:
    st.subheader(T("m_install") if st.session_state.page=="install" else T("m_table"))
    st.divider()
    with st.container(border=True):
        plan_type = st.radio(T("cr_type"), [T("cr_opt1"), T("cr_opt2")], horizontal=True)
        st.write("")
        c1, c2, c3 = st.columns(3)
        with c1: loan = st.number_input(T("pmt_loan"), value=100000.0, step=1000.0, format="%.2f")
        rate = c2.number_input(T("pmt_r"), value=1.20, format="%.2f")
        n = c3.number_input(T("pmt_n"), value=12)
        c4, c5 = st.columns(2)
        kkdf = c4.number_input("KKDF (%)", value=15.0, format="%.2f")
        bsmv = c5.number_input("BSMV (%)", value=5.0, format="%.2f")
        
        if st.button(T("calc"), type="primary"):
            if n > 0:
                sch = []; bal = loan; total_pay = 0; first_pmt_display = 0
                gross_rate = (rate/100) * (1 + (kkdf+bsmv)/100)

                if plan_type == T("cr_opt1"): # Eşit Taksit
                    if gross_rate > 0: pmt = loan * (gross_rate * (1+gross_rate)**n) / ((1+gross_rate)**n - 1)
                    else: pmt = loan / n
                    first_pmt_display = pmt
                    for i in range(1, int(n)+1):
                        raw_int = bal * (rate/100)
                        tax_k = raw_int * (kkdf/100); tax_b = raw_int * (bsmv/100)
                        princ = pmt - (raw_int + tax_k + tax_b)
                        bal -= princ; total_pay += pmt
                        sch.append([i, fmt(pmt), fmt(princ), fmt(raw_int), fmt(tax_k), fmt(tax_b), fmt(max(0, bal))])
                else: # Eşit Anapara
                    fixed_princ = loan / n 
                    for i in range(1, int(n)+1):
                        raw_int = bal * (rate/100)
                        tax_k = raw_int * (kkdf/100); tax_b = raw_int * (bsmv/100)
                        curr_pmt = fixed_princ + raw_int + tax_k + tax_b
                        if i == 1: first_pmt_display = curr_pmt 
                        bal -= fixed_princ; total_pay += curr_pmt
                        sch.append([i, fmt(curr_pmt), fmt(fixed_princ), fmt(raw_int), fmt(tax_k), fmt(tax_b), fmt(max(0, bal))])

                m1, m2 = st.columns(2)
                m1.metric(T("pmt_res"), f"{fmt(first_pmt_display)} ₺")
                m2.metric(T("pmt_res_total"), f"{fmt(total_pay)} ₺")
                if st.session_state.page == "table":
                    st.write("---")
                    st.dataframe(pd.DataFrame(sch, columns=T("tbl_cols")), use_container_width=True, hide_index=True)

elif st.session_state.page == "disc":
    st.subheader(T("m_disc"))
    st.divider()
    with st.container(border=True):
        receiv = st.number_input(T("dc_rec"), value=0.0, step=1000.0, format="%.2f")
        days = st.number_input(T("dc_day"), value=0)
        r_alt = st.number_input(T("dc_rate"), value=0.0, format="%.2f")
        
        if st.button(T("calc"), type="primary"):
            r = r_alt / 100
            if days > 0:
                pv = receiv / ((1 + r)**(days/365))
                disc_amt = receiv - pv
                c1, c2 = st.columns(2)
                c1.metric(T("dc_r1"), f"{fmt(pv)} ₺")
                c2.metric(T("dc_r2"), f"{fmt(disc_amt)} ₺", delta=f"-{fmt(disc_amt)} ₺")
