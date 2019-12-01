import numpy as np
import keras
from keras.models import Sequential, load_model, save_model
from keras.layers import Conv2D, Activation, Flatten, Dense, Dropout, MaxPooling2D
from keras.callbacks import TensorBoard
import time

MODEL_NAME = 'cats_and_dogs_convnet_64x4-64_b30_7e_V2_{}'.format(int(time.time()))

tensorboard = TensorBoard(log_dir='logs\\{}'.format(MODEL_NAME))

# Load in the data we made earlier
X = np.load('cats_and_dogs_features.npy')
y = np.load('cats_and_dogs_labels.npy')

# Pixel data ranges from 0 to 255, so normalizing the data is necessary
X = X/255.0

# Create a new sequential model
model = Sequential()

# Adding a new 2D Convolutional layer to the sequential model with 64 nodes, and a 3x3 window
# The data in X is structured as: (-1, LENGTH, LENGTH, 1), so by typing X.shape[1:] we specify everything except the 1st parameter
# As such, the input data will be structured as (LENGTH, LENGTH, 1), corresponding to the size of the image, and its grayscale colours
# We then add an activation layer and a max pooling layer
# The activation layer serves as an activation function to determine if the neuron will "fire" or not
# Max Pooling essentially "simplifies" or downsamples an image allowing to make assumptions about regions
# For a detailed explanation see: https://www.quora.com/What-is-max-pooling-in-convolutional-neural-networks/answer/Jay-Ricco
model.add(Conv2D(64, (3,3), input_shape = X.shape[1:], activation='relu'))
model.add(MaxPooling2D(2,2))

# We can add another layer and this time the shape does not have to be specified as Keras can infer shape from previous layers
model.add(Conv2D(64, (3,3), activation='relu'))
model.add(MaxPooling2D(2,2))

model.add(Conv2D(64, (3,3), activation='relu'))
model.add(MaxPooling2D(2,2))

model.add(Conv2D(64, (3,3), activation='relu'))
model.add(MaxPooling2D(2,2))

# A densely connected layer can be added, but it requires a 1 dimensional data input, so the data is flattened first
model.add(Flatten())
model.add(Dense(64, activation='relu'))

# Lastly a dense layer with 1 neuron is added. It will act as an output, either firing or not, depending on the resulting prediction being a cat or a dog
model.add(Dense(1, activation='sigmoid'))

# The model can then be compiled, since we only have 2 categories we can use binary crossentropy as our cost function
# The cost is then optimized with the 'Adam Optimizer'
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# We can then let the model fit the data and labels
# batch_size specifies the amount of data taken at once to train
# validation_split specifies the % of data to be used as a "validation set" to ensure the model is getting the coorect results
model.fit(X, y, batch_size=30, epochs=7, validation_split=0.1, callbacks=[tensorboard])
model.save("models\\{}.h5".format(MODEL_NAME))