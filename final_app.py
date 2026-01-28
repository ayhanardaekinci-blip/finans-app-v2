import streamlit as st
import pandas as pd
import math

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
# 2) DİL SÖZLÜKLERİ
#   NOT: Bu sürümde 4 dilde TAM olan kısım:
#        "Investment Evaluation" (NPV/IRR/Payback) modülüdür.
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

    # NEW (Final): CFO-grade Investment Evaluation
    "m_eval": "📉 Yatırım Değerlendirme (NPV • IRR • Payback)",
    "eval_title": "Yatırım Değerlendirme",
    "eval_project": "Proje Adı",
    "eval_ccy": "Para Birimi",
    "eval_wacc": "İskonto Oranı (WACC / Required Return) (%)",
    "eval_n": "Dönem Sayısı (Yıl)",
    "eval_cf0": "Başlangıç Yatırımı (CF0)",
    "eval_cft": "Nakit Akışı (CF)",
    "eval_calc": "HESAPLA",
    "eval_kpi_npv": "NPV (Net Bugünkü Değer)",
    "eval_kpi_irr": "IRR (İç Verim Oranı)",
    "eval_kpi_dpb": "Discounted Payback (Yıl)",
    "eval_kpi_pvsum": "Gelecek Akışlar PV Toplamı",
    "eval_summary_title": "Executive Summary",
    "eval_decision": "Karar",
    "eval_rationale": "Gerekçe",
    "eval_risk_note": "Risk Notu",
    "eval_dec_ok": "Ekonomik olarak uygundur",
    "eval_dec_review": "Şartlı / gözden geçirilmeli",
    "eval_dec_no": "Ekonomik olarak uygun değildir",
    "eval_warn_multi_irr": "Uyarı: Nakit akışında birden fazla işaret değişimi var; IRR birden fazla olabilir.",
    "eval_irr_na": "IRR hesaplanamadı",
    "eval_dpb_na": "Payback oluşmuyor",
    "eval_table_title": "İskontolu Nakit Akışı Tablosu",
    "eval_col_t": "Yıl",
    "eval_col_cf": "CF",
    "eval_col_df": "İskonto Katsayısı",
    "eval_col_pv": "PV(CF)",
    "eval_col_cum": "Kümülatif PV",

    "calc": "HESAPLA",
    "days_365": "Baz Gün (365/360)",
    "tax": "Vergi Oranı (%)",

    "cr_type": "Ödeme Planı Türü",
    "cr_opt1": "Eşit Taksitli (Standart)",
    "cr_opt2": "Eşit Anaparalı (Azalan)",
    "kkdf": "KKDF (%)",
    "bsmv": "BSMV (%)",

    "inv_buy": "Alış Tutarı",
    "inv_sell": "Satış Tutarı",
    "inv_day": "Vade (Gün)",

    "rt_what": "Ne Hesaplayalım?",
    "rt_days": "Gün Sayısı",
    "rt_base": "Baz Oran (%)",
    "opt_comp_rate": "Yıllık Bileşik Faiz (%)",
    "opt_simp_rate": "Yıllık Basit Faiz (%)",
    "rt_res": "Hesaplanan Oran",

    "s_p": "Anapara",
    "s_r": "Yıllık Faiz (%)",
    "s_d": "Vade (Gün)",
    "s_note": "Mevduat (-), Kredi (+)",
    "s_r1": "Faiz Tutarı",
    "s_r2": "Vade Sonu Toplam",

    "cm_what": "Ne Hesaplanacak?",
    "cm_r": "Dönemsel Faiz (%)",
    "cm_n": "Dönem Sayısı",
    "opt_pv": "Anapara (PV)",
    "opt_fv": "Vade Sonu (FV)",
    "cm_res": "Hesaplanan Tutar",
    "cm_res_diff": "Faiz Farkı",

    "pmt_loan": "Kredi Tutarı",
    "pmt_r": "Aylık Faiz (%)",
    "pmt_n": "Taksit Sayısı",
    "pmt_res": "İlk Taksit Tutarı",
    "pmt_res_total": "Toplam Geri Ödeme",

    "dc_rec": "Fatura/Alacak Tutarı",
    "dc_day": "Erken Ödeme Günü",
    "dc_rate": "Alternatif Getiri (%)",
    "dc_r1": "Ele Geçecek Tutar",
    "dc_r2": "Yapılan İskonto (İndirim)",

    "dep_amt": "Yatırılan Tutar (Mevduat)",
    "dep_days": "Vade (Gün)",
    "dep_rate": "Yıllık Faiz Oranı (%)",
    "dep_res_net": "Net Getiri (Ele Geçen)",
    "dep_res_total": "Vade Sonu Toplam Bakiye",
    "dep_info_stopaj": "Uygulanan Stopaj Oranı",
    "dep_info_desc": "ℹ️ 2025 Düzenlemesine göre vadeye bağlı otomatik stopaj uygulanmıştır.",

    "inv_r1": "Dönemsel Getiri",
    "inv_r2": "Yıllık Basit Getiri",
    "inv_r3": "Yıllık Bileşik Getiri",

    "tbl_cols": ["Dönem", "Taksit", "Anapara", "Faiz", "KKDF", "BSMV", "Kalan Borç"],
}

