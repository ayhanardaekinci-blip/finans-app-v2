import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf # IRR hesabı için

# --- 1. AYARLAR (EN BAŞTA OLMALI) ---
st.set_page_config(
    page_title="Finans Pro Ultimate",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS & MOBİL TASARIM ---
st.markdown("""
<style>
    .block-container {padding-top: 1rem; padding-bottom: 3rem;}
    /* Kart Görünümlü Butonlar */
    div.stButton > button:first-child {
        width: 100%; height: 4em; border-radius: 15px; border: 1px solid #ddd;
        font-weight: 700; background: linear-gradient(to bottom, #ffffff, #f8f9fa);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); color: #333; transition: all 0.2s;
    }
    div.stButton > button:hover {
        transform: translateY(-3px); box-shadow: 0 6px 12px rgba(0,123,255,0.15);
        border-color: #007bff; color: #007bff;
    }
    /* Metrikler */
    div[data-testid="stMetricValue"] {font-size: 1.4rem !important; color: #2e86de;}
</style>
""", unsafe_allow_html=True)

# --- 3. DİL SÖZLÜĞÜ (9 MODÜL İÇİN) ---
TR = {
    "flag": "🇹🇷", "home": "🏠 Ana Menü", "lang": "Dil / Language",
    "welcome": "Finansal Kontrol Merkezi", "sub": "Kurumsal & Bireysel Finans Yönetimi",
    # Menü
    "m_euro": "🌍 Eurobond Analizi", "m_cred": "💳 Kredi Hesapla",
    "m_depo": "💰 Mevduat Getirisi", "m_inv": "📈 Yatırım Getirisi",
    "m_rat": "📊 Finansal Oranlar", "m_tvm1": "⏳ Para Zaman (FV/PV)",
    "m_tvm2": "📉 İç Verim (IRR/NPV)", "m_com": "💸 Komisyon Maliyeti",
    "m_bond": "📜 Bono / Tahvil",
    # Genel
    "calc": "HESAPLA", "back": "⬅️ Ana Menüye Dön", "res": "Sonuçlar",
    # Eurobond
    "eb_inc": "Yıllık Kupon ($)", "eb_rate": "Dolar Kuru", "eb_res": "TL Karşılığı",
    "eb_warn": "⚠️ BEYAN GEREKİR (> {lim})", "eb_ok": "✅ BEYAN GEREKMEZ (< {lim})",
    # Kredi
    "cr_amt": "Kredi Tutarı", "cr_rate": "Aylık Faiz (%)", "cr_term": "Vade (Ay)",
    "cr_res": "Taksit Tutarı", "cr_tot": "Toplam Ödeme",
    # Mevduat
    "dp_amt": "Ana Para", "dp_rate": "Yıllık Faiz (%)", "dp_day": "Gün", "dp_stop": "Stopaj (%)",
    "dp_net": "Net Getiri",
    # Yatırım
    "in_buy": "Alış Fiyatı", "in_sell": "Satış Fiyatı", "in_day": "Gün",
    "in_sim": "Basit Getiri", "in_ann": "Yıllıklandırılmış",
    # Oranlar
    "rt_pv": "Ana Para (PV)", "rt_r": "Oran (%)", "rt_n": "Dönem", "rt_type": "Tip",
    "rt_simp": "Basit Faiz", "rt_comp": "Bileşik Faiz", "rt_fv": "Gelecek Değer (FV)",
    # TVM 1
    "tvm_r": "Dönemsel Oran (%)", "tvm_n": "Dönem Sayısı", "tvm_val": "Mevcut Değer",
    "tvm_fv": "Gelecek Değer (FV)", "tvm_pv": "Bugünkü Değer (PV)",
    # TVM 2
    "irr_cf": "Nakit Akışları (Virgülle ayırın: -100, 10, 110)", "irr_res": "İç Verim Oranı (IRR)",
    "npv_r": "İskonto Oranı (%)", "npv_res": "Net Bugünkü Değer (NPV)",
    # Komisyon
    "cm_amt": "İşlem Tutarı", "cm_day": "Vade (Gün)", "cm_comm": "Komisyon Tutarı", "cm_rate": "Piyasa Faizi (%)",
    "cm_cost": "Toplam Maliyet", "cm_eff": "Efektif Yıllık Oran",
    # Bono
    "bd_nom": "Nominal Değer", "bd_price": "Fiyat", "bd_res": "Basit Faiz", "bd_comp": "Bileşik Faiz"
}

EN = {
    "flag": "🇬🇧", "home": "🏠 Home", "lang": "Language",
    "welcome": "Financial Control Center", "sub": "Corporate & Personal Finance",
    "m_euro": "🌍 Eurobond Analysis", "m_cred": "💳 Loan Calculator",
    "m_depo": "💰 Deposit Return", "m_inv": "📈 Investment ROI",
    "m_rat": "📊 Financial Ratios", "m_tvm1": "⏳ TVM (FV/PV)",
    "m_tvm2": "📉 IRR / NPV Analysis", "m_com": "💸 Commission Cost",
    "m_bond": "📜 Bond / Bill",
    "calc": "CALCULATE", "back": "⬅️ Back to Menu", "res": "Results",
    "eb_inc": "Annual Coupon ($)", "eb_rate": "Exchange Rate", "eb_res": "TRY Equivalent",
    "eb_warn": "⚠️ DECLARATION REQUIRED (> {lim})", "eb_ok": "✅ NO DECLARATION (< {lim})",
    "cr_amt": "Loan Amount", "cr_rate": "Monthly Rate (%)", "cr_term": "Term (Months)",
    "cr_res": "Monthly Payment", "cr_tot": "Total Repayment",
    "dp_amt": "Principal", "dp_rate": "Annual Rate (%)", "dp_day": "Days", "dp_stop": "Withholding (%)",
    "dp_net": "Net Return",
    "in_buy": "Buy Price", "in_sell": "Sell Price", "in_day": "Days Held",
    "in_sim": "Simple Return", "in_ann": "Annualized",
    "rt_pv": "Principal (PV)", "rt_r": "Rate (%)", "rt_n": "Periods", "rt_type": "Type",
    "rt_simp": "Simple Interest", "rt_comp": "Compound Interest", "rt_fv": "Future Value",
    "tvm_r": "Periodic Rate (%)", "tvm_n": "Periods", "tvm_val": "Present Value",
    "tvm_fv": "Future Value", "tvm_pv": "Present Value",
    "irr_cf": "Cash Flows (comma separated: -100, 10, 110)", "irr_res": "Internal Rate of Return (IRR)",
    "npv_r": "Discount Rate (%)", "npv_res": "Net Present Value (NPV)",
    "cm_amt": "Transaction Amount", "cm_day": "Term (Days)", "cm_comm": "Commission", "cm_rate": "Market Rate (%)",
    "cm_cost": "Total Cost", "cm_eff": "Effective Annual Rate",
    "bd_nom": "Nominal Value", "bd_price": "Price", "bd_res": "Simple Yield", "bd_comp": "Compound Yield"
}

# (Diğer diller yer kaplamasın diye TR/EN yeterli şimdilik, mantık aynı)
LANGS = {"TR": TR, "EN": EN, "FR": TR, "DE": TR} # FR/DE için TR yedeği atandı hata vermesin diye

# --- 4. SİSTEM FONKSİYONLARI ---
if 'lang' not in st.session_state: st.session_state.lang = "TR"
if 'page' not in st.session_state: st.session_state.page = "home"

def T(k): return LANGS[st.session_state.lang].get(k, k)
def go(p): st.session_state.page = p; st.rerun()

# --- 5. ÜST BAR ---
c1, c2 = st.columns([3, 1.5])
with c1: st.caption("Eczacıbaşı & Sanofi Project v3.0")
with c2:
    sel = st.selectbox("", ["🇹🇷 TR", "🇬🇧 EN", "🇫🇷 FR", "🇩🇪 DE"], key="l_sel", label_visibility="collapsed")
    st.session_state.lang = sel.split(" ")[1]
st.divider()

# ==========================================
# SAYFA: ANA MENÜ (9 KUTU)
# ==========================================
if st.session_state.page == "home":
    st.title(T("welcome"))
    st.write(f"*{T('sub')}*")
    st.write("")
    
    # 3 Sütunlu Grid Yapısı (9 Buton için)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"{T('m_euro')}\n➡️", use_container_width=True): go("euro")
        if st.button(f"{T('m_inv')}\n➡️", use_container_width=True): go("inv")
        if st.button(f"{T('m_tvm2')}\n➡️", use_container_width=True): go("tvm2")
        
    with col2:
        if st.button(f"{T('m_cred')}\n➡️", use_container_width=True): go("cred")
        if st.button(f"{T('m_rat')}\n➡️", use_container_width=True): go("rat")
        if st.button(f"{T('m_com')}\n➡️", use_container_width=True): go("com")
        
    with col3:
        if st.button(f"{T('m_depo')}\n➡️", use_container_width=True): go("depo")
        if st.button(f"{T('m_tvm1')}\n➡️", use_container_width=True): go("tvm1")
        if st.button(f"{T('m_bond')}\n➡️", use_container_width=True): go("bond")

# ==========================================
# MODÜL 1: EUROBOND
# ==========================================
elif st.session_state.page == "euro":
    if st.button(T("back")): go("home")
    st.subheader(T("m_euro"))
    inc = st.number_input(T("eb_inc"), value=6000.0)
    rate = st.number_input(T("eb_rate"), value=34.5)
    if st.button(T("calc"), type="primary", use_container_width=True):
        res = inc * rate
        lim = 150000
        st.metric(T("eb_res"), f"{res:,.2f} ₺")
        if res > lim: st.error(T("eb_warn").format(lim=f"{lim:,}"))
        else: st.success(T("eb_ok").format(lim=f"{lim:,}"))

# ==========================================
# MODÜL 2: KREDİ
# ==========================================
elif st.session_state.page == "cred":
    if st.button(T("back")): go("home")
    st.subheader(T("m_cred"))
    amt = st.number_input(T("cr_amt"), value=100000.0)
    rate = st.number_input(T("cr_rate"), value=3.5)
    term = st.number_input(T("cr_term"), value=12)
    if st.button(T("calc"), type="primary", use_container_width=True):
        i = rate/100
        if i==0: pmt=amt/term
        else: pmt=amt*(i*(1+i)**term)/((1+i)**term-1)
        c1, c2 = st.columns(2)
        c1.metric(T("cr_res"), f"{pmt:,.2f} ₺")
        c2.metric(T("cr_tot"), f"{pmt*term:,.2f} ₺")

# ==========================================
# MODÜL 3: MEVDUAT
# ==========================================
elif st.session_state.page == "depo":
    if st.button(T("back")): go("home")
    st.subheader(T("m_depo"))
    amt = st.number_input(T("dp_amt"), value=100000.0)
    rate = st.number_input(T("dp_rate"), value=45.0)
    days = st.number_input(T("dp_day"), value=32)
    stop = st.number_input(T("dp_stop"), value=5.0)
    if st.button(T("calc"), type="primary", use_container_width=True):
        gross = (amt*rate*days)/36500
        net = gross*(1-stop/100)
        st.metric(T("dp_net"), f"{net:,.2f} ₺")

# ==========================================
# MODÜL 4: YATIRIM GETİRİSİ
# ==========================================
elif st.session_state.page == "inv":
    if st.button(T("back")): go("home")
    st.subheader(T("m_inv"))
    buy = st.number_input(T("in_buy"), value=100.0)
    sell = st.number_input(T("in_sell"), value=120.0)
    days = st.number_input(T("in_day"), value=90)
    if st.button(T("calc"), type="primary", use_container_width=True):
        simp = (sell-buy)/buy
        ann = (1+simp)**(365/days)-1 if days>0 else 0
        c1, c2 = st.columns(2)
        c1.metric(T("in_sim"), f"%{simp*100:.2f}")
        c2.metric(T("in_ann"), f"%{ann*100:.2f}")

# ==========================================
# MODÜL 5: FİNANSAL ORANLAR
# ==========================================
elif st.session_state.page == "rat":
    if st.button(T("back")): go("home")
    st.subheader(T("m_rat"))
    pv = st.number_input(T("rt_pv"), value=1000.0)
    r = st.number_input(T("rt_r"), value=5.0)
    n = st.number_input(T("rt_n"), value=10)
    typ = st.radio(T("rt_type"), [T("rt_simp"), T("rt_comp")])
    if st.button(T("calc"), type="primary", use_container_width=True):
        if typ == T("rt_simp"): fv = pv*(1 + (r/100)*n)
        else: fv = pv*((1 + r/100)**n)
        st.metric(T("rt_fv"), f"{fv:,.2f}")

# ==========================================
# MODÜL 6: TVM 1 (FV/PV)
# ==========================================
elif st.session_state.page == "tvm1":
    if st.button(T("back")): go("home")
    st.subheader(T("m_tvm1"))
    mode = st.radio("Mod", ["PV -> FV", "FV -> PV"])
    val = st.number_input(T("tvm_val"), value=1000.0)
    r = st.number_input(T("tvm_r"), value=3.0)
    n = st.number_input(T("tvm_n"), value=12)
    if st.button(T("calc"), type="primary", use_container_width=True):
        if "PV -> FV" in mode:
            res = val * ((1 + r/100)**n)
            lbl = T("tvm_fv")
        else:
            res = val / ((1 + r/100)**n)
            lbl = T("tvm_pv")
        st.metric(lbl, f"{res:,.2f}")

# ==========================================
# MODÜL 7: TVM 2 (IRR/NPV)
# ==========================================
elif st.session_state.page == "tvm2":
    if st.button(T("back")): go("home")
    st.subheader(T("m_tvm2"))
    cf_str = st.text_input(T("irr_cf"), "-1000, 200, 300, 400, 500")
    disc = st.number_input(T("npv_r"), value=10.0)
    if st.button(T("calc"), type="primary", use_container_width=True):
        try:
            cfs = [float(x) for x in cf_str.split(",")]
            irr = npf.irr(cfs)
            npv = npf.npv(disc/100, cfs)
            c1, c2 = st.columns(2)
            c1.metric(T("irr_res"), f"%{irr*100:.2f}" if irr else "Hata")
            c2.metric(T("npv_res"), f"{npv:,.2f}")
        except: st.error("Format hatası! Örn: -100, 50, 60")

# ==========================================
# MODÜL 8: KOMİSYON
# ==========================================
elif st.session_state.page == "com":
    if st.button(T("back")): go("home")
    st.subheader(T("m_com"))
    amt = st.number_input(T("cm_amt"), value=50000.0)
    comm = st.number_input(T("cm_comm"), value=250.0)
    days = st.number_input(T("cm_day"), value=30)
    if st.button(T("calc"), type="primary", use_container_width=True):
        total = amt + comm
        eff = (comm/amt)*(365/days)*100
        c1, c2 = st.columns(2)
        c1.metric(T("cm_cost"), f"{total:,.2f}")
        c2.metric(T("cm_eff"), f"%{eff:.2f}")

# ==========================================
# MODÜL 9: BONO / TAHVİL
# ==========================================
elif st.session_state.page == "bond":
    if st.button(T("back")): go("home")
    st.subheader(T("m_bond"))
    nom = st.number_input(T("bd_nom"), value=100.0)
    price = st.number_input(T("bd_price"), value=92.0)
    days = st.number_input(T("in_day"), value=180) # Yatırım'dan label al
    if st.button(T("calc"), type="primary", use_container_width=True):
        simp = ((nom-price)/price)*(365/days)*100
        comp = (((nom/price)**(365/days))-1)*100
        c1, c2 = st.columns(2)
        c1.metric(T("bd_res"), f"%{simp:.2f}")
        c2.metric(T("bd_comp"), f"%{comp:.2f}")
