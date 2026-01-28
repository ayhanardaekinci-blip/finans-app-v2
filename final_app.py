import streamlit as st
import pandas as pd
import numpy as np

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="Finansal Hesap Makinesi",
    page_icon="E",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. HAFIZA (SESSION STATE) BAŞLATMA ---
# Sayfa yenilendiğinde ayarların kaybolmaması için
if 'lang' not in st.session_state: st.session_state.lang = "TR"
if 'page' not in st.session_state: st.session_state.page = "home"
if 'dark_mode' not in st.session_state: st.session_state.dark_mode = False

# --- 3. DİL SÖZLÜKLERİ (EMOJİLER SADECE BURADA) ---
TR = {
    "app_name": "Finansal Hesap Makinesi",
    "subheader": "Eczacıbaşı Sağlık Hazine",
    "home": "🏠 Ana Menü",
    "info_sel": "Hesaplama modülünü seçiniz:",
    "mode_dark": "Gece Modu",
    "lang_sel": "Dil",
    
    # Modül İsimleri (Emojili)
    "m_invest": "📈 Yatırım Getiri Oranı",
    "m_rates": "🔄 Basit - Bileşik Faiz",
    "m_single": "📅 Tek Dönemlik Faiz",
    "m_comp": "💰 Bileşik Faizle Para",
    "m_install": "💳 Kredi / Taksit Hesapla",
    "m_table": "📋 Ödeme Tablosu Oluştur",
    "m_disc": "⚡ İskontolu Alacak",
    "m_deposit": "🏦 Mevduat Getirisi",
    
    # Etiketler
    "calc": "HESAPLA", "days_365": "Baz Gün", "tax": "Vergi (%)",
    "cr_type": "Plan Türü", "cr_opt1": "Eşit Taksit", "cr_opt2": "Eşit Anapara",
    "inv_buy": "Alış", "inv_sell": "Satış", "inv_day": "Vade (Gün)",
    "rt_what": "Ne Hesaplayalım?", "rt_days": "Gün", "rt_base": "Baz Oran (%)",
    "s_p": "Anapara", "s_r": "Yıllık Faiz (%)", "s_d": "Vade (Gün)", "s_note": "Mevduat (-), Kredi (+)",
    "cm_what": "Hesap Türü", "cm_val1": "Anapara (PV)", "cm_val2": "Vade Sonu (FV)", "cm_n": "Dönem", "cm_r": "Dönemsel Faiz (%)",
    "pmt_loan": "Kredi Tutarı", "pmt_r": "Aylık Faiz (%)", "pmt_n": "Taksit Sayısı",
    "dc_rec": "Fatura Tutarı", "dc_day": "Erken Ödeme Günü", "dc_rate": "Alternatif Getiri (%)",
    "dep_amt": "Yatırılan Tutar", "dep_days": "Vade (Gün)", "dep_rate": "Yıllık Faiz (%)",
    
    # Sonuçlar
    "inv_r1": "Dönemsel Getiri", "inv_r2": "Yıllık Basit", "inv_r3": "Yıllık Bileşik",
    "rt_res": "Sonuç Oran", "s_r1": "Faiz Tutarı", "s_r2": "Toplam",
    "cm_lbl_res": "Sonuç", "cm_res_diff": "Faiz Farkı",
    "pmt_res": "İlk Taksit", "pmt_res_total": "Toplam Ödeme",
    "dc_r1": "Ele Geçen", "dc_r2": "İskonto Tutarı",
    "dep_res_net": "Net Getiri", "dep_res_total": "Toplam Bakiye",
    "dep_info_stopaj": "Stopaj Oranı",
    "dep_info_desc": "ℹ️ 2025 Stopaj düzenlemesi aktiftir.",
    
    # Tablo ve Seçenekler
    "tbl_cols": ["Dönem", "Taksit", "Anapara", "Faiz", "KKDF", "BSMV", "Kalan"],
    "opt_comp_rate": "Bileşik Faiz (%)", "opt_simp_rate": "Basit Faiz (%)",
    "opt_pv": "Anapara (PV)", "opt_fv": "Vade Sonu (FV)"
}

# Diğer dilleri TR kopyası olarak başlatıp sadece başlıkları değiştiriyoruz (Pratiklik için)
EN = TR.copy(); FR = TR.copy(); DE = TR.copy()
EN["mode_dark"] = "Dark Mode"; FR["mode_dark"] = "Mode Sombre"; DE["mode_dark"] = "Dunkelmodus"
LANGS = {"TR": TR, "EN": EN, "FR": FR, "DE": DE}

