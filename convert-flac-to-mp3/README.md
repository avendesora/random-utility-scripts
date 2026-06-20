# convert-flac-to-mp3

Small CLI utility for converting `.flac` audio files to `.mp3` using `ffmpeg` + `typer`.

It supports:

- Converting a single file
- Batch converting all `.flac` files in a directory
- Optional downmixing to stereo (default) or keeping 6 channels
- Custom MP3 bitrate (default `320k`)
- Colored status output for single-file conversions
- A progress bar for batch conversions

---

## Requirements

- [`uv`](https://docs.astral.sh/uv/)
- [`ffmpeg`](https://ffmpeg.org/) installed and available on your `PATH`
- Python compatible with `pyproject.toml` (`>=3.14` currently)

Check tools:

```bash
uv --version
ffmpeg -version
```

---

## Install

From `convert-flac-to-mp3/`:

```bash
uv sync
```

This creates/updates the project environment from `pyproject.toml` and `uv.lock`.

---

## Quickstart

From `convert-flac-to-mp3/`, run one of these:

### Single file (3 commands)

```bash
uv sync
uv run python main.py --help
uv run python main.py convert input.flac output.mp3
```

### Batch directory (3 commands)

```bash
uv sync
uv run python main.py --help
uv run python main.py batch ./flac_files ./mp3_files
```

---

## Usage

Run from inside `convert-flac-to-mp3/`:

```bash
uv run python main.py --help
```

### Convert a single file

```bash
uv run python main.py convert input.flac output.mp3
```

With custom bitrate:

```bash
uv run python main.py convert input.flac output.mp3 --bitrate 192k
```

Keep 6 channels (instead of downmixing to stereo):

```bash
uv run python main.py convert input.flac output.mp3 --stereo False
```

---

### Batch convert a directory

Converts all `*.flac` files in `input_dir` and writes `.mp3` files to `output_dir`:

```bash
uv run python main.py batch ./flac_files ./mp3_files
```

In batch mode, the script shows a progress bar and colorized status messages while each file is converted.

Custom bitrate:

```bash
uv run python main.py batch ./flac_files ./mp3_files --bitrate 256k
```

Keep 6 channels:

```bash
uv run python main.py batch ./flac_files ./mp3_files --stereo False
```

---

## CLI options

### `convert`

- `input_file` (required): path to input `.flac` file
- `output_file` (required): output `.mp3` path
- `--bitrate` (optional, default `320k`)
- `--stereo` (optional, default `True`)

### `batch`

- `input_dir` (required): directory containing `.flac` files
- `output_dir` (required): output directory for `.mp3` files
- `--bitrate` (optional, default `320k`)
- `--stereo` (optional, default `True`)

---

## What the script does internally

For each conversion, it runs `ffmpeg` roughly like this:

```bash
ffmpeg -i input.flac -vn -ab 320k -ar 44100 -y -ac 2 output.mp3
```

- `-vn`: no video
- `-ab`: audio bitrate
- `-ar 44100`: sample rate
- `-y`: overwrite output
- `-ac 2` (stereo) or `-ac 6` (6 channels)

---

## Notes

- In batch mode, only files matching `*.flac` (lowercase extension) are picked up.
- Output files are overwritten if they already exist.
- Some MP3 players may not handle 6-channel MP3 well; stereo is the safest default.
