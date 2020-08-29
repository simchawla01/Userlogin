from flask import render_template, url_for, redirect, request
from Userlogin import app,db
from Userlogin.models import User
from Userlogin.forms import LoginForm,RegisterForm,ChooseUserForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required, logout_user, current_user

@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                return render_template('login.html',form=form)
        return redirect(url_for('signup'))
    return render_template('login.html',form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hash_pswd = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,password=hash_pswd)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html',form=form)
    

@app.route('/home', methods=['GET','POST'])
@login_required
def home():
    form = ChooseUserForm()
    form.username.choices = [(line.username) for line in User.query.all()]
    return render_template('home.html',form=form)

@app.route('/delete',methods=['GET','POST'])
@login_required
def delete():
    form = ChooseUserForm()
    User.query.filter_by(username=form.username.data).delete()
    db.session.commit()
    return redirect(url_for('home'))
    
@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))    
    
@app.errorhandler(404)
def page_not_found(e):
    return '<h1>404</h1>'
