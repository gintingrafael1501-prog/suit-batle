import random
import streamlit as st

st.set_page_config(page_title="Tactical Gun Duel", page_icon="⚔️", layout="centered")

# Mengatur emoji aksi dasar
emoji_aksi = {
    "Kokang": "🔌",
    "Shield": "🛡️",
    "Tembak": "🔫"
}

# Inisialisasi State Game
for kunci, nilai in {
    "peluru_pemain": 0,
    "peluru_komputer": 0,
    "hasil_duel": None,
    "popup": False
}.items():
    if kunci not in st.session_state:
        st.session_state[kunci] = nilai

def tentukan_pemenang(p_aksi, p_lv, k_aksi, k_lv):
    """Menentukan status pertempuran ronde ini."""
    if p_aksi == "Tembak":
        if k_aksi == "Tembak":
            if p_lv > k_lv: return "menang_tembus"
            elif k_lv > p_lv: return "kalah_tembus"
            else: return "seri_tabrakan"
        elif k_aksi == "Shield":
            if p_lv > k_lv: return "menang_jebol"
            else: return "tahan"
        else:
            return "menang_telak"
            
    elif k_aksi == "Tembak":
        if p_aksi == "Shield":
            if k_lv > p_lv: return "kalah_jebol"
            else: return "tahan"
        else:
            return "kalah_telak"
            
    return "aman"

def main_ronde(aksi_pemain, level_pemain):
    # 1. AI Komputer Memilih Aksi
    pilihan_komputer = ["Kokang", "Shield"]
    if st.session_state.peluru_komputer >= 1:
        pilihan_komputer.append("Tembak")
    aksi_komputer = random.choice(pilihan_komputer)
    
    # Tentukan level acak 1-4 untuk komputer
    level_komputer = random.randint(1, 4) if aksi_komputer != "Kokang" else 0
    
    # 2. Update Peluru
    if aksi_pemain == "Kokang": st.session_state.peluru_pemain += 1
    elif aksi_pemain == "Tembak": st.session_state.peluru_pemain -= level_pemain
        
    if aksi_komputer == "Kokang": st.session_state.peluru_komputer += 1
    elif aksi_komputer == "Tembak": st.session_state.peluru_komputer -= level_komputer

    # 3. Hitung Hasil
    hasil = tentukan_pemenang(aksi_pemain, level_pemain, aksi_komputer, level_komputer)
    
    # Olah pesan teks hasil untuk popup
    detail_teks = "Sama-sama aman!"
    status_akhir = "lanjut"
    
    if hasil == "menang_telak" or hasil == "menang_tembus" or hasil == "menang_jebol":
        status_akhir = "menang"
    elif hasil == "kalah_telak" or hasil == "kalah_tembus" or hasil == "kalah_jebol":
        status_akhir = "kalah"
    elif hasil == "seri_tabrakan":
        status_akhir = "seri_mati"
        
    if hasil == "menang_telak": detail_teks = "Kamu menembak komputer saat sedang kokang!"
    elif hasil == "menang_tembus": detail_teks = f"Peluru Lv {level_pemain} kamu menembus Peluru Lv {level_komputer} komputer!"
    elif hasil == "menang_jebol": detail_teks = f"Tembakan Lv {level_pemain} kamu menjebol Shield Lv {level_komputer} komputer!"
    elif hasil == "kalah_telak": detail_teks = "Komputer menembakmu saat kamu sedang kokang!"
    elif hasil == "kalah_tembus": detail_teks = f"Peluru Lv {level_komputer} komputer menembus Peluru Lv {level_pemain} kamu!"
    elif hasil == "kalah_jebol": detail_teks = f"Tembakan Lv {level_komputer} komputer menjebol Shield Lv {level_pemain} kamu!"
    elif hasil == "seri_tabrakan": detail_teks = "Kedua peluru bertabrakan dan meledak bersamaan!"
    elif hasil == "tahan": detail_teks = "Tembakan berhasil ditahan oleh tameng!"

    st.session_state.hasil_duel = {
        "p_aksi": aksi_pemain, "p_lv": level_pemain,
        "k_aksi": aksi_komputer, "k_lv": level_komputer,
        "status": status_akhir, "detail": detail_teks
    }
    st.session_state.popup = True

