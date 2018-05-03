from flask import Flask, render_template, request, flash, jsonify, url_for, redirect
from flask import session as login_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Register, Models, Companies, Booking, Workshop
from sqlalchemy.sql import text
import json
from sqlalchemy.orm import load_only
engine =  create_engine("postgresql+psycopg2://bhanu:bhanu@localhost/mendax")
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
session = DBsession()
DBsession.autoflush=True
app = Flask(__name__)


@app.route('/home')
@app.route('/')
def HomePage():
    return render_template('home.html')

@app.route('/register')
def RegisterSuccess():

    if request.method == 'GET':
        return render_template('register1.html')


@app.route('/user_register',methods=['GET','POST'])
def userRegister():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        try:
            user = session.query(Register).filter_by(email=request.form['email']).first()
            if request.form['pass'] != request.form['repass']:
                flash('Password does not match')
                return redirect('/register')
            if user == None:
                newuser = Register(name=request.form['name'],phone=request.form['phone'],email = request.form['email'], password = request.form['pass'])
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






@app.route('/workshop_register', methods=['POST','GET'])
def workshopRegister():
    if request.method == "GET":
        return render_template('workshop_register.html')
    if request.method == 'POST':
        newWorkshop = Workshop(name =request.form['name'], email_address =request.form['email'] , phone_number =request.form['phone'] ,password = request.form['pass'], aadhar_num = request.form['aadhar_number'],workshop_id = request.form['workshop_id'], gst = request.form['gst_number'] )
        session.add(newWorkshop)
        session.commit()
        flash("New Workshop Created")
        return redirect('/')



@app.route('/register/jsonapi', methods = ['POST','GET'])
def RegisterAPI():
    if request.method == 'GET':
        json = session.query(Register).all()
        return jsonify(users=[u.serialize for u in json])
    elif request.method == 'POST':

        #try:

            data = request.get_json()
            newuser = Register(email = data['email'], password = data['password'],phone=data['phone'], name=data['name'])
            session.add(newuser)
            session.commit()
            return jsonify({"result" : "!success"})
        #except:
            #session.rollback()
            #return jsonify({'result' : '!failure'})

@app.route('/login')
def Login():
    if login_session['username']== None and login_session['workshop'] == None:
        return render_template('login1.html')
        #user = session.query(Register).filter_by(email=request.form['email'],password = request.form['pass']).first()
    else:
        flash('Please logout first')
        return redirect('/home')
@app.route('/user_login',methods=['POST','GET'])
def userLogin():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
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

@app.route('/workshop_login',methods=['POST','GET'])
def workshopLogin():
    if request.method == 'GET':
        return render_template('workshop_login.html')
    if request.method == 'POST':
        try:
            user = session.query(Workshop).filter_by(email_address = request.form['email']).one()
            if user.email_address == request.form['email'] and user.password == request.form['pass']:
                flash('Yor are successfully logged into your Workshop')
                login_session['workshop']=request.form['email']
                return redirect('/')
        except:
            flash('Invalid Credentials')
            return redirect('/workshop_login')


@app.route('/background_process', methods=['POST'])
def backgroundProcess():
    #try:
        #car = request.args.get(model)
        carModel = request.get_data().decode('utf-8')
        data = json.loads(carModel)
        login_session['carmodel'] = data['model']
        #data = data['model'].encode('utf-8')
        que = session.query(Models).filter_by(model=data['model']).one()

        #payload = []
        #for result in que:
        #    content = {'model':que.model , 'basic' : que.basic, 'standard' : que.standard, 'comprehensive' : que.coprehensive}
        #    payload.append(content)
        #    content ={}
        return jsonify(model = que.model, basic = que.basic, standard = que.standard, comprehensive = que.comprehensive)
    #except:
        #return jsonify(result = "not successful"

@app.route('/schedule_service',methods=['POST'])
def scheduleService():
  try:
     if login_session['username'] != None:
      carmodel = login_session['carmodel']
      service_type = request.form['service']
      date_time = request.form['s_date']
      date, time = date_time.split(" ")
      user = session.query(Register).filter_by(email=login_session['username']).one()
      model = session.query(Models).filter_by(model = carmodel).one()
      model_id = model.model_id
      #print(type(model.str(service_type)))
      company = session.query(Companies).filter_by(id = model.id).one()
      #price = session.query(Models).filter_by(model = carmodel).options(load_only(*['comprehensive'])).first()
      price = session.execute("select {:s} from models where model_id = {:d}".format(service_type,model_id)).first()
      cost = price[0]
      print(cost)
      print(company.name)
      booking = Booking(user_id= user.id, company_id = company.id,model=carmodel, booking_type = service_type, price = cost, booking_date=date, time_slot1=time)
      session.add(booking)
      session.commit()
      #print(service_type)
      #print(date_time)
      #print(carmodel)
      #print(booking.id)
      #login_session['booking_id']= booking.id
      flash('Booking Scheduled')
      #return redirect('/')



      workshops = session.query(Workshop).all()
      return render_template('select_workshop.html',name = booking.model, date = booking.booking_date, workshops = workshops)
  except:
         flash('Please login first to Schedule a Service!')
         return redirect('/home')
    #except:
      # flash("Please login first To Schedule a Booking")
       #return redirect('/login')

#@app.route('/select_workshop',methods=['POST'])
#def selectWorkshop():

     # shop = request.get_data().decode('utf-8')
     # data = json.loads(shop)
     # print(data['workshop'])
     # booking = session.query(Booking).filter_by(id = login_session['booking_id']).one()
     # print(booking)
     # workshop = session.query(Workshop).filter_by(name = data['workshop']).one()
     # print (workshop)
      #booking.workshop_id = workshop.id
      #session.add(booking)
      #session.commit()
      #del login_session['carmodel']
      #return redirect('/')

@app.route('/_modal_processing', methods=['POST'])
def modalProcessing():
    company  = request.get_data().decode('utf-8')
    data = json.loads(company)
    print (data)
    query = session.query(Companies).filter_by(name = data['name']).one()
    models = session.query(Models).filter_by(id =  query.id).all()
    print (models)
    return jsonify(models =  models)

@app.route('/logout')
def logout():
    del login_session['username']
    flash('You are now logged out')
    return redirect('/')

@app.route('/workshop_logout')
def workshopLogout():
    del login_session['workshop']
    flash('Logged Out From you Workshop')
    return redirect('/')
@app.route('/profile')
def UserProfile():
    user  = session.query(Register).filter_by(email=login_session['username']).one()
    booking = session.query(Booking).filter_by(id = user.id).all()
    return render_template('profile.html', name = user.name, email = user.email, phone = user.phone, booking_time = booking.booking_time)

if __name__ =='__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port = 8000)
