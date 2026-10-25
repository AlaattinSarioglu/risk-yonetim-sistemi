import streamlit as st

# ==========================================
# --- ARKA PLAN ALGORİTMALARI ---
# ==========================================
def telegram_kasa_yonetimi(guncel_kasa, bahis_turu, adamin_bastigi, adamin_birimi, risk_modu):
    if adamin_birimi <= 0: return max(50, int(guncel_kasa * 0.01))
    
    if risk_modu == "🛡️ Muhafazakar (Güvenli)":
        temel_oran = 0.005
        canli_l, ozel_l, kombine_l = 0.01, 0.02, 0.05
    elif risk_modu == "⚖️ Dengeli (Önerilen)":
        temel_oran = 0.015
        canli_l, ozel_l, kombine_l = 0.03, 0.05, 0.10
    else:
        temel_oran = 0.03
        canli_l, ozel_l, kombine_l = 0.05, 0.10, 0.20
        
    bizim_birim = guncel_kasa * temel_oran  
    carpan = adamin_bastigi / adamin_birimi
    hesaplanan_tutar = bizim_birim * carpan
    
    if bahis_turu == "Canlı Bahis": maksimum_limit = guncel_kasa * canli_l  
    elif bahis_turu == "Özel Tekli": maksimum_limit = guncel_kasa * ozel_l  
    else: maksimum_limit = guncel_kasa * kombine_l  
        
    ham_tutar = min(hesaplanan_tutar, maksimum_limit)
    min_taban = max(50, int(guncel_kasa * 0.01))
    return max(int(round(ham_tutar, -1)), min_taban)

def bireysel_kasa_yonetimi(guncel_kasa, bahis_turu, oran, guven_puani, risk_modu):
    if risk_modu == "🛡️ Muhafazakar (Güvenli)":
        canli_l, ozel_l, kombine_l = 0.02, 0.03, 0.05
    elif risk_modu == "⚖️ Dengeli (Önerilen)":
        canli_l, ozel_l, kombine_l = 0.04, 0.06, 0.10
    else:
        canli_l, ozel_l, kombine_l = 0.08, 0.12, 0.20
        
    if bahis_turu == "Canlı Bahis": max_yuzde = canli_l  
    elif bahis_turu == "Özel Tekli": max_yuzde = ozel_l  
    else: max_yuzde = kombine_l  
    
    max_butce = guncel_kasa * max_yuzde
    oran_carpani = min(1.5 / oran if oran > 0 else 1, 1)
    
    algoritma_tutari = max_butce * oran_carpani
    guven_tutari = max_butce * (guven_puani / 10)
    
    min_taban = max(50, int(guncel_kasa * 0.01))
    alt_sinir = max(min_taban, int(round(min(algoritma_tutari, guven_tutari), -1)))
    ust_sinir = max(min_taban, int(round(max(algoritma_tutari, guven_tutari), -1)))
    return alt_sinir, ust_sinir

# ==========================================
# --- WEB ARAYÜZÜ (FRONTEND) ---
# ==========================================
st.set_page_config(page_title="RYS Pro Web", page_icon="📊", layout="wide")

# Hafıza Yönetimi
if 'guncel_kasa' not in st.session_state: st.session_state.guncel_kasa = 0.0
if 'adamin_birimi' not in st.session_state: st.session_state.adamin_birimi = 0.0
if 'bekleyen_kuponlar' not in st.session_state: st.session_state.bekleyen_kuponlar = []
if 'kupon_id' not in st.session_state: st.session_state.kupon_id = 1
if 'risk_modu' not in st.session_state: st.session_state.risk_modu = "⚖️ Dengeli (Önerilen)"

