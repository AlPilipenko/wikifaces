"importing Flask class"
"render_template allows to return html templates in our routes"
from flask import render_template, url_for, flash, redirect, request, send_from_directory, abort
from wikifaces.forms import UserInput
from flask import Blueprint
from flask import current_app
import os
import validators
from wikifaces import blender
import secrets
from pathlib import Path
import shutil
routes = Blueprint('routes', __name__)
import time
#== Functions ========================================================================
def processed_person_name(person , uploaded_img):
    print("PR PER NAME in ROUTES", person)
    if person == None:
        return {}

    return blender.blending_face_text(person, uploaded_img)


def clean_dir(keep_file, path):
    "deletes files in temp_images directory"
    # print(path)
    for filename in os.listdir(path[:-20]):
        if filename.endswith(".jpg") and filename != keep_file:
            file_path = os.path.join(path[:-20], filename)
            os.remove(file_path)


def allowed_file(filename):
    "filters file extensions"
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_uploaded_file(form_uploaded_file, usr_folder):
    "When user uploads file - saves it to the upload folder"
    file_path = os.path.join(usr_folder, 'user_uploaded_file.jpg')
    form_uploaded_file.save(file_path)
    return file_path


def clean_user_session(requests):
    "deletes images that were created during user session"
    to_delete = requests.get('filename')
    to_delete = to_delete[:-20]
    try:
        shutil.rmtree(to_delete)
    except:
        pass


def profilactic_clean():
    "delete files in temp_images if files are older than 5 min"
    for dirpath, dirnames, filenames in os.walk(current_app.config['UPLOAD_FOLDER']):
        if time.time() - int(os.stat(dirpath).st_mtime) > 300 and dirpath != current_app.config['UPLOAD_FOLDER']:
            shutil.rmtree(dirpath)


#== Decorators =======================================================================
"decorators allows us to navigate around routes on our website"
@routes.route('/home', methods=["GET","POST"])
@routes.route('/', methods=["GET","POST"])
def home():
    if request.args:
        clean_user_session(request.args)
    profilactic_clean()

    searched_person = UserInput()
    current_app.config["SESSION"]['searched_person'] = searched_person

    if searched_person.validate_on_submit() or searched_person.wiki_url.data:

        random_hex = secrets.token_hex(8)
        Path(current_app.config['UPLOAD_FOLDER'] + random_hex).mkdir(parents=True, exist_ok=True)
        usr_folder = current_app.config['UPLOAD_FOLDER'] + random_hex


        if searched_person.person.data == '' and searched_person.wiki_url.data == '':
            flash('Please fill at least one field!', 'danger')
            return redirect(url_for('routes.home'))

        image_file = request.files['file']

        if image_file.filename != '':
            if allowed_file(image_file.filename) == False:
                print("NOT ALLOWED!!!!")
                flash("""'Allowed image formats: "pdf", "png", "jpg", "jpeg"'""", 'danger')
                return redirect(url_for('routes.home'))
            uploaded_img = save_uploaded_file(image_file, usr_folder)
        else:
            uploaded_img = usr_folder

        searched_person = searched_person.person.data if searched_person.person.data != "" else searched_person.wiki_url.data

        return render_template('loading.html', title='processing',data=(searched_person, uploaded_img ))

    return render_template('home.html', searched_person=searched_person)


@routes.route('/image_factory', methods=["GET","POST"])
def image_factory():
    "proccess data and saves current session and some user data"
    s = request.args
    searched_person = s.get('data')
    uploaded_img = s.get('amp;data')

    if  validators.url(searched_person) == True:
        _, path, name = processed_person_name(
                                searched_person, uploaded_img )
    else:
        _, path, name = processed_person_name(
                                searched_person, uploaded_img )

    return redirect(url_for('routes.image_display', name=name, path=path))


@routes.route('/wikiface', methods=["GET","POST"])
def image_display():
    s = request.args
    name = s.get('name')
    path = s.get('path')
    return render_template('image_display.html', title=name, file=path)


@routes.route('/remake')
def remake():
    r = request.args
    data = r.get("data")
    filename = r.get('filename')
    clean_dir('ripped_face.jpg', filename)
    remake_data = data, filename
    return render_template('loading.html', title='remaking', data=remake_data)


"<path:path>  -  convert to path(string)"
@routes.route('/download/<path:filename>')
def download_file(filename):
    path = current_app.config['UPLOAD_FOLDER'][10:] + filename[-20:-3]

    try:
        return send_from_directory(path,
                                   filename=filename[-20:], as_attachment=True)
    except FileNotFoundError:
        abort(404)
