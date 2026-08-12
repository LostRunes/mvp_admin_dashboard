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

class GateUploaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("FocusFox GATE Image Uploader")
        self.geometry("1000x800")
        self.minsize(900, 750)
        
        # State variables
        self.selected_files = []
        self.thumbnails = []  # Maintain references to prevent garbage collection
        
        # Data lists/maps
        self.years = []
        self.subjects = []
        self.papers = []
        self.questions = []
        self.options = []
        
        self.selected_year = None
        self.selected_paper = None
        self.selected_subject_id = None
        self.selected_question = None
        self.selected_target_type = "Question"  # Or "Option A", "Option B", etc.
        self.selected_target_id = None  # UUID of the question or the specific option
        
        # UI Setup
        self.setup_layout()
        
        # Initial data load
        self.show_loading("Loading initial data...")
        threading.Thread(target=self.load_initial_data_thread, daemon=True).start()

    def setup_layout(self):
        # Configure Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Main Frame
        self.main_container = ctk.CTkFrame(self, corner_radius=15)
        self.main_container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=4) # Left side (filters and metadata)
        self.main_container.grid_columnconfigure(1, weight=5) # Right side (images and uploads)
        self.main_container.grid_rowconfigure(0, weight=0) # Title
        self.main_container.grid_rowconfigure(1, weight=1) # Main Content
        self.main_container.grid_rowconfigure(2, weight=0) # Progress/Upload
        
        # Title Label
        self.title_label = ctk.CTkLabel(
            self.main_container, 
            text="FocusFox GATE Image Uploader", 
            font=ctk.CTkFont(family="Inter", size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))
        
        # ----------------- LEFT COLUMN (FILTERS & META) -----------------
        self.left_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.left_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.left_frame.grid_columnconfigure(0, weight=1)
        
        # Form Container
        self.form_frame = ctk.CTkScrollableFrame(self.left_frame, label_text="Metadata Selection")
        self.form_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.form_frame.grid_columnconfigure(0, weight=1)
        
        # Year
        self.add_label(self.form_frame, "Year")
        self.year_dropdown = self.add_dropdown(self.form_frame, self.on_year_selected)
        
        # Paper
        self.add_label(self.form_frame, "Paper/Exam Set")
        self.paper_dropdown = self.add_dropdown(self.form_frame, self.on_paper_selected)
        
        # Subject
        self.add_label(self.form_frame, "Subject")
        self.subject_dropdown = self.add_dropdown(self.form_frame, self.on_subject_selected)
        
        # Question Number
        self.add_label(self.form_frame, "Question Number")
        self.question_dropdown = self.add_dropdown(self.form_frame, self.on_question_selected)
        
        # Question text preview (read-only textbox)
        self.add_label(self.form_frame, "Question Text Preview")
        self.q_preview_box = ctk.CTkTextbox(self.form_frame, height=100, wrap="word")
        self.q_preview_box.grid(row=self.form_frame.grid_size()[1], column=0, padx=10, pady=(2, 10), sticky="ew")
        self.q_preview_box.insert("1.0", "Select a question to display details.")
        self.q_preview_box.configure(state="disabled")
        
        # Explanation preview
        self.add_label(self.form_frame, "Explanation Preview")
        self.exp_preview_box = ctk.CTkTextbox(self.form_frame, height=80, wrap="word")
        self.exp_preview_box.grid(row=self.form_frame.grid_size()[1], column=0, padx=10, pady=(2, 10), sticky="ew")
        self.exp_preview_box.insert("1.0", "")
        self.exp_preview_box.configure(state="disabled")

        # Target selection dropdown (Question itself, Option A, Option B, etc.)
        self.add_label(self.form_frame, "Target Image Association")
        self.target_dropdown = self.add_dropdown(self.form_frame, self.on_target_selected)
        
        # ----------------- RIGHT COLUMN (IMAGES & CONTROL) -----------------
        self.right_frame = ctk.CTkFrame(self.main_container)
        self.right_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1) # Local selected images
        self.right_frame.grid_rowconfigure(3, weight=1) # Existing database images
        
        # Header for Right Panel (Local Selection)
        self.images_header_label = ctk.CTkLabel(
            self.right_frame, 
            text="Selected Local Images to Upload", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.images_header_label.grid(row=0, column=0, padx=10, pady=(10, 2), sticky="w")
        
        # Scrollable area for selected files/thumbnails
        self.images_container = ctk.CTkScrollableFrame(self.right_frame, fg_color="transparent", height=180)
        self.images_container.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.images_container.grid_columnconfigure(0, weight=1)
        
        # Control Buttons for images
        self.img_controls_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.img_controls_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
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
            text="Clear Selected", 
            command=self.clear_images,
            fg_color="#ef4444",
            hover_color="#dc2626"
        )
        self.clear_btn.pack(side="right", padx=5, fill="x", expand=True)

        # Header for Database Images
        self.db_images_header_label = ctk.CTkLabel(
            self.right_frame, 
            text="Existing Images in Database", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.db_images_header_label.grid(row=3, column=0, padx=10, pady=(15, 2), sticky="w")
        
        # Scrollable area for database images
        self.db_images_container = ctk.CTkScrollableFrame(self.right_frame, fg_color="transparent", height=180)
        self.db_images_container.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")
        self.db_images_container.grid_columnconfigure(0, weight=1)

        # Clear existing images button
        self.db_controls_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.db_controls_frame.grid(row=5, column=0, padx=10, pady=(5, 10), sticky="ew")
        
        self.clear_db_btn = ctk.CTkButton(
            self.db_controls_frame, 
            text="Delete All Existing Images for Target", 
            command=self.delete_existing_db_images,
            fg_color="#b91c1c",
            hover_color="#991b1b"
        )
        self.clear_db_btn.pack(fill="x", padx=5)

        # ----------------- BOTTOM PANEL (PROGRESS & UPLOAD) -----------------
        self.bottom_frame = ctk.CTkFrame(self.main_container, corner_radius=10)
        self.bottom_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="ew")
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(self.bottom_frame, text="Ready", font=ctk.CTkFont(size=13))
        self.status_label.grid(row=0, column=0, padx=20, pady=(10, 2))
        
        self.progress_bar = ctk.CTkProgressBar(self.bottom_frame)
        self.progress_bar.grid(row=1, column=0, padx=20, pady=(2, 10), sticky="ew")
        self.progress_bar.set(0)
        
        self.replace_checkbox = ctk.CTkCheckBox(self.bottom_frame, text="Replace existing database images")
        self.replace_checkbox.grid(row=2, column=0, padx=20, pady=5)
        
        self.upload_btn = ctk.CTkButton(
            self.bottom_frame, 
            text="Upload & Map Images", 
            command=self.start_upload,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            height=40
        )
        self.upload_btn.grid(row=3, column=0, padx=20, pady=(5, 15), sticky="ew")

    # Helper UI functions
    def add_label(self, parent, text):
        lbl = ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=12, weight="bold"))
        lbl.grid(row=parent.grid_size()[1], column=0, padx=10, pady=(10, 2), sticky="w")
        
    def add_dropdown(self, parent, callback):
        dd = ctk.CTkOptionMenu(parent, values=["Select..."], command=callback)
        dd.grid(row=parent.grid_size()[1], column=0, padx=10, pady=(2, 10), sticky="ew")
        return dd
        
    def update_dropdown(self, dropdown, values):
        dropdown.configure(values=["Select..."] + values)
        dropdown.set("Select...")

    def show_loading(self, message):
        self.status_label.configure(text=message)
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        
    def stop_loading(self, message="Ready"):
        self.status_label.configure(text=message)
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.stop()
        self.progress_bar.set(0)

    def handle_error(self, message, exception):
        self.stop_loading("Error occurred.")
        messagebox.showerror("Error", f"{message}:\n{str(exception)}")

    def update_text_box(self, box, text):
        box.configure(state="normal")
        box.delete("1.0", "end")
        box.insert("1.0", text)
        box.configure(state="disabled")

    # ----------------- BACKGROUND THREAD DATA RETRIEVAL -----------------
    def load_initial_data_thread(self):
        try:
            self.years = supabase_client.get_years()
            self.subjects = supabase_client.get_subjects()
            
            str_years = [str(y) for y in self.years]
            sub_names = ["All Subjects"] + [s["name"] for s in self.subjects]
            
            self.after(0, lambda: self.update_dropdown(self.year_dropdown, str_years))
            self.after(0, lambda: self.update_dropdown(self.subject_dropdown, sub_names))
            self.after(0, lambda: self.subject_dropdown.set("All Subjects"))
            self.after(0, lambda: self.stop_loading("Initial data loaded."))
        except Exception as e:
            self.after(0, lambda err=e: self.handle_error("Failed to load initial data", err))

    def on_year_selected(self, year_str):
        if not year_str or year_str == "Select...":
            return
        self.selected_year = int(year_str)
        self.show_loading("Loading papers...")
        
        # Reset dropdowns
        self.update_dropdown(self.paper_dropdown, [])
        self.update_dropdown(self.question_dropdown, [])
        self.update_dropdown(self.target_dropdown, [])
        self.update_text_box(self.q_preview_box, "")
        self.update_text_box(self.exp_preview_box, "")
        self.selected_paper = None
        self.selected_question = None
        self.selected_target_id = None
        self.selected_subject_id = None
        self.subject_dropdown.set("All Subjects")
        self.refresh_db_images()
        
        threading.Thread(target=self.load_papers_thread, args=(self.selected_year,), daemon=True).start()

    def load_papers_thread(self, year):
        try:
            self.papers = supabase_client.get_papers_by_year(year)
            paper_names = []
            for p in self.papers:
                set_str = f"Set {p['set_number']}" if p.get("set_number") else "No Set"
                paper_names.append(f"{p['exam']} ({set_str})")
            self.after(0, lambda: self.update_dropdown(self.paper_dropdown, paper_names))
            self.after(0, lambda: self.stop_loading("Papers loaded."))
        except Exception as e:
            self.after(0, lambda err=e: self.handle_error("Failed to load papers", err))

    def on_paper_selected(self, paper_disp):
        if not paper_disp or paper_disp == "Select...":
            return
        
        # Match paper
        selected_p = None
        for p in self.papers:
            set_str = f"Set {p['set_number']}" if p.get("set_number") else "No Set"
            disp = f"{p['exam']} ({set_str})"
            if disp == paper_disp:
                selected_p = p
                break
                
        if not selected_p:
            return
            
        self.selected_paper = selected_p
        self.show_loading("Loading questions...")
        
        # Reset dropdowns
        self.update_dropdown(self.question_dropdown, [])
        self.update_dropdown(self.target_dropdown, [])
        self.update_text_box(self.q_preview_box, "")
        self.update_text_box(self.exp_preview_box, "")
        self.selected_question = None
        self.selected_target_id = None
        self.selected_subject_id = None
        self.subject_dropdown.set("All Subjects")
        self.refresh_db_images()
        
        threading.Thread(target=self.load_questions_thread, args=(self.selected_paper["id"],), daemon=True).start()

    def on_subject_selected(self, subject_disp):
        if not subject_disp or subject_disp == "Select...":
            self.selected_subject_id = None
        elif subject_disp == "All Subjects":
            self.selected_subject_id = None
        else:
            selected_sub = next((s for s in self.subjects if s["name"] == subject_disp), None)
            if selected_sub:
                self.selected_subject_id = selected_sub["id"]
            else:
                self.selected_subject_id = None
                
        # Reset question dropdown and update questions list
        self.update_dropdown(self.question_dropdown, [])
        self.update_dropdown(self.target_dropdown, [])
        self.update_text_box(self.q_preview_box, "")
        self.update_text_box(self.exp_preview_box, "")
        self.selected_question = None
        self.selected_target_id = None
        self.refresh_db_images()
        
        self.populate_questions()

    def populate_questions(self):
        filtered_qs = self.questions
        if self.selected_subject_id:
            filtered_qs = [q for q in self.questions if q.get("subject_id") == self.selected_subject_id]
            
        q_numbers = [q["question_number"] for q in filtered_qs]
        self.update_dropdown(self.question_dropdown, q_numbers)

    def load_questions_thread(self, paper_id):
        try:
            self.questions = supabase_client.get_questions_by_paper(paper_id)
            self.after(0, self.populate_questions)
            self.after(0, lambda: self.stop_loading("Questions loaded."))
        except Exception as e:
            self.after(0, lambda err=e: self.handle_error("Failed to load questions", err))

    def on_question_selected(self, q_num):
        if not q_num or q_num == "Select...":
            return
            
        selected_q = next((q for q in self.questions if q["question_number"] == q_num), None)
        if not selected_q:
            return
            
        self.selected_question = selected_q
        self.update_text_box(self.q_preview_box, selected_q["question_text"])
        self.update_text_box(self.exp_preview_box, selected_q["explanation"])
        
        self.show_loading("Loading options...")
        # Reset target & db image list
        self.update_dropdown(self.target_dropdown, [])
        self.selected_target_id = None
        self.refresh_db_images()
        
        threading.Thread(target=self.load_options_thread, args=(selected_q["question_id"],), daemon=True).start()

    def load_options_thread(self, question_id):
        try:
            self.options = supabase_client.get_options_by_question(question_id)
            targets = ["Question itself"]
            for opt in self.options:
                lbl = opt["option_label"]
                text_snippet = opt["option_text"][:30] + "..." if len(opt["option_text"]) > 30 else opt["option_text"]
                targets.append(f"Option {lbl}: {text_snippet}")
                
            self.after(0, lambda: self.update_dropdown(self.target_dropdown, targets))
            self.after(0, lambda: self.stop_loading("Options loaded."))
        except Exception as e:
            self.after(0, lambda err=e: self.handle_error("Failed to load options", err))

    def on_target_selected(self, target_disp):
        if not target_disp or target_disp == "Select...":
            self.selected_target_id = None
            self.refresh_db_images()
            return
            
        if target_disp == "Question itself":
            self.selected_target_type = "Question"
            self.selected_target_id = self.selected_question["question_id"]
        else:
            # Option selection
            self.selected_target_type = "Option"
            opt_label = target_disp.split(":")[0].replace("Option ", "").strip()
            selected_opt = next((o for o in self.options if o["option_label"] == opt_label), None)
            if selected_opt:
                self.selected_target_id = selected_opt["id"]
            else:
                self.selected_target_id = None
                
        self.refresh_db_images()

    def refresh_db_images(self):
        # Clear database images container
        for widget in self.db_images_container.winfo_children():
            widget.destroy()
            
        if not self.selected_target_id:
            lbl = ctk.CTkLabel(self.db_images_container, text="Select target to see existing images.", text_color="gray")
            lbl.pack(pady=20)
            return
            
        self.show_loading("Fetching existing images from DB...")
        threading.Thread(target=self.load_db_images_thread, daemon=True).start()

    def load_db_images_thread(self):
        try:
            if self.selected_target_type == "Question":
                images = supabase_client.get_question_images(self.selected_target_id)
            else:
                images = supabase_client.get_option_images(self.selected_target_id)
                
            self.after(0, lambda imgs=images: self.display_db_images(imgs))
            self.after(0, lambda: self.stop_loading("Existing images loaded."))
        except Exception as e:
            self.after(0, lambda err=e: self.handle_error("Failed to load DB images", err))

    def display_db_images(self, images):
        if not images:
            lbl = ctk.CTkLabel(self.db_images_container, text="No existing images in database for this target.", text_color="gray")
            lbl.pack(pady=20)
            return
            
        for img in images:
            frame = ctk.CTkFrame(self.db_images_container, fg_color="#0f172a", corner_radius=8)
            frame.pack(fill="x", pady=4, padx=5)
            
            lbl_index = ctk.CTkLabel(frame, text=f"Order {img['order_index']}:", font=ctk.CTkFont(weight="bold"))
            lbl_index.pack(side="left", padx=10, pady=10)
            
            # Show URL in a read-only Entry so they can copy it
            entry_url = ctk.CTkEntry(frame, width=300)
            entry_url.insert(0, img["image_url"])
            entry_url.configure(state="readonly")
            entry_url.pack(side="left", fill="x", expand=True, padx=10, pady=10)

    def delete_existing_db_images(self):
        if not self.selected_target_id:
            messagebox.showwarning("Warning", "Please select a target first.")
            return
            
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete all database image records for this target?")
        if not confirm:
            return
            
        self.show_loading("Deleting existing database image records...")
        threading.Thread(target=self.delete_db_images_thread, daemon=True).start()

    def delete_db_images_thread(self):
        try:
            if self.selected_target_type == "Question":
                supabase_client.delete_question_images(self.selected_target_id)
            else:
                supabase_client.delete_option_images(self.selected_target_id)
                
            self.after(0, lambda: self.refresh_db_images())
            self.after(0, lambda: self.stop_loading("Existing images deleted."))
        except Exception as e:
            self.after(0, lambda err=e: self.handle_error("Failed to delete database images", err))

    # ----------------- LOCAL IMAGE SELECTION -----------------
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
            no_img_label = ctk.CTkLabel(self.images_container, text="No local images selected.", text_color="gray")
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
            
            filename_lbl = ctk.CTkLabel(info_frame, text=os.path.basename(filepath), font=ctk.CTkFont(weight="bold"))
            filename_lbl.pack(anchor="w")
            
            path_lbl = ctk.CTkLabel(info_frame, text=filepath, font=ctk.CTkFont(size=10), text_color="gray")
            path_lbl.pack(anchor="w")
            
            # Delete button
            del_btn = ctk.CTkButton(
                frame, 
                text="Remove", 
                width=60, 
                height=25,
                fg_color="#374151",
                hover_color="#4b5563",
                command=lambda p=filepath: self.remove_image(p)
            )
            del_btn.grid(row=0, column=2, padx=10, pady=8)

    # ----------------- UPLOAD COORDINATION -----------------
    def start_upload(self):
        if not self.selected_target_id:
            messagebox.showwarning("Warning", "Please select a Year, Paper, Question, and Target Entity first.")
            return
            
        if not self.selected_files:
            messagebox.showwarning("Warning", "Please select at least one local image to upload.")
            return
            
        self.upload_btn.configure(state="disabled")
        self.select_btn.configure(state="disabled")
        self.clear_btn.configure(state="disabled")
        self.replace_checkbox.configure(state="disabled")
        self.clear_db_btn.configure(state="disabled")
        
        replace = self.replace_checkbox.get()
        
        self.status_label.configure(text="Starting upload...")
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(0)
        
        threading.Thread(target=self.upload_process_thread, args=(replace,), daemon=True).start()

    def upload_progress_callback(self, current, total, message):
        self.after(0, lambda: self.status_label.configure(text=message))
        if total > 0:
            self.after(0, lambda: self.progress_bar.set(current / total))

    def upload_process_thread(self, replace_existing):
        try:
            if self.selected_target_type == "Question":
                uploader.upload_question_images(
                    self.selected_target_id,
                    self.selected_files,
                    self.upload_progress_callback,
                    replace_existing=replace_existing
                )
            else:
                uploader.upload_option_images(
                    self.selected_target_id,
                    self.selected_files,
                    self.upload_progress_callback,
                    replace_existing=replace_existing
                )
                
            self.after(0, self.on_upload_complete)
        except Exception as e:
            self.after(0, lambda err=e: self.handle_error("Upload failed", err))
            self.after(0, self.reset_upload_ui_state)

    def on_upload_complete(self):
        messagebox.showinfo("Success", "Images uploaded and mapped successfully!")
        self.selected_files = []
        self.refresh_image_list()
        self.refresh_db_images()
        self.reset_upload_ui_state()

    def reset_upload_ui_state(self):
        self.upload_btn.configure(state="normal")
        self.select_btn.configure(state="normal")
        self.clear_btn.configure(state="normal")
        self.replace_checkbox.configure(state="normal")
        self.clear_db_btn.configure(state="normal")
        self.stop_loading("Ready")

if __name__ == "__main__":
    app = GateUploaderApp()
    app.mainloop()
