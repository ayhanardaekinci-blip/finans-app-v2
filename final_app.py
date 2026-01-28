import streamlit as st
import pandas as pd
import numpy as np

# =========================================================
# 1) AYARLAR
# =========================================================
st.set_page_config(
    page_title="Finansal Hesap Makinesi",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 2) DİL SÖZLÜKLERİ (TR/EN/FR/DE TAM)
# =========================================================
TR = {
    "app_name": "Finansal Hesap Makinesi",
    "subheader": "Eczacıbaşı Sağlık Hazine Departmanı",
    "home": "🏠 Ana Menü",
    "mode_toggle": "🌙 Gece Modu",

    "m_invest": "Yatırım Getiri Oranı",
    "m_rates": "Basit - Bileşik Faiz",
    "m_single": "Tek Dönemlik Faiz",
    "m_comp": "Bileşik Faizle Para",
    "m_install": "Kredi / Taksit Hesapla",
    "m_table": "Ödeme Tablosu Oluştur",
    "m_disc": "⚡ İskontolu Alacak Hesapla",
    "m_deposit": "🏦 Mevduat Getirisi (Stopajlı)",
    "m_npv": "📉 NPV (Net Bugünkü Değer)",

    "calc": "HESAPLA", "days_365": "Baz Gün (365/360)", "tax": "Vergi Oranı (%)",
    "cr_type": "Ödeme Planı Türü",
    "cr_opt1": "Eşit Taksitli (Standart)",
    "cr_opt2": "Eşit Anaparalı (Azalan)",
    "kkdf": "KKDF (%)",
    "bsmv": "BSMV (%)",

    "inv_buy": "Alış Tutarı", "inv_sell": "Satış Tutarı", "inv_day": "Vade (Gün)",
    "rt_what": "Ne Hesaplayalım?", "rt_days": "Gün Sayısı", "rt_base": "Baz Oran (%)",
    "s_p": "Anapara", "s_r": "Yıllık Faiz (%)", "s_d": "Vade (Gün)", "s_note": "Mevduat (-), Kredi (+)",
    "cm_what": "Ne Hesaplanacak?", "cm_val1": "Anapara (PV)", "cm_val2": "Vade Sonu (FV)", "cm_n": "Dönem Sayısı", "cm_r": "Dönemsel Faiz (%)",
    "pmt_loan": "Kredi Tutarı", "pmt_r": "Aylık Faiz (%)", "pmt_n": "Taksit Sayısı",
    "dc_rec": "Fatura/Alacak Tutarı", "dc_day": "Erken Ödeme Günü", "dc_rate": "Alternatif Getiri (%)",
    "dep_amt": "Yatırılan Tutar (Mevduat)", "dep_days": "Vade (Gün)", "dep_rate": "Yıllık Faiz Oranı (%)",

    "inv_r1": "Dönemsel Getiri", "inv_r2": "Yıllık Basit Getiri", "inv_r3": "Yıllık Bileşik Getiri",
    "rt_res": "Hesaplanan Oran",
    "s_r1": "Faiz Tutarı", "s_r2": "Vade Sonu Toplam",
    "cm_lbl_res": "Hesaplanan Tutar", "cm_res_diff": "Faiz Farkı",
    "pmt_res": "İlk Taksit Tutarı", "pmt_res_total": "Toplam Geri Ödeme",
    "dc_r1": "Ele Geçecek Tutar", "dc_r2": "Yapılan İskonto (İndirim)",
    "dep_res_net": "Net Getiri (Ele Geçen)", "dep_res_total": "Vade Sonu Toplam Bakiye",
    "dep_info_stopaj": "Uygulanan Stopaj Oranı",
    "dep_info_desc": "ℹ️ 2025 Düzenlemesine göre vadeye bağlı otomatik stopaj uygulanmıştır.",

    "tbl_cols": ["Dönem", "Taksit", "Anapara", "Faiz", "KKDF", "BSMV", "Kalan Borç"],
    "opt_comp_rate": "Yıllık Bileşik Faiz (%)", "opt_simp_rate": "Yıllık Basit Faiz (%)",
    "opt_pv": "Anapara (PV)", "opt_fv": "Vade Sonu Değer (FV)",

    # NPV
    "npv_c0": "Başlangıç Yatırımı (CF0)",
    "npv_rate": "İskonto Oranı (%)",
    "npv_n": "Dönem Sayısı (N)",
    "npv_cf": "Nakit Akışı (CF)",
    "npv_res": "NPV (Net Bugünkü Değer)",
    "npv_pv_sum": "Gelecek Akışlar PV Toplamı",
    "npv_hint": "ℹ️ CF0 genelde negatiftir (yatırım). CF1..CFN nakit giriş/çıkışlarıdır."
}

