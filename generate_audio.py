import numpy as np
import random
import string
from scipy.io.wavfile import write
import os

# Sample audio files storage
TEST_DIR = "audio_files"
os.makedirs(TEST_DIR, exist_ok=True)

# Possible genres, artifact types and categories
GENRES = ["pianomusic", "rapmusic", "rockmusic", "jazzmusic", "classicalmusic", "popmusic"]
ARTIFACTS = ["gap", "clean", "glitch", "noise", "static"]
DURATION_CATEGORIES = {
    "short": (10, 29),
    "medium": (30, 180),
    "long": (181, 240)
}

# Generate a dummy WAV file and random file names

def generate_wav(filename, duration_sec, sr=22050):
    t = np.linspace(0, duration_sec, int(sr * duration_sec), False)  # Time axis
    signal = 0.5 * np.sin(2 * np.pi * 440 * t)  # Generate sine wave (440Hz)
    write(os.path.join(TEST_DIR, filename), sr, (signal * 32767).astype(np.int16))

def generate_random_filename(file_id):
    genre = random.choice(GENRES)
    artifact = random.choice(ARTIFACTS)
    duration_category = random.choice(list(DURATION_CATEGORIES.keys()))
    duration = random.randint(*DURATION_CATEGORIES[duration_category])
    filename = f"test_wav_{file_id}_{genre}_{artifact}.wav"
    return filename, duration

NUM_FILES = 20
file_data = [generate_random_filename(i) for i in range(1, NUM_FILES + 1)]


for file, duration in file_data:
    generate_wav(file, duration)

print(f"Randomly generated {NUM_FILES} .wav files in '{TEST_DIR}' directory.")
