import streamlit as st
from google import genai

# 1. SETUP HALAMAN
st.set_page_config(page_title="Global Lyrics Finder", page_icon="🎵", layout="centered")

# 2. CUSTOM CSS (Tema Gelap ala Spotify)
st.markdown("""
<style>
    .stApp { background-color: #121212; color: #FFFFFF; }
    h1, h2, p, label { color: #FFFFFF !important; }
    .stTextInput input { background-color: #282828 !important; color: white !important; border: 1px solid #1DB954 !important; }
    .stButton button { background-color: #1DB954 !important; color: white !important; font-weight: bold; border-radius: 20px; border: none; }
    .stButton button:hover { background-color: #1ed760 !important; }
    .result-box { background-color: #1E1E1E; padding: 20px; border-radius: 10px; margin-top: 20px; border-left: 5px solid #1DB954; white-space: pre-line; }
</style>
""", unsafe_allow_html=True)

# 3. HEADER APLIKASI
st.title("🎵 Global Lyrics Finder")
st.write("Mesin pencari lirik lagu dari artis dan genre apa saja di seluruh dunia.")
st.markdown("---")

# 4. AMBIL API KEY DARI BRANKAS
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("🔒 API Key belum dipasang di Streamlit Secrets!")
    st.stop()

# 5. KOLOM INPUT (Judul & Artis)
col1, col2 = st.columns(2)
with col1:
    judul = st.text_input("Judul Lagu:", placeholder="Contoh: Hati-Hati di Jalan")
with col2:
    artis = st.text_input("Nama Artis/Band:", placeholder="Contoh: Tulus")

# 6. TOMBOL PROSES
if st.button("🔍 Cari Lirik"):
    if judul and artis:
        with st.spinner("Mencari lirik...") :
            try:
                # Prompt yang dipersingkat: HANYA minta lirik
                prompt = f"""
                Berikan lirik lagu lengkap untuk lagu berjudul '{judul}' dari artis '{artis}'.
                ATURAN SANGAT PENTING: 
                - HANYA berikan teks liriknya saja. 
                - JANGAN berikan penjelasan, intro, arti, atau analisis apapun.
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Waduh, server Google lagi penuh. Coba klik tombolnya sekali lagi ya! Error detail: {e}")
    else:
        st.warning("⚠️ Isi dulu judul lagu dan nama artisnya ya!")