EN = {
    "app_name": "Financial Calculator",
    "subheader": "Eczacıbaşı Healthcare Treasury Dept.",
    "home": "🏠 Home",
    "mode_toggle": "🌙 Dark Mode",

    "m_invest": "Investment ROI",
    "m_rates": "Simple vs Compound Rates",
    "m_single": "Single Period Interest",
    "m_comp": "TVM Calculations",
    "m_install": "Loan / Installment Calc",
    "m_table": "Amortization Schedule",
    "m_disc": "⚡ Discounted Receivables",
    "m_deposit": "🏦 Deposit Return (Withholding)",
    "m_npv": "📉 NPV (Net Present Value)",

    "calc": "CALCULATE", "days_365": "Day Count Basis (365/360)", "tax": "Tax / Withholding (%)",
    "cr_type": "Repayment Plan Type",
    "cr_opt1": "Equal Installments (Annuity)",
    "cr_opt2": "Equal Principal (Decreasing)",
    "kkdf": "Tax 1 (KKDF) (%)",
    "bsmv": "Tax 2 (BSMV) (%)",

    "inv_buy": "Purchase Price", "inv_sell": "Selling Price", "inv_day": "Tenor (Days)",
    "rt_what": "Calculate What?", "rt_days": "Days", "rt_base": "Base Rate (%)",
    "s_p": "Principal Amount", "s_r": "Annual Rate (%)", "s_d": "Tenor (Days)", "s_note": "Deposit (-), Loan (+)",
    "cm_what": "Calculate What?", "cm_val1": "Present Value (PV)", "cm_val2": "Future Value (FV)", "cm_n": "Number of Periods", "cm_r": "Periodic Rate (%)",
    "pmt_loan": "Loan Amount", "pmt_r": "Monthly Rate (%)", "pmt_n": "Installments",
    "dc_rec": "Receivable Amount", "dc_day": "Days Paid Early", "dc_rate": "Opportunity Cost (%)",
    "dep_amt": "Deposit Amount", "dep_days": "Maturity (Days)", "dep_rate": "Annual Interest Rate (%)",

    "inv_r1": "Periodic Return", "inv_r2": "Annual Simple Return", "inv_r3": "Annual Compound Return",
    "rt_res": "Resulting Rate",
    "s_r1": "Interest Amount", "s_r2": "Total Maturity Value",
    "cm_lbl_res": "Calculated Amount", "cm_res_diff": "Interest Component",
    "pmt_res": "First Installment", "pmt_res_total": "Total Repayment",
    "dc_r1": "Net Payable Amount", "dc_r2": "Discount Amount",
    "dep_res_net": "Net Return", "dep_res_total": "Total Ending Balance",
    "dep_info_stopaj": "Applied Withholding Tax",
    "dep_info_desc": "ℹ️ Withholding tax applied automatically based on 2025 regulation.",

    "tbl_cols": ["Period", "Payment", "Principal", "Interest", "Tax 1", "Tax 2", "Balance"],
    "opt_comp_rate": "Annual Compound Rate (%)", "opt_simp_rate": "Annual Simple Rate (%)",
    "opt_pv": "Principal (PV)", "opt_fv": "Future Value (FV)",

    # NPV
    "npv_c0": "Initial Investment (CF0)",
    "npv_rate": "Discount Rate (%)",
    "npv_n": "Number of Periods (N)",
    "npv_cf": "Cash Flow (CF)",
    "npv_res": "NPV (Net Present Value)",
    "npv_pv_sum": "PV Sum of Future Flows",
    "npv_hint": "ℹ️ CF0 is usually negative. CF1..CFN are inflows/outflows."
}

