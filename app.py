import streamlit as st
import requests

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="SAY IT, PLAY IT!", 
    page_icon="🎙️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CACHING DATA (Solusi agar tidak lambat/loading terus)
@st.cache_data(ttl=3600)  # Data disimpan di memori selama 1 jam
def get_photos_from_github(folder_path):
    username = "andrey-creator"
    repo = "say-it-play-it"
    url = f"https://api.github.com/repos/{username}/{repo}/contents/photos/{folder_path}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            files = response.json()
            # Filter hanya file gambar
            image_urls = [file['download_url'] for file in files if file['name'].lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]
            return image_urls
    except Exception as e:
        return []
    return []

# 3. INISIALISASI STATE
if 'menu_pilihan' not in st.session_state:
    st.session_state.menu_pilihan = 'Home'
if 'sub_menu_galeri' not in st.session_state:
    st.session_state.sub_menu_galeri = None

# 4. CSS UNTUK INTERFACE PREMIUM
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');
    
    .main { background-color: #05070a; }
    
    .header-container { text-align: center; padding: 20px 0; }
    .logo-img { width: 100px; filter: invert(1) drop-shadow(0 0 12px #00f2ff); border-radius: 50%; }
    .glow-text {
        font-family: 'Orbitron', sans-serif;
        color: white;
        text-shadow: 0 0 10px #00f2ff;
        font-size: 2.5rem;
        margin: 10px 0 0 0;
    }
    .sub-text {
        font-family: 'Rajdhani', sans-serif;
        color: #00f2ff;
        letter-spacing: 4px;
        font-size: 1rem;
        margin-bottom: 30px;
    }

    /* Tombol Style */
    div.stButton > button {
        transition: all 0.3s ease;
        border: 1px solid #00f2ff !important;
        background-color: transparent;
        color: white;
        font-family: 'Orbitron', sans-serif;
        border-radius: 10px;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 15px #00f2ff !important;
        transform: translateY(-2px);
        background-color: #00f2ff !important;
        color: black !important;
    }

    /* Label Gambar */
    .img-label {
        text-align: center; 
        font-family: 'Rajdhani', sans-serif; 
        color: #00f2ff; 
        font-size: 0.85rem; 
        margin-top: -10px; 
        margin-bottom: 25px;
        letter-spacing: 1px;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI NAVIGASI ---
def set_page(name):
    st.session_state.menu_pilihan = name
    st.session_state.sub_menu_galeri = None

# --- SIDEBAR & HEADER LOGIC ---
if st.session_state.menu_pilihan == 'Home':
    st.markdown("<style>[data-testid='stSidebar'], [data-testid='collapsedControl'], header {display: none; visibility: hidden;}</style>", unsafe_allow_html=True)

st.markdown(f"""
    <div class="header-container">
        <img src="https://raw.githubusercontent.com/andrey-creator/say-it-play-it/main/logo_ec.jpeg" class="logo-img">
        <h1 class="glow-text">ENGLISH CLUB</h1>
        <p class="sub-text">ENGLISH CLUB • SMAN 1 DEPOK</p>
    </div>
    """, unsafe_allow_html=True)

# --- HALAMAN UTAMA ---
if st.session_state.menu_pilihan == 'Home':
    _, col_center, _ = st.columns([1, 2, 1])
    with col_center:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🖼️\n\nGALERI EC", key="btn_galeri", use_container_width=True):
                set_page('Galeri')
                st.rerun()
        with c2:
            if st.button("🎵\n\nREQUEST SONG", key="btn_req", use_container_width=True):
                set_page('Request')
                st.rerun()
        
        c3, c4 = st.columns(2)
        with c3:
            if st.button("📜\n\nQUEUE", key="btn_queue", use_container_width=True):
                set_page('Queue')
                st.rerun()
        with c4:
            if st.button("💬\n\nFEEDBACK", key="btn_feed", use_container_width=True):
                set_page('Feedback')
                st.rerun()

# --- HALAMAN REQUEST & FEEDBACK (IFRAME) ---
elif st.session_state.menu_pilihan in ['Request', 'Feedback']:
    _, cb, _ = st.columns([2, 1, 2])
    with cb: 
        if st.button("⬅️ DASHBOARD"): set_page('Home'); st.rerun()
    
    url_form = "https://docs.google.com/forms/d/e/1FAIpQLSel5biF_8tox1dWjFDwHUdyvgJ7Wq1LeCMsmKGeACCR4zxgbQ/viewform" if st.session_state.menu_pilihan == 'Request' else "https://docs.google.com/forms/d/e/1FAIpQLSe78jlTfLisNf0eukcchESd9Ti9P25ATij1CHX5mhDx49iMxQ/viewform"
    
    st.write("##")
    _, col_form, _ = st.columns([1, 6, 1])
    with col_form:
        st.components.v1.iframe(f"{url_form}?embedded=true", height=800, scrolling=True)

# --- HALAMAN GALERI ---
elif st.session_state.menu_pilihan == 'Galeri':
    _, cb, _ = st.columns([2, 1, 2])
    with cb: 
        if st.button("⬅️ DASHBOARD"): set_page('Home'); st.rerun()
    
    st.markdown("<h2 style='text-align:center; color:#00f2ff; font-family:Orbitron;'>GALERI</h2>", unsafe_allow_html=True)

    if st.session_state.sub_menu_galeri is None:
        _, col_galeri, _ = st.columns([1, 2, 1])
        with col_galeri:
            g1, g2 = st.columns(2)
            with g1:
                if st.button("👥\n\nINTEGRAL MEMBER", use_container_width=True):
                    st.session_state.sub_menu_galeri = "integral-member"
                    st.rerun()
            with g2:
                if st.button("📸\n\nACTIVITY", use_container_width=True):
                    st.session_state.sub_menu_galeri = "activity"
                    st.rerun()
    else:
        if st.button("⬅️ BACK TO CATEGORIES"):
            st.session_state.sub_menu_galeri = None
            st.rerun()
            
        with st.spinner("Accessing Database..."):
            images = get_photos_from_github(st.session_state.sub_menu_galeri)
        
        if images:
            cols = st.columns(3)
            for idx, img_url in enumerate(images):
                # Ekstrak nama file tanpa ekstensi
                file_name = img_url.split('/')[-1].split('.')[0]
                clean_name = file_name.replace('-', ' ').replace('_', ' ').upper()

                with cols[idx % 3]: 
                    st.image(img_url, use_container_width=True)
                    st.markdown(f'<p class="img-label">{clean_name}</p>', unsafe_allow_html=True)
        else:
            st.warning("No files found.")

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<p style='font-family:Orbitron; color:#00f2ff; font-size:0.7rem;'>CONTROL STATION</p>", unsafe_allow_html=True)
    if st.button("REBOOT"): set_page('Home'); st.rerun()
    st.markdown("---")
    with st.expander("ADMIN"):
        pw = st.text_input("ACCESS CODE", type="password")
        if pw == "AndreEC2026":
            st.link_button("DATABASE", "https://docs.google.com/spreadsheets/d/13a0SStLqMqXMO8fgUImPyMI8jhSEMMQJTE7hQSIYInY/edit?gid=1587199457#gid=1587199457", use_container_width=True)