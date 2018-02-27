from flask import Flask, render_template, request, flash, jsonify, url_for, redirect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Register
import json

engine =  create_engine("postgresql+psycopg2://bhanu:bhanu@localhost/acws6")
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
        user = session.query(Register).filter_by(email=request.form['email']).first()

        if user != True:
            newuser = Register(email = request.form['email'], password = request.form['pass'])
            session.add(newuser)
            session.commit()
            flash('New User %s created successfully' % newuser.email)
            flash('You can Now login')
            return redirect('/login')
        else:
            return redirect('/register')






@app.route('/register/jsonapi')
def RegisterAPI():
    json = session.query(Register).all()
    return jsonify(users=[u.serialize for u in json])

@app.route('/login', methods=['POST','GET'])
def Login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        #user = session.query(Register).filter_by(email=request.form['email'],password = request.form['pass']).first()
        if session.query(Register).filter_by(email=request.form['email']).one() !=None:
            new = session.query(Register).filter_by(email=request.form['email']).one()
            if new.email == request.form['email'] and new.password == request.form['pass']:
                return redirect('/')
        elif session.query(Register).filter_by(email=request.form['email']).one() == None:
            return 'Register Yourself'
if __name__ =='__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port = 8000)
