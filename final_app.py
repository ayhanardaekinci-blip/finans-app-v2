import streamlit as st
import pandas as pd
import numpy as np

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Finans Pro Ultimate",
    page_icon="💸",
    layout="centered"
)

# --- TASARIM DÜZELTME (SİYAH YAZI GARANTİSİ) ---
st.markdown("""
<style>
    div.stButton > button:first-child {
        height: 4em;
        width: 100%;
        font-size: 16px;
        font-weight: bold;
        border-radius: 12px;
        
        /* ÖNEMLİ: Arka plan Beyaz, Yazı Siyah olsun */
        background-color: #ffffff !important; 
        color: #000000 !important; 
        border: 2px solid #e0e0e0;
        
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        /* Üstüne gelince Kırmızı/Beyaz olsun */
        border-color: #ff4b4b;
        color: #ff4b4b !important;
        background-color: #fff0f0 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- OTURUM YÖNETİMİ ---
if 'page' not in st.session_state:
    st.session_state.page = "Ana Sayfa"
if 'sub_mode' not in st.session_state:
    st.session_state.sub_mode = "Varsayilan"

def git(sayfa, mod="Varsayilan"):
    st.session_state.page = sayfa
    st.session_state.sub_mode = mod
    st.rerun()

# --- YAN MENÜ ---
with st.sidebar:
    st.title("📂 Menü")
    if st.button("🏠 Ana Sayfa"): git("Ana Sayfa")
    st.write("---")
    st.caption("NAKİT YÖNETİMİ")
    if st.button("💰 Mevduat Getirisi"): git("Nakit", "Mevduat")
    if st.button("💳 Kredi Hesapla"): git("Nakit", "Kredi")
    st.caption("YATIRIM ARAÇLARI")
    if st.button("📄 Bono (İskonto)"): git("Yatırım", "Bono")
    if st.button("📜 Tahvil (Kuponlu)"): git("Yatırım", "Tahvil")
    if st.button("🌍 Eurobond Vergi"): git("Yatırım", "Eurobond")
    st.caption("TİCARİ")
    if st.button("📊 POS / Komisyon"): git("Ticari", "Komisyon")
    
# ==========================================
# 1. ANA SAYFA (9'LU VİTRİN)
# ==========================================
if st.session_state.page == "Ana Sayfa":
    st.markdown("<h1 style='text-align: center;'>Finansal Kontrol Paneli</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Hızlı işlem menüsü</p>", unsafe_allow_html=True)
    st.write("") 

    # 1. SATIR
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("💰\nMevduat Getirisi"): git("Nakit", "Mevduat")
    with c2:
        if st.button("💳\nKredi Planı"): git("Nakit", "Kredi")
    with c3:
        if st.button("📊\nPOS Komisyon"): git("Ticari", "Komisyon")

    # 2. SATIR
    c4, c5, c6 = st.columns(3)
    with c4:
        if st.button("📄\nBono (Hazine)"): git("Yatırım", "Bono")
    with c5:
        if st.button("📜\nTahvil (Özel)"): git("Yatırım", "Tahvil")
    with c6:
        if st.button("🌍\nEurobond Vergi"): git("Yatırım", "Eurobond")

    # 3. SATIR
    c7, c8, c9 = st.columns(3)
    with c7:
        if st.button("📉\nİskonto Hesabı"): git("Yatırım", "Bono")
    with c8:
        if st.button("💱\nNetten Brüte"): git("Ticari", "Komisyon")
    with c9:
        st.button("⚙️\nAyarlar", disabled=True)

    st.write("---")
    st.info("💡 İpucu: Sol menüden veya yukarıdaki kartlardan istediğiniz modüle direkt geçiş yapabilirsiniz.")

# ==========================================
# 2. NAKİT SAYFASI
# ==========================================
elif st.session_state.page == "Nakit":
    st.title("Nakit Akışı Yönetimi")
    
    tabs = st.tabs(["💰 Mevduat Getirisi", "💳 Kredi Ödeme Planı"])
    
    # Seçime göre sekmeyi aktif yapma mantığı eklenebilir ama 
    # Streamlit'te tab'leri programla açmak için st.tabs yapısı sabittir.
    # Kullanıcı doğru tab'e manuel tıklar.

    with tabs[0]:
        st.header("Mevduat Faizi Hesapla")
        col1, col2 = st.columns(2)
        with col1:
            ana_para = st.number_input("Ana Para (TL)", value=100000.0, step=1000.0, key="mev_ana")
            faiz = st.number_input("Faiz Oranı (%)", value=45.0, key="mev_faiz")
        with col2:
            gun = st.number_input("Gün Sayısı", value=32, key="mev_gun")
            stopaj = st.number_input("Stopaj (%)", value=5.0, key="mev_stop")
        
        if st.button("Hesapla (Mevduat)", type="primary"):
            brut = (ana_para * faiz * gun) / 36500
            net = brut * (1 - stopaj/100)
            st.success(f"Net Getiri: {net:,.2f} TL")
            st.info(f"Toplam Bakiye: {ana_para + net:,.2f} TL")

    with tabs[1]:
        st.header("Kredi Geri Ödeme Planı")
        col1, col2 = st.columns(2)
        with col1:
            kredi_tutar = st.number_input("Kredi Tutarı", value=100000.0, key="krd_tut")
            vade = st.number_input("Taksit Sayısı", value=12, key="krd_vad")
        with col2:
            aylik_faiz = st.number_input("Aylık Faiz (%)", value=3.5, key="krd_faiz")
            
        if st.button("Plan Oluştur", type="primary"):
            i = aylik_faiz / 100
            if i == 0: taksit = kredi_tutar / vade
            else: taksit = kredi_tutar * (i * (1+i)**vade) / ((1+i)**vade - 1)
            st.metric("Aylık Taksit Tutarınız", f"{taksit:,.2f} TL")
            
            plan = []
            kalan = kredi_tutar
            for d in range(1, int(vade)+1):
                f_pay = kalan * i
                a_pay = taksit - f_pay
                kalan -= a_pay
                plan.append({"Taksit": d, "Ödeme": taksit, "Anapara": a_pay, "Faiz": f_pay, "Kalan": max(0, kalan)})
            st.dataframe(pd.DataFrame(plan).style.format("{:,.2f}"))

# ==========================================
# 3. YATIRIM SAYFASI
# ==========================================
elif st.session_state.page == "Yatırım":
    st.title("Yatırım Araçları")
    tabs = st.tabs(["📄 Bono & Tahvil", "🌍 Eurobond Vergi"])

    with tabs[0]:
        st.header("Bono ve Tahvil Fiyatlama")
        tur = st.radio("Kağıt Türü Seçiniz:", ["İskontolu Bono (Hazine)", "Kuponlu Tahvil (Özel Sektör)"], horizontal=True)
        c1, c2 = st.columns(2)
        with c1:
            nominal = st.number_input("Nominal Değer", value=100.0, key="bon_nom")
            basit_faiz = st.number_input("Basit Faiz / Piyasa (%)", value=40.0, key="bon_faiz")
        with c2:
            gun = st.number_input("Vadeye Kalan Gün", value=90, key="bon_gun")
        if tur == "Kuponlu Tahvil (Özel Sektör)":
            kupon_faiz = st.number_input("Kupon Faizi (%)", value=10.0)

        if st.button("Fiyatı Hesapla", type="primary"):
            if tur == "İskontolu Bono (Hazine)":
                fiyat = nominal / (1 + (basit_faiz/100)*(gun/365))
                st.metric("Bono Fiyatı", f"{fiyat:,.4f} TL")
            else:
                fiyat = (nominal * (1 + kupon_faiz/100)) / (1 + (basit_faiz/100) * (gun/365))
                st.metric("Tahvil Fiyatı (Yaklaşık)", f"{fiyat:,.4f} TL")

    with tabs[1]:
        st.header("Eurobond Gelir Vergisi Analizi")
        gelir = st.number_input("Yıllık Toplam Kupon Geliri ($)", value=6000.0, key="eu_gel")
        kur = st.number_input("Ortalama Dolar Kuru", value=34.5, key="eu_kur")
        sinir = 150000 
        if st.button("Vergi Kontrolü Yap", type="primary"):
            tl_karsilik = gelir * kur
            st.write(f"💵 TL Karşılığı: **{tl_karsilik:,.2f} TL**")
            if tl_karsilik > sinir:
                st.error("⚠️ Sınır aşıldı! Beyanname vermeniz gerekir.")
            else:
                st.success("✅ Sınırın altındasınız. Beyanname gerekmez.")

# ==========================================
# 4. TİCARİ SAYFASI
# ==========================================
elif st.session_state.page == "Ticari":
    st.title("Ticari Hesaplamalar")
    st.header("POS Komisyonu ve Maliyet")
    col1, col2 = st.columns(2)
    with col1:
        tutar = st.number_input("Çekim Tutarı (TL)", value=1000.0, key="pos_tut")
    with col2:
        komisyon = st.number_input("Komisyon Oranı (%)", value=2.99, key="pos_kom")
    if st.button("Hesapla", type="primary"):
        kesinti = tutar * (komisyon/100)
        net = tutar - kesinti
        c1, c2, c3 = st.columns(3)
        c1.metric("Müşteriden", f"{tutar:,.2f} TL")
        c2.metric("Kesinti", f"{kesinti:,.2f} TL", delta_color="inverse")
        c3.metric("Net Geçen", f"{net:,.2f} TL")