EN = {
    "app_name": "Financial Calculator",
    "subheader": "Eczacıbaşı Healthcare Treasury Dept.",
    "home": "🏠 Home",
    "mode_toggle": "🌙 Dark Mode",

    "m_invest": "Investment ROI",
    "m_rates": "Simple vs Compound",
    "m_single": "Single Period Interest",
    "m_comp": "TVM Calculations",
    "m_install": "Loan / Installment",
    "m_table": "Amortization Schedule",
    "m_disc": "⚡ Discounted Receivables",
    "m_deposit": "🏦 Deposit Return (Withholding)",

    # NEW (Final): CFO-grade Investment Evaluation
    "m_eval": "📉 Investment Evaluation (NPV • IRR • Payback)",
    "eval_title": "Investment Evaluation",
    "eval_project": "Project Name",
    "eval_ccy": "Currency",
    "eval_wacc": "Discount Rate (WACC / Required Return) (%)",
    "eval_n": "Number of Periods (Years)",
    "eval_cf0": "Initial Investment (CF0)",
    "eval_cft": "Cash Flow (CF)",
    "eval_calc": "CALCULATE",
    "eval_kpi_npv": "NPV (Net Present Value)",
    "eval_kpi_irr": "IRR (Internal Rate of Return)",
    "eval_kpi_dpb": "Discounted Payback (Years)",
    "eval_kpi_pvsum": "PV Sum of Future Flows",
    "eval_summary_title": "Executive Summary",
    "eval_decision": "Decision",
    "eval_rationale": "Rationale",
    "eval_risk_note": "Risk Note",
    "eval_dec_ok": "Economically viable",
    "eval_dec_review": "Conditional / requires review",
    "eval_dec_no": "Not economically viable",
    "eval_warn_multi_irr": "Warning: Cash flows have multiple sign changes; multiple IRRs may exist.",
    "eval_irr_na": "IRR not available",
    "eval_dpb_na": "No payback within horizon",
    "eval_table_title": "Discounted Cash Flow Table",
    "eval_col_t": "Year",
    "eval_col_cf": "CF",
    "eval_col_df": "Discount Factor",
    "eval_col_pv": "PV(CF)",
    "eval_col_cum": "Cumulative PV",

    "calc": "CALCULATE",
    "days_365": "Day Count (365/360)",
    "tax": "Tax / Withholding (%)",

    "cr_type": "Repayment Plan Type",
    "cr_opt1": "Equal Installments (Annuity)",
    "cr_opt2": "Equal Principal (Decreasing)",
    "kkdf": "Tax 1 (KKDF) (%)",
    "bsmv": "Tax 2 (BSMV) (%)",

    "inv_buy": "Purchase Price",
    "inv_sell": "Selling Price",
    "inv_day": "Tenor (Days)",

    "rt_what": "Calculate What?",
    "rt_days": "Days",
    "rt_base": "Base Rate (%)",
    "opt_comp_rate": "Annual Compound Rate (%)",
    "opt_simp_rate": "Annual Simple Rate (%)",
    "rt_res": "Resulting Rate",

    "s_p": "Principal Amount",
    "s_r": "Annual Rate (%)",
    "s_d": "Tenor (Days)",
    "s_note": "Deposit (-), Loan (+)",
    "s_r1": "Interest Amount",
    "s_r2": "Total Maturity Value",

    "cm_what": "Calculate What?",
    "cm_r": "Periodic Rate (%)",
    "cm_n": "Number of Periods",
    "opt_pv": "Present Value (PV)",
    "opt_fv": "Future Value (FV)",
    "cm_res": "Calculated Amount",
    "cm_res_diff": "Interest Component",

    "pmt_loan": "Loan Amount",
    "pmt_r": "Monthly Rate (%)",
    "pmt_n": "Installments",
    "pmt_res": "First Installment",
    "pmt_res_total": "Total Repayment",

    "dc_rec": "Receivable Amount",
    "dc_day": "Days Paid Early",
    "dc_rate": "Opportunity Cost (%)",
    "dc_r1": "Net Payable Amount",
    "dc_r2": "Discount Amount",

    "dep_amt": "Deposit Amount",
    "dep_days": "Maturity (Days)",
    "dep_rate": "Annual Interest Rate (%)",
    "dep_res_net": "Net Return",
    "dep_res_total": "Total Ending Balance",
    "dep_info_stopaj": "Applied Withholding Tax",
    "dep_info_desc": "ℹ️ Withholding tax applied automatically based on 2025 regulation.",

    "inv_r1": "Periodic Return",
    "inv_r2": "Annual Simple Return",
    "inv_r3": "Annual Compound Return",

    "tbl_cols": ["Period", "Payment", "Principal", "Interest", "Tax 1", "Tax 2", "Balance"],
}

