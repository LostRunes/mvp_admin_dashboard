
# This script writes the new dashboard_app.py
import os

code = r'''import os
import sys
import json
import re
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image
from pypdf import PdfReader, PdfWriter
from dotenv import load_dotenv

try:
    from supabase import create_client
except ImportError:
    create_client = None

try:
    from imagekitio import ImageKit
except ImportError:
    ImageKit = None

load_dotenv()
ctk.set_appearance_mode("Dark")

# ── Soft, cozy, cute palette ──────────────────────────────────────────────────
BG       = "#1c1917"   # stone-900
SIDEBAR  = "#14110f"   # deeper stone
CARD     = "#292524"   # stone-800
CARD2    = "#3c3330"   # warm card surface
BORDER   = "#57534e"   # stone-600
ACCENT   = "#fb923c"   # soft orange
ACCENTLT = "#fdba74"   # lighter orange
CREAM    = "#fef3c7"   # warm cream
TEXTMAIN = "#fafaf9"   # stone-50
TEXTMUTE = "#a8a29e"   # stone-400
GREEN    = "#4ade80"
RED      = "#f87171"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMGS     = os.path.join(BASE_DIR, "images")

def img_path(n): return os.path.join(IMGS, n)

HELP = {
    "guide": ("fox_happy.png",
        "Welcome to Cozy Hub!\n\n"
        "This is your all-in-one FocusFox admin workspace.\n"
        "Navigate using the sidebar on the left.\n\n"
        "Every section has a  ?  button for help.\n"
        "All data syncs to your Supabase cloud database.\n\n"
        "Tip: Credentials load from your .env file —\n"
        "no manual config needed!"
    ),
    "yt": ("pegion.png",
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
}

class CozyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("☕ Cozy Hub — FocusFox Admin")
        self.geometry("1280x880")
        self.minsize(1060, 760)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.configure(fg_color=BG)

        self.supabase_url      = os.getenv("SUPABASE_URL",          "https://hoihnpzdlivaoywrshmk.supabase.co")
        self.supabase_key      = os.getenv("SUPABASE_KEY",          "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhvaWhucHpkbGl2YW95d3JzaG1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczMDc1MjAsImV4cCI6MjA5Mjg4MzUyMH0.0XavqpSZjXVvuVRdEvI1Iy7ZGCOxCfGBA0cROVHyvHI")
        self.imagekit_public   = os.getenv("IMAGEKIT_PUBLIC_KEY",   "public_czXZbyoBKtF2iM2UY6bWAg9tgkI=")
        self.imagekit_private  = os.getenv("IMAGEKIT_PRIVATE_KEY",  "private_pAlFPi/MgMKYXqpcuvuioTjBHVk=")
        self.imagekit_endpoint = os.getenv("IMAGEKIT_URL_ENDPOINT", "https://ik.imagekit.io/focusfox")

        self._load_mascots()
        self._init_connections()
        self._build_sidebar()
        self.pages = {}
        self._build_pages()
        self.switch("guide")

    def _load_mascots(self):
        self.mascots = {}
        wanted = {
            "fox":      ("fox_happy.png",                   (90, 90)),
            "panda":    ("panda.png",                       (70, 70)),
            "panda_r":  ("pegion.png", (80, 80)),
            "owl":      ("owl.png",                         (70, 70)),
            "lil_fox":  ("lil_fox.png",                     (70, 70)),
            "logo":     ("focus_fox_nobg.png",              (44, 44)),
            "coffee":   ("coffee.png",                      (28, 28)),
        }
        for key, (fname, sz) in wanted.items():
            try:
                im = Image.open(img_path(fname)).convert("RGBA")
                self.mascots[key] = ctk.CTkImage(light_image=im, dark_image=im, size=sz)
            except Exception:
                self.mascots[key] = None

    def _init_connections(self):
        self.supabase = None
        self.imagekit = None
        if create_client:
            try:
                self.supabase = create_client(self.supabase_url, self.supabase_key)
            except Exception as e:
                print(f"Supabase error: {e}")
        if ImageKit and self.imagekit_private:
            try:
                self.imagekit = ImageKit(private_key=self.imagekit_private)
            except Exception as e:
                print(f"ImageKit error: {e}")

    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, width=256, corner_radius=0, fg_color=SIDEBAR)
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)
        sb.grid_columnconfigure(0, weight=1)
        sb.grid_rowconfigure(9, weight=1)

        logo_row = ctk.CTkFrame(sb, fg_color="transparent")
        logo_row.grid(row=0, column=0, padx=18, pady=(26,4), sticky="ew")
        if self.mascots.get("logo"):
            ctk.CTkLabel(logo_row, image=self.mascots["logo"], text="").pack(side="left", padx=(0,10))
        ctk.CTkLabel(logo_row, text="Cozy Hub",
                     font=ctk.CTkFont("Inter", 20, "bold"), text_color=ACCENTLT).pack(side="left")
        ctk.CTkLabel(sb, text="FocusFox Admin Dashboard",
                     font=ctk.CTkFont("Inter", 11), text_color=TEXTMUTE
                     ).grid(row=1, column=0, padx=20, pady=(0,16), sticky="w")
        ctk.CTkFrame(sb, height=1, fg_color=BORDER).grid(row=2, column=0, padx=16, pady=(0,10), sticky="ew")
        ctk.CTkLabel(sb, text="  NAVIGATION",
                     font=ctk.CTkFont(size=10, weight="bold"), text_color=TEXTMUTE
                     ).grid(row=3, column=0, padx=16, pady=(0,6), sticky="w")

        self._nav_btns = {}
        nav = [
            ("guide",       "📖", "Usage Guide"),
            ("yt",          "🎥", "College PYQ & YT"),
            ("gate",        "🎓", "GATE Admin Portal"),
            ("college_img", "🖼️",  "College Image Upload"),
            ("gate_img",    "📐", "GATE Image Upload"),
        ]
        for i, (key, icon, label) in enumerate(nav, start=4):
            btn = ctk.CTkButton(sb, text=f"  {icon}  {label}", anchor="w",
                                command=lambda k=key: self.switch(k),
                                fg_color="transparent", text_color=TEXTMAIN,
                                hover_color=CARD2, corner_radius=12,
                                font=ctk.CTkFont("Inter", 13), height=44)
            btn.grid(row=i, column=0, padx=10, pady=2, sticky="ew")
            self._nav_btns[key] = btn

        ctk.CTkFrame(sb, height=1, fg_color=BORDER).grid(row=10, column=0, padx=16, pady=(0,10), sticky="ew")
        conn_txt = "🟢  Connected" if self.supabase else "🔴  Offline"
        conn_clr = GREEN if self.supabase else RED
        ctk.CTkLabel(sb, text=conn_txt, font=ctk.CTkFont("Inter", 11),
                     text_color=conn_clr).grid(row=11, column=0, padx=20, pady=(0,4), sticky="w")
        ctk.CTkLabel(sb, text="v1.3.0  •  Cozy Pack",
                     font=ctk.CTkFont("Inter", 10, slant="italic"), text_color=TEXTMUTE
                     ).grid(row=12, column=0, padx=20, pady=(0,22), sticky="w")

    def _build_pages(self):
        self._cont = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self._cont.grid(row=0, column=1, sticky="nsew")
        self._cont.grid_rowconfigure(0, weight=1)
        self._cont.grid_columnconfigure(0, weight=1)
        self.pages["guide"]       = self._page_guide()
        self.pages["yt"]          = self._page_yt()
        self.pages["gate"]        = self._page_gate()
        self.pages["college_img"] = self._page_college_img()
        self.pages["gate_img"]    = self._page_gate_img()

    def switch(self, key):
        for k, f in self.pages.items():
            if k == key: f.grid(row=0, column=0, sticky="nsew", padx=24, pady=22)
            else: f.grid_forget()
        for k, b in self._nav_btns.items():
            b.configure(fg_color=CARD2 if k==key else "transparent",
                        text_color=ACCENTLT if k==key else TEXTMAIN)

    # ── shared helpers ─────────────────────────────────────────────────────────
    def _page_frame(self, title, key):
        f = ctk.CTkFrame(self._cont, fg_color="transparent")
        f.grid_columnconfigure(0, weight=1)
        f.grid_rowconfigure(1, weight=1)
        row = ctk.CTkFrame(f, fg_color="transparent")
        row.grid(row=0, column=0, sticky="ew", pady=(0,16))
        row.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(row, text=title,
                     font=ctk.CTkFont("Inter", 22, "bold"), text_color=CREAM
                     ).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(row, text="  ?  Guide", width=100, height=32, corner_radius=16,
                      fg_color=CARD2, hover_color=BORDER, text_color=ACCENTLT,
                      font=ctk.CTkFont(size=12),
                      command=lambda k=key: self._show_help(k)
                      ).grid(row=0, column=1, padx=(10,0), sticky="e")
        return f

    def _show_help(self, key):
        img_name, text = HELP.get(key, ("fox_happy.png", "No guide available."))
        pop = ctk.CTkToplevel(self)
        pop.title("Help Guide")
        pop.geometry("480x500")
        pop.resizable(False, False)
        pop.configure(fg_color=CARD)
        pop.grab_set(); pop.lift()
        hdr = ctk.CTkFrame(pop, fg_color=CARD2, corner_radius=0, height=58)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        try:
            im = Image.open(img_path(img_name)).convert("RGBA")
            ci = ctk.CTkImage(light_image=im, dark_image=im, size=(38, 38))
            ctk.CTkLabel(hdr, image=ci, text="").pack(side="left", padx=14, pady=10)
        except Exception: pass
        ctk.CTkLabel(hdr, text="Help & Usage Guide",
                     font=ctk.CTkFont("Inter", 14, "bold"), text_color=ACCENTLT
                     ).pack(side="left", pady=10)
        body = ctk.CTkScrollableFrame(pop, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=14)
        ctk.CTkLabel(body, text=text, font=ctk.CTkFont("Consolas", 12),
                     text_color=TEXTMAIN, justify="left", wraplength=410, anchor="nw"
                     ).pack(fill="both", anchor="nw")
        ctk.CTkButton(pop, text="Got it!", fg_color=ACCENT, text_color=BG,
                      width=120, height=36, corner_radius=18,
                      command=pop.destroy).pack(pady=(4,16))

    def _card(self, parent, **kw):
        return ctk.CTkFrame(parent, fg_color=CARD, corner_radius=18,
                            border_color=BORDER, border_width=1, **kw)

    def _dropdown(self, parent, label, cb):
        ctk.CTkLabel(parent, text=label,
                     font=ctk.CTkFont(weight="bold"), text_color=ACCENTLT
                     ).pack(anchor="w", pady=(6,2))
        dr = ctk.CTkOptionMenu(parent, values=["-"], command=cb,
                               fg_color=CARD2, button_color=BORDER,
                               text_color=TEXTMAIN, corner_radius=10)
        dr.pack(fill="x", pady=(0,8))
        return dr

    def _entry(self, parent, ph=""):
        return ctk.CTkEntry(parent, fg_color=CARD2, border_color=BORDER,
                            border_width=1, corner_radius=10,
                            placeholder_text=ph, text_color=TEXTMAIN,
                            placeholder_text_color=TEXTMUTE)

    def _btn_p(self, parent, text, cmd, **kw):
        return ctk.CTkButton(parent, text=text, fg_color=ACCENT, text_color=BG,
                             hover_color=ACCENTLT, corner_radius=14, height=40,
                             command=cmd, **kw)

    def _btn_s(self, parent, text, cmd, **kw):
        return ctk.CTkButton(parent, text=text, fg_color=CARD2, text_color=TEXTMAIN,
                             hover_color=BORDER, corner_radius=14, height=38,
                             command=cmd, **kw)

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 1 — GUIDE
    # ══════════════════════════════════════════════════════════════════════════
    def _page_guide(self):
        p = self._page_frame("📚  Dashboard Overview", "guide")
        outer = self._card(p)
        outer.grid(row=1, column=0, sticky="nsew")
        outer.grid_columnconfigure(0, weight=1)
        outer.grid_rowconfigure(0, weight=1)
        sc = ctk.CTkScrollableFrame(outer, fg_color="transparent")
        sc.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        sc.grid_columnconfigure(0, weight=1)

        # Welcome banner
        banner = ctk.CTkFrame(sc, fg_color=CARD2, corner_radius=20)
        banner.pack(fill="x", pady=(0,16))
        banner.grid_columnconfigure(1, weight=1)
        if self.mascots.get("fox"):
            ctk.CTkLabel(banner, image=self.mascots["fox"], text=""
                         ).grid(row=0, column=0, padx=20, pady=16, rowspan=2)
        ctk.CTkLabel(banner, text="Welcome to your Cozy Hub!",
                     font=ctk.CTkFont("Inter", 17, "bold"), text_color=ACCENTLT
                     ).grid(row=0, column=1, sticky="sw", padx=8, pady=(18,2))
        ctk.CTkLabel(banner,
                     text="All your FocusFox admin tools in one cozy workspace.",
                     font=ctk.CTkFont("Inter", 13), text_color=TEXTMAIN
                     ).grid(row=1, column=1, sticky="nw", padx=8, pady=(0,18))

        sections = [
            ("panda_r", "🎥", "College PYQ & YouTube Uploader",
             "Manage subjects, branches, years. Upload YouTube lecture links and import bulk PYQ JSON data."),
            ("owl",     "🎓", "GATE Admin Portal",
             "Split large GATE PDFs into chapters. Import GATE questions, topics, options and papers."),
            ("panda",   "🖼️",  "College Image Uploader",
             "Upload step-by-step solution images for college questions to ImageKit CDN."),
            ("lil_fox", "📐", "GATE Image Uploader",
             "Upload images for GATE question bodies or individual answer options."),
        ]
        for mk, icon, title, desc in sections:
            c = ctk.CTkFrame(sc, fg_color=CARD2, corner_radius=16,
                             border_color=BORDER, border_width=1)
            c.pack(fill="x", pady=5)
            c.grid_columnconfigure(2, weight=1)
            if self.mascots.get(mk):
                ctk.CTkLabel(c, image=self.mascots[mk], text=""
                             ).grid(row=0, column=0, padx=14, pady=14, rowspan=2)
            ctk.CTkLabel(c, text=f"{icon}  {title}",
                         font=ctk.CTkFont("Inter", 13, "bold"), text_color=ACCENT
                         ).grid(row=0, column=2, sticky="sw", padx=8, pady=(14,2))
            ctk.CTkLabel(c, text=desc, font=ctk.CTkFont("Inter", 12),
                         text_color=TEXTMUTE, justify="left", wraplength=560
                         ).grid(row=1, column=2, sticky="nw", padx=8, pady=(0,14))

        tip = ctk.CTkFrame(sc, fg_color="#1e2a1e", corner_radius=14)
        tip.pack(fill="x", pady=(10,0))
        ctk.CTkLabel(tip, text="💡  Tips",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color="#86efac"
                     ).pack(anchor="w", padx=18, pady=(14,4))
        ctk.CTkLabel(tip,
                     text="• Every section has a  ?  button for detailed help.\n"
                          "• All uploads run in the background — UI stays snappy.\n"
                          "• Credentials come from your .env file — never shown in-app.",
                     font=ctk.CTkFont("Inter", 12), text_color=TEXTMAIN, justify="left"
                     ).pack(anchor="w", padx=18, pady=(0,14))
        return p

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 2 — COLLEGE PYQ & YT
    # ══════════════════════════════════════════════════════════════════════════
    def _page_yt(self):
        p = self._page_frame("🎥  College PYQ & YT Link Uploader", "yt")
        self.yt_subjects = []; self.yt_subject_map = {}

        tabs = ctk.CTkTabview(p, fg_color=CARD, corner_radius=18)
        tabs.grid(row=1, column=0, sticky="nsew")
        tabs.add("YouTube Links")
        tabs.add("Subject & Branch")
        tabs.add("JSON Importer")

        # Tab 1 ─ YouTube Links
        t1 = tabs.tab("YouTube Links")
        t1.grid_columnconfigure(0, weight=1); t1.grid_rowconfigure(1, weight=1)
        c1 = self._card(t1); c1.grid(row=0, column=0, sticky="ew", padx=4, pady=(8,8))
        c1.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(c1, text="Select Subject",
                     font=ctk.CTkFont(weight="bold"), text_color=ACCENTLT
                     ).grid(row=0, column=0, sticky="w", padx=16, pady=(14,4))
        self.yt_sub = ctk.CTkOptionMenu(c1, values=["Loading..."],
                                        command=self._yt_sub_sel,
                                        fg_color=CARD2, button_color=BORDER,
                                        text_color=TEXTMAIN, corner_radius=10)
        self.yt_sub.grid(row=1, column=0, sticky="ew", padx=16, pady=(0,14))
        c2 = self._card(t1); c2.grid(row=1, column=0, sticky="nsew", padx=4, pady=(0,8))
        c2.grid_columnconfigure(0, weight=1); c2.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(c2, text="YouTube Links  (one per line)",
                     font=ctk.CTkFont(weight="bold"), text_color=ACCENTLT
                     ).grid(row=0, column=0, sticky="w", padx=16, pady=(14,4))
        self.yt_box = ctk.CTkTextbox(c2, fg_color=CARD2, border_color=BORDER,
                                     border_width=1, corner_radius=10)
        self.yt_box.grid(row=1, column=0, sticky="nsew", padx=16)
        self._btn_p(c2, "💾  Save Links", self._yt_save
                    ).grid(row=2, column=0, sticky="ew", padx=16, pady=14)

        # Tab 2 ─ Subject & Branch
        t2 = tabs.tab("Subject & Branch")
        t2.grid_columnconfigure(0, weight=1); t2.grid_columnconfigure(1, weight=1)
        t2.grid_rowconfigure(0, weight=1)
        sc = self._card(t2); sc.grid(row=0, column=0, padx=(4,8), pady=8, sticky="nsew")
        ctk.CTkLabel(sc, text="Create Subject",
                     font=ctk.CTkFont(size=15, weight="bold"), text_color=ACCENT
                     ).pack(anchor="w", padx=16, pady=(16,12))
        for lbl, attr in [("Subject Name *","ent_sn"),("Subject Code *","ent_sc"),
                           ("PYQ Drive Link","ent_sp"),("Notes Drive Link","ent_sno")]:
            ctk.CTkLabel(sc, text=lbl, text_color=ACCENTLT).pack(anchor="w", padx=16)
            e = self._entry(sc); e.pack(fill="x", padx=16, pady=(2,10))
            setattr(self, attr, e)
        ctk.CTkButton(sc, text="➕  Create Subject",
                      fg_color="#166534", text_color="#dcfce7",
                      corner_radius=14, height=40, command=self._create_subj
                      ).pack(fill="x", padx=16, pady=(4,16))

        bc = self._card(t2); bc.grid(row=0, column=1, padx=(8,4), pady=8, sticky="nsew")
        ctk.CTkLabel(bc, text="Create Branch / Year",
                     font=ctk.CTkFont(size=15, weight="bold"), text_color=ACCENT
                     ).pack(anchor="w", padx=16, pady=(16,12))
        ctk.CTkLabel(bc, text="Branch Name", text_color=ACCENTLT).pack(anchor="w", padx=16)
        self.ent_bn = self._entry(bc, "e.g. Computer Science")
        self.ent_bn.pack(fill="x", padx=16, pady=(2,10))
        self._btn_s(bc, "➕  Create Branch", self._create_branch
                    ).pack(fill="x", padx=16, pady=(0,10))
        ctk.CTkFrame(bc, height=1, fg_color=BORDER).pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(bc, text="Year Name", text_color=ACCENTLT
                     ).pack(anchor="w", padx=16, pady=(10,0))
        self.ent_yn = self._entry(bc, "e.g. 2nd Year")
        self.ent_yn.pack(fill="x", padx=16, pady=(2,10))
        self._btn_s(bc, "➕  Create Year", self._create_year
                    ).pack(fill="x", padx=16, pady=(0,16))

        # Tab 3 ─ JSON Importer
        t3 = tabs.tab("JSON Importer")
        t3.grid_columnconfigure(0, weight=1); t3.grid_rowconfigure(1, weight=1)
        jt = self._card(t3); jt.grid(row=0, column=0, sticky="ew", padx=4, pady=(8,8))
        jt.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(jt, text="Select subject, then import JSON",
                     font=ctk.CTkFont(weight="bold"), text_color=ACCENTLT
                     ).grid(row=0, column=0, sticky="w", padx=16, pady=(14,4))
        self.json_sub = ctk.CTkOptionMenu(jt, values=["Loading..."],
                                          fg_color=CARD2, button_color=BORDER,
                                          text_color=TEXTMAIN, corner_radius=10)
        self.json_sub.grid(row=1, column=0, sticky="ew", padx=16, pady=(0,8))
        self.btn_json = self._btn_p(jt, "📂  Choose JSON & Import", self._import_college_json)
        self.btn_json.grid(row=2, column=0, sticky="ew", padx=16, pady=(0,14))
        jl = self._card(t3); jl.grid(row=1, column=0, sticky="nsew", padx=4, pady=(0,8))
        jl.grid_columnconfigure(0, weight=1); jl.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(jl, text="Import Log",
                     font=ctk.CTkFont(weight="bold"), text_color=ACCENTLT
                     ).grid(row=0, column=0, sticky="w", padx=16, pady=(12,4))
        self.college_log = ctk.CTkTextbox(jl, fg_color=CARD2, border_color=BORDER,
                                          border_width=1, corner_radius=10)
        self.college_log.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0,16))

        threading.Thread(target=self._yt_load, daemon=True).start()
        p.grid_rowconfigure(1, weight=1)
        return p

    def _yt_load(self):
        if not self.supabase: return
        try:
            r = self.supabase.table("subjects").select("id,name,code,yt_links").order("name").execute()
            self.yt_subjects    = r.data
            self.yt_subject_map = {f"{s['name']} ({s['code']})": s for s in r.data}
            keys = list(self.yt_subject_map.keys())
            if keys:
                self.yt_sub.configure(values=keys)
                self.yt_sub.set(keys[0])
                self._yt_sub_sel(keys[0])
                self.json_sub.configure(values=keys)
                self.json_sub.set(keys[0])
        except Exception as e: print(e)

    def _yt_sub_sel(self, val):
        s = self.yt_subject_map.get(val)
        if s:
            self.yt_box.delete("1.0", tk.END)
            self.yt_box.insert("1.0", "\n".join(s.get("yt_links") or []))

    def _yt_save(self):
        if not self.supabase: return
        s = self.yt_subject_map.get(self.yt_sub.get())
        if not s: return
        ll = [l.strip() for l in self.yt_box.get("1.0", tk.END).strip().split("\n") if l.strip()]
        try:
            self.supabase.table("subjects").update({"yt_links": ll}).eq("id", s["id"]).execute()
            s["yt_links"] = ll
            messagebox.showinfo("Saved", "Links saved!")
        except Exception as e: messagebox.showerror("Error", str(e))

    def _create_subj(self):
        if not self.supabase: return
        n, c = self.ent_sn.get().strip(), self.ent_sc.get().strip()
        if not n or not c:
            messagebox.showwarning("Warning", "Name and Code are required.")
            return
        try:
            self.supabase.table("subjects").insert({
                "name": n, "code": c,
                "pyq_drive_link": self.ent_sp.get().strip() or None,
                "notes_drive_link": self.ent_sno.get().strip() or None
            }).execute()
            messagebox.showinfo("Done", f"Subject '{n}' created!")
            for e in [self.ent_sn, self.ent_sc, self.ent_sp, self.ent_sno]:
                e.delete(0, tk.END)
            threading.Thread(target=self._yt_load, daemon=True).start()
        except Exception as e: messagebox.showerror("Error", str(e))

    def _create_branch(self):
        if not self.supabase: return
        n = self.ent_bn.get().strip()
        if not n: return
        try:
            self.supabase.table("branches").insert({"name": n}).execute()
            messagebox.showinfo("Done", f"Branch '{n}' created!")
            self.ent_bn.delete(0, tk.END)
        except Exception as e: messagebox.showerror("Error", str(e))

    def _create_year(self):
        if not self.supabase: return
        n = self.ent_yn.get().strip()
        if not n: return
        try:
            self.supabase.table("years").insert({"name": n}).execute()
            messagebox.showinfo("Done", f"Year '{n}' created!")
            self.ent_yn.delete(0, tk.END)
        except Exception as e: messagebox.showerror("Error", str(e))

    def _import_college_json(self):
        fp = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not fp: return
        s = self.yt_subject_map.get(self.json_sub.get())
        if not s:
            messagebox.showwarning("Warning", "Select a valid subject.")
            return
        self.btn_json.configure(state="disabled")
        threading.Thread(target=self._college_json_work, args=(s["id"], fp), daemon=True).start()

    def _college_json_work(self, sid, fp):
        def log(m): self.college_log.insert(tk.END, m+"\n"); self.college_log.see(tk.END)
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
            messagebox.showinfo("Done", "Import complete!")
        except Exception as e:
            log(f"ERROR: {e}"); messagebox.showerror("Error", str(e))
        finally: self.btn_json.configure(state="normal")

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 3 — GATE ADMIN
    # ══════════════════════════════════════════════════════════════════════════
    def _page_gate(self):
        p = self._page_frame("🎓  GATE Admin Portal", "gate")
        tabs = ctk.CTkTabview(p, fg_color=CARD, corner_radius=18)
        tabs.grid(row=1, column=0, sticky="nsew")
        tabs.add("🗂  PDF Splitter")
        tabs.add("📥  JSON Importer")

        ts = tabs.tab("🗂  PDF Splitter")
        ts.grid_columnconfigure(0, weight=1)
        tc = self._card(ts); tc.grid(row=0, column=0, sticky="ew", padx=4, pady=(8,8))
        tc.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(tc, text="GATE PDF File",
                     font=ctk.CTkFont(weight="bold"), text_color=ACCENTLT
                     ).grid(row=0, column=0, sticky="w", padx=16, pady=(14,4))
        self.pdf_lbl = ctk.CTkLabel(tc, text="No file selected.", text_color=TEXTMUTE, anchor="w")
        self.pdf_lbl.grid(row=1, column=0, sticky="ew", padx=16)
        self._btn_s(tc, "📂  Browse PDF", self._browse_pdf
                    ).grid(row=2, column=0, sticky="ew", padx=16, pady=(8,8))
        ctk.CTkLabel(tc, text="Page Ranges  (e.g. 1-10, 11-20)",
                     font=ctk.CTkFont(weight="bold"), text_color=ACCENTLT
                     ).grid(row=3, column=0, sticky="w", padx=16, pady=(4,4))
        self.ent_ranges = self._entry(tc, "1-10, 11-20")
        self.ent_ranges.grid(row=4, column=0, sticky="ew", padx=16, pady=(0,8))
        self._btn_p(tc, "🗂  Split & Export PDFs", self._split_pdf
                    ).grid(row=5, column=0, sticky="ew", padx=16, pady=(4,16))

        ti = tabs.tab("📥  JSON Importer")
        ti.grid_columnconfigure(0, weight=1); ti.grid_rowconfigure(1, weight=1)
        tic = self._card(ti); tic.grid(row=0, column=0, sticky="ew", padx=4, pady=(8,8))
        tic.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(tic, text="Import GATE JSON into gate_questions",
                     font=ctk.CTkFont(weight="bold"), text_color=ACCENTLT
                     ).grid(row=0, column=0, sticky="w", padx=16, pady=(14,8))
        self.btn_gate_imp = self._btn_p(tic, "📂  Browse & Import JSON", self._import_gate_json)
        self.btn_gate_imp.grid(row=1, column=0, sticky="ew", padx=16, pady=(0,14))
        gl = self._card(ti); gl.grid(row=1, column=0, sticky="nsew", padx=4, pady=(0,8))
        gl.grid_columnconfigure(0, weight=1); gl.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(gl, text="Import Log",
                     font=ctk.CTkFont(weight="bold"), text_color=ACCENTLT
                     ).grid(row=0, column=0, sticky="w", padx=16, pady=(12,4))
        self.gate_log = ctk.CTkTextbox(gl, fg_color=CARD2, border_color=BORDER,
                                       border_width=1, corner_radius=10)
        self.gate_log.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0,16))
        p.grid_rowconfigure(1, weight=1)
        return p

    def _browse_pdf(self):
        fp = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        if fp: self.pdf_lbl.configure(text=fp)

    def _split_pdf(self):
        fp = self.pdf_lbl.cget("text")
        if not os.path.exists(fp):
            messagebox.showwarning("Warning", "Select a PDF first."); return
        rs = self.ent_ranges.get().strip()
        if not rs: messagebox.showwarning("Warning", "Enter page ranges."); return
        try:
            ranges = [(int(x.split("-")[0])-1, int(x.split("-")[1])) for x in rs.split(",")]
        except Exception:
            messagebox.showerror("Error", "Bad range format."); return
        try:
            rdr = PdfReader(fp)
            out = filedialog.askdirectory(title="Output folder")
            if not out: return
            for i, (s, e) in enumerate(ranges):
                w = PdfWriter()
                for n in range(s, min(e, len(rdr.pages))): w.add_page(rdr.pages[n])
                with open(os.path.join(out, f"Split_Part_{i+1}.pdf"), "wb") as f: w.write(f)
            messagebox.showinfo("Done", "Split complete!")
        except Exception as e: messagebox.showerror("Error", str(e))

    def _import_gate_json(self):
        fp = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not fp: return
        self.btn_gate_imp.configure(state="disabled")
        threading.Thread(target=self._gate_json_work, args=(fp,), daemon=True).start()

    def _gate_json_work(self, fp):
        def log(m): self.gate_log.insert(tk.END, m+"\n"); self.gate_log.see(tk.END)
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
            messagebox.showinfo("Done", "GATE import complete!")
        except Exception as e:
            log(f"ERROR: {e}"); messagebox.showerror("Error", str(e))
        finally: self.btn_gate_imp.configure(state="normal")

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 4 — COLLEGE IMAGE UPLOAD
    # ══════════════════════════════════════════════════════════════════════════
    def _page_college_img(self):
        p = self._page_frame("🖼️  College PYQ Image Uploader", "college_img")
        self.c_branches=[]; self.c_subjects=[]; self.c_questions=[]
        self.c_sel_q=None; self.c_files=[]; self.c_thumbs=[]
        p.grid_columnconfigure(0,weight=5); p.grid_columnconfigure(1,weight=5); p.grid_rowconfigure(1,weight=1)

        lc = self._card(p); lc.grid(row=1,column=0,sticky="nsew",padx=(0,8))
        lc.grid_columnconfigure(0,weight=1); lc.grid_rowconfigure(1,weight=1)
        ctk.CTkLabel(lc, text="Select Question",
                     font=ctk.CTkFont(size=14,weight="bold"), text_color=ACCENT
                     ).pack(anchor="w", padx=16, pady=(14,8))
        fs = ctk.CTkScrollableFrame(lc, fg_color="transparent")
        fs.pack(fill="both", expand=True, padx=8, pady=(0,8))
        self.c_dr_br  = self._dropdown(fs, "Branch",       self._c_br_sel)
        self.c_dr_sem = self._dropdown(fs, "Semester",      self._c_sem_sel)
        self.c_dr_sub = self._dropdown(fs, "Subject",       self._c_sub_sel)
        self.c_dr_yr  = self._dropdown(fs, "Year",          self._c_yr_sel)
        self.c_dr_ex  = self._dropdown(fs, "Exam Type",     self._c_ex_sel)
        self.c_dr_sea = self._dropdown(fs, "Season",        self._c_sea_sel)
        self.c_dr_q   = self._dropdown(fs, "Question #",    self._c_q_sel)
        ctk.CTkLabel(fs, text="Question Preview",
                     font=ctk.CTkFont(weight="bold"), text_color=ACCENTLT
                     ).pack(anchor="w", pady=(8,2))
        self.c_preview = ctk.CTkTextbox(fs, height=80, fg_color=CARD2,
                                        border_color=BORDER, border_width=1, corner_radius=10)
        self.c_preview.pack(fill="x", pady=(0,10))
        self.c_preview.insert("1.0","Select options above."); self.c_preview.configure(state="disabled")

        rc = self._card(p); rc.grid(row=1,column=1,sticky="nsew",padx=(8,0))
        rc.grid_columnconfigure(0,weight=1); rc.grid_rowconfigure(1,weight=1)
        ctk.CTkLabel(rc, text="Images",
                     font=ctk.CTkFont(size=14,weight="bold"), text_color=ACCENT
                     ).grid(row=0,column=0,padx=16,pady=(14,4),sticky="w")
        self.c_img_sc = ctk.CTkScrollableFrame(rc, fg_color="transparent")
        self.c_img_sc.grid(row=1,column=0,padx=12,pady=4,sticky="nsew")
        af = ctk.CTkFrame(rc, fg_color="transparent")
        af.grid(row=2,column=0,padx=16,pady=12,sticky="ew")
        self._btn_s(af,"📂",self._c_browse).pack(side="left",fill="x",expand=True,padx=(0,4))
        ctk.CTkButton(af,text="🧹",fg_color="#450a0a",text_color=RED,
                      corner_radius=14,height=38,command=self._c_clear
                      ).pack(side="left",fill="x",expand=True,padx=4)
        self._btn_p(af,"📤  Upload",self._c_upload_t
                    ).pack(side="left",fill="x",expand=True,padx=(4,0))
        self.c_status = ctk.CTkLabel(rc, text="Ready.", font=ctk.CTkFont(slant="italic"),
                                     text_color=TEXTMUTE, anchor="w")
        self.c_status.grid(row=3,column=0,padx=16,pady=(0,14),sticky="ew")
        threading.Thread(target=self._c_load_br, daemon=True).start()
        return p

    def _c_load_br(self):
        if not self.supabase: return
        try:
            r=self.supabase.table("branches").select("*").order("name").execute()
            self.c_branches=r.data; names=[b["name"] for b in r.data]
            self.c_dr_br.configure(values=names or ["-"])
            if names: self.c_dr_br.set(names[0]); self._c_br_sel(names[0])
        except Exception as e: print(e)

    def _c_br_sel(self, val):
        b=next((x for x in self.c_branches if x["name"]==val),None)
        if not b: return
        try:
            r=self.supabase.table("branch_subjects").select("semester").eq("branch_id",b["id"]).execute()
            sems=sorted(list(set(x["semester"] for x in r.data if x.get("semester") is not None)))
            ss=[str(s) for s in sems]; self.c_dr_sem.configure(values=ss or ["-"])
            if ss: self.c_dr_sem.set(ss[0]); self._c_sem_sel(ss[0])
            else: self.c_dr_sem.set("-")
        except Exception as e: print(e)

    def _c_sem_sel(self, val):
        if val=="-": return
        bn=self.c_dr_br.get(); b=next((x for x in self.c_branches if x["name"]==bn),None)
        if not b: return
        try:
            r=self.supabase.table("branch_subjects").select("subject_id,subjects(id,name,code)").eq("branch_id",b["id"]).eq("semester",int(val)).execute()
            self.c_subjects=[]; seen=set()
            for row in r.data:
                s=row.get("subjects")
                if s and s["id"] not in seen: seen.add(s["id"]); self.c_subjects.append(s)
            ns=[f"{s['name']} ({s['code']})" for s in self.c_subjects]
            self.c_dr_sub.configure(values=ns or ["-"])
            if ns: self.c_dr_sub.set(ns[0]); self._c_sub_sel(ns[0])
            else: self.c_dr_sub.set("-")
        except Exception as e: print(e)

    def _c_sub_sel(self, val):
        if val=="-": return
        s=next((x for x in self.c_subjects if f"{x['name']} ({x['code']})"==val),None)
        if not s: return
        try:
            r=self.supabase.table("pyq_sources").select("year").eq("subject_id",s["id"]).execute()
            yrs=sorted(list(set(x["year"] for x in r.data if x.get("year") is not None)),reverse=True)
            ys=[str(y) for y in yrs]; self.c_dr_yr.configure(values=ys or ["-"])
            if ys: self.c_dr_yr.set(ys[0]); self._c_yr_sel(ys[0])
            else: self.c_dr_yr.set("-")
        except Exception as e: print(e)

    def _c_yr_sel(self, val):
        if val=="-": return
        sn=self.c_dr_sub.get(); s=next((x for x in self.c_subjects if f"{x['name']} ({x['code']})"==sn),None)
        if not s: return
        try:
            r=self.supabase.table("pyq_sources").select("exam_type").match({"subject_id":s["id"],"year":int(val)}).execute()
            exs=sorted(list(set(x["exam_type"] for x in r.data if x.get("exam_type") is not None)))
            self.c_dr_ex.configure(values=exs or ["-"])
            if exs: self.c_dr_ex.set(exs[0]); self._c_ex_sel(exs[0])
            else: self.c_dr_ex.set("-")
        except Exception as e: print(e)

    def _c_ex_sel(self, val):
        if val=="-": return
        sn=self.c_dr_sub.get(); s=next((x for x in self.c_subjects if f"{x['name']} ({x['code']})"==sn),None)
        yv=self.c_dr_yr.get()
        if not s or yv=="-": return
        try:
            r=self.supabase.table("pyq_sources").select("season").match({"subject_id":s["id"],"year":int(yv),"exam_type":val}).execute()
            seas=sorted(list(set(x["season"] for x in r.data if x.get("season") is not None)))
            self.c_dr_sea.configure(values=seas or ["-"])
            if seas: self.c_dr_sea.set(seas[0]); self._c_sea_sel(seas[0])
            else: self.c_dr_sea.set("-")
        except Exception as e: print(e)

    def _c_sea_sel(self, val):
        if val=="-": return
        sn=self.c_dr_sub.get(); s=next((x for x in self.c_subjects if f"{x['name']} ({x['code']})"==sn),None)
        yv=self.c_dr_yr.get(); ev=self.c_dr_ex.get()
        if not s or yv=="-" or ev=="-": return
        try:
            r=self.supabase.table("pyq_sources").select("id,question_number").match({"subject_id":s["id"],"year":int(yv),"exam_type":ev,"season":val}).execute()
            self.c_questions=r.data; qns=[q["question_number"] for q in r.data]
            self.c_dr_q.configure(values=qns or ["-"])
            if qns: self.c_dr_q.set(qns[0]); self._c_q_sel(qns[0])
            else: self.c_dr_q.set("-")
        except Exception as e: print(e)

    def _c_q_sel(self, val):
        if val=="-": return
        qo=next((q for q in self.c_questions if q["question_number"]==val),None)
        if not qo: return
        try:
            r=self.supabase.table("question_pyq_map").select("question_id,questions(question_text)").eq("pyq_source_id",qo["id"]).execute()
            if r.data:
                row=r.data[0]
                self.c_sel_q={"question_id":row["question_id"],"question_text":row["questions"]["question_text"] if row.get("questions") else ""}
                self.c_preview.configure(state="normal")
                self.c_preview.delete("1.0",tk.END)
                self.c_preview.insert("1.0",self.c_sel_q["question_text"])
                self.c_preview.configure(state="disabled")
        except Exception as e: print(e)

    def _c_browse(self):
        fs=filedialog.askopenfilenames(filetypes=[("Images","*.png *.jpg *.jpeg *.webp")])
        if fs: self.c_files.extend(fs); self._c_render()

    def _c_clear(self): self.c_files=[]; self._c_render()

    def _c_render(self):
        for w in self.c_img_sc.winfo_children(): w.destroy()
        self.c_thumbs=[]
        for i,fp in enumerate(self.c_files):
            try:
                im=Image.open(fp); im.thumbnail((110,110))
                ci=ctk.CTkImage(light_image=im,dark_image=im,size=(110,110)); self.c_thumbs.append(ci)
                ctk.CTkLabel(self.c_img_sc,image=ci,text="").grid(row=i//3,column=i%3,padx=8,pady=8)
            except Exception as e: print(e)

    def _c_upload_t(self):
        if not self.c_sel_q: messagebox.showwarning("Warning","Select a question first."); return
        if not self.c_files: messagebox.showwarning("Warning","No images selected."); return
        if not self.imagekit: messagebox.showerror("Error","ImageKit not connected."); return
        threading.Thread(target=self._c_upload_work, daemon=True).start()

    def _c_upload_work(self):
        qid=self.c_sel_q["question_id"]; total=len(self.c_files)
        try:
            self.c_status.configure(text="Removing old images...")
            self.supabase.table("images").delete().eq("question_id",qid).execute()
            for i,fp in enumerate(self.c_files,1):
                self.c_status.configure(text=f"Uploading {i}/{total}...")
                _,ext=os.path.splitext(fp); ext=ext.lower() or ".png"
                with open(fp,"rb") as f:
                    ik=self.imagekit.files.upload(file=f,file_name=f"{i}{ext}",folder=f"images/{qid}",use_unique_file_name=False,public_key=self.imagekit_public)
                self.supabase.table("images").insert({"question_id":qid,"image_url":ik.url,"order_index":i}).execute()
            self.c_status.configure(text="✅ Done!")
            messagebox.showinfo("Done","Images uploaded!")
            self._c_clear()
        except Exception as e:
            self.c_status.configure(text="Failed."); messagebox.showerror("Error",str(e))

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 5 — GATE IMAGE UPLOAD
    # ══════════════════════════════════════════════════════════════════════════
    def _page_gate_img(self):
        p = self._page_frame("📐  GATE Image Uploader", "gate_img")
        self.g_papers=[]; self.g_subjects=[]; self.g_questions=[]; self.g_options=[]
        self.g_sel_q=None; self.g_sel_tid=None; self.g_files=[]; self.g_thumbs=[]
        p.grid_columnconfigure(0,weight=5); p.grid_columnconfigure(1,weight=5); p.grid_rowconfigure(1,weight=1)

        lc=self._card(p); lc.grid(row=1,column=0,sticky="nsew",padx=(0,8))
        lc.grid_columnconfigure(0,weight=1); lc.grid_rowconfigure(1,weight=1)
        ctk.CTkLabel(lc,text="Select Target",font=ctk.CTkFont(size=14,weight="bold"),text_color=ACCENT
                     ).pack(anchor="w",padx=16,pady=(14,8))
        fs=ctk.CTkScrollableFrame(lc,fg_color="transparent"); fs.pack(fill="both",expand=True,padx=8,pady=(0,8))
        self.g_dr_yr  =self._dropdown(fs,"Year",           self._g_yr_sel)
        self.g_dr_pap =self._dropdown(fs,"Paper / Set",    self._g_pap_sel)
        self.g_dr_sub =self._dropdown(fs,"Subject",        self._g_sub_sel)
        self.g_dr_q   =self._dropdown(fs,"Question #",     self._g_q_sel)
        ctk.CTkLabel(fs,text="Question Preview",font=ctk.CTkFont(weight="bold"),text_color=ACCENTLT
                     ).pack(anchor="w",pady=(8,2))
        self.g_preview=ctk.CTkTextbox(fs,height=80,fg_color=CARD2,border_color=BORDER,border_width=1,corner_radius=10)
        self.g_preview.pack(fill="x",pady=(0,10))
        self.g_preview.insert("1.0","Select options above."); self.g_preview.configure(state="disabled")
        self.g_dr_tgt =self._dropdown(fs,"Target Association",self._g_tgt_sel)

        rc=self._card(p); rc.grid(row=1,column=1,sticky="nsew",padx=(8,0))
        rc.grid_columnconfigure(0,weight=1); rc.grid_rowconfigure(1,weight=1)
        ctk.CTkLabel(rc,text="Images",font=ctk.CTkFont(size=14,weight="bold"),text_color=ACCENT
                     ).grid(row=0,column=0,padx=16,pady=(14,4),sticky="w")
        self.g_img_sc=ctk.CTkScrollableFrame(rc,fg_color="transparent")
        self.g_img_sc.grid(row=1,column=0,padx=12,pady=4,sticky="nsew")
        af=ctk.CTkFrame(rc,fg_color="transparent"); af.grid(row=2,column=0,padx=16,pady=12,sticky="ew")
        self._btn_s(af,"📂",self._g_browse).pack(side="left",fill="x",expand=True,padx=(0,4))
        ctk.CTkButton(af,text="🧹",fg_color="#450a0a",text_color=RED,corner_radius=14,height=38,
                      command=self._g_clear).pack(side="left",fill="x",expand=True,padx=4)
        self._btn_p(af,"📤  Upload",self._g_upload_t).pack(side="left",fill="x",expand=True,padx=(4,0))
        self.g_status=ctk.CTkLabel(rc,text="Ready.",font=ctk.CTkFont(slant="italic"),text_color=TEXTMUTE,anchor="w")
        self.g_status.grid(row=3,column=0,padx=16,pady=(0,14),sticky="ew")
        threading.Thread(target=self._g_load_yr, daemon=True).start()
        return p

    def _g_load_yr(self):
        if not self.supabase: return
        try:
            r=self.supabase.table("gate_papers").select("year").execute()
            yrs=sorted(list(set(x["year"] for x in r.data if x.get("year") is not None)),reverse=True)
            ys=[str(y) for y in yrs]; self.g_dr_yr.configure(values=ys or ["-"])
            if ys: self.g_dr_yr.set(ys[0]); self._g_yr_sel(ys[0])
        except Exception as e: print(e)

    def _g_yr_sel(self,val):
        try:
            r=self.supabase.table("gate_papers").select("*").eq("year",int(val)).execute()
            self.g_papers=sorted(r.data,key=lambda x:(x.get("exam") or "",x.get("set_number") or 0))
            labs=[f"{p.get('exam','GATE')} Set {p.get('set_number',0)}" for p in self.g_papers]
            self.g_dr_pap.configure(values=labs or ["-"])
            if labs: self.g_dr_pap.set(labs[0]); self._g_pap_sel(labs[0])
        except Exception as e: print(e)

    def _g_pap_sel(self,val):
        try:
            r=self.supabase.table("gate_subjects").select("*").execute()
            self.g_subjects=sorted(r.data,key=lambda x:x.get("name") or "")
            ns=[s["name"] for s in self.g_subjects]
            self.g_dr_sub.configure(values=ns or ["-"])
            if ns: self.g_dr_sub.set(ns[0]); self._g_sub_sel(ns[0])
        except Exception as e: print(e)

    def _g_sub_sel(self,val):
        try:
            pv=self.g_dr_pap.get(); vl=list(self.g_dr_pap.configure()["values"])
            if pv not in vl: return
            pi=vl.index(pv)
            if pi>=len(self.g_papers): return
            pap=self.g_papers[pi]; sub=next((s for s in self.g_subjects if s["name"]==val),None)
            if not sub: return
            r=self.supabase.table("gate_question_occurrences").select("question_id,question_number,gate_questions(id,question_text,explanation,subject_id)").eq("paper_id",pap["id"]).execute()
            self.g_questions=[]
            for row in r.data:
                gq=row.get("gate_questions")
                if gq and gq.get("subject_id")==sub["id"]:
                    self.g_questions.append({"question_id":row["question_id"],"question_number":row["question_number"],"question_text":gq.get("question_text") or ""})
            try: self.g_questions.sort(key=lambda q:[int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)",q["question_number"])])
            except: self.g_questions.sort(key=lambda x:x["question_number"])
            qns=[q["question_number"] for q in self.g_questions]
            self.g_dr_q.configure(values=qns or ["-"])
            if qns: self.g_dr_q.set(qns[0]); self._g_q_sel(qns[0])
            else: self.g_dr_q.set("-")
        except Exception as e: print(e)

    def _g_q_sel(self,val):
        if val=="-": return
        self.g_sel_q=next((q for q in self.g_questions if q["question_number"]==val),None)
        if not self.g_sel_q: return
        self.g_preview.configure(state="normal"); self.g_preview.delete("1.0",tk.END)
        self.g_preview.insert("1.0",self.g_sel_q["question_text"]); self.g_preview.configure(state="disabled")
        try:
            r=self.supabase.table("gate_options").select("*").eq("question_id",self.g_sel_q["question_id"]).execute()
            self.g_options=sorted(r.data,key=lambda x:x.get("option_label") or "")
            tgts=["Question Text / Body"]+[f"Option {o['option_label']}" for o in self.g_options]
            self.g_dr_tgt.configure(values=tgts); self.g_dr_tgt.set(tgts[0]); self._g_tgt_sel(tgts[0])
        except Exception as e: print(e)

    def _g_tgt_sel(self,val):
        if not self.g_sel_q: return
        if val=="Question Text / Body": self.g_sel_tid=self.g_sel_q["question_id"]
        else:
            ol=val.replace("Option ","").strip(); o=next((x for x in self.g_options if x["option_label"]==ol),None)
            if o: self.g_sel_tid=o["id"]

    def _g_browse(self):
        fs=filedialog.askopenfilenames(filetypes=[("Images","*.png *.jpg *.jpeg *.webp")])
        if fs: self.g_files.extend(fs); self._g_render()

    def _g_clear(self): self.g_files=[]; self._g_render()

    def _g_render(self):
        for w in self.g_img_sc.winfo_children(): w.destroy()
        self.g_thumbs=[]
        for i,fp in enumerate(self.g_files):
            try:
                im=Image.open(fp); im.thumbnail((110,110))
                ci=ctk.CTkImage(light_image=im,dark_image=im,size=(110,110)); self.g_thumbs.append(ci)
                ctk.CTkLabel(self.g_img_sc,image=ci,text="").grid(row=i//3,column=i%3,padx=8,pady=8)
            except Exception as e: print(e)

    def _g_upload_t(self):
        if not self.g_sel_tid: messagebox.showwarning("Warning","Select question & target."); return
        if not self.g_files: messagebox.showwarning("Warning","No images selected."); return
        if not self.imagekit: messagebox.showerror("Error","ImageKit not connected."); return
        threading.Thread(target=self._g_upload_work, daemon=True).start()

    def _g_upload_work(self):
        tid=self.g_sel_tid; iq=(self.g_dr_tgt.get()=="Question Text / Body")
        tn="gate_question_images" if iq else "gate_option_images"
        kc="question_id" if iq else "option_id"
        fp2="questions" if iq else "options"; total=len(self.g_files)
        try:
            self.g_status.configure(text="Removing old images...")
            self.supabase.table(tn).delete().eq(kc,tid).execute()
            for i,fp in enumerate(self.g_files,1):
                self.g_status.configure(text=f"Uploading {i}/{total}...")
                _,ext=os.path.splitext(fp); ext=ext.lower() or ".png"
                with open(fp,"rb") as f:
                    ik=self.imagekit.files.upload(file=f,file_name=f"{fp2}_{i}{ext}",folder=f"gate/{fp2}/{tid}",use_unique_file_name=False,public_key=self.imagekit_public)
                self.supabase.table(tn).insert({kc:tid,"image_url":ik.url,"order_index":i}).execute()
            self.g_status.configure(text="✅ Done!")
            messagebox.showinfo("Done","GATE images uploaded!")
            self._g_clear()
        except Exception as e:
            self.g_status.configure(text="Failed."); messagebox.showerror("Error",str(e))

if __name__=="__main__":
    app=CozyApp()
    app.mainloop()
'''

with open('dashboard_app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print(f"Written {len(code)} bytes to dashboard_app.py")
