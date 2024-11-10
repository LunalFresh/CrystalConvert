import customtkinter as ctk
import ffmpeg
import os
import threading
from tkinter import filedialog, messagebox, Tk, Toplevel, Label

# Initialize the app with a custom theme and appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark_theme.json")

# Initialize the main app window
app = ctk.CTk()
app.title("File Converter")
app.geometry("400x500")  # Base size for app window
app.configure(bg="black")

# Global variables to store selected file paths and format options
selected_files = []
current_format_type = None

# Expanded format options for different file types, supported by FFmpeg
format_options = {
    "audio": ["MP3", "WAV", "AAC", "OGG", "FLAC", "M4A", "WMA", "OPUS", "AIFF", "ALAC", "DSD", "AC3", "EAC3", "PCM", "MP2", "MP1", "AMR", "GSM"],
    "video": ["MP4", "MKV", "AVI", "MOV", "WMV", "FLV", "MPEG", "WEBM", "M4V", "VOB", "OGV", "3GP", "TS", "RM", "ASF", "MTS", "DIVX"],
    "image": ["JPEG", "JPG", "PNG", "BMP", "TIFF", "WEBP", "PGM", "PPM", "TGA", "GIF"]
}

# User-configurable options for conversion parameters
bitrate_options = ["None", "64k - Low", "128k - Medium", "192k - High", "256k - Very High", "320k - Max Quality"]
resolution_options = ["None", "640x480 - SD", "1280x720 - HD", "1920x1080 - Full HD", "2560x1440 - QHD", "3840x2160 - 4K"]
codec_options = ["None", "libx264 - H.264", "libx265 - H.265", "aac - AAC Audio", "mp3 - MP3 Audio"]
quality_scale_options = ["None", "Low - Fastest", "Medium - Balanced", "High - Best Quality"]
compression_options = ["None", "fast - Quick Processing", "medium - Balanced Speed/Quality", "slow - Improved Quality", "very slow - Max Compression"]
image_quality_options = [
    "None", "2 - Best Quality", "5 - Very High Quality", "10 - High Quality",
    "15 - Medium Quality", "20 - Low Quality", "25 - Very Low Quality", "31 - Minimum Quality"
]

# Function to show tooltip on hover
def create_tooltip(widget, text):
    def on_enter(event):
        tooltip = Toplevel(app)
        tooltip.overrideredirect(True)
        tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        label = Label(tooltip, text=text, background="black", foreground="white", borderwidth=1, relief="solid")
        label.pack()
        widget.tooltip = tooltip
    def on_leave(event):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

# Function to extract file extension
def get_file_extension(file_path):
    _, ext = os.path.splitext(file_path)
    return ext[1:].upper()

# Function to allow user to select files and display detected formats in the UI
def select_files():
    global selected_files, current_format_type
    selected_files = filedialog.askopenfilenames()
    file_listbox.delete("1.0", 'end')
    
    if selected_files:
        first_file_extension = get_file_extension(selected_files[0])
        # Determine which formats are available based on the file type of the first selected file
        if first_file_extension in format_options["audio"]:
            current_format_type = "audio"
            available_formats = format_options["audio"]
            toggle_advanced_options("audio")
        elif first_file_extension in format_options["video"]:
            current_format_type = "video"
            available_formats = format_options["video"]
            toggle_advanced_options("video")
        elif first_file_extension in format_options["image"]:
            current_format_type = "image"
            available_formats = format_options["image"]
            toggle_advanced_options("image")
        else:
            messagebox.showerror("Unsupported File", "This file type is not supported for conversion.")
            return
        
        file_type_label.configure(text=f"Detected file type: {first_file_extension}")
        output_format_menu.configure(values=available_formats)
        output_format_menu.set(available_formats[0])
        
        # Display each selected file in the file list UI
        for file in selected_files:
            file_listbox.insert('end', os.path.basename(file) + "\n")

