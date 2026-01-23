import streamlit as st
import datetime
import pandas as pd
import numpy as np
from scipy.optimize import newton

# ==========================================
# AYARLAR VE STİL
# ==========================================
st.set_page_config(page_title="Finansal Hesap Makinesi Pro", page_icon="🚀", layout="wide")

# ==========================================
# YARDIMCI FONKSİYONLAR
# ==========================================
def _to_float(text: str) -> float:
    t = str(text).strip().replace(" ", "")
    if t == "": return 0.0
    if "," in t and "." in t:
        t = t.replace(".", "").replace(",", ".")
    else:
        t = t.replace(",", ".")
    return float(t)

def _parse_cashflows(text: str) -> list[float]:
    parts = [p.strip() for p in text.split(",")]
    cfs = [_to_float(p) for p in parts if p != ""]
    return cfs

# ==========================================
# MENÜ YAPISI
# ==========================================
st.sidebar.title("🚀 Menü")

menu_secenekleri = [
    "Ana Sayfa",
    "Yatırım Getiri Oranı",
    "Oran Hesaplamaları",
    "Para Hesaplamaları (I)",
    "Para Hesaplamaları (II)",
    "Bono / Tahvil",
    "Eşit Taksit (PMT)",
    "Ödeme Tablosu (Amortisman)",
    "Komisyon Dahil Maliyet",   # <-- ARTIK BU DA AKTİF!
    "Eurobond"
]

secim = st.sidebar.radio("Araç Seçin:", menu_secenekleri)

# ==========================================
# 1. ANA SAYFA
# ==========================================
if secim == "Ana Sayfa":
    st.title("✅ Finansal Hesap Makinesi Pro")
    st.markdown("""
    ### Hoş Geldiniz 👋
    
    Tüm modüller başarıyla web arayüzüne taşınmıştır.
    
    **Sistem Durumu:**
    * ✅ **Komisyon Maliyeti:** EKLENDİ!
    * ✅ **Eşit Taksit (PMT):** Aktif
    * ✅ **Bono / Tahvil:** Aktif
    * ✅ **Para Hesaplamaları (I & II):** Aktif
    * ✅ **Oranlar & ROI:** Aktif
    * ✅ **Eurobond & Amortisman:** Aktif
    """)

# ==========================================
# 2. YATIRIM GETİRİ ORANI (ROI)
# ==========================================
elif secim == "Yatırım Getiri Oranı":
    st.title("📈 Yatırım Getiri Analizi")
    with st.form("roi_form"):
        c1, c2, c3 = st.columns(3)
        with c1: alis = st.number_input("Alış Tutarı", min_value=0.01, value=100000.0)
        with c2: satis = st.number_input("Satış Tutarı", min_value=0.0, value=110000.0)
        with c3: gun = st.number_input("Vade (Gün)", min_value=1, value=90)
        if st.form_submit_button("Getiriyi Hesapla"):
            basit_getiri = (satis / alis) - 1
            yillik_getiri = (1 + basit_getiri) ** (365 / gun) - 1
            st.divider()
            c_res1, c_res2 = st.columns(2)
            delta_color = "normal" if basit_getiri >= 0 else "inverse"
            c_res1.metric("Basit Getiri", f"%{basit_getiri*100:.4f}", f"Net: {satis - alis:,.2f}", delta_color=delta_color)
            c_res2.metric("Yıllıklandırılmış Getiri", f"%{yillik_getiri*100:.4f}")

# ==========================================
# 3. ORAN HESAPLAMALARI
# ==========================================
elif secim == "Oran Hesaplamaları":
    st.title("➗ Oran ve Faiz Hesaplamaları")
    tab1, tab2 = st.tabs(["💰 Basit/Bileşik Faiz", "🔄 Oran Dönüştürücü"])
    with tab1:
        with st.form("faiz_form"):
            c1, c2 = st.columns(2)
            pv = c1.number_input("Anapara (PV)", value=100000.0)
            rate = c2.number_input("Dönemsel Faiz (%)", value=5.0)
            c3, c4 = st.columns(2)
            n = c3.number_input("Dönem", value=12.0)
            mode = c4.radio("Yöntem", ["Basit Faiz", "Bileşik Faiz"], horizontal=True)
            if st.form_submit_button("Hesapla"):
                r = rate / 100.0
                fv = pv * (1 + r * n) if mode == "Basit Faiz" else pv * ((1 + r) ** n)
                st.metric("Gelecek Değer (FV)", f"{fv:,.2f}", f"Getiri: {fv-pv:,.2f}")
    with tab2:
        with st.form("donusum_form"):
            c1, c2 = st.columns(2)
            c_rate = c1.number_input("Oran (%)", value=50.0)
            yon = c2.selectbox("Yön", ["Yıllık ➡️ Aylık", "Aylık ➡️ Yıllık"])
            if st.form_submit_button("Dönüştür"):
                r = c_rate / 100.0
                res = (1 + r) ** (1/12) - 1 if "Yıllık ➡️ Aylık" in yon else (1 + r) ** 12 - 1
                st.success(f"Sonuç: **%{res*100:.4f}**")

