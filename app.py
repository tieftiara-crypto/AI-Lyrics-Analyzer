import streamlit as st
from google import genai
from google.genai import types

# 1. SETUP HALAMAN
st.set_page_config(page_title="AI Lyrics Analyzer", page_icon="🎵", layout="centered")

# 2. CUSTOM CSS (Tema Gelap ala Spotify)
st.markdown("""
<style>
    .stApp { background-color: #121212; color: #FFFFFF; }
    h1, h2, h3, p, label { color: #FFFFFF !important; }
    .stTextInput input { background-color: #282828 !important; color: white !important; border: 1px solid #1DB954 !important; }
    .stButton button { background-color: #1DB954 !important; color: white !important; font-weight: bold; border-radius: 20px; border: none; }
    .stButton button:hover { background-color: #1ed760 !important; }
    .result-box { background-color: #1E1E1E; padding: 20px; border-radius: 10px; margin-top: 20px; border-left: 5px solid #1DB954; }
</style>
""", unsafe_allow_html=True)

# 3. HEADER APLIKASI
st.title("🎵 AI Lyrics & Meaning Analyzer")
st.write("Cari lirik lagu dari genre apa saja, dan biarkan AI membedah makna filosofis serta fakta unik di baliknya!")
st.markdown("---")

# 4. AMBIL API KEY DARI BRANKAS
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("🔒 API Key belum dipasang di Streamlit Secrets! Tambahkan dulu di pengaturan dashboard Streamlit.")
    st.stop()

# 5. KOLOM INPUT (Judul & Artis)
col1, col2 = st.columns(2)
with col1:
    judul = st.text_input("Judul Lagu:", placeholder="Contoh: Hati-Hati di Jalan")
with col2:
    artis = st.text_input("Nama Artis/Band:", placeholder="Contoh: Tulus")

# 6. TOMBOL PROSES
if st.button("🔍 Cari Lirik & Bedah Makna"):
    if judul and artis:
        with st.spinner(f"AI sedang mendengarkan dan menganalisis lagu '{judul}'...") :
            try:
                # Prompt Engineering Khusus Pakar Musik
                prompt = f"""
                Kamu adalah seorang pakar musik dan kritikus seni tingkat dunia.
                Tolong berikan informasi komprehensif untuk lagu '{judul}' oleh '{artis}':
                
                1. 🎤 **Lirik Lengkap**: Tuliskan lirik lagu aslinya secara utuh (jangan dipotong).
                2. 🧠 **Bedah Makna**: Berikan analisis mendalam tentang apa arti sebenarnya, pesan tersembunyi, atau cerita di balik lagu ini.
                3. 💡 **Fakta Menarik**: Sebutkan 2-3 fakta unik tentang proses pembuatan lagu ini, inspirasinya, atau pencapaian rekornya.
                4. 🎧 **Genre & Vibe**: Sebutkan genre utama dan mood (suasana emosional) dari lagu ini.
                
                Sajikan dengan format yang rapi.
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.success("🎉 Berhasil dianalisis!")
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Waduh, gagal menganalisis: {e}")
    else:
        st.warning("⚠️ Isi dulu judul lagu dan nama artisnya ya biar AI-nya nggak bingung!")