FR = {
    "app_name": "Calculatrice Financière",
    "subheader": "Dépt. Trésorerie Santé Eczacıbaşı",
    "home": "🏠 Menu Principal",
    "mode_toggle": "🌙 Mode Sombre",

    "m_invest": "ROI Investissement",
    "m_rates": "Taux Simples vs Composés",
    "m_single": "Intérêt Période Unique",
    "m_comp": "Calculs TVM (VA/VC)",
    "m_install": "Calcul de Prêt",
    "m_table": "Tableau d'Amortissement",
    "m_disc": "⚡ Créances Escomptées",
    "m_deposit": "🏦 Rendement Dépôt (Net)",
    "m_npv": "📉 VAN (Valeur Actuelle Nette)",

    "calc": "CALCULER", "days_365": "Base Jours (365/360)", "tax": "Taxe / Retenue (%)",
    "cr_type": "Type d'Amortissement",
    "cr_opt1": "Mensualités Constantes",
    "cr_opt2": "Amortissement Constant",
    "kkdf": "Taxe 1 (KKDF) (%)",
    "bsmv": "Taxe 2 (BSMV) (%)",

    "inv_buy": "Prix d'Achat", "inv_sell": "Prix de Vente", "inv_day": "Durée (Jours)",
    "rt_what": "Que Calculer?", "rt_days": "Jours", "rt_base": "Taux de Base (%)",
    "s_p": "Principal", "s_r": "Taux Annuel (%)", "s_d": "Durée (Jours)", "s_note": "Dépôt (-), Prêt (+)",
    "cm_what": "Que Calculer?", "cm_val1": "Valeur Actuelle (VA)", "cm_val2": "Valeur Future (VC)", "cm_n": "Périodes", "cm_r": "Taux Périodique (%)",
    "pmt_loan": "Montant du Prêt", "pmt_r": "Taux Mensuel (%)", "pmt_n": "Échéances",
    "dc_rec": "Montant Créance", "dc_day": "Jours Anticipés", "dc_rate": "Taux d'Opportunité (%)",
    "dep_amt": "Montant du Dépôt", "dep_days": "Maturité (Jours)", "dep_rate": "Taux Annuel (%)",

    "inv_r1": "Rendement Périodique", "inv_r2": "Rendement Annuel Simple", "inv_r3": "Rendement Annuel Composé",
    "rt_res": "Taux Résultant",
    "s_r1": "Montant des Intérêts", "s_r2": "Valeur Totale",
    "cm_lbl_res": "Montant Calculé", "cm_res_diff": "Part Intérêts",
    "pmt_res": "Première Échéance", "pmt_res_total": "Remboursement Total",
    "dc_r1": "Net à Payer", "dc_r2": "Montant de l'Escompte",
    "dep_res_net": "Rendement Net", "dep_res_total": "Solde Final Total",
    "dep_info_stopaj": "Taxe Appliquée (Retenue)",
    "dep_info_desc": "ℹ️ Taxe appliquée automatiquement selon la régulation 2025.",

    "tbl_cols": ["Période", "Paiement", "Principal", "Intérêts", "Taxe 1", "Taxe 2", "Solde Restant"],
    "opt_comp_rate": "Taux Annuel Composé (%)", "opt_simp_rate": "Taux Annuel Simple (%)",
    "opt_pv": "Valeur Actuelle (VA)", "opt_fv": "Valeur Future (VC)",

    "npv_c0": "Investissement Initial (CF0)",
    "npv_rate": "Taux d'Actualisation (%)",
    "npv_n": "Nombre de Périodes (N)",
    "npv_cf": "Flux de Trésorerie (CF)",
    "npv_res": "VAN (Valeur Actuelle Nette)",
    "npv_pv_sum": "Somme VA des Flux Futurs",
    "npv_hint": "ℹ️ CF0 est généralement négatif. CF1..CFN sont des entrées/sorties."
}