# ==========================================
# 4. PARA HESAPLAMALARI I
# ==========================================
elif secim == "Para Hesaplamaları (I)":
    st.title("💵 Paranın Zaman Değeri (TVM)")
    tab_fv, tab_pv, tab_npv = st.tabs(["🔮 Gelecek Değer (FV)", "🔙 Bugünkü Değer (PV)", "📊 Net Bugünkü Değer (NPV)"])
    
    with tab_fv:
        with st.form("fv_form"):
            c1, c2 = st.columns(2)
            pv_in = c1.number_input("Bugünkü Değer (PV)", value=10000.0)
            r_fv = c2.number_input("Faiz (%)", value=3.0)
            n_fv = st.number_input("Dönem", value=12.0)
            if st.form_submit_button("FV Hesapla"):
                res = pv_in * ((1 + r_fv/100) ** n_fv)
                st.metric("FV", f"{res:,.2f}", f"Fark: {res-pv_in:,.2f}")

    with tab_pv:
        with st.form("pv_form"):
            c1, c2 = st.columns(2)
            fv_in = c1.number_input("Hedef FV", value=15000.0)
            r_pv = c2.number_input("İskonto (%)", value=3.0)
            n_pv = st.number_input("Dönem", value=12.0)
            if st.form_submit_button("PV Hesapla"):
                res = fv_in / ((1 + r_pv/100) ** n_pv)
                st.metric("PV", f"{res:,.2f}")

    with tab_npv:
        st.info("Akışları virgülle ayırın (Örn: -100000, 30000, 40000). İlk değer eksi olmalı.")
        with st.form("npv_simple"):
            r_npv = st.number_input("İskonto (%)", value=10.0)
            txt_npv = st.text_input("Akışlar", value="-100000, 30000, 40000, 50000")
            if st.form_submit_button("NPV Hesapla"):
                try:
                    r = r_npv / 100.0
                    cfs = _parse_cashflows(txt_npv)
                    npv_val = sum([cf / ((1 + r) ** t) for t, cf in enumerate(cfs)])
                    lbl = "✅ Kârlı" if npv_val > 0 else "❌ Zararlı"
                    st.metric(f"NPV - {lbl}", f"{npv_val:,.2f}")
                except: st.error("Format hatası.")

# ==========================================
# 5. PARA HESAPLAMALARI II
# ==========================================
elif secim == "Para Hesaplamaları (II)":
    st.title("📊 Gelişmiş Yatırım Analizi")
    
    def _npv_internal(rate, cfs): return sum([cf / ((1 + rate) ** t) for t, cf in enumerate(cfs)])
    def _irr_bisection(cfs):
        lo, hi = -0.90, 10.0
        f_lo = _npv_internal(lo, cfs)
        f_hi = _npv_internal(hi, cfs)
        tries = 0
        while f_lo * f_hi > 0 and tries < 30 and hi < 1000:
            hi *= 1.5
            f_hi = _npv_internal(hi, cfs)
            tries += 1
        if f_lo * f_hi > 0: return None
        for _ in range(120):
            mid = (lo + hi) / 2
            f_mid = _npv_internal(mid, cfs)
            if f_lo * f_mid <= 0: hi, f_hi = mid, f_mid
            else: lo, f_lo = mid, f_mid
        return (lo + hi) / 2
    def _payback_calc(cfs):
        cum = 0.0
        for t, cf in enumerate(cfs):
            prev, cum = cum, cum + cf
            if cum >= 0 and t > 0:
                return float(t) if cf == 0 else (t - 1) + (-prev / cf)
        return None
    def _discounted_payback_calc(rate, cfs):
        cum = 0.0
        for t, cf in enumerate(cfs):
            disc = cf / ((1 + rate) ** t)
            prev, cum = cum, cum + disc
            if cum >= 0 and t > 0:
                return float(t) if disc == 0 else (t - 1) + (-prev / disc)
        return None

    tab_irr, tab_pb, tab_dpb = st.tabs(["📉 IRR", "⏱️ Payback", "⏳ Discounted Payback"])
    with tab_irr:
        inp = st.text_input("Akışlar (IRR)", value="-100000, 30000, 40000, 50000")
        if st.button("IRR Hesapla"):
            try:
                val = _irr_bisection(_parse_cashflows(inp))
                st.metric("IRR", f"%{val*100:.4f}" if val else "Bulunamadı")
            except: st.error("Hata")
    with tab_pb:
        inp = st.text_input("Akışlar (Payback)", value="-100000, 30000, 40000, 50000")
        if st.button("Payback Hesapla"):
            try:
                val = _payback_calc(_parse_cashflows(inp))
                st.metric("Süre", f"{val:.2f} Dönem" if val else "Amorti etmiyor")
            except: st.error("Hata")
    with tab_dpb:
        r = st.number_input("İskonto (%)", 10.0)
        inp = st.text_input("Akışlar (D. Payback)", value="-100000, 30000, 40000, 50000")
        if st.button("D. Payback Hesapla"):
            try:
                val = _discounted_payback_calc(r/100, _parse_cashflows(inp))
                st.metric("Süre", f"{val:.2f} Dönem" if val else "Amorti etmiyor")
            except: st.error("Hata")

