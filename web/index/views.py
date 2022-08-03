from flask import flash, render_template

from .forms import LogbookForm
from .models import db, LogbookModel


def index():
    form = LogbookForm()
    if form.validate_on_submit():
        first = form.data['first']
        last = form.data['last']
        record = LogbookModel(first=first, last=last)
        db.session.add(record)
        db.session.commit()
        flash('You signed! View the database table in the Admin site.')
    return render_template('index.html', form=form)