# Function to toggle advanced settings based on the file type
def toggle_advanced_options(file_type):
    if file_type == "audio":
        bitrate_label.pack(pady=5)
        bitrate_dropdown.pack(pady=5)
        codec_label.pack(pady=5)
        codec_dropdown.pack(pady=5)
        resolution_label.pack_forget()
        resolution_dropdown.pack_forget()
        quality_label.pack_forget()
        quality_dropdown.pack_forget()
        compression_label.pack_forget()
        compression_dropdown.pack_forget()
        image_quality_label.pack_forget()
        image_quality_dropdown.pack_forget()
        app.geometry("400x650")  # Resize for audio options
    elif file_type == "video":
        bitrate_label.pack_forget()
        bitrate_dropdown.pack_forget()
        codec_label.pack(pady=5)
        codec_dropdown.pack(pady=5)
        resolution_label.pack(pady=5)
        resolution_dropdown.pack(pady=5)
        quality_label.pack(pady=5)
        quality_dropdown.pack(pady=5)
        compression_label.pack(pady=5)
        compression_dropdown.pack(pady=5)
        image_quality_label.pack_forget()
        image_quality_dropdown.pack_forget()
        app.geometry("400x925")  # Resize for video options
    elif file_type == "image":
        bitrate_label.pack_forget()
        bitrate_dropdown.pack_forget()
        codec_label.pack_forget()
        codec_dropdown.pack_forget()
        resolution_label.pack_forget()
        resolution_dropdown.pack_forget()
        quality_label.pack_forget()
        quality_dropdown.pack_forget()
        compression_label.pack_forget()
        compression_dropdown.pack_forget()
        image_quality_label.pack(pady=5)
        image_quality_dropdown.pack(pady=5)
        app.geometry("400x600")  # Resize for image options

# Function to ensure unique filenames for converted files
def get_unique_filename(file_path):
    if not os.path.exists(file_path):
        return file_path
    base, ext = os.path.splitext(file_path)
    counter = 1
    new_file = f"{base}_{counter}{ext}"
    while os.path.exists(new_file):
        counter += 1
        new_file = f"{base}_{counter}{ext}"
    return new_file

# Core function to convert selected files with FFmpeg, using selected advanced settings
def convert_files():
    output_format = output_format_menu.get()
    total_files = len(selected_files)

    for index, file in enumerate(selected_files):
        output_file = get_unique_filename(file.rsplit('.', 1)[0] + f".{output_format.lower()}")

        try:
            ffmpeg_cmd = ffmpeg.input(file)
            output_params = {}

            # Apply settings based on file type
            if current_format_type == "audio":
                if bitrate_dropdown.get() != "None":
                    output_params['audio_bitrate'] = bitrate_dropdown.get().split()[0]
                if codec_dropdown.get() != "None":
                    output_params['acodec'] = codec_dropdown.get().split()[0]
            elif current_format_type == "video":
                if resolution_dropdown.get() != "None":
                    output_params['s'] = resolution_dropdown.get().split()[0]
                if codec_dropdown.get() != "None":
                    output_params['vcodec'] = codec_dropdown.get().split()[0]
                if quality_dropdown.get() != "None":
                    output_params['preset'] = quality_dropdown.get()
                if compression_dropdown.get() != "None":
                    output_params['compression_level'] = compression_dropdown.get().split()[0]
            elif current_format_type == "image":
                if output_format in ["JPG", "JPEG", "WEBP"] and image_quality_dropdown.get() != "None":
                    output_params['q:v'] = image_quality_dropdown.get().split()[0]
                elif output_format == "PNG" and compression_dropdown.get() != "None":
                    output_params['compression_level'] = compression_dropdown.get().split()[0]

            ffmpeg_cmd = ffmpeg_cmd.output(output_file, **output_params)
            ffmpeg_cmd.run(cmd="C:/ffmpeg/bin/ffmpeg.exe", overwrite_output=True)

            progress_label.configure(text=f"Converting: {os.path.basename(file)} ({index + 1}/{total_files})")
            progress_bar.set((index + 1) / total_files)
            app.update_idletasks()
        except Exception as e:
            messagebox.showerror("Conversion Error", f"Error with {file}: {str(e)}")
            return

    messagebox.showinfo("Conversion Complete", "All files have been successfully converted.")
    progress_label.configure(text="Conversion Complete")
    progress_bar.set(0)

# Function to start conversion in a new thread to prevent UI blocking
def start_conversion_thread():
    if not selected_files:
        messagebox.showerror("No Files Selected", "Please select files to convert.")
        return

    conversion_thread = threading.Thread(target=convert_files)
    conversion_thread.start()

# Toggle button for Advanced Settings
def toggle_advanced():
    if advanced_frame.winfo_ismapped():
        advanced_frame.pack_forget()
        app.geometry("400x500")
    else:
        advanced_frame.pack(fill="both", expand=True)
        app.geometry("400x925")