# ==========================================
# 6. BONO / TAHVİL
# ==========================================
elif secim == "Bono / Tahvil":
    st.title("📜 Bono ve Tahvil Hesaplayıcı")
    col_set, _ = st.columns([1, 3])
    with col_set: day_base = st.selectbox("Gün Sayım Bazı", [365, 360])
    base = float(day_base)

    tab_fiyat, tab_faiz = st.tabs(["💰 Fiyat Hesapla", "📉 Faiz Hesapla"])
    with tab_fiyat:
        with st.form("bond_price"):
            c1, c2, c3 = st.columns(3)
            nom1 = c1.number_input("Nominal", 100000.0)
            rate1 = c2.number_input("Faiz (%)", 45.0)
            days1 = c3.number_input("Gün", 90)
            if st.form_submit_button("Hesapla"):
                if days1 > 0:
                    price = nom1 / (1 + (rate1/100) * (days1 / base))
                    st.metric("Fiyat", f"{price:,.2f}")
    with tab_faiz:
        with st.form("bond_rate"):
            c1, c2, c3 = st.columns(3)
            nom2 = c1.number_input("Nominal", 100000.0)
            price2 = c2.number_input("Fiyat", 90000.0)
            days2 = c3.number_input("Gün", 90)
            if st.form_submit_button("Hesapla"):
                if days2 > 0 and price2 > 0:
                    r = (nom2 / price2 - 1) / (days2 / base)
                    st.metric("Faiz", f"%{r*100:.4f}")

# ==========================================
# 7. EŞİT TAKSİT (PMT)
# ==========================================
elif secim == "Eşit Taksit (PMT)":
    st.title("💳 Eşit Taksit Hesaplayıcı (PMT)")
    with st.form("quick_pmt"):
        col1, col2, col3 = st.columns(3)
        with col1: p_quick = st.number_input("Kredi Tutarı", value=50000.0)
        with col2: r_quick = st.number_input("Aylık Faiz (%)", value=3.5)
        with col3: n_quick = st.number_input("Vade (Ay)", value=6)
        
        if st.form_submit_button("Taksiti Hesapla"):
            r = r_quick / 100.0
            if n_quick > 0 and p_quick > 0:
                pmt = p_quick / n_quick if r == 0 else p_quick * (r * (1 + r) ** n_quick) / ((1 + r) ** n_quick - 1)
                st.metric("Aylık Taksit", f"{pmt:,.2f} TL")
                st.info(f"Toplam Geri Ödeme: **{(pmt * n_quick):,.2f} TL**")

