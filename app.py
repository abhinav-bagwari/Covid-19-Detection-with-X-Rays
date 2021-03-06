from __future__ import division, print_function
# coding = utf-8
import sys
import os
import glob
import re
import numpy as np




# keras
from keras.models import load_model
from keras.preprocessing import image

# flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename


#Define a flask app
app = Flask(__name__)

#Load the saved model
MODEL_PATH = 'covid_model.h5'

# Loading trained model
model = load_model(MODEL_PATH)
# model._make_predict_function()



def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(256, 256))

    # Preprocessing the image
    img = image.img_to_array(img)/255

    img = np.array([img])

    preds = (model.predict(img) > 0.5).astype("int32")
    preds_op = preds[0]
    return preds_op[0]



@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')



@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

        if (preds == 0):
            result = "COVID"
        else:
            result = "NOT COVID"
        return result
    return None
        


if __name__ == '__main__':
    app.run(debug=True)
    