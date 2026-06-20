import subprocess
from pathlib import Path

import typer


app = typer.Typer()


@app.command()
def merge_mp3_files(
    input_folder: str = typer.Argument(
        ..., help="Path to the input folder containing MP3 files."
    ),
    output_file: str = typer.Argument(..., help="Path to save the merged MP3 file."),
) -> None:
    """Merge multiple MP3 files into a single MP3 file.

    :param input_folder: string path to the folder containing MP3 files.
    :param output_file: string path to save the merged MP3 file.
    """

    input_path = Path(input_folder)
    output_path = Path(output_file)

    if not input_path.exists() or not input_path.is_dir():
        typer.echo(
            f"Input folder '{input_folder}' does not exist or is not a directory."
        )
        raise typer.Exit(code=1)

    mp3_files = sorted(input_path.glob("*.mp3"))

    if not mp3_files:
        typer.echo("No MP3 files found in the specified folder.")
        raise typer.Exit(code=1)

    print(f"Merging {len(mp3_files)} MP3 files into {output_path}...")

    # Run ffmpeg command to merge the files
    merge_command = f'ffmpeg -i "concat:{"|".join(str(mp3_file) for mp3_file in mp3_files)}" -acodec copy "{output_path}"'
    subprocess.run(merge_command, shell=True)
