""" A MIDI Controller interface for the fantastic LSC Clarity Lighting Control Software. """

__product__     = "LSC Clarity MIDI Control"
__author__      = "Anthony Eden"
__copyright__   = "Copyright 2018, Anthony Eden / Media Realm"
__credits__     = ["Anthony Eden"]
__license__     = "GPL v3"
__version__     = "1.0.0"


import os
import json
import rtmidi
from pythonosc import udp_client


def print_message_unmapped(midi):
    if midi.isNoteOn():
        print('ON: ', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
    elif midi.isNoteOff():
        print('OFF:', midi.getMidiNoteName(midi.getNoteNumber()))
    elif midi.isController():
        print('CONTROLLER', midi.getControllerNumber(), midi.getControllerValue())


if __name__ == "__main__":
    midiin = rtmidi.RtMidiIn()
    midi_ports = range(midiin.getPortCount())
    midi_port = None

    if not midi_ports:
        print('NO MIDI INPUT PORTS!')
        exit()

    # Load the config file
    Config_JSON = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")).read()
    CONFIG = json.loads(Config_JSON)

    # Connect to LSC Clarity Incoming OSC Port
    osc_client = udp_client.SimpleUDPClient(CONFIG['osc_clarity_ip'], CONFIG['osc_clarity_port'])

    print("AVAILABLE MIDI PORTS:")

    # List all midi ports and connect to the specified one
    for i in midi_ports:
        port_name = midiin.getPortName(i)

        if CONFIG['midi_port'] == port_name and midi_port is None:
            print("MIDI Port #" + str(i) + "-" + port_name + " - OPENING!")
            midi_port = i
            midiin.openPort(midi_port)

        else:
            print("MIDI Port #" + str(i) + "-" + port_name)
    
    print()

    if midi_port is None:
        print("Specified port" + CONFIG['midi_port'] + "not found")
        exit()

    while True:
        m = midiin.getMessage(250)

        if m:
            command = None
            value = None

            for fader in CONFIG['control_map']:
                if fader['midi_controller'] == m.getControllerNumber() and fader['type'] == "fader":
                    # Set cue fader level
                    command = '/cuelist/setfader'
                    value = round(m.getControllerValue() / 127, 3)
                    value = [fader['cuename'], str(value)]

                elif fader['midi_controller'] == m.getControllerNumber() and fader['type'] == "go" and m.getControllerValue() == 127:
                    # Go on a cuelist
                    command = '/cuelist/go'
                    value = fader['cuename']
                    

                elif fader['midi_controller'] == m.getControllerNumber() and fader['type'] == "release" and m.getControllerValue() == 127:
                    # Release a cuelist
                    command = '/cuelist/release'
                    value = fader['cuename']

                elif fader['type'] == "grandmaster":
                    # Grand master fader
                    command = '/setgrandmaster'
                    value = round(m.getControllerValue() / 127, 3)

            if command is not None and value is not None:
                osc_client.send_message(command, value)
            else:
                print_message_unmapped(m)
