import random
import streamlit as st

st.set_page_config(page_title="Suit Battle", page_icon="🪨✂️📄", layout="centered")

pilihan = {"Batu" : "🪨", "Gunting" : "✂️", "Kertas" : "📄"}

for kunci, nilai in {"skor_pemain" : 0, "skor_komputer" : 0, "hasil" : None, "popup" : False }.items():
    if kunci not in st.session_state:
        st.session_state[kunci] = nilai

def tentukan_pemenang(pemain, komputer):
    if pemain == komputer:
        return "seri"
    if (pemain, komputer) in [("Batu", "Gunting"), ("Gunting", "Kertas"), ("Kertas", "Batu")]:
        return "menang"
    return "kalah"

def main(nama):
    komputer = random.choice(list(pilihan.keys()))
    hasil = tentukan_pemenang(nama, komputer)
    
    if hasil == "menang":
        st.session_state.skor_pemain += 1
    elif hasil == "kalah":
        st.session_state.skor_komputer += 1
        
    st.session_state.hasil = {"pemain" : nama, "komputer" : komputer, "hasil" : hasil}
    st.session_state.popup = True

def reset():
    st.session_state.skor_pemain = 0
    st.session_state.skor_komputer = 0
    st.session_state.hasil = None

@st.dialog("🎮 Hasil Pertandingan")
def tampilkan_popup(data):
    kiri, kanan = st.columns(2)
    kiri.markdown(f"<h1 style='text-align:center'>{pilihan[data['pemain']]}</h1><p style='text-align:center'>Kamu</p>", unsafe_allow_html=True)
    kanan.markdown(f"<h1 style='text-align:center'>{pilihan[data['komputer']]}</h1><p style='text-align:center'>Komputer</p>", unsafe_allow_html=True)
    
    if data["hasil"] == "menang":
        st.success("Selamat kamu menang!")
        st.balloons()
    elif data["hasil"] == "kalah":
        st.error("Yah komputer menang")
        st.snow()
    else:
        st.info("Hasilnya seri!")
        
    if st.button("Main lagi", use_container_width=True):
        st.rerun()

st.title("Suit Battle 🪨✂️📄")
st.caption("Tantang komputer dalam permainan batu, gunting, kertas!")

col1, col2 = st.columns(2)
col1.metric("Skor kamu", st.session_state.skor_pemain)
col2.metric("Skor Komputer", st.session_state.skor_komputer)
st.divider()

st.subheader("Pilih jurusmu")
kolom = st.columns(3)
for i, nama in enumerate(pilihan):
    with kolom[i]: # Perbaikan: menggunakan indeks i agar tombol menyebar di 3 kolom
        st.markdown(f"<h1 style='text-align:center'>{pilihan[nama]}</h1>", unsafe_allow_html=True)
        st.button(nama, key=nama, use_container_width=True, on_click=main, args=(nama,))

if st.session_state.popup:
    st.session_state.popup = False
    tampilkan_popup(st.session_state.hasil)

st.divider()
st.button("Reset skor", use_container_width=True, on_click=reset)
st.caption("Suit Battle | Dibuat dengan Python dan Streamlit")