# FR/DE: genel metinlerde EN fallback; Investment Evaluation kısmı PRO çeviri.
FR = {
    "app_name": "Calculatrice Financière",
    "subheader": "Trésorerie Santé – Eczacıbaşı",
    "home": "🏠 Accueil",
    "mode_toggle": "🌙 Mode Sombre",

    # Menü (EN fallback olsa da sorun değil)
    "m_eval": "📉 Évaluation d’Investissement (VAN • TRI • Payback)",

    # Investment Evaluation (PRO)
    "eval_title": "Évaluation d’Investissement",
    "eval_project": "Nom du Projet",
    "eval_ccy": "Devise",
    "eval_wacc": "Taux d’Actualisation (CMPC / Rendement Exigé) (%)",
    "eval_n": "Nombre de Périodes (Années)",
    "eval_cf0": "Investissement Initial (CF0)",
    "eval_cft": "Flux de Trésorerie (CF)",
    "eval_calc": "CALCULER",
    "eval_kpi_npv": "VAN (Valeur Actuelle Nette)",
    "eval_kpi_irr": "TRI (Taux de Rendement Interne)",
    "eval_kpi_dpb": "Payback Actualisé (Années)",
    "eval_kpi_pvsum": "Somme des Flux Actualisés (PV)",
    "eval_summary_title": "Synthèse Exécutive",
    "eval_decision": "Décision",
    "eval_rationale": "Justification",
    "eval_risk_note": "Note de Risque",
    "eval_dec_ok": "Économiquement viable",
    "eval_dec_review": "Sous conditions / à revoir",
    "eval_dec_no": "Non viable économiquement",
    "eval_warn_multi_irr": "Avertissement : plusieurs changements de signe des flux ; plusieurs TRI possibles.",
    "eval_irr_na": "TRI indisponible",
    "eval_dpb_na": "Payback non atteint sur l’horizon",
    "eval_table_title": "Tableau des Flux Actualisés",
    "eval_col_t": "Année",
    "eval_col_cf": "Flux",
    "eval_col_df": "Facteur d’Actualisation",
    "eval_col_pv": "VA (Flux)",
    "eval_col_cum": "VA Cumulée",

    **{k: v for k, v in EN.items() if k not in {
        "app_name","subheader","home","mode_toggle",
        "m_eval","eval_title","eval_project","eval_ccy","eval_wacc","eval_n","eval_cf0","eval_cft","eval_calc",
        "eval_kpi_npv","eval_kpi_irr","eval_kpi_dpb","eval_kpi_pvsum","eval_summary_title","eval_decision",
        "eval_rationale","eval_risk_note","eval_dec_ok","eval_dec_review","eval_dec_no","eval_warn_multi_irr",
        "eval_irr_na","eval_dpb_na","eval_table_title","eval_col_t","eval_col_cf","eval_col_df","eval_col_pv","eval_col_cum"
    }},
}

