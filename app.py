import random
from utils import propagator, util
from note_seq.protobuf import music_pb2
from note_seq import note_seq
import soundfile as sf

model, train_x, reversed_map, map = propagator.prepare()


def melody_sequence_transform(melody):
    instrument = music_pb2.NoteSequence()
    start_time = 0
    end_time = 0
    print("encoded melody=",melody,end="\n")
    for i in range(0, len(melody)-1, 2):
        if melody[i] =='R':
            continue
        pitch = int(melody[i])
        duration = (len(melody[i+1])+1)*4.0*(0.0625)
        end_time = start_time+duration

        instrument.notes.add(pitch=pitch, start_time=start_time,
                             end_time=end_time, velocity=80)
        start_time += duration

    instrument.total_time = start_time
    instrument.tempos.add(qpm=60)
    return instrument


def generate_melody(r):
    # randomSeedIndex = random.randint(0, 100000)
    melody_sequence = util.generate_melody_sequence(
        seed=train_x[r], stop=map['/'], model=model)
    print("melody sequence=",melody_sequence,"\n")
    encoded_melody = util.demapping(melody_sequence, reversed_map)
    
    instrument = melody_sequence_transform(encoded_melody)
    pm_seq = note_seq.note_sequence_to_pretty_midi(instrument)
    sf.write("./outs/fist_melody_very_fast.wav",
             data=pm_seq.fluidsynth(), samplerate=88200)


r = random.randint(0, 100000)
print("Random number between 5 and 15 is % s" % (r))
import ctypes.util
orig_ctypes_util_find_library = ctypes.util.find_library
def proxy_find_library(lib):
  if lib == 'fluidsynth':
    return 'libfluidsynth.so.1'
  else:
    return orig_ctypes_util_find_library(lib)
ctypes.util.find_library = proxy_find_library

generate_melody(r)
