import base64, secrets, io, os
from PIL import Image,ImageOps
from urllib.request import urlopen

from flask import Flask, request, jsonify, render_template, redirect, url_for
import numpy as np

from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

import psycopg2
import psycopg2.extras


##Env variables
import os
from dotenv import load_dotenv
load_dotenv()
conn = psycopg2.connect(dbname=os.environ['DB_NAME'], user=os.environ['DB_USER'], password=os.environ['DB_PASS'], 
                        host=os.environ['DB_HOST'])

model = load_model("./procesamiento/mnist_trained.h5")

app = Flask(__name__)

def predecir_im(im, invertir=True):
    image = img_to_array(im)
    image.shape

    # Scale the image pixels by 255 (or use a scaler from sklearn here)
    image /= 255

    # Flatten into a 1x28*28 array 
    img = image.flatten().reshape(-1, 28*28)
    img.shape
    if invertir:
        img = 1 - img
        
    # plt.imshow(img.reshape(28, 28), cmap=plt.cm.Greys)

    resultado = model.predict(img)
    resultado = np.argmax(resultado, axis=-1)
    return int(resultado[0])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api", methods=["POST"])
def main():
    miJSON = request.json
    try:
        imagen64 = miJSON["imagen"]
        imgdata = urlopen(imagen64)
        imgdata = imgdata.read()
        imgdata = Image.open(io.BytesIO(imgdata))

        password_length = 13
        extension = "png"
        nomre_unico = f'{secrets.token_urlsafe(password_length)}.{extension}'
        imgdata = imgdata.resize((28,28))
        imgdata.save(nomre_unico)

        im = image.load_img(nomre_unico, color_mode='grayscale',target_size=(28,28))
        os.remove(nomre_unico)

        etiqueta = predecir_im(im, invertir=False)
        respuesta= {"etiqueta": etiqueta}

        return jsonify(respuesta)
    except:
        return {"error": "We've had a problem"}
    
@app.route('/post_result', methods = ['GET','POST'])
def post_result():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        try:
            correct = request.form['correct']
            print(correct)
            print('Posting data')
            api_response = request.form['predicted']
            print(api_response)
            ##cur.execute('''INSERT INTO correct_classification_test values (%s %s %s)''', (predicted, correct, im))
        except:
            pass
        return redirect(url_for('index'))
    return render_template("index.html")

if __name__ == "__main__":
    app.run()