DE = {
    "app_name": "Finanzrechner",
    "subheader": "Treasury – Eczacıbaşı Health",
    "home": "🏠 Start",
    "mode_toggle": "🌙 Dunkelmodus",

    "m_eval": "📉 Investitionsbewertung (NPV • IRR • Payback)",

    # Investment Evaluation (PRO)
    "eval_title": "Investitionsbewertung",
    "eval_project": "Projektname",
    "eval_ccy": "Währung",
    "eval_wacc": "Diskontsatz (WACC / Required Return) (%)",
    "eval_n": "Anzahl Perioden (Jahre)",
    "eval_cf0": "Anfangsinvestition (CF0)",
    "eval_cft": "Cashflow (CF)",
    "eval_calc": "BERECHNEN",
    "eval_kpi_npv": "NPV (Kapitalwert)",
    "eval_kpi_irr": "IRR (Interner Zinsfuß)",
    "eval_kpi_dpb": "Abgezinster Payback (Jahre)",
    "eval_kpi_pvsum": "Barwertsumme der zukünftigen Cashflows",
    "eval_summary_title": "Executive Summary",
    "eval_decision": "Entscheidung",
    "eval_rationale": "Begründung",
    "eval_risk_note": "Risikohinweis",
    "eval_dec_ok": "Wirtschaftlich sinnvoll",
    "eval_dec_review": "Bedingt / prüfen",
    "eval_dec_no": "Nicht wirtschaftlich sinnvoll",
    "eval_warn_multi_irr": "Warnung: Mehrere Vorzeichenwechsel der Cashflows; mehrere IRRs möglich.",
    "eval_irr_na": "IRR nicht verfügbar",
    "eval_dpb_na": "Kein Payback im Betrachtungszeitraum",
    "eval_table_title": "Abgezinste Cashflow-Tabelle",
    "eval_col_t": "Jahr",
    "eval_col_cf": "Cashflow",
    "eval_col_df": "Diskontfaktor",
    "eval_col_pv": "Barwert (CF)",
    "eval_col_cum": "Kumul. Barwert",

    **{k: v for k, v in EN.items() if k not in {
        "app_name","subheader","home","mode_toggle",
        "m_eval","eval_title","eval_project","eval_ccy","eval_wacc","eval_n","eval_cf0","eval_cft","eval_calc",
        "eval_kpi_npv","eval_kpi_irr","eval_kpi_dpb","eval_kpi_pvsum","eval_summary_title","eval_decision",
        "eval_rationale","eval_risk_note","eval_dec_ok","eval_dec_review","eval_dec_no","eval_warn_multi_irr",
        "eval_irr_na","eval_dpb_na","eval_table_title","eval_col_t","eval_col_cf","eval_col_df","eval_col_pv","eval_col_cum"
    }},
}

LANGS = {"TR": TR, "EN": EN, "FR": FR, "DE": DE}

# =========================================================
# 3) HELPERS
# =========================================================
def fmt(value):
    if value is None or (isinstance(value, float) and (math.isnan(value) or math.isinf(value))):
        return "0,00"
    try:
        s = "{:,.2f}".format(float(value))
        return s.replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "0,00"

def fmt_pct(value):
    if value is None or (isinstance(value, float) and (math.isnan(value) or math.isinf(value))):
        return "N/A"
    return f"%{fmt(value)}"

def T(key: str) -> str:
    return LANGS[st.session_state.lang].get(key, key)

def sign_changes(seq):
    # count sign changes ignoring zeros
    cleaned = [x for x in seq if abs(x) > 1e-12]
    if len(cleaned) < 2:
        return 0
    changes = 0
    for a, b in zip(cleaned, cleaned[1:]):
        if a * b < 0:
            changes += 1
    return changes

def npv_calc(c0, cfs, r):
    # r as decimal annual
    total = c0
    for t, cf in enumerate(cfs, start=1):
        total += cf / ((1.0 + r) ** t)
    return total

def irr_calc(c0, cfs):
    """
    Robust IRR:
    - find root of NPV(r)=0 with bisection
    - return None if no sign change in search range
    """
    cash = [c0] + list(cfs)
    # Need at least one sign change for IRR existence (common case)
    if sign_changes(cash) == 0:
        return None

    # Lower bound cannot be <= -1
    lo = -0.9999
    hi = 1.0

    f_lo = npv_calc(c0, cfs, lo)
    f_hi = npv_calc(c0, cfs, hi)

    # Expand hi until sign change or limit
    expand = 0
    while f_lo * f_hi > 0 and hi < 10.0 and expand < 40:
        hi *= 1.5
        f_hi = npv_calc(c0, cfs, hi)
        expand += 1

    if f_lo * f_hi > 0:
        return None

    # Bisection
    for _ in range(120):
        mid = (lo + hi) / 2.0
        f_mid = npv_calc(c0, cfs, mid)
        if abs(f_mid) < 1e-9:
            return mid
        if f_lo * f_mid <= 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid

    return (lo + hi) / 2.0

def discounted_payback_years(c0, cfs, r):
    """
    Discounted payback on cumulative PV including CF0.
    Returns float years (e.g., 2.75) or None if never >= 0.
    """
    cum = c0
    if cum >= 0:
        return 0.0

    prev_cum = cum
    for t, cf in enumerate(cfs, start=1):
        pv = cf / ((1.0 + r) ** t)
        cum += pv
        if cum >= 0:
            # interpolate within year t
            denom = (cum - prev_cum)
            if abs(denom) < 1e-12:
                return float(t)
            frac = (0.0 - prev_cum) / denom
            return (t - 1) + max(0.0, min(1.0, frac))
        prev_cum = cum
    return None

