import csv
import io

import streamlit as st
import streamlit.components.v1 as components
import requests
from urllib.parse import unquote

DAFTAR_BATCH = ["batch-2025-2026", "batch-2026-2027"]

# Data demo dipakai sebagai FALLBACK kalau Google Sheet belum di-set / gagal diambil.
# Format sheet yang diharapkan (kolom, header wajib persis nama ini):
#   batch | judul | url
# Contoh baris: batch-2025-2026 | English Club Demo Day 2026 | https://youtu.be/G0S84LEE1qQ
DATA_DEMO_EKSKUL_FALLBACK = {
    "batch-2025-2026": [
        {"judul": "English Club Demo Day 2026", "url": "https://youtu.be/G0S84LEE1qQ"},
    ],
    "batch-2026-2027": [
        {"judul": "-", "url": "-"},
        {"judul": "-", "url": "-"},
    ]
}

GALERI_PER_PAGE = 12  # jumlah foto per halaman di galeri

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


# ==================== OPEN GRAPH META TAG (BEST EFFORT) ====================
def inject_og_tags():
    """
    Menyuntikkan Open Graph meta tag ke <head> lewat JavaScript.
    CATATAN PENTING: Streamlit adalah aplikasi client-side (JS-rendered).
    Crawler WhatsApp/Instagram/FB TIDAK menjalankan JavaScript saat mengambil
    preview link, jadi cara ini TIDAK menjamin preview bagus muncul di WhatsApp dsb.
    Ini best-effort untuk tab browser & beberapa crawler modern yang render JS.
    Untuk jaminan penuh di WhatsApp/FB, perlu solusi server-side terpisah
    (misal halaman statis pembungkus / proxy) di luar Streamlit murni.
    """
    og_html = """
    <script>
        function setMeta(property, content) {
            let doc = window.parent.document;
            let el = doc.querySelector(`meta[property='${property}']`);
            if (!el) {
                el = doc.createElement('meta');
                el.setAttribute('property', property);
                doc.head.appendChild(el);
            }
            el.setAttribute('content', content);
        }
        setMeta('og:title', 'English Club SMAN 1 Depok');
        setMeta('og:description', 'Galeri aktivitas, request lagu, demo ekskul, dan feedback English Club SMAN 1 Depok.');
        setMeta('og:image', 'https://raw.githubusercontent.com/andrey-creator/say-it-play-it/main/logo_ec.jpeg');
        setMeta('og:type', 'website');
    </script>
    """
    components.html(og_html, height=0, width=0)


inject_og_tags()


@st.cache_data(ttl=300)
def get_photos_from_github(folder_path):
    username = "andrey-creator"
    repo = "say-it-play-it"
    url = f"https://api.github.com/repos/{username}/{repo}/contents/photos/{folder_path}"

    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    has_token = "GITHUB_TOKEN" in st.secrets
    if has_token:
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
        elif response.status_code == 403:
            remaining = response.headers.get("X-RateLimit-Remaining")
            if remaining == "0":
                if has_token:
                    st.sidebar.error("⚠️ Rate limit GitHub API habis. Coba lagi beberapa saat lagi.")
                else:
                    st.sidebar.error(
                        "⚠️ Rate limit GitHub API habis (60 request/jam tanpa token). "
                        "Set GITHUB_TOKEN di secrets supaya limitnya jauh lebih longgar (5000/jam)."
                    )
            else:
                st.sidebar.error("⚠️ Akses ke GitHub API ditolak (403). Cek token/permission.")
        elif response.status_code == 404:
            # Folder belum ada / belum ada foto di batch ini — bukan error, biarkan return []
            pass
        else:
            st.sidebar.error(f"GitHub API Error: {response.status_code}")
    except requests.exceptions.Timeout:
        st.sidebar.warning("⚠️ Koneksi ke GitHub timeout. Coba refresh lagi.")
    except requests.exceptions.RequestException as e:
        st.sidebar.warning(f"⚠️ Gagal konek ke GitHub: {e}")
    except Exception as e:
        st.sidebar.warning(f"⚠️ Terjadi error tak terduga saat ambil foto: {e}")
    return []


