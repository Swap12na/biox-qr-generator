"""
QR Code Generator Application
----------------------------
Author: Biox Systems Developer
Date: May 13, 2025
Organization: Biox Systems

Description:
    This application generates QR codes from URL inputs.
    Users can enter a URL, generate a QR code, and save it as an image file.
    Features include customizable QR code size, error correction, and various
    export options.
"""

import os
import io
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
import webbrowser

class QRCodeGenerator:
    """
    A class to create a GUI application for generating QR codes from URLs.
    """
    
    def __init__(self, root):
        """
        Initialize the application.
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        self.root.title("Biox Systems QR Code Generator")
        self.root.geometry("600x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Set application icon (uncomment and replace with actual icon path if available)
        # self.root.iconbitmap("path_to_icon.ico")
        
        self.qr_image = None
        self.pil_image = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface components."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Biox Systems QR Code Generator", 
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)
        
        # URL input frame
        input_frame = ttk.LabelFrame(main_frame, text="Enter URL", padding=10)
        input_frame.pack(fill=tk.X, pady=10)
        
        # URL entry
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(input_frame, textvariable=self.url_var, width=50)
        self.url_entry.pack(fill=tk.X, pady=5)
        
        # QR code options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding=10)
        options_frame.pack(fill=tk.X, pady=10)
        
        # QR code size option
        size_frame = ttk.Frame(options_frame)
        size_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(size_frame, text="QR Code Size:").pack(side=tk.LEFT, padx=5)
        
        self.size_var = tk.IntVar(value=10)
        size_scale = ttk.Scale(
            size_frame, 
            from_=5, 
            to=15,
            variable=self.size_var, 
            orient=tk.HORIZONTAL, 
            length=200
        )
        size_scale.pack(side=tk.LEFT, padx=10)
        
        self.size_label = ttk.Label(size_frame, text="10")
        self.size_label.pack(side=tk.LEFT, padx=5)
        
        # Update size label when scale is moved
        size_scale.configure(command=lambda val: self.size_label.configure(text=str(int(float(val)))))
        
        # Error correction level options
        error_frame = ttk.Frame(options_frame)
        error_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(error_frame, text="Error Correction:").pack(side=tk.LEFT, padx=5)
        
        self.error_var = tk.StringVar(value="H")
        error_options = ["L", "M", "Q", "H"]
        error_labels = {
            "L": "Low (7%)", 
            "M": "Medium (15%)", 
            "Q": "Quartile (25%)", 
            "H": "High (30%)"
        }
        
        for option in error_options:
            rb = ttk.Radiobutton(
                error_frame,
                text=error_labels[option],
                value=option,
                variable=self.error_var
            )
            rb.pack(side=tk.LEFT, padx=5)
            
        # Color options
        color_frame = ttk.Frame(options_frame)
        color_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(color_frame, text="QR Fill Color:").pack(side=tk.LEFT, padx=5)
        
        self.fill_color_var = tk.StringVar(value="black")
        fill_colors = ["black", "darkblue", "darkgreen", "darkred", "purple"]
        fill_combobox = ttk.Combobox(
            color_frame,
            textvariable=self.fill_color_var,
            values=fill_colors,
            width=10,
            state="readonly"
        )
        fill_combobox.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(color_frame, text="Background:").pack(side=tk.LEFT, padx=5)
        
        self.bg_color_var = tk.StringVar(value="white")
        bg_colors = ["white", "lightgray", "lightblue", "lightyellow"]
        bg_combobox = ttk.Combobox(
            color_frame,
            textvariable=self.bg_color_var,
            values=bg_colors,
            width=10,
            state="readonly"
        )
        bg_combobox.pack(side=tk.LEFT, padx=5)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Generate button
        generate_btn = ttk.Button(
            button_frame,
            text="Generate QR Code",
            command=self.generate_qr_code
        )
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Save button
        self.save_btn = ttk.Button(
            button_frame,
            text="Download Image",
            command=self.save_image,
            state=tk.DISABLED
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_btn = ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Copy to clipboard button
        self.copy_btn = ttk.Button(
            button_frame,
            text="Copy to Clipboard",
            command=self.copy_to_clipboard,
            state=tk.DISABLED
        )
        self.copy_btn.pack(side=tk.LEFT, padx=5)
        
        # QR code display frame
        self.display_frame = ttk.LabelFrame(main_frame, text="QR Code", padding=10)
        self.display_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # QR code image label
        self.qr_label = ttk.Label(self.display_frame)
        self.qr_label.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, anchor=tk.W)
        status_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Credits label (clickable link)
        credits_label = ttk.Label(
            status_frame, 
            text="Biox Systems QR Generator v1.0",
            foreground="blue", 
            cursor="hand2"
        )
        credits_label.pack(side=tk.RIGHT, padx=10, pady=5)
        credits_label.bind("<Button-1>", lambda e: webbrowser.open("https://www.biosystems.com"))
    
    def generate_qr_code(self):
        """Generate a QR code from the input URL."""
        url = self.url_var.get().strip()
        
        # Validate URL
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        
        # Add http:// prefix if not present
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
            self.url_var.set(url)
        
        try:
            # Update status
            self.status_var.set("Generating QR code...")
            self.root.update_idletasks()
            
            # Get error correction level
            error_level = self.error_var.get()
            error_correction = {
                'L': qrcode.constants.ERROR_CORRECT_L,
                'M': qrcode.constants.ERROR_CORRECT_M,
                'Q': qrcode.constants.ERROR_CORRECT_Q,
                'H': qrcode.constants.ERROR_CORRECT_H
            }[error_level]
            
            # Create QR code instance
            size = self.size_var.get()
            qr = qrcode.QRCode(
                version=1,
                error_correction=error_correction,
                box_size=size,
                border=4,
            )
            
            # Add data to QR code
            qr.add_data(url)
            qr.make(fit=True)
            
            # Get colors
            fill_color = self.fill_color_var.get()
            bg_color = self.bg_color_var.get()
            
            # Create an image from the QR code
            self.pil_image = qr.make_image(fill_color=fill_color, back_color=bg_color)
            
            # Display QR code
            self.display_qr_code()
            
            # Enable save and copy buttons
            self.save_btn.config(state=tk.NORMAL)
            self.copy_btn.config(state=tk.NORMAL)
            
            # Update status
            self.status_var.set(f"QR code generated for: {url}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")
            self.status_var.set("Error generating QR code")
    
    def display_qr_code(self):
        """Display the generated QR code in the UI."""
        # Resize image to fit display frame (keeping aspect ratio)
        display_width = self.display_frame.winfo_width() - 20
        display_height = self.display_frame.winfo_height() - 20
        
        if display_width <= 1:  # If frame width not yet determined
            display_width = 400
            display_height = 400
        
        # Convert PIL image to Tkinter PhotoImage
        image = self.pil_image.copy()
        
        # Resize while maintaining aspect ratio
        image_width, image_height = image.size
        ratio = min(display_width/image_width, display_height/image_height)
        new_width = int(image_width * ratio)
        new_height = int(image_height * ratio)
        
        image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Convert to PhotoImage
        self.qr_image = ImageTk.PhotoImage(image)
        
        # Update label with new image
        self.qr_label.configure(image=self.qr_image)
        self.qr_label.image = self.qr_image  # Keep a reference!
    
    def save_image(self):
        """Save the generated QR code as an image file."""
        if not self.pil_image:
            messagebox.showerror("Error", "No QR code to save")
            return
        
        # Get file save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ],
            initialfile="qr_code.png"
        )
        
        if not file_path:
            return  # User canceled
        
        try:
            # Save the image
            self.pil_image.save(file_path)
            
            # Update status
            self.status_var.set(f"QR code saved to: {os.path.basename(file_path)}")
            
            # Show success message
            messagebox.showinfo("Success", f"QR code saved successfully to:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save QR code: {str(e)}")
            self.status_var.set("Error saving QR code")
    
    def copy_to_clipboard(self):
        """Copy the generated QR code to clipboard."""
        if not self.pil_image:
            messagebox.showerror("Error", "No QR code to copy")
            return
        
        try:
            # Create a temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                temp_filename = temp_file.name
            
            # Save image to temporary file
            self.pil_image.save(temp_filename)
            
            # Copy to clipboard
            self.root.clipboard_clear()
            
            # Platform-specific clipboard handling
            import platform
            system = platform.system()
            
            if system == "Windows":
                # Use Pillow to copy to clipboard on Windows
                from PIL import ImageGrab
                image = Image.open(temp_filename)
                output = io.BytesIO()
                image.convert('RGB').save(output, 'BMP')
                data = output.getvalue()[14:]  # Remove header
                output.close()
                self.root.clipboard_append(data)
                
            elif system == "Darwin":  # macOS
                # Use subprocess to copy to clipboard on macOS
                import subprocess
                subprocess.run(['osascript', '-e', 
                               f'set the clipboard to (read (POSIX file "{temp_filename}") as JPEG picture)'])
                
            else:  # Linux and others
                # Try using xclip if available
                try:
                    import subprocess
                    subprocess.run(['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i', temp_filename])
                except FileNotFoundError:
                    messagebox.showinfo("Info", "Clipboard functionality requires xclip on Linux systems.")
                    return
            
            # Clean up temp file
            import os
            os.unlink(temp_filename)
            
            # Update status
            self.status_var.set("QR code copied to clipboard")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")
            self.status_var.set("Error copying to clipboard")
    
    def clear(self):
        """Clear the URL input and QR code display."""
        self.url_var.set("")
        self.qr_label.config(image="")
        self.qr_image = None
        self.pil_image = None
        self.save_btn.config(state=tk.DISABLED)
        self.copy_btn.config(state=tk.DISABLED)
        self.status_var.set("Ready")


if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()