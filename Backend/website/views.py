from flask import Blueprint, render_template, request, flash, jsonify, Response
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Note,Profile
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Feedback/Suggestion is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Feedback/Suggestion added!', category='success')
    return render_template("feedback.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/profile', methods=['POST'])
@login_required
def upload():
    pic = request.files['pic']
    if not pic:
        return 'No pic uploaded!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    img = Profile(img=pic.read(), name=filename, mimetype=mimetype, user_id=current_user.id)
    db.session.add(img)
    db.session.commit()

    return 'Img Uploaded!', 200

@views.route('/reports')
@login_required
def get_img():
    id= current_user.id
    img = Profile.query.filter_by(id=id).first()
    if not img:
        return 'No Report Found!', 404

    return Response(img.img, mimetype=img.mimetype)