import streamlit as st

from webui.config import img_path
from webui.ui import page_header

SECTIONS = [
    ("pegion.png", "📺", "College PYQ & YouTube Uploader",
     "Manage subjects, branches, years. Upload YouTube lecture links and import bulk PYQ JSON data.", "yt"),
    ("owl.png", "🎓", "GATE Admin Portal",
     "Split large GATE PDFs into chapters. Import GATE questions, topics, options and papers.", "gate"),
    ("fox_happy.png", "🖼️", "College Image Uploader",
     "Upload step-by-step solution images for college questions to ImageKit CDN.", "college_img"),
    ("lil_fox.png", "📐", "GATE Image Uploader",
     "Upload images for GATE question bodies or individual answer options.", "gate_img"),
    ("raccoon.png", "📁", "GATE DB Editor (Protected)",
     "View, edit, and delete GATE questions directly in your Supabase database.", "gate_db"),
]


def render(go):
    page_header("📚  Dashboard Overview", "guide")

    with st.container(border=True):
        c1, c2 = st.columns([1, 8], vertical_alignment="center")
        if img_path("fox_happy.png"):
            c1.image(img_path("fox_happy.png"), width=60)
        c2.markdown("#### Welcome to your Cozy Hub!\nAll your FocusFox admin tools in one cozy workspace.")

    for img, icon, title, desc, key in SECTIONS:
        with st.container(border=True):
            c1, c2, c3 = st.columns([1, 7, 1.4], vertical_alignment="center")
            if img_path(img):
                c1.image(img_path(img), width=50)
            c2.markdown(f"**{icon}  {title}**  \n{desc}")
            c3.button("Launch", key=f"launch_{key}", on_click=go, args=(key,), width="stretch")

    st.markdown(
        '<div class="ff-tip"><b>💡  Tips</b><br>'
        "• Every section has a ❓ Help button for detailed help.<br>"
        "• Long imports run in the background — you can keep using the dashboard.<br>"
        "• Credentials live in the server's secrets — they are never sent to your browser."
        "</div>", unsafe_allow_html=True)
