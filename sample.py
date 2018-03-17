from flask import Flask, render_template, request, flash, jsonify, url_for, redirect
from flask import session as login_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Register
import json
engine =  create_engine("postgresql+psycopg2://bhanu:bhanu@localhost/experiment6")
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
session = DBsession()
DBsession.autoflush=True
app = Flask(__name__)


@app.route('/home')
@app.route('/')
def HomePage():
    return render_template('home.html')

@app.route('/register', methods=['POST','GET'])
def RegisterSuccess():

    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        try:
            user = session.query(Register).filter_by(email=request.form['email']).first()
            if request.form['pass'] != request.form['repass']:
                flash('Password does not match')
                return redirect('/register')
            if user == None:
                newuser = Register(email = request.form['email'], password = request.form['pass'])
                session.add(newuser)
                flash ('User Created Succcessfully')
                flash('You Can Now Login')
                session.commit()
                return redirect('/login')
            if user.email == request.form['email']:
                flash('User Already exist')
                return redirect('/login')

        except:
            session.rollback()
            flash('Invalid Credentials')
            return redirect("/register")


@app.route('/register/jsonapi', methods = ['POST','GET'])
def RegisterAPI():
    if request.method == 'GET':
        json = session.query(Register).all()
        return jsonify(users=[u.serialize for u in json])
    elif request.method == 'POST':

        try:

            data = request.get_json()
            newuser = Register(email = data['email'], password = data['password'])
            session.add(newuser)
            session.commit()
            return jsonify({"result" : "!success"})
        except:
            session.rollback()
            return jsonify({'result' : '!failure'})

@app.route('/login', methods=['POST','GET'])
def Login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        #user = session.query(Register).filter_by(email=request.form['email'],password = request.form['pass']).first()
        try:
            user = session.query(Register).filter_by(email=request.form['email']).one()
            if user.email == request.form['email'] and user.password == request.form['pass']:
                flash('You are now logged in')
                login_session['username'] = user.email
                return redirect('/')
            elif user.email != request.form['email']:
                flash('User Does Not Exist! Register First Please')
                return('/register')
            elif user.email == request.form['email'] and user.password != request.form['pass']:
                flash('Please Enter Correct Password!')
                return redirect('/login')
        except:
            flash('Invalid credentials! Please Register')
            return redirect('/register')
@app.route('/backgroud_process')
def backgroundProcess():
    try:
        model = request.args.get('carModel')
        return jsonify(result = 'Hell')
    except Exception(e):
        return(str(e))


@app.route('/logout')
def logout():
    del login_session['username']
    flash('You are now logged out')
    return redirect('/')
@app.route('/profile')
def UserProfile():
    return render_template('profile.html')


if __name__ =='__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port = 8000)
