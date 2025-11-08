import numpy as np
import random
from mido import Message, MidiFile, MidiTrack
from scales import SCALES
import time
import os

timestamp_int = int(time.time())
# usr input
print("Please enter a scale.\n We've got the following scales:\n", " / ".join(SCALES.keys()))
scale_input = input().strip()
if scale_input not in SCALES:
    print("Invalid scale! Default = Cmaj")
    scale_input = "Cmaj"
scale = SCALES[scale_input] if scale_input in SCALES else SCALES["Cmaj"]

print("Please select a formula: 1 = sin, 2 = linear, 3 = fibonacci.")
formula = int(input().strip())

length = int(input("Please enter the number of the notes (must be an integer).\n").strip())

entropy_input = input("Optional: Enter the entropy (must be an integer).\n "
                          "If left blank, a random entropy between 1 and 10 would be used.\n"
                          "The larger the entropy, the more chaotic the melody.\n").strip()
entropy = int(entropy_input) if entropy_input else random.randint(1, 11)

seed_input = input("Optional: Enter the seed.\n")
seed = int(seed_input) if seed_input else None
random.seed(seed)

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
user_pitches_noise = user_pitches + noise
user_pitches_noise_scale = snap_to_scale(user_pitches_noise, scale)
print("The original pitches: ", user_pitches, "\n")
print("The pitches with noise: ", user_pitches_noise, "\n")
print(f"The pitches in {scale}: ", user_pitches_noise_scale, "\n")


def write_midi(p_pitches: list, file_name="output.mid", tempo=480):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    for p in p_pitches:
        track.append(Message('note_on', note=int(p), velocity=80, time=0))
        track.append(Message('note_off', note=int(p), velocity=64, time=tempo))
    mid.save("output/" + file_name)
    print(f"Midi file saved to 'output/{file_name}'")
try:
    os.makedirs("output", exist_ok = True)
except OSError as e:
    print(f"Error creating output directory: {e}")

write_midi(user_pitches_noise_scale, f"pet_{timestamp_int}_{scale_input}f{formula}e{entropy}s{seed}l{length}.mid")