DE = {
    "app_name": "Finanzrechner",
    "subheader": "Eczacıbaşı Gesundheits-Schatzamt",
    "home": "🏠 Hauptmenü",
    "mode_toggle": "🌙 Dunkelmodus",

    "m_invest": "Investitions-ROI",
    "m_rates": "Einfache vs Zinseszinsen",
    "m_single": "Einmalige Zinszahlung",
    "m_comp": "Zeitwert des Geldes",
    "m_install": "Kreditrechner",
    "m_table": "Tilgungsplan Erstellen",
    "m_disc": "⚡ Forderungsdiskontierung",
    "m_deposit": "🏦 Einlagerendite (Netto)",
    "m_npv": "📉 NPV (Kapitalwert)",

    "calc": "BERECHNEN", "days_365": "Zinstage (365/360)", "tax": "Steuersatz (%)",
    "cr_type": "Tilgungsart",
    "cr_opt1": "Gleiche Raten (Annuität)",
    "cr_opt2": "Gleiche Tilgung (Ratentilgung)",
    "kkdf": "Steuer 1 (KKDF) (%)",
    "bsmv": "Steuer 2 (BSMV) (%)",

    "inv_buy": "Kaufpreis", "inv_sell": "Verkaufspreis", "inv_day": "Laufzeit (Tage)",
    "rt_what": "Was berechnen?", "rt_days": "Tage", "rt_base": "Basiszinssatz (%)",
    "s_p": "Kapitalbetrag", "s_r": "Jahreszins (%)", "s_d": "Laufzeit (Tage)", "s_note": "Einlage (-), Kredit (+)",
    "cm_what": "Was berechnen?", "cm_val1": "Barwert (PV)", "cm_val2": "Endwert (FV)", "cm_n": "Anzahl Perioden", "cm_r": "Periodischer Zins (%)",
    "pmt_loan": "Kreditbetrag", "pmt_r": "Monatszins (%)", "pmt_n": "Ratenanzahl",
    "dc_rec": "Forderungsbetrag", "dc_day": "Tage früher", "dc_rate": "Alternativzins (%)",
    "dep_amt": "Einlagebetrag", "dep_days": "Laufzeit (Tage)", "dep_rate": "Jahreszins (%)",

    "inv_r1": "Periodenrendite", "inv_r2": "Jährliche Einfache Rendite", "inv_r3": "Jährliche Effektivrendite",
    "rt_res": "Ergebniszinssatz",
    "s_r1": "Zinsbetrag", "s_r2": "Gesamtendwert",
    "cm_lbl_res": "Berechneter Betrag", "cm_res_diff": "Zinsanteil",
    "pmt_res": "Erste Rate", "pmt_res_total": "Gesamtrückzahlung",
    "dc_r1": "Auszahlungsbetrag", "dc_r2": "Skontobetrag",
    "dep_res_net": "Nettoertrag", "dep_res_total": "Gesamtendbestand",
    "dep_info_stopaj": "Angewandte Steuer",
    "dep_info_desc": "ℹ️ Steuer automatisch nach Vorschrift 2025 angewendet.",

    "tbl_cols": ["Periode", "Rate", "Tilgung", "Zins", "Steuer 1", "Steuer 2", "Restschuld"],
    "opt_comp_rate": "Effektivzinssatz (%)", "opt_simp_rate": "Nominalzinssatz (%)",
    "opt_pv": "Barwert (PV)", "opt_fv": "Endwert (FV)",

    "npv_c0": "Anfangsinvestition (CF0)",
    "npv_rate": "Abzinsungssatz (%)",
    "npv_n": "Anzahl Perioden (N)",
    "npv_cf": "Cashflow (CF)",
    "npv_res": "NPV (Kapitalwert)",
    "npv_pv_sum": "Barwertsumme der zukünftigen Flüsse",
    "npv_hint": "ℹ️ CF0 ist meist negativ. CF1..CFN sind Ein-/Auszahlungen."
}

LANGS = {"TR": TR, "EN": EN, "FR": FR, "DE": DE}

# =========================================================
# 3) FONKSİYONLAR
# =========================================================
def fmt(value):
    if value is None:
        return "0,00"
    try:
        s = "{:,.2f}".format(float(value))
        return s.replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "0,00"

def update_lang():
    st.session_state.lang = st.session_state.l_sel.split(" ")[1]
    st.rerun()  # dil değişince sayfadaki tüm label'lar anında yenilensin

def T(k):
    return LANGS[st.session_state.lang].get(k, k)

def go(p):
    st.session_state.page = p
    st.rerun()

