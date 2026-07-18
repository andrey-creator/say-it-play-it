import streamlit as st
import requests
from urllib.parse import unquote

DAFTAR_BATCH = ["batch-2025-2026", "batch-2026-2027"]

DATA_DEMO_EKSKUL = {
    "batch-2025-2026": [
        {"judul": "English Club Demo Day 2026", "url": "https://youtu.be/G0S84LEE1qQ"},
    ],
    "batch-2026-2027": [
        {"judul": "-", "url": "-"},
        {"judul": "-", "url": "-"},
    ]
}

st.set_page_config(
    page_title="English Club SMAN 1 Depok", 
    page_icon="🎙️", 
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://ec-sman1depok.streamlit.app/',
        'Report a bug': None,
        'About': "# Dashboard English Club SMAN 1 Depok. \nTempat galeri aktivitas, request lagu, dan kirim feedback!"
    }
)

@st.cache_data(ttl=2)
def get_photos_from_github(folder_path):
    username = "andrey-creator"
    repo = "say-it-play-it"
    url = f"https://api.github.com/repos/{username}/{repo}/contents/photos/{folder_path}"
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    if "GITHUB_TOKEN" in st.secrets:
        headers["Authorization"] = f"token {st.secrets['GITHUB_TOKEN']}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            files = response.json()
            if isinstance(files, list):
                image_urls = [
                    file['download_url'] for file in files 
                    if file['name'].lower().endswith(('png', 'jpg', 'jpeg', 'webp'))
                ]
                image_urls.reverse() 
                return image_urls
        else:
            st.sidebar.error(f"GitHub API Error: {response.status_code}")
    except Exception:
        return []
    return []

# Inisialisasi session state
if 'menu_pilihan' not in st.session_state:
    st.session_state.menu_pilihan = 'Home'
if 'sub_menu_galeri' not in st.session_state:
    st.session_state.sub_menu_galeri = None
if 'angkatan_pilihan' not in st.session_state:
    st.session_state.angkatan_pilihan = DAFTAR_BATCH[0]
if 'angkatan_demo' not in st.session_state:
    st.session_state.angkatan_demo = DAFTAR_BATCH[0]

