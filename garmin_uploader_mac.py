#!/usr/bin/env python3
"""
Garmin Workout Uploader for Mac
A guided app to upload .FIT workout files to your Garmin watch.
"""

import os
import sys
import shutil
import subprocess
import webbrowser
from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog, messagebox

class GarminUploaderMac:
    def __init__(self, root):
        self.root = root
        self.root.title("Garmin Workout Uploader")
        self.root.geometry("580x620")
        self.root.resizable(False, False)
        
        # Styling
        self.root.configure(bg='#f5f5f7')
        
        self.style = ttk.Style()
        self.style.configure("Title.TLabel", font=('SF Pro Display', 22, 'bold'), background='#f5f5f7')
        self.style.configure("Subtitle.TLabel", font=('SF Pro Text', 12), background='#f5f5f7', foreground='#666')
        self.style.configure("Step.TLabel", font=('SF Pro Text', 11), background='#fff')
        self.style.configure("StepNum.TLabel", font=('SF Pro Display', 14, 'bold'), background='#007AFF', foreground='white')
        self.style.configure("Big.TButton", font=('SF Pro Text', 13), padding=12)
        self.style.configure("Card.TFrame", background='#fff')
        
        # Paths
        self.home = Path.home()
        self.staging_folder = self.home / "GarminWorkouts"
        self.staging_folder.mkdir(exist_ok=True)
        
        self.selected_files = []
        self.openmtp_installed = self.check_openmtp()
        
        self.create_ui()
    
    def check_openmtp(self):
        """Check if OpenMTP is installed"""
        paths = [
            Path("/Applications/OpenMTP.app"),
            self.home / "Applications/OpenMTP.app"
        ]
        return any(p.exists() for p in paths)
    
    def create_ui(self):
        """Create the main interface"""
        # Main container
        main = Frame(self.root, bg='#f5f5f7', padx=30, pady=25)
        main.pack(fill=BOTH, expand=True)
        
        # Header
        ttk.Label(main, text="Garmin Workout Uploader", style="Title.TLabel").pack()
        ttk.Label(main, text="Upload .FIT workouts to your Garmin watch", style="Subtitle.TLabel").pack(pady=(5, 20))
        
        # Step 1: Select Files
        self.create_step(main, "1", "Select Your Workout Files", self.create_file_selector)
        
        # Step 2: Prepare Transfer  
        self.create_step(main, "2", "Prepare for Transfer", self.create_prepare_section)
        
        # Step 3: Transfer Files
        self.create_step(main, "3", "Transfer to Watch", self.create_transfer_section)
        
        # Help link
        help_frame = Frame(main, bg='#f5f5f7')
        help_frame.pack(fill=X, pady=(15, 0))
        
        help_btn = Label(help_frame, text="Need help? Click here", fg='#007AFF', bg='#f5f5f7',
                        cursor='hand2', font=('SF Pro Text', 11, 'underline'))
        help_btn.pack()
        help_btn.bind('<Button-1>', lambda e: self.show_help())
    
    def create_step(self, parent, number, title, content_func):
        """Create a step card"""
        # Card frame
        card = Frame(parent, bg='#fff', highlightbackground='#e0e0e0', 
                    highlightthickness=1, padx=15, pady=12)
        card.pack(fill=X, pady=(0, 12))
        
        # Header row
        header = Frame(card, bg='#fff')
        header.pack(fill=X, pady=(0, 10))
        
        # Step number circle
        num_canvas = Canvas(header, width=28, height=28, bg='#fff', highlightthickness=0)
        num_canvas.pack(side=LEFT, padx=(0, 10))
        num_canvas.create_oval(2, 2, 26, 26, fill='#007AFF', outline='')
        num_canvas.create_text(14, 14, text=number, fill='white', font=('SF Pro Display', 13, 'bold'))
        
        # Title
        Label(header, text=title, font=('SF Pro Text', 13, 'bold'), bg='#fff').pack(side=LEFT)
        
        # Content
        content_frame = Frame(card, bg='#fff')
        content_frame.pack(fill=X)
        content_func(content_frame)
    
    def create_file_selector(self, parent):
        """Step 1: File selection"""
        # Listbox
        list_frame = Frame(parent, bg='#fff')
        list_frame.pack(fill=X)
        
        self.file_listbox = Listbox(list_frame, height=4, font=('SF Pro Text', 11),
                                     selectbackground='#007AFF', activestyle='none',
                                     highlightthickness=1, highlightbackground='#e0e0e0',
                                     relief=FLAT)
        self.file_listbox.pack(fill=X, pady=(0, 8))
        
        # Placeholder text
        self.file_listbox.insert(END, "  No files selected - click 'Add Files' below")
        self.file_listbox.config(fg='#999')
        
        # Buttons
        btn_frame = Frame(parent, bg='#fff')
        btn_frame.pack(fill=X)
        
        self.add_btn = Button(btn_frame, text="＋ Add Files", font=('SF Pro Text', 11),
                              command=self.add_files, bg='#007AFF', fg='white',
                              padx=15, pady=5, relief=FLAT, cursor='hand2')
        self.add_btn.pack(side=LEFT)
        
        self.clear_btn = Button(btn_frame, text="Clear", font=('SF Pro Text', 11),
                                command=self.clear_files, padx=10, pady=5, relief=FLAT)
        self.clear_btn.pack(side=LEFT, padx=(8, 0))
        
        self.file_count = Label(btn_frame, text="", font=('SF Pro Text', 11), bg='#fff', fg='#666')
        self.file_count.pack(side=RIGHT)
    
    def create_prepare_section(self, parent):
        """Step 2: Prepare transfer"""
        # Instructions
        instructions = Frame(parent, bg='#fff')
        instructions.pack(fill=X)
        
        steps_text = """Before transferring, make sure:

✓  Your Garmin watch is connected via USB
✓  On your watch: Settings → System → USB Mode → MTP
✓  Accept "Use MTP" prompt on the watch if asked
✓  Garmin Express is closed (quit it if running)"""
        
        Label(instructions, text=steps_text, font=('SF Pro Text', 11), bg='#fff',
              justify=LEFT, anchor='w').pack(fill=X)
        
        # Prepare button
        self.prepare_btn = Button(parent, text="✓ Ready - Stage My Files", 
                                   font=('SF Pro Text', 12, 'bold'),
                                   command=self.stage_files, bg='#34C759', fg='white',
                                   padx=20, pady=8, relief=FLAT, cursor='hand2',
                                   state=DISABLED)
        self.prepare_btn.pack(pady=(12, 0))
    
    def create_transfer_section(self, parent):
        """Step 3: Transfer"""
        self.transfer_frame = parent
        
        # Initial state - waiting
        self.transfer_status = Label(parent, 
            text="Stage your files first (Step 2), then transfer instructions will appear here.",
            font=('SF Pro Text', 11), bg='#fff', fg='#666', wraplength=480, justify=LEFT)
        self.transfer_status.pack(fill=X)
    
    def add_files(self):
        """Open file dialog to add .FIT files"""
        files = filedialog.askopenfilenames(
            title="Select Workout Files",
            filetypes=[("FIT files", "*.fit *.FIT"), ("All files", "*.*")]
        )
        
        if not files:
            return
        
        # Clear placeholder if present
        if not self.selected_files:
            self.file_listbox.delete(0, END)
            self.file_listbox.config(fg='black')
        
        for f in files:
            if f not in self.selected_files:
                # Only accept .fit files
                if f.lower().endswith('.fit'):
                    self.selected_files.append(f)
                    name = os.path.basename(f)
                    self.file_listbox.insert(END, f"  📄 {name}")
        
        self.update_ui_state()
    
    def clear_files(self):
        """Clear all selected files"""
        self.selected_files = []
        self.file_listbox.delete(0, END)
        self.file_listbox.insert(END, "  No files selected - click 'Add Files' below")
        self.file_listbox.config(fg='#999')
        self.update_ui_state()
    
    def update_ui_state(self):
        """Update button states based on current state"""
        count = len(self.selected_files)
        
        if count > 0:
            self.file_count.config(text=f"{count} file{'s' if count != 1 else ''}")
            self.prepare_btn.config(state=NORMAL)
        else:
            self.file_count.config(text="")
            self.prepare_btn.config(state=DISABLED)
    
    def stage_files(self):
        """Copy files to staging folder and prepare for transfer"""
        if not self.selected_files:
            return
        
        # Kill Garmin Express
        self.kill_garmin_express()
        
        # Clear staging folder
        for f in self.staging_folder.glob('*.fit'):
            f.unlink()
        for f in self.staging_folder.glob('*.FIT'):
            f.unlink()
        
        # Copy files
        staged = []
        for filepath in self.selected_files:
            try:
                filename = os.path.basename(filepath)
                dest = self.staging_folder / filename
                shutil.copy2(filepath, dest)
                staged.append(filename)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy {filename}: {e}")
        
        if not staged:
            return
        
        # Update Step 3 with transfer instructions
        self.show_transfer_instructions(staged)
        
        # Open OpenMTP and staging folder
        self.open_openmtp()
        subprocess.run(['open', str(self.staging_folder)])
        
        # Show success
        self.prepare_btn.config(text="✓ Files Staged!", bg='#666', state=DISABLED)
    
    def show_transfer_instructions(self, staged_files):
        """Show detailed transfer instructions in Step 3"""
        # Clear current content
        for widget in self.transfer_frame.winfo_children():
            widget.destroy()
        
        # Success message
        success_frame = Frame(self.transfer_frame, bg='#e8f5e9', padx=10, pady=8)
        success_frame.pack(fill=X, pady=(0, 10))
        
        Label(success_frame, text=f"✓ {len(staged_files)} file(s) ready to transfer!", 
              font=('SF Pro Text', 12, 'bold'), bg='#e8f5e9', fg='#2e7d32').pack()
        
        # Instructions with visual
        instr = Frame(self.transfer_frame, bg='#fff')
        instr.pack(fill=X)
        
        # Visual diagram
        diagram = """
┌─────────────────────┐         ┌─────────────────────┐
│   📁 GarminWorkouts │   ───►  │  📁 GARMIN          │
│   (Finder window)   │  DRAG   │     └─ 📁 NewFiles  │
│                     │         │        (in OpenMTP) │
└─────────────────────┘         └─────────────────────┘
"""
        
        Label(instr, text="Drag your files:", font=('SF Pro Text', 11, 'bold'), 
              bg='#fff', anchor='w').pack(fill=X)
        
        Label(instr, text=diagram, font=('Menlo', 10), bg='#f8f8f8', 
              justify=LEFT, padx=10, pady=5).pack(fill=X, pady=5)
        
        steps = """1. A Finder window opened with your workout files
2. OpenMTP should show your Garmin watch
3. In OpenMTP: Navigate to GARMIN → NewFiles
4. Drag all .fit files from Finder into NewFiles
5. Wait for transfer to complete
6. Disconnect watch - done! 🎉"""
        
        Label(instr, text=steps, font=('SF Pro Text', 11), bg='#fff',
              justify=LEFT, anchor='w').pack(fill=X, pady=(5, 0))
        
        # Buttons
        btn_frame = Frame(self.transfer_frame, bg='#fff')
        btn_frame.pack(fill=X, pady=(12, 0))
        
        Button(btn_frame, text="📂 Open Folder Again", font=('SF Pro Text', 11),
               command=lambda: subprocess.run(['open', str(self.staging_folder)]),
               padx=10, pady=5, relief=FLAT).pack(side=LEFT)
        
        Button(btn_frame, text="🔄 Open OpenMTP", font=('SF Pro Text', 11),
               command=self.open_openmtp, padx=10, pady=5, relief=FLAT).pack(side=LEFT, padx=(8, 0))
        
        # If OpenMTP not installed
        if not self.openmtp_installed:
            warning = Frame(self.transfer_frame, bg='#fff3e0', padx=10, pady=8)
            warning.pack(fill=X, pady=(10, 0))
            
            Label(warning, text="⚠️ OpenMTP not found!", 
                  font=('SF Pro Text', 11, 'bold'), bg='#fff3e0', fg='#e65100').pack()
            
            Label(warning, text="Download it free from: openmtp.ganeshrvel.com", 
                  font=('SF Pro Text', 11), bg='#fff3e0').pack()
            
            Button(warning, text="Download OpenMTP", font=('SF Pro Text', 11),
                   command=lambda: webbrowser.open('https://openmtp.ganeshrvel.com'),
                   bg='#ff9800', fg='white', padx=10, pady=5, relief=FLAT,
                   cursor='hand2').pack(pady=(5, 0))
    
    def kill_garmin_express(self):
        """Kill Garmin Express to free MTP access"""
        subprocess.run(['pkill', '-f', 'Garmin Express'], capture_output=True)
        subprocess.run(['pkill', '-f', 'GarminExpressService'], capture_output=True)
    
    def open_openmtp(self):
        """Open OpenMTP application"""
        paths = [
            "/Applications/OpenMTP.app",
            str(self.home / "Applications/OpenMTP.app")
        ]
        
        for path in paths:
            if os.path.exists(path):
                subprocess.run(['open', path])
                return True
        
        # Try Android File Transfer as fallback
        aft = "/Applications/Android File Transfer.app"
        if os.path.exists(aft):
            subprocess.run(['open', aft])
            return True
        
        return False
    
    def show_help(self):
        """Show help dialog"""
        help_window = Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("500x450")
        help_window.configure(bg='#f5f5f7')
        help_window.transient(self.root)
        
        frame = Frame(help_window, bg='#f5f5f7', padx=25, pady=20)
        frame.pack(fill=BOTH, expand=True)
        
        Label(frame, text="Help & Troubleshooting", font=('SF Pro Display', 18, 'bold'),
              bg='#f5f5f7').pack(pady=(0, 15))
        
        help_text = """Why do I need OpenMTP?
Mac doesn't support MTP (the protocol Garmin uses).
OpenMTP bridges this gap - it's free and works great.

Watch not showing in OpenMTP?
• Make sure USB cable supports data (not charge-only)
• On watch: Settings → System → USB Mode → MTP
• Quit Garmin Express completely
• Unplug and replug the watch
• Click "Refresh" in OpenMTP

Can't find NewFiles folder?
Look for: GARMIN → NewFiles
If only "Workouts" exists, use that instead.

Workouts not appearing on watch?
• Restart your watch after transfer
• Check: Training → Workouts
• Make sure files are valid .FIT workout files

Where do workouts come from?
• Create in Garmin Connect (web or app)
• Export from TrainingPeaks, Intervals.icu, etc.
• Download from training plan providers

My files are stuck in GarminWorkouts folder?
That's just the staging folder on your Mac.
You still need to drag them to OpenMTP."""
        
        Label(frame, text=help_text, font=('SF Pro Text', 11), bg='#f5f5f7',
              justify=LEFT, anchor='w').pack(fill=X)
        
        Button(frame, text="Get OpenMTP", font=('SF Pro Text', 11),
               command=lambda: webbrowser.open('https://openmtp.ganeshrvel.com'),
               bg='#007AFF', fg='white', padx=15, pady=8, relief=FLAT,
               cursor='hand2').pack(pady=(15, 10))
        
        Button(frame, text="Close", command=help_window.destroy,
               font=('SF Pro Text', 11), padx=15, pady=5, relief=FLAT).pack()


def main():
    root = Tk()
    
    # Center on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() - 580) // 2
    y = (root.winfo_screenheight() - 620) // 2
    root.geometry(f"+{x}+{y}")
    
    # Mac-specific styling
    root.tk.call('tk', 'scaling', 2.0)  # Retina support
    
    app = GarminUploaderMac(root)
    root.mainloop()


if __name__ == "__main__":
    main()