def reset():
    st.session_state.peluru_pemain = 0
    st.session_state.peluru_komputer = 0
    st.session_state.hasil_duel = None

@st.dialog("🎮 Hasil Duel")
def tampilkan_popup(data):
    kiri, kanan = st.columns(2)
    txt_p = f"{emoji_aksi[data['p_aksi']]} Lv {data['p_lv']}" if data['p_lv'] > 0 else emoji_aksi[data['p_aksi']]
    txt_k = f"{emoji_aksi[data['k_aksi']]} Lv {data['k_lv']}" if data['k_lv'] > 0 else emoji_aksi[data['k_aksi']]
    
    kiri.markdown(f"<h1 style='text-align:center'>{txt_p}</h1><p style='text-align:center'>Kamu</p>", unsafe_allow_html=True)
    kanan.markdown(f"<h1 style='text-align:center'>{txt_k}</h1><p style='text-align:center'>Komputer</p>", unsafe_allow_html=True)
    
    st.write(f"**Info:** {data['detail']}")
    
    if data["status"] == "menang":
        st.success("Selamat kamu menang duel!")
        st.balloons()
    elif data["status"] == "kalah":
        st.error("Yah kamu kalah tertembak!")
        st.snow()
    elif data["status"] == "seri_mati":
        st.warning("Kalian berdua kalah bersamaan!")
    else:
        st.info("Pertempuran masih berlanjut!")
        
    if st.button("Lanjut Ronde", use_container_width=True):
        if data["status"] in ["menang", "kalah", "seri_mati"]:
            reset()
        st.rerun()

# TAMPILAN UTAMA (Simpel & Minimalis)
st.title("⚔️ Tactical Gun Duel")
st.caption("Kumpulkan peluru, atur level tameng, dan tembak komputer!")

col1, col2 = st.columns(2)
col1.metric("Peluru kamu", st.session_state.peluru_pemain)
col2.metric("Peluru Komputer", st.session_state.peluru_komputer)
st.divider()

st.subheader("Pilih jurusmu")
kolom = st.columns(3)

# Kolom 1: Kokang
with kolom[0]:
    st.markdown(f"<h1 style='text-align:center'>{emoji_aksi['Kokang']}</h1>", unsafe_allow_html=True)
    st.button("Kokang", key="btn_kokang", use_container_width=True, on_click=main_ronde, args=("Kokang", 0))

# Kolom 2: Shield (Pilihan Level lewat Selectbox agar simpel)
with kolom[1]:
    st.markdown(f"<h1 style='text-align:center'>{emoji_aksi['Shield']}</h1>", unsafe_allow_html=True)
    lv_s = st.selectbox("Pilih Level Shield", [1, 2, 3, 4], key="sel_s", label_visibility="collapsed")
    st.button(f"Shield Lv {lv_s}", key="btn_shield", use_container_width=True, on_click=main_ronde, args=("Shield", lv_s))

# Kolom 3: Tembak
with kolom[2]:
    st.markdown(f"<h1 style='text-align:center'>{emoji_aksi['Tembak']}</h1>", unsafe_allow_html=True)
    lv_t = st.selectbox("Pilih Level Tembak", [1, 2, 3, 4], key="sel_t", label_visibility="collapsed")
    
    # Tombol mati/terkunci otomatis jika peluru tidak mencukupi level tembakan yang dipilih
    bisa_nembak = st.session_state.peluru_pemain >= lv_t
    st.button(f"Tembak Lv {lv_t}", key="btn_tembak", use_container_width=True, disabled=not bisa_nembak, on_click=main_ronde, args=("Tembak", lv_t))

if st.session_state.popup:
    st.session_state.popup = False
    tampilkan_popup(st.session_state.hasil_duel)

st.divider()
st.button("Reset Game", use_container_width=True, on_click=reset)
