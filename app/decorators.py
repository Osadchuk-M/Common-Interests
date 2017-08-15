from functools import wraps

from flask import redirect, flash, url_for
from flask_login import current_user


def interviewed(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.interviewed:
            return func(*args, **kwargs)
        flash('You should pass the poll before get access to this page.')
        return redirect(url_for('main.poll'))
    return decorated_view


def not_interviewed(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.interviewed:
            return func(*args, **kwargs)
        flash('You are already interviewed.')
        return redirect(url_for('main.home'))
    return decorated_view
