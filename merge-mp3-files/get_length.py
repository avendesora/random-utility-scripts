import os
import subprocess


def get_mp3_duration(file_path):
    """Get duration of an MP3 file in seconds using ffprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                file_path,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0


def get_total_duration_in_folder(folder_path):
    total_duration = 0.0
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".mp3"):
                file_path = os.path.join(root, file)
                duration = get_mp3_duration(file_path)
                total_duration += duration
                print(f"{file}: {duration:.2f} seconds")
    return total_duration


if __name__ == "__main__":
    folder = input("Enter the path to the folder: ").strip()
    total = get_total_duration_in_folder(folder)
    print(f"\nTotal duration: {total:.2f} seconds ({total / 60 / 60:.2f} hours)")
