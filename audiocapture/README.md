# AudioCapture: Record and Mix Microphone & System Audio

This project allows you to **simultaneously record your microphone and system audio** (what you hear) on Linux, then automatically mix them into a single audio file.

---

## Features

- Records microphone and system audio at the same time
- Mixes both recordings into one WAV file
- Fully automated with a single script

---

## Requirements

- **Operating System:** Linux (tested on Ubuntu/Debian)
- **Python:** 3.7 or newer

---

## Dependencies

### System Packages

Install these with `apt`:

```bash
sudo apt-get update
sudo apt-get install python3 python3-venv python3-pip \
    libportaudio2 portaudio19-dev pulseaudio-utils sox libsox-fmt-all ffmpeg
```

### Python Packages

Create and activate a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

Install Python dependencies:

```bash
pip install sounddevice numpy pydub
```

---

## Setup

### 1. Find Your Monitor Source

To record system audio, you need your PulseAudio monitor source name:

```bash
pactl list short sources
```

Look for a line ending with `.monitor` (e.g., `alsa_output.pci-0000_00_1b.0.analog-stereo.monitor`).

Edit `record_and_mix.py` and set the `monitor_source` variable to your monitor source.

---

## Usage

Run the script:

```bash
python record_and_mix.py
```

- The script will record both microphone and system audio for the specified duration (default: 120 seconds).
- After recording, it will mix both tracks and save the result as `mixed_output.wav`.

---

## Output Files

- `mic_output.wav` — Microphone recording
- `system_output.wav` — System audio recording
- `mixed_output.wav` — Mixed audio (mic + system)

---

## Troubleshooting

- **No module named 'pydub'**  
  Install with: `pip install pydub`
- **OSError: PortAudio library not found**  
  Install with: `sudo apt-get install libportaudio2 portaudio19-dev`
- **FileNotFoundError: 'sox'**  
  Install with: `sudo apt-get install sox libsox-fmt-all`
- **Stream error: No such entity**  
  Check your `monitor_source` value with `pactl list short sources`
- **No system audio recorded**  
  Ensure you are using the correct monitor source and that your output device supports monitoring.

---

## License

MIT License