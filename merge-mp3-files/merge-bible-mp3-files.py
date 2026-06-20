import subprocess
from pathlib import Path

import typer

import pythonbible as bible


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

    new_testament_books: dict[bible.Book, list[str]] = {}
    old_testament_books: dict[bible.Book, list[str]] = {}

    if not input_path.exists() or not input_path.is_dir():
        typer.echo(
            f"Input folder '{input_folder}' does not exist or is not a directory."
        )
        raise typer.Exit(code=1)

    all_mp3_files = input_path.glob("*.mp3")

    if not all_mp3_files:
        typer.echo("No MP3 files found in the specified folder.")
        raise typer.Exit(code=1)

    for mp3_file in all_mp3_files:
        book_id = mp3_file.name.split("_")[0]

        if book_id.startswith("A"):
            # Old Testament books
            book = bible.Book(int(book_id[1:]))
            book_files = old_testament_books.get(book, [])
            book_files.append(mp3_file.name)
            old_testament_books[book] = sorted(book_files)
        elif book_id.startswith("B"):
            # New Testament books
            book = bible.Book(int(book_id[1:]) + 39)
            book_files = new_testament_books.get(book, [])
            book_files.append(mp3_file.name)
            new_testament_books[book] = sorted(book_files)

    commands: list[str] = []

    for book, book_files in old_testament_books.items():
        merge_list = "|".join(
            (input_path / file_name).as_posix() for file_name in book_files
        )
        book_output_folder = output_path / "Old Testament"
        book_output_folder.mkdir(parents=True, exist_ok=True)
        book_output_file = book_output_folder / f"{book.value:02d}_{book.name}.mp3"
        merge_command = (
            f'ffmpeg -i "concat:{merge_list}" -acodec copy "{book_output_file}"'
        )
        commands.append(merge_command)

    for book, book_files in new_testament_books.items():
        merge_list = "|".join(
            (input_path / file_name).as_posix() for file_name in book_files
        )
        book_output_folder = output_path / "New Testament"
        book_output_folder.mkdir(parents=True, exist_ok=True)
        book_output_file = book_output_folder / f"{book.value - 39:02d}_{book.name}.mp3"
        merge_command = (
            f'ffmpeg -i "concat:{merge_list}" -acodec copy "{book_output_file}"'
        )
        commands.append(merge_command)

    for command in commands:
        print(f"Running command: {command}")
        subprocess.run(command, shell=True)