@st.cache_data(ttl=300)
def get_demo_data_from_sheet():
    """
    Ambil data demo ekskul dari Google Sheet (published as CSV) supaya admin
    bisa update video tanpa perlu edit & redeploy kode.

    Cara setup:
    1. Di Google Sheet, File > Share > Publish to web > pilih sheet yang berisi
       kolom: batch, judul, url > format CSV > Publish.
    2. Copy link CSV yang dihasilkan, simpan di st.secrets sebagai:
       DEMO_SHEET_CSV_URL = "https://docs.google.com/.../pub?output=csv"

    Kalau secrets belum di-set atau fetch gagal, fallback ke data hardcoded.
    """
    csv_url = st.secrets.get("DEMO_SHEET_CSV_URL")
    if not csv_url:
        return DATA_DEMO_EKSKUL_FALLBACK

    try:
        response = requests.get(csv_url, timeout=10)
        if response.status_code != 200:
            st.sidebar.warning("⚠️ Gagal ambil data demo dari Sheet, pakai data cadangan.")
            return DATA_DEMO_EKSKUL_FALLBACK

        reader = csv.DictReader(io.StringIO(response.text))
        data = {batch: [] for batch in DAFTAR_BATCH}
        for row in reader:
            batch = (row.get("batch") or "").strip()
            judul = (row.get("judul") or "").strip()
            url = (row.get("url") or "").strip()
            if batch in data and judul and url:
                data[batch].append({"judul": judul, "url": url})

        # Kalau sheet kosong / semua batch kosong, fallback ke data cadangan
        if not any(data.values()):
            return DATA_DEMO_EKSKUL_FALLBACK
        return data

    except requests.exceptions.RequestException:
        st.sidebar.warning("⚠️ Gagal konek ke Google Sheet, pakai data cadangan.")
        return DATA_DEMO_EKSKUL_FALLBACK
    except Exception:
        st.sidebar.warning("⚠️ Format data demo di Sheet tidak sesuai, pakai data cadangan.")
        return DATA_DEMO_EKSKUL_FALLBACK


@st.dialog("PREVIEW", width="large")
def tampilkan_lightbox(img_url, caption):
    st.image(img_url, use_container_width=True)
    if caption:
        st.markdown(f'<p class="img-label">{caption}</p>', unsafe_allow_html=True)

    try:
        img_bytes = requests.get(img_url, timeout=10).content
        file_ext = img_url.split('/')[-1].rsplit('.', 1)[-1] if '.' in img_url.split('/')[-1] else 'jpg'
        file_name = (caption or "foto").replace(' ', '_').lower() + f".{file_ext}"
        st.download_button(
            "⬇️ Download Foto",
            data=img_bytes,
            file_name=file_name,
            mime=f"image/{file_ext}",
            use_container_width=True
        )
    except requests.exceptions.RequestException:
        st.warning("⚠️ Gagal menyiapkan file untuk didownload.")


if 'menu_pilihan' not in st.session_state:
    st.session_state.menu_pilihan = 'Home'
if 'sub_menu_galeri' not in st.session_state:
    st.session_state.sub_menu_galeri = None
if 'angkatan_pilihan' not in st.session_state:
    st.session_state.angkatan_pilihan = DAFTAR_BATCH[0]
if 'angkatan_demo' not in st.session_state:
    st.session_state.angkatan_demo = DAFTAR_BATCH[0]
