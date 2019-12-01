import keras
import os
from keras.models import Sequential, load_model, save_model
from keras.layers import Conv2D, Activation, Flatten, Dense, Dropout, MaxPooling2D
import numpy as np
from CatsAndDogsPredictionConverter import convert_data

def CatOrDog(data):
    MODELS_DIR = "D:\\PythonProjects\\CatsAndDogsML\\models"
    MODEL = "cats_and_dogs_convnet_64x4-64_b30_7e_V2_1574617104.h5"
    model = load_model(os.path.join(MODELS_DIR, MODEL))

    if (model.predict(convert_data(data)))[0] == 0:
        return "dog"
    else:
        return "cat"