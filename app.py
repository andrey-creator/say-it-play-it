import streamlit as st
import requests
from urllib.parse import unquote

st.set_page_config(
    page_title="SAY IT, PLAY IT!", 
    page_icon="🎙️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_data(ttl=3600)
def get_photos_from_github(folder_path):
    username = "andrey-creator"
    repo = "say-it-play-it"
    url = f"https://api.github.com/repos/{username}/{repo}/contents/photos/{folder_path}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            files = response.json()
            image_urls = [file['download_url'] for file in files if file['name'].lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]
            return image_urls
    except Exception as e:
        return []
    return []

if 'menu_pilihan' not in st.session_state:
    st.session_state.menu_pilihan = 'Home'
if 'sub_menu_galeri' not in st.session_state:
    st.session_state.sub_menu_galeri = None

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

def set_page(name):
    st.session_state.menu_pilihan = name
    st.session_state.sub_menu_galeri = None

if st.session_state.menu_pilihan == 'Home':
    st.markdown("<style>[data-testid='stSidebar'], [data-testid='collapsedControl'], header {display: none; visibility: hidden;}</style>", unsafe_allow_html=True)

st.markdown(f"""
    <div class="header-container">
        <img src="https://raw.githubusercontent.com/andrey-creator/say-it-play-it/main/logo_ec.jpeg" class="logo-img">
        <h1 class="glow-text">ENGLISH CLUB</h1>
        <p class="sub-text">ENGLISH CLUB • SMAN 1 DEPOK</p>
    </div>
    """, unsafe_allow_html=True)

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

        st.markdown("""
            <div style="text-align: center; margin-top: 40px; padding: 20px; border-top: 1px solid rgba(0, 242, 255, 0.2);">
                <p style="font-family: 'Rajdhani', sans-serif; color: #00f2ff; letter-spacing: 2px; font-size: 1.1rem; font-weight: 500; font-style: italic;">
                    "United we stand • Divided we fall • Never be defeated"
                </p>
            </div>
        """, unsafe_allow_html=True)

elif st.session_state.menu_pilihan in ['Request', 'Feedback']:
    _, cb, _ = st.columns([2, 1, 2])
    with cb: 
        if st.button("⬅️ DASHBOARD"): 
            set_page('Home')
            st.rerun()
    
    if st.session_state.menu_pilihan == 'Request':
        form_url = "https://docs.google.com/forms/d/e/1FAIpQLSel5biF_8tox1dWjFDwHUdyvgJ7Wq1LeCMsmKGeACCR4zxgbQ/viewform"
        header_text = "REQUEST YOUR SONG"
        btn_label = "OPEN REQUEST FORM"
        desc_text = "Click the button below to suggest your favorite tracks for our next session."
    else:
        form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeDaPA8ftqOYm35gT2y6f5BWBwerICz07DmanAVjcLVfLRIZQ/viewform?usp=dialog"
        header_text = "CLUB FEEDBACK"
        btn_label = "OPEN FEEDBACK FORM"
        desc_text = "Share your thoughts or suggestions to help us improve the English Club."

    st.write("##")
    _, col_content, _ = st.columns([1, 2, 1])
    with col_content:
        st.markdown(f"""
            <div style="text-align: center; padding: 30px; border: 1px solid rgba(0, 242, 255, 0.3); border-radius: 15px; background: rgba(0, 242, 255, 0.05);">
                <h2 style="font-family: 'Orbitron'; color: #00f2ff; margin-bottom: 20px;">{header_text}</h2>
                <p style="font-family: 'Rajdhani'; color: white; font-size: 1.1rem; margin-bottom: 30px;">{desc_text}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("##")
        st.link_button(btn_label, form_url, use_container_width=True)

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
                # Memperbaiki nama file agar tidak ada %20
                file_name_encoded = img_url.split('/')[-1].split('.')[0]
                file_name_decoded = unquote(file_name_encoded)
                clean_name = file_name_decoded.replace('-', ' ').replace('_', ' ').upper()
                
                with cols[idx % 3]: 
                    st.image(img_url, use_container_width=True)
                    st.markdown(f'<p class="img-label">{clean_name}</p>', unsafe_allow_html=True)
        else:
            st.warning("No files found.")

with st.sidebar:
    st.markdown("<p style='font-family:Orbitron; color:#00f2ff; font-size:0.7rem;'>CONTROL STATION</p>", unsafe_allow_html=True)
    if st.button("REBOOT"): set_page('Home'); st.rerun()
    st.markdown("---")
    with st.expander("ADMIN"):
        pw = st.text_input("ACCESS CODE", type="password")
        if pw == "AndreEC2026":
            st.link_button("DATABASE", "https://docs.google.com/spreadsheets/d/13a0SStLqMqXMO8fgUImPyMI8jhSEMMQJTE7hQSIYInY/edit?gid=1587199457#gid=1587199457", use_container_width=True)

st.markdown("""
    <div style="
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(5, 7, 10, 0.9);
        color: #00f2ff;
        text-align: center;
        padding: 10px 0;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.8rem;
        letter-spacing: 2px;
        border-top: 1px solid rgba(0, 242, 255, 0.2);
        backdrop-filter: blur(5px);
        z-index: 999;
    ">
        © 2026 • ARYASATYA KEANDRE - DAVIN PRIMA • ENGLISH CLUB • SMAN 1 DEPOK
    </div>
    <div style="margin-bottom: 80px;"></div>
""", unsafe_allow_html=True)