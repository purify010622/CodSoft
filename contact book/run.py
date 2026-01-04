#!/usr/bin/env python3
"""
Simple launcher for SmartConnect Contact Management System
"""

import sys
import os
from tkinter import messagebox

def main():
    """Launch SmartConnect with integrated login."""
    try:
        # Set appearance
        import customtkinter as ctk
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Import and run the main application
        from smartconnect_with_login import SmartConnectWithLogin
        
        app = SmartConnectWithLogin()
        app.run()
        
    except ImportError as e:
        error_msg = f"Missing required dependencies: {e}\n\nPlease install requirements:\npip install -r requirements.txt"
        print(f"ERROR: {error_msg}")
        try:
            messagebox.showerror("Missing Dependencies", error_msg)
        except:
            pass
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"Failed to start SmartConnect: {str(e)}"
        print(f"ERROR: {error_msg}")
        try:
            messagebox.showerror("Application Error", error_msg)
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()