# =========================================================
# 4) QUERY PARAM (LANG/DARK/PAGE KALICI)
# =========================================================
def qp_get(key: str, default: str) -> str:
    try:
        v = st.query_params.get(key, None)
        if v is None:
            return default
        if isinstance(v, list):
            return v[0] if v else default
        return str(v)
    except Exception:
        try:
            return st.experimental_get_query_params().get(key, [default])[0]
        except Exception:
            return default

def qp_set(**kwargs):
    try:
        for k, v in kwargs.items():
            st.query_params[k] = v
    except Exception:
        try:
            st.experimental_set_query_params(**kwargs)
        except Exception:
            pass

def go(page: str):
    st.session_state.page = page
    qp_set(page=page)
    st.rerun()

def on_lang_change():
    st.session_state.lang = st.session_state.l_sel.split(" ")[1]
    qp_set(lang=st.session_state.lang)

def on_dark_change():
    qp_set(dark="1" if st.session_state.dark_mode else "0")

# =========================================================
# 5) STATE INIT
# =========================================================
if "page" not in st.session_state:
    st.session_state.page = qp_get("page", "home")

if "lang" not in st.session_state:
    st.session_state.lang = qp_get("lang", "TR")
else:
    st.session_state.lang = qp_get("lang", st.session_state.lang)

dark_from_qp = (qp_get("dark", "0") == "1")
st.session_state.dark_mode = dark_from_qp

flag_map = {"TR": "🇹🇷 TR", "EN": "🇬🇧 EN", "FR": "🇫🇷 FR", "DE": "🇩🇪 DE"}
st.session_state.l_sel = flag_map.get(st.session_state.lang, "🇹🇷 TR")

is_dark = bool(st.session_state.dark_mode)

# =========================================================
# 6) RENKLER
# =========================================================
if is_dark:
    bg_color = "#0e1117"
    card_bg = "#1f2430"
    input_bg = "#121622"
    text_color = "#ffffff"
    muted_text = "#cbd5e1"
    input_text = "#ffffff"
    border_color = "#3b4252"
    metric_color = "#4dabf7"
    shadow = "0.22"
else:
    bg_color = "#ffffff"
    card_bg = "#f6f7fb"
    input_bg = "#ffffff"
    text_color = "#111827"
    muted_text = "#475569"
    input_text = "#111827"
    border_color = "#e5e7eb"
    metric_color = "#0d25cf"
    shadow = "0.10"

STREAMLIT_TOPBAR_PX = 64
TOPBAR_THIN_PADDING_Y = "0.20rem"
TOPBAR_THIN_PADDING_X = "0.55rem"

