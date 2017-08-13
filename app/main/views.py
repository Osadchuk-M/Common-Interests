from flask import render_template
from flask_login import login_required

from ..decorators import interviewed
from . import main


@main.route('/')
@login_required
@interviewed
def home():
    return render_template('index.html')


@main.route('/poll')
def poll():
    return render_template('poll.html')
