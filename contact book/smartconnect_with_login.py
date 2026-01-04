#!/usr/bin/env python3
"""
SmartConnect with Integrated Login
Single window - Login first, then show contacts (user-specific)
"""

import sys
import os
import customtkinter as ctk
from tkinter import messagebox

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auth_system import AuthenticationSystem


class SmartConnectWithLogin:
    """SmartConnect with integrated login - single window."""
    
    def __init__(self):
        """Initialize the application."""
        self.auth_system = AuthenticationSystem("contacts.db")
        self.session_token = None
        self.user_data = None
        self.root = None
        self.smartconnect_app = None
        
    def run(self):
        """Run the application."""
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("SmartConnect - Contact Management")
        self.root.geometry("500x650")
        
        # Show login screen first
        self._show_login_screen()
        
        self.root.mainloop()
    
    def _show_login_screen(self):
        """Show login/signup screen."""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header = ctk.CTkLabel(
            main_frame,
            text="SmartConnect",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        header.pack(pady=(10, 5))
        
        subtitle = ctk.CTkLabel(
            main_frame,
            text="Contact Management System",
            font=ctk.CTkFont(size=14)
        )
        subtitle.pack(pady=(0, 15))
        
        # Tabview for Login/Signup
        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.tabview.add("Login")
        self.tabview.add("Sign Up")
        
        self._setup_login_tab()
        self._setup_signup_tab()
        
        self.tabview.set("Login")
    
    def _setup_login_tab(self):
        """Setup login tab."""
        login_tab = self.tabview.tab("Login")
        
        content_frame = ctk.CTkFrame(login_tab, fg_color="transparent")
        content_frame.pack(expand=True, pady=15)
        
        # Email
        email_label = ctk.CTkLabel(content_frame, text="Email:", font=ctk.CTkFont(size=12), anchor="w", width=300)
        email_label.pack(padx=20, pady=(10, 5))
        
        self.login_email = ctk.CTkEntry(content_frame, placeholder_text="Enter your email", width=300)
        self.login_email.pack(padx=20, pady=(0, 10))
        self.login_email.bind("<Return>", lambda e: self._handle_login())
        
        # Password
        password_label = ctk.CTkLabel(content_frame, text="Password:", font=ctk.CTkFont(size=12), anchor="w", width=300)
        password_label.pack(padx=20, pady=(0, 5))
        
        self.login_password = ctk.CTkEntry(content_frame, placeholder_text="Enter your password", show="*", width=300)
        self.login_password.pack(padx=20, pady=(0, 15))
        self.login_password.bind("<Return>", lambda e: self._handle_login())
        
        # Login button
        login_btn = ctk.CTkButton(
            content_frame,
            text="Login",
            command=self._handle_login,
            width=300,
            height=45,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        login_btn.pack(padx=20, pady=(0, 10))
        

    
    def _setup_signup_tab(self):
        """Setup signup tab."""
        signup_tab = self.tabview.tab("Sign Up")
        
        content_frame = ctk.CTkFrame(signup_tab, fg_color="transparent")
        content_frame.pack(expand=True, pady=15)
        
        # Name
        name_label = ctk.CTkLabel(content_frame, text="Full Name:", font=ctk.CTkFont(size=12), anchor="w", width=300)
        name_label.pack(padx=20, pady=(10, 5))
        
        self.signup_name = ctk.CTkEntry(content_frame, placeholder_text="Enter your full name", width=300)
        self.signup_name.pack(padx=20, pady=(0, 10))
        self.signup_name.bind("<Return>", lambda e: self._handle_signup())
        
        # Email
        email_label = ctk.CTkLabel(content_frame, text="Email:", font=ctk.CTkFont(size=12), anchor="w", width=300)
        email_label.pack(padx=20, pady=(0, 5))
        
        self.signup_email = ctk.CTkEntry(content_frame, placeholder_text="Enter your email", width=300)
        self.signup_email.pack(padx=20, pady=(0, 10))
        self.signup_email.bind("<Return>", lambda e: self._handle_signup())
        
        # Password
        password_label = ctk.CTkLabel(content_frame, text="Password:", font=ctk.CTkFont(size=12), anchor="w", width=300)
        password_label.pack(padx=20, pady=(0, 5))
        
        self.signup_password = ctk.CTkEntry(content_frame, placeholder_text="Minimum 8 characters", show="*", width=300)
        self.signup_password.pack(padx=20, pady=(0, 10))
        self.signup_password.bind("<Return>", lambda e: self._handle_signup())
        
        # Confirm Password
        confirm_label = ctk.CTkLabel(content_frame, text="Confirm Password:", font=ctk.CTkFont(size=12), anchor="w", width=300)
        confirm_label.pack(padx=20, pady=(0, 5))
        
        self.signup_confirm = ctk.CTkEntry(content_frame, placeholder_text="Re-enter password", show="*", width=300)
        self.signup_confirm.pack(padx=20, pady=(0, 15))
        self.signup_confirm.bind("<Return>", lambda e: self._handle_signup())
        
        # Signup button
        signup_btn = ctk.CTkButton(
            content_frame,
            text="Create Account",
            command=self._handle_signup,
            width=300,
            height=45,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        signup_btn.pack(padx=20, pady=(0, 10))
    
    def _handle_login(self):
        """Handle login."""
        email = self.login_email.get().strip()
        password = self.login_password.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter email and password")
            return
        
        success, message, session_token, user_data = self.auth_system.login(email, password)
        
        if success:
            self.session_token = session_token
            self.user_data = user_data
            self._show_smartconnect()
        else:
            messagebox.showerror("Login Failed", message)
            self.login_password.delete(0, 'end')
    
    def _handle_signup(self):
        """Handle signup."""
        name = self.signup_name.get().strip()
        email = self.signup_email.get().strip()
        password = self.signup_password.get()
        confirm = self.signup_confirm.get()
        
        if not name or not email or not password:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        success, message = self.auth_system.signup(name, email, password)
        
        if success:
            messagebox.showinfo("Success", message)
            self.tabview.set("Login")
            self.login_email.delete(0, 'end')
            self.login_email.insert(0, email)
            self.login_password.focus()
        else:
            messagebox.showerror("Signup Failed", message)
    
    def _show_smartconnect(self):
        """Show SmartConnect GUI after login - same window."""
        # Clear login screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Keep same window, just resize
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        self.root.minsize(800, 600)
        
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Create profile header (like a website)
        self._create_profile_header()
        
        # Create SmartConnect content below
        self._create_smartconnect_content()
    
    def _create_profile_header(self):
        """Create profile header section (like website header)."""
        header = ctk.CTkFrame(self.root, height=60, fg_color=("#2b2b2b", "#1a1a1a"))
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header.grid_columnconfigure(1, weight=1)
        header.grid_propagate(False)
        
        # App title/logo
        title = ctk.CTkLabel(
            header,
            text="SmartConnect",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#ffffff", "#ffffff")
        )
        title.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        # Profile section (right side)
        profile_frame = ctk.CTkFrame(header, fg_color="transparent")
        profile_frame.grid(row=0, column=2, padx=20, pady=10, sticky="e")
        
        # Admin Panel button (only for admins)
        if self.user_data.get('role') == 'admin':
            admin_btn = ctk.CTkButton(
                profile_frame,
                text="⚙️ Admin Panel",
                command=self._open_admin_panel,
                width=120,
                height=32,
                fg_color=("#6c757d", "#5a6268"),
                hover_color=("#5a6268", "#545b62")
            )
            admin_btn.pack(side="left", padx=(0, 15))
        
        # User avatar/icon
        avatar = ctk.CTkLabel(
            profile_frame,
            text="👤",
            font=ctk.CTkFont(size=24)
        )
        avatar.pack(side="left", padx=(0, 10))
        
        # User info
        user_info = ctk.CTkFrame(profile_frame, fg_color="transparent")
        user_info.pack(side="left", padx=(0, 15))
        
        name_label = ctk.CTkLabel(
            user_info,
            text=self.user_data['name'],
            font=ctk.CTkFont(size=13, weight="bold")
        )
        name_label.pack(anchor="e")
        
        email_label = ctk.CTkLabel(
            user_info,
            text=self.user_data['email'],
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        email_label.pack(anchor="e")
        
        # Logout button
        logout_btn = ctk.CTkButton(
            profile_frame,
            text="Logout",
            command=self._logout,
            width=80,
            height=32,
            fg_color=("#dc3545", "#c82333"),
            hover_color=("#c82333", "#bd2130")
        )
        logout_btn.pack(side="left", padx=(10, 0))
    
    def _create_smartconnect_content(self):
        """Create SmartConnect content area."""
        # Content frame
        content_frame = ctk.CTkFrame(self.root)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        try:
            # Import required modules
            from database import ContactDatabase
            from contact_manager import ContactManager
            from search_engine import ContactSearchEngine
            
            # Initialize backend components directly
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contacts.db")
            database = ContactDatabase(db_path)
            database.set_current_user(self.user_data['id'])
            
            contact_manager = ContactManager(database)
            search_engine = ContactSearchEngine(contact_manager)
            
            # Create SmartConnect GUI components manually in our content frame
            self._create_embedded_smartconnect(content_frame, database, contact_manager, search_engine)
            
            # Show welcome message
            self.root.after(500, lambda: messagebox.showinfo(
                "Welcome!",
                f"Welcome {self.user_data['name']}!\n\n"
                "Your contacts are private and only visible to you.\n"
                "Start adding contacts using the form on the right."
            ))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load SmartConnect:\n{str(e)}")
            self._show_login_screen()
    
    def _create_embedded_smartconnect(self, parent_frame, database, contact_manager, search_engine):
        """Create embedded SmartConnect GUI components."""
        # Store references
        self.database = database
        self.contact_manager = contact_manager
        self.search_engine = search_engine
        self.selected_contact_id = None
        self.form_entries = {}
        self.validation_labels = {}
        
        # Configure parent frame grid
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)
        
        # Create search frame
        self._create_embedded_search_frame(parent_frame)
        
        # Create main content (contact list + form)
        self._create_embedded_main_content(parent_frame)
        
        # Create status bar
        self._create_embedded_status_bar(parent_frame)
        
        # Load contacts
        self._refresh_embedded_contact_list()
    
    def _create_embedded_search_frame(self, parent):
        """Create search interface."""
        search_frame = ctk.CTkFrame(parent)
        search_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        search_frame.grid_columnconfigure(1, weight=1)
        
        # Search label
        search_label = ctk.CTkLabel(search_frame, text="Search:")
        search_label.grid(row=0, column=0, padx=10, pady=10)
        
        # Search entry
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search by name or phone...")
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        self.search_entry.bind("<KeyRelease>", lambda e: self._refresh_embedded_contact_list())
        
        # Sort options
        sort_label = ctk.CTkLabel(search_frame, text="Sort by:")
        sort_label.grid(row=0, column=2, padx=10, pady=10)
        
        self.sort_var = ctk.StringVar(value="name")
        sort_menu = ctk.CTkOptionMenu(search_frame, values=["name", "recent"],
                                     variable=self.sort_var,
                                     command=lambda v: self._refresh_embedded_contact_list())
        sort_menu.grid(row=0, column=3, padx=10, pady=10)
        
        # Clear button
        clear_btn = ctk.CTkButton(search_frame, text="Clear", width=80,
                                 command=self._clear_embedded_search)
        clear_btn.grid(row=0, column=4, padx=10, pady=10)
    
    def _create_embedded_main_content(self, parent):
        """Create main content area with contact list and form."""
        content_frame = ctk.CTkFrame(parent)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        content_frame.grid_columnconfigure(0, weight=2)
        content_frame.grid_columnconfigure(1, weight=3)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Contact list (left)
        self._create_embedded_contact_list(content_frame)
        
        # Contact form (right)
        self._create_embedded_contact_form(content_frame)
    
    def _create_embedded_contact_list(self, parent):
        """Create contact list frame."""
        list_frame = ctk.CTkFrame(parent)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header = ctk.CTkLabel(list_frame, text="Contacts", font=ctk.CTkFont(size=16, weight="bold"))
        header.grid(row=0, column=0, pady=10)
        
        # Scrollable list
        self.contact_listbox = ctk.CTkScrollableFrame(list_frame)
        self.contact_listbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.contact_listbox.grid_columnconfigure(0, weight=1)
    
    def _create_embedded_contact_form(self, parent):
        """Create contact form."""
        form_frame = ctk.CTkFrame(parent)
        form_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Header
        self.form_header = ctk.CTkLabel(form_frame, text="Contact Details", 
                                       font=ctk.CTkFont(size=16, weight="bold"))
        self.form_header.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Form fields
        fields = [
            ("Name*", "name"),
            ("Phone", "phone"),
            ("Email", "email"),
            ("Address", "address"),
            ("Company", "company"),
            ("Job Title", "job_title")
        ]
        
        for i, (label_text, field_name) in enumerate(fields, start=1):
            label = ctk.CTkLabel(form_frame, text=label_text)
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            
            entry = ctk.CTkEntry(form_frame, width=300)
            entry.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
            self.form_entries[field_name] = entry
            
            error_label = ctk.CTkLabel(form_frame, text="", text_color="red", font=ctk.CTkFont(size=10))
            error_label.grid(row=i, column=2, sticky="w", padx=5, pady=5)
            self.validation_labels[field_name] = error_label
        
        # Category
        category_label = ctk.CTkLabel(form_frame, text="Category")
        category_label.grid(row=len(fields) + 1, column=0, sticky="w", padx=10, pady=5)
        
        self.category_var = ctk.StringVar(value="Friends")
        category_menu = ctk.CTkOptionMenu(form_frame, values=["Family", "Friends", "Work"],
                                         variable=self.category_var)
        category_menu.grid(row=len(fields) + 1, column=1, sticky="ew", padx=10, pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame)
        button_frame.grid(row=len(fields) + 2, column=0, columnspan=3, pady=20)
        
        self.save_btn = ctk.CTkButton(button_frame, text="Save Contact", 
                                     command=self._save_embedded_contact)
        self.save_btn.grid(row=0, column=0, padx=10)
        
        self.update_btn = ctk.CTkButton(button_frame, text="Update Contact", 
                                       command=self._update_embedded_contact)
        self.update_btn.grid(row=0, column=1, padx=10)
        self.update_btn.grid_remove()
        
        self.delete_btn = ctk.CTkButton(button_frame, text="Delete Contact", 
                                       fg_color="red", hover_color="darkred",
                                       command=self._delete_embedded_contact)
        self.delete_btn.grid(row=0, column=2, padx=10)
        self.delete_btn.grid_remove()
        
        clear_btn = ctk.CTkButton(button_frame, text="Clear Form", 
                                 command=self._clear_embedded_form)
        clear_btn.grid(row=0, column=3, padx=10)
    
    def _create_embedded_status_bar(self, parent):
        """Create status bar."""
        status_frame = ctk.CTkFrame(parent, height=30)
        status_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=(0, 5))
        status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(status_frame, text="Ready")
        self.status_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        self.count_label = ctk.CTkLabel(status_frame, text="")
        self.count_label.grid(row=0, column=1, sticky="e", padx=10, pady=5)
    
    def _refresh_embedded_contact_list(self):
        """Refresh contact list."""
        # Clear existing
        for widget in self.contact_listbox.winfo_children():
            widget.destroy()
        
        # Get contacts
        search_query = self.search_entry.get() if hasattr(self, 'search_entry') else ""
        sort_by = self.sort_var.get() if hasattr(self, 'sort_var') else "name"
        
        if search_query.strip():
            contacts = self.search_engine.search_combined(search_query)
            if sort_by == "recent":
                contacts = self.search_engine.sort_contacts(contacts, "recent")
            else:
                contacts = self.search_engine.sort_contacts(contacts, "name")
        else:
            contacts = self.contact_manager.get_all_contacts(sort_by)
        
        # Display contacts
        if not contacts:
            empty_frame = ctk.CTkFrame(self.contact_listbox, fg_color="transparent")
            empty_frame.grid(row=0, column=0, pady=20, padx=20, sticky="ew")
            
            empty_icon = ctk.CTkLabel(empty_frame, text="📇", font=ctk.CTkFont(size=32))
            empty_icon.pack(pady=(0, 10))
            
            if search_query.strip():
                empty_label = ctk.CTkLabel(empty_frame, text=f"No contacts found for '{search_query}'",
                                          font=ctk.CTkFont(size=14, weight="bold"))
            else:
                empty_label = ctk.CTkLabel(empty_frame, text="No contacts yet",
                                          font=ctk.CTkFont(size=14, weight="bold"))
            empty_label.pack()
            
            suggestion = ctk.CTkLabel(empty_frame, 
                                     text="Add your first contact using the form on the right",
                                     font=ctk.CTkFont(size=12), text_color="gray")
            suggestion.pack(pady=(5, 0))
        else:
            for i, contact in enumerate(contacts):
                self._create_embedded_contact_item(contact, i)
        
        # Update count
        total = self.contact_manager.get_contact_count()
        if search_query.strip():
            self.count_label.configure(text=f"Showing {len(contacts)} of {total} contacts")
        else:
            self.count_label.configure(text=f"Total contacts: {total}")
    
    def _create_embedded_contact_item(self, contact, row):
        """Create contact item widget."""
        from models import Contact
        
        item_frame = ctk.CTkFrame(self.contact_listbox)
        item_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
        item_frame.grid_columnconfigure(0, weight=1)
        
        name_label = ctk.CTkLabel(item_frame, text=contact.name, 
                                 font=ctk.CTkFont(size=14, weight="bold"))
        name_label.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 0))
        
        details = []
        if contact.phone:
            details.append(f"📞 {contact.phone}")
        if contact.email:
            details.append(f"✉️ {contact.email}")
        if contact.company:
            details.append(f"🏢 {contact.company}")
        
        if details:
            details_text = " | ".join(details)
            details_label = ctk.CTkLabel(item_frame, text=details_text, font=ctk.CTkFont(size=12))
            details_label.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 5))
        
        def on_click(event=None, cid=contact.id):
            self._select_embedded_contact(cid)
        
        item_frame.bind("<Button-1>", on_click)
        name_label.bind("<Button-1>", on_click)
        if details:
            details_label.bind("<Button-1>", on_click)
    
    def _select_embedded_contact(self, contact_id):
        """Select and populate form with contact."""
        contact = self.contact_manager.get_contact(contact_id)
        if contact:
            self.selected_contact_id = contact_id
            
            self.form_entries['name'].delete(0, 'end')
            self.form_entries['name'].insert(0, contact.name)
            
            self.form_entries['phone'].delete(0, 'end')
            self.form_entries['phone'].insert(0, contact.phone)
            
            self.form_entries['email'].delete(0, 'end')
            self.form_entries['email'].insert(0, contact.email)
            
            self.form_entries['address'].delete(0, 'end')
            self.form_entries['address'].insert(0, contact.address)
            
            self.form_entries['company'].delete(0, 'end')
            self.form_entries['company'].insert(0, contact.company)
            
            self.form_entries['job_title'].delete(0, 'end')
            self.form_entries['job_title'].insert(0, contact.job_title)
            
            self.category_var.set(contact.category)
            
            # Switch to edit mode
            self.form_header.configure(text=f"Editing: {contact.name}")
            self.save_btn.grid_remove()
            self.update_btn.grid()
            self.delete_btn.grid()
            
            self.status_label.configure(text=f"Selected: {contact.name}")
    
    def _save_embedded_contact(self):
        """Save new contact."""
        contact_data = {
            'name': self.form_entries['name'].get(),
            'phone': self.form_entries['phone'].get(),
            'email': self.form_entries['email'].get(),
            'address': self.form_entries['address'].get(),
            'company': self.form_entries['company'].get(),
            'job_title': self.form_entries['job_title'].get(),
            'category': self.category_var.get()
        }
        
        success, message = self.contact_manager.create_contact(contact_data)
        
        if success:
            messagebox.showinfo("Success", message)
            self._clear_embedded_form()
            self._refresh_embedded_contact_list()
        else:
            messagebox.showerror("Error", message)
    
    def _update_embedded_contact(self):
        """Update selected contact."""
        if not self.selected_contact_id:
            messagebox.showerror("Error", "No contact selected")
            return
        
        contact_data = {
            'name': self.form_entries['name'].get(),
            'phone': self.form_entries['phone'].get(),
            'email': self.form_entries['email'].get(),
            'address': self.form_entries['address'].get(),
            'company': self.form_entries['company'].get(),
            'job_title': self.form_entries['job_title'].get(),
            'category': self.category_var.get()
        }
        
        success, message = self.contact_manager.update_contact(self.selected_contact_id, contact_data)
        
        if success:
            messagebox.showinfo("Success", message)
            self._refresh_embedded_contact_list()
        else:
            messagebox.showerror("Error", message)
    
    def _delete_embedded_contact(self):
        """Delete selected contact."""
        if not self.selected_contact_id:
            messagebox.showerror("Error", "No contact selected")
            return
        
        contact = self.contact_manager.get_contact(self.selected_contact_id)
        if contact and messagebox.askyesno("Confirm Delete", 
                                          f"Delete contact '{contact.name}'?\n\nThis cannot be undone."):
            success, message = self.contact_manager.delete_contact(self.selected_contact_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self._clear_embedded_form()
                self._refresh_embedded_contact_list()
            else:
                messagebox.showerror("Error", message)
    
    def _clear_embedded_form(self):
        """Clear form and reset to new mode."""
        for entry in self.form_entries.values():
            entry.delete(0, 'end')
        
        self.category_var.set("Friends")
        self.selected_contact_id = None
        
        self.form_header.configure(text="Contact Details")
        self.save_btn.grid()
        self.update_btn.grid_remove()
        self.delete_btn.grid_remove()
        
        self.status_label.configure(text="Ready")
    
    def _clear_embedded_search(self):
        """Clear search field."""
        self.search_entry.delete(0, 'end')
        self._refresh_embedded_contact_list()
    
    def _logout(self):
        """Logout user."""
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
            self.auth_system.logout(self.session_token)
            self.session_token = None
            self.user_data = None
            self._show_login_screen()
    
    def _open_admin_panel(self):
        """Open admin panel for user management (embedded in same window)."""
        try:
            # Clear current content
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Recreate profile header with "Back to Contacts" button
            self._create_admin_header()
            
            # Create admin panel content
            self._create_admin_panel_content()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open admin panel:\n{str(e)}")
    
    def _create_admin_header(self):
        """Create profile header for admin panel with back button."""
        header = ctk.CTkFrame(self.root, height=60, fg_color=("#2b2b2b", "#1a1a1a"))
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header.grid_columnconfigure(1, weight=1)
        header.grid_propagate(False)
        
        # App title/logo
        title = ctk.CTkLabel(
            header,
            text="SmartConnect - Admin Panel",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#ffffff", "#ffffff")
        )
        title.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        # Profile section (right side)
        profile_frame = ctk.CTkFrame(header, fg_color="transparent")
        profile_frame.grid(row=0, column=2, padx=20, pady=10, sticky="e")
        
        # Back to Contacts button
        back_btn = ctk.CTkButton(
            profile_frame,
            text="← Back to Contacts",
            command=self._back_to_contacts,
            width=140,
            height=32,
            fg_color=("#6c757d", "#5a6268"),
            hover_color=("#5a6268", "#545b62")
        )
        back_btn.pack(side="left", padx=(0, 15))
        
        # User avatar/icon
        avatar = ctk.CTkLabel(
            profile_frame,
            text="👤",
            font=ctk.CTkFont(size=24)
        )
        avatar.pack(side="left", padx=(0, 10))
        
        # User info
        user_info = ctk.CTkFrame(profile_frame, fg_color="transparent")
        user_info.pack(side="left", padx=(0, 15))
        
        name_label = ctk.CTkLabel(
            user_info,
            text=self.user_data['name'],
            font=ctk.CTkFont(size=13, weight="bold")
        )
        name_label.pack(anchor="e")
        
        email_label = ctk.CTkLabel(
            user_info,
            text=self.user_data['email'],
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        email_label.pack(anchor="e")
        
        # Logout button
        logout_btn = ctk.CTkButton(
            profile_frame,
            text="Logout",
            command=self._logout,
            width=80,
            height=32,
            fg_color=("#dc3545", "#c82333"),
            hover_color=("#c82333", "#bd2130")
        )
        logout_btn.pack(side="left", padx=(10, 0))
    
    def _back_to_contacts(self):
        """Go back to contacts view."""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Recreate contacts view
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        self._create_profile_header()
        self._create_smartconnect_content()
    
    def _create_admin_panel_content(self):
        """Create admin panel content embedded in main window."""
        from admin_user_controller import AdminUserController
        
        # Initialize controller first
        self.admin_controller = AdminUserController(self.auth_system)
        
        # Main container with proper sizing
        main_frame = ctk.CTkFrame(self.root)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)  # User list should expand
        
        # Statistics panel - ensure it has enough space
        self._create_admin_statistics(main_frame)
        
        # User list container with improved layout
        list_container = ctk.CTkFrame(main_frame)
        list_container.grid(row=1, column=0, sticky="nsew", padx=0, pady=(5, 0))
        list_container.grid_columnconfigure(0, weight=1)
        list_container.grid_rowconfigure(1, weight=1)
        
        # User list header with better styling
        header_frame = ctk.CTkFrame(list_container, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(10, 5))
        header_frame.grid_columnconfigure(0, weight=1)
        
        list_header = ctk.CTkLabel(
            header_frame,
            text="User Accounts",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        list_header.grid(row=0, column=0, sticky="w", padx=15)
        
        # Column headers for better alignment
        headers_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        headers_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(5, 0))
        headers_frame.grid_columnconfigure(0, weight=0)
        headers_frame.grid_columnconfigure(1, weight=1)
        headers_frame.grid_columnconfigure(2, weight=0)
        headers_frame.grid_columnconfigure(3, weight=0)
        
        # Header labels with proper spacing
        name_header = ctk.CTkLabel(
            headers_frame,
            text="Name & Email",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="gray",
            anchor="w",
            width=280
        )
        name_header.grid(row=0, column=0, sticky="w", padx=(5, 0))
        
        role_header = ctk.CTkLabel(
            headers_frame,
            text="Role & Status",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="gray",
            anchor="center",
            width=180
        )
        role_header.grid(row=0, column=2, padx=10)
        
        actions_header = ctk.CTkLabel(
            headers_frame,
            text="Actions",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="gray",
            anchor="center",
            width=150
        )
        actions_header.grid(row=0, column=3, padx=(10, 5))
        
        # Scrollable frame for users
        self.admin_users_frame = ctk.CTkScrollableFrame(list_container, fg_color="transparent")
        self.admin_users_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        self.admin_users_frame.grid_columnconfigure(0, weight=1)
        
        # Action buttons with better layout
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=(5, 0))
        
        create_btn = ctk.CTkButton(
            button_frame,
            text="➕ Create User",
            command=self._admin_create_user,
            width=140,
            height=36,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        create_btn.pack(side="left", padx=(15, 8), pady=10)
        
        refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Refresh",
            command=self._admin_load_users,
            width=110,
            height=36,
            fg_color="#6c757d",
            hover_color="#5a6268",
            font=ctk.CTkFont(size=13)
        )
        refresh_btn.pack(side="left", padx=2, pady=10)
        
        # Load users
        self._admin_load_users()
    
    def _create_admin_statistics(self, parent):
        """Create statistics panel for admin with perfect alignment."""
        stats_frame = ctk.CTkFrame(parent)
        stats_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 15))
        
        # Configure equal column weights for perfect alignment
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1, uniform="stat_cards")
        
        # Get statistics with session token
        if hasattr(self, 'admin_controller'):
            success, message, stats = self.admin_controller.get_user_statistics(self.session_token)
            if not success:
                stats = {'total_users': 0, 'active_users': 0, 'banned_users': 0, 'admin_users': 0}
        else:
            stats = {'total_users': 0, 'active_users': 0, 'banned_users': 0, 'admin_users': 0}
        
        # Create stat cards with equal sizing
        stat_items = [
            ("Total Users", stats.get('total_users', 0), "#3498db"),
            ("Active Users", stats.get('active_users', 0), "#2ecc71"),
            ("Banned Users", stats.get('banned_users', 0), "#e74c3c"),
            ("Admins", stats.get('admin_users', 0), "#9b59b6")
        ]
        
        for i, (label, value, color) in enumerate(stat_items):
            # Create card with fixed height
            card = ctk.CTkFrame(stats_frame, fg_color=color, corner_radius=10, height=120)
            card.grid(row=0, column=i, sticky="ew", padx=5, pady=15, ipadx=10, ipady=10)
            card.grid_propagate(False)  # Maintain fixed height
            
            # Center content in card
            card.grid_rowconfigure(0, weight=1)
            card.grid_rowconfigure(1, weight=1)
            card.grid_columnconfigure(0, weight=1)
            
            value_label = ctk.CTkLabel(
                card,
                text=str(value),
                font=ctk.CTkFont(size=32, weight="bold"),
                text_color="white"
            )
            value_label.grid(row=0, column=0, sticky="ew", pady=(15, 0))
            
            text_label = ctk.CTkLabel(
                card,
                text=label,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white"
            )
            text_label.grid(row=1, column=0, sticky="ew", pady=(0, 15))
    
    def _admin_load_users(self):
        """Load and display users in admin panel."""
        # Clear existing users only (not the whole interface)
        for widget in self.admin_users_frame.winfo_children():
            widget.destroy()
        
        # Get all users - returns (success, message, users)
        result = self.admin_controller.get_all_users(self.session_token)
        
        if len(result) == 3:
            success, message, users = result
        else:
            success, users = result
            message = ""
        
        if not success:
            error_label = ctk.CTkLabel(
                self.admin_users_frame,
                text=f"Failed to load users: {message}",
                font=ctk.CTkFont(size=14),
                text_color="red"
            )
            error_label.pack(pady=20)
            return
        
        if not users:
            empty_label = ctk.CTkLabel(
                self.admin_users_frame,
                text="No users found",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            empty_label.pack(pady=20)
            return
        
        # Display users
        for user in users:
            self._create_admin_user_card(user)
        
        # Refresh statistics only - don't destroy the whole layout
        self._refresh_admin_statistics()
    
    def _refresh_admin_statistics(self):
        """Refresh statistics without destroying layout."""
        try:
            # Find the main frame
            main_frame = None
            for widget in self.root.winfo_children():
                if isinstance(widget, ctk.CTkFrame) and widget.grid_info().get('row') == 1:
                    main_frame = widget
                    break
            
            if not main_frame:
                return
            
            # Find and update the statistics frame
            stats_frame = None
            for widget in main_frame.winfo_children():
                if isinstance(widget, ctk.CTkFrame) and widget.grid_info().get('row') == 0:
                    stats_frame = widget
                    break
            
            if stats_frame:
                # Get updated statistics
                success, message, stats = self.admin_controller.get_user_statistics(self.session_token)
                if success:
                    # Update the stat cards
                    stat_values = [
                        stats.get('total_users', 0),
                        stats.get('active_users', 0),
                        stats.get('banned_users', 0),
                        stats.get('admin_users', 0)
                    ]
                    
                    # Find and update each stat card
                    card_index = 0
                    for widget in stats_frame.winfo_children():
                        if isinstance(widget, ctk.CTkFrame) and card_index < len(stat_values):
                            # Find the value label in this card
                            for card_widget in widget.winfo_children():
                                if isinstance(card_widget, ctk.CTkLabel):
                                    try:
                                        # Check if this is a number (the value label)
                                        int(card_widget.cget("text"))
                                        card_widget.configure(text=str(stat_values[card_index]))
                                        break
                                    except:
                                        continue
                            card_index += 1
        except Exception as e:
            print(f"Error refreshing statistics: {e}")
            # If refresh fails, just skip it
    
    def _create_admin_user_card(self, user):
        """Create user card in admin panel with perfect alignment."""
        card = ctk.CTkFrame(self.admin_users_frame)
        card.pack(fill="x", padx=5, pady=3)
        
        # Configure grid for perfect alignment
        card.grid_columnconfigure(0, weight=0)  # Name column - fixed width
        card.grid_columnconfigure(1, weight=1)  # Spacer - expandable
        card.grid_columnconfigure(2, weight=0)  # Role/Status - fixed width
        card.grid_columnconfigure(3, weight=0)  # Actions - fixed width
        
        # User info (left side) - reduced width to match header
        info_frame = ctk.CTkFrame(card, fg_color="transparent", width=280)
        info_frame.grid(row=0, column=0, sticky="w", padx=10, pady=12)
        info_frame.grid_propagate(False)  # Maintain fixed width
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=user['name'],
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        name_label.pack(anchor="w", fill="x")
        
        email_label = ctk.CTkLabel(
            info_frame,
            text=user['email'],
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w"
        )
        email_label.pack(anchor="w", fill="x")
        
        # Role and status (center-right) - reduced width
        role_status_frame = ctk.CTkFrame(card, fg_color="transparent", width=180)
        role_status_frame.grid(row=0, column=2, padx=10, pady=12, sticky="e")
        role_status_frame.grid_propagate(False)
        
        # Role badge
        role_color = "#9b59b6" if user['role'] == 'admin' else "#3498db"
        role_label = ctk.CTkLabel(
            role_status_frame,
            text=user['role'].upper(),
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=role_color,
            width=55
        )
        role_label.pack(side="left", padx=(0, 8))
        
        # Status badge
        status_color = "#2ecc71" if user['status'] == 'active' else "#e74c3c"
        status_label = ctk.CTkLabel(
            role_status_frame,
            text=user['status'].upper(),
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=status_color,
            width=55
        )
        status_label.pack(side="left", padx=(0, 5))
        
        # Action buttons (right side) - reduced width
        action_frame = ctk.CTkFrame(card, fg_color="transparent", width=150)
        action_frame.grid(row=0, column=3, padx=10, pady=12, sticky="e")
        action_frame.grid_propagate(False)
        
        if user['status'] == 'active':
            ban_btn = ctk.CTkButton(
                action_frame,
                text="Ban",
                command=lambda u=user: self._admin_ban_user(u['id']),
                width=65,
                height=28,
                fg_color="#e74c3c",
                hover_color="#c0392b",
                font=ctk.CTkFont(size=11)
            )
            ban_btn.pack(side="left", padx=1)
        else:
            unban_btn = ctk.CTkButton(
                action_frame,
                text="Unban",
                command=lambda u=user: self._admin_unban_user(u['id']),
                width=65,
                height=28,
                fg_color="#2ecc71",
                hover_color="#27ae60",
                font=ctk.CTkFont(size=11)
            )
            unban_btn.pack(side="left", padx=1)
        
        delete_btn = ctk.CTkButton(
            action_frame,
            text="Delete",
            command=lambda u=user: self._admin_delete_user(u['id'], u['name']),
            width=65,
            height=28,
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            font=ctk.CTkFont(size=11)
        )
        delete_btn.pack(side="left", padx=1)
    
    def _admin_create_user(self):
        """Create new user dialog."""
        from user_creation_dialog import UserCreationDialog
        
        dialog = UserCreationDialog(self.root, self.auth_system)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self._admin_load_users()
    
    def _admin_ban_user(self, user_id):
        """Ban a user."""
        if messagebox.askyesno("Confirm Ban", "Are you sure you want to ban this user?"):
            success, message = self.admin_controller.ban_user(self.session_token, user_id)
            if success:
                messagebox.showinfo("Success", message)
                self._admin_load_users()
            else:
                messagebox.showerror("Error", message)
    
    def _admin_unban_user(self, user_id):
        """Unban a user."""
        success, message = self.admin_controller.reactivate_user(self.session_token, user_id)
        if success:
            messagebox.showinfo("Success", message)
            self._admin_load_users()
        else:
            messagebox.showerror("Error", message)
    
    def _admin_delete_user(self, user_id, user_name):
        """Delete a user."""
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to permanently delete user '{user_name}'?\n\nThis action cannot be undone."):
            success, message = self.admin_controller.delete_user(self.session_token, user_id)
            if success:
                messagebox.showinfo("Success", message)
                self._admin_load_users()
            else:
                messagebox.showerror("Error", message)


if __name__ == "__main__":
    try:
        app = SmartConnectWithLogin()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Failed to start application:\n{str(e)}")
        sys.exit(1)