# =========================================================
# 7) CSS
#   - Tek kontrol: checkbox (native)
#   - Cloud dropdown portal renk fix
# =========================================================
st.markdown(
    f"""
<style>
.stApp {{
  background: {bg_color};
  color: {text_color};
}}
.block-container {{
  padding-top: 0.35rem;
  padding-bottom: 1.0rem;
  max-width: 1240px;
}}

h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {{
  color: {text_color} !important;
  opacity: 1 !important;
}}
.stCaption, small {{
  color: {muted_text} !important;
  opacity: 1 !important;
}}

div[data-testid="stVerticalBlockBorderWrapper"] {{
  background: {card_bg} !important;
  border: 1px solid {border_color} !important;
  border-radius: 14px !important;
}}

div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stRadio"] label,
div[data-testid="stCheckbox"] label {{
  color: {text_color} !important;
  opacity: 1 !important;
  font-weight: 800 !important;
}}
div[data-testid="stRadio"] * {{
  color: {text_color} !important;
  opacity: 1 !important;
}}

.stNumberInput input {{
  color: {input_text} !important;
  background: {input_bg} !important;
  border: 1px solid {border_color} !important;
  border-radius: 12px !important;
  font-weight: 900 !important;
}}

div[data-testid="stSelectbox"] div[data-baseweb="select"] {{
  background: {input_bg} !important;
  border: 1px solid {border_color} !important;
  border-radius: 12px !important;
}}
div[data-testid="stSelectbox"] div[data-baseweb="select"] * {{
  color: {input_text} !important;
  opacity: 1 !important;
}}
div[data-testid="stSelectbox"] div[data-baseweb="select"] svg {{
  fill: {input_text} !important;
  color: {input_text} !important;
}}
div[data-testid="stSelectbox"] div[data-baseweb="select"] input {{
  color: {input_text} !important;
  -webkit-text-fill-color: {input_text} !important;
}}

div[data-baseweb="popover"],
div[data-baseweb="popover"] * {{
  background: {card_bg} !important;
  border-color: {border_color} !important;
}}
div[role="listbox"],
ul[role="listbox"] {{
  background: {card_bg} !important;
  border: 1px solid {border_color} !important;
}}
div[role="option"],
li[role="option"],
div[data-baseweb="menu"] * {{
  color: {text_color} !important;
  opacity: 1 !important;
}}
div[role="option"][aria-selected="true"],
li[role="option"][aria-selected="true"] {{
  background: rgba(13,110,253,0.12) !important;
}}
div[role="option"]:hover,
li[role="option"]:hover {{
  background: rgba(13,110,253,0.10) !important;
}}

div.stButton > button:first-child {{
  width: 100%;
  height: 2.7em;
  border-radius: 12px;
  border: 1px solid {border_color};
  font-weight: 900;
  background: {card_bg};
  color: {text_color};
  box-shadow: 0 3px 12px rgba(0,0,0,{shadow});
  transition: 0.15s;
}}
div.stButton > button:first-child:hover {{
  transform: translateY(-1px);
  border-color: #0d6efd;
  color: #0d6efd;
}}

div[data-testid="stMetricValue"] {{
  font-size: 1.55rem !important;
  color: {metric_color} !important;
  font-weight: 900 !important;
}}
div[data-testid="stMetricLabel"] {{
  font-size: 0.98rem !important;
  font-weight: 800;
  color: {text_color} !important;
  opacity: 1 !important;
}}

div[data-testid="stVerticalBlock"] > div:has(.topbar-marker) {{
  position: sticky;
  top: {STREAMLIT_TOPBAR_PX}px;
  z-index: 999999;
  background: {card_bg};
  border: 1px solid {border_color};
  border-radius: 14px;
  box-shadow: 0 6px 18px rgba(0,0,0,{shadow});
  padding: {TOPBAR_THIN_PADDING_Y} {TOPBAR_THIN_PADDING_X};
  margin-bottom: 0.55rem;
}}
div[data-testid="stVerticalBlock"] > div:has(.topbar-marker) * {{
  color: {text_color} !important;
  opacity: 1 !important;
}}
.topbar-title {{
  font-weight: 950;
  font-size: 1.02rem;
  padding-left: 0.25rem;
}}
.icon-btn div.stButton > button:first-child {{
  height: 2.35em !important;
  width: 2.90em !important;
  padding: 0 !important;
  border-radius: 12px !important;
  font-size: 1.05rem !important;
}}
h1, h2, h3 {{
  scroll-margin-top: calc({STREAMLIT_TOPBAR_PX}px + 72px);
}}
.home-title h1 {{
  margin-top: 0.15rem !important;
  margin-bottom: 0.35rem !important;
  line-height: 1.03 !important;
}}

div[data-testid="stCheckbox"] input[type="checkbox"] {{
  accent-color: #ef4444;
}}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# 8) TOPBAR (STICKY BLOK)
# =========================================================
with st.container():
    st.markdown('<div class="topbar-marker"></div>', unsafe_allow_html=True)

    c_home, c_title, c_switch, c_lang = st.columns([1, 6, 2, 2], vertical_alignment="center")

    with c_home:
        st.markdown('<div class="icon-btn">', unsafe_allow_html=True)
        if st.button("🏠", help=T("home"), key="btn_home"):
            go("home")
        st.markdown("</div>", unsafe_allow_html=True)

    with c_title:
        st.markdown(f"<div class='topbar-title'>{T('subheader')}</div>", unsafe_allow_html=True)

    with c_switch:
        st.checkbox(
            T("mode_toggle"),
            value=st.session_state.dark_mode,
            key="dark_mode",
            on_change=on_dark_change,
        )

    with c_lang:
        st.selectbox(
            "Dil / Language",
            ["🇹🇷 TR", "🇬🇧 EN", "🇫🇷 FR", "🇩🇪 DE"],
            key="l_sel",
            on_change=on_lang_change,
        )

# =========================================================
# 9) HOME
# =========================================================
if st.session_state.page == "home":
    st.markdown("<div class='home-title'>", unsafe_allow_html=True)
    st.title(T("app_name"))
    st.markdown("</div>", unsafe_allow_html=True)

    with st.container(border=True):
        left, right = st.columns(2, gap="medium")

        with left:
            if st.button(f"📈 {T('m_invest')}", use_container_width=True): go("invest")
            if st.button(f"🔄 {T('m_rates')}", use_container_width=True): go("rates")
            if st.button(f"📅 {T('m_single')}", use_container_width=True): go("single")
            if st.button(f"💰 {T('m_comp')}", use_container_width=True): go("comp")
            if st.button(f"{T('m_eval')}", use_container_width=True): go("eval")

        with right:
            if st.button(f"💳 {T('m_install')}", use_container_width=True): go("install")
            if st.button(f"📋 {T('m_table')}", use_container_width=True): go("table")
            if st.button(f"{T('m_deposit')}", use_container_width=True): go("deposit")
            if st.button(f"{T('m_disc')}", use_container_width=True): go("disc")

# =========================================================
# 10) MODÜLLER
# =========================================================
elif st.session_state.page == "eval":
    st.title(T("eval_title"))
    st.divider()

    # ---------- Inputs + Summary layout ----------
    inp_col, sum_col = st.columns([1.15, 1.0], gap="large")

    with inp_col:
        with st.container(border=True):
            project = st.text_input(T("eval_project"), value=st.session_state.get("eval_project_val", "Project A"), key="eval_project_val")
            ccy = st.selectbox(T("eval_ccy"), ["TRY", "USD", "EUR"], index=0, key="eval_ccy_val")

            wacc = st.number_input(T("eval_wacc"), value=float(st.session_state.get("eval_wacc_val", 30.0)), format="%.2f", key="eval_wacc_val")
            n = st.number_input(T("eval_n"), value=int(st.session_state.get("eval_n_val", 5)), min_value=1, step=1, key="eval_n_val")

            st.write("---")
            c0 = st.number_input(T("eval_cf0"), value=float(st.session_state.get("eval_cf0_val", -100000.0)), step=1000.0, format="%.2f", key="eval_cf0_val")

            cols = st.columns(3)
            cfs = []
            for i in range(1, int(n) + 1):
                with cols[(i - 1) % 3]:
                    cf = st.number_input(
                        f"{T('eval_cft')} {i}",
                        value=float(st.session_state.get(f"eval_cf_{i}", 30000.0)),
                        step=1000.0,
                        format="%.2f",
                        key=f"eval_cf_{i}",
                    )
                    cfs.append(cf)

            calc = st.button(T("eval_calc"), type="primary", use_container_width=True)

    # ---------- Computation & Rendering ----------
    if calc:
        r = float(wacc) / 100.0

        cash_all = [c0] + list(cfs)
        multi_irr_risk = (sign_changes(cash_all) > 1)

        npv = npv_calc(c0, cfs, r)
        pv_sum = npv - c0
        irr = irr_calc(c0, cfs)
        dpb = discounted_payback_years(c0, cfs, r)

        # Decision logic (simple, CFO-friendly)
        # - OK: NPV>0 and (IRR exists and IRR>WACC)
        # - NO: NPV<0 and (IRR missing or IRR<WACC)
        # - REVIEW: otherwise (mixed signals)
        ok = (npv > 0) and (irr is not None) and (irr > r)
        no = (npv < 0) and ((irr is None) or (irr < r))
        if ok:
            decision = T("eval_dec_ok")
        elif no:
            decision = T("eval_dec_no")
        else:
            decision = T("eval_dec_review")

        # Rationale & risk note text
        irr_txt = T("eval_irr_na") if irr is None else f"{(irr*100):.2f}%"
        wacc_txt = f"{(r*100):.2f}%"

        if irr is None:
            rationale = f"{T('eval_kpi_npv')} {('pozitiftir' if st.session_state.lang=='TR' else 'is positive' ) if npv>0 else ('negatiftir' if st.session_state.lang=='TR' else 'is negative')}. {T('eval_irr_na')}."
        else:
            # language-neutral sentence pattern; still reads fine
            rationale = f"{T('eval_kpi_npv')}: {fmt(npv)} • {T('eval_kpi_irr')}: {irr_txt} • {T('eval_wacc')}: {wacc_txt}"

        if dpb is None:
            risk_note = T("eval_dpb_na")
        else:
            risk_note = f"{T('eval_kpi_dpb')}: {dpb:.2f}"

        with sum_col:
            # KPI band
            k1, k2, k3 = st.columns(3)
            k1.metric(T("eval_kpi_npv"), f"{fmt(npv)} {ccy}")
            k2.metric(T("eval_kpi_irr"), (T("eval_irr_na") if irr is None else f"%{fmt(irr*100)}"))
            k3.metric(T("eval_kpi_dpb"), (T("eval_dpb_na") if dpb is None else f"{dpb:.2f}"))

            k4, _ = st.columns([1, 1])
            k4.metric(T("eval_kpi_pvsum"), f"{fmt(pv_sum)} {ccy}")

            st.write("")
            with st.container(border=True):
                st.subheader(T("eval_summary_title"))
                st.write(f"**{T('eval_decision')}:** {decision}")
                st.write(f"**{T('eval_rationale')}:** {rationale}")
                st.write(f"**{T('eval_risk_note')}:** {risk_note}")
                if multi_irr_risk:
                    st.warning(T("eval_warn_multi_irr"))

        # Table (full width)
        st.write("")
        st.subheader(T("eval_table_title"))
        rows = []
        cum = c0
        rows.append([0, c0, 1.0, c0, cum])
        for t, cf in enumerate(cfs, start=1):
            df = 1.0 / ((1.0 + r) ** t)
            pv = cf * df
            cum += pv
            rows.append([t, cf, df, pv, cum])

        df_table = pd.DataFrame(
            rows,
            columns=[T("eval_col_t"), T("eval_col_cf"), T("eval_col_df"), T("eval_col_pv"), T("eval_col_cum")],
        )

        # format display
        disp = df_table.copy()
        disp[T("eval_col_cf")] = disp[T("eval_col_cf")].apply(lambda x: f"{fmt(x)} {ccy}")
        disp[T("eval_col_df")] = disp[T("eval_col_df")].apply(lambda x: f"{x:.6f}")
        disp[T("eval_col_pv")] = disp[T("eval_col_pv")].apply(lambda x: f"{fmt(x)} {ccy}")
        disp[T("eval_col_cum")] = disp[T("eval_col_cum")].apply(lambda x: f"{fmt(x)} {ccy}")

        st.dataframe(disp, use_container_width=True, hide_index=True)

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
        with c1:
            mode = st.selectbox(T("rt_what"), [T("opt_comp_rate"), T("opt_simp_rate")], key="rt_mode")
        with c2:
            days = st.number_input(T("rt_days"), value=365, key="rt_days")

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
            m2.metric(T("s_r2"), f"{fmt(p + net)} ₺")

elif st.session_state.page == "comp":
    st.title(T("m_comp"))
    st.divider()
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            target = st.selectbox(T("cm_what"), [T("opt_pv"), T("opt_fv")], key="cm_target")
        with c2:
            lbl = T("opt_fv") if target == T("opt_pv") else T("opt_pv")
            val = st.number_input(lbl, value=0.0, step=1000.0, format="%.2f", key="cm_val")

        c3, c4 = st.columns(2)
        with c3: r = st.number_input(T("cm_r"), value=0.0, format="%.2f", key="cm_r")
        with c4: n = st.number_input(T("cm_n"), value=1, key="cm_n")

        tax = st.number_input(T("tax"), value=0.0, format="%.2f", key="cm_tax")

        if st.button(T("calc"), type="primary"):
            net_r = (r / 100) * (1 - tax / 100)
            if target == T("opt_pv"):
                res = val / ((1 + net_r) ** n)
            else:
                res = val * ((1 + net_r) ** n)

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
            if days <= 182: stopaj_rate = 17.5
            elif days <= 365: stopaj_rate = 15.0
            else: stopaj_rate = 10.0

            gross_int = (amount * rate * days) / 36500
            net_int = gross_int * (1 - stopaj_rate / 100)
            total_bal = amount + net_int

            c1, c2, c3 = st.columns(3)
            c1.metric(T("dep_info_stopaj"), f"%{stopaj_rate}")
            c2.metric(T("dep_res_net"), f"{fmt(net_int)} ₺")
            c3.metric(T("dep_res_total"), f"{fmt(total_bal)} ₺")

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
            if n > 0:
                sch = []
                bal = loan
                total_pay = 0
                first_pmt_display = 0

                gross_rate = (rate / 100) * (1 + (kkdf + bsmv) / 100)

                if plan_type == T("cr_opt1"):
                    if gross_rate > 0:
                        pmt = loan * (gross_rate * (1 + gross_rate) ** n) / ((1 + gross_rate) ** n - 1)
                    else:
                        pmt = loan / n

                    first_pmt_display = pmt
                    for i in range(1, int(n) + 1):
                        raw_int = bal * (rate / 100)
                        tax_k = raw_int * (kkdf / 100)
                        tax_b = raw_int * (bsmv / 100)
                        princ = pmt - (raw_int + tax_k + tax_b)
                        bal -= princ
                        total_pay += pmt
                        sch.append([i, fmt(pmt), fmt(princ), fmt(raw_int), fmt(tax_k), fmt(tax_b), fmt(max(0, bal))])
                else:
                    fixed_princ = loan / n
                    for i in range(1, int(n) + 1):
                        raw_int = bal * (rate / 100)
                        tax_k = raw_int * (kkdf / 100)
                        tax_b = raw_int * (bsmv / 100)
                        curr_pmt = fixed_princ + raw_int + tax_k + tax_b
                        if i == 1:
                            first_pmt_display = curr_pmt
                        bal -= fixed_princ
                        total_pay += curr_pmt
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
                pv = receiv / ((1 + r) ** (days / 365))
                disc_amt = receiv - pv
                m1, m2 = st.columns(2)
                m1.metric(T("dc_r1"), f"{fmt(pv)} ₺")
                m2.metric(T("dc_r2"), f"{fmt(disc_amt)} ₺")