if 'galeri_page' not in st.session_state:
    st.session_state.galeri_page = 0

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

    div.stButton > button, div.stLinkButton > a, div.stDownloadButton > button {
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
    div.stButton > button:hover, div.stLinkButton > a:hover, div.stDownloadButton > button:hover {
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

    .skeleton-box {
        width: 100%;
        aspect-ratio: 1 / 1;
        border-radius: 10px;
        margin-bottom: 25px;
        background: linear-gradient(90deg, rgba(0,242,255,0.05) 25%, rgba(0,242,255,0.15) 37%, rgba(0,242,255,0.05) 63%);
        background-size: 400% 100%;
        animation: shimmer 1.4s ease-in-out infinite;
    }
    @keyframes shimmer {
        0% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .page-indicator {
        text-align: center;
        font-family: 'Rajdhani', sans-serif;
        color: #00f2ff;
        letter-spacing: 1px;
        padding-top: 8px;
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
                    st.session_state.galeri_page = 0
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
            if angkatan != st.session_state.angkatan_pilihan:
                st.session_state.galeri_page = 0  # reset halaman kalau ganti batch
            st.session_state.angkatan_pilihan = angkatan

        path_pencarian = f"{st.session_state.sub_menu_galeri}/{st.session_state.angkatan_pilihan}"

        st.write("##")

        skeleton_slot = st.empty()
        with skeleton_slot.container():
            skel_cols = st.columns(3)
            for i in range(6):
                with skel_cols[i % 3]:
                    st.markdown('<div class="skeleton-box"></div>', unsafe_allow_html=True)

        images = get_photos_from_github(path_pencarian)
        skeleton_slot.empty()

        if images:
            total_pages = max(1, (len(images) - 1) // GALERI_PER_PAGE + 1)
            # Jaga-jaga kalau halaman tersimpan sudah di luar batas (misal setelah data berkurang)
            st.session_state.galeri_page = min(st.session_state.galeri_page, total_pages - 1)

            start = st.session_state.galeri_page * GALERI_PER_PAGE
            end = start + GALERI_PER_PAGE
            images_page = images[start:end]

            cols = st.columns(3)
            for idx, img_url in enumerate(images_page):
                file_name_encoded = img_url.split('/')[-1].rsplit('.', 1)[0]
                file_name_decoded = unquote(file_name_encoded)
                clean_name = file_name_decoded.replace('-', ' ').replace('_', ' ').upper()

                with cols[idx % 3]:
                    st.image(img_url, use_container_width=True, caption=clean_name)
                    if st.button("🔍 Zoom", key=f"lightbox_{start + idx}_{path_pencarian}", use_container_width=True):
                        tampilkan_lightbox(img_url, clean_name)

            if total_pages > 1:
                st.write("##")
                p_prev, p_info, p_next = st.columns([1, 2, 1])
                with p_prev:
                    if st.button("⬅️ PREV", use_container_width=True, disabled=st.session_state.galeri_page == 0):
                        st.session_state.galeri_page -= 1
                        st.rerun()
                with p_info:
                    st.markdown(
                        f"<p class='page-indicator'>PAGE {st.session_state.galeri_page + 1} / {total_pages}</p>",
                        unsafe_allow_html=True
                    )
                with p_next:
                    if st.button("NEXT ➡️", use_container_width=True, disabled=st.session_state.galeri_page >= total_pages - 1):
                        st.session_state.galeri_page += 1
                        st.rerun()
        else:
            st.warning("No files found in this category.")

# ==================== MENU DEMO EKSKUL ====================
elif st.session_state.menu_pilihan == 'Demo':
    _, cb, _ = st.columns([2, 1, 2])
    with cb:
        if st.button("⬅️ DASHBOARD"):
            set_page('Home')
            st.rerun()

    st.markdown("<h2 style='text-align:center; color:#00f2ff; font-family:Orbitron; margin-bottom:20px;'>DEMO EKSKUL</h2>", unsafe_allow_html=True)

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

    _, col_demo_content, _ = st.columns([1, 2, 1])
    with col_demo_content:
        data_demo = get_demo_data_from_sheet()
        list_link = data_demo.get(st.session_state.angkatan_demo, [])

        item_siap = [item for item in list_link if item['judul'] != "-" and item['url'] != "-"]
        item_belum_siap = len(list_link) - len(item_siap)

        if item_siap:
            for item in item_siap:
                st.markdown(f"""
                    <div class="demo-card">
                        <h4 style="font-family: 'Rajdhani'; color: white; margin-bottom: 15px; letter-spacing: 1px;">{item['judul'].upper()}</h4>
                    </div>
                """, unsafe_allow_html=True)
                try:
                    st.video(item['url'])
                except Exception:
                    st.warning("Video can't be opened, move toward direct link")
                st.link_button("🔗 OPEN IN YOUTUBE", item['url'], use_container_width=True)
                st.write("")

        if item_belum_siap > 0:
            st.markdown(f"""
                <div class="demo-card" style="opacity: 0.5;">
                    <h4 style="font-family: 'Rajdhani'; color: #00f2ff; margin-bottom: 5px; letter-spacing: 1px;">COMING SOON</h4>
                    <p style="font-family: 'Rajdhani'; color: white; font-size: 0.85rem; margin: 0;">{item_belum_siap} demo video(s) haven't been uploaded</p>
                </div>
            """, unsafe_allow_html=True)

        if not item_siap and item_belum_siap == 0:
            st.warning("No demo links found for this batch.")


with st.sidebar:
    st.markdown("<p style='font-family:Orbitron; color:#00f2ff; font-size:0.7rem;'>CONTROL STATION</p>", unsafe_allow_html=True)
    if st.button("REBOOT"):
        set_page('Home')
        st.rerun()
    st.markdown("---")
    with st.expander("ADMIN"):
        pw = st.text_input("ACCESS CODE", type="password")
        admin_password = st.secrets.get("ADMIN_PASSWORD")
        if not admin_password:
            st.caption("⚠️ ADMIN_PASSWORD belum di-set di secrets.")
        elif pw and pw == admin_password:
            st.link_button("DATABASE", "https://docs.google.com/spreadsheets/d/13a0SStLqMqXMO8fgUImPyMI8jhSEMMQJTE7hQSIYInY/edit?gid=1587199457#gid=1587199457", use_container_width=True)
        elif pw:
            st.error("Access code salah.")

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