import os
from flask import Flask, request, redirect, url_for, send_file
from flask.templating import render_template
from flask_autoindex import AutoIndex

from werkzeug.utils import redirect, secure_filename
from zipfile import ZipFile
from os.path import basename


ppath = 'shared'

app = Flask(__name__)
app.config['UPLOAD_PATH'] = ppath


AutoIndex(app, browse_root=ppath)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
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


@app.route('/zip', methods=['POST'])
def zip():
    name = request.form.get('zipname')
    zip_files = request.files.getlist("dir[]")
    for file in zip_files:
        filename = secure_filename(file.filename)
        if filename != '':
            file.save(os.path.join('zips', filename))
    if len(os.listdir('zips')) != 0:
        zipObj = ZipFile(f'shared/{name}.zip', 'w')
        for folderName, subfolders, filenames in os.walk('zips'):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, basename(filePath))
        for f in os.listdir('zips'):
            os.remove(os.path.join('zips', f))
    return redirect(url_for('autoindex'))


@app.route('/download/<file>')
def downloadFile(file):
    return send_file(ppath + "\\" + file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