# --- 4. YARDIMCI FONKSİYONLAR ---
def T(k): return LANGS[st.session_state.lang].get(k, k)
def update_lang(): st.session_state.lang = st.session_state.l_sel.split(" ")[1]
def go(p): st.session_state.page = p; st.rerun()
def fmt(value):
    if value is None: return "0,00"
    try:
        s = "{:,.2f}".format(float(value))
        return s.replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "0,00"

# --- 5. RENK VE TEMA MANTIĞI (CSS'DEN ÖNCE!) ---
# Hata almamak için renkleri önce tanımlıyoruz.
is_dark = st.session_state.dark_mode

if is_dark:
    # --- GECE MODU ---
    bg_color = "#0e1117"
    card_bg = "#262730"
    text_color = "#ffffff"
    metric_color = "#4dabf7" # Açık Mavi
    input_bg = "#262730"
    input_text = "#ffffff"
    btn_border = "#495057"
else:
    # --- GÜNDÜZ MODU ---
    bg_color = "#ffffff"
    card_bg = "#f8f9fa"
    text_color = "#000000"
    metric_color = "#0d25cf" # Koyu Mavi
    input_bg = "#ffffff"
    input_text = "#000000"
    btn_border = "#dee2e6"

# --- 6. CSS İLE TASARIM (ŞİMDİ GÜVENLE BOYUYORUZ) ---
st.markdown(f"""
<style>
    /* 1. GENEL ARKAPLAN VE YAZI RENGİ */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    
    /* 2. YAN MENÜYÜ TAMAMEN GİZLE */
    [data-testid="stSidebar"] {{display: none;}}
    
    /* 3. TÜM YAZILARI ZORLA RENKLENDİR (Görünmezlik Önlemi) */
    h1, h2, h3, h4, h5, h6, p, label, span, div, li {{
        color: {text_color} !important;
    }}
    
    /* Gece Modu Tikinin Yanındaki Yazı */
    div[data-testid="stMarkdownContainer"] p {{
        color: {text_color} !important;
        font-weight: bold;
    }}

    /* 4. HEADER (Üst Kısım) DÜZENİ */
    .header-container {{
        padding-bottom: 20px;
        border-bottom: 1px solid {btn_border};
    }}

    /* 5. INPUT KUTULARI (Selectbox ve NumberInput) */
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        color: {input_text} !important; 
        font-weight: 700 !important;
        background-color: {input_bg} !important; 
        border: 1px solid {btn_border} !important;
    }}
    /* Selectbox içindeki açılır menü */
    ul[data-baseweb="menu"] {{
        background-color: {input_bg} !important;
    }}
    
    /* 6. BUTONLAR */
    div.stButton > button:first-child {{
        width: 100%; 
        height: 3.5em; /* Mobil için ideal yükseklik */
        border-radius: 8px; 
        border: 1px solid {btn_border}; 
        font-weight: 700; 
        background: {card_bg}; 
        color: {text_color} !important; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    
    /* 7. SONUÇ RAKAMLARI */
    div[data-testid="stMetricValue"] {{
        color: {metric_color} !important; font-weight: 800 !important;
    }}
    
    /* 8. OK İŞARETLERİ */
    svg {{ fill: {text_color} !important; }}
</style>
""", unsafe_allow_html=True)

# --- 7. HEADER (ÜST MENÜ - MOBİL DOSTU) ---
# Burası her sayfanın tepesinde sabit kalır

top_c1, top_c2, top_c3 = st.columns([6, 3, 2])

with top_c1:
    # Logo ve Başlık
    st.markdown(f"### {T('app_name')}")
    st.caption(T("subheader"))

with top_c2:
    # Dil Seçimi
    st.selectbox(T("lang_sel"), ["🇹🇷 TR", "🇬🇧 EN", "🇫🇷 FR", "🇩🇪 DE"], key="l_sel", on_change=update_lang, label_visibility="collapsed")

with top_c3:
    # Gece Modu (Toggle)
    st.session_state.dark_mode = st.toggle(T("mode_dark"), value=st.session_state.dark_mode)

# Eğer Ana Sayfada değilsek, bir "Geri Dön" butonu koyalım
if st.session_state.page != "home":
    if st.button(f"⬅️ {T('home')}", type="secondary"):
        go("home")

st.divider()

# --- 8. SAYFALAR VE MODÜLLER ---

