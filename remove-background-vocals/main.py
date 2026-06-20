import subprocess
from pathlib import Path

import typer


app = typer.Typer()


channel_map = {
    "left": "FL",
    "right": "FR",
}


@app.command()
def remove_background_vocals(
    input_folder: str = typer.Argument(
        ..., help="Path to the input stereo audio file."
    ),
    output_folder: str = typer.Argument(
        ..., help="Path to save the output mono audio file."
    ),
    file_type: str = typer.Option("mp3", help="Type of the audio file (default: mp3)."),
    channel_without_vocals: str = typer.Option(
        "left", help="Channel without vocals (default: left)."
    ),
):
    """Remove background vocals from a stereo audio file.

    :param input_folder: string path to the stereo audio file.
    :param output_folder: string path to save the mono audio file.
    :param file_type: Type of the audio file (default: mp3).
    :param channel_without_vocals: Channel with vocals (default: left).
    """

    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    channel = channel_map.get(channel_without_vocals.lower(), "FL")

    for file in input_path.glob(f"*.{file_type}"):
        input_file = input_path / file.name
        output_file = output_path / file.name

        print(f"Removing background vocals from {input_file}...")
        convert_command = f'ffmpeg -i "{input_file}" -c:v copy -af "pan=stereo|FL={channel}|FR={channel}" "{output_file}"'
        subprocess.run(convert_command, shell=True)


if __name__ == "__main__":
    app()