# Sol Menü (Silme derdi olmayan temiz metin kutuları)
with st.sidebar:
    st.title("⚙️ Sistem Ayarları")
    st.markdown("---")
    
    # Kullanıcıyı uğraştırmayan text_input yapısı (İçinde hazır sayı kalabalığı yok)
    girilen_kasa_str = st.text_input("Başlangıç Kasanız (TL)", value=str(int(st.session_state.guncel_kasa)) if st.session_state.guncel_kasa > 0 else "", placeholder="Örn: 5000")
    girilen_birim_str = st.text_input("Kanalın Standart Birimi (TL)", value=str(int(st.session_state.adamin_birimi)) if st.session_state.adamin_birimi > 0 else "", placeholder="Örn: 100")
    
    st.markdown("---")
    st.subheader("🎯 Risk Profili (Mod Seçimi)")
    secilen_mod = st.selectbox(
        "Kullanıcı Modu", 
        ["⚖️ Dengeli (Önerilen)", "🛡️ Muhafazakar (Güvenli)", "🔥 Agresif (Yüksek Kazanç)"],
        index=["⚖️ Dengeli (Önerilen)", "🛡️ Muhafazakar (Güvenli)", "🔥 Agresif (Yüksek Kazanç)"].index(st.session_state.risk_modu)
    )
    
    if st.button("Kasa Sistemini Başlat", type="primary", use_container_width=True):
        try:
            # Metin olarak girilen değerleri güvenle sayıya çeviriyoruz
            yeni_kasa = float(girilen_kasa_str.replace(",", "."))
            yeni_birim = float(girilen_birim_str.replace(",", "."))
            
            if yeni_kasa > 0 and yeni_birim > 0:
                st.session_state.guncel_kasa = yeni_kasa
                st.session_state.adamin_birimi = yeni_birim
                st.session_state.risk_modu = secilen_mod
                st.toast(f"✅ Kasa kuruldu! Kasa: {yeni_kasa} TL | Mod: {secilen_mod}")
                st.rerun()
            else:
                st.error("Lütfen 0'dan büyük geçerli sayılar girin.")
        except ValueError:
            st.error("Lütfen geçerli bir sayı giriniz (Örn: 5000).")

# Ana Ekran Başlığı
st.title("📊 Risk Yönetim Sistemi")
st.markdown(f"*Aktif Mod: **{st.session_state.risk_modu}** | Profesyonel İddaa Analiz ve Kasa Takibi*")

# Sekmeler
tab1, tab2 = st.tabs(["📊 Özet Paneli", "➕ Yeni Kupon Oyna"])

# Özet Paneli
with tab1:
    st.header("Sistem Özeti")
    col1, col2, col3 = st.columns(3)
    toplam_risk = sum(k['Risk Tutarı (TL)'] for k in st.session_state.bekleyen_kuponlar)
    
    col1.metric("💰 Güncel Kasa", f"{st.session_state.guncel_kasa:.2f} TL")
    col2.metric("⚠️ Masadaki Risk", f"{toplam_risk:.2f} TL")
    col3.metric("📝 Bekleyen Kupon", f"{len(st.session_state.bekleyen_kuponlar)}")
    
    st.markdown("---")
    st.subheader("Bekleyen Kuponlar Masası")
    
    if not st.session_state.bekleyen_kuponlar:
        st.info("Şu an bekleyen kuponunuz bulunmuyor. Lütfen sol menüden kasanızı kurup kupon ekleyin.")
    else:
        for k in st.session_state.bekleyen_kuponlar:
            st.markdown(f"🎫 **ID: {k['ID']}** | 🏆 **{k['Maç Adı']}** | Oran: {k['Oran']} | Risk: {k['Risk Tutarı (TL)']} TL | Kazanç: +{k['Kazanç (TL)']:.2f} TL")
        
        st.markdown("---")
        st.subheader("Kupon Sonuçlandır")
        sonuc_col1, sonuc_col2, sonuc_col3 = st.columns([2, 1, 1])
        secilen_id = sonuc_col1.selectbox("İşlem Yapılacak Kupon ID", [k['ID'] for k in st.session_state.bekleyen_kuponlar])
        
        if sonuc_col2.button("✅ Geldi (Kazandı)", use_container_width=True):
            for k in st.session_state.bekleyen_kuponlar:
                if k['ID'] == secilen_id:
                    st.session_state.guncel_kasa += k['Kazanç (TL)']
                    st.session_state.bekleyen_kuponlar.remove(k)
                    st.toast(f"Tebrikler! {k['Kazanç (TL)']} TL kasaya eklendi.")
                    st.rerun()
                    
        if sonuc_col3.button("❌ Yattı (Kaybetti)", use_container_width=True):
            for k in st.session_state.bekleyen_kuponlar:
                if k['ID'] == secilen_id:
                    st.session_state.bekleyen_kuponlar.remove(k)
                    st.toast("Geçmiş olsun, kupon masadan silindi.")
                    st.rerun()