# User Interface Elements
select_button = ctk.CTkButton(app, text="Select Files", command=select_files)
select_button.pack(pady=10)

file_type_label = ctk.CTkLabel(app, text="Detected file type: None", fg_color="#4B0082", text_color="white")
file_type_label.pack(pady=10)

convert_to_label = ctk.CTkLabel(app, text="Convert to:", text_color="white")
convert_to_label.pack(pady=5)

output_format_menu = ctk.CTkOptionMenu(app, values=["Select a file first"], fg_color="#4B0082", text_color="white")
output_format_menu.pack(pady=5)

file_listbox = ctk.CTkTextbox(app, width=240, height=100)
file_listbox.pack(pady=10)
file_listbox.insert('end', "Selected files will appear here.\n")

convert_button = ctk.CTkButton(app, text="Convert", command=start_conversion_thread)
convert_button.pack(pady=10)

progress_bar = ctk.CTkProgressBar(app, width=200, fg_color="#4B0082")
progress_bar.set(0)
progress_bar.pack(pady=10)

progress_label = ctk.CTkLabel(app, text="Progress: 0%", text_color="white")
progress_label.pack(pady=5)

# Toggle button for Advanced Settings
advanced_toggle = ctk.CTkButton(app, text="Advanced Options", command=toggle_advanced)
advanced_toggle.pack(pady=10)

# Advanced Settings Frame (initially hidden)
advanced_frame = ctk.CTkFrame(app, fg_color="black")

# Each dropdown includes a brief explanation of its purpose
bitrate_label = ctk.CTkLabel(advanced_frame, text="Bitrate (Audio Quality)", text_color="white")
bitrate_dropdown = ctk.CTkOptionMenu(advanced_frame, values=bitrate_options)
bitrate_dropdown.set("None")

resolution_label = ctk.CTkLabel(advanced_frame, text="Resolution (Video Quality)", text_color="white")
resolution_dropdown = ctk.CTkOptionMenu(advanced_frame, values=resolution_options)
resolution_dropdown.set("None")

codec_label = ctk.CTkLabel(advanced_frame, text="Codec (Compression Format)", text_color="white")
codec_dropdown = ctk.CTkOptionMenu(advanced_frame, values=codec_options)
codec_dropdown.set("None")

quality_label = ctk.CTkLabel(advanced_frame, text="Quality Scale (Output Quality)", text_color="white")
quality_dropdown = ctk.CTkOptionMenu(advanced_frame, values=quality_scale_options)
quality_dropdown.set("None")

compression_label = ctk.CTkLabel(advanced_frame, text="Compression Level (Speed/Quality Trade-off)", text_color="white")
compression_dropdown = ctk.CTkOptionMenu(advanced_frame, values=compression_options)
compression_dropdown.set("None")

image_quality_label = ctk.CTkLabel(advanced_frame, text="Image Quality (JPEG/WebP)", text_color="white")
image_quality_dropdown = ctk.CTkOptionMenu(advanced_frame, values=image_quality_options)
image_quality_dropdown.set("None")

# Pack the advanced options into the frame but initially hidden
bitrate_label.pack(pady=5)
bitrate_dropdown.pack(pady=5)
resolution_label.pack(pady=5)
resolution_dropdown.pack(pady=5)
codec_label.pack(pady=5)
codec_dropdown.pack(pady=5)
quality_label.pack(pady=5)
quality_dropdown.pack(pady=5)
compression_label.pack(pady=5)
compression_dropdown.pack(pady=5)
image_quality_label.pack(pady=5)
image_quality_dropdown.pack(pady=5)
advanced_frame.pack_forget()  # Hide initially

# Attach tooltips with usage guidance for each option
create_tooltip(bitrate_label, "Bitrate: Set the audio quality; higher bitrates mean better quality but larger files.")
create_tooltip(resolution_label, "Resolution: Define output resolution; use lower settings for smaller file size.")
create_tooltip(codec_label, "Codec: Choose a format for encoding; H.264 is common for video, MP3/AAC for audio.")
create_tooltip(quality_label, "Quality Scale: Balance speed and output quality; high quality takes longer to process.")
create_tooltip(compression_label, "Compression Level: Adjust speed-quality balance; slower processing can improve quality.")
create_tooltip(image_quality_label, "Image Quality: Lower values improve quality for JPEG/WebP (2 = best, 31 = minimum).")

# Run the app
app.mainloop()
