import os
import pandas as pd
import ffmpeg
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import save

# Load API key from environment variables (or replace with your API key directly)
load_dotenv()
client = ElevenLabs(="Your API KEY")

# Paths
MAIN1_AUDIO_PATH = "main1.mp3"  # First main audio file
MAIN2_AUDIO_PATH = "main2.mp3"  # Second main audio file
OUTPUT_FOLDER = "Generated_Audio"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# Function to generate and save audio
def create_audio(text, filename, voice_id="", model_id=""):
    if not text.strip():
        print(f"⚠️ Skipping empty text for {filename}")
        return None

    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128",
    )
    save(audio, filename)
    return filename


# Function to merge audio and save final output
def merge_audio(output_filename, *input_files):
    input_txt = "temp_input.txt"
    with open(input_txt, "w") as f:
        for file in input_files:
            f.write(f"file '{file}'\n")

    os.system(f"ffmpeg -f concat -safe 0 -i {input_txt} -c copy {output_filename} -y")
    os.remove(input_txt)

    # Cleanup temporary files (except MAIN1 and MAIN2)
    for file in input_files:
        if file not in [MAIN1_AUDIO_PATH, MAIN2_AUDIO_PATH]:
            os.remove(file)

    return output_filename


# Read Excel data
EXCEL_FILE = "sample.xlsx"
df = pd.read_excel(EXCEL_FILE)

# Process each contact
for index, row in df.iterrows():
    client_name = str(row.get("Name", "")).strip()
    client_address = str(row.get("Address", "")).strip()

    if not client_name or not client_address:
        print(f"⚠️ Skipping row {index}: Missing Name or Address")
        continue

    print(f"🎙️ Generating audio for {client_name}")

    # Step 1: Generate "Hi [Name]" audio
    hi_name_audio = create_audio(f"Hi {client_name}", f"temp_hi_name_{index}.mp3")

    # Step 2: Use main1.mp3 (already available)

    # Step 3: Generate address audio
    address_audio = create_audio(client_address, f"temp_address_{index}.mp3")

    # Step 4: Use main2.mp3 (already available)

    # Step 5: Merge in order: Hi Name → Main1 → Address → Main2
    final_audio = os.path.join(OUTPUT_FOLDER, f"{client_name.replace(' ', '_')}.mp3")
    merge_audio(
        final_audio, hi_name_audio, MAIN1_AUDIO_PATH, address_audio, MAIN2_AUDIO_PATH
    )

    print(f"✅ Final audio saved: {final_audio}")

print("🚀 Automation completed successfully!")
