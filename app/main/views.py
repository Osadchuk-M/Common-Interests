from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from ..decorators import interviewed, not_interviewed
from ..models import Interest, User
from . import main
from .forms import PollForm


@main.route('/')
@login_required
@interviewed
def home():
    return render_template('index.html')


@main.route('/poll', methods=['GET', 'POST'])
@login_required
@not_interviewed
def poll():
    form = PollForm()
    if request.method == 'POST':
        user = current_user._get_current_object()
        user.update_interest_from_form(form)
        user.interviewed = True
        flash('Your interest has been saved.')
        return redirect(url_for('main.home'))
    return render_template('poll.html', form=form)


@main.route('/user/<username>')
@login_required
def user_page(username):
    user = User.query.filter_by(username=username).first()
    columns = Interest.__table__.columns
    return render_template('user.html', user=user, columns=columns)


@main.route('/difference/<username>')
@login_required
def diff_table(username):
    user = User.query.filter_by(username=username).first()
    distances = user.calculate()
    return render_template('distance.html', user=user, distances=distances)
