import os
from flask import Flask, request, redirect, url_for, send_file
from flask_autoindex import AutoIndex
from werkzeug.utils import redirect, secure_filename


ppath = 'shared'

app = Flask(__name__)

AutoIndex(app, browse_root=ppath)

app.config['UPLOAD_PATH'] = 'shared'


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_files = request.files.getlist("file[]")
    for uploaded_file in uploaded_files:
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            uploaded_file.save(os.path.join(
                app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('autoindex'))


@app.route('/delete/<path>')
def delete(path):
    os.remove(ppath + "\\" + path)
    return redirect(url_for('autoindex'))


@app.route('/download/<file>')
def downloadFile(file):
    return send_file(ppath + "\\" + file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
