from flask import Flask, jsonify, request, render_template, url_for, session
from forms import SignUp, Login, AdminLogin ,AdminSignUp
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
#import re
import mysql.connector
import pymysql.cursors
import json


import sqlite3
import os
import re

currentdirectory = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

app.config['SECRET_KEY'] = 'MANI26'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password123'
# app.config['MYSQL_DB'] = 'Trainticketing'
# mysql = MySQL(app)

connection = pymysql.connect(host='mani26.mysql.pythonanywhere-services.com',
                             user='mani26',
                             password='Phaniraj61@',
                             database='mani26$TTS',
                             cursorclass=pymysql.cursors.DictCursor)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    form = Login()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # connection = pymysql.connect(host='localhost',
        #                              user='root',
        #                              password='password123',
        #                              database='sys',
        #                              cursorclass=pymysql.cursors.DictCursor)
        #connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM Users WHERE (username = '{u}' AND password = '{p}')".format(u=username, p=password))
        account = cursor.fetchone()
        if account:
            print(account)
            session['logged_in'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            print("LOGIN STATUS", session['logged_in'])
            return render_template('home.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg, form=form)


@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    msg = ''
    admin_flag=False
    form = AdminLogin()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(username,password)
        # connection = pymysql.connect(host='localhost',
        #                              user='root',
        #                              password='password123',
        #                              database='sys',
        #                              cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM Admin_Users WHERE (AdminName = '{n}' and AdminPassword='{p}' )".format(n=username, p=password))
        account = cursor.fetchone()
        print("ACCOUNT",account)
        if account:

            session['logged_in'] = "admintrue"
            session['id'] = account['AdminID']
            session['username'] = account['AdminName']
            msg = 'Logged in successfully as Admin!'
            print("LOGIN STATUS", session['logged_in'])
            #session['logged_in'] = "admintrue"
            #print("ADMIN FLAG",session['logged_in'])
            return render_template('home.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
            admin_flag=False
    return render_template('adminlogin.html', msg=msg, form=form,admin_flag=admin_flag)


@app.route('/succesfull', methods=['GET', 'POST'])
def successful():
    return render_template("successful.html")

@app.route('/updatedb',methods=['GET','POST'])
def updatedb():
    result=''
    if request.method =='POST' and 'query' in request.form:
        query = request.form['query']
        # connection = pymysql.connect(host='localhost',
        #                              user='root',
        #                              password='password123',
        #                              database='sys',
        #                              cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

    return render_template("updatedb.html",result=result)
@app.route('/logout')
def logout():
    session['logged_in'] = False

    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('home.html')




@app.route('/myaccount', methods=['GET', 'POST'])
def myaccount():
    user_id = session['id']
    # connection = pymysql.connect(host='localhost',
    #                              user='root',
    #                              password='password123',
    #                              database='sys',
    #                              cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT o.username,o.train_name,s.source_location,s.destination_location,s.travel_date,s.time FROM Orders as o join Subways as s on o.train_id = s.train_id WHERE (id = '{uid}')".format(
            uid=user_id))

    result = cursor.fetchall()
    return render_template('myaccount.html', result=result)


@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    return render_template('contactus.html')

@app.route('/aboutus')
def aboutus():
    return render_template('Aboutus.html')


@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    msg = 'Please select train'

    if request.method == 'POST' and 'train' in request.form:
        print(request)
        print("REQUEST FORM", request.form)
        print(session['username'])
        print(session['id'])
        train = request.form.get("train")

        print(type(train),train)
        train = train[1:-1]
        train = train.split(',')
        print(type(train), train)
        train_id = train[0][12:]
        print("TRAIN ID",train_id)
        train_name = train[1][15:]
        source = train[2][21:-1]
        destination = train[3][26:-1]
        price = train[4][9:]
        print("VALUES",type(train_id),train_name[16:-1],source[21:-1],destination[26:-1],price[9:])
        msg = "From " + source + " to " + destination+ " costs $" + price + " for " + train_name
        print(msg)
        booking_status = True
        # connection = pymysql.connect(host='localhost',
        #                              user='root',
        #                              password='password123',
        #                              database='sys',
        #                              cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        sameorder_check = "SELECT * FROM Orders WHERE username = '{s}' and train_id={t}".format(s=session['username'],t=train_id)
        cursor.execute(sameorder_check)
        print("BEFORE IF LOOP")
        account = cursor.fetchone()
        if account:
            msg = 'Ticket has already booked. Please check in Reports my account'
            print(msg)
        else:

            cursor.execute(
                "INSERT INTO Orders VALUES ('{tid}', '{uid}', '{bs}', "'{tn}'",'{un}')".format(tid=train_id,
                                                                                               uid=session['id'],
                                                                                               bs=booking_status,
                                                                                               tn=train_name,
                                                                                               un=session['username']))

            connection.commit()
            print(cursor.execute("select * from Orders"))
            connection.close()

            #msg = 'You have successfully booked !'
    return render_template('checkout.html', msg=msg)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ''
    form = SignUp()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # connection = pymysql.connect(host='localhost',
        #                              user='root',
        #                              password='password123',
        #                              database='sys',
        #                              cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        query_signup = "SELECT * FROM Users WHERE username = '{s}'".format(s=username)
        cursor.execute(query_signup)
        print("BEFORE IF LOOP")
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            print("GOING TO ELSE LOOP")
            cursor.execute(
                "INSERT INTO Users VALUES (NULL,'{u}', '{p}', '{e}')".format(u=username, p=password, e=email))
            connection.commit()
            connection.close()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg=msg, form=form)


