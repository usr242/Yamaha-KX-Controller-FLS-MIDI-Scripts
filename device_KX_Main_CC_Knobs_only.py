# name=Yamaha KX Main CC Knobs
# url=https://github.com/usr242/Yamaha-KX-Controller-FLS-MIDI-Scripts

# this set of controller modifications are intended for the "Main" mode or
# Keyboard section of the KX Controller.


import midi
import channels

# using the four CC knobs - generic template from KX Template library
# First bank of four knobs:
#    channel volume, channel pan, channel cutoff, channel resonance
# Second bank of four knobs:
#    Assignable 1, 2, 3, 4
# each knob will be assigned the variable name CCK[#] with a comment label below

cck1 = 74  # CC Knob 1 - Channel Cutoff (not implemented in API?)
cck2 = 71  # CC Knob 2 - Channel Resonance (not implemented in API?)
cck3 = 10  # CC Knob 3 - Channel Pan
cck4 = 7   # CC Knob 4 - Channel Volume
cck5 = 73  # CC Knob 5
cck6 = 72  # CC Knob 6
cck7 = 91  # CC Knob 7
cck8 = 93  # CC Knob 8

def OnMidiMsg(event):
    event.handled = False
    if event.midiId == midi.MIDI_CONTROLCHANGE:
        if event.data1 > 0:
            if event.data1 == cck1:
                # stub for cck1 change
                pass
            if event.data1 == cck2:
                # stub for cck2 change
                pass
            if event.data1 == cck3:
                chNum = channels.channelNumber()
                panConv = (event.data2 - 64) / 64
                channels.setChannelPan(chNum, panConv)
                event.handled = True
            if event.data1 == cck4:
                chNum = channels.channelNumber()
                channels.setChannelVolume(chNum, event.data2 * (1 / 127))
                event.handled = True
            if event.data1 == cck5:
                # stub for cck5 change
                pass
            if event.data1 == cck6:
                # stub for cck6 change
                pass
            if event.data1 == cck7:
                # stub for cck7 change
                pass
            elif event.data1 == cck8:
                # stub for cck8 change
                pass


# vim: tabstop=4:softtabstop=4:shiftwidth=4:expandtab