if st.session_state.page == "home":
    st.info(T("info_sel"))
    
    # 2 Sütunlu Izgara (Mobil Uyumlu)
    c1, c2 = st.columns(2)
    
    with c1:
        if st.button(T("m_invest"), use_container_width=True): go("invest")
        if st.button(T("m_comp"), use_container_width=True): go("comp")
        if st.button(T("m_single"), use_container_width=True): go("single")
        if st.button(T("m_deposit"), use_container_width=True): go("deposit")
        
    with c2:
        if st.button(T("m_rates"), use_container_width=True): go("rates")
        if st.button(T("m_install"), use_container_width=True): go("install")
        if st.button(T("m_table"), use_container_width=True): go("table")
        if st.button(T("m_disc"), use_container_width=True): go("disc")

# --- HESAPLAMA EKRANLARI ---

elif st.session_state.page == "invest":
    st.subheader(T("m_invest"))
    c1, c2 = st.columns(2)
    with c1: buy = st.number_input(T("inv_buy"), value=0.0, format="%.2f", key="inv_buy")
    with c2: sell = st.number_input(T("inv_sell"), value=0.0, format="%.2f", key="inv_sell")
    days = st.number_input(T("inv_day"), value=30, step=1, key="inv_days")
    if st.button(T("calc"), type="primary", use_container_width=True):
        if buy > 0 and days > 0:
            per = (sell - buy) / buy
            ann_s = per * (365/days); ann_c = ((1 + per)**(365/days)) - 1
            r1, r2, r3 = st.columns(3)
            r1.metric(T("inv_r1"), f"%{fmt(per*100)}")
            r2.metric(T("inv_r2"), f"%{fmt(ann_s*100)}")
            r3.metric(T("inv_r3"), f"%{fmt(ann_c*100)}")

elif st.session_state.page == "rates":
    st.subheader(T("m_rates"))
    c1, c2 = st.columns(2)
    with c1: mode = st.selectbox(T("rt_what"), [T("opt_comp_rate"), T("opt_simp_rate")], key="rt_mode")
    with c2: days = st.number_input(T("rt_days"), value=365, key="rt_days")
    base = st.number_input(T("rt_base"), value=0.0, format="%.2f", key="rt_base")
    if st.button(T("calc"), type="primary", use_container_width=True):
        r = base / 100
        if days > 0:
            if mode == T("opt_comp_rate"): res = ((1 + r * (days/365))**(365/days)) - 1
            else: res = (((1 + r)**(days/365)) - 1) * (365/days)
            st.metric(T("rt_res"), f"%{fmt(res*100)}")

elif st.session_state.page == "single":
    st.subheader(T("m_single"))
    c1, c2 = st.columns(2)
    with c1: p = st.number_input(T("s_p"), value=0.0, step=1000.0, format="%.2f", key="s_p")
    with c2: r = st.number_input(T("s_r"), value=0.0, format="%.2f", key="s_r")
    c3, c4 = st.columns(2)
    with c3: d = st.number_input(T("s_d"), value=32, key="s_d")
    with c4: tax = st.number_input(T("tax"), value=0.0, format="%.2f", key="s_tax")
    if st.button(T("calc"), type="primary", use_container_width=True):
        gross = (p * r * d) / 36500; net = gross * (1 - tax/100)
        m1, m2 = st.columns(2)
        m1.metric(T("s_r1"), f"{fmt(net)} ₺")
        m2.metric(T("s_r2"), f"{fmt(p+net)} ₺")

elif st.session_state.page == "comp":
    st.subheader(T("m_comp"))
    c1, c2 = st.columns(2)
    with c1: target = st.selectbox(T("cm_what"), [T("opt_pv"), T("opt_fv")], key="cm_target")
    with c2: 
        lbl = T("opt_fv") if target == T("opt_pv") else T("opt_pv")
        val = st.number_input(lbl, value=0.0, step=1000.0, format="%.2f", key="cm_val")
    c3, c4 = st.columns(2)
    with c3: r = st.number_input(T("cm_r"), value=0.0, format="%.2f", key="cm_r")
    with c4: n = st.number_input(T("cm_n"), value=1, key="cm_n")
    if st.button(T("calc"), type="primary", use_container_width=True):
        net_r = r/100
        if target == T("opt_pv"): res = val / ((1 + net_r)**n); res_lbl = T("opt_pv")
        else: res = val * ((1 + net_r)**n); res_lbl = T("opt_fv")
        m1, m2 = st.columns(2)
        m1.metric(res_lbl, f"{fmt(res)} ₺")
        m2.metric(T("cm_res_diff"), f"{fmt(abs(val-res))} ₺")