# Styling CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');
    
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

    div.stButton > button, div.stLinkButton > a {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        border: 1px solid #00f2ff !important;
        background-color: transparent;
        color: white !important;
        font-family: 'Orbitron', sans-serif;
        border-radius: 10px;
        text-decoration: none;
    }
    div.stButton > button:hover, div.stLinkButton > a:hover {
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
    
    .demo-card {
        padding: 20px; 
        border: 1px solid rgba(0, 242, 255, 0.3); 
        border-radius: 10px; 
        background: rgba(0, 242, 255, 0.02);
        margin-bottom: 15px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

def set_page(name):
    st.session_state.menu_pilihan = name
    st.session_state.sub_menu_galeri = None

if st.session_state.menu_pilihan == 'Home':
    st.markdown(
        "<style>[data-testid='stSidebar'], [data-testid='collapsedControl'], header {display: none; visibility: hidden;}</style>", 
        unsafe_allow_html=True
    )

st.markdown(f"""
    <div class="header-container">
        <img src="https://raw.githubusercontent.com/andrey-creator/say-it-play-it/main/logo_ec.jpeg" class="logo-img">
        <h1 class="glow-text">ENGLISH CLUB</h1>
        <p class="sub-text">ENGLISH CLUB • SMAN 1 DEPOK</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== MENU HOME ====================
if st.session_state.menu_pilihan == 'Home':
    _, col_center, _ = st.columns([1, 2, 1])
    with col_center:
        # Baris Pertama: Galeri & Request
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🖼️\n\nGALERI EC", key="btn_galeri", use_container_width=True):
                set_page('Galeri')
                st.rerun()
        with c2:
            if st.button("🎵\n\nREQUEST SONG", key="btn_req", use_container_width=True):
                set_page('Request')
                st.rerun()
        
        # Baris Kedua: Queue & Feedback
        c3, c4 = st.columns(2)
        with c3:
            if st.button("📜\n\nQUEUE", key="btn_queue", use_container_width=True):
                set_page('Queue')
                st.rerun()
        with c4:
            if st.button("💬\n\nFEEDBACK", key="btn_feed", use_container_width=True):
                set_page('Feedback')
                st.rerun()

        # Baris Ketiga: Fitur Baru (Demo Ekskul)
        if st.button("🚀\n\nDEMO EKSKUL", key="btn_demo", use_container_width=True):
            set_page('Demo')
            st.rerun()

        st.markdown("""
            <div style="text-align: center; margin-top: 40px; padding: 20px; border-top: 1px solid rgba(0, 242, 255, 0.2);">
                <p style="font-family: 'Rajdhani', sans-serif; color: #00f2ff; letter-spacing: 2px; font-size: 1.1rem; font-weight: 500; font-style: italic;">
                    "United we stand • Divided we fall • Never be defeated"
                </p>
            </div>
        """, unsafe_allow_html=True)

# ==================== MENU REQUEST / FEEDBACK ====================
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

# ==================== MENU GALERI ====================
elif st.session_state.menu_pilihan == 'Galeri':
    _, cb, _ = st.columns([2, 1, 2])
    with cb: 
        if st.button("⬅️ DASHBOARD"): 
            set_page('Home')
            st.rerun()
    
    st.markdown("<h2 style='text-align:center; color:#00f2ff; font-family:Orbitron;'>GALERI</h2>", unsafe_allow_html=True)

    if st.session_state.sub_menu_galeri is None:
        _, col_galeri, _ = st.columns([1, 2, 1])
        with col_galeri:
            g1, g2 = st.columns(2)
            with g1:
                if st.button("📸\n\nACTIVITY", use_container_width=True):
                    st.session_state.sub_menu_galeri = "activity"
                    st.session_state.angkatan_pilihan = DAFTAR_BATCH[0]
                    st.rerun()
            with g2:
                st.link_button("👥\n\nINTEGRAL MEMBER", "https://ec-member-gallery-sman1depok.streamlit.app/", use_container_width=True)
                    
    else:
        c_back, _, c_select = st.columns([2, 1, 2])
        with c_back:
            if st.button("⬅️ BACK TO CATEGORIES"):
                st.session_state.sub_menu_galeri = None
                st.rerun()
        
        with c_select:
            angkatan = st.selectbox(
                "SELECT BATCH",
                DAFTAR_BATCH, 
                index=DAFTAR_BATCH.index(st.session_state.angkatan_pilihan) if st.session_state.angkatan_pilihan in DAFTAR_BATCH else 0,
                label_visibility="collapsed"
            )
            st.session_state.angkatan_pilihan = angkatan
        
        path_pencarian = f"{st.session_state.sub_menu_galeri}/{st.session_state.angkatan_pilihan}"
            
        st.write("##")
        with st.spinner("Accessing Database..."):
            images = get_photos_from_github(path_pencarian)
        
        if images:
            cols = st.columns(3)
            for idx, img_url in enumerate(images):
                file_name_encoded = img_url.split('/')[-1].split('.')[0]
                file_name_decoded = unquote(file_name_encoded)
                clean_name = file_name_decoded.replace('-', ' ').replace('_', ' ').upper()
                
                with cols[idx % 3]: 
                    st.image(img_url, use_container_width=True)
                    st.markdown(f'<p class="img-label">{clean_name}</p>', unsafe_allow_html=True)
        else:
            st.warning("No files found in this category.")

# ==================== MENU BARU: DEMO EKSKUL ====================
elif st.session_state.menu_pilihan == 'Demo':
    _, cb, _ = st.columns([2, 1, 2])
    with cb: 
        if st.button("⬅️ DASHBOARD"): 
            set_page('Home')
            st.rerun()
            
    st.markdown("<h2 style='text-align:center; color:#00f2ff; font-family:Orbitron; margin-bottom:20px;'>DEMO EKSKUL</h2>", unsafe_allow_html=True)
    
    # Pilih Tahun / Batch
    _, c_select_demo, _ = st.columns([2, 1, 2])
    with c_select_demo:
        angkatan_demo = st.selectbox(
            "SELECT DEMO BATCH",
            DAFTAR_BATCH, 
            index=DAFTAR_BATCH.index(st.session_state.angkatan_demo) if st.session_state.angkatan_demo in DAFTAR_BATCH else 0,
            label_visibility="visible"
        )
        st.session_state.angkatan_demo = angkatan_demo

    st.write("##")
    
    # Menampilkan daftar link berdasarkan tahun yang dipilih
    _, col_demo_content, _ = st.columns([1, 2, 1])
    with col_demo_content:
        list_link = DATA_DEMO_EKSKUL.get(st.session_state.angkatan_demo, [])
        
        if list_link:
            for item in list_link:
                st.markdown(f"""
                    <div class="demo-card">
                        <h4 style="font-family: 'Rajdhani'; color: white; margin-bottom: 15px; letter-spacing: 1px;">{item['judul'].upper()}</h4>
                    </div>
                """, unsafe_allow_html=True)
                st.link_button("🔗 VISIT LINK", item['url'], use_container_width=True)
                st.write("") # Spacing
        else:
            st.warning("No demo links found for this batch.")

# Sidebar & Footer tetap sama...
with st.sidebar:
    st.markdown("<p style='font-family:Orbitron; color:#00f2ff; font-size:0.7rem;'>CONTROL STATION</p>", unsafe_allow_html=True)
    if st.button("REBOOT"): 
        set_page('Home')
        st.rerun()
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