# ==========================================
# 8. ÖDEME TABLOSU (AMORTİSMAN)
# ==========================================
elif secim == "Ödeme Tablosu (Amortisman)":
    st.title("📅 Ödeme Tablosu (Amortisman)")
    with st.form("amort_form"):
        col1, col2, col3 = st.columns(3)
        with col1: amount = st.number_input("Kredi Tutarı", value=100000.0)
        with col2: rate_input = st.number_input("Aylık Faiz (%)", value=3.5)
        with col3: term = st.number_input("Vade (Ay)", value=12)
        submit = st.form_submit_button("Tabloyu Oluştur")
    if submit:
        P, r, n = amount, rate_input/100, int(term)
        pmt = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1) if r > 0 else P / n
        balance, total_int, data = P, 0, []
        for m in range(1, n + 1):
            interest = balance * r
            principal = pmt - interest
            balance -= principal
            if m == n and abs(balance) < 0.1: balance = 0
            total_int += interest
            data.append({"Ay": m, "Taksit": pmt, "Anapara": principal, "Faiz": interest, "Kalan": balance})
        st.divider()
        k1, k2, k3 = st.columns(3)
        k1.metric("Aylık Taksit", f"{pmt:,.2f}")
        k2.metric("Toplam Faiz", f"{total_int:,.2f}")
        k3.metric("Toplam Ödeme", f"{P+total_int:,.2f}")
        st.dataframe(pd.DataFrame(data).style.format("{:,.2f}"), use_container_width=True)

# ==========================================
# 9. KOMİSYON DAHİL MALİYET [YENİ]
# ==========================================
elif secim == "Komisyon Dahil Maliyet":
    st.title("💸 Komisyon Dahil Maliyet")
    st.markdown("Komisyonun işlem maliyetine ve efektif faize etkisini hesaplayın.")

    with st.form("comm_form"):
        c1, c2 = st.columns(2)
        amount = c1.number_input("İşlem Tutarı", value=100000.0, step=1000.0)
        days = c2.number_input("Vade (Gün)", value=90, step=1)
        
        c3, c4 = st.columns(2)
        rate = c3.number_input("Yıllık Faiz (%) [Bilgi Amaçlı]", value=45.0)
        comm_type = c4.selectbox("Komisyon Türü", ["Tutar", "Oran (%)"])
        
        comm_val = st.number_input("Komisyon Değeri", value=500.0)
        
        if st.form_submit_button("Hesapla"):
            if amount > 0 and days > 0:
                # Hesaplama
                if comm_type == "Tutar":
                    commission = comm_val
                else:
                    commission = amount * (comm_val / 100.0)
                
                total_cost = amount + commission
                # Efektif Yıllık Oran (Komisyonun yıllık maliyeti)
                effective_rate = (commission / amount) * (365.0 / days)
                
                st.divider()
                k1, k2 = st.columns(2)
                k1.metric("Toplam Maliyet", f"{total_cost:,.2f}", f"Komisyon: {commission:,.2f}", delta_color="inverse")
                k2.metric("Komisyonun Yıllık Maliyeti (Efektif)", f"%{effective_rate*100:.4f}", help="Sadece komisyonun yıllık faize denk gelen maliyeti.")
                
                if rate > 0:
                    st.info(f"ℹ️ Not: %{rate} faiz oranına ek olarak, komisyon size yıllık **+{effective_rate*100:.2f}%** ek maliyet yaratıyor.")
            else:
                st.error("Tutar ve gün sayısı 0'dan büyük olmalı.")

# ==========================================
# 10. EUROBOND
# ==========================================
elif secim == "Eurobond":
    def solve_ytm(price, cfs, times):
        try: return newton(lambda r: sum([c/((1+r)**t) for c,t in zip(cfs, times)]) - price, 0.05)
        except: return None

    st.title("💰 Eurobond Analizi")
    c1, c2 = st.columns([1, 2])
    with c1:
        settlement = st.date_input("Valör", datetime.date.today())
        maturity = st.date_input("Vade", datetime.date(2034, 2, 14))
        coupon = st.number_input("Kupon (%)", value=8.0)
        price_in = st.number_input("Fiyat", value=120.0)
    with c2:
        if settlement < maturity:
            freq = 2
            p_coupon = (coupon/100*100)/freq
            dates = []
            curr = maturity
            while curr > settlement:
                dates.append(curr)
                m = curr.month - 6
                y = curr.year
                if m <= 0: m+=12; y-=1
                try: curr = curr.replace(year=y, month=m)
                except: curr = curr.replace(year=y, month=m, day=28)
            dates = sorted(dates)
            if dates:
                accrued = (180 - (dates[0]-settlement).days)/180 * p_coupon
                if accrued < 0: accrued = 0
                dirty = price_in + accrued
                cfs = [p_coupon + (100 if d==maturity else 0) for d in dates]
                times = [(d-settlement).days/365 for d in dates]
                ytm = solve_ytm(dirty, cfs, times)
                st.metric("Kirli Fiyat", f"{dirty:.3f}")
                st.metric("YTM (Getiri)", f"%{ytm*100:.4f}" if ytm else "-")