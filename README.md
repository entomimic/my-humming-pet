# myHummingPet
A simple melody generator using math formulas and musical scales. Generates random MIDI snippets for inspiration.

## Features
- Choose from preset scales (e.g. Cmaj, Amin, Cpent...)
- Select a formula (sin, linear, fibonacci)
- Set length, BPM, entropy (randomness) and seed
- Output MIDI files with tempo

## Usage
Run from terminal:
~~~
python main.py
~~~
Follow the prompts to choose scale, formula, etc.
Your `.mid` file will be saved under the `output/` folder.

## Examples
Some favorite results are available in the `examples/` folder.
Open them with ant MIDI player or your DAW!

## Environment
Tested with:
- Python 3.12.6
- mido 1.3.3
- numpy 2.3.4
