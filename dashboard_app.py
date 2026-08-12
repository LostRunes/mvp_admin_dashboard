import os
import sys
import json
import re
import threading
import webbrowser
from dotenv import load_dotenv

# PySide6 components
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QComboBox, QFileDialog,
    QMessageBox, QScrollArea, QGridLayout, QTabWidget, QSizePolicy,
    QDialog, QTextBrowser
)
from PySide6.QtCore import Qt, QSize, QTimer, QThread, Signal
from PySide6.QtGui import QPixmap, QFont, QPalette, QColor, QImage, QPainter

# Firebase auth module (optional — login screen shown if available)
try:
    import firebase_auth
    _auth_ok = True
except ImportError:
    _auth_ok = False

try:
    from supabase import create_client
except ImportError:
    create_client = None

try:
    from imagekitio import ImageKit
except ImportError:
    ImageKit = None

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    PdfReader, PdfWriter = None, None

load_dotenv()

# ── Theme Palettes ───────────────────────────────────────────────────────────
THEME_PALETTES = {
    "light": {
        "bg": "#DDEFFF",
        "pink": "#F3A6C3",
        "lavender": "#E8DEFF",
        "purple": "#8174D6",
        "cream": "#FFF6DC",
        "white": "rgba(255, 253, 253, 210)",
        "text": "#5C5874",
        "muted": "#8D89A5",
        "green": "#A8D99B",
        "red": "#E8899D"
    },
    "dark": {
        "bg": "#1C1B29",
        "pink": "#F3A6C3",
        "lavender": "#8174D6",
        "purple": "#5C53A3",
        "cream": "#2E2A47",
        "white": "rgba(40, 36, 68, 210)",
        "text": "#E8E2FF",
        "muted": "#8D89A5",
        "green": "#A8D99B",
        "red": "#E8899D"
    }
}

COLORS = THEME_PALETTES["dark"]    # default

def get_qss(colors):
    return f"""
    QMainWindow {{ background-color: {colors["bg"]}; }}
    QFrame#sidebar {{
        background: {colors["white"]};
        border: 2px solid {colors["purple"]};
        border-radius: 8px;
    }}
    QFrame#glassWindow {{
        background: {colors["white"]};
        border: 2px solid {colors["purple"]};
        border-radius: 8px;
    }}
    QFrame#titleBar {{ background: {colors["pink"]}; border-radius: 4px; }}
    QLabel {{
        color: {colors["text"]};
        font-family: "Pixelify Sans", "Courier New", sans-serif;
    }}
    QPushButton {{
        background-color: {colors["white"]};
        color: {colors["text"]};
        border: 2px solid {colors["purple"]};
        border-radius: 6px;
        font-family: "Pixelify Sans", sans-serif;
        font-size: 11px;
        font-weight: bold;
        padding: 6px;
    }}
    QPushButton:hover {{ background-color: {colors["lavender"]}; }}
    QLineEdit, QTextEdit, QComboBox {{
        background-color: {colors["white"]};
        border: 2px solid {colors["purple"]};
        border-radius: 6px;
        color: {colors["text"]};
        padding: 4px;
    }}
    QTabWidget::pane {{
        border: 2px solid {colors["purple"]};
        border-radius: 6px;
        background: transparent;
    }}
    QTabBar::tab {{
        background: {colors["white"]};
        border: 2px solid {colors["purple"]};
        border-bottom: none;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        padding: 6px 12px;
        margin-right: 2px;
        color: {colors["text"]};
    }}
    QTabBar::tab:selected {{ background: {colors["pink"]}; }}
    QFrame#card {{
        background: {colors["white"]};
        border: 2px solid {colors["purple"]};
        border-radius: 8px;
    }}
    QFrame#banner {{
        background: {colors["cream"]};
        border: 2px solid {colors["purple"]};
        border-radius: 8px;
    }}
    QFrame#rowcard {{
        background: {colors["cream"]};
        border-radius: 6px;
        padding: 4px;
    }}
    QFrame#tip {{
        background: {colors["bg"] == "#1C1B29" and "#122015" or "#E6F4EA"};
        border: 2px solid {colors["bg"] == "#1C1B29" and "#2E7D32" or "#A3E635"};
        border-radius: 8px;
    }}
    QScrollArea {{
        background: transparent;
        border: none;
    }}
    QWidget {{
        background: transparent;
    }}
    """

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMGS     = os.path.join(BASE_DIR, "images")

def img_path(n): return os.path.join(IMGS, n)

HELP = {
    "guide": ("fox_happy.png",
        "This is your all-in-one FocusFox admin workspace.\n"
        "Navigate using the sidebar on the left.\n\n"
        "Every section has a  ?  button for help.\n"
        "All data syncs to your Supabase cloud database.\n\n"
        "Tip: Credentials load from your .env file —\n"
        "no manual config needed!"
    ),
    "yt": ("lil_fox.png",
        "College PYQ & YouTube Uploader\n\n"
        "Tab 1 — YouTube Link Uploader\n"
        "1. Select a subject from the dropdown.\n"
        "2. Edit links (one URL per line).\n"
        "3. Click Save to persist changes.\n\n"
        "Tab 2 — Subject & Branch Manager\n"
        "Fill Subject Name + Code (required).\n"
        "Optionally add Drive links.\n"
        "Create branches and year labels.\n\n"
        "Tab 3 — JSON PYQ Importer\n"
        "1. Select target subject.\n"
        "2. Pick a .json file with topics & questions.\n"
        "3. Watch the log for progress."
    ),
    "gate": ("owl.png",
        "GATE Admin Portal\n\n"
        "Tab 1 — PDF Splitter\n"
        "1. Browse to a GATE PDF.\n"
        "2. Enter ranges:  1-10, 11-20\n"
        "3. Pick output folder — done!\n\n"
        "Tab 2 — GATE JSON Importer\n"
        "JSON schema:\n"
        "{ subject:{}, topics:[], questions:[] }\n\n"
        "Each question needs: question_text,\n"
        "options[], topics[], pyq_sources[].\n"
        "Subjects & topics are auto-created."
    ),
    "college_img": ("panda.png",
        "College Image Uploader\n\n"
        "Left: cascade dropdowns\n"
        "Branch->Sem->Subject->Year->Exam->Season->Q\n\n"
        "Preview shows the question text.\n\n"
        "Right panel:\n"
        "1. Click Choose Images.\n"
        "2. Thumbnails appear in the grid.\n"
        "3. Click Upload — images go to ImageKit\n"
        "   CDN and saved to Supabase images table.\n\n"
        "Note: Uploading REPLACES existing images."
    ),
    "gate_img": ("lil_fox.png",
        "GATE Image Uploader\n\n"
        "Left: select\n"
        "Year -> Paper -> Subject -> Question\n\n"
        "Target:\n"
        "Question Text / Body\n"
        "Option A / B / C / D\n\n"
        "Right panel:\n"
        "1. Choose images.\n"
        "2. Upload — stored under gate/questions/<id>\n"
        "   or gate/options/<id> on ImageKit.\n\n"
        "Note: Uploading REPLACES existing images."
    ),
    "gate_db": ("raccoon.png",
        "GATE DB Editor (Protected)\n\n"
        "This section lets you view, edit,\n"
        "and delete GATE questions directly\n"
        "in your Supabase database.\n\n"
        "1. Select a subject from the top bar.\n"
        "2. Type in the search box to filter.\n"
        "3. Click a question row to load it.\n"
        "4. Edit fields on the right panel.\n"
        "5. Click Save Changes to persist.\n"
        "6. Click Delete Question to remove\n"
        "   the question and all its options.\n\n"
        "Options panel:\n"
        "• Edit label / text / correct flag.\n"
        "• Click  +  to add a new option.\n"
        "• Click  🗑  to delete an option.\n\n"
        "⚠  Changes are permanent."
    ),
    "todo": ("coffee.png",
        "Developer Task Manager\n\n"
        "This section keeps track of your to-do lists and syncs tasks directly to your profile in Firestore.\n\n"
        "1. Add Task: Type in the box and press Enter or click 'Add Task'.\n"
        "2. Complete: Click the checkbox button to mark a task as completed (gets strike-through styling).\n"
        "3. Delete: Click the trash icon to permanently remove the item."
    ),
    "spotify": ("coffee.png",
        "Focus Music Player\n\n"
        "Integrates Spotify focus music into your coding workspace.\n\n"
        "1. Open App: Launches the Spotify Desktop application directly to the playlist.\n"
        "2. Open Web: Opens the playlist in your system's default web browser.\n"
        "3. Custom Playlists: Paste your own Spotify playlist link and click 'Save'. It will sync with Firestore so it is saved to your account profile."
    ),
}

QSS = get_qss(COLORS)  # initial stylesheet (light theme)

class _GuideWorker(QThread):
    result_ready = Signal(dict)
    
    def __init__(self, key, fallback_data):
        super().__init__()
        self.key = key
        self.fallback_data = fallback_data

    def run(self):
        res = None
        if _auth_ok:
            try:
                res = firebase_auth.get_guide(self.key)
            except Exception as e:
                print(f"Error loading firestore guide: {e}")
        if not res:
            res = {
                "title": f"Help Guide ({self.key})",
                "text": self.fallback_data[1],
                "image": self.fallback_data[0],
                "schema": "Database schema offline."
            }
        self.result_ready.emit(res)

