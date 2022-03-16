import json
import numpy as np

def dataset_read(data_path,file_name="dataset"):
    with open(data_path+file_name,"r") as file_path:
        dataset=file_path.read()
    return dataset

def dataset_spliter(dataset):
    note_set = set()
    splited_data = dataset.split("/")
    songs = []
    for song in splited_data:
        splited_notes = song.split(",")
        song_notes = []
        for note in splited_notes:
            index = len(note)
            for i in range(len(note)):
                if (note[i] == 'X'):
                    index = i
                    break
            song_notes.append(note[:index])
            note_set.add(note[:index])
            if (len(note)-index) > 0:
                song_notes.append(note[index:])
                note_set.add(note[index:])
        song_notes.append("/")
        songs.append(song_notes)
    note_set.add("/")
    return songs, note_set


def create_map(character_set):
    map = dict()
    i = 0
    for s in character_set:
        map[s] = i
        i += 1
    return map


def map_load(map_path, map_name):
    with open(map_path+map_name, "r") as fp:
        map = json.load(fp)
    return map


def map_write(map, map_path, map_name):
    with open(map_path+map_name, "w") as fp:
        json.dump(map, fp, indent=4)


def mapping(song_notes, map):
    mapped_songs = []
    for song in song_notes:
        note_int = []
        for symbol in song:
            note_int.append(map[symbol])
        mapped_songs.append(note_int)
    return mapped_songs


def get_train_test(datas, sequence_len, sep):
    x, y = [], []

    for data in datas:
        if (len(data)-sequence_len) > 0:
            for j in range(len(data)-sequence_len):
                x.append(data[j:j+sequence_len])
                y.append(data[j+sequence_len])
        else:  # (len(data)-sequence_len) ==0
            alt = data[:-1]
            for i in range(len(alt), sequence_len):
                alt.append(sep)
            x.append(alt)
            y.append(data[-1])
    return x, y


def create_reverse_map(map):
    reversed_map = {}
    for key in map:
        reversed_map[map[key]] = key
    return reversed_map

def demapping(sequence,map):
  new_sequence=[]
  for value in sequence:
    new_sequence.append(map[value])
  return new_sequence

def generate_melody_sequence(seed, stop, model):
    created_melody = seed
    for i in range(512):
        predicted = model.predict(
            np.array(created_melody[-64:]).reshape(1, 64, 1))
        predicted = predicted.argmax()
        created_melody.append(predicted)
        if predicted == stop:
            return created_melody
    created_melody.append(stop)
    return created_melody

