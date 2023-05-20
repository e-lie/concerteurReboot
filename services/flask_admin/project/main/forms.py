from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, RadioField, FloatField
from wtforms.validators import InputRequired, DataRequired

class AddQuestionForm(FlaskForm):
    title = StringField('Titre de la question', validators=[InputRequired()])
    text = TextAreaField('Texte de la question', validators=[InputRequired()])
    submit = SubmitField('Envoyer')

class AddMessageForm(FlaskForm):
    num = StringField('numéro de téléphone associé au message (33634354637 pour un portable)', validators=[InputRequired()])
    text = TextAreaField('Texte du message', validators=[InputRequired()])
    submit = SubmitField('Envoyer')

class ChangeScenarioForm(FlaskForm):
    num_messages = IntegerField('Nombre de messages à jouer', default=5, validators=[DataRequired()])
    play_interval = IntegerField('Interval de temps entre chanque message (ms)', validators=[DataRequired()], default=200)
    play_question = RadioField('Lire la question au début', choices=[('oui', 'Oui'), ('non', 'Non')], default='non', validators=[DataRequired()])
    random_play = RadioField('Lecture aléatoire', choices=[('oui', 'Oui'), ('non', 'Non')], default='oui', validators=[DataRequired()])
    virgule1_filename = StringField('Nom de fichier de virgule sonore initial (avec .wav extension)', default='virgule1.wav')
    virgule2_filename = StringField('Nom de fichier de virgule sonore séparatrice de réponse (avec .wav extension)', default='virgule2.wav')
    submit = SubmitField('Envoyer')
