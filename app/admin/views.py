from flask import url_for, redirect, flash
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask import session
from app.database.functions import generate_hash, get_hash
from datetime import datetime


class MyIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if session['User'] == 'Admin':
            return self.render('admin/index.html')
        elif session['User'] == 'User':
            return redirect(url_for('auth.auth_index'))
        return redirect(url_for('index'))


class CustomModelView(ModelView):
    def is_accessible(self):
        if session['User'] == 'Admin':
            return True
        return False


class UserView(CustomModelView):
    def create_model(self, form):
        flash('Password automatically generated', 'success')
        form.password.data = generate_hash(form.password.data)
        super(UserView, self).create_model(form)
        return True


class FileView(CustomModelView):
    def create_model(self, form):
        if form.hash.data is None:
            form.hash.data = get_hash(form.file_address.data)
            flash('File automatically hashed', 'success')
        if form.date.data is None:
            flash('Date automatically added', 'success')
            form.date.data = datetime.now()
        super(FileView, self).create_model(form)
        return True