class GuideDialog(QDialog):
    def __init__(self, parent, title, text, img_name):
        super().__init__(parent)
        self.setWindowTitle("Help Guide")
        self.resize(520, 420)
        self.setMinimumSize(420, 320)
        
        # Design layout
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(12)
        
        hdr_lay = QHBoxLayout()
        hdr_lay.setSpacing(12)
        
        # Icon
        p_path = img_path(img_name)
        if os.path.exists(p_path):
            lbl_icon = QLabel()
            lbl_icon.setPixmap(QPixmap(p_path).scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            hdr_lay.addWidget(lbl_icon)
            
        lbl_t = QLabel(title)
        lbl_t.setStyleSheet("font-size: 15px; font-weight: bold; font-family: 'Pixelify Sans';")
        lbl_t.setWordWrap(True)
        hdr_lay.addWidget(lbl_t, 1)
        lay.addLayout(hdr_lay)
        
        # Text Browser for scrollability + clickable links
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        self.browser.setStyleSheet("background: transparent; border: none; font-size: 12px; font-family: 'Pixelify Sans';")
        
        html_text = self._format_text(text)
        self.browser.setHtml(html_text)
        lay.addWidget(self.browser, 1)
        
        # Buttons
        btn_box = QHBoxLayout()
        btn_box.addStretch()
        ok_btn = QPushButton("Got it!")
        ok_btn.clicked.connect(self.accept)
        btn_box.addWidget(ok_btn)
        lay.addLayout(btn_box)

    def _format_text(self, text):
        # Escape HTML tags first
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        # Regex to match URLs
        url_re = re.compile(r'(https?://[^\s()<>]+)')
        # Replace URLs with HTML links styled pink
        text = url_re.sub(r'<a href="\1" style="color: #F3A6C3; text-decoration: underline;">\1</a>', text)
        # Replace newlines with <br>
        return text.replace("\n", "<br>")

class GlassWindow(QFrame):
    def __init__(self, title="", icon_pix=None, parent=None):
        super().__init__(parent)
        self.setObjectName("glassWindow")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(4, 4, 4, 8)
        self.layout.setSpacing(4)

        # Title bar
        titlebar = QFrame()
        titlebar.setObjectName("titleBar")
        titlebar.setFixedHeight(34)
        t_lay = QHBoxLayout(titlebar)
        t_lay.setContentsMargins(10, 0, 10, 0)
        t_lay.setSpacing(6)

        if icon_pix:
            lbl_icon = QLabel()
            lbl_icon.setPixmap(icon_pix.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            t_lay.addWidget(lbl_icon)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-weight: bold; font-size: 12px;")
        t_lay.addWidget(lbl_title)
        t_lay.addStretch()

        controls = QLabel("— □ ×")
        controls.setStyleSheet("font-size: 11px; font-weight: bold;")
        t_lay.addWidget(controls)
        self.layout.addWidget(titlebar)

        self.body = QFrame()
        self.body_layout = QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(12, 12, 12, 12)
        self.body_layout.setSpacing(8)
        self.layout.addWidget(self.body)

    def content_layout(self):
        return self.body_layout

class FocusFoxApp(QMainWindow):
    def __init__(self, user: dict | None = None):
        super().__init__()
        self.setWindowTitle("☕ FocusFox  Admin Desktop")
        self._auth_user = user  # logged-in developer dict (or None)
        self.resize(1280, 880)
        self.setMinimumSize(1060, 760)

        self.supabase_url      = os.getenv("SUPABASE_URL", "https://hoihnpzdlivaoywrshmk.supabase.co")
        self.supabase_key      = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhvaWhucHpkbGl2YW95d3JzaG1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczMDc1MjAsImV4cCI6MjA5Mjg4MzUyMH0.0XavqpSZjXVvuVRdEvI1Iy7ZGCOxCfGBA0cROVHyvHI")
        self.imagekit_public   = os.getenv("IMAGEKIT_PUBLIC_KEY", "public_czXZbyoBKtF2iM2UY6bWAg9tgkI=")
        self.imagekit_private  = os.getenv("IMAGEKIT_PRIVATE_KEY", "private_pAlFPi/MgMKYXqpcuvuioTjBHVk=")
        self.imagekit_endpoint = os.getenv("IMAGEKIT_URL_ENDPOINT", "https://ik.imagekit.io/focusfox")

        self._load_mascots()
        self._init_connections()

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.main_layout = QHBoxLayout(self.central)
        self.main_layout.setContentsMargins(12, 12, 12, 12)
        self.main_layout.setSpacing(12)

        self._build_sidebar()

        self.workspace = QStackedWidgetWrapper()
        self.main_layout.addWidget(self.workspace, 1)

        self.pages = {}
        self._build_pages()
        self.switch("guide")

        # Load initial wallpaper (dark theme by default)
        self._update_background("dark_deskbg2.jpg", "dark")

    def _load_mascots(self):
        self.mascots = {}
        wanted = ["fox", "panda", "panda_r", "owl", "lil_fox", "logo", "coffee", "raccoon"]
        for key in wanted:
            fn = f"{key}.png" if key != "logo" else "focus_fox_nobg.png"
            if key == "panda_r": fn = "pegion.png"
            p = img_path(fn)
            if os.path.exists(p):
                self.mascots[key] = QPixmap(p)
            else:
                self.mascots[key] = None

    def _init_connections(self):
        self.supabase = None
        self.imagekit = None
        if create_client:
            try:
                self.supabase = create_client(self.supabase_url, self.supabase_key)
            except Exception as e:
                print(f"Supabase connection failed: {e}")
        if ImageKit and self.imagekit_private:
            try:
                self.imagekit = ImageKit(private_key=self.imagekit_private)
            except Exception as e:
                print(f"ImageKit connection failed: {e}")

    def _build_sidebar(self):
        self._sb = QFrame()
        self._sb.setObjectName("sidebar")
        self._sb.setFixedWidth(256)
        self.main_layout.addWidget(self._sb)

        layout = QVBoxLayout(self._sb)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # Title launcher header
        header = QFrame()
        header.setFixedHeight(44)
        header.setStyleSheet(f"background-color: {COLORS['pink']}; border-radius: 6px;")
        h_lay = QHBoxLayout(header)
        h_lay.setContentsMargins(10, 0, 10, 0)
        
        lbl_h = QLabel("FOCUSFOX.EXE")
        lbl_h.setStyleSheet("font-weight: bold; font-size: 12px;")
        h_lay.addWidget(lbl_h)
        h_lay.addStretch()

        self._btn_col = QPushButton("☰")
        self._btn_col.setFixedSize(28, 28)
        self._btn_col.clicked.connect(self._toggle_sidebar)
        h_lay.addWidget(self._btn_col)
        layout.addWidget(header)

        self._lbl_sub = QLabel("✦ Admin Workspace ✦")
        self._lbl_sub.setStyleSheet(f"color: {COLORS['muted']}; font-size: 10px; margin-left: 6px;")
        layout.addWidget(self._lbl_sub)

        # Separator line
        sep = QFrame()
        sep.setFixedHeight(2)
        sep.setStyleSheet(f"background-color: {COLORS['purple']};")
        layout.addWidget(sep)

        self._lbl_prog = QLabel("  PROGRAMS")
        self._lbl_prog.setStyleSheet(f"color: {COLORS['muted']}; font-size: 9px; font-weight: bold;")
        layout.addWidget(self._lbl_prog)

        self._nav_btns = {}
        self._nav_data = [
            ("guide",       "🏠", "Home Menu"),
            ("yt",          "📺", "College PYQ"),
            ("gate",        "🎓", "GATE Portal"),
            ("college_img", "🖼️", "College Images"),
            ("gate_img",    "📐", "GATE Images"),
            ("gate_db",     "📁", "GATE DB Editor"),
            ("todo",        "📝", "Developer Tasks"),
            ("spotify",     "🎵", "Focus Music"),
        ]

        for key, icon, label in self._nav_data:
            btn = QPushButton(f" {icon}  {label}")
            btn.setStyleSheet("text-align: left; padding-left: 10px; font-size: 11px;")
            btn.clicked.connect(lambda checked=False, k=key: self.switch(k))
            layout.addWidget(btn)
            self._nav_btns[key] = btn

        layout.addStretch()

        sep2 = QFrame()
        sep2.setFixedHeight(2)
        sep2.setStyleSheet(f"background-color: {COLORS['purple']};")
        layout.addWidget(sep2)

        # Logged-in developer identity
        if self._auth_user:
            lbl_user = QLabel(f"👤  {self._auth_user.get('name', 'Developer')}")
            lbl_user.setStyleSheet(f"color: {COLORS['text']}; font-size: 10px; font-weight: bold; margin-left: 6px; margin-top: 4px;")
            layout.addWidget(lbl_user)
            lbl_email = QLabel(self._auth_user.get("email", ""))
            lbl_email.setStyleSheet(f"color: {COLORS['muted']}; font-size: 9px; margin-left: 6px;")
            layout.addWidget(lbl_email)

        self._lbl_conn = QLabel("☁  Connected" if self.supabase else "☁  Offline")
        self._lbl_conn.setStyleSheet(f"color: {COLORS['green'] if self.supabase else COLORS['red']}; font-size: 10px; margin-left: 6px;")
        layout.addWidget(self._lbl_conn)

        # Theme toggle button
        self._is_dark = True
        self._btn_theme = QPushButton("🌙  Dark Theme")
        self._btn_theme.clicked.connect(self._toggle_theme)
        layout.addWidget(self._btn_theme)

        self._lbl_ver = QLabel("v1.3.0  •  Retro Desktop")
        self._lbl_ver.setStyleSheet(f"color: {COLORS['muted']}; font-size: 9px; margin-left: 6px; margin-bottom: 6px;")
        layout.addWidget(self._lbl_ver)

    def _toggle_theme(self):
        self._is_dark = not self._is_dark
        if self._is_dark:
            self._btn_theme.setText("🌙  Dark Theme")
            self._update_background("dark_deskbg2.jpg", "dark")
        else:
            self._btn_theme.setText("☀️  Light Theme")
            self._update_background("light_bg.jpg", "light")

    def paintEvent(self, event):
        """Draw wallpaper scaled-to-cover behind all widgets."""
        if getattr(self, "_bg_pixmap", None):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            scaled = self._bg_pixmap.scaled(
                self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
            x = (self.width()  - scaled.width())  // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        super().paintEvent(event)

    def _update_background(self, img_name, mode="light"):
        p = img_path(img_name)
        self._bg_pixmap = QPixmap(p) if os.path.exists(p) else None
        self.setStyleSheet(get_qss(THEME_PALETTES[mode]))
        self.update()

    def _toggle_sidebar(self):
        self._sidebar_collapsed = not getattr(self, "_sidebar_collapsed", False)
        if self._sidebar_collapsed:
            self._sb.setFixedWidth(60)
            self._lbl_sub.hide()
            self._lbl_prog.hide()
            self._lbl_conn.hide()
            self._lbl_ver.hide()
            for key, btn in self._nav_btns.items():
                icon = next(x[1] for x in self._nav_data if x[0] == key)
                btn.setText(f" {icon} ")
                btn.setStyleSheet("text-align: center;")
        else:
            self._sb.setFixedWidth(256)
            self._lbl_sub.show()
            self._lbl_prog.show()
            self._lbl_conn.show()
            self._lbl_ver.show()
            for key, btn in self._nav_btns.items():
                icon, label = next((x[1], x[2]) for x in self._nav_data if x[0] == key)
                btn.setText(f" {icon}  {label}")
                btn.setStyleSheet("text-align: left; padding-left: 10px;")

    def switch(self, key):
        if key == "gate_db" and not getattr(self, "_gate_db_unlocked", False):
            self._prompt_password()
            return
        
        self.workspace.setCurrentWidget(self.pages[key])
        
        for k, btn in self._nav_btns.items():
            if k == key:
                btn.setStyleSheet(f"background-color: {COLORS['pink']}; text-align: left; padding-left: 10px;")
            else:
                btn.setStyleSheet("background-color: transparent; text-align: left; padding-left: 10px;")

    def _prompt_password(self):
        ADMIN_PW = os.getenv("ADMIN_PASSWORD", "focusfox2024")
        pop = QMessageBox(self)
        pop.setWindowTitle("🔒 Protected Area")
        pop.setText("Admin Access Required.\nEnter admin password:")
        
        entry = QLineEdit(pop)
        entry.setEchoMode(QLineEdit.Password)
        pop.layout().addWidget(entry)
        
        pop.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if pop.exec() == QMessageBox.Ok:
            if entry.text() == ADMIN_PW:
                self._gate_db_unlocked = True
                self.switch("gate_db")
                self._gdb_load_subjects()
            else:
                QMessageBox.critical(self, "Error", "Incorrect password.")

    def _build_pages(self):
        self.pages["guide"]       = self._page_guide()
        self.pages["yt"]          = self._page_yt()
        self.pages["gate"]        = self._page_gate()
        self.pages["college_img"] = self._page_college_img()
        self.pages["gate_img"]    = self._page_gate_img()
        self.pages["gate_db"]     = self._page_gate_db()
        self.pages["todo"]        = self._page_todo()
        self.pages["spotify"]     = self._page_spotify()

        for k, w in self.pages.items():
            self.workspace.addWidget(w)

    def _page_frame(self, title, key):
        f = QWidget()
        lay = QVBoxLayout(f)
        lay.setContentsMargins(0, 0, 0, 0)
        
        hdr = QHBoxLayout()
        lbl = QLabel(title)
        lbl.setStyleSheet("font-family: 'Pixelify Sans'; font-size: 18px; font-weight: bold;")
        hdr.addWidget(lbl)
        hdr.addStretch()

        btn_h = QPushButton("❓ Help")
        btn_h.clicked.connect(lambda: self._show_help(key))
        hdr.addWidget(btn_h)
        lay.addLayout(hdr)
        
        f.main_layout = lay
        return f

    def _page_todo(self):
        p = self._page_frame("📝  Developer Tasks", "todo")
        win, body = self._window("DEVELOPER_TODO.EXE", "coffee")
        p.main_layout.addWidget(win, 1)

        # Top layout for adding tasks
        top_lay = QHBoxLayout()
        self.todo_input = QLineEdit()
        self.todo_input.setPlaceholderText("Enter new task here...")
        self.todo_input.returnPressed.connect(self._add_todo_clicked)
        top_lay.addWidget(self.todo_input, 1)

        btn_add = QPushButton("➕ Add Task")
        btn_add.clicked.connect(self._add_todo_clicked)
        top_lay.addWidget(btn_add)
        body.layout().addLayout(top_lay)

        # Scroll Area for todo list
        self.todo_scroll = QScrollArea()
        self.todo_scroll.setWidgetResizable(True)
        self.todo_scroll.setStyleSheet("background: transparent; border: none;")
        body.layout().addWidget(self.todo_scroll, 1)

        self.todo_container = QWidget()
        self.todo_list_lay = QVBoxLayout(self.todo_container)
        self.todo_list_lay.setContentsMargins(0, 8, 0, 8)
        self.todo_list_lay.setSpacing(8)
        self.todo_list_lay.addStretch(1)
        self.todo_scroll.setWidget(self.todo_container)

        # Fetch initial tasks
        QTimer.singleShot(100, self._load_todos)
        return p

    def _load_todos(self):
        def _fetch():
            if not _auth_ok:
                return
            items = firebase_auth.get_todos()
            QTimer.singleShot(0, lambda: self._populate_todos(items))
        threading.Thread(target=_fetch, daemon=True).start()

    def _populate_todos(self, items):
        # Clear old rows
        while self.todo_list_lay.count() > 1:
            w = self.todo_list_lay.takeAt(0).widget()
            if w: w.deleteLater()

        for item in items:
            self._add_todo_row_ui(item)

    def _add_todo_row_ui(self, item):
        row = QFrame()
        row.setObjectName("rowcard")
        row_lay = QHBoxLayout(row)
        row_lay.setContentsMargins(10, 8, 10, 8)
        row_lay.setSpacing(10)

        # Checkbox button
        chk = QPushButton("✔️" if item.get("completed") else "⬜")
        chk.setFixedSize(28, 28)
        chk.setStyleSheet("font-size: 11px; padding: 0px;")
        
        # Text label
        lbl = QLabel(item.get("text", ""))
        lbl.setWordWrap(True)
        if item.get("completed"):
            lbl.setStyleSheet(f"color: {COLORS['muted']}; text-decoration: line-through;")
        else:
            lbl.setStyleSheet(f"color: {COLORS['text']};")

        # Toggle handler
        def _toggle(checked=False, i=item, c=chk, l=lbl):
            new_val = not i.get("completed")
            i["completed"] = new_val
            c.setText("✔️" if new_val else "⬜")
            if new_val:
                l.setStyleSheet(f"color: {COLORS['muted']}; text-decoration: line-through;")
            else:
                l.setStyleSheet(f"color: {COLORS['text']};")
            threading.Thread(target=lambda: firebase_auth.update_todo_completed(i["id"], new_val), daemon=True).start()

        chk.clicked.connect(_toggle)
        row_lay.addWidget(chk)
        row_lay.addWidget(lbl, 1)

        # Delete button
        btn_del = QPushButton("🗑")
        btn_del.setFixedSize(28, 28)
        btn_del.setStyleSheet("font-size: 11px; padding: 0px;")
        
        def _delete(checked=False, i=item, r=row):
            r.deleteLater()
            threading.Thread(target=lambda: firebase_auth.delete_todo(i["id"]), daemon=True).start()

        btn_del.clicked.connect(_delete)
        row_lay.addWidget(btn_del)

        self.todo_list_lay.insertWidget(self.todo_list_lay.count() - 1, row)

    def _page_spotify(self):
        p = self._page_frame("🎵  Focus Music Player", "spotify")
        win, body = self._window("SPOTIFY_LAUNCHER.EXE", "coffee")
        p.main_layout.addWidget(win, 1)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        body.layout().addWidget(scroll)

        sc_widget = QWidget()
        sc_lay = QVBoxLayout(sc_widget)
        sc_lay.setContentsMargins(10, 10, 10, 10)
        sc_lay.setSpacing(12)
        scroll.setWidget(sc_widget)

        # Welcome text
        intro = QLabel("🎧 Focus Sessions Spotify Player\nLaunch curated or custom focus playlists directly in your Spotify application or web browser.")
        intro.setStyleSheet("font-family: 'Pixelify Sans'; font-size: 12px; color: #E8E2FF;")
        intro.setWordWrap(True)
        sc_lay.addWidget(intro)

        # Custom Playlist input row
        custom_box = QFrame()
        custom_box.setObjectName("card")
        cb_lay = QVBoxLayout(custom_box)
        cb_lay.setContentsMargins(12, 12, 12, 12)
        cb_lay.setSpacing(8)

        cb_title = QLabel("🔗 Custom Spotify Playlist Link:")
        cb_title.setStyleSheet("font-family: 'Pixelify Sans'; font-weight: bold; font-size: 12px;")
        cb_lay.addWidget(cb_title)

        in_lay = QHBoxLayout()
        self.spotify_input = QLineEdit()
        self.spotify_input.setPlaceholderText("Paste Spotify playlist link here (e.g., https://open.spotify.com/playlist/...)")
        self.spotify_input.setStyleSheet("font-size: 11px;")
        in_lay.addWidget(self.spotify_input, 1)

        btn_save = QPushButton("💾 Save")
        btn_save.setFixedWidth(70)
        btn_save.clicked.connect(self._save_spotify_playlist)
        in_lay.addWidget(btn_save)

        btn_play_custom = QPushButton("▶️ Play Custom")
        btn_play_custom.setFixedWidth(100)
        btn_play_custom.setStyleSheet("background-color: #A8D99B; color: #1C1B29; font-weight: bold;")
        btn_play_custom.clicked.connect(self._play_custom_playlist)
        in_lay.addWidget(btn_play_custom)
        cb_lay.addLayout(in_lay)
        sc_lay.addWidget(custom_box)

        # Grid of curated playlists
        grid_title = QLabel("🎵 Curated Focus Playlists:")
        grid_title.setStyleSheet("font-family: 'Pixelify Sans'; font-weight: bold; font-size: 13px; margin-top: 10px;")
        sc_lay.addWidget(grid_title)

        grid = QGridLayout()
        grid.setSpacing(12)
        sc_lay.addLayout(grid)

        # Popular focus playlists
        curated_playlists = [
            ("Lofi Beats 🌸", "37i9dQZF1DWWQRwui0EXPn", "Chill beats to study or relax to."),
            ("Deep Focus 🧠", "37i9dQZF1DXcBWIGmqZ7XF", "Keep calm and focus with ambient sounds."),
            ("Chill Lofi Study 📚", "37i9dQZF1DX8UebhpwM67e", "Cozy lofi hip hop playlist."),
            ("Jazz Vibes 🎷", "37i9dQZF1DX0SMZkqi27Z2", "Relaxing jazz tunes for coding sessions."),
            ("Synthwave Chill 🌌", "37i9dQZF1DXdLTE75A7KXO", "Retro futuristic electronic background vibes."),
            ("Peaceful Piano 🎹", "37i9dQZF1DX4sWSpwq3LiO", "Beautiful, gentle solo piano works.")
        ]

        for idx, (title, playlist_id, desc) in enumerate(curated_playlists):
            card = QFrame()
            card.setObjectName("card")
            card_lay = QVBoxLayout(card)
            card_lay.setContentsMargins(12, 12, 12, 12)
            card_lay.setSpacing(6)

            t_lbl = QLabel(title)
            t_lbl.setStyleSheet("font-family: 'Pixelify Sans'; font-size: 13px; font-weight: bold; color: #F3A6C3;")
            card_lay.addWidget(t_lbl)

            d_lbl = QLabel(desc)
            d_lbl.setStyleSheet("font-size: 11px; color: #8D89A5;")
            d_lbl.setWordWrap(True)
            card_lay.addWidget(d_lbl)

            btn_lay = QHBoxLayout()
            # Play in Spotify App (using URI scheme)
            btn_app = QPushButton("🚀 Open App")
            btn_app.clicked.connect(lambda checked=False, pid=playlist_id: self._play_spotify(pid, use_app=True))
            btn_lay.addWidget(btn_app)

            # Play in browser
            btn_web = QPushButton("🌐 Open Web")
            btn_web.clicked.connect(lambda checked=False, pid=playlist_id: self._play_spotify(pid, use_app=False))
            btn_lay.addWidget(btn_web)

            card_lay.addLayout(btn_lay)
            grid.addWidget(card, idx // 2, idx % 2)

        # Load user saved playlist URL if any
        QTimer.singleShot(100, self._load_saved_spotify_playlist)
        return p

    def _play_spotify(self, playlist_id, use_app=True):
        if use_app:
            # spotify:playlist:<id>
            uri = f"spotify:playlist:{playlist_id}"
            webbrowser.open(uri)
            firebase_auth.log_action("PLAY_MUSIC", content_type="spotify_app", subject=playlist_id)
        else:
            url = f"https://open.spotify.com/playlist/{playlist_id}"
            webbrowser.open(url)
            firebase_auth.log_action("PLAY_MUSIC", content_type="spotify_web", subject=playlist_id)

    def _load_saved_spotify_playlist(self):
        def _fetch():
            if _auth_ok:
                url = firebase_auth.get_spotify_playlist()
                QTimer.singleShot(0, lambda: self.spotify_input.setText(url))
        threading.Thread(target=_fetch, daemon=True).start()

    def _save_spotify_playlist(self):
        url = self.spotify_input.text().strip()
        def _save():
            if _auth_ok:
                firebase_auth.save_spotify_playlist(url)
                QTimer.singleShot(0, lambda: QMessageBox.information(self, "Saved", "Spotify playlist link saved!"))
        threading.Thread(target=_save, daemon=True).start()

    def _play_custom_playlist(self):
        url = self.spotify_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Warning", "Please paste a Spotify playlist link first.")
            return
        
        # Try to extract playlist ID
        playlist_id = ""
        if "spotify:playlist:" in url:
            playlist_id = url.split("spotify:playlist:")[-1].split("?")[0]
        elif "open.spotify.com/playlist/" in url:
            playlist_id = url.split("open.spotify.com/playlist/")[-1].split("?")[0]

        if playlist_id:
            # Default to opening in app first
            webbrowser.open(f"spotify:playlist:{playlist_id}")
            firebase_auth.log_action("PLAY_MUSIC", content_type="spotify_custom_app", subject=playlist_id)
        else:
            # fallback to opening the url raw
            webbrowser.open(url)
            firebase_auth.log_action("PLAY_MUSIC", content_type="spotify_custom_raw", subject=url)

    def _add_todo_clicked(self):
        text = self.todo_input.text().strip()
        if not text:
            return
        self.todo_input.clear()

        # Optimistically add to UI first
        temp_item = {"id": "temp", "text": text, "completed": False}
        self._add_todo_row_ui(temp_item)

        # Save to Firestore and reload after a short delay so SERVER_TIMESTAMP resolves
        def _save():
            if _auth_ok:
                firebase_auth.add_todo(text)
                import time; time.sleep(1.5)
                self._load_todos()
        threading.Thread(target=_save, daemon=True).start()

    def _show_help(self, key):
        fallback = HELP.get(key, ("fox_happy.png", "No guide available."))
        
        loading = QMessageBox(self)
        loading.setWindowTitle("Loading Guide...")
        loading.setText("Fetching detailed guidelines and database schema from Firestore...")
        loading.setStandardButtons(QMessageBox.Cancel)
        loading.show()
        
        finished = False
        
        def display_guide(data):
            nonlocal finished
            if finished:
                return
            finished = True
            loading.close()
            
            full_text = data.get("text", "")
            if data.get("schema"):
                full_text += "\n\n" + "="*50 + "\n" + data.get("schema")
                
            img_name = data.get("image", "fox_happy.png")
            pop = GuideDialog(self, data.get("title", "Guide"), full_text, img_name)
            pop.exec()

        # Start loading thread
        self._guide_thread = _GuideWorker(key, fallback)
        self._guide_thread.result_ready.connect(display_guide)
        self._guide_thread.start()

        # Auto-timeout after 2.5 seconds
        def on_timeout():
            nonlocal finished
            if not finished:
                finished = True
                loading.close()
                display_guide({
                    "title": f"Help Guide ({key})",
                    "text": fallback[1],
                    "image": fallback[0],
                    "schema": "Database schema offline (network timeout)."
                })

        QTimer.singleShot(2500, on_timeout)

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 1 — GUIDE / HOME
    # ══════════════════════════════════════════════════════════════════════════
    def _page_guide(self):
        p = self._page_frame("📚  Dashboard Overview", "guide")
        win, body = self._window("DESKTOP_HOME.EXE", "fox")
        p.main_layout.addWidget(win, 1)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        body.layout().addWidget(scroll)

        sc_widget = QWidget()
        sc_lay = QVBoxLayout(sc_widget)
        sc_lay.setContentsMargins(10, 10, 10, 10)
        sc_lay.setSpacing(12)
        scroll.setWidget(sc_widget)

        # Welcome banner
        banner = QFrame()
        banner.setObjectName("banner")
        b_lay = QHBoxLayout(banner)
        b_lay.setContentsMargins(16, 16, 16, 16)
        b_lay.setSpacing(16)
        if self.mascots.get("fox"):
            lbl_f = QLabel()
            lbl_f.setPixmap(self.mascots["fox"].scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            b_lay.addWidget(lbl_f)
        
        lbl_vbox = QVBoxLayout()
        lbl_vbox.setSpacing(4)
        lbl_title = QLabel("Welcome to your Cozy Hub!")
        lbl_title.setStyleSheet("font-family: 'Pixelify Sans'; font-size: 16px; font-weight: bold;")
        lbl_vbox.addWidget(lbl_title)
        
        lbl_desc = QLabel("All your FocusFox admin tools in one cozy workspace.")
        lbl_desc.setStyleSheet("font-family: 'Pixelify Sans'; font-size: 12px;")
        lbl_vbox.addWidget(lbl_desc)
        b_lay.addLayout(lbl_vbox, 1)
        sc_lay.addWidget(banner)

        sections = [
            ("panda_r", "📺", "College PYQ & YouTube Uploader",
             "Manage subjects, branches, years. Upload YouTube lecture links and import bulk PYQ JSON data.",
             lambda: self.switch("yt")),
            ("owl",     "🎓", "GATE Admin Portal",
             "Split large GATE PDFs into chapters. Import GATE questions, topics, options and papers.",
             lambda: self.switch("gate")),
            ("fox",     "🖼️",  "College Image Uploader",
             "Upload step-by-step solution images for college questions to ImageKit CDN.",
             lambda: self.switch("college_img")),
            ("lil_fox", "📐", "GATE Image Uploader",
             "Upload images for GATE question bodies or individual answer options.",
             lambda: self.switch("gate_img")),
            ("raccoon", "📁", "GATE DB Editor (Protected)",
             "View, edit, and delete GATE questions directly in your Supabase database.",
             lambda: self.switch("gate_db")),
        ]

        for mk, icon, title, desc, action in sections:
            c = QFrame()
            c.setObjectName("card")
            c_lay = QHBoxLayout(c)
            c_lay.setContentsMargins(14, 14, 14, 14)
            c_lay.setSpacing(14)

            if self.mascots.get(mk):
                lbl_icon = QLabel()
                lbl_icon.setPixmap(self.mascots[mk].scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                c_lay.addWidget(lbl_icon)

            text_lay = QVBoxLayout()
            text_lay.setSpacing(4)
            
            t_lbl = QLabel(f"{icon}  {title}")
            t_lbl.setStyleSheet("font-family: 'Pixelify Sans'; font-size: 13px; font-weight: bold;")
            text_lay.addWidget(t_lbl)

            d_lbl = QLabel(desc)
            d_lbl.setStyleSheet("font-family: 'Pixelify Sans'; font-size: 11px;")
            d_lbl.setWordWrap(True)
            text_lay.addWidget(d_lbl)
            
            c_lay.addLayout(text_lay, 1)

            btn = QPushButton("Launch")
            btn.setFixedWidth(80)
            btn.clicked.connect(action)
            c_lay.addWidget(btn, 0, Qt.AlignVCenter)

            sc_lay.addWidget(c)

        # Tips card
        tip = QFrame()
        tip.setObjectName("tip")
        tip_lay = QVBoxLayout(tip)
        tip_lay.setContentsMargins(16, 16, 16, 16)
        tip_lay.setSpacing(8)
        
        t_title = QLabel("💡  Tips")
        t_title.setStyleSheet("font-family: 'Pixelify Sans'; font-size: 13px; font-weight: bold;")
        tip_lay.addWidget(t_title)

        tips_text = (
            "• Every section has a  ?  button for detailed help.\n"
            "• All uploads run in the background — UI stays snappy.\n"
            "• Credentials come from your .env file — never shown in-app."
        )
        t_desc = QLabel(tips_text)
        t_desc.setStyleSheet("font-family: 'Pixelify Sans'; font-size: 11px;")
        t_desc.setWordWrap(True)
        tip_lay.addWidget(t_desc)
        sc_lay.addWidget(tip)

        sc_lay.addStretch(1)

        return p

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 2 — COLLEGE PYQ & YT
    # ══════════════════════════════════════════════════════════════════════════
    def _page_yt(self):
        p = self._page_frame("🎥  College PYQ & YT Link Uploader", "yt")
        self.yt_subjects = []
        self.yt_subject_map = {}
        self._yt_filter_mode = "ALL"

        tabs = QTabWidget()
        p.main_layout.addWidget(tabs, 1)

        # Tab 1: YouTube
        t1 = QWidget()
        t1_lay = QVBoxLayout(t1)
        
        c1 = QFrame()
        c1.setObjectName("card")
        c1_lay = QVBoxLayout(c1)
        
        c1_lay.addWidget(QLabel("Subject Filter"))
        
        filt_row = QHBoxLayout()
        self._yt_btn_all = QPushButton("ALL")
        self._yt_btn_with = QPushButton("WITH LINKS")
        self._yt_btn_wout = QPushButton("WITHOUT LINKS")
        
        self._yt_btn_all.clicked.connect(lambda: self._yt_set_filter("ALL"))
        self._yt_btn_with.clicked.connect(lambda: self._yt_set_filter("WITH LINKS"))
        self._yt_btn_wout.clicked.connect(lambda: self._yt_set_filter("WITHOUT LINKS"))
        
        filt_row.addWidget(self._yt_btn_all)
        filt_row.addWidget(self._yt_btn_with)
        filt_row.addWidget(self._yt_btn_wout)
        c1_lay.addLayout(filt_row)

        self._yt_sub_sel = QComboBox()
        self._yt_sub_sel.currentTextChanged.connect(self._yt_subject_selected)
        c1_lay.addWidget(self._yt_sub_sel)
        t1_lay.addWidget(c1)

        c2 = QFrame()
        c2.setObjectName("card")
        c2_lay = QVBoxLayout(c2)
        c2_lay.addWidget(QLabel("YouTube Lecture URLs (one per line)"))
        
        self._yt_txt_links = QTextEdit()
        c2_lay.addWidget(self._yt_txt_links)

        btn_save = QPushButton("💾  Save YouTube Links")
        btn_save.clicked.connect(self._yt_save_links)
        c2_lay.addWidget(btn_save)
        t1_lay.addWidget(c2, 1)

        tabs.addTab(t1, "YouTube Links")

        # Tab 2: Subject & Branch
        t2 = QWidget()
        t2_lay = QVBoxLayout(t2)
        
        c3 = QFrame()
        c3.setObjectName("card")
        c3_lay = QVBoxLayout(c3)
        c3_lay.addWidget(QLabel("Add New Subject"))
        
        self.ent_sn = QLineEdit(); self.ent_sn.setPlaceholderText("Subject Name")
        self.ent_sc = QLineEdit(); self.ent_sc.setPlaceholderText("Subject Code")
        self.ent_sp = QLineEdit(); self.ent_sp.setPlaceholderText("PYQ Drive Link")
        self.ent_sno = QLineEdit(); self.ent_sno.setPlaceholderText("Notes Drive Link")
        self.ent_sco = QLineEdit(); self.ent_sco.setPlaceholderText("Course Outcome Link")
        
        c3_lay.addWidget(self.ent_sn)
        c3_lay.addWidget(self.ent_sc)
        c3_lay.addWidget(self.ent_sp)
        c3_lay.addWidget(self.ent_sno)
        c3_lay.addWidget(self.ent_sco)

        # Mapping dropdowns
        c3_lay.addWidget(QLabel("Map New Subject To branch/year/sem"))
        self._yt_map_branch_dr = QComboBox()
        self._yt_map_year_dr = QComboBox()
        self._yt_map_sem_dr = QComboBox()
        self._yt_map_sem_dr.addItems([str(i) for i in range(1, 9)])
        
        c3_lay.addWidget(self._yt_map_branch_dr)
        c3_lay.addWidget(self._yt_map_year_dr)
        c3_lay.addWidget(self._yt_map_sem_dr)

        btn_sub = QPushButton("✚  CREATE SUBJECT & MAP")
        btn_sub.clicked.connect(self._create_subject)
        c3_lay.addWidget(btn_sub)
        t2_lay.addWidget(c3)

        # Branch / Year Managers
        c4 = QFrame()
        c4.setObjectName("card")
        c4_lay = QHBoxLayout(c4)
        
        b_box = QVBoxLayout()
        b_box.addWidget(QLabel("Add New Branch"))
        self.ent_bn = QLineEdit()
        b_box.addWidget(self.ent_bn)
        btn_b = QPushButton("✚  ADD BRANCH")
        btn_b.clicked.connect(self._create_branch)
        b_box.addWidget(btn_b)
        c4_lay.addLayout(b_box)

        y_box = QVBoxLayout()
        y_box.addWidget(QLabel("Add New Year"))
        self.ent_yn = QLineEdit()
        y_box.addWidget(self.ent_yn)
        btn_y = QPushButton("✚  ADD YEAR")
        btn_y.clicked.connect(self._create_year)
        y_box.addWidget(btn_y)
        c4_lay.addLayout(y_box)
        t2_lay.addWidget(c4)

        tabs.addTab(t2, "Subject & Branch")

        # Tab 3: JSON Importer
        t3 = QWidget()
        t3_lay = QVBoxLayout(t3)
        
        c5 = QFrame()
        c5.setObjectName("card")
        c5_lay = QVBoxLayout(c5)
        c5_lay.addWidget(QLabel("Import Questions JSON"))
        
        self.json_sub = QComboBox()
        c5_lay.addWidget(self.json_sub)

        self.btn_json = QPushButton("📂  Select JSON & Import")
        self.btn_json.clicked.connect(self._import_college_json)
        c5_lay.addWidget(self.btn_json)
        t3_lay.addWidget(c5)

        c6 = QFrame()
        c6.setObjectName("card")
        c6_lay = QVBoxLayout(c6)
        c6_lay.addWidget(QLabel("Import logs"))
        self.college_log = QTextEdit()
        c6_lay.addWidget(self.college_log)
        t3_lay.addWidget(c6, 1)

        tabs.addTab(t3, "JSON Importer")

        threading.Thread(target=self._yt_load, daemon=True).start()
        return p

    def _yt_load(self):
        if not self.supabase: return
        try:
            r = self.supabase.table("subjects").select("id,name,code,yt_links").order("name").execute()
            self.yt_subjects = r.data
            self.yt_subject_map = {f"{s['name']} ({s['code']})": s for s in r.data}

            self._yt_sub_sel.clear()
            self._yt_sub_sel.addItems(list(self.yt_subject_map.keys()))
            self.json_sub.clear()
            self.json_sub.addItems(list(self.yt_subject_map.keys()))

            # Fetch branches
            rb = self.supabase.table("branches").select("id,name").order("name").execute()
            self._yt_branches = rb.data
            self._yt_map_branch_dr.clear()
            self._yt_map_branch_dr.addItems([b["name"] for b in rb.data])

            # Fetch years
            ry = self.supabase.table("years").select("id,name").order("name").execute()
            self._yt_years = ry.data
            self._yt_map_year_dr.clear()
            self._yt_map_year_dr.addItems([y["name"] for y in ry.data])
        except Exception as e:
            print(f"Error loading YT subjects: {e}")

    def _yt_set_filter(self, mode):
        self._yt_filter_mode = mode
        # Re-filter active subjects
        filtered = []
        for s in self.yt_subjects:
            links = s.get("yt_links") or []
            if mode == "ALL":
                filtered.append(s)
            elif mode == "WITH LINKS" and len(links) > 0:
                filtered.append(s)
            elif mode == "WITHOUT LINKS" and len(links) == 0:
                filtered.append(s)

        self._yt_sub_sel.clear()
        self._yt_sub_sel.addItems([f"{s['name']} ({s['code']})" for s in filtered])

    def _yt_subject_selected(self, val):
        s = self.yt_subject_map.get(val)
        if s:
            links = s.get("yt_links") or []
            self._yt_txt_links.setPlainText("\n".join(links))

    def _yt_save_links(self):
        sn = self._yt_sub_sel.currentText()
        s = self.yt_subject_map.get(sn)
        if not s: return
        urls = [line.strip() for line in self._yt_txt_links.toPlainText().split("\n") if line.strip()]
        try:
            self.supabase.table("subjects").update({"yt_links": urls}).eq("id", s["id"]).execute()
            QMessageBox.information(self, "Saved", "YouTube links saved successfully!")
            self._yt_load()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _create_subject(self):
        s_name = self.ent_sn.text().strip()
        s_code = self.ent_sc.text().strip()
        pyq_l  = self.ent_sp.text().strip() or None
        note_l = self.ent_sno.text().strip() or None
        co_l   = self.ent_sco.text().strip() or None

        if not s_name or not s_code:
            QMessageBox.warning(self, "Warning", "Subject Name and Code are required.")
            return

        b_name = self._yt_map_branch_dr.currentText()
        y_name = self._yt_map_year_dr.currentText()
        sem_val = int(self._yt_map_sem_dr.currentText())

        br_obj = next((x for x in self._yt_branches if x["name"] == b_name), None)
        yr_obj = next((x for x in self._yt_years if x["name"] == y_name), None)

        if not br_obj or not yr_obj: return

        try:
            res_s = self.supabase.table("subjects").insert({
                "name": s_name, "code": s_code,
                "pyq_drive_link": pyq_l, "notes_drive_link": note_l,
                "course_outcome_link": co_l
            }).execute()

            if res_s.data:
                subj_id = res_s.data[0]["id"]
                self.supabase.table("branch_subjects").insert({
                    "branch_id": br_obj["id"],
                    "subject_id": subj_id,
                    "year_id": yr_obj["id"],
                    "semester": sem_val
                }).execute()
                QMessageBox.information(self, "Success", f"Subject '{s_name}' created!")
                self._yt_load()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _create_branch(self):
        n = self.ent_bn.text().strip()
        if not n: return
        try:
            self.supabase.table("branches").insert({"name": n}).execute()
            QMessageBox.information(self, "Done", f"Branch '{n}' created!")
            self.ent_bn.clear()
            self._yt_load()
        except Exception as e: QMessageBox.critical(self, "Error", str(e))

    def _create_year(self):
        n = self.ent_yn.text().strip()
        if not n: return
        try:
            self.supabase.table("years").insert({"name": n}).execute()
            QMessageBox.information(self, "Done", f"Year '{n}' created!")
            self.ent_yn.clear()
            self._yt_load()
        except Exception as e: QMessageBox.critical(self, "Error", str(e))

    def _import_college_json(self):
        fp, _ = QFileDialog.getOpenFileName(self, "Import JSON", "", "JSON (*.json)")
        if not fp: return
        s = self.yt_subject_map.get(self.json_sub.currentText())
        if not s: return
        self.btn_json.setEnabled(False)
        threading.Thread(target=self._college_json_work, args=(s["id"], fp), daemon=True).start()

    def _college_json_work(self, sid, fp):
        def log(m): self.college_log.append(m)
        try:
            with open(fp, "r", encoding="utf-8") as f: data = json.load(f)
            topics = data.get("topics", []); qs = data.get("questions", [])
            log(f"Importing: {len(topics)} topics, {len(qs)} questions")
            tm = {}
            for t in topics:
                r = self.supabase.table("topics").insert({
                    "subject_id": sid, "name": t["topic_name"], "summary": t.get("summary")
                }).execute()
                if r.data: tm[t["topic_name"]] = r.data[0]["id"]; log(f"  Topic: {t['topic_name']}")
            for i, q in enumerate(qs):
                rq = self.supabase.table("questions").insert({
                    "question_text": q["question_text"], "difficulty": q.get("difficulty", "easy")
                }).execute()
                if not rq.data: continue
                qid = rq.data[0]["id"]
                for tn in q.get("topics", []):
                    tid = tm.get(tn)
                    if tid: self.supabase.table("question_topics").insert({"question_id":qid,"topic_id":tid}).execute()
                for src in q.get("pyq_sources", []):
                    ex = self.supabase.table("pyq_sources").select("id").match({**src,"subject_id":sid}).execute()
                    pid = ex.data[0]["id"] if ex.data else (self.supabase.table("pyq_sources").insert({**src,"subject_id":sid}).execute().data or [{}])[0].get("id")
                    if pid: self.supabase.table("question_pyq_map").insert({"question_id":qid,"pyq_source_id":pid}).execute()
                log(f"  Q {i+1}/{len(qs)}")
            log("✅ Done!")
            QMessageBox.information(self, "Done", "Import complete!")
        except Exception as e:
            log(f"ERROR: {e}"); QMessageBox.critical(self, "Error", str(e))
        finally: self.btn_json.setEnabled(True)

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 3 — GATE ADMIN
    # ══════════════════════════════════════════════════════════════════════════
    def _page_gate(self):
        p = self._page_frame("🎓  GATE Admin Portal", "gate")
        tabs = QTabWidget()
        p.main_layout.addWidget(tabs, 1)

        ts = QWidget()
        ts_lay = QVBoxLayout(ts)
        
        # Upload Bar Card
        u_card = QFrame()
        u_card.setObjectName("card")
        u_card_lay = QVBoxLayout(u_card)
        u_card_lay.addWidget(QLabel("Upload your GATE Question Bank PDF"))

        br_fr = QFrame()
        br_fr_lay = QHBoxLayout(br_fr)
        self._pdf_file_path = ""
        self._pdf_total_pages = 0
        self._pdf_name_lbl = QLabel("📁  Select a PDF file to begin...")
        br_fr_lay.addWidget(self._pdf_name_lbl)

        self._pdf_browse_btn = QPushButton("Browse File")
        self._pdf_browse_btn.clicked.connect(self._pdf_splitter_browse)
        br_fr_lay.addWidget(self._pdf_browse_btn)
        u_card_lay.addWidget(br_fr)
        ts_lay.addWidget(u_card)

        # Splits Setup Layout Area
        splits_fr = QFrame()
        splits_fr.setObjectName("card")
        splits_lay = QVBoxLayout(splits_fr)
        splits_lay.addWidget(QLabel("Define Custom Splits"))

        self._split_scroll_widget = QWidget()
        self._split_scroll_lay = QVBoxLayout(self._split_scroll_widget)
        self._split_scroll = QScrollArea()
        self._split_scroll.setWidgetResizable(True)
        self._split_scroll.setWidget(self._split_scroll_widget)
        splits_lay.addWidget(self._split_scroll)

        self._pdf_split_ranges = []

        side_fr = QFrame()
        side_lay = QHBoxLayout(side_fr)
        btn_add = QPushButton("➕ Add Range")
        btn_add.clicked.connect(self._pdf_add_range_row)
        btn_clr = QPushButton("🧹 Clear All")
        btn_clr.clicked.connect(self._pdf_clear_all_ranges)
        side_lay.addWidget(btn_add)
        side_lay.addWidget(btn_clr)
        splits_lay.addWidget(side_fr)

        self._pdf_split_run_btn = QPushButton("🚀 Process & Split PDF")
        self._pdf_split_run_btn.setStyleSheet(f"background-color: {COLORS['red']}; color: white;")
        self._pdf_split_run_btn.clicked.connect(self._pdf_run_splits)
        splits_lay.addWidget(self._pdf_split_run_btn)
        ts_lay.addWidget(splits_fr, 1)

        tabs.addTab(ts, "🗂  PDF Splitter")

        # Importer Tab
        ti = QWidget()
        ti_lay = QVBoxLayout(ti)
        tic = QFrame()
        tic.setObjectName("card")
        tic_lay = QVBoxLayout(tic)
        tic_lay.addWidget(QLabel("Import GATE JSON into gate_questions"))
        self.btn_gate_imp = QPushButton("📂  Browse & Import JSON")
        self.btn_gate_imp.clicked.connect(self._import_gate_json)
        tic_lay.addWidget(self.btn_gate_imp)
        ti_lay.addWidget(tic)

        gl = QFrame()
        gl.setObjectName("card")
        gl_lay = QVBoxLayout(gl)
        gl_lay.addWidget(QLabel("Import Log"))
        self.gate_log = QTextEdit()
        gl_lay.addWidget(self.gate_log)
        ti_lay.addWidget(gl, 1)

        tabs.addTab(ti, "📥  JSON Importer")
        return p

    def _pdf_splitter_browse(self):
        fp, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF (*.pdf)")
        if not fp: return
        self._pdf_file_path = fp
        try:
            rdr = PdfReader(fp)
            self._pdf_total_pages = len(rdr.pages)
            self._pdf_name_lbl.setText(f"📄  {os.path.basename(fp)} ({self._pdf_total_pages} pages)")
            self._pdf_clear_all_ranges()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed: {e}")

    def _pdf_clear_all_ranges(self):
        for r in self._pdf_split_ranges:
            r["frame"].deleteLater()
        self._pdf_split_ranges = []
        self._pdf_add_range_row()

    def _pdf_add_range_row(self):
        row_idx = len(self._pdf_split_ranges) + 1
        row = QFrame()
        row.setObjectName("rowcard")
        r_lay = QHBoxLayout(row)

        lbl = QLabel(f"Range #{row_idx}")
        r_lay.addWidget(lbl)

        name_ent = QLineEdit(f"Split_Part_{row_idx}")
        r_lay.addWidget(name_ent)

        start_ent = QLineEdit("1")
        r_lay.addWidget(start_ent)

        end_ent = QLineEdit(str(self._pdf_total_pages or 5))
        r_lay.addWidget(end_ent)

        btn_del = QPushButton("🗑")
        btn_del.setFixedWidth(30)
        btn_del.clicked.connect(lambda: self._pdf_delete_range_row(row))
        r_lay.addWidget(btn_del)

        self._split_scroll_lay.addWidget(row)
        self._pdf_split_ranges.append({
            "frame": row,
            "name_ent": name_ent,
            "start_ent": start_ent,
            "end_ent": end_ent
        })

    def _pdf_delete_range_row(self, row_widget):
        if len(self._pdf_split_ranges) <= 1:
            QMessageBox.warning(self, "Warning", "Must keep at least one split range.")
            return
        row_widget.deleteLater()
        self._pdf_split_ranges = [r for r in self._pdf_split_ranges if r["frame"] != row_widget]

    def _pdf_run_splits(self):
        if not self._pdf_file_path or not os.path.exists(self._pdf_file_path):
            QMessageBox.warning(self, "Warning", "Select a valid PDF first.")
            return
        parsed_ranges = []
        for idx, r in enumerate(self._pdf_split_ranges):
            name = r["name_ent"].text().strip()
            if not name.endswith(".pdf"): name += ".pdf"
            try:
                s = int(r["start_ent"].text())
                e = int(r["end_ent"].text())
            except ValueError:
                QMessageBox.critical(self, "Error", f"Invalid page numbers in Range #{idx+1}.")
                return
            parsed_ranges.append((name, s - 1, e))

        out_dir = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if not out_dir: return

        try:
            rdr = PdfReader(self._pdf_file_path)
            for out_name, s, e in parsed_ranges:
                w = PdfWriter()
                for page_num in range(s, e):
                    w.add_page(rdr.pages[page_num])
                with open(os.path.join(out_dir, out_name), "wb") as f:
                    w.write(f)
            QMessageBox.information(self, "Success", "Successfully split and exported PDFs!")
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Failed: {ex}")

    def _import_gate_json(self):
        fp, _ = QFileDialog.getOpenFileName(self, "Import GATE JSON", "", "JSON (*.json)")
        if not fp: return
        self.btn_gate_imp.setEnabled(False)
        threading.Thread(target=self._gate_json_work, args=(fp,), daemon=True).start()

    def _gate_json_work(self, fp):
        def log(m): self.gate_log.append(m)
        try:
            with open(fp, "r", encoding="utf-8") as f: data = json.load(f)
            sd = data.get("subject", {}); topics = data.get("topics", []); qs = data.get("questions", [])
            log(f"Subject: {sd.get('subject_name')}")
            rs = self.supabase.table("gate_subjects").select("*").eq("code", sd.get("subject_code")).execute()
            if rs.data:
                sid = rs.data[0]["id"]
            else:
                ri = self.supabase.table("gate_subjects").insert({
                    "name": sd.get("subject_name"), "code": sd.get("subject_code"), "display_order": 0
                }).execute()
                sid = ri.data[0]["id"]
            tm = {}
            for t in topics:
                rt = self.supabase.table("gate_topics").select("id").match({"subject_id":sid,"name":t["topic_name"]}).execute()
                if rt.data: tm[t["topic_name"]] = rt.data[0]["id"]
                else:
                    ri = self.supabase.table("gate_topics").insert({"subject_id":sid,"name":t["topic_name"],"summary":t.get("summary")}).execute()
                    if ri.data: tm[t["topic_name"]] = ri.data[0]["id"]
            for i, q in enumerate(qs):
                rq = self.supabase.table("gate_questions").insert({
                    "subject_id":sid, "question_text":q["question_text"],
                    "explanation":q.get("explanation"), "question_type":q.get("question_type","MCQ"),
                    "marks":q.get("marks",1), "difficulty":q.get("difficulty","easy")
                }).execute()
                if not rq.data: continue
                qid = rq.data[0]["id"]
                for tn in q.get("topics",[]):
                    tid = tm.get(tn)
                    if tid: self.supabase.table("gate_question_topics").insert({"question_id":qid,"topic_id":tid}).execute()
                for opt in q.get("options",[]):
                    self.supabase.table("gate_options").insert({"question_id":qid,"option_label":opt.get("label"),"option_text":opt.get("text"),"is_correct":opt.get("is_correct",False)}).execute()
                for src in q.get("pyq_sources",[]):
                    rp = self.supabase.table("gate_papers").select("id").match({"exam":src.get("exam","GATE CSE"),"year":src["year"],"set_number":src.get("set")}).execute()
                    if rp.data: pid = rp.data[0]["id"]
                    else:
                        ri2 = self.supabase.table("gate_papers").insert({"exam":src.get("exam","GATE CSE"),"year":src["year"],"set_number":src.get("set")}).execute()
                        pid = ri2.data[0]["id"] if ri2.data else None
                    if pid: self.supabase.table("gate_question_occurrences").insert({"question_id":qid,"paper_id":pid,"question_number":src["question_number"]}).execute()
                log(f"  Q {i+1}/{len(qs)}")
            log("✅ Done!")
            QMessageBox.information(self, "Done", "GATE import complete!")
        except Exception as e:
            log(f"ERROR: {e}"); QMessageBox.critical(self, "Error", str(e))
        finally: self.btn_gate_imp.setEnabled(True)

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 4 — COLLEGE IMAGE UPLOADER
    # ══════════════════════════════════════════════════════════════════════════
    def _page_college_img(self):
        p = self._page_frame("🖼️  College Solution Image Uploader", "college_img")
        self.c_subjects = []
        self.c_questions = []
        self.c_sel_q = None
        self.c_files = []

        lay = QHBoxLayout()
        p.main_layout.addLayout(lay, 1)

        # Left controls
        lf = QFrame()
        lf.setObjectName("card")
        lf_lay = QVBoxLayout(lf)
        
        self.c_dr_sub = QComboBox()
        self.c_dr_sub.currentTextChanged.connect(self._c_sub_sel)
        self.c_dr_sem = QComboBox()
        self.c_dr_sem.currentTextChanged.connect(self._c_sem_sel)
        self.c_dr_yr = QComboBox()
        self.c_dr_yr.currentTextChanged.connect(self._c_yr_sel)
        self.c_dr_ex = QComboBox()
        self.c_dr_ex.currentTextChanged.connect(self._c_ex_sel)
        self.c_dr_sea = QComboBox()
        self.c_dr_sea.currentTextChanged.connect(self._c_sea_sel)
        self.c_dr_q = QComboBox()
        self.c_dr_q.currentTextChanged.connect(self._c_q_sel)

        lf_lay.addWidget(QLabel("Subject"))
        lf_lay.addWidget(self.c_dr_sub)
        lf_lay.addWidget(QLabel("Semester"))
        lf_lay.addWidget(self.c_dr_sem)
        lf_lay.addWidget(QLabel("Year"))
        lf_lay.addWidget(self.c_dr_yr)
        lf_lay.addWidget(QLabel("Exam Type"))
        lf_lay.addWidget(self.c_dr_ex)
        lf_lay.addWidget(QLabel("Season"))
        lf_lay.addWidget(self.c_dr_sea)
        lf_lay.addWidget(QLabel("Question"))
        lf_lay.addWidget(self.c_dr_q)

        self.c_preview = QTextEdit()
        self.c_preview.setReadOnly(True)
        lf_lay.addWidget(QLabel("Question Text Preview:"))
        lf_lay.addWidget(self.c_preview)
        lay.addWidget(lf, 1)

        # Right grid uploader
        rf = QFrame()
        rf.setObjectName("card")
        rf_lay = QVBoxLayout(rf)
        
        btn_br = QPushButton("📸  Choose Images")
        btn_br.clicked.connect(self._c_browse)
        rf_lay.addWidget(btn_br)

        self.c_img_scroll = QScrollArea()
        self.c_img_scroll_widget = QWidget()
        self.c_img_grid = QGridLayout(self.c_img_scroll_widget)
        self.c_img_scroll.setWidget(self.c_img_scroll_widget)
        self.c_img_scroll.setWidgetResizable(True)
        rf_lay.addWidget(self.c_img_scroll)

        btn_up = QPushButton("🚀  Upload solution images to cloud")
        btn_up.clicked.connect(self._c_upload_t)
        rf_lay.addWidget(btn_up)
        lay.addWidget(rf, 1)

        threading.Thread(target=self._c_load_initial, daemon=True).start()
        return p

    def _c_load_initial(self):
        if not self.supabase: return
        try:
            r = self.supabase.table("subjects").select("id,name,code").order("name").execute()
            self.c_subjects = r.data
            self.c_dr_sub.clear()
            self.c_dr_sub.addItems([f"{s['name']} ({s['code']})" for s in r.data])
        except Exception as e: print(e)

    def _c_sub_sel(self, val):
        s = next((x for x in self.c_subjects if f"{x['name']} ({x['code']})"==val), None)
        if not s: return
        try:
            r = self.supabase.table("branch_subjects").select("semester").eq("subject_id", s["id"]).execute()
            sems = sorted(list(set(str(x["semester"]) for x in r.data)))
            self.c_dr_sem.clear()
            self.c_dr_sem.addItems(sems or ["-"])
        except Exception as e: print(e)

    def _c_sem_sel(self, val):
        if val=="-": return
        sn = self.c_dr_sub.currentText()
        s = next((x for x in self.c_subjects if f"{x['name']} ({x['code']})"==sn), None)
        if not s: return
        try:
            r = self.supabase.table("branch_subjects").select("year_id,years(name)").match({"subject_id":s["id"],"semester":int(val)}).execute()
            yrs = sorted(list(set(x["years"]["name"] for x in r.data if x.get("years"))))
            self.c_dr_yr.clear()
            self.c_dr_yr.addItems(yrs or ["-"])
        except Exception as e: print(e)

    def _c_yr_sel(self, val):
        if val=="-": return
        sn = self.c_dr_sub.currentText()
        s = next((x for x in self.c_subjects if f"{x['name']} ({x['code']})"==sn), None)
        if not s or val=="-": return
        try:
            r = self.supabase.table("pyq_sources").select("exam_type").match({"subject_id":s["id"],"year":int(val)}).execute()
            exs = sorted(list(set(x["exam_type"] for x in r.data if x.get("exam_type") is not None)))
            self.c_dr_ex.clear()
            self.c_dr_ex.addItems(exs or ["-"])
        except Exception as e: print(e)

    def _c_ex_sel(self, val):
        if val=="-": return
        sn = self.c_dr_sub.currentText()
        s = next((x for x in self.c_subjects if f"{x['name']} ({x['code']})"==sn), None)
        yv = self.c_dr_yr.currentText()
        if not s or yv=="-": return
        try:
            r = self.supabase.table("pyq_sources").select("season").match({"subject_id":s["id"],"year":int(yv),"exam_type":val}).execute()
            seas = sorted(list(set(x["season"] for x in r.data if x.get("season") is not None)))
            self.c_dr_sea.clear()
            self.c_dr_sea.addItems(seas or ["-"])
        except Exception as e: print(e)

    def _c_sea_sel(self, val):
        if val=="-": return
        sn = self.c_dr_sub.currentText()
        s = next((x for x in self.c_subjects if f"{x['name']} ({x['code']})"==sn), None)
        yv = self.c_dr_yr.currentText()
        ev = self.c_dr_ex.currentText()
        if not s or yv=="-" or ev=="-": return
        try:
            r = self.supabase.table("pyq_sources").select("id,question_number").match({"subject_id":s["id"],"year":int(yv),"exam_type":ev,"season":val}).execute()
            self.c_questions = r.data
            qns = [str(q["question_number"]) for q in r.data]
            self.c_dr_q.clear()
            self.c_dr_q.addItems(qns or ["-"])
        except Exception as e: print(e)

    def _c_q_sel(self, val):
        if val=="-": return
        qo = next((q for q in self.c_questions if str(q["question_number"])==val), None)
        if not qo: return
        try:
            r = self.supabase.table("question_pyq_map").select("question_id,questions(question_text)").eq("pyq_source_id", qo["id"]).execute()
            if r.data:
                row = r.data[0]
                self.c_sel_q = {
                    "question_id": row["question_id"],
                    "question_text": row["questions"]["question_text"] if row.get("questions") else ""
                }
                self.c_preview.setPlainText(self.c_sel_q["question_text"])
        except Exception as e: print(e)

    def _c_browse(self):
        fs, _ = QFileDialog.getOpenFileNames(self, "Choose solution images", "", "Images (*.png *.jpg *.jpeg *.webp)")
        if fs:
            self.c_files.extend(fs)
            self._c_render()

    def _c_render(self):
        # Clear layout
        while self.c_img_grid.count():
            w = self.c_img_grid.takeAt(0).widget()
            if w: w.deleteLater()
        
        for idx, fp in enumerate(self.c_files):
            pix = QPixmap(fp)
            lbl = QLabel()
            lbl.setPixmap(pix.scaled(110, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.c_img_grid.addWidget(lbl, idx // 3, idx % 3)

    def _c_upload_t(self):
        if not self.c_sel_q:
            QMessageBox.warning(self, "Warning", "Select a question first.")
            return
        if not self.c_files:
            QMessageBox.warning(self, "Warning", "No images selected.")
            return
        threading.Thread(target=self._c_upload_work, daemon=True).start()

    def _c_upload_work(self):
        # Uploads images to ImageKit, keeps map in Supabase.
        # Clear existing solution images matching question_id
        qid = self.c_sel_q["question_id"]
        try:
            self.supabase.table("images").delete().eq("question_id", qid).execute()
            for idx, fp in enumerate(self.c_files):
                with open(fp, "rb") as f:
                    bin_data = f.read()
                res = self.imagekit.upload_file(
                    file=bin_data,
                    file_name=f"sol_{qid}_{idx}.jpg",
                    options={"folder": f"solutions/{qid}"}
                )
                url = res.url
                self.supabase.table("images").insert({
                    "question_id": qid,
                    "image_url": url,
                    "image_order": idx + 1
                }).execute()
            
            QMessageBox.information(self, "Success", "Images uploaded successfully!")
            self.c_files = []
            self._c_render()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Upload failed: {e}")

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 5 — GATE IMAGE UPLOADER
    # ══════════════════════════════════════════════════════════════════════════
    def _page_gate_img(self):
        p = self._page_frame("📐  GATE Image Asset Uploader", "gate_img")
        self.g_years = []
        self.g_papers = []
        self.g_subjects = []
        self.g_questions = []
        self.g_options = []
        self.g_sel_q = None
        self.g_sel_o = None
        self.g_file = ""

        lay = QHBoxLayout()
        p.main_layout.addLayout(lay, 1)

        lf = QFrame()
        lf.setObjectName("card")
        lf_lay = QVBoxLayout(lf)
        
        self.g_dr_yr = QComboBox()
        self.g_dr_yr.currentTextChanged.connect(self._g_yr_sel)
        self.g_dr_pap = QComboBox()
        self.g_dr_pap.currentTextChanged.connect(self._g_pap_sel)
        self.g_dr_sub = QComboBox()
        self.g_dr_sub.currentTextChanged.connect(self._g_sub_sel)
        self.g_dr_q = QComboBox()
        self.g_dr_q.currentTextChanged.connect(self._g_q_sel)

        lf_lay.addWidget(QLabel("Year"))
        lf_lay.addWidget(self.g_dr_yr)
        lf_lay.addWidget(QLabel("Paper"))
        lf_lay.addWidget(self.g_dr_pap)
        lf_lay.addWidget(QLabel("Subject"))
        lf_lay.addWidget(self.g_dr_sub)
        lf_lay.addWidget(QLabel("Question"))
        lf_lay.addWidget(self.g_dr_q)

        self.g_dr_target = QComboBox()
        self.g_dr_target.addItems(["Question Body", "Option A", "Option B", "Option C", "Option D"])
        self.g_dr_target.currentTextChanged.connect(self._g_target_sel)
        lf_lay.addWidget(QLabel("Target component"))
        lf_lay.addWidget(self.g_dr_target)

        self.g_preview = QTextEdit()
        self.g_preview.setReadOnly(True)
        lf_lay.addWidget(QLabel("Question Text Preview:"))
        lf_lay.addWidget(self.g_preview)
        lay.addWidget(lf, 1)

        rf = QFrame()
        rf.setObjectName("card")
        rf_lay = QVBoxLayout(rf)
        
        self.lbl_gate_img = QLabel("No image selected.")
        rf_lay.addWidget(self.lbl_gate_img)

        btn_sel = QPushButton("📂  Select Image")
        btn_sel.clicked.connect(self._g_browse)
        rf_lay.addWidget(btn_sel)

        btn_up = QPushButton("🚀  Upload Image")
        btn_up.clicked.connect(self._g_upload_t)
        rf_lay.addWidget(btn_up)
        lay.addWidget(rf, 1)

        threading.Thread(target=self._g_load_initial, daemon=True).start()
        return p

    def _g_load_initial(self):
        if not self.supabase: return
        try:
            r = self.supabase.table("gate_papers").select("year").execute()
            yrs = sorted(list(set(str(x["year"]) for x in r.data)))
            self.g_dr_yr.clear()
            self.g_dr_yr.addItems(yrs or ["-"])
        except Exception as e: print(e)

    def _g_yr_sel(self, val):
        if val=="-": return
        try:
            r = self.supabase.table("gate_papers").select("id,exam,set_number").eq("year", int(val)).execute()
            self.g_papers = r.data
            paps = [f"{p['exam']} (Set {p['set_number']})" for p in r.data]
            self.g_dr_pap.clear()
            self.g_dr_pap.addItems(paps or ["-"])
        except Exception as e: print(e)

    def _g_pap_sel(self, val):
        if val=="-": return
        po = next((p for p in self.g_papers if f"{p['exam']} (Set {p['set_number']})"==val), None)
        if not po: return
        try:
            # Query subjects mapped via occurrences
            r = self.supabase.table("gate_question_occurrences").select("gate_questions(subject_id,gate_subjects(id,name))").eq("paper_id", po["id"]).execute()
            subjs = {}
            for row in r.data:
                q = row.get("gate_questions")
                if q and q.get("gate_subjects"):
                    s = q["gate_subjects"]
                    subjs[s["name"]] = s["id"]
            self.g_subjects = subjs
            self.g_dr_sub.clear()
            self.g_dr_sub.addItems(list(subjs.keys()) or ["-"])
        except Exception as e: print(e)

    def _g_sub_sel(self, val):
        sid = self.g_subjects.get(val)
        po = next((p for p in self.g_papers if f"{p['exam']} (Set {p['set_number']})"==self.g_dr_pap.currentText()), None)
        if not sid or not po: return
        try:
            r = self.supabase.table("gate_question_occurrences").select("question_number,question_id,gate_questions(question_text)").match({"paper_id":po["id"]}).execute()
            qns = []
            for row in r.data:
                q = row.get("gate_questions")
                if q:
                    qns.append((str(row["question_number"]), row["question_id"], q["question_text"]))
            self.g_questions = qns
            self.g_dr_q.clear()
            self.g_dr_q.addItems([x[0] for x in qns] or ["-"])
        except Exception as e: print(e)

    def _g_q_sel(self, val):
        qo = next((q for q in self.g_questions if q[0]==val), None)
        if not qo: return
        self.g_sel_qid = qo[1]
        self.g_preview.setPlainText(qo[2])
        # Fetch options
        try:
            r = self.supabase.table("gate_options").select("id,option_label").eq("question_id", qo[1]).execute()
            self.g_options = r.data
        except Exception as e: print(e)

    def _g_target_sel(self, val):
        if val=="Question Body":
            self.g_sel_o = None
        else:
            lbl = val.split(" ")[-1]
            opt = next((o for o in self.g_options if o["option_label"]==lbl), None)
            self.g_sel_o = opt

    def _g_browse(self):
        fp, _ = QFileDialog.getOpenFileName(self, "Select asset image", "", "Images (*.png *.jpg *.jpeg)")
        if fp:
            self.g_file = fp
            self.lbl_gate_img.setPixmap(QPixmap(fp).scaled(200, 200, Qt.KeepAspectRatio))

    def _g_upload_t(self):
        if not getattr(self, "g_sel_qid", None):
            QMessageBox.warning(self, "Warning", "Select a question first.")
            return
        if not self.g_file:
            QMessageBox.warning(self, "Warning", "Select an image file.")
            return
        threading.Thread(target=self._g_upload_work, daemon=True).start()

    def _g_upload_work(self):
        try:
            with open(self.g_file, "rb") as f:
                bin_data = f.read()
            
            if self.g_sel_o:
                # Option uploader
                oid = self.g_sel_o["id"]
                res = self.imagekit.upload_file(
                    file=bin_data,
                    file_name=f"opt_{oid}.jpg",
                    options={"folder": "gate/options"}
                )
                self.supabase.table("gate_options").update({"image_url": res.url}).eq("id", oid).execute()
            else:
                # Body uploader
                qid = self.g_sel_qid
                res = self.imagekit.upload_file(
                    file=bin_data,
                    file_name=f"q_{qid}.jpg",
                    options={"folder": "gate/questions"}
                )
                self.supabase.table("gate_questions").update({"image_url": res.url}).eq("id", qid).execute()
            
            QMessageBox.information(self, "Success", "GATE asset image uploaded successfully!")
            self.g_file = ""
            self.lbl_gate_img.setText("No image selected.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Upload failed: {e}")

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 6 — GATE DB EDITOR (PROTECTED)
    # ══════════════════════════════════════════════════════════════════════════
    def _page_gate_db(self):
        p = self._page_frame("🎓  Protected GATE Question Database Editor", "gate_db")
        self._gdb_subjects = []
        self._gdb_questions = []
        self._gdb_sel_qid = None
        self._gdb_opt_widgets = []

        lay = QHBoxLayout()
        p.main_layout.addLayout(lay, 1)

        # Left list
        lf = QFrame()
        lf.setObjectName("card")
        lf_lay = QVBoxLayout(lf)
        
        self.gdb_sub_sel = QComboBox()
        self.gdb_sub_sel.currentTextChanged.connect(self._gdb_sub_changed)
        lf_lay.addWidget(QLabel("Select Subject"))
        lf_lay.addWidget(self.gdb_sub_sel)

        self.gdb_search = QLineEdit()
        self.gdb_search.setPlaceholderText("Search question body text...")
        self.gdb_search.textChanged.connect(self._gdb_search_changed)
        lf_lay.addWidget(self.gdb_search)

        self.gdb_scroll = QScrollArea()
        self.gdb_scroll_widget = QWidget()
        self.gdb_list_lay = QVBoxLayout(self.gdb_scroll_widget)
        self.gdb_scroll.setWidget(self.gdb_scroll_widget)
        self.gdb_scroll.setWidgetResizable(True)
        lf_lay.addWidget(self.gdb_scroll)
        lay.addWidget(lf, 1)

        # Right editing panel
        rf = QFrame()
        rf.setObjectName("card")
        rf_lay = QVBoxLayout(rf)

        self._gdb_txt = QTextEdit()
        rf_lay.addWidget(QLabel("Question Text Body:"))
        rf_lay.addWidget(self._gdb_txt)

        self._gdb_exp = QTextEdit()
        rf_lay.addWidget(QLabel("Explanation:"))
        rf_lay.addWidget(self._gdb_exp)

        # Dropdowns
        dr_row = QHBoxLayout()
        self._gdb_diff = QComboBox()
        self._gdb_diff.addItems(["easy", "medium", "hard"])
        self._gdb_qtype = QComboBox()
        self._gdb_qtype.addItems(["MCQ", "NAT", "MSQ"])
        self._gdb_marks = QLineEdit("1")
        
        dr_row.addWidget(QLabel("Difficulty"))
        dr_row.addWidget(self._gdb_diff)
        dr_row.addWidget(QLabel("Type"))
        dr_row.addWidget(self._gdb_qtype)
        dr_row.addWidget(QLabel("Marks"))
        dr_row.addWidget(self._gdb_marks)
        rf_lay.addLayout(dr_row)

        # Options list
        self._gdb_opts_widget = QWidget()
        self._gdb_opts_lay = QVBoxLayout(self._gdb_opts_widget)
        self._gdb_opts_scroll = QScrollArea()
        self._gdb_opts_scroll.setWidget(self._gdb_opts_widget)
        self._gdb_opts_scroll.setWidgetResizable(True)
        rf_lay.addWidget(QLabel("Options Manager"))
        rf_lay.addWidget(self._gdb_opts_scroll)

        opt_acts = QHBoxLayout()
        btn_add_o = QPushButton("➕  Add Option")
        btn_add_o.clicked.connect(self._gdb_add_option_row)
        opt_acts.addWidget(btn_add_o)
        rf_lay.addLayout(opt_acts)

        btn_save = QPushButton("💾  Save Changes")
        btn_save.clicked.connect(self._gdb_save_changes)
        btn_del = QPushButton("🗑  Delete Question")
        btn_del.setStyleSheet(f"background-color: {COLORS['red']}; color: white;")
        btn_del.clicked.connect(self._gdb_delete_question)
        
        rf_lay.addWidget(btn_save)
        rf_lay.addWidget(btn_del)
        lay.addWidget(rf, 1.2)

        return p

    def _gdb_load_subjects(self):
        if not self.supabase: return
        try:
            r = self.supabase.table("gate_subjects").select("id,name").order("name").execute()
            self._gdb_subjects = r.data
            self.gdb_sub_sel.clear()
            self.gdb_sub_sel.addItems([s["name"] for s in r.data])
        except Exception as e: print(e)

    def _gdb_sub_changed(self, val):
        subj = next((s for s in self._gdb_subjects if s["name"]==val), None)
        if not subj: return
        try:
            r = self.supabase.table("gate_questions").select("id,question_text,difficulty,marks,question_type,explanation").eq("subject_id", subj["id"]).execute()
            self._gdb_questions = r.data
            self._gdb_render_list()
        except Exception as e: print(e)

    def _gdb_search_changed(self, val):
        self._gdb_render_list()

    def _gdb_render_list(self):
        # Clear grid
        while self.gdb_list_lay.count():
            w = self.gdb_list_lay.takeAt(0).widget()
            if w: w.deleteLater()
        
        query = self.gdb_search.text().strip().lower()
        for q in self._gdb_questions:
            txt = q["question_text"]
            if query and query not in txt.lower(): continue
            
            btn = QPushButton(txt[:55] + "...")
            btn.setStyleSheet("text-align: left;")
            btn.clicked.connect(lambda checked=False, qid=q["id"]: self._gdb_load_question(qid))
            self.gdb_list_lay.addWidget(btn)

    def _gdb_load_question(self, qid):
        self._gdb_sel_qid = qid
        q = next((x for x in self._gdb_questions if x["id"]==qid), None)
        if not q: return
        
        self._gdb_txt.setPlainText(q["question_text"])
        self._gdb_exp.setPlainText(q.get("explanation") or "")
        self._gdb_diff.setCurrentText(q.get("difficulty") or "easy")
        self._gdb_qtype.setCurrentText(q.get("question_type") or "MCQ")
        self._gdb_marks.setText(str(q.get("marks") or 1))

        # Load options
        # Clear old option rows
        while self._gdb_opts_lay.count():
            w = self._gdb_opts_lay.takeAt(0).widget()
            if w: w.deleteLater()
        self._gdb_opt_widgets = []

        try:
            r = self.supabase.table("gate_options").select("id,option_label,option_text,is_correct").eq("question_id", qid).execute()
            for opt in r.data:
                self._gdb_add_option_row(opt)
        except Exception as e: print(e)

    def _gdb_add_option_row(self, opt_data=None):
        row = QFrame()
        row.setObjectName("rowcard")
        r_lay = QHBoxLayout(row)

        lbl = QLineEdit(opt_data.get("option_label") if opt_data else "A")
        lbl.setFixedWidth(30)
        r_lay.addWidget(lbl)

        txt = QLineEdit(opt_data.get("option_text") if opt_data else "")
        r_lay.addWidget(txt)

        corr = QComboBox()
        corr.addItems(["False", "True"])
        if opt_data and opt_data.get("is_correct"):
            corr.setCurrentText("True")
        r_lay.addWidget(corr)

        btn_del = QPushButton("🗑")
        btn_del.setFixedWidth(30)
        btn_del.clicked.connect(lambda: self._gdb_delete_option_row(row, opt_data))
        r_lay.addWidget(btn_del)

        self._gdb_opts_lay.addWidget(row)
        self._gdb_opt_widgets.append({
            "frame": row,
            "label_ent": lbl,
            "text_ent": txt,
            "correct_var": corr,
            "id": opt_data.get("id") if opt_data else None
        })

    def _gdb_delete_option_row(self, row, opt_data):
        row.deleteLater()
        if opt_data and opt_data.get("id"):
            try:
                self.supabase.table("gate_options").delete().eq("id", opt_data["id"]).execute()
            except Exception as e: print(e)
        self._gdb_opt_widgets = [w for w in self._gdb_opt_widgets if w["frame"] != row]

    def _gdb_save_changes(self):
        if not self._gdb_sel_qid: return
        qid = self._gdb_sel_qid
        try:
            self.supabase.table("gate_questions").update({
                "question_text": self._gdb_txt.toPlainText(),
                "explanation": self._gdb_exp.toPlainText(),
                "difficulty": self._gdb_diff.currentText(),
                "marks": int(self._gdb_marks.text()),
                "question_type": self._gdb_qtype.currentText()
            }).eq("id", qid).execute()

            # Save options
            for w in self._gdb_opt_widgets:
                lbl = w["label_ent"].text()
                text = w["text_ent"].text()
                corr = w["correct_var"].currentText() == "True"
                oid = w.get("id")
                if oid:
                    self.supabase.table("gate_options").update({
                        "option_label": lbl, "option_text": text, "is_correct": corr
                    }).eq("id", oid).execute()
                else:
                    self.supabase.table("gate_options").insert({
                        "question_id": qid, "option_label": lbl, "option_text": text, "is_correct": corr
                    }).execute()
            QMessageBox.information(self, "Saved", "GATE Question changes saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Save failed: {e}")

    def _gdb_delete_question(self):
        if not self._gdb_sel_qid: return
        if QMessageBox.question(self, "Delete?", "Delete this question permanently?") == QMessageBox.Yes:
            try:
                qid = self._gdb_sel_qid
                self.supabase.table("gate_options").delete().eq("question_id", qid).execute()
                self.supabase.table("gate_questions").delete().eq("id", qid).execute()
                QMessageBox.information(self, "Deleted", "Question deleted.")
                self._gdb_sub_changed(self.gdb_sub_sel.currentText())
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def _window(self, title, icon_key=""):
        icon_pix = self.mascots.get(icon_key)
        win = GlassWindow(title, icon_pix)
        return win, win.body

class QStackedWidgetWrapper(QFrame):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self._widgets = []
        self._current = None

    def addWidget(self, w):
        self._widgets.append(w)
        self.layout.addWidget(w)
        w.hide()

    def setCurrentWidget(self, w):
        if self._current:
            self._current.hide()
        self._current = w
        w.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if _auth_ok:
        # ── Login worker — runs OAuth in background thread so UI stays responsive
        class _LoginWorker(QThread):
            success = Signal(dict)
            failed  = Signal(str)
            def run(self):
                try:
                    user = firebase_auth.login()
                    self.success.emit(user) if user else self.failed.emit("Cancelled.")
                except Exception as e:
                    self.failed.emit(str(e))

        # ── Login screen
        class LoginWindow(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("\U0001f98a FocusFox \u2014 Sign In")
                self.resize(520, 400)
                self.setFixedSize(520, 400)
                p = img_path("dark_deskbg2.jpg")
                self._bg_pixmap = QPixmap(p) if os.path.exists(p) else None
                self.setStyleSheet(get_qss(THEME_PALETTES["dark"]))

                central = QWidget()
                self.setCentralWidget(central)
                root = QVBoxLayout(central)
                root.setContentsMargins(0, 0, 0, 0)
                root.addStretch(1)

                card = QFrame()
                card.setObjectName("glassWindow")
                card.setFixedWidth(360)
                c_lay = QVBoxLayout(card)
                c_lay.setContentsMargins(32, 28, 32, 28)
                c_lay.setSpacing(14)

                logo = QPixmap(img_path("focus_fox_nobg.png"))
                lbl_logo = QLabel()
                if not logo.isNull():
                    lbl_logo.setPixmap(logo.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                lbl_logo.setAlignment(Qt.AlignCenter)
                c_lay.addWidget(lbl_logo)

                lbl_t = QLabel("FocusFox Admin")
                lbl_t.setAlignment(Qt.AlignCenter)
                lbl_t.setStyleSheet("font-size: 20px; font-weight: bold; color: #E8E2FF;")
                c_lay.addWidget(lbl_t)

                lbl_s = QLabel("Sign in with Google to continue")
                lbl_s.setAlignment(Qt.AlignCenter)
                lbl_s.setStyleSheet(f"font-size: 11px; color: {THEME_PALETTES['dark']['muted']};")
                c_lay.addWidget(lbl_s)

                self._btn = QPushButton("\U0001f511  Sign in with Google")
                self._btn.setFixedHeight(40)
                self._btn.setStyleSheet(
                    "background-color: #F3A6C3; color: #1C1B29; font-size: 13px; "
                    "font-weight: bold; border: none; border-radius: 8px;"
                )
                self._btn.clicked.connect(self._start)
                c_lay.addWidget(self._btn)

                self._lbl_st = QLabel("")
                self._lbl_st.setAlignment(Qt.AlignCenter)
                self._lbl_st.setStyleSheet(f"font-size: 10px; color: {THEME_PALETTES['dark']['muted']};")
                c_lay.addWidget(self._lbl_st)

                h = QHBoxLayout()
                h.addStretch(); h.addWidget(card); h.addStretch()
                root.addLayout(h)
                root.addStretch(1)
                self._worker = None
                self._main = None

            def paintEvent(self, event):
                if self._bg_pixmap:
                    painter = QPainter(self)
                    painter.setRenderHint(QPainter.SmoothPixmapTransform)
                    sc = self._bg_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                    painter.drawPixmap((self.width()-sc.width())//2, (self.height()-sc.height())//2, sc)
                super().paintEvent(event)

            def _start(self):
                self._btn.setEnabled(False)
                self._btn.setText("\u23f3  Opening browser...")
                self._lbl_st.setText("A browser tab will open \u2014 sign in with your Google account.")
                self._worker = _LoginWorker()
                self._worker.success.connect(self._ok)
                self._worker.failed.connect(self._fail)
                self._worker.start()

            def _ok(self, user):
                self._main = FocusFoxApp(user=user)
                self._main.show()
                self.close()

            def _fail(self, err):
                self._btn.setEnabled(True)
                self._btn.setText("\U0001f511  Sign in with Google")
                self._lbl_st.setText(f"Login failed: {err}")

        win = LoginWindow()
    else:
        win = FocusFoxApp()
    win.show()
    sys.exit(app.exec())
