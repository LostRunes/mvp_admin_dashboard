import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import customtkinter as ctk

import supabase_client
import uploader

# Set modern look & feel
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class FocusFoxUploaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("FocusFox Question Image Uploader")
        self.geometry("900x750")
        self.minsize(800, 700)
        
        # State variables
        self.selected_files = []
        self.thumbnails = []  # Maintain references to prevent garbage collection
        
        # Data lists/maps
        self.branches = []
        self.semesters = []
        self.subjects = []
        self.years = []
        self.exam_types = []
        self.seasons = []
        self.pyq_questions = []
        self.selected_question_details = None
        
        # UI Setup
        self.setup_layout()
        
        # Initial data load (run in background thread to avoid freeze)
        self.show_loading("Loading branches...")
        threading.Thread(target=self.load_branches_thread, daemon=True).start()

    def setup_layout(self):
        # Configure Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Main Frame
        self.main_container = ctk.CTkFrame(self, corner_radius=15)
        self.main_container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=0) # Title
        self.main_container.grid_rowconfigure(1, weight=1) # Form and List
        self.main_container.grid_rowconfigure(2, weight=0) # Progress/Buttons
        
        # Title Label
        self.title_label = ctk.CTkLabel(
            self.main_container, 
            text="FocusFox Image Uploader", 
            font=ctk.CTkFont(family="Inter", size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))
        
        # ----------------- LEFT COLUMN (FILTERS) -----------------
        self.left_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.left_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.left_frame.grid_columnconfigure(0, weight=1)
        
        # Form Container
        self.form_frame = ctk.CTkScrollableFrame(self.left_frame, label_text="Metadata Selection")
        self.form_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.form_frame.grid_columnconfigure(0, weight=1)
        
        # Branch
        self.add_label(self.form_frame, "Branch")
        self.branch_dropdown = self.add_dropdown(self.form_frame, self.on_branch_selected)
        
        # Semester
        self.add_label(self.form_frame, "Semester")
        self.semester_dropdown = self.add_dropdown(self.form_frame, self.on_semester_selected)
        
        # Subject
        self.add_label(self.form_frame, "Subject")
        self.subject_dropdown = self.add_dropdown(self.form_frame, self.on_subject_selected)
        
        # Year
        self.add_label(self.form_frame, "Year")
        self.year_dropdown = self.add_dropdown(self.form_frame, self.on_year_selected)
        
        # Exam Type
        self.add_label(self.form_frame, "Exam Type")
        self.exam_dropdown = self.add_dropdown(self.form_frame, self.on_exam_selected)
        
        # Season
        self.add_label(self.form_frame, "Season")
        self.season_dropdown = self.add_dropdown(self.form_frame, self.on_season_selected)
        
        # Question
        self.add_label(self.form_frame, "Question Number")
        self.question_dropdown = self.add_dropdown(self.form_frame, self.on_question_selected)
        
        # Question text preview (read-only textbox)
        self.add_label(self.form_frame, "Question Text Preview")
        self.q_preview_box = ctk.CTkTextbox(self.form_frame, height=80, wrap="word")
        self.q_preview_box.grid(row=self.form_frame.grid_size()[1], column=0, padx=10, pady=(2, 10), sticky="ew")
        self.q_preview_box.insert("1.0", "Select metadata to display question description.")
        self.q_preview_box.configure(state="disabled")

        # ----------------- RIGHT COLUMN (IMAGES) -----------------
        self.right_frame = ctk.CTkFrame(self.main_container)
        self.right_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)
        
        # Header for Right Panel
        self.images_header_label = ctk.CTkLabel(
            self.right_frame, 
            text="Selected Images", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.images_header_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Scrollable area for selected files/thumbnails
        self.images_container = ctk.CTkScrollableFrame(self.right_frame, fg_color="transparent")
        self.images_container.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.images_container.grid_columnconfigure(0, weight=1)
        
        # Control Buttons for images
        self.img_controls_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.img_controls_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        self.select_btn = ctk.CTkButton(
            self.img_controls_frame, 
            text="Choose Images", 
            command=self.select_images,
            fg_color="#4f46e5",
            hover_color="#4338ca"
        )
        self.select_btn.pack(side="left", padx=5, fill="x", expand=True)
        
        self.clear_btn = ctk.CTkButton(
            self.img_controls_frame, 
            text="Clear", 
            command=self.clear_images,
            fg_color="#ef4444",
            hover_color="#dc2626"
        )
        self.clear_btn.pack(side="right", padx=5, fill="x", expand=True)

        # ----------------- BOTTOM PANEL (PROGRESS & UPLOAD) -----------------
        self.bottom_frame = ctk.CTkFrame(self.main_container, corner_radius=10)
        self.bottom_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="ew")
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(self.bottom_frame, text="Ready", font=ctk.CTkFont(size=13))
        self.status_label.grid(row=0, column=0, padx=20, pady=(10, 2))
        
        self.progress_bar = ctk.CTkProgressBar(self.bottom_frame)
        self.progress_bar.grid(row=1, column=0, padx=20, pady=(2, 10), sticky="ew")
        self.progress_bar.set(0)
        
        self.upload_btn = ctk.CTkButton(
            self.bottom_frame, 
            text="Upload", 
            command=self.start_upload,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            height=40
        )
        self.upload_btn.grid(row=2, column=0, padx=20, pady=(5, 15), sticky="ew")

    # Helper ui functions
    def add_label(self, parent, text):
        lbl = ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=12, weight="bold"))
        lbl.grid(row=parent.grid_size()[1], column=0, padx=10, pady=(10, 2), sticky="w")
        
    def add_dropdown(self, parent, callback):
        dd = ctk.CTkOptionMenu(parent, values=["Select..."], command=callback)
        dd.grid(row=parent.grid_size()[1], column=0, padx=10, pady=(2, 10), sticky="ew")
        return dd

    def show_loading(self, message):
        self.status_label.configure(text=message)
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        
    def stop_loading(self, message="Ready"):
        self.status_label.configure(text=message)
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.stop()
        self.progress_bar.set(0)

    # ----------------- BACKGROUND THREAD DATA RETRIEVAL -----------------
    def load_branches_thread(self):
        try:
            self.branches = supabase_client.get_branches()
            branch_names = [b["name"] for b in self.branches]
            self.after(0, lambda: self.update_dropdown(self.branch_dropdown, branch_names))
            self.after(0, lambda: self.stop_loading("Branches loaded."))
        except Exception as e:
            self.after(0, lambda err=e: self.handle_error("Failed to load branches", err))

    def on_branch_selected(self, name):
        selected_branch = next((b for b in self.branches if b["name"] == name), None)
        if not selected_branch:
            return
            
        self.show_loading("Loading semesters...")
        # Reset child dropdowns
        self.update_dropdown(self.semester_dropdown, [])
        self.update_dropdown(self.subject_dropdown, [])
        self.update_dropdown(self.year_dropdown, [])
        self.update_dropdown(self.exam_dropdown, [])
        self.update_dropdown(self.season_dropdown, [])
        self.update_dropdown(self.question_dropdown, [])
        self.update_q_preview("Select metadata to display question description.")
        self.selected_question_details = None

        threading.Thread(target=self.load_semesters_thread, args=(selected_branch["id"],), daemon=True).start()

    def load_semesters_thread(self, branch_id):
        try:
            self.semesters = supabase_client.get_semesters_by_branch(branch_id)
            str_semesters = [f"Semester {sem}" for sem in self.semesters]
            self.after(0, lambda: self.update_dropdown(self.semester_dropdown, str_semesters))
            self.after(0, lambda: self.stop_loading("Semesters loaded."))
        except Exception as e:
            self.after(0, lambda err=e: self.handle_error("Failed to load semesters", err))

    def on_semester_selected(self, display_name):
        if not display_name or display_name == "Select...":
            return
            
        branch_name = self.branch_dropdown.get()
        selected_branch = next((b for b in self.branches if b["name"] == branch_name), None)
        if not selected_branch:
            return
            
        try:
            semester = int(display_name.replace("Semester ", ""))
        except ValueError:
            return
            
        self.show_loading("Loading subjects...")
        # Reset child dropdowns
        self.update_dropdown(self.subject_dropdown, [])
        self.update_dropdown(self.year_dropdown, [])
        self.update_dropdown(self.exam_dropdown, [])
        self.update_dropdown(self.season_dropdown, [])
        self.update_dropdown(self.question_dropdown, [])
        self.update_q_preview("Select metadata to display question description.")
        self.selected_question_details = None

        threading.Thread(target=self.load_subjects_thread, args=(selected_branch["id"], semester), daemon=True).start()

    def load_subjects_thread(self, branch_id, semester):
        try:
            self.subjects = supabase_client.get_subjects_by_branch_and_semester(branch_id, semester)
            names = [f"{s['name']} ({s['code']})" if s.get("code") else s["name"] for s in self.subjects]
            self.after(0, lambda: self.update_dropdown(self.subject_dropdown, names))
            self.after(0, lambda: self.stop_loading("Subjects loaded."))
        except Exception as e:
            self.after(0, lambda err=e: self.handle_error("Failed to load subjects", err))

    def on_subject_selected(self, display_name):
        # Match subject
        selected_subj = None
        for s in self.subjects:
            s_name = f"{s['name']} ({s['code']})" if s.get("code") else s["name"]
            if s_name == display_name:
                selected_subj = s
                break
                
        if not selected_subj:
            return
            
        self.show_loading("Loading years...")
        self.update_dropdown(self.year_dropdown, [])
        self.update_dropdown(self.exam_dropdown, [])
        self.update_dropdown(self.season_dropdown, [])
        self.update_dropdown(self.question_dropdown, [])
        self.update_q_preview("Select metadata to display question description.")
        self.selected_question_details = None
        
        threading.Thread(target=self.load_years_thread, args=(selected_subj["id"],), daemon=True).start()

    def load_years_thread(self, subject_id):
        try:
            self.years = supabase_client.get_years_by_subject(subject_id)
            str_years = [str(y) for y in self.years]
            self.after(0, lambda: self.update_dropdown(self.year_dropdown, str_years))
            self.after(0, lambda: self.stop_loading("Years loaded."))
        except Exception as e:
            self.after(0, lambda err=e: self.handle_error("Failed to load years", err))

    def on_year_selected(self, year_str):
        if not year_str or year_str == "Select...":
            return
            
        # Get selected subject
        subj_disp = self.subject_dropdown.get()
        selected_subj = None
        for s in self.subjects:
            s_name = f"{s['name']} ({s['code']})" if s.get("code") else s["name"]
            if s_name == subj_disp:
                selected_subj = s
                break
                
        if not selected_subj:
            return
            
        self.show_loading("Loading exam types...")
        self.update_dropdown(self.exam_dropdown, [])
        self.update_dropdown(self.season_dropdown, [])
        self.update_dropdown(self.question_dropdown, [])
        self.update_q_preview("Select metadata to display question description.")
        self.selected_question_details = None
        
        threading.Thread(
            target=self.load_exams_thread, 
            args=(selected_subj["id"], int(year_str)), 
            daemon=True
        ).start()

    def load_exams_thread(self, subject_id, year):
        try:
            self.exam_types = supabase_client.get_exam_types_by_subject_and_year(subject_id, year)
            self.after(0, lambda: self.update_dropdown(self.exam_dropdown, self.exam_types))
            self.after(0, lambda: self.stop_loading("Exam types loaded."))
        except Exception as e:
            self.after(0, lambda err=e: self.handle_error("Failed to load exam types", err))

    def on_exam_selected(self, exam_type):
        if not exam_type or exam_type == "Select...":
            return
            
        # Get subject & year
        subj_disp = self.subject_dropdown.get()
        selected_subj = None
        for s in self.subjects:
            s_name = f"{s['name']} ({s['code']})" if s.get("code") else s["name"]
            if s_name == subj_disp:
                selected_subj = s
                break
        year = int(self.year_dropdown.get())
        
        self.show_loading("Loading seasons...")
        self.update_dropdown(self.season_dropdown, [])
        self.update_dropdown(self.question_dropdown, [])
        self.update_q_preview("Select metadata to display question description.")
        self.selected_question_details = None
        
        threading.Thread(
            target=self.load_seasons_thread,
            args=(selected_subj["id"], year, exam_type),
            daemon=True
        ).start()

    def load_seasons_thread(self, subject_id, year, exam_type):
        try:
            self.seasons = supabase_client.get_seasons_by_subject_year_and_exam_type(subject_id, year, exam_type)
            self.after(0, lambda: self.update_dropdown(self.season_dropdown, self.seasons))
            self.after(0, lambda: self.stop_loading("Seasons loaded."))
        except Exception as e:
            self.after(0, lambda err=e: self.handle_error("Failed to load seasons", err))

    def on_season_selected(self, season):
        if not season or season == "Select...":
            return
            
        # Get subject & year & exam
        subj_disp = self.subject_dropdown.get()
        selected_subj = None
        for s in self.subjects:
            s_name = f"{s['name']} ({s['code']})" if s.get("code") else s["name"]
            if s_name == subj_disp:
                selected_subj = s
                break
        year = int(self.year_dropdown.get())
        exam_type = self.exam_dropdown.get()
        
        self.show_loading("Loading questions...")
        self.update_dropdown(self.question_dropdown, [])
        self.update_q_preview("Select metadata to display question description.")
        self.selected_question_details = None
        
        threading.Thread(
            target=self.load_questions_thread,
            args=(selected_subj["id"], year, exam_type, season),
            daemon=True
        ).start()

    def load_questions_thread(self, subject_id, year, exam_type, season):
        try:
            self.pyq_questions = supabase_client.get_pyq_questions(subject_id, year, exam_type, season)
            nums = [q["question_number"] for q in self.pyq_questions]
            self.after(0, lambda: self.update_dropdown(self.question_dropdown, nums))
            self.after(0, lambda: self.stop_loading("Questions loaded."))
        except Exception as e:
            self.after(0, lambda err=e: self.handle_error("Failed to load questions", err))

    def on_question_selected(self, q_num):
        selected_q = next((q for q in self.pyq_questions if q["question_number"] == q_num), None)
        if not selected_q:
            return
            
        self.show_loading("Loading question preview...")
        self.selected_question_details = None
        
        threading.Thread(
            target=self.load_question_details_thread,
            args=(selected_q["id"],),
            daemon=True
        ).start()

    def load_question_details_thread(self, pyq_source_id):
        try:
            details = supabase_client.get_question_details(pyq_source_id)
            if details:
                self.selected_question_details = details
                self.after(0, lambda: self.update_q_preview(details["question_text"]))
            else:
                self.after(0, lambda: self.update_q_preview("No linked question text details found in map."))
            self.after(0, lambda: self.stop_loading("Question selected."))
        except Exception as e:
            self.after(0, lambda err=e: self.handle_error("Failed to load question details", err))

    # Dropdown helper
    def update_dropdown(self, dropdown, values):
        dropdown.configure(values=["Select..."] + values)
        dropdown.set("Select...")
        
    def update_q_preview(self, text):
        self.q_preview_box.configure(state="normal")
        self.q_preview_box.delete("1.0", "end")
        self.q_preview_box.insert("1.0", text)
        self.q_preview_box.configure(state="disabled")

    def handle_error(self, message, exception):
        self.stop_loading("Error occurred.")
        messagebox.showerror("Error", f"{message}:\n{str(exception)}")

    # ----------------- IMAGE MANAGEMENT -----------------
    def select_images(self):
        files = filedialog.askopenfilenames(
            title="Select Images to Upload",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")]
        )
        if files:
            self.selected_files.extend(files)
            # Remove duplicates
            self.selected_files = list(dict.fromkeys(self.selected_files))
            self.refresh_image_list()

    def clear_images(self):
        self.selected_files = []
        self.refresh_image_list()

    def remove_image(self, filepath):
        if filepath in self.selected_files:
            self.selected_files.remove(filepath)
            self.refresh_image_list()

    def refresh_image_list(self):
        # Clear container
        for widget in self.images_container.winfo_children():
            widget.destroy()
            
        self.thumbnails = [] # Clear references
        
        if not self.selected_files:
            no_img_label = ctk.CTkLabel(self.images_container, text="No images selected.", text_color="gray")
            no_img_label.pack(pady=20)
            return

        for filepath in self.selected_files:
            frame = ctk.CTkFrame(self.images_container, fg_color="#1e293b", corner_radius=8)
            frame.pack(fill="x", pady=4, padx=5)
            frame.grid_columnconfigure(1, weight=1)
            
            # Create thumbnail
            try:
                img = Image.open(filepath)
                img.thumbnail((60, 60))
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                self.thumbnails.append(ctk_img) # keep reference
                
                img_lbl = ctk.CTkLabel(frame, image=ctk_img, text="")
                img_lbl.grid(row=0, column=0, padx=8, pady=8)
            except Exception:
                # Fallback if image load fails
                fail_lbl = ctk.CTkLabel(frame, text="[Err]", text_color="red")
                fail_lbl.grid(row=0, column=0, padx=8, pady=8)
                
            # Filename & Path
            info_frame = ctk.CTkFrame(frame, fg_color="transparent")
            info_frame.grid(row=0, column=1, sticky="w", padx=5)
            
            fname_lbl = ctk.CTkLabel(info_frame, text=os.path.basename(filepath), font=ctk.CTkFont(weight="bold"))
            fname_lbl.pack(anchor="w")
            
            size_bytes = os.path.getsize(filepath)
            size_kb = f"{size_bytes / 1024:.1f} KB"
            size_lbl = ctk.CTkLabel(info_frame, text=size_kb, text_color="gray", font=ctk.CTkFont(size=10))
            size_lbl.pack(anchor="w")
            
            # Delete button
            del_btn = ctk.CTkButton(
                frame, 
                text="✕", 
                width=30, 
                height=30, 
                fg_color="#ef4444", 
                hover_color="#dc2626",
                command=lambda p=filepath: self.remove_image(p)
            )
            del_btn.grid(row=0, column=2, padx=10)

    # ----------------- UPLOAD MANAGEMENT -----------------
    def start_upload(self):
        # Validations
        if not self.selected_question_details:
            messagebox.showwarning("Warning", "Please select a valid question first.")
            return
            
        if not self.selected_files:
            messagebox.showwarning("Warning", "Please select at least one image to upload.")
            return
            
        question_id = self.selected_question_details["question_id"]
        
        # Check if images already exist
        self.show_loading("Checking database for existing images...")
        threading.Thread(
            target=self.check_existing_and_upload_thread,
            args=(question_id,),
            daemon=True
        ).start()

    def check_existing_and_upload_thread(self, question_id):
        try:
            existing = supabase_client.get_existing_images(question_id)
            replace_existing = False
            
            if existing:
                self.after(0, self.stop_loading)
                ans = messagebox.askyesno(
                    "Overwrite Images?",
                    f"This question already has {len(existing)} image(s) associated with it.\n"
                    "Do you want to REPLACE them?\n\n"
                    "Select Yes to delete them and upload new images.\n"
                    "Select No to cancel the operation."
                )
                if not ans:
                    self.after(0, lambda: self.stop_loading("Upload cancelled by user."))
                    return
                replace_existing = True
                
            self.after(0, lambda: self.disable_controls())
            self.after(0, lambda: self.show_loading("Uploading..."))
            
            # Execute upload
            uploader.upload_images(
                question_id=question_id,
                file_paths=self.selected_files,
                progress_callback=self.upload_progress_callback,
                replace_existing=replace_existing
            )
            
            self.after(0, lambda: self.on_upload_success())
        except Exception as e:
            self.after(0, lambda: self.enable_controls())
            self.after(0, lambda err=e: self.handle_error("Upload failed", err))

    def upload_progress_callback(self, current, total, message):
        # Calculate ratio
        ratio = current / total if total > 0 else 0
        self.after(0, lambda: self.progress_bar.set(ratio))
        self.after(0, lambda: self.status_label.configure(text=message))

    def on_upload_success(self):
        self.stop_loading("Upload completed successfully!")
        self.enable_controls()
        messagebox.showinfo("Success", "All images uploaded and saved successfully!")
        self.clear_images()

    def disable_controls(self):
        self.upload_btn.configure(state="disabled")
        self.select_btn.configure(state="disabled")
        self.clear_btn.configure(state="disabled")
        self.branch_dropdown.configure(state="disabled")
        self.semester_dropdown.configure(state="disabled")
        self.subject_dropdown.configure(state="disabled")
        self.year_dropdown.configure(state="disabled")
        self.exam_dropdown.configure(state="disabled")
        self.season_dropdown.configure(state="disabled")
        self.question_dropdown.configure(state="disabled")

    def enable_controls(self):
        self.upload_btn.configure(state="normal")
        self.select_btn.configure(state="normal")
        self.clear_btn.configure(state="normal")
        self.branch_dropdown.configure(state="normal")
        self.semester_dropdown.configure(state="normal")
        self.subject_dropdown.configure(state="normal")
        self.year_dropdown.configure(state="normal")
        self.exam_dropdown.configure(state="normal")
        self.season_dropdown.configure(state="normal")
        self.question_dropdown.configure(state="normal")
