# Audio Analyzer

## Description
Audio Analyzer is a cross-platform desktop application developed in Python with PyQt6. 

It allows analyzing audio files, providing information about their duration, dBFS, and LUFS.  

Coded with love by [Celerolab.Com](https://celerolab.com)

## Features
- Modern and accessible graphical interface.
- Detailed analysis of audio files (.mp3, .wav, .ogg, .flac).
- Calculation of LUFS (Loudness Units Full Scale).
- Support for changing the FFmpeg path.

## Requirements
- Windows, macOS, or Linux
- FFmpeg (included in the packaged version or manually configurable)
- Required dependencies (already included in the executable):
  - PyQt6
  - pydub
  - pyloudnorm
  - numpy

## Installation
If the executable is provided in a compressed format (.dmg, .zip or .tar.gz), extract the file to a folder of your choice.

### Windows and macOS
- Run the app directly.

### Linux
1. Open a terminal in the folder where you extracted the files.
2. Grant execution permissions if necessary:
   ```bash
   chmod +x AudioAnalyzer
   ```
3. Run the application:
   ```bash
   ./AudioAnalyzer
   ```

## Usage
1. Open the application.
2. Click **Load Audio File** and select an audio file.
3. The file information will be displayed on the screen.
4. If FFmpeg is not properly configured, select a new path from **Change FFmpeg Path**.

## Legal Notice Regarding FFmpeg
This application may include a bundled version of FFmpeg for convenience. FFmpeg is an open-source multimedia framework licensed under the **GNU Lesser General Public License (LGPL) version 2.1** or later, as well as the **GNU General Public License (GPL) version 2** or later for certain components.

Users are free to replace the FFmpeg executable with their own version, as the application provides an option to manually set the FFmpeg path. For more details about FFmpeg’s licensing and source code, visit the official FFmpeg website:

[https://ffmpeg.org/legal.html](https://ffmpeg.org/legal.html)

## Additional Notes
- If FFmpeg is not available in the default path, the application may not load certain audio formats.
