import subprocess
from pathlib import Path

import typer


app = typer.Typer()


@app.command()
def merge_mp3_files(
    input_folder: str = typer.Argument(
        ..., help="Path to the input folder containing MP3 files."
    ),
    output_folder: str = typer.Argument(..., help="Path to save the merged MP3 files."),
) -> None:
    """Merge the Bible mp3 files into one mp3 file per book.

    :param input_folder: string path to the folder containing MP3 files.
    :param output_folder: string path to save the merged MP3 file.
    """

    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    all_mp3_files = input_path.glob("*.mp3")

    if not all_mp3_files:
        typer.echo("No MP3 files found in the specified folder.")
        raise typer.Exit(code=1)

    for mp3_file in all_mp3_files:
        output_file = output_path / mp3_file.name
        command = f'ffmpeg -i "{mp3_file}" -filter:a "atempo=3.0" "{output_file}"'
        subprocess.run(command, shell=True)
