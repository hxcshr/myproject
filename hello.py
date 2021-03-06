
import os
from flask import Flask, flash, request, redirect, url_for, render_template
from flask.helpers import send_file
from werkzeug.utils import secure_filename
from flask import send_from_directory
import zipfile


UPLOAD_FOLDER = './uploadsImgs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024



def allowed_file(filename):
    extension = ''
    if '.' in filename:
        extension = filename.rsplit('.',1)[1].lower()
    else:
        return (False,extension)
    return (extension in ALLOWED_EXTENSIONS, extension)


@app.route('/', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        username = request.form['username']
        usertel = request.form['usertel']
        if 'file' not in request.files or 'file2' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        file2 = request.files['file2']
        if file.filename == '' or file2.filename == '':
            flash('No selected file')
            return redirect(request.url)
        result = allowed_file(file.filename)
        result2 = allowed_file(file2.filename)
        if file and file2 and result[0] and result2[0]:
            filename = username + '_' + usertel + '健康码.' + result[1]
            file2name = username + '_' + usertel + '行程码.' + result2[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'],file2name))
            return redirect(url_for('uploaded_file',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>上传信息</h1>
    <form method=post enctype=multipart/form-data>
    学生姓名: <input type=text name=username><br>
    电话号码: <input type="tel" name=usertel><br>
    健康码   :<input type=file name=file><br>
    行程码   :<input type=file name=file2><br>
    <input type=submit value=立即上传>
    </form>
    '''


def zip_imgs():
    zf = zipfile.ZipFile('./imgs.zip','w',zipfile.ZIP_DEFLATED)
    files = os.listdir(UPLOAD_FOLDER)
    for tmp in files:
        zf.write(UPLOAD_FOLDER+'/'+tmp)
    zf.close()
    


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download/')
def download_imgs():
    imgpath = './imgs.zip'
    if os.path.exists(imgpath):
        os.remove()
    zip_imgs()
    return send_file(imgpath)


@app.route('/')
def index():
    return "Index page"

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return request.method
    # return render_template('hello.html',name=name+request.method)

@app.route("/user/<username>")
def show_user_profile(username):
    return 'User %s' % (username)

@app.route('/number/<int:mynum>')
def show_my_num(mynum):
    return 'my num is %s' % mynum

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return 'subpath is %s' % subpath


        