elif st.session_state.page == "deposit":
    st.subheader(T("m_deposit"))
    st.info(T("dep_info_desc"))
    c1, c2 = st.columns(2)
    with c1: amount = st.number_input(T("dep_amt"), value=100000.0, step=1000.0, format="%.2f", key="dep_amt")
    with c2: rate = st.number_input(T("dep_rate"), value=45.0, format="%.2f", key="dep_rate")
    days = st.number_input(T("dep_days"), value=32, step=1, key="dep_days")
    if st.button(T("calc"), type="primary", use_container_width=True):
        if days <= 182: stopaj_rate = 17.5
        elif days <= 365: stopaj_rate = 15.0
        else: stopaj_rate = 10.0
        gross = (amount * rate * days) / 36500
        net = gross * (1 - stopaj_rate/100)
        c1, c2, c3 = st.columns(3)
        c1.metric(T("dep_info_stopaj"), f"%{stopaj_rate}")
        c2.metric(T("dep_res_net"), f"{fmt(net)} ₺")
        c3.metric(T("dep_res_total"), f"{fmt(amount + net)} ₺")

elif st.session_state.page in ["install", "table"]:
    st.subheader(T("m_install") if st.session_state.page=="install" else T("m_table"))
    plan_type = st.radio(T("cr_type"), [T("cr_opt1"), T("cr_opt2")], horizontal=True, key="cr_plan")
    c1, c2 = st.columns(2)
    with c1: loan = st.number_input(T("pmt_loan"), value=100000.0, step=1000.0, format="%.2f", key="pmt_loan")
    with c2: rate = st.number_input(T("pmt_r"), value=1.20, format="%.2f", key="pmt_rate")
    c3, c4, c5 = st.columns(3)
    with c3: n = st.number_input(T("pmt_n"), value=12, key="pmt_n")
    with c4: kkdf = st.number_input("KKDF (%)", value=15.0, format="%.2f", key="pmt_kkdf")
    with c5: bsmv = st.number_input("BSMV (%)", value=5.0, format="%.2f", key="pmt_bsmv")
    if st.button(T("calc"), type="primary", use_container_width=True):
        sch = []; bal = loan; total_pay = 0; first_pmt = 0
        gross_rate = (rate/100) * (1 + (kkdf+bsmv)/100)
        if plan_type == T("cr_opt1"): 
            if gross_rate > 0: pmt = loan * (gross_rate * (1+gross_rate)**n) / ((1+gross_rate)**n - 1)
            else: pmt = loan / n
            first_pmt = pmt
            for i in range(1, int(n)+1):
                raw_int = bal * (rate/100); tax_k = raw_int * (kkdf/100); tax_b = raw_int * (bsmv/100)
                princ = pmt - (raw_int + tax_k + tax_b); bal -= princ; total_pay += pmt
                sch.append([i, fmt(pmt), fmt(princ), fmt(raw_int), fmt(tax_k), fmt(tax_b), fmt(max(0, bal))])
        else: 
            fixed_princ = loan / n 
            for i in range(1, int(n)+1):
                raw_int = bal * (rate/100); tax_k = raw_int * (kkdf/100); tax_b = raw_int * (bsmv/100)
                curr_pmt = fixed_princ + raw_int + tax_k + tax_b
                if i == 1: first_pmt = curr_pmt 
                bal -= fixed_princ; total_pay += curr_pmt
                sch.append([i, fmt(curr_pmt), fmt(fixed_princ), fmt(raw_int), fmt(tax_k), fmt(tax_b), fmt(max(0, bal))])
        m1, m2 = st.columns(2)
        m1.metric(T("pmt_res"), f"{fmt(first_pmt)} ₺")
        m2.metric(T("pmt_res_total"), f"{fmt(total_pay)} ₺")
        if st.session_state.page == "table":
            st.write("---")
            st.dataframe(pd.DataFrame(sch, columns=T("tbl_cols")), use_container_width=True, hide_index=True)

elif st.session_state.page == "disc":
    st.subheader(T("m_disc"))
    c1, c2 = st.columns(2)
    with c1: receiv = st.number_input(T("dc_rec"), value=0.0, step=1000.0, format="%.2f", key="dc_rec")
    with c2: days = st.number_input(T("dc_day"), value=0, key="dc_days")
    r_alt = st.number_input(T("dc_rate"), value=0.0, format="%.2f", key="dc_rate")
    if st.button(T("calc"), type="primary", use_container_width=True):
        r = r_alt / 100
        if days > 0:
            pv = receiv / ((1 + r)**(days/365)); disc_amt = receiv - pv
            m1, m2 = st.columns(2)
            m1.metric(T("dc_r1"), f"{fmt(pv)} ₺")
            m2.metric(T("dc_r2"), f"{fmt(disc_amt)} ₺", delta=f"-{fmt(disc_amt)} ₺")