# =========================================================
# 4) SESSION STATE
# =========================================================
if "lang" not in st.session_state: st.session_state.lang = "TR"
if "page" not in st.session_state: st.session_state.page = "home"
if "dark_mode_toggle" not in st.session_state: st.session_state.dark_mode_toggle = False
if "l_sel" not in st.session_state: st.session_state.l_sel = "🇹🇷 TR"

is_dark = st.session_state.dark_mode_toggle

# =========================================================
# 5) TEMA RENKLERİ
# =========================================================
if is_dark:
    bg_color = "#0e1117"
    topbar_bg = "#0e1117"
    card_bg = "#262730"
    input_bg = "#1b1d24"
    text_color = "#ffffff"
    input_text = "#ffffff"
    border_color = "#495057"
    metric_color = "#4dabf7"
else:
    bg_color = "#ffffff"
    topbar_bg = "#ffffff"
    card_bg = "#f8f9fa"
    input_bg = "#ffffff"
    text_color = "#000000"
    input_text = "#000000"
    border_color = "#dee2e6"
    metric_color = "#0d25cf"

# Home'da scroll olmasın: (sticky bozulmasın diye sadece home'da body overflow kapatıyoruz)
no_scroll_css = ""
if st.session_state.page == "home":
    no_scroll_css = "html, body { overflow: hidden !important; }"

# Streamlit Cloud üst header offset
APP_HEADER_OFFSET_PX = 62

# =========================================================
# 6) CSS (1) Dark mode toggle tik/knob görünürlüğü FIX
#            (2) Sticky geri geldi
#            (3) Home tek ekrana sığsın diye boşlukları sıkıştır
# =========================================================
st.markdown(
    f"""
<style>
{no_scroll_css}

/* Genel */
.stApp {{
    background-color: {bg_color};
    color: {text_color};
}}
/* Home tek sayfaya sığsın: paddingleri azalt */
.block-container {{
    padding-top: 0.35rem;
    padding-bottom: 0.55rem;
    max-width: 1200px;
}}
/* Başlık boşluklarını azalt */
h1 {{
    margin-top: 0.05rem !important;
    margin-bottom: 0.20rem !important;
    line-height: 1.03 !important;
}}
/* Divider kompakt */
hr {{
    margin: 0.55rem 0 !important;
}}

/* Kart */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    border: 1px solid {border_color} !important;
    background: {card_bg} !important;
    border-radius: 16px !important;
}}

/* Inputlar */
.stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
    color: {input_text} !important;
    font-weight: 800 !important;
    background-color: {input_bg} !important;
    border: 1px solid {border_color} !important;
    border-radius: 12px !important;
}}

/* Butonlar (home’da daha kısa) */
div.stButton > button:first-child {{
    width: 100%;
    height: 2.78em; /* home tek sayfa */
    border-radius: 14px;
    border: 1px solid {border_color};
    font-weight: 900;
    background: {card_bg};
    color: {text_color};
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    transition: 0.15s;
}}
div.stButton > button:first-child:hover {{
    transform: translateY(-1px);
    border-color: #0d6efd;
    color: #0d6efd;
}}

/* Metric */
div[data-testid="stMetricValue"] {{
    font-size: 1.55rem !important;
    color: {metric_color} !important;
    font-weight: 900 !important;
}}
div[data-testid="stMetricLabel"] {{
    font-size: 0.98rem !important;
    font-weight: 800;
    color: {text_color} !important;
    opacity: 0.95;
}}

/* Selectbox label gizle (üst bar sade) */
div[data-testid="stSelectbox"] label {{ display: none !important; }}

/* ============ STICKY TOPBAR (geri geldi) ============ */
.sticky-topbar {{
    position: sticky;
    top: {APP_HEADER_OFFSET_PX}px;
    z-index: 9999;
    background: {topbar_bg};
    padding: 0.40rem 0.35rem 0.45rem 0.35rem;
    border: 1px solid {border_color};
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    margin-bottom: 0.40rem;
}}
.icon-btn div.stButton > button:first-child {{
    height: 2.45em !important;
    width: 3.00em !important;
    padding: 0 !important;
    border-radius: 14px !important;
    font-size: 1.1rem !important;
}}

/* ============ TOGGLE: “tik/knob” görünmezlik FIX (çok daha sağlam selector seti) ============ */
/* Track */
div[data-testid="stToggle"] [data-baseweb="toggle"] > div {{
    background-color: {"#2b2f36" if is_dark else "#e5e7eb"} !important;
    border: 1px solid {border_color} !important;
    border-radius: 999px !important;
}}
/* Knob (bazı versiyonlarda span, bazılarında div) */
div[data-testid="stToggle"] [data-baseweb="toggle"] span,
div[data-testid="stToggle"] [data-baseweb="toggle"] > div > div {{
    background-color: {"#ffffff" if is_dark else "#111827"} !important;
    border: 1px solid {"#a3a3a3" if is_dark else "#111827"} !important;
}}
/* Knob içi ikon (svg/path) */
div[data-testid="stToggle"] [data-baseweb="toggle"] svg,
div[data-testid="stToggle"] [data-baseweb="toggle"] svg path {{
    fill: {"#111827" if is_dark else "#ffffff"} !important;
}}

/* Home’da başlık sonrası ekstra boşlukları azalt */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {{
    gap: 0.45rem !important;
}}
</style>
""",
    unsafe_allow_html=True
)

