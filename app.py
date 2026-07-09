import streamlit as st
from google import genai
from google.genai import types

# 1. SETUP HALAMAN
st.set_page_config(page_title="Global Lyrics Finder", page_icon="🎵", layout="centered")

# 2. CUSTOM CSS
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
st.write("Mesin pencari lirik lagu dari artis dan genre apa saja. Dilengkapi dengan **Google Search Grounding** agar lirik 100% akurat dan anti-ngarang.")
st.markdown("---")

# 4. AMBIL API KEY
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("🔒 API Key belum dipasang di Streamlit Secrets!")
    st.stop()

# 5. KOLOM INPUT
col1, col2 = st.columns(2)
with col1:
    judul = st.text_input("Judul Lagu:", placeholder="Contoh: Rayuan Perempuan Gila")
with col2:
    artis = st.text_input("Nama Artis/Band:", placeholder="Contoh: Nadin Amizah")

# 6. TOMBOL PROSES
if st.button("🔍 Cari Lirik"):
    if judul and artis:
        with st.spinner("AI sedang browsing internet nyari lirik aslinya...") :
            try:
                # Perintah yang ditegaskan
                prompt = f"""
                Cari lirik lagu asli untuk '{judul}' dari '{artis}' di internet. 
                ATURAN MUTLAK:
                1. Kamu TIDAK BOLEH mengarang lirik.
                2. HANYA berikan teks liriknya saja dari awal sampai akhir.
                3. Jangan berikan intro, penjelasan, atau teks tambahan apapun.
                """
                
                # INI KUNCI RAHASIANYA: NGASIH AKSES GOOGLE SEARCH KE AI
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[{"google_search": {}}]  # <--- Fitur Anti-Ngarang (Search Grounding)
                    )
                )
                
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Waduh, server Google lagi sibuk nih. Coba klik lagi! Error: {e}")
    else:
        st.warning("⚠️ Isi dulu judul lagu dan nama artisnya ya!")
