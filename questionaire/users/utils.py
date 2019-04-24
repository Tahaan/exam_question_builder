import os
import uuid

from PIL import Image
from flask import url_for, current_app
from flask_mail import Message

from questionaire import mail


def save_picture(form_picture):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(uuid.uuid4()) + f_ext
    picture_path = os.path.join(current_app.root_path, 'static', 'profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request',
                  sender="noreply@demo.com",
                  recipients=[user.email])
    msg.body = '''
To reset your password, visit the following link:
{reset_link}

If you did not make this request you can safely ignore this message
'''.format(reset_link=url_for('users.reset_token', token=token, _external=True))

    mail.send(msg)