# =========================================================
# 7) STICKY ÜST BAR (Home - Mod - Dil)
# =========================================================
st.markdown('<div class="sticky-topbar">', unsafe_allow_html=True)
top_home, top_title, top_mode, top_lang = st.columns([1, 6, 2, 2], vertical_alignment="center")

with top_home:
    st.markdown('<div class="icon-btn">', unsafe_allow_html=True)
    if st.button("🏠", help=T("home"), key="btn_home"):
        go("home")
    st.markdown("</div>", unsafe_allow_html=True)

with top_title:
    st.markdown(
        f"<div style='font-weight:950; font-size:1.03rem; opacity:0.85; padding-left:0.25rem;'>"
        f"{T('app_name')}</div>",
        unsafe_allow_html=True
    )

with top_mode:
    st.toggle(T("mode_toggle"), key="dark_mode_toggle")

with top_lang:
    st.selectbox("Dil / Language", ["🇹🇷 TR", "🇬🇧 EN", "🇫🇷 FR", "🇩🇪 DE"], key="l_sel", on_change=update_lang)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# 8) HOME MENÜ (Info kutusu kaldırıldı → araçlar yukarı)
# =========================================================
if st.session_state.page == "home":
    st.title(T("subheader"))

    with st.container(border=True):
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            if st.button(f"📈 {T('m_invest')}", use_container_width=True): go("invest")
            if st.button(f"🔄 {T('m_rates')}", use_container_width=True): go("rates")
            if st.button(f"📅 {T('m_single')}", use_container_width=True): go("single")
            if st.button(f"💰 {T('m_comp')}", use_container_width=True): go("comp")
            if st.button(f"{T('m_npv')}", use_container_width=True): go("npv")
        with c2:
            if st.button(f"💳 {T('m_install')}", use_container_width=True): go("install")
            if st.button(f"📋 {T('m_table')}", use_container_width=True): go("table")
            if st.button(f"{T('m_deposit')}", use_container_width=True): go("deposit")
            if st.button(f"{T('m_disc')}", use_container_width=True): go("disc")

# =========================================================
# 9) MODÜLLER
# =========================================================
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
                if mode == T("opt_comp_rate"):
                    res = ((1 + r * (days / 365)) ** (365 / days)) - 1
                else:
                    res = (((1 + r) ** (days / 365)) - 1) * (365 / days)
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
            m2.metric(T("s_r2"), f"{fmt(p+net)} ₺")

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
            net_r = (r/100) * (1 - tax/100)
            if target == T("opt_pv"):
                res = val / ((1 + net_r)**n); res_lbl = T("opt_pv")
            else:
                res = val * ((1 + net_r)**n); res_lbl = T("opt_fv")
            m1, m2 = st.columns(2)
            m1.metric(res_lbl, f"{fmt(res)} ₺")
            m2.metric(T("cm_res_diff"), f"{fmt(abs(val-res))} ₺")

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
            if days <= 182: stopaj_rate = 17.5
            elif days <= 365: stopaj_rate = 15.0
            else: stopaj_rate = 10.0

            gross_int = (amount * rate * days) / 36500
            net_int = gross_int * (1 - stopaj_rate/100)
            total_bal = amount + net_int

            c1, c2, c3 = st.columns(3)
            c1.metric(T("dep_info_stopaj"), f"%{stopaj_rate}")
            c2.metric(T("dep_res_net"), f"{fmt(net_int)} ₺")
            c3.metric(T("dep_res_total"), f"{fmt(total_bal)} ₺")

