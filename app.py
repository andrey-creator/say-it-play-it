import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(page_title="SAY IT, PLAY IT!", page_icon="🎙️", layout="wide")

# 2. CSS untuk Estetika Modern, Musik, dan Logo
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500&display=swap');
    
    .main {
        background-color: #0e1117;
    }
    
    /* Center Logo */
    .logo-container {
        display: flex;
        justify-content: center;
        padding: 10px;
    }
    .logo-img {
        width: 150px;
        filter: drop-shadow(0 0 10px rgba(0, 242, 255, 0.5));
    }

    .glow-text {
        font-family: 'Orbitron', sans-serif;
        color: #00f2ff;
        text-shadow: 0 0 12px #00f2ff;
        text-align: center;
        font-size: 2.5rem;
        margin-top: 10px;
    }

    /* Efek Animasi Musik Halus */
    .music-bar {
        display: inline-block;
        width: 3px;
        height: 15px;
        background: #00f2ff;
        margin: 0 2px;
        animation: equalizer 1s ease-in-out infinite;
    }
    @keyframes equalizer {
        0%, 100% { height: 10.5px; }
        50% { height: 25px; }
    }
    
    .bar-1 { animation-delay: 0.1s; }
    .bar-2 { animation-delay: 0.3s; }
    .bar-3 { animation-delay: 0.2s; }

    /* Container Iframe */
    .stIframe {
        border: 1px solid rgba(0, 242, 255, 0.3);
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BAGIAN ATAS (LOGO & JUDUL) ---
st.markdown(f"""
    <div class="logo-container">
        <img src="https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/say-it-play-it/main/logo_ec.jpg" class="logo-img">
    </div>
    <div style="text-align:center;">
        <span class="music-bar bar-1"></span>
        <span class="music-bar bar-2"></span>
        <span class="music-bar bar-3"></span>
        <span style="font-family:'Rajdhani'; color:white; font-size:1.2rem; vertical-align:super; margin: 0 15px;"> 
            NOW BROADCASTING 
        </span>
        <span class="music-bar bar-3"></span>
        <span class="music-bar bar-2"></span>
        <span class="music-bar bar-1"></span>
    </div>
    <h1 class="glow-text">SAY IT, PLAY IT!</h1>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#00f2ff; font-family:Orbitron;'>STATION CONTROL</h2>", unsafe_allow_html=True)
    page = st.radio("MENU", ["🛰️ TRANSMIT REQUEST", "🛡️ COMMAND CENTER"])
    st.markdown("---")
    st.write("Status: 🟢 **Operational**")
    st.write("Vibe: 🎵 **Chilled English Club**")

# --- KONTEN UTAMA ---
if page == "🛰️ TRANSMIT REQUEST":
    st.markdown("<p style='text-align:center; color:gray;'>Fill the frequency below to send your request.</p>", unsafe_allow_html=True)
    
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSel5biF_8tox1dWjFDwHUdyvgJ7Wq1LeCMsmKGeACCR4zxgbQ/viewform?embedded=true"
    st.components.v1.iframe(form_url, height=800, scrolling=True)

else:
    st.markdown("<h2 style='color:#00f2ff; font-family:Orbitron;'>🛡️ COMMAND CENTER</h2>", unsafe_allow_html=True)
    password = st.text_input("AUTHORIZATION CODE", type="password")
    
    if password == "AndreEC2026":
        st.success("Welcome, King Andre.")
        sheet_url = "https://docs.google.com/spreadsheets/d/13a0SStLqMqXMO8fgUImPyMI8jhSEMMQJTE7hQSIYInY/edit?gid=1587199457#gid=1587199457"
        st.link_button("🚀 OPEN DATABASE", sheet_url)
    elif password:
        st.error("ACCESS DENIED.")