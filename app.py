import csv
import io
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components
import requests
from urllib.parse import unquote

DAFTAR_BATCH = ["batch-2025-2026", "batch-2026-2027"]

DATA_DEMO_EKSKUL_FALLBACK = {
    "batch-2025-2026": [
        {"judul": "English Club Demo Day 2026", "url": "https://youtu.be/G0S84LEE1qQ"},
    ],
    "batch-2026-2027": [
        {"judul": "-", "url": "-"},
    ]
}

GALERI_PER_PAGE = 12


EVENT_BERIKUTNYA_FALLBACK = {
    "nama": "DEMO DAY BERIKUTNYA",
    "tanggal": "2026-09-05T09:00:00",
}


DATA_PENGURUS_FALLBACK = [
    {"nama": "-", "jabatan": "Ketua"},
    {"nama": "-", "jabatan": "Wakil Ketua"},
    {"nama": "-", "jabatan": "Sekretaris"},
    {"nama": "-", "jabatan": "Bendahara"},
]


WOTD_FALLBACK = {
    "tanggal": "",
    "kata": "Nevrine",
    "pengucapan": "/ˈnɜːrviːn/",
    "arti": "The feeling of missing someone who was never yours, yet somehow still feels like a loss.",
    "jenis_kata": "adj",
    "contoh": "Oh, she's going through a nevrine episode right now, she misses Andre and Davin",
}


WHATSAPP_GROUP_LINK = "https://chat.whatsapp.com/HXO5L4AhuXR5bBqzt1aFpc"
WHATSAPP_QR_IMAGE_URL = "https://raw.githubusercontent.com/andrey-creator/say-it-play-it/main/QR_WhatsApp_Group.png"


ICON_GALERI = '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>'
ICON_MUSIK = '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>'
ICON_ANTRIAN = '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>'
ICON_FEEDBACK = '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>'
ICON_ROKET = '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>'
ICON_USERS = '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
ICON_TV = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>'
ICON_BACK = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>'
ICON_NEXT = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
ICON_KAMERA = '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>'
ICON_SEARCH = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'
ICON_DOWNLOAD = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>'
ICON_EKSTERNAL = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>'
ICON_MOON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
ICON_WHATSAPP = '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/><path d="M9 10a0.5 0.5 0 0 0 1 0"/><path d="M14 10a0.5 0.5 0 0 0 1 0"/><path d="M9 13c.5 1 1.5 1.5 3 1.5s2.5-.5 3-1.5"/></svg>'
ICON_BUKU = '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>'

def render_icon(svg, color="#00f2ff", margin_bottom=8):
    return f'<div style="display:flex;justify-content:center;color:{color};margin-bottom:{margin_bottom}px;">{svg}</div>'

