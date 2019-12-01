# Importing all necessary libraries
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
import random

# Specifying the data directory and the categories of images
DATADIR = 'D:\\MLTrainImages\\CatsAndDogs2\\train'
CATEGORIES = ['Dog', 'Cat']
LENGTH = 70

# Create a list of out data for training
training_data = []

# Define a function for dataset creation
def data_maker():

    # Loop over the categories in the list of categories
    for category in CATEGORIES:

        # Specify the path to the images of a given category
        # os.path.join joins its arguments into a system path, in this case we have a folder for data training, in which we have a 'cat' and a 'dog' folder
        path = os.path.join(DATADIR, category)

        # Specify a number by which to categorize the images, by taking the index of the category
        class_number = CATEGORIES.index(category)

        # Cycle through each image in the directory. os.listdir will list the items in the directory specified
        for image in os.listdir(path):
            
            # Try to do the following:
            try:
                # Read an image, and convert it to grayscale
                image_array = cv2.imread(os.path.join(path, image), cv2.IMREAD_GRAYSCALE)

                # Resize the image to make processing more manageable and to standardize the size for the neural network
                new_image_array = cv2.resize(image_array, (LENGTH, LENGTH))

                # Add the image along with its identifier to the training data set
                training_data.append([new_image_array, class_number])
            
            # If the above fails, pass
            except Exception:
                pass
        
data_maker()

# Shuffle the data, as feeding ALL cats and then ALL dogs wouldn't properly train the neural network
random.shuffle(training_data)

# We then separate the features (image data) and their labels into 2 arrays which we define first
X = []
y = []

for feature, label in training_data:
    X.append(feature)
    y.append(label)

# X needs to be converted from a list, to a numpy array for Keras to process it correctly
# The -1 in reshape specifies the amount of features we have, where -1 can be used for any value.
# The 2 LENGHTs specify the size of the feature, and the 1 essentially means the image is grayscale
X = np.array(X).reshape(-1, LENGTH, LENGTH, 1)

# Lastly, so that we do not have to remake the dataset every single time we run the program, the X and y arrays are saved to their own files
np.save('cats_and_dogs_features.npy', X)
np.save('cats_and_dogs_labels.npy', y)