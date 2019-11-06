import os
import time
from flask import Flask, render_template, url_for, redirect, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
from yolo import get_predictions
import base64
import cv2

UPLOAD_FOLDER = 'image'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def showData():
        return render_template('index.html')

@app.route('/uploadpic1',methods=['GET', 'POST'])
def upload_file1():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'img1' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['img1'] 
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):

            filename = secure_filename(str(datetime.now()) + ".jpeg")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # ..........................................................
            image = cv2.imread(app.config['UPLOAD_FOLDER'] + '/' + filename)
            _, img_encoded = cv2.imencode(".jpg", image)
            predictions = get_predictions(img_encoded)

            # annotate the image
            for pred in predictions:
                # print prediction
                print(pred)

                # extract the bounding box coordinates
                (x, y) = (pred["boxes"][0], pred["boxes"][1])
                (w, h) = (pred["boxes"][2], pred["boxes"][3])

                # draw a bounding box rectangle and label on the image
                cv2.rectangle(image, (x, y), (x + w, y + h), pred["color"], 2)
                text = "{}: {:.4f}".format(pred["label"], pred["confidence"])
                cv2.putText(
                    image, 
                    text, 
                    (x, y - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, 
                    pred["color"], 
                    2
                )

            # save annotated image
            cv2.imwrite("static/img/" + filename, image)
            # 
            return redirect(url_for('showResult', file=filename))
            # return render_template('result.html', filename=filename)
        
        else:
			flash('Allowed file types are jpg or jpeg')
			return redirect(request.url)

@app.route('/uploadpic2',methods=['GET', 'POST'])
def upload_file2():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'img2' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['img2'] 
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):

            filename = secure_filename(str(datetime.now()) + ".jpeg")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # ..........................................................
            image = cv2.imread(app.config['UPLOAD_FOLDER'] + '/' + filename)
            _, img_encoded = cv2.imencode(".jpg", image)
            predictions = get_predictions(img_encoded)

            # annotate the image
            for pred in predictions:
                # print prediction
                print(pred)

                # extract the bounding box coordinates
                (x, y) = (pred["boxes"][0], pred["boxes"][1])
                (w, h) = (pred["boxes"][2], pred["boxes"][3])

                # draw a bounding box rectangle and label on the image
                cv2.rectangle(image, (x, y), (x + w, y + h), pred["color"], 2)
                text = "{}: {:.4f}".format(pred["label"], pred["confidence"])
                cv2.putText(
                    image, 
                    text, 
                    (x, y - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, 
                    pred["color"], 
                    2
                )

            # save annotated image
            cv2.imwrite("static/img/" + filename, image)
            return redirect(url_for('showResult', file=filename)) 

        else:
			flash('Allowed file types are jpg or jpeg')
			return redirect(request.url)
        

@app.route('/result', methods=['GET', 'POST'])
def showResult():
    return render_template('result.html', filename=request.args.get('file'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

