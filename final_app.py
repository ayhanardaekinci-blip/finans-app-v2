import streamlit as st
import pandas as pd

# =========================================================
# 1) AYARLAR
# =========================================================
st.set_page_config(
    page_title="Finansal Hesap Makinesi",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# 2) STATE INIT (HAFIZA)
# =========================================================
if "lang" not in st.session_state: st.session_state.lang = "TR"
if "page" not in st.session_state: st.session_state.page = "home"
if "dark_mode" not in st.session_state: st.session_state.dark_mode = False

# =========================================================
# 3) DİL SÖZLÜKLERİ
# =========================================================
TR = {
    "app_name": "Finansal Hesap Makinesi",
    "subheader": "Eczacıbaşı Sağlık Hazine Departmanı",
    "home": "🏠 Ana Menü",
    "mode_toggle": "Gece Modu",
    "m_invest": "Yatırım Getiri Oranı", "m_rates": "Basit - Bileşik Faiz",
    "m_single": "Tek Dönemlik Faiz", "m_comp": "Bileşik Faizle Para",
    "m_install": "Kredi / Taksit Hesapla", "m_table": "Ödeme Tablosu Oluştur",
    "m_disc": "⚡ İskontolu Alacak Hesapla", "m_deposit": "🏦 Mevduat Getirisi (Stopajlı)",
    "m_npv": "📉 NPV (Net Bugünkü Değer)",
    "calc": "HESAPLA", "days_365": "Baz Gün (365/360)", "tax": "Vergi Oranı (%)",
    "cr_type": "Ödeme Planı Türü", "cr_opt1": "Eşit Taksitli (Standart)", "cr_opt2": "Eşit Anaparalı (Azalan)",
    "kkdf": "KKDF (%)", "bsmv": "BSMV (%)",
    "inv_buy": "Alış Tutarı", "inv_sell": "Satış Tutarı", "inv_day": "Vade (Gün)",
    "rt_what": "Ne Hesaplayalım?", "rt_days": "Gün Sayısı", "rt_base": "Baz Oran (%)",
    "opt_comp_rate": "Yıllık Bileşik Faiz (%)", "opt_simp_rate": "Yıllık Basit Faiz (%)",
    "rt_res": "Hesaplanan Oran", "s_p": "Anapara", "s_r": "Yıllık Faiz (%)", "s_d": "Vade (Gün)",
    "s_note": "Mevduat (-), Kredi (+)", "s_r1": "Faiz Tutarı", "s_r2": "Vade Sonu Toplam",
    "cm_what": "Ne Hesaplanacak?", "cm_r": "Dönemsel Faiz (%)", "cm_n": "Dönem Sayısı",
    "opt_pv": "Anapara (PV)", "opt_fv": "Vade Sonu (FV)", "cm_res": "Hesaplanan Tutar", "cm_res_diff": "Faiz Farkı",
    "pmt_loan": "Kredi Tutarı", "pmt_r": "Aylık Faiz (%)", "pmt_n": "Taksit Sayısı", "pmt_res": "İlk Taksit Tutarı",
    "pmt_res_total": "Toplam Geri Ödeme", "dc_rec": "Fatura/Alacak Tutarı", "dc_day": "Erken Ödeme Günü",
    "dc_rate": "Alternatif Getiri (%)", "dc_r1": "Ele Geçecek Tutar", "dc_r2": "Yapılan İskonto (İndirim)",
    "dep_amt": "Yatırılan Tutar (Mevduat)", "dep_days": "Vade (Gün)", "dep_rate": "Yıllık Faiz Oranı (%)",
    "dep_res_net": "Net Getiri (Ele Geçen)", "dep_res_total": "Vade Sonu Toplam Bakiye",
    "dep_info_stopaj": "Uygulanan Stopaj Oranı", "dep_info_desc": "ℹ️ 2025 Düzenlemesine göre vadeye bağlı otomatik stopaj uygulanmıştır.",
    "inv_r1": "Dönemsel Getiri", "inv_r2": "Yıllık Basit Getiri", "inv_r3": "Yıllık Bileşik Getiri",
    "tbl_cols": ["Dönem", "Taksit", "Anapara", "Faiz", "KKDF", "BSMV", "Kalan Borç"],
    "npv_c0": "Başlangıç Yatırımı (CF0)", "npv_rate": "İskonto Oranı (%)", "npv_n": "Dönem Sayısı (N)",
    "npv_cf": "Nakit Akışı (CF)", "npv_res": "NPV (Net Bugünkü Değer)", "npv_pv_sum": "Gelecek Akışlar PV Toplamı",
    "npv_hint": "ℹ️ CF0 genelde negatiftir (yatırım). CF1..CFN nakit giriş/çıkışlarıdır.",
}
EN = TR.copy(); FR = TR.copy(); DE = TR.copy()
EN["mode_toggle"] = "Dark Mode"; FR["mode_toggle"] = "Mode Sombre"; DE["mode_toggle"] = "Dunkelmodus"
LANGS = {"TR": TR, "EN": EN, "FR": FR, "DE": DE}

def T(key: str) -> str: return LANGS[st.session_state.lang].get(key, key)
def fmt(value):
    if value is None: return "0,00"
    try: s = "{:,.2f}".format(float(value)); return s.replace(",", "X").replace(".", ",").replace("X", ".")
    except: return "0,00"
def go(page: str): st.session_state.page = page; st.rerun()
def update_lang(): st.session_state.lang = st.session_state.l_sel.split(" ")[1]
def toggle_theme(): st.session_state.dark_mode = not st.session_state.dark_mode

# =========================================================
# 4) RENKLER (KRİTİK: CSS'DEN ÖNCE TANIMLANMALI)
# =========================================================
is_dark = st.session_state.dark_mode

if is_dark:
    # GECE MODU
    bg_color = "#0e1117"
    card_bg = "#1f2430"
    input_bg = "#262730"
    text_color = "#ffffff"
    muted_text = "#cbd5e1"
    input_text = "#ffffff" # Kutuların içindeki yazı BEYAZ
    border_color = "#3b4252"
    metric_color = "#4dabf7"
    shadow = "0.22"
    toggle_bg = "#2b2f36"
    toggle_knob = "#ffffff"
else:
    # GÜNDÜZ MODU
    bg_color = "#ffffff"
    card_bg = "#f6f7fb"
    input_bg = "#ffffff"
    text_color = "#111827"
    muted_text = "#475569"
    input_text = "#000000" # Kutuların içindeki yazı SİYAH
    border_color = "#e5e7eb"
    metric_color = "#0d25cf"
    shadow = "0.10"
    toggle_bg = "#e5e7eb"
    toggle_knob = "#111827"

# =========================================================
# 5) CSS (HATA DÜZELTMELERİ YAPILDI)
# =========================================================
st.markdown(f"""
<style>
/* 1. GENEL ARKAPLAN */
.stApp {{
  background: {bg_color};
  color: {text_color};
}}
/* 2. YAN MENÜYÜ GİZLE */
[data-testid="stSidebar"] {{display: none;}}

/* 3. BOŞLUKLARI AL */
.block-container {{
  padding-top: 1rem !important;
  padding-bottom: 2rem !important;
  max-width: 1240px;
}}

/* 4. METİN RENKLERİNİ ZORLA (Okunurluk Fix) */
h1, h2, h3, h4, h5, h6, p, label, span, div, li {{
  color: {text_color} !important;
}}
.stCaption {{
  color: {muted_text} !important;
}}

/* 5. INPUT KUTULARI (Siyah üstüne siyah yazı sorununu çözer) */
.stNumberInput input {{
  background-color: {input_bg} !important;
  color: {input_text} !important;
  border: 1px solid {border_color} !important;
  font-weight: 700 !important;
}}

/* 6. SELECTBOX (Açılır Menü) Düzeltmesi */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
    background-color: {input_bg} !important;
    border-color: {border_color} !important;
    color: {input_text} !important;
}}
div[data-testid="stSelectbox"] div[data-baseweb="select"] span {{
    color: {input_text} !important;
}}
/* Açılır listenin kendisi */
ul[data-baseweb="menu"] {{
    background-color: {input_bg} !important;
}}
ul[data-baseweb="menu"] li {{
    color: {input_text} !important;
}}

/* 7. BUTONLAR */
div.stButton > button:first-child {{
  width: 100%; height: 3em; border-radius: 8px;
  border: 1px solid {border_color}; font-weight: 700;
  background: {card_bg}; color: {text_color};
  box-shadow: 0 2px 5px rgba(0,0,0,{shadow});
}}

/* 8. SONUÇ RAKAMLARI */
div[data-testid="stMetricValue"] {{
  font-size: 1.6rem !important;
  color: {metric_color} !important;
  font-weight: 900 !important;
}}

/* =========================================
   9. CHECKBOX HACK (Tik Yerine Switch) 
   ========================================= */

/* Gece Modu Yazısı: Mor Renk (#8A2BE2) */
div[data-testid="stCheckbox"] label p {{
    color: #8A2BE2 !important;
    font-weight: 800 !important;
    font-size: 1.1rem !important;
}}

/* Standart Tiki (SVG) Gizle */
div[data-testid="stCheckbox"] svg {{
    display: none !important;
}}

/* Kutuyu Gizle, Yerine Hap Şekli Çiz */
div[data-testid="stCheckbox"] input[type="checkbox"] {{
    appearance: none !important;
    -webkit-appearance: none !important;
    width: 50px !important;
    height: 26px !important;
    border-radius: 15px !important;
    background: {toggle_bg} !important;
    border: 1px solid {border_color} !important;
    outline: none !important;
    cursor: pointer !important;
    position: relative !important;
}}

/* İçindeki Yuvarlak Topu Çiz */
div[data-testid="stCheckbox"] input[type="checkbox"]::after {{
    content: "";
    position: absolute !important;
    top: 2px !important;
    left: 2px !important;
    width: 20px !important;
    height: 20px !important;
    border-radius: 50% !important;
    background: {toggle_knob} !important;
    transition: all 0.3s ease !important;
    display: block !important;
}}

/* Tıklanınca (Checked) Durumu */
div[data-testid="stCheckbox"] input[type="checkbox"]:checked {{
    background: #8A2BE2 !important; /* Mor Arka Plan */
    border-color: #8A2BE2 !important;
}}
div[data-testid="stCheckbox"] input[type="checkbox"]:checked::after {{
    left: 26px !important; /* Sağa Kaydır */
    background: #ffffff !important;
}}

</style>
""", unsafe_allow_html=True)

# =========================================================
# 6) HEADER (ÜST MENÜ)
# =========================================================
c1, c2, c3, c4 = st.columns([5, 2, 2, 1], vertical_alignment="center")

with c1:
    st.markdown(f"#### {T('app_name')}")
    st.caption(T("subheader"))

with c2:
    st.selectbox("Dil / Language", ["🇹🇷 TR", "🇬🇧 EN", "🇫🇷 FR", "🇩🇪 DE"], key="l_sel", on_change=update_lang, label_visibility="collapsed")

with c3:
    # Checkbox'ı Switch gibi gösteriyoruz
    st.checkbox(T("mode_toggle"), value=st.session_state.dark_mode, key="dark_mode_chk", on_change=toggle_theme)

with c4:
    if st.button("🏠", key="home_btn"): go("home")

st.divider()

# =========================================================
# 7) SAYFALAR
# =========================================================

if st.session_state.page == "home":
    st.info(T("info_sel"))
    c1, c2 = st.columns(2)
    with c1:
        if st.button(T("m_invest"), use_container_width=True): go("invest")
        if st.button(T("m_comp"), use_container_width=True): go("comp")
        if st.button(T("m_single"), use_container_width=True): go("single")
        if st.button(T("m_deposit"), use_container_width=True): go("deposit")
        if st.button(T("m_npv"), use_container_width=True): go("npv")
    with c2:
        if st.button(T("m_rates"), use_container_width=True): go("rates")
        if st.button(T("m_install"), use_container_width=True): go("install")
        if st.button(T("m_table"), use_container_width=True): go("table")
        if st.button(T("m_disc"), use_container_width=True): go("disc")

elif st.session_state.page == "invest":
    st.title(T("m_invest"))
    st.divider()
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1: buy = st.number_input(T("inv_buy"), value=0.0, format="%.2f", key="inv_buy")
        with c2: sell = st.number_input(T("inv_sell"), value=0.0, format="%.2f", key="inv_sell")
        days = st.number_input(T("inv_day"), value=30, step=1, key="inv_days")
        if st.button(T("calc"), type="primary"):
            if buy > 0 and days > 0:
                per = (sell - buy) / buy
                ann_s = per * (365 / days)
                ann_c = ((1 + per) ** (365 / days)) - 1
                r1, r2, r3 = st.columns(3)
                r1.metric(T("inv_r1"), f"%{fmt(per*100)}")
                r2.metric(T("inv_r2"), f"%{fmt(ann_s*100)}")
                r3.metric(T("inv_r3"), f"%{fmt(ann_c*100)}")

elif st.session_state.page == "rates":
    st.title(T("m_rates"))
    st.divider()
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1: mode = st.selectbox(T("rt_what"), [T("opt_comp_rate"), T("opt_simp_rate")], key="rt_mode")
        with c2: days = st.number_input(T("rt_days"), value=365, key="rt_days")
        base = st.number_input(T("rt_base"), value=0.0, format="%.2f", key="rt_base")
        if st.button(T("calc"), type="primary"):
            r = base / 100
            if days > 0:
                if mode == T("opt_comp_rate"): res = ((1 + r * (days / 365)) ** (365 / days)) - 1
                else: res = (((1 + r) ** (days / 365)) - 1) * (365 / days)
                st.metric(T("rt_res"), f"%{fmt(res*100)}")

elif st.session_state.page == "single":
    st.title(T("m_single"))
    st.divider()
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1: p = st.number_input(T("s_p"), value=0.0, step=1000.0, format="%.2f", key="s_p")
        with c2: r = st.number_input(T("s_r"), value=0.0, format="%.2f", key="s_r")
        c3, c4 = st.columns(2)
        with c3: d = st.number_input(T("s_d"), value=32, key="s_d")
        with c4: tax = st.number_input(T("tax"), value=0.0, format="%.2f", help=T("s_note"), key="s_tax")
        day_base = st.selectbox(T("days_365"), [365, 360], key="s_base")
        if st.button(T("calc"), type="primary"):
            gross = (p * r * d) / (day_base * 100)
            net = gross * (1 - tax / 100)
            m1, m2 = st.columns(2)
            m1.metric(T("s_r1"), f"{fmt(net)} ₺")
            m2.metric(T("s_r2"), f"{fmt(p + net)} ₺")

elif st.session_state.page == "comp":
    st.title(T("m_comp"))
    st.divider()
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1: target = st.selectbox(T("cm_what"), [T("opt_pv"), T("opt_fv")], key="cm_target")
        with c2: 
            lbl = T("opt_fv") if target == T("opt_pv") else T("opt_pv")
            val = st.number_input(lbl, value=0.0, step=1000.0, format="%.2f", key="cm_val")
        c3, c4 = st.columns(2)
        with c3: r = st.number_input(T("cm_r"), value=0.0, format="%.2f", key="cm_r")
        with c4: n = st.number_input(T("cm_n"), value=1, key="cm_n")
        tax = st.number_input(T("tax"), value=0.0, format="%.2f", key="cm_tax")
        if st.button(T("calc"), type="primary"):
            net_r = (r / 100) * (1 - tax / 100)
            if target == T("opt_pv"): res = val / ((1 + net_r) ** n)
            else: res = val * ((1 + net_r) ** n)
            m1, m2 = st.columns(2)
            m1.metric(T("cm_res"), f"{fmt(res)} ₺")
            m2.metric(T("cm_res_diff"), f"{fmt(abs(val - res))} ₺")

elif st.session_state.page == "deposit":
    st.title(T("m_deposit"))
    st.divider()
    st.info(T("dep_info_desc"))
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1: amount = st.number_input(T("dep_amt"), value=100000.0, step=1000.0, format="%.2f", key="dep_amt")
        with c2: rate = st.number_input(T("dep_rate"), value=45.0, format="%.2f", key="dep_rate")
        days = st.number_input(T("dep_days"), value=32, step=1, key="dep_days")
        if st.button(T("calc"), type="primary"):
            if days <= 182: stopaj = 17.5
            elif days <= 365: stopaj = 15.0
            else: stopaj = 10.0
            gross = (amount * rate * days) / 36500
            net = gross * (1 - stopaj / 100)
            total = amount + net
            c1, c2, c3 = st.columns(3)
            c1.metric(T("dep_info_stopaj"), f"%{stopaj}")
            c2.metric(T("dep_res_net"), f"{fmt(net)} ₺")
            c3.metric(T("dep_res_total"), f"{fmt(total)} ₺")

elif st.session_state.page in ["install", "table"]:
    st.title(T("m_install") if st.session_state.page == "install" else T("m_table"))
    st.divider()
    with st.container(border=True):
        plan_type = st.radio(T("cr_type"), [T("cr_opt1"), T("cr_opt2")], horizontal=True, key="cr_plan")
        c1, c2 = st.columns(2)
        with c1: loan = st.number_input(T("pmt_loan"), value=100000.0, step=1000.0, format="%.2f", key="pmt_loan")
        with c2: rate = st.number_input(T("pmt_r"), value=1.20, format="%.2f", key="pmt_rate")
        c3, c4, c5 = st.columns(3)
        with c3: n = st.number_input(T("pmt_n"), value=12, key="pmt_n")
        with c4: kkdf = st.number_input(T("kkdf"), value=15.0, format="%.2f", key="pmt_kkdf")
        with c5: bsmv = st.number_input(T("bsmv"), value=5.0, format="%.2f", key="pmt_bsmv")
        if st.button(T("calc"), type="primary"):
            sch = []; bal = loan; total_pay = 0; first_pmt = 0
            gross = (rate / 100) * (1 + (kkdf + bsmv) / 100)
            if plan_type == T("cr_opt1"):
                if gross > 0: pmt = loan * (gross * (1 + gross) ** n) / ((1 + gross) ** n - 1)
                else: pmt = loan / n
                first_pmt = pmt
                for i in range(1, int(n) + 1):
                    raw_int = bal * (rate / 100); tax_k = raw_int * (kkdf / 100); tax_b = raw_int * (bsmv / 100)
                    princ = pmt - (raw_int + tax_k + tax_b); bal -= princ; total_pay += pmt
                    sch.append([i, fmt(pmt), fmt(princ), fmt(raw_int), fmt(tax_k), fmt(tax_b), fmt(max(0, bal))])
            else:
                fixed = loan / n
                for i in range(1, int(n) + 1):
                    raw_int = bal * (rate / 100); tax_k = raw_int * (kkdf / 100); tax_b = raw_int * (bsmv / 100)
                    curr = fixed + raw_int + tax_k + tax_b
                    if i == 1: first_pmt = curr
                    bal -= fixed; total_pay += curr
                    sch.append([i, fmt(curr), fmt(fixed), fmt(raw_int), fmt(tax_k), fmt(tax_b), fmt(max(0, bal))])
            m1, m2 = st.columns(2)
            m1.metric(T("pmt_res"), f"{fmt(first_pmt)} ₺")
            m2.metric(T("pmt_res_total"), f"{fmt(total_pay)} ₺")
            if st.session_state.page == "table":
                st.write("---")
                st.dataframe(pd.DataFrame(sch, columns=T("tbl_cols")), use_container_width=True, hide_index=True)

elif st.session_state.page == "disc":
    st.title(T("m_disc"))
    st.divider()
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1: receiv = st.number_input(T("dc_rec"), value=0.0, step=1000.0, format="%.2f", key="dc_rec")
        with c2: days = st.number_input(T("dc_day"), value=0, key="dc_days")
        r_alt = st.number_input(T("dc_rate"), value=0.0, format="%.2f", key="dc_rate")
        if st.button(T("calc"), type="primary"):
            r = r_alt / 100
            if days > 0:
                pv = receiv / ((1 + r) ** (days / 365)); disc = receiv - pv
                m1, m2 = st.columns(2)
                m1.metric(T("dc_r1"), f"{fmt(pv)} ₺")
                m2.metric(T("dc_r2"), f"{fmt(disc)} ₺")

elif st.session_state.page == "npv":
    st.title(T("m_npv"))
    st.divider()
    st.info(T("npv_hint"))
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1: c0 = st.number_input(T("npv_c0"), value=-100000.0, step=1000.0, format="%.2f", key="npv_c0")
        with c2: rate = st.number_input(T("npv_rate"), value=30.0, format="%.2f", key="npv_rate")
        n = st.number_input(T("npv_n"), value=5, min_value=1, step=1, key="npv_n")
        cols = st.columns(3); flows = []
        for i in range(1, int(n) + 1):
            with cols[(i - 1) % 3]:
                cf = st.number_input(f"{T('npv_cf')} {i}", value=30000.0, step=1000.0, format="%.2f", key=f"npv_cf_{i}")
                flows.append(cf)
        if st.button(T("calc"), type="primary"):
            r = rate / 100.0; pv_sum = 0.0
            for t, cf in enumerate(flows, start=1): pv_sum += cf / ((1 + r) ** t)
            npv = c0 + pv_sum
            m1, m2 = st.columns(2)
            m1.metric(T("npv_res"), f"{fmt(npv)} ₺")
            m2.metric(T("npv_pv_sum"), f"{fmt(pv_sum)} ₺")