st.set_page_config(
    page_title="English Club SMAN 1 Depok",
    page_icon="https://raw.githubusercontent.com/andrey-creator/say-it-play-it/main/logo_ec.jpeg",
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
    -
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
    st.iframe(og_html, height=1)


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
                    st.sidebar.error("Rate limit GitHub API habis. Coba lagi beberapa saat lagi.", icon=":material/error:")
                else:
                    st.sidebar.error(
                        "Rate limit GitHub API habis (60 request/jam tanpa token). "
                        "Set GITHUB_TOKEN di secrets supaya limitnya jauh lebih longgar (5000/jam).",
                        icon=":material/error:"
                    )
            else:
                st.sidebar.error("Akses ke GitHub API ditolak (403). Cek token/permission.", icon=":material/error:")
        elif response.status_code == 404:
            # Folder belum ada / belum ada foto di batch ini — bukan error, biarkan return []
            pass
        else:
            st.sidebar.error(f"GitHub API Error: {response.status_code}", icon=":material/error:")
    except requests.exceptions.Timeout:
        st.sidebar.warning("Koneksi ke GitHub timeout. Coba refresh lagi.", icon=":material/warning:")
    except requests.exceptions.RequestException as e:
        st.sidebar.warning(f"Gagal konek ke GitHub: {e}", icon=":material/warning:")
    except Exception as e:
        st.sidebar.warning(f"Terjadi error tak terduga saat ambil foto: {e}", icon=":material/warning:")
    return []


@st.cache_data(ttl=3600)
def get_demo_data_from_sheet():
    csv_url = st.secrets.get("DEMO_SHEET_CSV_URL")
    if not csv_url:
        return DATA_DEMO_EKSKUL_FALLBACK

    try:
        response = requests.get(csv_url, timeout=10)
        if response.status_code != 200:
            st.toast("Gagal ambil data demo dari Sheet, pakai data cadangan.", icon=":material/warning:")
            return DATA_DEMO_EKSKUL_FALLBACK

        reader = csv.DictReader(io.StringIO(response.text))
        data = {batch: [] for batch in DAFTAR_BATCH}
        for row in reader:
            batch = (row.get("batch") or "").strip()
            judul = (row.get("judul") or "").strip()
            url = (row.get("url") or "").strip()
            if batch in data and judul and url:
                data[batch].append({"judul": judul, "url": url})

        if not any(data.values()):
            return DATA_DEMO_EKSKUL_FALLBACK
        return data

    except requests.exceptions.RequestException:
        st.toast("Gagal konek ke Google Sheet, pakai data cadangan.", icon=":material/warning:")
        return DATA_DEMO_EKSKUL_FALLBACK
    except Exception:
        st.toast("Format data demo di Sheet tidak sesuai, pakai data cadangan.", icon=":material/warning:")
        return DATA_DEMO_EKSKUL_FALLBACK


@st.cache_data(ttl=300)
def get_event_from_sheet():
    """
    Ambil daftar event dari Google Sheet (kolom: nama, tanggal — format ISO
    contoh 2026-09-05T09:00:00). Otomatis pilih event dengan tanggal terdekat
    yang belum lewat. Kalau secrets belum diisi / gagal / kosong, pakai fallback.
    """
    csv_url = st.secrets.get("EVENT_SHEET_CSV_URL")
    if not csv_url:
        return EVENT_BERIKUTNYA_FALLBACK

    try:
        response = requests.get(csv_url, timeout=10)
        if response.status_code != 200:
            st.sidebar.warning("Gagal ambil data event dari Sheet, pakai data cadangan.", icon=":material/warning:")
            return EVENT_BERIKUTNYA_FALLBACK

        reader = csv.DictReader(io.StringIO(response.text))
        kandidat = []
        for row in reader:
            nama = (row.get("nama") or "").strip()
            tanggal_str = (row.get("tanggal") or "").strip()
            if not nama or not tanggal_str:
                continue
            try:
                tanggal_obj = datetime.fromisoformat(tanggal_str)
            except ValueError:
                continue
            kandidat.append({"nama": nama, "tanggal": tanggal_str, "_dt": tanggal_obj})

        if not kandidat:
            return EVENT_BERIKUTNYA_FALLBACK

        # Pilih event dengan tanggal terdekat yang belum lewat; kalau semua sudah
        # lewat, pakai yang paling baru lewat (biar tidak kosong).
        sekarang = datetime.now()
        akan_datang = sorted([k for k in kandidat if k["_dt"] >= sekarang], key=lambda k: k["_dt"])
        if akan_datang:
            terpilih = akan_datang[0]
        else:
            terpilih = sorted(kandidat, key=lambda k: k["_dt"])[-1]

        return {"nama": terpilih["nama"], "tanggal": terpilih["tanggal"]}

    except requests.exceptions.RequestException:
        st.sidebar.warning("Gagal konek ke Google Sheet (event), pakai data cadangan.", icon=":material/warning:")
        return EVENT_BERIKUTNYA_FALLBACK
    except Exception:
        st.sidebar.warning("Format data event di Sheet tidak sesuai, pakai data cadangan.", icon=":material/warning:")
        return EVENT_BERIKUTNYA_FALLBACK


@st.cache_data(ttl=3600)
def get_pengurus_from_sheet():
    """
    Ambil data pengurus dari Google Sheet (kolom: nama, jabatan, urutan[opsional]).
    Kalau secrets belum diisi / gagal / kosong, pakai fallback.
    """
    csv_url = st.secrets.get("PENGURUS_SHEET_CSV_URL")
    if not csv_url:
        return DATA_PENGURUS_FALLBACK

    try:
        response = requests.get(csv_url, timeout=10)
        if response.status_code != 200:
            st.toast("Gagal ambil data pengurus dari Sheet, pakai data cadangan.", icon=":material/warning:")
            return DATA_PENGURUS_FALLBACK

        # Buang BOM (kalau ada) biar header pertama nggak ketuker jadi '\ufeffnama'
        raw_text = response.text.lstrip('\ufeff')
        reader = csv.DictReader(io.StringIO(raw_text))

        data = []
        for i, row in enumerate(reader):
            # Normalisasi key: lowercase + strip, biar 'Nama', ' urutan ', dll tetap kebaca
            row_norm = {(k or "").strip().lower(): (v or "").strip() for k, v in row.items()}

            nama = row_norm.get("nama", "")
            jabatan = row_norm.get("jabatan", "")
            urutan_str = row_norm.get("urutan", "")

            if not nama or not jabatan:
                continue

            # Bersihkan format angka yang umum dari Sheets (misal "1.0", "1,0", spasi)
            urutan_str = urutan_str.replace(",", ".").strip()
            try:
                urutan = int(float(urutan_str)) if urutan_str else i
            except ValueError:
                urutan = i

            data.append({"nama": nama, "jabatan": jabatan, "_urutan": urutan})

        if not data:
            return DATA_PENGURUS_FALLBACK

        data.sort(key=lambda d: d["_urutan"])
        return [{"nama": d["nama"], "jabatan": d["jabatan"]} for d in data]

    except requests.exceptions.RequestException:
        st.toast("Gagal konek ke Google Sheet (pengurus), pakai data cadangan.", icon=":material/warning:")
        return DATA_PENGURUS_FALLBACK
    except Exception:
        st.toast("Format data pengurus di Sheet tidak sesuai, pakai data cadangan.", icon=":material/warning:")
        return DATA_PENGURUS_FALLBACK


@st.cache_data(ttl=3600)
def get_wotd_from_sheet():
    """
    -
    """
    csv_url = st.secrets.get("WOTD_SHEET_CSV_URL")
    if not csv_url:
        return WOTD_FALLBACK

    try:
        response = requests.get(csv_url, timeout=10)
        if response.status_code != 200:
            st.toast("Gagal ambil Word of the Day dari Sheet, pakai data cadangan.", icon=":material/warning:")
            return WOTD_FALLBACK

        raw_text = response.text.lstrip('\ufeff')
        reader = csv.DictReader(io.StringIO(raw_text))

        daftar = []
        for row in reader:
            row_norm = {(k or "").strip().lower(): (v or "").strip() for k, v in row.items()}
            kata = row_norm.get("kata", "")
            if not kata:
                continue
            daftar.append({
                "tanggal": row_norm.get("tanggal", ""),
                "kata": kata,
                "pengucapan": row_norm.get("pengucapan", ""),
                "arti": row_norm.get("arti", ""),
                "jenis_kata": row_norm.get("jenis_kata", ""),
                "contoh": row_norm.get("contoh", ""),
            })

        if not daftar:
            return WOTD_FALLBACK

        hari_ini_str = datetime.now().strftime("%Y-%m-%d")
        cocok = [d for d in daftar if d["tanggal"] == hari_ini_str]
        if cocok:
            return cocok[0]

        # Tidak ada tanggal yang cocok -> rotasi otomatis pakai hari ke-N dalam setahun
        hari_ke_n = datetime.now().timetuple().tm_yday
        return daftar[hari_ke_n % len(daftar)]

    except requests.exceptions.RequestException:
        st.toast("Gagal konek ke Google Sheet (WOTD), pakai data cadangan.", icon=":material/warning:")
        return WOTD_FALLBACK
    except Exception:
        st.toast("Format data Word of the Day di Sheet tidak sesuai, pakai data cadangan.", icon=":material/warning:")
        return WOTD_FALLBACK


@st.cache_data(ttl=60)
def get_queue_from_sheet():
    csv_url = st.secrets.get("QUEUE_SHEET_CSV_URL")
    if not csv_url:
        return []

    try:
        response = requests.get(csv_url, timeout=10)
        if response.status_code != 200:
            return []

        raw_text = response.text.lstrip('\ufeff')
        reader = csv.DictReader(io.StringIO(raw_text))

        data = []
        for row in reader:
            row_norm = {
                (k or "").strip().lower(): (v or "").strip()
                for k, v in row.items()
            }

            data.append({
    "name": row_norm.get("Full Name/Anonymous:") or "-",
    "class": row_norm.get("Class") or "-",
    "song": row_norm.get("Song artist - tittle") or "-",
})

        return data[:20]

    except Exception:
        return []


@st.dialog("Preview Foto", width="large")
def tampilkan_lightbox(img_url, caption):
    st.image(img_url, use_container_width=True)
    if caption:
        st.markdown(f'<p class="img-label">{caption}</p>', unsafe_allow_html=True)

    col_dl, col_share = st.columns(2)

    with col_dl:
        try:
            img_bytes = requests.get(img_url, timeout=10).content
            file_ext = img_url.split('/')[-1].rsplit('.', 1)[-1] if '.' in img_url.split('/')[-1] else 'jpg'
            file_name = (caption or "foto").replace(' ', '_').lower() + f".{file_ext}"
            st.markdown(render_icon(ICON_DOWNLOAD, margin_bottom=2), unsafe_allow_html=True)
            downloaded = st.download_button(
                "Download Foto",
                data=img_bytes,
                file_name=file_name,
                mime=f"image/{file_ext}",
                use_container_width=True
            )
            if downloaded:
                st.toast("Foto berhasil didownload!", icon=":material/check_circle:")
        except requests.exceptions.RequestException:
            st.warning("Gagal menyiapkan file untuk didownload.", icon=":material/warning:")

    with col_share:
        st.markdown(render_icon(ICON_EKSTERNAL, margin_bottom=2), unsafe_allow_html=True)
        share_html = f"""
        <button id="share-btn" style="
            width:100%; padding:0.65rem 1rem; border-radius:10px;
            border:1px solid #00f2ff; background:transparent; color:white;
            font-family:'Orbitron', sans-serif; font-size:0.85rem; cursor:pointer;
        ">SHARE FOTO</button>
        <script>
        const btn = document.getElementById('share-btn');
        btn.addEventListener('click', async () => {{
            const shareData = {{
                title: 'English Club SMAN 1 Depok',
                text: '{(caption or "Foto").replace("'", "")} - English Club SMAN 1 Depok',
                url: '{img_url}'
            }};
            try {{
                if (navigator.share) {{
                    await navigator.share(shareData);
                }} else {{
                    await navigator.clipboard.writeText('{img_url}');
                    btn.innerText = 'LINK TERSALIN!';
                    setTimeout(() => btn.innerText = 'SHARE FOTO', 1500);
                }}
            }} catch (err) {{
                console.log('Share dibatalkan atau gagal', err);
            }}
        }});
        </script>
        """
        components.html(share_html, height=50)


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
if 'simple_mode' not in st.session_state:
    st.session_state.simple_mode = False

# ==================== MODE KIOSK (TV / MADING) ====================
# Akses lewat URL: <alamat-dashboard>?kiosk=1
if st.query_params.get("kiosk") == "1":
    st.markdown("""
        <style>
        [data-testid='stSidebar'], [data-testid='collapsedControl'], header, footer,
        .block-container { display: none !important; padding: 0 !important; margin: 0 !important; }
        .stApp { background-color: #000000; }
        </style>
    """, unsafe_allow_html=True)

    def get_semua_foto_galeri():
        semua = []
        for batch in DAFTAR_BATCH:
            semua.extend(get_photos_from_github(f"activity/{batch}"))
        return semua

    gambar_kiosk = get_semua_foto_galeri()

    if not gambar_kiosk:
        st.warning("Belum ada foto untuk ditampilkan di mode kiosk.")
        st.stop()

    kiosk_html = f"""
    <div style="position:relative; width:100%; height:100vh; background:#000000; overflow:hidden;">
      <img id="kiosk-img" src="{gambar_kiosk[0]}"
           style="width:100%; height:100%; object-fit:contain; transition:opacity 1s ease-in-out; opacity:1;">
      <div style="position:absolute; bottom:24px; left:0; right:0; text-align:center;
                  font-family:'Orbitron', sans-serif; color:#00f2ff; letter-spacing:3px;
                  text-shadow:0 0 10px #00f2ff; font-size:1rem;">
        ENGLISH CLUB • SMAN 1 DEPOK
      </div>
    </div>
    <script>
      const gambarList = {gambar_kiosk};
      let idx = 0;
      const el = document.getElementById("kiosk-img");
      setInterval(() => {{
          idx = (idx + 1) % gambarList.length;
          el.style.opacity = 0;
          setTimeout(() => {{
              el.src = gambarList[idx];
              el.style.opacity = 1;
          }}, 800);
      }}, 6000);
    </script>
    """
    st.iframe(kiosk_html, height=900)
    st.stop()

# Styling CSS (mode neon/default)
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

# ==================== SIMPLE MODE (matikan efek berat) ====================
if st.session_state.simple_mode:
    st.markdown("""
        <style>
        /* ===== SIMPLE MODE: matikan glow, shadow, animasi berat ===== */
        .glow-text {
            text-shadow: none !important;
            color: #eeeeee !important;
        }
        .sub-text, .img-label, .page-indicator {
            color: #999999 !important;
            text-shadow: none !important;
        }
        .logo-img {
            filter: none !important;
        }
        div.stButton > button, div.stLinkButton > a, div.stDownloadButton > button {
            border: 1px solid #666666 !important;
            color: #eeeeee !important;
            transition: none !important;
        }
        div.stButton > button:hover, div.stLinkButton > a:hover, div.stDownloadButton > button:hover {
            box-shadow: none !important;
            background-color: #333333 !important;
            color: #eeeeee !important;
            transform: none !important;
        }
        .demo-card {
            border: 1px solid #444444 !important;
            background: #1a1a1a !important;
        }
        .demo-card h4 {
            color: #cccccc !important;
        }
        .skeleton-box {
            animation: none !important;
            background: #222222 !important;
        }
        div[style*="text-shadow"] {
            text-shadow: none !important;
        }
        div[style*="backdrop-filter"] {
            backdrop-filter: none !important;
        }
        </style>
    """, unsafe_allow_html=True)


def set_page(name):
    st.session_state.menu_pilihan = name
    st.session_state.sub_menu_galeri = None


def tombol_dashboard():
    st.markdown(render_icon(ICON_BACK, margin_bottom=2), unsafe_allow_html=True)
    if st.button("DASHBOARD"):
        set_page('Home')
        st.rerun()


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


        event_berikutnya = get_event_from_sheet()


        NAMA_BULAN = [
            "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ]
        try:
            dt_event = datetime.fromisoformat(event_berikutnya['tanggal'])
            tanggal_ramah = f"{dt_event.day} {NAMA_BULAN[dt_event.month]} {dt_event.year}, {dt_event.strftime('%H:%M')}"
        except (ValueError, IndexError):
            tanggal_ramah = event_berikutnya['tanggal']

        countdown_html = f"""
        <div style="font-family:'Orbitron', sans-serif; text-align:center; padding:16px;
                    border:1px solid rgba(0, 242, 255, 0.35); border-radius:12px;
                    background:rgba(0, 242, 255, 0.05); color:#ffffff; margin-bottom:20px;">
          <div style="font-size:0.8rem; letter-spacing:2px; color:#00f2ff; margin-bottom:8px;">
            {event_berikutnya['nama']}
          </div>
          <div id="cd-timer" style="font-size:1.5rem; font-weight:700; letter-spacing:1px;">--H : --J : --M : --D</div>
          <div style="font-family:'Rajdhani', sans-serif; font-size:0.8rem; letter-spacing:1px; color:#aaaaaa; margin-top:8px;">
            {tanggal_ramah}
          </div>
        </div>
        <script>
          const target = new Date("{event_berikutnya['tanggal']}").getTime();
          function tick() {{
            const now = new Date().getTime();
            const diff = target - now;
            const el = document.getElementById("cd-timer");
            if (!el) return;
            if (diff <= 0) {{ el.innerText = "Hari ini!"; return; }}
            const d = Math.floor(diff / (1000*60*60*24));
            const h = Math.floor((diff % (1000*60*60*24)) / (1000*60*60));
            const m = Math.floor((diff % (1000*60*60)) / (1000*60));
            const s = Math.floor((diff % (1000*60)) / 1000);
            el.innerText = d + "H : " + String(h).padStart(2,'0') + "J : " + String(m).padStart(2,'0') + "M : " + String(s).padStart(2,'0') + "D";
          }}
          setInterval(tick, 1000);
          tick();
        </script>
        """
        st.iframe(countdown_html, height=155)


        wotd_home = get_wotd_from_sheet()
        wotd_card_html = f"""
        <div style="font-family:'Rajdhani', sans-serif; text-align:center; padding:14px;
                    border:1px solid rgba(0, 242, 255, 0.25); border-radius:12px;
                    background:rgba(0, 242, 255, 0.04); color:#ffffff; margin-bottom:20px;">
          <div style="font-size:0.7rem; letter-spacing:2px; color:#00f2ff; font-family:'Orbitron', sans-serif;">
            WORD OF THE DAY
          </div>
          <div style="font-size:1.4rem; font-weight:700; margin-top:6px;">{wotd_home['kata']}</div>
          <div style="font-size:0.85rem; color:#aaaaaa; font-style:italic;">{wotd_home.get('pengucapan', '')} · {wotd_home.get('jenis_kata', '')}</div>
          <div style="font-size:0.95rem; color:#dddddd; margin-top:6px;">{wotd_home.get('arti', '')}</div>
        </div>
        """
        st.markdown(wotd_card_html, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(render_icon(ICON_GALERI), unsafe_allow_html=True)
            if st.button("GALERI EC", key="btn_galeri", use_container_width=True):
                set_page('Galeri')
                st.rerun()
        with c2:
            st.markdown(render_icon(ICON_MUSIK), unsafe_allow_html=True)
            if st.button("REQUEST SONG", key="btn_req", use_container_width=True):
                set_page('Request')
                st.rerun()

        c3, c4 = st.columns(2)
        with c3:
            st.markdown(render_icon(ICON_ANTRIAN), unsafe_allow_html=True)
            if st.button("QUEUE", key="btn_queue", use_container_width=True):
                set_page('Queue')
                st.rerun()
        with c4:
            st.markdown(render_icon(ICON_FEEDBACK), unsafe_allow_html=True)
            if st.button("FEEDBACK", key="btn_feed", use_container_width=True):
                set_page('Feedback')
                st.rerun()

        c5, c6 = st.columns(2)
        with c5:
            st.markdown(render_icon(ICON_ROKET), unsafe_allow_html=True)
            if st.button("DEMO EKSKUL", key="btn_demo", use_container_width=True):
                set_page('Demo')
                st.rerun()
        with c6:
            st.markdown(render_icon(ICON_USERS), unsafe_allow_html=True)
            if st.button("ABOUT US", key="btn_tentang", use_container_width=True):
                set_page('Tentang')
                st.rerun()

        c7, c8 = st.columns(2)
        with c7:
            st.markdown(render_icon(ICON_WHATSAPP), unsafe_allow_html=True)
            if st.button("WHATSAPP GROUP", key="btn_wa", use_container_width=True):
                set_page('WhatsApp')
                st.rerun()
        with c8:
            st.markdown(render_icon(ICON_BUKU), unsafe_allow_html=True)
            if st.button("WORD OF THE DAY", key="btn_wotd", use_container_width=True):
                set_page('WOTD')
                st.rerun()

        st.markdown("""
            <div style="text-align: center; margin-top: 40px; padding: 20px; border-top: 1px solid rgba(0, 242, 255, 0.2);">
                <p style="font-family: 'Rajdhani', sans-serif; color: #00f2ff; letter-spacing: 2px; font-size: 1.1rem; font-weight: 500; font-style: italic;">
                    "United we stand • Divided we fall • Never be defeated"
                </p>
            </div>
        """, unsafe_allow_html=True)

# ==================== MENU QUEUE ====================
elif st.session_state.menu_pilihan == 'Queue':
    _, cb, _ = st.columns([2, 1, 2])
    with cb:
        tombol_dashboard()

    st.markdown(render_icon(ICON_ANTRIAN, margin_bottom=10), unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#00f2ff; font-family:Orbitron;'>SONG QUEUE</h2>", unsafe_allow_html=True)

    queue_data = get_queue_from_sheet()

    if not queue_data:
        st.warning("Belum ada data queue.")
    else:
        now_playing = queue_data[0]

        now_playing_html = (
            '<div class="demo-card">'
            '<h4 style="color:#00f2ff;font-family:Orbitron;margin-bottom:10px;">NOW PLAYING</h4>'
            f'<p style="font-size:1.2rem;color:white;">🎵 {now_playing["song"]}</p>'
            f'<p style="color:#cccccc;">{now_playing["name"]} ({now_playing["class"]})</p>'
            '</div>'
        )
        st.markdown(now_playing_html, unsafe_allow_html=True)

        st.write("### Up Next")

        for idx, item in enumerate(queue_data[1:], start=1):
            item_html = (
                '<div class="demo-card">'
                f'<h4 style="color:#00f2ff;margin-bottom:5px;">#{idx}</h4>'
                f'<p style="color:white;margin:0;"><b>{item["name"]}</b> ({item["class"]})</p>'
                f'<p style="margin-top:5px;">🎵 {item["song"]}</p>'
                '</div>'
            )
            st.markdown(item_html, unsafe_allow_html=True)

# ==================== MENU WHATSAPP GROUP ====================
elif st.session_state.menu_pilihan == 'WhatsApp':
    _, cb, _ = st.columns([2, 1, 2])
    with cb:
        tombol_dashboard()

    st.markdown(render_icon(ICON_WHATSAPP, margin_bottom=10), unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#00f2ff; font-family:Orbitron;'>WHATSAPP GROUP</h2>", unsafe_allow_html=True)

    st.write("##")
    _, col_wa, _ = st.columns([1, 2, 1])
    with col_wa:
        st.markdown("""
            <div class="demo-card">
                <p style="font-family:'Rajdhani'; color:white; font-size:1.05rem; margin-bottom:20px;">
                    Join our WhatsApp group to stay up to date with the latest English Club info,
                    announcements, and activities. Scan the QR Code below or tap the button to join directly.
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.image(WHATSAPP_QR_IMAGE_URL, use_container_width=True, caption="SCAN TO JOIN")

        st.write("##")
        st.markdown(render_icon(ICON_EKSTERNAL, margin_bottom=2), unsafe_allow_html=True)
        st.link_button("OPEN WHATSAPP GROUP LINK", WHATSAPP_GROUP_LINK, use_container_width=True)

# ==================== MENU REQUEST / FEEDBACK ====================
elif st.session_state.menu_pilihan in ['Request', 'Feedback']:
    _, cb, _ = st.columns([2, 1, 2])
    with cb:
        tombol_dashboard()

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
        tombol_dashboard()

    st.markdown("<h2 style='text-align:center; color:#00f2ff; font-family:Orbitron;'>GALERI</h2>", unsafe_allow_html=True)

    if st.session_state.sub_menu_galeri is None:
        _, col_galeri, _ = st.columns([1, 2, 1])
        with col_galeri:
            g1, g2 = st.columns(2)
            with g1:
                st.markdown(render_icon(ICON_KAMERA), unsafe_allow_html=True)
                if st.button("ACTIVITY", use_container_width=True):
                    st.session_state.sub_menu_galeri = "activity"
                    st.session_state.angkatan_pilihan = DAFTAR_BATCH[0]
                    st.session_state.galeri_page = 0
                    st.rerun()
            with g2:
                st.markdown(render_icon(ICON_USERS), unsafe_allow_html=True)
                st.link_button("INTEGRAL MEMBER", "https://ec-member-gallery-sman1depok.streamlit.app/", use_container_width=True)

    else:
        c_back, _, c_select = st.columns([2, 1, 2])
        with c_back:
            st.markdown(render_icon(ICON_BACK, margin_bottom=2), unsafe_allow_html=True)
            if st.button("BACK TO CATEGORIES"):
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
                    st.markdown(render_icon(ICON_SEARCH, margin_bottom=2), unsafe_allow_html=True)
                    if st.button("Zoom", key=f"lightbox_{start + idx}_{path_pencarian}", use_container_width=True):
                        tampilkan_lightbox(img_url, clean_name)

            if total_pages > 1:
                st.write("##")
                p_prev, p_info, p_next = st.columns([1, 2, 1])
                with p_prev:
                    st.markdown(render_icon(ICON_BACK, margin_bottom=2), unsafe_allow_html=True)
                    if st.button("PREV", use_container_width=True, disabled=st.session_state.galeri_page == 0):
                        st.session_state.galeri_page -= 1
                        st.rerun()
                with p_info:
                    st.markdown(
                        f"<p class='page-indicator'>PAGE {st.session_state.galeri_page + 1} / {total_pages}</p>",
                        unsafe_allow_html=True
                    )
                with p_next:
                    st.markdown(render_icon(ICON_NEXT, margin_bottom=2), unsafe_allow_html=True)
                    if st.button("NEXT", use_container_width=True, disabled=st.session_state.galeri_page >= total_pages - 1):
                        st.session_state.galeri_page += 1
                        st.rerun()
        else:
            st.warning("No files found in this category.")

# ==================== MENU DEMO EKSKUL ====================
elif st.session_state.menu_pilihan == 'Demo':
    _, cb, _ = st.columns([2, 1, 2])
    with cb:
        tombol_dashboard()

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
                st.markdown(render_icon(ICON_EKSTERNAL, margin_bottom=2), unsafe_allow_html=True)
                st.link_button("OPEN IN YOUTUBE", item['url'], use_container_width=True)
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

# ==================== MENU WORD OF THE DAY ====================
elif st.session_state.menu_pilihan == 'WOTD':
    _, cb, _ = st.columns([2, 1, 2])
    with cb:
        tombol_dashboard()

    st.markdown(render_icon(ICON_BUKU, margin_bottom=10), unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#00f2ff; font-family:Orbitron;'>WORD OF THE DAY</h2>", unsafe_allow_html=True)

    st.write("##")
    _, col_wotd, _ = st.columns([1, 2, 1])
    with col_wotd:
        wotd = get_wotd_from_sheet()
        st.markdown(f"""
            <div class="demo-card" style="text-align:center;">
                <h1 style="font-family:'Orbitron'; color:white; font-size:2rem; margin-bottom:4px;">{wotd['kata']}</h1>
                <p style="font-family:'Rajdhani'; color:#00f2ff; font-style:italic; font-size:1rem; margin-bottom:16px;">
                    {wotd.get('pengucapan', '')} · {wotd.get('jenis_kata', '')}
                </p>
                <p style="font-family:'Rajdhani'; color:white; font-size:1.1rem; margin-bottom:16px;">
                    <strong>Meaning:</strong> {wotd.get('arti', '-')}
                </p>
                <p style="font-family:'Rajdhani'; color:#dddddd; font-size:1rem; font-style:italic;">
                    "{wotd.get('contoh', '-')}"
                </p>
            </div>
        """, unsafe_allow_html=True)

# ==================== MENU TENTANG KAMI ====================
elif st.session_state.menu_pilihan == 'Tentang':
    _, cb, _ = st.columns([2, 1, 2])
    with cb:
        tombol_dashboard()

    st.markdown(render_icon(ICON_USERS, margin_bottom=10), unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#00f2ff; font-family:Orbitron; margin-bottom:10px;'>ABOUT US</h2>", unsafe_allow_html=True)
    st.markdown("""
        <p style="text-align:center; font-family:'Rajdhani'; color:white; font-size:1rem; max-width:600px; margin:0 auto 30px auto;">
            English Club SMAN 1 Depok is an extra-curricular society where students sharpen their English language skills through discussions, presentations, debates, broadcasting, and a host of other fun activities.
        </p>
    """, unsafe_allow_html=True)

    _, col_pengurus, _ = st.columns([1, 2, 1])
    with col_pengurus:
        data_pengurus = get_pengurus_from_sheet()


        total_pengurus_terisi = sum(1 for o in data_pengurus if o['nama'] != "-")
        total_foto_semua_batch = sum(
            len(get_photos_from_github(f"activity/{batch}")) for batch in DAFTAR_BATCH
        )

        s1, s2 = st.columns(2)
        with s1:
            st.markdown(f"""
                <div class="demo-card">
                    <h4 style="font-family:'Rajdhani'; color:#00f2ff; margin-bottom:6px; letter-spacing:1px; font-size:0.8rem;">TOTAL PHOTOS</h4>
                    <p style="font-family:'Orbitron'; color:white; font-size:1.6rem; margin:0; font-weight:700;">{total_foto_semua_batch}</p>
                </div>
            """, unsafe_allow_html=True)
        with s2:
            st.markdown(f"""
                <div class="demo-card">
                    <h4 style="font-family:'Rajdhani'; color:#00f2ff; margin-bottom:6px; letter-spacing:1px; font-size:0.8rem;">COMMITTEE POSITIONS FILLED</h4>
                    <p style="font-family:'Orbitron'; color:white; font-size:1.6rem; margin:0; font-weight:700;">{total_pengurus_terisi}/{len(data_pengurus)}</p>
                </div>
            """, unsafe_allow_html=True)

        st.write("##")

        p_cols = st.columns(2)
        for idx, orang in enumerate(data_pengurus):
            nama_tampil = orang['nama'] if orang['nama'] != "-" else "Unfilled"
            with p_cols[idx % 2]:
                st.markdown(f"""
                    <div class="demo-card">
                        <h4 style="font-family:'Rajdhani'; color:#00f2ff; margin-bottom:6px; letter-spacing:1px; font-size:0.8rem;">{orang['jabatan'].upper()}</h4>
                        <p style="font-family:'Rajdhani'; color:white; font-size:1rem; margin:0; font-weight:600;">{nama_tampil}</p>
                    </div>
                """, unsafe_allow_html=True)


with st.sidebar:
    st.markdown("<p style='font-family:Orbitron; color:#00f2ff; font-size:0.7rem;'>CONTROL STATION</p>", unsafe_allow_html=True)
    if st.button("REBOOT"):
        set_page('Home')
        st.rerun()

    st.markdown("---")
    st.markdown(render_icon(ICON_MOON, margin_bottom=4), unsafe_allow_html=True)
    simple_mode = st.toggle("Simple Mode (hemat performa)", value=st.session_state.simple_mode)
    if simple_mode != st.session_state.simple_mode:
        st.session_state.simple_mode = simple_mode
        st.rerun()
    st.caption("Matikan efek glow & animasi neon buat device/TV yang lebih ringan.")

    st.markdown("---")
    st.markdown(render_icon(ICON_TV, margin_bottom=4), unsafe_allow_html=True)
    st.link_button("MODE KIOSK (TV)", "?kiosk=1", use_container_width=True)
    st.caption("Buka link ini di browser TV/mading untuk mode slideshow otomatis.")
    st.markdown("---")
    with st.expander("ADMIN"):
        pw = st.text_input("ACCESS CODE", type="password")
        admin_password = st.secrets.get("ADMIN_PASSWORD")
        if not admin_password:
            st.caption("ADMIN_PASSWORD belum di-set di secrets.")
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
