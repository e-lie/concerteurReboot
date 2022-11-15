from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired

class AddQuestionForm(FlaskForm):
    title = StringField('Titre de la question', validators=[InputRequired()])
    text = TextAreaField('Texte de la question', validators=[InputRequired()])
    submit = SubmitField('Submit')

class AddMessageForm(FlaskForm):
    num = StringField('numéro de téléphone associé au message (33634354637 pour un portable)', validators=[InputRequired()])
    text = TextAreaField('Texte du message', validators=[InputRequired()])
    submit = SubmitField('Submit')
