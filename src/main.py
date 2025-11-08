import numpy as np
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
from scales import SCALES
import time
import os

timestamp_int = int(time.time())

def safe_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError) as err:
        print(f"Invalid input '{value}': {err}. Defaulting to {default}. >:(")
        return default
# usr input
print("Please enter a scale.\n We've got the following scales:\n", " / ".join(SCALES.keys()))
scale_input = input().strip()
if scale_input not in SCALES:
    print("Invalid scale! Default = Cmaj")
    scale_input = "Cmaj"
scale = SCALES.get(scale_input, SCALES["Cmaj"])

bpm_input = input("Please enter the bpm. Default = 120\n").strip()
bpm = safe_int(bpm_input, 120)

print("Please select a formula: 1 = sin, 2 = linear, 3 = fibonacci. Default = 1")
formula = safe_int(input().strip(), 1)

print("Please enter the number of the notes (must be an integer). Default = 32")
length = safe_int(input().strip(), 32)

entropy_input = input("Optional: Enter the entropy (must be an integer).\n "
                          "If left blank, a random entropy between 1 and 10 would be used.\n"
                          "The larger the entropy, the more chaotic the melody.\n").strip()
entropy = safe_int(entropy_input, np.random.randint(1, 11)) if entropy_input else np.random.randint(1, 11)

seed_input = input("Optional: Enter the seed. Default = None\n")
seed = safe_int(seed_input, None) if seed_input else None
np.random.seed(seed)

tempo = mido.bpm2tempo(bpm)
#print(tempo)

def generate_pitches(p_formula: int, p_length: int) -> list:
    x = np.arange(p_length)
    if p_formula == 1:
        pitches = (np.sin(x / 2) * 6).astype(int) + 60        # around C4
    elif p_formula == 2:
        pitches = 60 + (x % 8)
    elif p_formula == 3:
        fib = [0, 1]
        for i in range(2, p_length):
            fib.append(fib[-1] + fib[-2])
        pitches = 60 + (np.array(fib) % 12)
    else:
        pitches = 60 + (x % 7)
    return pitches

def snap_to_scale(p_pitches: list, p_scale: list) -> list:
    snapped = []
    for p in p_pitches:
        pitch_mod = p % 12
        octave = p // 12
        # find the nearest
        nearest = min(p_scale, key=lambda s: abs(s - pitch_mod))
        snapped.append(int(octave * 12 + nearest))

    return snapped

user_pitches: list = generate_pitches(formula, length)
noise: list = np.random.randint(-entropy, entropy, size=len(user_pitches)).tolist()
user_pitches_noise = [p + n for p, n in zip(user_pitches, noise)]
user_pitches_noise_scale = snap_to_scale(user_pitches_noise, scale)
#print("The original pitches: ", user_pitches, "\n")
#print("The pitches with noise: ", user_pitches_noise, "\n")
print(f"The snapped pitches in {scale_input}: ", user_pitches_noise_scale, "\n")

print("Writing midi...\n")

def write_midi(p_pitches: list, file_name="output.mid", p_tempo=500000):
    mid = MidiFile(ticks_per_beat=480)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=p_tempo, time=0))
    for p in p_pitches:
        track.append(Message("note_on", note=int(p), velocity=80, time=0))
        track.append(Message("note_off", note=int(p), velocity=64, time=480))
    mid.save("output/" + file_name)
    print(f"Midi file saved to 'output/{file_name}'")

try:
    os.makedirs("output", exist_ok = True)
except OSError as e:
    print(f"Error creating output directory: {e}")

write_midi(user_pitches_noise_scale,
           f"pet_{timestamp_int}_{scale_input}b{bpm}f{formula}e{entropy}s{seed}l{length}.mid",
           tempo)

input("Press Enter to exit...")