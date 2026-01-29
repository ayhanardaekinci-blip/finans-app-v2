import streamlit as st
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import io

# =========================================================
# 1) AYARLAR
# =========================================================
st.set_page_config(
    page_title="Finansal Hesap Makinesi",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown("""
<style>
/* Hide Streamlit default UI */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
/* Reduce top padding/margins */
.block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
/* Make widget heights more consistent */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] div[role="combobox"] {
  min-height: 44px;
}
/* Tighten spacing */
div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stExpander"]) {margin-top: 0.25rem;}
/* Make top menu sticky */
div.block-container > div:first-child {
  position: sticky;
  top: 0;
  z-index: 999;
  backdrop-filter: blur(6px);
}
div.block-container > div:first-child > div {
  background: rgba(0,0,0,0.35);
  border-radius: 16px;
  padding: 0.25rem 0.75rem;
}
/* Make top menu sticky (override) */
div.block-container {padding-top: 0.5rem !important;}
div.block-container > div:first-child {
  position: sticky !important;
  top: 0 !important;
  z-index: 9999 !important;
}
div.block-container > div:first-child > div {
  background: #0B1220 !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  box-shadow: 0 10px 30px rgba(0,0,0,0.35) !important;
  border-radius: 16px !important;
  padding: 0.5rem 0.75rem !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2) DİL SÖZLÜKLERİ
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
    "m_npv": "📉 Yatırım Değerlendirme (NPV / IRR / Geri Ödeme)",

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

    # ---- NPV / IRR / PAYBACK (PRO) ----
    "inv_eval_title": "Yatırım Değerlendirme",
    "proj_name": "Proje Adı",
    "currency": "Para Birimi",
    "wacc": "İskonto Oranı (WACC / Required Return) (%)",
    "periods": "Dönem Sayısı (Yıl)",
    "cf0": "Başlangıç Yatırımı (CF0)",
    "cf": "Nakit Akışı (CF)",
    "tab_npv": "NPV",
    "tab_irr": "IRR",
    "tab_payback": "Payback",
    "npv": "NPV (Net Bugünkü Değer)",
    "pv_sum": "Gelecek Akışlar PV Toplamı",
    "irr": "IRR (İç Verim Oranı)",
    "payback": "Geri Ödeme Süresi",
    "payback_disc": "İskontolu Geri Ödeme",
    "payback_never": "Dönem içinde geri ödeme oluşmuyor",
    "breakeven": "Break-even WACC (NPV=0)",
    "scenario": "Senaryo Analizi",
    "base": "Base",
    "best": "Best",
    "worst": "Worst",
    "cf_mult": "Nakit akışı çarpanı",
    "wacc_shift": "WACC kaydırma (puan)",
    "sensitivity": "WACC Duyarlılık (±5 puan)",
    "sens_note": "WACC ±5 puan aralığında NPV'nin nasıl değiştiğini gösterir.",
                "chart": "NPV - WACC Eğrisi",
                "details": "ℹ️ Bilgi",
                "npv_details": (
                "NPV, gelecekte beklenen nakit akışlarının bugünkü değerleri toplamından başlangıç yatırımının çıkarılmasıdır. "
                "NPV>0 ise proje, belirlenen iskonto oranında değer yaratır.\n\n"
                "WACC / Required Return, projenin riskine göre talep edilen minimum getiriyi temsil eder. "
                "Kurumsal karar setlerinde NPV, IRR ve Payback birlikte değerlendirilir."
                ),
                "irr_details": (
                "IRR, NPV'yi sıfıra eşitleyen iskonto oranıdır. IRR, proje getirisini tek bir oranla özetler.\n\n"
                "Dikkat: Nakit akışlarında birden fazla işaret değişimi varsa birden fazla IRR oluşabilir. "
                "Bu uygulama, ekonomik olarak anlamlı kökü arar; raporlama için NPV profili (NPV-WACC eğrisi) ile birlikte yorumlanması önerilir."
                ),
                "payback_details": (
                "Payback, kümülatif nakit akışlarının başlangıç yatırımını hangi dönemde karşıladığını gösterir. "
                "İskontolu Payback ise aynı hesabı WACC ile bugünkü değere indirgenmiş akışlarla yapar.\n\n"
                "Payback likidite riskini özetler; ancak değer yaratmayı NPV kadar iyi temsil etmez. "
                "Bu nedenle CFO seviyesinde Payback mutlaka NPV/IRR ile birlikte değerlendirilmelidir."
                ),
                "scenario_details": (
                "Senaryo analizi, belirsizlik altında karar kalitesini artırır. Tipik kullanım: "
                "Base (en olası), Best (yüksek satış/marj), Worst (talep düşüşü/maliyet artışı).\n\n"
                "Bu modelde senaryolar iki eksen üzerinden yönetilir:\n"
                "1) Nakit akışı çarpanı (operasyonel performans etkisi)\n"
                "2) WACC kaydırma (risk primi / finansman koşulları etkisi)"
                ),
                "sens_details": (
                "WACC duyarlılığı, sermaye maliyeti veya risk primi değiştiğinde yatırımın değerinin ne kadar oynadığını gösterir. "
                "Özellikle volatil piyasalarda (faiz, CDS, ülke risk primi) CFO kararlarında kritik bir göstergedir.\n\n"
                "Break-even WACC, NPV'nin sıfırlandığı eşiği verir: bu oran aşıldığında yatırım değer yaratmaz."
                ),
                }

                EN = {
                "app_name": "Financial Calculator",
                "subheader": "Eczacıbaşı Healthcare Treasury Dept.",
                "home": "🏠 Home",
                "mode_toggle": "🌙 Dark Mode",

                "m_invest": "Investment ROI",
                "m_rates": "Simple - Compound",
                "m_single": "Single Period Interest",
                "m_comp": "Time Value of Money (PV/FV)",
                "m_install": "Loan / Installment",
                "m_table": "Amortization Schedule",
                "m_disc": "⚡ Discounted Receivables",
                "m_deposit": "🏦 Deposit Return (Withholding)",
                "m_npv": "📉 Investment Appraisal (NPV / IRR / Payback)",

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

                # ---- NPV / IRR / PAYBACK (PRO) ----
                "inv_eval_title": "Investment Appraisal",
                "proj_name": "Project Name",
                "currency": "Currency",
                "wacc": "Discount Rate (WACC / Required Return) (%)",
                "periods": "Number of Periods (Years)",
                "cf0": "Initial Investment (CF0)",
                "cf": "Cash Flow (CF)",
                "tab_npv": "NPV",
                "tab_irr": "IRR",
                "tab_payback": "Payback",
                "npv": "NPV (Net Present Value)",
                "pv_sum": "PV Sum of Future Flows",
                "irr": "IRR (Internal Rate of Return)",
                "payback": "Payback Period",
                "payback_disc": "Discounted Payback",
                "payback_never": "No payback within the horizon",
                "breakeven": "Break-even WACC (NPV=0)",
                "scenario": "Scenario Analysis",
                "base": "Base",
                "best": "Best",
                "worst": "Worst",
                "cf_mult": "Cash flow multiplier",
                "wacc_shift": "WACC shift (pp)",
                "sensitivity": "WACC Sensitivity (±5pp)",
                "sens_note": "Shows how NPV changes as WACC moves ±5 percentage points.",
                "chart": "NPV vs WACC Curve",
                "details": "Detailed Notes (CFO Level)",
                "npv_details": (
                "NPV equals the present value of expected future cash flows minus the initial investment. "
                "If NPV>0, the project creates value at the stated discount rate.\n\n"
                "WACC / Required Return represents the minimum return demanded given the project risk. "
                "In corporate decision-making, NPV is typically interpreted together with IRR and Payback."
                ),
                "irr_details": (
                "IRR is the discount rate that sets NPV to zero. It compresses the project economics into a single rate.\n\n"
                "Note: If cash flows change sign more than once, multiple IRRs may exist. "
                "This tool searches for an economically meaningful root; best practice is to interpret IRR alongside the NPV profile (NPV vs WACC)."
                ),
                "payback_details": (
                "Payback indicates when cumulative cash flows recover the initial investment. "
                "Discounted Payback performs the same calculation using cash flows discounted at WACC.\n\n"
                "Payback is useful for liquidity/risk discussions, but it is not a value metric like NPV. "
                "For CFO-level decisions, always evaluate Payback together with NPV/IRR."
                ),
                "scenario_details": (
                "Scenario analysis improves decision quality under uncertainty: Base (most likely), Best (upside), Worst (downside).\n\n"
                "This model manages scenarios across two drivers:\n"
                "1) Cash flow multiplier (operational performance)\n"
                "2) WACC shift (risk premium / funding conditions)"
                ),
                "sens_details": (
                "WACC sensitivity quantifies how valuation changes with capital cost/risk premium movements. "
                "It is critical in volatile markets (rates, spreads, country risk).\n\n"
                "Break-even WACC is the threshold where NPV hits zero: above it, the project stops creating value."
                ),
                }

                FR = {
                "app_name": "Calculateur Financier",
                "subheader": "Département Trésorerie – Eczacıbaşı Santé",
                "home": "🏠 Menu Principal",
                "mode_toggle": "🌙 Mode Sombre",

                "m_invest": "Rendement de l’Investissement",
                "m_rates": "Intérêts Simples et Composés",
                "m_single": "Intérêt sur Période Unique",
                "m_comp": "Valeur Temps de l’Argent (VA / VF)",
                "m_install": "Calcul de Crédit / Échéances",
                "m_table": "Tableau d’Amortissement",
                "m_disc": "⚡ Actualisation des Créances",
                "m_deposit": "🏦 Rendement du Dépôt (Net)",
                "m_npv": "📉 Analyse d’Investissement (VAN / TRI / Payback)",

                "calc": "CALCULER",
                "days_365": "Base de Calcul (365 / 360)",
                "tax": "Taux d’Imposition (%)",

                "cr_type": "Type de Plan de Remboursement",
                "cr_opt1": "Annuités Constantes",
                "cr_opt2": "Amortissement Constant",
                "kkdf": "Taxe KKDF (%)",
                "bsmv": "Taxe BSMV (%)",

                "inv_buy": "Montant d’Achat",
                "inv_sell": "Montant de Vente",
                "inv_day": "Durée (Jours)",

                "rt_what": "Type de Calcul",
                "rt_days": "Nombre de Jours",
                "rt_base": "Taux de Référence (%)",
                "opt_comp_rate": "Taux Annuel Composé (%)",
                "opt_simp_rate": "Taux Annuel Simple (%)",
                "rt_res": "Taux Calculé",

                "s_p": "Capital Initial",
                "s_r": "Taux Annuel (%)",
                "s_d": "Durée (Jours)",
                "s_note": "Dépôt (-), Crédit (+)",
                "s_r1": "Montant des Intérêts",
                "s_r2": "Valeur Totale à Échéance",

                "cm_what": "Valeur à Calculer",
                "cm_r": "Taux Périodique (%)",
                "cm_n": "Nombre de Périodes",
                "opt_pv": "Valeur Actuelle (VA)",
                "opt_fv": "Valeur Future (VF)",
                "cm_res": "Valeur Calculée",
                "cm_res_diff": "Part des Intérêts",

                "pmt_loan": "Montant du Crédit",
                "pmt_r": "Taux Mensuel (%)",
                "pmt_n": "Nombre d’Échéances",
                "pmt_res": "Première Échéance",
                "pmt_res_total": "Remboursement Total",

                "dc_rec": "Montant de la Créance",
                "dc_day": "Paiement Anticipé (Jours)",
                "dc_rate": "Taux de Rendement Alternatif (%)",
                "dc_r1": "Montant Actualisé",
                "dc_r2": "Montant de l’Escompte",

                "dep_amt": "Montant du Dépôt",
                "dep_days": "Durée (Jours)",
                "dep_rate": "Taux Annuel (%)",
                "dep_res_net": "Intérêts Nets",
                "dep_res_total": "Solde Final",
                "dep_info_stopaj": "Taux de Retenue",
                "dep_info_desc": "ℹ️ Retenue appliquée automatiquement selon la réglementation 2025.",

                "inv_r1": "Rendement de la Période",
                "inv_r2": "Rendement Annuel Simple",
                "inv_r3": "Rendement Annuel Composé",

                "tbl_cols": ["Période", "Échéance", "Principal", "Intérêts", "KKDF", "BSMV", "Solde Restant"],

                # ---- NPV / IRR / PAYBACK (PRO) ----
                "inv_eval_title": "Analyse d’Investissement",
                "proj_name": "Nom du Projet",
                "currency": "Devise",
                "wacc": "Taux d’Actualisation (CMPC / Rendement Exigé) (%)",
                "periods": "Nombre de Périodes (Années)",
                "cf0": "Investissement Initial (CF0)",
                "cf": "Flux de Trésorerie (CF)",
                "tab_npv": "VAN",
                "tab_irr": "TRI",
                "tab_payback": "Payback",
                "npv": "VAN (Valeur Actuelle Nette)",
                "pv_sum": "Somme Actualisée des Flux",
                "irr": "TRI (Taux de Rendement Interne)",
                "payback": "Délai de Récupération",
                "payback_disc": "Payback Actualisé",
                "payback_never": "Pas de récupération sur l’horizon",
                "breakeven": "CMPC Seuil (VAN=0)",
                "scenario": "Analyse de Scénarios",
                "base": "Base",
                "best": "Optimiste",
                "worst": "Pessimiste",
                "cf_mult": "Multiplicateur des flux",
                "wacc_shift": "Décalage du CMPC (pts)",
                "sensitivity": "Sensibilité du CMPC (±5 pts)",
                "sens_note": "Montre l’évolution de la VAN lorsque le CMPC varie de ±5 points.",
                "chart": "Courbe VAN vs CMPC",
                "details": "Notes Détaillées (Niveau CFO)",
                "npv_details": (
                "La VAN correspond à la somme des valeurs actuelles des flux futurs moins l’investissement initial. "
                "Si VAN>0, le projet crée de la valeur au taux d’actualisation retenu.\n\n"
                "Le CMPC / rendement exigé représente le minimum attendu compte tenu du risque. "
                "En pratique, VAN, TRI et Payback se lisent ensemble."
                ),
                "irr_details": (
                "Le TRI est le taux qui annule la VAN (VAN=0). Il résume l’économie du projet en un seul taux.\n\n"
                "Attention : plusieurs TRI peuvent exister si les flux changent de signe plusieurs fois. "
                "La lecture recommandée est de compléter avec le profil VAN (VAN vs taux)."
                ),
                "payback_details": (
                "Le Payback indique quand les flux cumulés couvrent l’investissement initial. "
                "Le Payback actualisé applique le CMPC aux flux.\n\n"
                "Le Payback est utile pour la liquidité/risque, mais ce n’est pas une mesure de valeur comme la VAN."
                ),
                "scenario_details": (
                "Les scénarios renforcent la décision sous incertitude : Base, Optimiste, Pessimiste.\n\n"
                "Ici, deux leviers : (1) multiplicateur de flux (performance) (2) décalage du CMPC (prime de risque)."
                ),
                "sens_details": (
                "La sensibilité au CMPC mesure l’impact des mouvements de taux/spreads sur la valeur. "
                "Le CMPC seuil (VAN=0) indique le point à partir duquel le projet ne crée plus de valeur."
                ),
                }

                DE = {
                "app_name": "Finanzrechner",
                "subheader": "Treasury-Abteilung – Eczacıbaşı Gesundheit",
                "home": "🏠 Hauptmenü",
                "mode_toggle": "🌙 Dunkelmodus",

                "m_invest": "Investitionsrendite",
                "m_rates": "Einfache und Zusammengesetzte Zinsen",
                "m_single": "Einperiodige Verzinsung",
                "m_comp": "Zeitwert des Geldes (BW / EW)",
                "m_install": "Kredit- / Ratenberechnung",
                "m_table": "Tilgungsplan",
                "m_disc": "⚡ Forderungsabzinsung",
                "m_deposit": "🏦 Einlagenrendite (Netto)",
                "m_npv": "📉 Investitionsbewertung (NPV / IRR / Payback)",

                "calc": "BERECHNEN",
                "days_365": "Zinstage (365 / 360)",
                "tax": "Steuersatz (%)",

                "cr_type": "Rückzahlungsart",
                "cr_opt1": "Annuitätendarlehen",
                "cr_opt2": "Lineare Tilgung",
                "kkdf": "KKDF-Steuer (%)",
                "bsmv": "BSMV-Steuer (%)",

                "inv_buy": "Kaufbetrag",
                "inv_sell": "Verkaufsbetrag",
                "inv_day": "Laufzeit (Tage)",

                "rt_what": "Berechnungsart",
                "rt_days": "Anzahl der Tage",
                "rt_base": "Referenzzinssatz (%)",
                "opt_comp_rate": "Effektiver Jahreszins (%)",
                "opt_simp_rate": "Nominaler Jahreszins (%)",
                "rt_res": "Berechneter Zinssatz",

                "s_p": "Anfangskapital",
                "s_r": "Jahreszins (%)",
                "s_d": "Laufzeit (Tage)",
                "s_note": "Einlage (-), Kredit (+)",
                "s_r1": "Zinsbetrag",
                "s_r2": "Endbetrag",

                "cm_what": "Zu Berechnender Wert",
                "cm_r": "Periodischer Zinssatz (%)",
                "cm_n": "Anzahl der Perioden",
                "opt_pv": "Barwert (BW)",
                "opt_fv": "Endwert (EW)",
                "cm_res": "Berechneter Betrag",
                "cm_res_diff": "Zinsanteil",

                "pmt_loan": "Kreditbetrag",
                "pmt_r": "Monatlicher Zinssatz (%)",
                "pmt_n": "Anzahl der Raten",
                "pmt_res": "Erste Rate",
                "pmt_res_total": "Gesamtrückzahlung",

                "dc_rec": "Forderungsbetrag",
                "dc_day": "Vorzeitige Zahlung (Tage)",
                "dc_rate": "Alternativer Zinssatz (%)",
                "dc_r1": "Abgezinster Betrag",
                "dc_r2": "Abzinsungsbetrag",

                "dep_amt": "Einlagebetrag",
                "dep_days": "Laufzeit (Tage)",
                "dep_rate": "Jahreszinssatz (%)",
                "dep_res_net": "Nettozinsertrag",
                "dep_res_total": "Endsaldo",
                "dep_info_stopaj": "Quellensteuersatz",
                "dep_info_desc": "ℹ️ Automatische Besteuerung gemäß Regelung 2025.",

                "inv_r1": "Periodenrendite",
                "inv_r2": "Einfache Jahresrendite",
                "inv_r3": "Effektive Jahresrendite",

                "tbl_cols": ["Periode", "Rate", "Tilgung", "Zinsen", "KKDF", "BSMV", "Restschuld"],

                # ---- NPV / IRR / PAYBACK (PRO) ----
                "inv_eval_title": "Investitionsbewertung",
                "proj_name": "Projektname",
                "currency": "Währung",
                "wacc": "Diskontsatz (WACC / Mindestrendite) (%)",
                "periods": "Anzahl der Perioden (Jahre)",
                "cf0": "Anfangsinvestition (CF0)",
                "cf": "Cashflow (CF)",
                "tab_npv": "NPV",
                "tab_irr": "IRR",
                "tab_payback": "Payback",
                "npv": "Kapitalwert (NPV)",
                "pv_sum": "Barwertsumme der Zahlungsströme",
                "irr": "IRR (Interner Zinsfuß)",
                "payback": "Amortisationsdauer",
                "payback_disc": "Abgezinste Amortisation",
                "payback_never": "Keine Amortisation im Horizont",
                "breakeven": "Break-even WACC (NPV=0)",
                "scenario": "Szenarioanalyse",
                "base": "Base",
                "best": "Optimistisch",
                "worst": "Pessimistisch",
                "cf_mult": "Cashflow-Multiplikator",
                "wacc_shift": "WACC-Verschiebung (pp)",
                "sensitivity": "WACC-Sensitivität (±5pp)",
                "sens_note": "Zeigt, wie sich der NPV bei ±5 Prozentpunkten WACC verändert.",
                "chart": "NPV-WACC-Kurve",
                "details": "Detaillierte Hinweise (CFO-Niveau)",
                "npv_details": (
                "Der NPV ist die Summe der Barwerte zukünftiger Cashflows abzüglich der Anfangsinvestition. "
                "NPV>0 bedeutet Wertschaffung beim angegebenen Diskontsatz.\n\n"
                "WACC/Mindestrendite spiegelt die geforderte Rendite gemäß Projektrisiko wider. "
                "In der Praxis werden NPV, IRR und Payback gemeinsam bewertet."
                ),
                "irr_details": (
                "IRR ist der Diskontsatz, bei dem NPV=0. Er fasst die Projektrendite als einen Zinssatz zusammen.\n\n"
                "Hinweis: Bei mehreren Vorzeichenwechseln können mehrere IRRs existieren. "
                "Empfehlung: IRR immer zusammen mit der NPV-WACC-Kurve interpretieren."
                ),
                "payback_details": (
                "Payback zeigt, wann kumulierte Cashflows die Anfangsinvestition decken. "
                "Abgezinster Payback nutzt dazu diskontierte Cashflows (WACC).\n\n"
                "Payback ist ein Liquiditäts-/Risikomaß, aber kein Wertmaß wie NPV."
                ),
                "scenario_details": (
                "Szenarien erhöhen die Entscheidungsqualität unter Unsicherheit: Base, Optimistisch, Pessimistisch.\n\n"
                "Hier gesteuert über: (1) Cashflow-Multiplikator (Performance) (2) WACC-Verschiebung (Risikoprämie)."
                ),
                "sens_details": (
                "WACC-Sensitivität zeigt, wie stark die Bewertung auf Kapitalmarkt-/Risikoprämienänderungen reagiert. "
                "Break-even WACC ist die Schwelle, ab der kein Wert mehr geschaffen wird (NPV=0)."
                ),
                }

                LANGS = {"TR": TR, "EN": EN, "FR": FR, "DE": DE}

                # =========================================================
                # 3) HELPERS
                # =========================================================
                def fmt(value):
                if value is None:
                return "0,00"
                try:
                s = "{:,.2f}".format(float(value))
                return s.replace(",", "X").replace(".", ",").replace("X", ".")
                except Exception:
                return "0,00"

                def T(key: str) -> str:
                return LANGS[st.session_state.lang].get(key, key)

                def _safe_float(x, default=0.0):
                try:
                if x is None:
                return default
                v = float(x)
                if math.isnan(v) or math.isinf(v):
                return default
                return v
                except Exception:
                return default


                def _build_excel_bytes(sheets: dict):
                """Return XLSX bytes for given {sheet_name: dataframe}.
                Tries openpyxl first, then xlsxwriter. Returns None if no engine available."""
                excel_buf = io.BytesIO()

                engine = None
                try:
                import openpyxl  # noqa: F401
                engine = "openpyxl"
                except Exception:
                try:
                import xlsxwriter  # noqa: F401
                engine = "xlsxwriter"
                except Exception:
                engine = None

                if engine is None:
                return None

                with pd.ExcelWriter(excel_buf, engine=engine) as writer:
                for name, df in sheets.items():
                df.to_excel(writer, sheet_name=str(name)[:31], index=False)
                excel_buf.seek(0)
                return excel_buf.getvalue()


                def npv_from_flows(cf0: float, cfs: list[float], r: float) -> float:
                # r decimal (0.30 = 30%)
                pv_sum = 0.0
                for t, cf in enumerate(cfs, start=1):
                pv_sum += cf / ((1.0 + r) ** t)
                return cf0 + pv_sum

                def pv_sum_from_flows(cfs: list[float], r: float) -> float:
                pv_sum = 0.0
                for t, cf in enumerate(cfs, start=1):
                pv_sum += cf / ((1.0 + r) ** t)
                return pv_sum

                def find_breakeven_rate(cf0: float, cfs: list[float], lo: float, hi: float, iters: int = 80):
                # bisection on NPV, returns decimal rate or None
                f_lo = npv_from_flows(cf0, cfs, lo)
                f_hi = npv_from_flows(cf0, cfs, hi)
                if f_lo == 0:
                return lo
                if f_hi == 0:
                return hi
                if f_lo * f_hi > 0:
                return None
                a, b = lo, hi
                fa, fb = f_lo, f_hi
                for _ in range(iters):
                m = (a + b) / 2.0
                fm = npv_from_flows(cf0, cfs, m)
                if abs(fm) < 1e-8:
                return m
                if fa * fm <= 0:
                b, fb = m, fm
                else:
                a, fa = m, fm
                return (a + b) / 2.0

                def irr_from_flows(cf0: float, cfs: list[float]):
                # robust-ish IRR search on [-0.9, 5.0] (i.e., -90% to 500%)
                # If multiple sign changes, returns one economically meaningful root (if found).
                rates = np.linspace(-0.9, 5.0, 600)
                vals = np.array([npv_from_flows(cf0, cfs, r) for r in rates])
                signs = np.sign(vals)
                idx = np.where(np.diff(signs) != 0)[0]
                if len(idx) == 0:
                return None
                # pick the first crossing close to typical ranges
                i = int(idx[0])
                lo, hi = float(rates[i]), float(rates[i + 1])
                return find_breakeven_rate(cf0, cfs, lo, hi)

                def payback_period(cf0: float, cfs: list[float]):
                # simple payback with linear interpolation within the period
                cum = cf0
                if cum >= 0:
                return 0.0
                for i, cf in enumerate(cfs, start=1):
                prev = cum
                cum += cf
                if cum >= 0:
                if cf == 0:
                return float(i)
                frac = (0 - prev) / cf
                return (i - 1) + frac
                return None

                def discounted_payback_period(cf0: float, cfs: list[float], r: float):
                cum = cf0
                if cum >= 0:
                return 0.0
                for i, cf in enumerate(cfs, start=1):
                disc_cf = cf / ((1.0 + r) ** i)
                prev = cum
                cum += disc_cf
                if cum >= 0:
                if disc_cf == 0:
                return float(i)
                frac = (0 - prev) / disc_cf
                return (i - 1) + frac
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
                if "dark_mode" not in st.session_state:
                st.session_state.dark_mode = dark_from_qp
                else:
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
                #   - Switch çizimi yok: sadece tick (native checkbox)
                #   - Selectbox hem kapalı halde hem de açılan listbox/portal katmanında zorlanır
                # =========================================================
                st.markdown(
                f"""
                <style>
                /* App genel */
                .stApp {{
                background: {bg_color};
                color: {text_color};
                }}
                .block-container {{
                padding-top: 0.35rem;
                padding-bottom: 1.0rem;
                max-width: 1240px;
                }}

                /* Metinler */
                h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {{
                color: {text_color} !important;
                opacity: 1 !important;
                }}
                .stCaption, small {{
                color: {muted_text} !important;
                opacity: 1 !important;
                }}

                /* Kart */
                div[data-testid="stVerticalBlockBorderWrapper"] {{
                background: {card_bg} !important;
                border: 1px solid {border_color} !important;
                border-radius: 14px !important;
                }}

                /* Label + radio/checkbox text */
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

                /* Number input */
                .stNumberInput input {{
                color: {input_text} !important;
                background: {input_bg} !important;
                border: 1px solid {border_color} !important;
                border-radius: 12px !important;
                font-weight: 900 !important;
                }}

                /* =====================================================
                SELECTBOX FIX (KAPALI HAL + FOCUS HAL + ICON + INPUT)
                ===================================================== */
                div[data-testid="stSelectbox"] div[data-baseweb="select"] {{
                background: {input_bg} !important;
                border: 1px solid {border_color} !important;
                border-radius: 12px !important;
                }}

                /* Kapalı selectbox'ın asıl boyalı katmanı (cloud'da bazen burası beyaz kalıyor) */
                div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
                background: {input_bg} !important;
                }}

                /* Combobox role'u da zorla */
                div[data-testid="stSelectbox"] div[role="combobox"] {{
                background: {input_bg} !important;
                color: {input_text} !important;
                }}

                /* İç yazı/placeholder/ikon */
                div[data-testid="stSelectbox"] div[data-baseweb="select"] *,
                div[data-testid="stSelectbox"] div[role="combobox"] * {{
                color: {input_text} !important;
                opacity: 1 !important;
                -webkit-text-fill-color: {input_text} !important;
                }}
                div[data-testid="stSelectbox"] svg {{
                fill: {input_text} !important;
                color: {input_text} !important;
                }}

                /* =====================================================
                DROPDOWN AÇILINCA (PORTAL/POPOVER/LISTBOX/MENU)
                ===================================================== */
                div[data-baseweb="popover"] {{
                background: {card_bg} !important;
                }}
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
                div[data-baseweb="menu"] *,
                div[data-baseweb="menu"] span {{
                color: {text_color} !important;
                opacity: 1 !important;
                -webkit-text-fill-color: {text_color} !important;
                }}

                div[role="option"][aria-selected="true"],
                li[role="option"][aria-selected="true"] {{
                background: rgba(13,110,253,0.12) !important;
                }}
                div[role="option"]:hover,
                li[role="option"]:hover {{
                background: rgba(13,110,253,0.10) !important;
                }}

                /* Buttons */
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
                opacity: 1 !important;
                }}

                /* Sticky topbar */
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

                /* Checkbox: tek kontrol tick */
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
                if st.button(f"{T('m_npv')}", use_container_width=True): go("npv")

                with right:
                if st.button(f"💳 {T('m_install')}", use_container_width=True): go("install")
                if st.button(f"📋 {T('m_table')}", use_container_width=True): go("table")
                if st.button(f"{T('m_deposit')}", use_container_width=True): go("deposit")
                if st.button(f"{T('m_disc')}", use_container_width=True): go("disc")

                # =========================================================
                # 10) MODÜLLER
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
                with c3:
                r = st.number_input(T("cm_r"), value=0.0, format="%.2f", key="cm_r")
                with c4:
                n = st.number_input(T("cm_n"), value=1, min_value=0, step=1, key="cm_n")

                tax = st.number_input(T("tax"), value=0.0, format="%.2f", key="cm_tax")

                if st.button(T("calc"), type="primary"):
                # Net periodic rate after tax
                net_r = (r / 100.0) * (1 - tax / 100.0)

                if n < 0:
                st.error("Dönem sayısı 0 veya pozitif olmalı.")
                else:
                if target == T("opt_pv"):
                # Given PV -> compute FV
                pv = _safe_float(val, 0.0)
                fv = pv * ((1 + net_r) ** n)
                diff = fv - pv
                st.metric(T("cm_res"), f"{fmt(fv)} ₺")
                st.caption(f"{T('cm_res_diff')}: {fmt(diff)} ₺")
                else:
                # Given FV -> compute PV
                fv = _safe_float(val, 0.0)
                if (1 + net_r) == 0 and n > 0:
                st.error("Faiz oranı -100% iken indirgeme yapılamaz.")
                else:
                pv = fv / ((1 + net_r) ** n) if n > 0 else fv
                diff = fv - pv
                st.metric(T("cm_res"), f"{fmt(pv)} ₺")
                st.caption(f"{T('cm_res_diff')}: {fmt(diff)} ₺")


                elif st.session_state.page == "npv":
                st.title(T("m_npv"))
                st.divider()

                # ---------------------------
                # 1) Üst Parametreler
                # ---------------------------
                with st.container(border=True):
                c1, c2, c3, c4 = st.columns([3, 2, 2, 2], vertical_alignment="center")

                with c1:
                st.caption(T("proj_name"))
                proj = st.text_input("", value="Project A", key="inv_eval_proj", label_visibility="collapsed")
                with c2:
                st.caption(T("currency"))
                ccy = st.selectbox("", ["TRY","USD","EUR"], index=0, key="inv_eval_ccy", label_visibility="collapsed")
                with c3:
                st.caption(T("wacc"))
                wacc_pct = st.number_input("", value=30.0, format="%.2f", key="inv_eval_wacc", label_visibility="collapsed")
                with c4:
                n = st.number_input(T("periods"), value=5, min_value=1, step=1, key="inv_eval_n")

                r = _safe_float(wacc_pct, 0.0) / 100.0

                # ---------------------------
                # 2) CFO Detayları (Açılır-Kapanır)
                # ---------------------------
                with st.expander(f"ℹ️ {T('details')}", expanded=False):
                st.markdown(f"**NPV:** {T('npv_details')}")
                st.markdown("---")
                st.markdown(f"**IRR:** {T('irr_details')}")
                st.markdown("---")
                st.markdown(f"**Payback:** {T('payback_details')}")
                st.markdown("---")
                st.markdown(f"**Senaryo:** {T('scenario_details')}")
                st.markdown("---")
                st.markdown(f"**Duyarlılık:** {T('sens_details')}")

                # ---------------------------
                # ---------------------------
                # 3) Senaryo Ayarları (CFO Preset + Custom)
                # ---------------------------
                with st.container(border=True):
                s1, s2, s3 = st.columns([2, 2, 3], vertical_alignment="center")

                with s1:
                scenario = st.radio(
                T("scenario"),
                [T("base"), T("best"), T("worst")],
                horizontal=True,
                key="inv_eval_scenario",
                )

                # CFO preset mantığı:
                # - Base: çarpan 1.00, WACC kayması 0.00pp
                # - Best: nakit akışı +10%, WACC -1.00pp
                # - Worst: nakit akışı -10%, WACC +1.00pp
                if scenario == T("base"):
                preset_mult = 1.00
                preset_shift_pp = 0.00
                elif scenario == T("best"):
                preset_mult = 1.10
                preset_shift_pp = -1.00
                else:
                preset_mult = 0.90
                preset_shift_pp = 1.00

                with s2:
                use_custom = st.checkbox("Custom", value=False, key="inv_eval_custom")

                with s3:
                if use_custom:
                cA, cB = st.columns(2)
                with cA:
                cf_mult = st.number_input(
                T("cf_mult"),
                value=float(preset_mult),
                format="%.2f",
                key="inv_eval_cf_mult",
                )
                with cB:
                wacc_shift_pp = st.number_input(
                T("wacc_shift"),
                value=float(preset_shift_pp),
                format="%.2f",
                key="inv_eval_wacc_shift",
                )
                else:
                # Custom kapalıyken presetleri kilitle
                st.caption("Preset senaryo aktif. Detay değiştirmek için **Custom** aç.")
                cf_mult = preset_mult
                wacc_shift_pp = preset_shift_pp

                # Senaryo parametreleri
                scen_mult = _safe_float(cf_mult, 1.0)
                scen_shift = _safe_float(wacc_shift_pp, 0.0) / 100.0
                r_scen = max(-0.999, r + scen_shift)  # güvenlik


                # ---------------------------
                # 4) Nakit Akışları
                # ---------------------------
                with st.container(border=True):
                st.subheader(T("inv_eval_title"))

                c0 = st.number_input(T("cf0"), value=-100000.0, step=1000.0, format="%.2f", key="inv_eval_cf0")

                cols = st.columns(3)
                base_cfs = []
                for i in range(1, int(n) + 1):
                with cols[(i - 1) % 3]:
                cf_i = st.number_input(
                f"{T('cf')} {i}",
                value=30000.0,
                step=1000.0,
                format="%.2f",
                key=f"inv_eval_cf_{i}",
                )
                base_cfs.append(_safe_float(cf_i, 0.0))

                # Senaryoya göre akışları uygula:
                # İstersen Best/Worst’ta otomatik farklı multiplier da verebiliriz,
                # ama sen zaten CFO esnekliği için manuel multiplier koymuşsun.
                if scenario == T("base"):
                cfs = base_cfs[:]
                r_used = r
                else:
                cfs = [cf * scen_mult for cf in base_cfs]
                r_used = r_scen

                # ---------------------------
                # 5) Sekmeler (NPV / IRR / Payback)
                # ---------------------------
                tab1, tab2, tab3 = st.tabs([T("tab_npv"), T("tab_irr"), T("tab_payback")])

                do_calc = st.button(T("calc"), type="primary")

                if do_calc:
                # ---- Hesaplar (ortak) ----
                npv_val = npv_from_flows(_safe_float(c0, 0.0), cfs, r_used)
                pv_sum = pv_sum_from_flows(cfs, r_used)
                irr_val = irr_from_flows(_safe_float(c0, 0.0), cfs)

                pb = payback_period(_safe_float(c0, 0.0), cfs)
                dpb = discounted_payback_period(_safe_float(c0, 0.0), cfs, r_used)

                # Break-even WACC (NPV=0) aralığı: 0%..300%
                be = find_breakeven_rate(_safe_float(c0, 0.0), cfs, 0.0, 3.0)  # decimal

                # =========================
                # CFO Executive Summary
                # =========================
                with st.container(border=True):
                st.subheader("Executive Summary")
                k1, k2, k3, k4 = st.columns(4)
                k1.metric("NPV", f"{fmt(npv_val)} {ccy}")
                k2.metric("IRR", ("—" if irr_val is None else f"%{fmt(irr_val*100)}"))
                k3.metric("Payback", ("—" if pb is None else f"{fmt(pb)} yıl"))
                k4.metric("Break-even WACC", ("—" if be is None else f"%{fmt(be*100)}"))

                # Karar sinyalleri (basit)
                sig1 = "✅" if npv_val > 0 else "⚠️"
                sig2 = "✅" if (irr_val is not None and irr_val > r_used) else "⚠️"
                st.caption(f"{sig1} NPV {'pozitif' if npv_val > 0 else 'negatif'} | "
                f"{sig2} IRR {'WACC üzerinde' if (irr_val is not None and irr_val > r_used) else 'WACC altında / hesaplanamadı'}")

                # =========================
                # Export (Excel / CSV)
                # =========================
                st.markdown("""
                <style>
                /* Download buttons: force readable styling (dark mode safe) */
                div[data-testid="stDownloadButton"] > button,
                .stDownloadButton > button,
                button[kind="secondary"] {
                background: rgba(255,255,255,0.10) !important;
                color: #F9FAFB !important;
                border: 1px solid rgba(255,255,255,0.35) !important;
                box-shadow: none !important;
                }
                div[data-testid="stDownloadButton"] > button:hover,
                .stDownloadButton > button:hover {
                background: rgba(255,255,255,0.16) !important;
                }
                div[data-testid="stDownloadButton"] > button:disabled,
                .stDownloadButton > button:disabled {
                opacity: 0.5 !important;
                }
                </style>
                """, unsafe_allow_html=True)

                exp1, exp2 = st.columns(2, vertical_alignment="center")

                # Summary tables
                _assumptions = {
                "Project": proj,
                "Currency": ccy,
                "WACC (base %)": float(wacc_pct),
                "Scenario": scenario,
                "CF multiplier": float(scen_mult),
                "WACC shift (pp)": float(wacc_shift_pp),
                "WACC used (%)": float(r_used * 100),
                "Initial investment (C0)": float(_safe_float(c0, 0.0)),
                "Cashflows": ", ".join([str(_safe_float(x, 0.0)) for x in cfs]),
                }
                _results = {
                "NPV": float(npv_val),
                "IRR": (None if irr_val is None else float(irr_val)),
                "Payback (years)": (None if pb is None else float(pb)),
                "Discounted Payback (years)": (None if dpb is None else float(dpb)),
                "Break-even WACC": (None if be is None else float(be)),
                }

                df_assum = pd.DataFrame(list(_assumptions.items()), columns=["Field", "Value"])
                df_res = pd.DataFrame(list(_results.items()), columns=["Metric", "Value"])

                # Excel bytes
                # Excel bytes (robust)
                excel_bytes = _build_excel_bytes({
                "Summary": df_res,
                "Assumptions": df_assum,
                })
                if excel_bytes is None:
                st.warning("Excel export için gerekli kütüphane bulunamadı (openpyxl / xlsxwriter). CSV export çalışır durumda.")

            with exp1:
                if excel_bytes is None:
                    st.caption("Excel export devre dışı (openpyxl / xlsxwriter yok).")
                else:
                    st.download_button(
                        "Download Excel",
                        data=excel_bytes,
                        file_name="investment_summary.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
            with exp2:
                st.download_button(
                    "Download Summary CSV",
                    data=df_res.to_csv(index=False).encode("utf-8"),
                    file_name="investment_summary.csv",
                    mime="text/csv",
                )

        st.write("")

        # =========================
        # TAB 1: NPV
        # =========================
        with tab1:
            m1, m2, m3 = st.columns(3)
            m1.metric(T("npv"), f"{fmt(npv_val)} {ccy}")
            m2.metric(T("pv_sum"), f"{fmt(pv_sum)} {ccy}")
            m3.metric(T("breakeven"), ("—" if be is None else f"%{fmt(be*100)}"))

            st.write("---")
            st.caption(T("sens_note"))

            # WACC duyarlılık tablosu (±5 puan)
            rows = []
            for pp in range(-5, 6):  # -5 .. +5
                rr = (r_used + (pp / 100.0))
                rr = max(-0.999, rr)
                rows.append(
                    {
                        "WACC (%)": (rr * 100.0),
                        "NPV": npv_from_flows(_safe_float(c0, 0.0), cfs, rr),
                    }
                )

            df = pd.DataFrame(rows)
            df["WACC (%)"] = df["WACC (%)"].apply(lambda x: float(f"{x:.2f}"))
            df["NPV"] = df["NPV"].apply(lambda x: f"{fmt(x)} {ccy}")
            with st.expander('📈 WACC Sensitivity (Table + Chart)', expanded=False):
                st.dataframe(df, use_container_width=True, hide_index=True)

                # 2D Duyarlılık: WACC x Nakit Akışı (Expander)
            with st.expander('📊 2D Sensitivity (WACC x Cashflow)', expanded=False):
                sA, sB, sC = st.columns([2, 2, 2])
                with sA:
                    cf_range = st.selectbox('CF değişimi aralığı', ['±10%', '±20%', '±30%'], index=1, key='sens2d_cf_range')
                with sB:
                    wacc_range = st.selectbox('WACC aralığı', ['±3pp', '±5pp', '±7pp'], index=1, key='sens2d_wacc_range')
                with sC:
                    step_pp = st.selectbox('WACC adım', [1, 2], index=0, key='sens2d_wacc_step')

                cf_map = {'±10%': 10, '±20%': 20, '±30%': 30}
                wr_map = {'±3pp': 3, '±5pp': 5, '±7pp': 7}
                cf_lim = cf_map.get(cf_range, 20)
                wr_lim = wr_map.get(wacc_range, 5)

                cf_levels = list(range(-cf_lim, cf_lim + 1, 5))  # 5% adım
                wacc_levels = list(range(-wr_lim, wr_lim + 1, int(step_pp)))  # pp adım

                grid_rows = []
                for cf_pct in cf_levels:
                    row = {'CF %': cf_pct}
                    cfs_adj = [cf * (1.0 + cf_pct / 100.0) for cf in cfs]
                    for wpp in wacc_levels:
                        rr = max(-0.999, r_used + (wpp / 100.0))
                        row[f'WACC {wpp:+d}pp'] = npv_from_flows(_safe_float(c0, 0.0), cfs_adj, rr)
                    grid_rows.append(row)

                df2 = pd.DataFrame(grid_rows)
                # format
                for col in [c for c in df2.columns if c.startswith('WACC')]:
                    df2[col] = df2[col].apply(lambda x: f"{fmt(x)} {ccy}")
                st.dataframe(df2, use_container_width=True, hide_index=True)


            st.write("---")
            st.subheader(T("chart"))

            # Grafik: NPV vs WACC (0..max(50, wacc+10))
            max_r_pct = int(max(50, round((r_used * 100) + 10)))
            xs = list(range(0, max_r_pct + 1))
            ys = [npv_from_flows(_safe_float(c0, 0.0), cfs, x / 100.0) for x in xs]

            fig = plt.figure()
            plt.plot(xs, ys)
            plt.axhline(0)
            plt.xlabel("WACC (%)")
            plt.ylabel(f"NPV ({ccy})")
            st.pyplot(fig, clear_figure=True)

        # =========================
        # TAB 2: IRR
        # =========================
        with tab2:
            if irr_val is None:
                st.warning("IRR hesaplanamadı (yakınsamama / çoklu IRR olabilir). NPV-WACC eğrisini referans alın.")
            else:
                st.metric(T("irr"), f"%{fmt(irr_val*100)}")

        # =========================
        # TAB 3: PAYBACK
        # =========================
        with tab3:
            cA, cB = st.columns(2)
            with cA:
                if pb is None:
                    st.warning(T("payback_never"))
                else:
                    st.metric(T("payback"), f"{fmt(pb)}")
            with cB:
                if dpb is None:
                    st.warning(T("payback_never"))
                else:
                    st.metric(T("payback_disc"), f"{fmt(dpb)}")
                    


elif st.session_state.page == "install":
    st.title(T("m_install"))
    st.divider()
    st.info("Bu modül (Kredi / Taksit) bu dosyada henüz ekli değil. Bir sonraki adımda birlikte ekleyebiliriz.")

elif st.session_state.page == "table":
    st.title(T("m_table"))
    st.divider()
    st.info("Bu modül (Ödeme Tablosu) bu dosyada henüz ekli değil. Bir sonraki adımda birlikte ekleyebiliriz.")

elif st.session_state.page == "deposit":
    st.title(T("m_deposit"))
    st.divider()
    st.info("Bu modül (Mevduat Getirisi) bu dosyada henüz ekli değil. Bir sonraki adımda birlikte ekleyebiliriz.")

elif st.session_state.page == "disc":
    st.title(T("m_disc"))
    st.divider()
    st.info("Bu modül (İskontolu Alacak) bu dosyada henüz ekli değil. Bir sonraki adımda birlikte ekleyebiliriz.")

else:
    st.title("Modül bulunamadı")
    st.info(
        f"Seçilen sayfa: **{st.session_state.get('page', 'home')}**\n\n"
        "Bu sayfa için henüz bir ekran tanımı yok."
    )
