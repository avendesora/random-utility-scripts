import subprocess
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)

app = typer.Typer(help="Convert FLAC 5.1 audio files to MP3 using ffmpeg.")
console = Console()


def run_ffmpeg(
    input_file: Path, output_file: Path, bitrate: str = "320k", downmix: bool = True
):
    """
    Run ffmpeg to convert FLAC 5.1 to MP3.

    Args:
        input_file (Path): Input .flac file
        output_file (Path): Output .mp3 file
        bitrate (str): MP3 bitrate (default 320k)
        downmix (bool): If True, downmix 5.1 to stereo
    """
    cmd = [
        "ffmpeg",
        "-i",
        str(input_file),
        "-vn",  # no video
        "-ab",
        bitrate,
        "-ar",
        "44100",  # sample rate
        "-y",  # overwrite output
    ]

    if downmix:
        # Downmix to stereo
        cmd.extend(["-ac", "2"])
    else:
        # Keep all 6 channels (mp3 supports up to 5.1, but not all players handle it)
        cmd.extend(["-ac", "6"])

    cmd.append(str(output_file))
    output_file.parent.mkdir(parents=True, exist_ok=True)

    console.print(f"[cyan]Running:[/cyan] {' '.join(cmd)}")

    try:
        completed = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        console.print("[bold red]ffmpeg was not found on your PATH.[/bold red]")
        raise typer.Exit(code=1) from None
    except subprocess.CalledProcessError as exc:
        console.print(
            f"[bold red]ffmpeg failed while converting {input_file}.[/bold red]"
        )
        if exc.stderr:
            console.print(f"[red]{exc.stderr.strip()}[/red]")
        raise typer.Exit(code=1) from exc

    if completed.stdout.strip():
        console.print(completed.stdout.strip())


@app.command()
def convert(
    input_file: Path = typer.Argument(
        ..., exists=True, dir_okay=False, help="Input FLAC file."
    ),
    output_file: Path = typer.Argument(..., help="Output MP3 file."),
    bitrate: str = typer.Option("320k", help="MP3 bitrate."),
    stereo: bool = typer.Option(True, help="Downmix to stereo (default: True)."),
):
    """
    Convert a single FLAC 5.1 file to MP3.
    """
    console.print(
        f"[bold magenta]Converting[/bold magenta] {input_file.name} -> {output_file.name}"
    )
    run_ffmpeg(input_file, output_file, bitrate, downmix=stereo)
    console.print(f"[bold green]Done:[/bold green] {output_file}")


@app.command()
def batch(
    input_dir: Path = typer.Argument(
        ..., exists=True, file_okay=False, help="Directory of FLAC files."
    ),
    output_dir: Path = typer.Argument(..., help="Directory to save MP3 files."),
    bitrate: str = typer.Option("320k", help="MP3 bitrate."),
    stereo: bool = typer.Option(True, help="Downmix to stereo (default: True)."),
):
    """
    Convert all FLAC files in a directory to MP3.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    flac_files = sorted(input_dir.glob("*.flac"))
    if not flac_files:
        console.print(f"[bold yellow]No .flac files found in[/bold yellow] {input_dir}")
        return

    console.print(
        f"[bold magenta]Found {len(flac_files)} file(s) to convert.[/bold magenta]"
    )

    progress = Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("{task.description}"),
        BarColumn(bar_width=None, style="cyan", complete_style="green"),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=False,
    )

    with progress:
        task = progress.add_task("Preparing conversions...", total=len(flac_files))

        for flac_file in flac_files:
            mp3_file = output_dir / f"{flac_file.stem}.mp3"
            progress.update(task, description=f"Converting {flac_file.name}")
            run_ffmpeg(flac_file, mp3_file, bitrate, downmix=stereo)
            progress.advance(task)

    console.print(
        f"[bold green]Finished converting[/bold green] {len(flac_files)} file(s) to {output_dir}"
    )


if __name__ == "__main__":
    app()
