# name=Yamaha KX Remote Buttons
# url=https://github.com/usr242/Yamaha-KX-Controller-FLS-MIDI-Scripts

# this set of controller modifications are intended for the "Remote" mode or
# MCU section of the KX Controller.  A different script is provided for the
# CC Knobs.

# The generic Mackie Control profile provides access to the transport.
# But some functionality is not the same as the labeling on the hardware.
# This script matches the intended button use as much as possible.

import midi
import patterns
import channels
import mixer
import device
import transport
import arrangement
import general
import launchMapPages
import playlist
import ui
import screen

kx_rmt_vstw = 0x3D  # toggle vst/editor window
kx_rmt_adIns = 0x3C  # Open Plugin Browser (add instrument)
kx_rmt_cubA = 0x36  # Browser open/close/focus (not working API broken)
kx_rmt_cubB = 0x37  # New Pattern w/ naming
kx_rmt_asn1 = 0x38  # Open Current Channel's Piano Roll Editor
kx_rmt_asn2 = 0x39  # Metronome Enable/Disable
kx_rmt_mute = 0x3A  # Mute (testing - not working)
kx_rmt_solo = 0x3B  # Solo (testing)
kx_rmt_inc = 0  # No reason to override increment function
kx_rmt_dec = 0  # No reason to override decrement function
kx_rmt_rew = 0x5B  # transport rewind
kx_rmt_ffwd = 0x5C  # transport fast forward
kx_rmt_loop = 0x56  # loop/song mode
kx_rmt_stop = 0x5D  # transport stop
kx_rmt_play = 0x5E  # transport play/pause
kx_rmt_rec = 0x5F  # transport record


def OnInit():
    device_name = device.getName()
    if "Yamaha KX" in device_name:
        if "Yamaha KX-2" in device_name:
            print("Device Match! Yamaha KX-2 found.")
            # Init
            print("  - Browser visible state is: ", ui.getVisible(4))
            print("  - Track Count is: ", playlist.trackCount())
            print("  - Track 1 is named: ", playlist.getTrackName(1))
        else:
            print("This MIDI script is intended for the Yamaha KX-2 Device!")
            print("A different script should be used for Yamaha KX-1.")
            print("Yamaha KX-1 uses either the FLS \"generic controller\"", end=' ')
            print("or the \"Yamaha KX Main CC Knobs\" script.")
    else:
        print("Expected Device Name: \"Yamaha KX-2\"")
        print("Device Name Polled from your controller: {device_name}.")
        print("This does not appear to be a Yamaha KX Controller.")


def OnDeInit():
    print("Script execution has ended.")


def OnMidiMsg(event):
    event.handled = False
    chNum = channels.selectedChannel()
    testToggle = False

    if event.midiId == midi.MIDI_NOTEON:
        if event.data1 > 0:

            # VST BUTTON
            if event.data1 == kx_rmt_vstw:
                channels.showCSForm(chNum)
                event.handled = True

            # ADD INSTRUMENT BUTTON
            if event.data1 == kx_rmt_adIns:
                transport.globalTransport(
                        midi.FPT_F8,
                        8,
                        int(event.data2 > 0) * 2,
                        event.pmeFlags
                )
                event.handled = True

            # CUBASE FUNCTION A BUTTON (Generic Menu)
            if event.data1 == kx_rmt_cubA:
                transport.globalTransport(
                        midi.FPT_Menu,
                        int(event.data2 > 0) * 2,
                        event.pmeFlags
                )
                event.handled = True

            # CUBASE FUNCTION B BUTTON (New Pattern w/ Naming)
            if event.data1 == kx_rmt_cubB:
                transport.globalTransport(
                        midi.FPT_F4,
                        int(event.data2 > 0) * 2,
                        event.pmeFlags
                )
                event.handled = True

            # ASSIGN 1 BUTTON (Piano Roll)
            if event.data1 == kx_rmt_asn1 and event.data2 == 0x7F:
                ui.openEventEditor(
                       channels.getRecEventId(chNum) +
                       midi.REC_Chan_PianoRoll, midi.EE_PR)
                event.handled = True
            if event.data1 == kx_rmt_asn1 and event.data2 == 0x00:
                event.handled = True

            # ASSIGN 2 BUTTON (Metronome)
            if event.data1 == kx_rmt_asn2:
                transport.globalTransport(
                        midi.FPT_Metronome,
                        int(event.data2 > 0) * 2,
                        event.pmeFlags
                )
                event.handled = True

            # TRACK MUTE BUTTON (Channel Mute/momentary)
            if event.data1 == kx_rmt_mute:
                channels.muteChannel(chNum)
                event.handled = True

            # TRACK SOLO BUTTON (Channel Solo/momentary)
            if event.data1 == kx_rmt_solo:
                channels.soloChannel(chNum)
                event.handled = True

            if event.data1 == kx_rmt_inc:
                pass # stubbed for modification if desired

            if event.data1 == kx_rmt_dec:
                pass # stubbed for modification if desired

            # TRANSPORT REWIND BUTTON
            if event.data1 == kx_rmt_rew:
                transport.globalTransport(
                        midi.FPT_Rewind + int(event.data1 == 0x5C),
                        int(event.data2 > 0) * 2,
                        event.pmeFlags
                )
                event.handled = True

            # TRANSPORT FAST FORWARD BUTTON
            if event.data1 == kx_rmt_ffwd:
                transport.globalTransport(
                        midi.FPT_FastForward + int(event.data1 == 0x5B),
                        int(event.data2 > 0) * 2,
                        event.pmeFlags
                )
                event.handled = True

            # TRANSPORT LOOP BUTTON
            if event.data1 == kx_rmt_loop:
                transport.globalTransport(
                        midi.FPT_Loop,
                        int(event.data2 > 0) * 2,
                        event.pmeFlags
                )
                event.handled = True

            # TRANSPORT STOP BUTTON
            if event.data1 == kx_rmt_stop:
                transport.globalTransport(
                        midi.FPT_Stop,
                        int(event.data2 > 0) * 2,
                        event.pmeFlags
                )
                event.handled = True

            # TRANSPORT PLAY BUTTON
            if event.data1 == kx_rmt_play and event.data2 == 0x7F:
                transport.globalTransport(
                        midi.FPT_Play,
                        int(event.data2 > 0) * 2,
                        event.pmeFlags
                )
                event.handled = True

            # TRANSPORT RECORD BUTTON
            if event.data1 == kx_rmt_rec:
                transport.globalTransport(
                        midi.FPT_Record,
                        int(event.data2 > 0) * 2,
                        event.pmeFlags
               )
                event.handled = True

# vim: tabstop=4:softtabstop=4:shiftwidth=4:expandtab
