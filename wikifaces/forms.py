from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Length, URL, Optional
from wikifaces import blender

class UserInput(FlaskForm):
    person = StringField('Search for anyone',
                         validators=[ Length(max=20),Optional()], #DataRequired(),
                         render_kw={"placeholder": "Search for:"})
    wiki_url = StringField('Past here link of person on wikipedia',
                         validators=[Optional()],
                            render_kw={"placeholder": "Insert Wikipedia URL here"})
    uploaded_file = FileField('file')
    submit = SubmitField('Process')

    # def processed_person_name(flask_form_object, person , uploaded_img):
    #     if person == None:
    #         return {}
    #
    #     return blender.blending_face_text(person, uploaded_img)



class Processing(FlaskForm):
    submit = SubmitField('Processing...')