@app.route('/adminsignup', methods=['GET', 'POST'])
def adminsignup():
    msg = ''
    form = AdminSignUp()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'railway_id' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        railway_id = request.form['railway_id']
        # connection = pymysql.connect(host='localhost',
        #                              user='root',
        #                              password='password123',
        #                              database='sys',
        #                              cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        query_admin = "SELECT * FROM Admin_Users WHERE AdminName = '{s}' and AdminPassword='{p}' and AdminEmail='{e}'and AdminRaliwayID= '{r}'".format(s=username,p=password,e=email,r=railway_id)
        cursor.execute(query_admin)
        print("BEFORE IF LOOP")
        print(cursor.fetchall(),"CUROSR",cursor.fetchone())
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            print("GOING TO ELSE LOOP")
            cursor.execute(
                "INSERT INTO Admin_Users VALUES (NULL,'{u}', '{p}', '{e}', '{r}')".format(u=username, p=password, e=email,
                                                                                     r=railway_id))
            connection.commit()
            connection.close()
            msg = 'You have successfully registered as Admin!'
    elif request.method == 'POST':
        msg = 'Please fill out the admin form !'
    return render_template('admin.html', msg=msg, form=form)


@app.route('/', methods=['GET', 'POST'])
def home():
    print(request.form)
    print(request.form.get("source"))
    return render_template("home.html", title='home')


@app.route('/subways', methods=['GET', 'POST'])
def subway():
    msg='Please select the trains'
    result=''
    try:
        if request.method == 'POST':
            print(request)
            source = request.form.get("source")
            destination = request.form.get("destination")
            date = request.form.get("Travel Date")
            # connection = pymysql.connect(host='localhost',
            #                              user='root',
            #                              password='password123',
            #                              database='sys',
            #                              cursorclass=pymysql.cursors.DictCursor)
            cursor = connection.cursor()
            print("SOURCE LOcation & destination & date", source, destination, date)
            query1 = "select * from Subways where (source_location='{s}' and destination_location='{d}' and travel_date='{dd}')".format(
                s=source, d=destination, dd=date)
            print(query1)
            cursor.execute(query1)
            result = cursor.fetchall()
            msg="available trains are"
            print(result,"result before fetchall")


            print("RESULT after fetchall", result)
            return render_template("subway.html", result=result,msg=msg)
    except:
        msg = "No trains available"
        print("result")
        return render_template("subway.html", result=result,msg=msg)
    return render_template("subway.html",msg=msg)

if __name__ == '__main__':
    app.run(debug=True)
