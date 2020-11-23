from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# HTML 화면 보여주기
@app.route('/', methods=['GET'])
def home():
    return render_template('fileupload.html')


@app.route('/uploadajax', methods=['POST'])
def upload():
    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('./', filename))

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
