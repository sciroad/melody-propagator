import json
import os
import music21 as music
import numpy as np
import pandas as pd
import math
import keras

from . import util 


def prepare():
    dataset_path = "dataset/"
    base_path = "./"
    map_path = "map/"
    dataset_name = "dataset"
    map_name = "map_file.json"
    map = util.map_load(base_path+map_path, "map_file.json")
    dataset = util.dataset_read(base_path+dataset_path, dataset_name)
    splited_dataset, note_set = util.dataset_spliter(dataset)
    mapped_dataset = util.mapping(splited_dataset, map)
    train_x, train_y = util.get_train_test(mapped_dataset, 64, sep=map["/"])
    arr = np.array(train_x)
    df = pd.DataFrame(arr)
    model = keras.models.load_model(
        base_path+"models/model_with_2dropout_8418percent.h5")
    reversed_map = util.create_reverse_map(map)
    return model, train_x, reversed_map, map