# Kupon Oyna Sekmesi
with tab2:
    st.header("Kupon Yönetimi & Analiz")
    
    if st.session_state.guncel_kasa <= 0:
        st.warning("⚠️ Masaya kupon ekleyebilmek için lütfen önce sol menüden kasanızı kurun!")
    else:
        kupon_tab1, kupon_tab2 = st.tabs(["📲 Telegram Takip", "🧠 Bireysel Analiz"])
        
        with kupon_tab1:
            st.markdown(f"#### Telegram Kanal Verisi ile Risk ({st.session_state.risk_modu})")
            t_mac = st.text_input("🏆 Maç Adı (Örn: Galatasaray - Fenerbahçe)")
            t_tur = st.selectbox("Bahis Türü", ["Normal Kombine", "Canlı Bahis", "Özel Tekli"], key="t_tur")
            t_oran = st.number_input("📈 Oran", min_value=1.0, value=1.85, step=0.05, format="%.2f", key="t_oran")
            t_basilan = st.number_input("💵 Kanalın Bastığı Tutar (Birim)", min_value=0.0, value=100.0, step=10.0, format="%.0f", key="t_basilan")
            
            if st.button("🚀 Riski Hesapla ve Masaya Ekle", type="primary", use_container_width=True, key="t_btn"):
                if t_mac and t_oran > 0 and t_basilan > 0:
                    hesaplanan_tutar = telegram_kasa_yonetimi(st.session_state.guncel_kasa, t_tur, t_basilan, st.session_state.adamin_birimi, st.session_state.risk_modu)
                    kazanc = hesaplanan_tutar * t_oran
                    
                    st.session_state.guncel_kasa -= hesaplanan_tutar
                    st.session_state.bekleyen_kuponlar.append({
                        "ID": st.session_state.kupon_id,
                        "Maç Adı": t_mac,
                        "Oran": t_oran,
                        "Risk Tutarı (TL)": hesaplanan_tutar,
                        "Kazanç (TL)": kazanc
                    })
                    st.session_state.kupon_id += 1
                    st.toast(f"Başarılı! Risk: {hesaplanan_tutar} TL masaya eklendi.")
                    st.rerun()
                else:
                    st.error("Lütfen tüm alanları doğru doldurun.")
                    
        with kupon_tab2:
            st.markdown(f"#### Kendi Analiziniz ({st.session_state.risk_modu})")
            b_mac = st.text_input("🏆 Maç Adı", key="b_mac")
            b_tur = st.selectbox("Bahis Türü", ["Normal Kombine", "Canlı Bahis", "Özel Tekli"], key="b_tur_b")
            b_oran = st.number_input("📈 Oran", min_value=1.0, value=2.00, step=0.05, format="%.2f", key="b_oran_b")
            b_guven = st.slider("⭐ Güven Puanınız", min_value=1, max_value=10, value=5, key="b_guven")
            
            alt_limit, ust_limit = bireysel_kasa_yonetimi(st.session_state.guncel_kasa, b_tur, b_oran, b_guven, st.session_state.risk_modu)
            st.info(f"💡 **Sistemin Bütçe Önerisi:** {alt_limit} TL - {ust_limit} TL")
            
            b_oynanacak = st.number_input("Ne kadar basmak istersiniz? (TL)", min_value=0.0, value=float(alt_limit), step=10.0, format="%.0f", key="b_oynanacak")
            
            if st.button("🚀 Bireysel Kuponu Masaya Ekle", type="primary", use_container_width=True, key="b_ekle"):
                if b_mac and b_oran > 0 and b_oynanacak > 0:
                    kazanc = b_oynanacak * b_oran
                    
                    st.session_state.guncel_kasa -= b_oynanacak
                    st.session_state.bekleyen_kuponlar.append({
                        "ID": st.session_state.kupon_id,
                        "Maç Adı": b_mac,
                        "Oran": b_oran,
                        "Risk Tutarı (TL)": b_oynanacak,
                        "Kazanç (TL)": kazanc
                    })
                    st.session_state.kupon_id += 1
                    st.toast(f"Bireysel kupon eklendi! Risk: {b_oynanacak} TL")
                    st.rerun()
                else:
                    st.error("Lütfen tüm alanları doldurun.")