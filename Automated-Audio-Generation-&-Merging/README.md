# Audio Generation Automation

This project automates the generation of personalized audio messages using text-to-speech (TTS) and FFmpeg. The script reads client information from an Excel file, generates personalized speech, and merges it with predefined audio files.

## Features
- Reads client names and addresses from an Excel file
- Generates personalized audio messages using **ElevenLabs API**
- Merges generated speech with pre-existing MP3 files (`main1.mp3` and `main2.mp3`)
- Outputs final audio files in the `Generated_Audio` directory
- Automatically removes temporary files after processing

## Prerequisites
Before running the script, make sure you have the following installed:
- Python 3.8+
- `ffmpeg` (Must be available in system PATH)
- Required Python libraries (install via pip):
  ```sh
  pip install pandas ffmpeg-python python-dotenv elevenlabs
  ```
- An **ElevenLabs API Key** (stored in `.env` file or manually set in the script)

## Setup
1. **Clone the repository**
   ```sh
   git clone <repo>
   cd project directory
   ```
2. **Add your ElevenLabs API key**:
   ```sh
   client = ElevenLabs(api_key="your_api_key_here")
   ```
3. **Prepare required files:**
   - Ensure `sample.xlsx` contains columns **Name** and **Address**.
   - Place `main1.mp3` and `main2.mp3` in the project directory.

## Usage
Run the script using:
```sh
python script.py
```

This will generate personalized audio files in the `Generated_Audio` folder.

## File Structure
```
📂 audio-automation
├── 📄 script.py               # Main script
├── 📄 sample.xlsx             # Input Excel file with client details
├── 🎵 main1.mp3               # Pre-recorded audio part 1
├── 🎵 main2.mp3               # Pre-recorded audio part 2
├── 📂 Generated_Audio         # Folder for final output files
├── 📄 .env                    # API key storage
└── 📄 README.md               # Project documentation
```

## Output Format
Each final MP3 file is named as:
```
Generated_Audio/{Client_Name}.mp3
```
Example output:
```
Generated_Audio/John_Doe.mp3
```

## Notes
- If a row in `sample.xlsx` is missing a Name or Address, it will be skipped.
- Temporary files are automatically removed after processing.
- Ensure `ffmpeg` is properly installed and accessible in your system PATH.

## License
This project is open-source and can be modified as needed.

## Author
Eshwar Adduri | [https://github.com/EshwarAdduri]