elif st.session_state.page in ["install", "table"]:
    st.title(T("m_install") if st.session_state.page=="install" else T("m_table"))
    st.divider()
    with st.container(border=True):
        plan_type = st.radio(T("cr_type"), [T("cr_opt1"), T("cr_opt2")], horizontal=True, key="cr_plan")
        st.write("")
        c1, c2 = st.columns(2)
        with c1: loan = st.number_input(T("pmt_loan"), value=100000.0, step=1000.0, format="%.2f", key="pmt_loan")
        with c2: rate = st.number_input(T("pmt_r"), value=1.20, format="%.2f", key="pmt_rate")

        c3, c4, c5 = st.columns(3)
        with c3: n = st.number_input(T("pmt_n"), value=12, key="pmt_n")
        with c4: kkdf = st.number_input(T("kkdf"), value=15.0, format="%.2f", key="pmt_kkdf")
        with c5: bsmv = st.number_input(T("bsmv"), value=5.0, format="%.2f", key="pmt_bsmv")

        if st.button(T("calc"), type="primary"):
            if n > 0:
                sch = []; bal = loan; total_pay = 0; first_pmt_display = 0
                gross_rate = (rate/100) * (1 + (kkdf+bsmv)/100)

                if plan_type == T("cr_opt1"):
                    if gross_rate > 0:
                        pmt = loan * (gross_rate * (1+gross_rate)**n) / ((1+gross_rate)**n - 1)
                    else:
                        pmt = loan / n
                    first_pmt_display = pmt
                    for i in range(1, int(n)+1):
                        raw_int = bal * (rate/100)
                        tax_k = raw_int * (kkdf/100); tax_b = raw_int * (bsmv/100)
                        princ = pmt - (raw_int + tax_k + tax_b)
                        bal -= princ; total_pay += pmt
                        sch.append([i, fmt(pmt), fmt(princ), fmt(raw_int), fmt(tax_k), fmt(tax_b), fmt(max(0, bal))])
                else:
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
                pv = receiv / ((1 + r)**(days/365))
                disc_amt = receiv - pv
                m1, m2 = st.columns(2)
                m1.metric(T("dc_r1"), f"{fmt(pv)} ₺")
                m2.metric(T("dc_r2"), f"{fmt(disc_amt)} ₺", delta=f"-{fmt(disc_amt)} ₺")

elif st.session_state.page == "npv":
    st.title(T("m_npv"))
    st.divider()
    st.info(T("npv_hint"))

    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            c0 = st.number_input(T("npv_c0"), value=-100000.0, step=1000.0, format="%.2f", key="npv_c0")
        with c2:
            rate = st.number_input(T("npv_rate"), value=30.0, format="%.2f", key="npv_rate")

        n = st.number_input(T("npv_n"), value=5, min_value=1, step=1, key="npv_n")

        st.write("")
        cf_cols = st.columns(3)
        cash_flows = []
        for i in range(1, int(n) + 1):
            col = cf_cols[(i - 1) % 3]
            with col:
                cf = st.number_input(f"{T('npv_cf')} {i}", value=30000.0, step=1000.0, format="%.2f", key=f"npv_cf_{i}")
                cash_flows.append(cf)

        if st.button(T("calc"), type="primary"):
            r = rate / 100.0
            pv_sum = 0.0
            for t, cf in enumerate(cash_flows, start=1):
                pv_sum += cf / ((1 + r) ** t)
            npv = c0 + pv_sum

            m1, m2 = st.columns(2)
            m1.metric(T("npv_res"), f"{fmt(npv)} ₺")
            m2.metric(T("npv_pv_sum"), f"{fmt(pv_sum)} ₺")
