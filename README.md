# LSC Clarity MIDI Control
Use a MIDI Control Surface, such as the Behringer BCF2000, to control LSC Clarity. This script is a simple protocol translater to take MIDI commands and turn them into OSC commands that Clarity can understand.

## Installation

You need Python 3.

Install the modules `rtmidi` and `pythonosc` (via PIP or otherwise).

Rename "`config-sample-bcf2000.json`" to "`config.json`" and edit as needed (insert your Cue List Names, and Clarity IP Address / OSC Port number).

Run `python3 clarity-midicontrol.py`
