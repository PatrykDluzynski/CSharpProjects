from flask import Flask, redirect, render_template, request, url_for
from keras.models import Sequential, load_model, save_model
from keras.layers import Conv2D, Activation, Flatten, Dense, Dropout, MaxPooling2D
import keras
import numpy as np
import os
import cv2

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Define temp storage for images and max amount of uploads
TMP_STORAGE = "static\\tmp\\"
AMOUNT = 10

LENGTH = 70
MODELS_DIR = "models"
MODEL = "cats_and_dogs_convnet_64x4-64_b30_7e_V2_1574617104.h5"
model = load_model(os.path.join(MODELS_DIR, MODEL))

# Define a redirect to home
@app.route('/')
def index():
    return redirect("/home")

# Render homepage
@app.route('/home')
def home():
    return render_template("home.html")

# Define predict page
@app.route('/predict', methods=["GET", "POST"])
def predict():
    # If a user gets the page, render x amount of spaces for file uploads, each space having its own label to iterate through the images
    if request.method == "GET":
        return render_template("predict.html")

    # If a user posts images...
    elif request.method == "POST":
        # Clear the tmp folder of its images
        for img in os.listdir(TMP_STORAGE):
            os.remove(os.path.join(TMP_STORAGE, img))

        # Iterate through the file upload spaces, and if there was a file, save it to the tmp folder
        if request.files["Files"]:
            images = request.files.getlist("Files")
            for i in range(len(images)):
                images[i].save(os.path.join(TMP_STORAGE, images[i].filename))
        
        predictions = []
        images = []
        for img in os.listdir(TMP_STORAGE):
            try:
                image_array = cv2.imread(os.path.join(TMP_STORAGE, img), cv2.IMREAD_GRAYSCALE)
                new_image_array = cv2.resize(image_array, (LENGTH, LENGTH))
                data = np.array(new_image_array).reshape(-1, LENGTH, LENGTH, 1)
                if (model.predict(data))[0] == 0:
                    predictions.append("dog")
                else:
                    predictions.append("cat")

                images.append(img)

            except Exception:
                return render_template("error.html", image=img)

        cards = []

        for i in range(len(predictions)):
            cards.append(
            """<div class='col mb-4'>
                \n\t<div class='card h-100'>
                \n\t<img src='/static/tmp/{}' class='card-img-top h-75'>
                    \n\t\t<div class='card-body'>
                        \n\t\t\t<h5 class='card-title'>Image {}</h5>
                        \n\t\t\t<p class='card-text'>I think that this is a {}.</p>
                    \n\t\t</div>
                \n\t</div>
            \n</div>""".format(images[i], i+1, predictions[i])
            )

        return render_template("prediction.html", cards=cards, amount=len(predictions))

@app.route('/credits')
def credits():
    return render_template('credits.html')

if __name__ == '__main__':
    app.run()