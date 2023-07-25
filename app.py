import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp', 'jpeg', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TESTING'] = True
app.testing = True
app.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def processImage(filename, operation):
    print(f"The file name is {filename}, and the operation is {operation}")
    # Use f-string to include the filename variable
    img = cv2.imread(f"uploads/{filename}")

    if operation == "cgray":
        print("1")
        imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print("2")
        newFilename = f"static/{filename}"
        print("3")
        cv2.imwrite(newFilename, imgProcessed)
        print("4")
        return newFilename
    elif operation == "cwebp":
        newFilename = f"static/{filename.split('.')[0]}.webp"
        cv2.imwrite(newFilename, img)
        return newFilename
    elif operation == "cjpg":
        newFilename = f"static/{filename.split('.')[0]}.jpg"
        cv2.imwrite(newFilename, img)
        return newFilename
    elif operation == "cpng":
        newFilename = f"static/{filename.split('.')[0]}.png"
        cv2.imwrite(newFilename, img)
        return newFilename


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    if request.method == 'POST':
        # check if the post request has the file part
        operation = request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return "NO file part "
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(
                f"Your file is processed and is available at <a href='{new}' target='_blank'>here</a>")
            return render_template("index.html")

    return render_template("index.html")


app.run(debug=True, port=5000)
