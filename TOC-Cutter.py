import os
import re
from pydub import AudioSegment

SUPPORTED_FORMATS = [".wav", ".flac", ".mp3", ".aac"]

def cue_to_ms(time_str):
    mm, ss, ff = map(int, time_str.split(":"))
    return (mm * 60 + ss) * 1000 + int(ff * (1000 / 75))

def parse_cue(cue_path):
    tracks = []
    with open(cue_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    current_track = None

    for line in lines:
        line = line.strip()

        if line.startswith("TRACK"):
            current_track = {"title": f"Track_{len(tracks)+1}"}

        elif line.startswith("TITLE") and current_track:
            title = re.findall(r'"(.*?)"', line)
            if title:
                current_track["title"] = title[0]

        elif "INDEX 01" in line and current_track:
            time = line.split()[-1]
            current_track["start"] = cue_to_ms(time)
            tracks.append(current_track)

    return tracks

def find_matching_audio(cue_path):
    base_name = os.path.splitext(os.path.basename(cue_path))[0]
    folder = os.path.dirname(cue_path)

    for file in os.listdir(folder):
        name, ext = os.path.splitext(file)
        if name == base_name and ext.lower() in SUPPORTED_FORMATS:
            return os.path.join(folder, file)

    return None

def split_audio(audio_path, cue_path):
    print(f"Loading audio: {audio_path}")
    audio = AudioSegment.from_file(audio_path)

    tracks = parse_cue(cue_path)

    if not tracks:
        print("No tracks found in the .cue file")
        return

    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    ext = os.path.splitext(audio_path)[1].replace(".", "").lower()

    output_folder = os.path.join(os.path.dirname(audio_path), base_name + "_split")
    os.makedirs(output_folder, exist_ok=True)

    print(f"Exporting to: {output_folder}")

    for i in range(len(tracks)):
        start = tracks[i]["start"]
        end = tracks[i+1]["start"] if i+1 < len(tracks) else len(audio)

        segment = audio[start:end]

        safe_title = re.sub(r'[\\/*?:"<>|]', "", tracks[i]["title"])
        filename = f"{i+1:02d} - {safe_title}.{ext}"
        output_path = os.path.join(output_folder, filename)

        segment.export(output_path, format=ext)
        print(f"✔ Exported: {filename}")

    print("✅ Process completed")

def main():
    print("=== TOC-Cutter ===")

    cue_path = input("Drag and drop the .cue file here and press Enter:\n").strip('"')

    if not os.path.exists(cue_path) or not cue_path.lower().endswith(".cue"):
        print("❌ Invalid .cue file")
        return

    audio_path = find_matching_audio(cue_path)

    if not audio_path:
        print("❌ No matching audio file found")
        print("Make sure the .cue and audio file have the same name")
        return

    print(f"✔ Audio found: {os.path.basename(audio_path)}")

    split_audio(audio_path, cue_path)

if __name__ == "__main__":
    main()
