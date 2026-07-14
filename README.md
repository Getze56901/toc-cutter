# toc-cutter
a Python tool designed to split a full CD audio file into individual tracks using data from a .cue file.

# TOC-Cutter

TOC-Cutter is a Python tool designed to split a full CD audio file into individual tracks using data from a `.cue` file. It is especially useful for CD rips where all songs are contained in a single file, allowing automatic separation into properly named tracks.

---

## Overview

This program uses a `.cue` file as a reference, which contains the exact start times of each track (TOC - Table of Contents), and applies that information to cut the corresponding audio file into multiple individual tracks.

The workflow is straightforward:

1. Load the `.cue` file
2. Extract track start times (`INDEX 01`)
3. Locate the matching audio file
4. Split the audio based on timestamps
5. Export each track as a separate file

---

## How it works

TOC-Cutter parses the `.cue` file line by line to extract:

* Track titles
* Start times in mm:ss:ff format

These timestamps are converted into milliseconds to allow precise slicing of the audio file.

Then:

* The full audio file is loaded into memory
* It is split into segments using the extracted timestamps
* Each segment is exported as an individual file

The final result is a folder containing all tracks, properly ordered and named.

---

## Why use TOC-Cutter?

* Automates a normally tedious manual process
* Uses accurate timing directly from the original `.cue`
* Prevents cutting errors between tracks
* Ideal for archivists, collectors, and physical media enthusiasts

---

## Requirements

For proper functionality:

* The `.cue` file and the audio file must have the same name
* Both files must be located in the same directory

Example:

```
album.cue
album.flac
```

---

## Supported formats

TOC-Cutter supports the following audio formats:

* `.wav`
* `.flac`
* `.mp3`
* `.aac`

The output format will match the original audio file.

---

## Dependencies

* Python 3.x
* pydub
* ffmpeg (required for audio processing)

---

## Building

N/A

---

## Basic usage

1. Run the script
2. Drag and drop the `.cue` file into the terminal
3. The program will automatically detect the matching audio file
4. A new folder with the split tracks will be generated

---

## Output

The program creates a folder named after the original file with a `_split` suffix, containing all tracks:

```
album_split/
├── 01 - Track Name.mp3
├── 02 - Track Name.mp3
├── ...
```

---

## Notes

* `INDEX 00` (pregaps) are ignored
* File names are sanitized to avoid system errors
* Works best with accurate rips matching the `.cue` file

---

## Future improvements

* Graphical user interface (GUI)
* Multi-file `.cue` support
* Configurable export format (force MP3/FLAC)
* Automatic playlist generation (`.m3u`)

---
