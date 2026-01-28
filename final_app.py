import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Yatırım Değerlendirme | NPV • IRR • Payback",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================
# STYLE (tight, professional)
# =========================
st.markdown(
    """
<style>
/* tighter overall */
.block-container { padding-top: 0.75rem; padding-bottom: 1.0rem; max-width: 1280px; }
h1, h2, h3 { margin-top: 0.35rem !important; margin-bottom: 0.35rem !important; }
div[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 14px !important; }
div[data-testid="stMetricValue"] { font-weight: 800 !important; }
div[data-testid="stMetricLabel"] { font-weight: 700 !important; }
[data-testid="stTabs"] button { font-weight: 700 !important; }
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# FINANCE HELPERS
# =========================
def _npv(rate: float, cashflows: list[float]) -> float:
    total = 0.0
    for t, cf in enumerate(cashflows):
        total += cf / ((1 + rate) ** t)
    return total

def _irr(cashflows: list[float], guess: float = 0.20, tol: float = 1e-7, max_iter: int = 200):
    # Newton-Raphson on NPV=0
    r = guess
    for _ in range(max_iter):
        f = 0.0
        df = 0.0
        for t, cf in enumerate(cashflows):
            f += cf / ((1 + r) ** t)
            if t > 0:
                df += -t * cf / ((1 + r) ** (t + 1))
        if abs(f) < tol:
            return r
        if df == 0:
            return None
        r_next = r - f / df
        if r_next <= -0.9999 or r_next > 10:
            return None
        r = r_next
    return None

def _payback_simple(cashflows: list[float]):
    # returns (year_float or None, cumulative_list)
    cum = 0.0
    cum_list = []
    for i, cf in enumerate(cashflows):
        cum += cf
        cum_list.append(cum)
        if i > 0 and cum >= 0:
            prev = cum - cf
            if cf == 0:
                return float(i), cum_list
            frac = (0 - prev) / cf
            return (i - 1) + frac, cum_list
    return None, cum_list

# =========================
# HEADER
# =========================
st.markdown("## Yatırım Değerlendirme")
st.caption("NPV, IRR ve Payback hesaplamalarını tek ekranda yönetin. Cashflow girişleri Excel benzeri tabloda yapılır.")

# =========================
# TOP SETTINGS
# =========================
top_left, top_mid, top_right = st.columns([2, 1, 1], vertical_alignment="center")

with top_left:
    project = st.text_input("Proje Adı", value="Project A")

with top_mid:
    currency = st.selectbox("Para Birimi", ["TRY", "USD", "EUR"], index=0)

with top_right:
    disc_pct = st.number_input("İskonto (WACC / Required Return) %", value=30.00, min_value=0.0, max_value=500.0, format="%.2f")

st.divider()

# =========================
# MAIN LAYOUT
# =========================
left, right = st.columns([3, 2], vertical_alignment="top")

with left:
    with st.container(border=True):
        st.markdown("### Nakit Akışları")
        n_years = st.number_input("Dönem Sayısı (Yıl)", value=5, min_value=1, step=1)

        # Build default table (stable key approach)
        if "cf_table" not in st.session_state or st.session_state.get("cf_n_years") != int(n_years):
            rows = [{"Dönem": 0, "Nakit Akışı": -100000.0}]
            for t in range(1, int(n_years) + 1):
                rows.append({"Dönem": t, "Nakit Akışı": 30000.0})
            st.session_state["cf_table"] = pd.DataFrame(rows)
            st.session_state["cf_n_years"] = int(n_years)

        cf_df = st.data_editor(
            st.session_state["cf_table"],
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
            column_config={
                "Dönem": st.column_config.NumberColumn("Dönem", disabled=True),
                "Nakit Akışı": st.column_config.NumberColumn("Nakit Akışı", format="%.2f"),
            },
            key="cf_editor",
        )

        # persist changes
        st.session_state["cf_table"] = cf_df.copy()

        cashflows = cf_df["Nakit Akışı"].astype(float).tolist()
        r = float(disc_pct) / 100.0

        st.caption("İpucu: CF0 genelde negatiftir (başlangıç yatırım). CF1..CFN net nakit giriş/çıkışlarıdır.")

with right:
    with st.container(border=True):
        st.markdown("### Özet")
        st.write(f"**Proje:** {project}")
        st.write(f"**Para Birimi:** {currency}")
        st.write(f"**İskonto (WACC):** {disc_pct:.2f}%")
        st.write(f"**Dönem:** {int(n_years)} yıl")

    with st.container(border=True):
        st.markdown("### Kümülatif Nakit Akışı")
        cum = 0.0
        rows = []
        for t, cf in enumerate(cashflows):
            cum += cf
            rows.append({"Dönem": t, "CF": cf, "Kümülatif": cum})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    with st.expander("ℹ️ NPV / IRR / Payback açıklaması"):
        st.markdown(
            """
- **NPV (Net Bugünkü Değer):** Gelecek nakit akışlarının bugünkü değeri − başlangıç yatırım.  
  - **NPV > 0**: değer yaratır (varsayımlar altında).
- **IRR (İç Verim Oranı):** NPV’yi **0** yapan iskonto oranı.  
  - **IRR > WACC**: genelde olumlu yorumlanır.
- **Payback (Geri Ödeme):** Kümülatif nakit akışı **0’a ne zaman gelir** (basit payback iskonto içermez).
"""
        )

st.divider()

# =========================
# TABS: NPV | IRR | PAYBACK
# =========================
tab1, tab2, tab3 = st.tabs(["NPV", "IRR", "Payback"])

with tab1:
    with st.container(border=True):
        val_npv = _npv(r, cashflows)
        st.metric("NPV (Net Bugünkü Değer)", f"{val_npv:,.2f} {currency}")
        st.caption("NPV, seçilen iskonto oranına (WACC/Required Return) göre hesaplanır.")

with tab2:
    with st.container(border=True):
        val_irr = _irr(cashflows, guess=max(0.01, r))
        if val_irr is None:
            st.warning("IRR hesaplanamadı. Nakit akışlarında çoklu işaret değişimi / yakınsamama olabilir.")
        else:
            st.metric("IRR (İç Verim Oranı)", f"{val_irr*100:,.2f} %")
            st.caption("IRR, NPV’yi sıfıra getiren iskonto oranıdır.")

with tab3:
    with st.container(border=True):
        pb, _ = _payback_simple(cashflows)
        if pb is None:
            st.warning("Payback bulunamadı: Kümülatif nakit akışı hiç pozitife dönmüyor.")
        else:
            st.metric("Basit Payback Süresi", f"{pb:,.2f} yıl")
        st.caption("Not: Basit payback iskonto içermez. İstersen ‘Discounted Payback’ da ekleyebiliriz.")
