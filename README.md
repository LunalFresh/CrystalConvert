# File Converter

A CustomTkinter-based file converter that leverages FFmpeg for converting audio, video, and image files. This application offers advanced options for controlling quality, compression, resolution, and more, providing flexible conversion options for a variety of formats.

# Features

-Supports multiple file formats:
Audio: MP3, WAV, AAC, OGG, FLAC, M4A, WMA, and more.
Video: MP4, MKV, AVI, MOV, WMV, FLV, and more.
Image: JPEG, PNG, BMP, TIFF, WEBP, and others.

- User-friendly interface with customizable themes.

- Advanced settings to adjust bitrate, resolution, codec, quality scale, and compression level.

# Getting Started: Prerequisites

- FFmpeg must be installed on your system. 
- The application uses C:/ffmpeg/bin/ffmpeg.exe as the executable path. 
  - (Ensure FFmpeg is installed at this path, or modify the code to specify the correct location.)
- Python 3.7+ should be installed on your system.

# Installation

- Download the Source Code
- Download the source ZIP from the repository or provided link.
- Extract the contents to a folder on your system.

1 - Install Dependencies

2 - Open a terminal in the extracted folder and run the following command to install required libraries:

- pip install customtkinter ffmpeg-python

3 - Run the Application
  - Run the app by executing:

- python File_Converter.py

# Usage

- Launch the App: Start the application, which opens a UI with options to select files, adjust formats, and configure       advanced settings.
- Select Files: Click "Select Files" to choose the files for conversion.
- Select Output Format: After selecting files, the app detects the file type and shows available formats for conversion     in the dropdown menu.
- Advanced Options:
- Audio: Set bitrate, codec, and quality options.
- Video: Adjust resolution, codec, quality scale, and compression level.
- Image: Modify image quality or compression settings.
- Click "Advanced Options" to toggle these settings on or off.
- Convert Files: Press "Convert" to begin file conversion. The progress bar updates during the conversion, displaying the   status for each file.


# Troubleshooting

- FFmpeg Path Issue: If FFmpeg is not located at C:/ffmpeg/bin/ffmpeg.exe, modify the convert_files() function with your FFmpeg path.

- Unsupported File Type: If an unsupported file type is selected, an error will display. Ensure that selected files are compatible with FFmpeg.

- Conversion Error: In case of an error during conversion, a dialog box will display the issue. Common errors are often due to incompatible settings or FFmpeg path misconfiguration.

- Advanced Options Not Visible: Advanced options are based on the detected file type (audio, video, or image). Ensure you have selected compatible files to reveal these options.

# License
Licensed under the Apache 2.0 License. See LICENSE for more information.
