import threading
import subprocess
import sounddevice as sd
import numpy as np
import wave
from pydub import AudioSegment

# --- Configuration ---
duration = 120  # seconds
fs = 44100
mic_output = "mic_output.wav"
system_output = "system_output.wav"
mixed_output = "mixed_output.wav"
monitor_source = "alsa_output.pci-0000_10_00.6.analog-stereo.monitor"  # Update as needed

# --- Microphone Recording Function ---
def record_mic():
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    with wave.open(mic_output, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())

# --- System Audio Recording Function ---
def record_system():
    parec_cmd = [
        "parec",
        "--format=s16le",
        "--rate=44100",
        "--channels=1",
        "-d", monitor_source
    ]
    sox_cmd = [
        "sox",
        "-t", "raw",
        "-r", "44100",
        "-e", "signed",
        "-b", "16",
        "-c", "1",
        "-",
        system_output,
        "trim", "0", str(duration)
    ]
    parec = subprocess.Popen(parec_cmd, stdout=subprocess.PIPE)
    subprocess.run(sox_cmd, stdin=parec.stdout)
    parec.stdout.close()
    parec.wait()

# --- Start Both Recordings ---
mic_thread = threading.Thread(target=record_mic)
system_thread = threading.Thread(target=record_system)

print("Recording mic and system audio...")
mic_thread.start()
system_thread.start()
mic_thread.join()
system_thread.join()
print("Recording finished.")

# --- Mix the Audio ---
mic = AudioSegment.from_wav(mic_output)
system = AudioSegment.from_wav(system_output)
combined = mic.overlay(system)
combined.export(mixed_output, format="wav")
print(f"Mixed audio saved as {mixed_output}")