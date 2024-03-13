from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send

import dataBase

app = Flask(__name__)
app.config['SECRET'] = 'salom'
socketio = SocketIO(app, cors_allowed_origins="*",)

users = []

@socketio.on("message")
def sendMessage(message):
    print(request.sid,message)
    send(message, broadcast=True)
    # users.append(request.sid)
    # print(users)
    # send() function will emit a message vent by default

def validate(n,u,p,p_c):
    errors = []
    if len(n)<4:
        errors.append({'name':'name xato'})
    if len(u)<6:
        errors.append({'username':'username xato'})
    if p!=p_c:
        errors.append({'password':'password mos emas'})
    return errors


@app.route("/")
def homePage():
    return render_template("index.html")

@app.route("/message")
def message():
    return render_template("message.html")

@app.route("/login",methods=['get','post'])
def loginPage():
    print(request.method)
    if request.method=='POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        errors = validate(name,username,password,password_confirm)
        print(errors)
        if len(errors)==0:
            dataBase.insertUser(name,username,password)
            return render_template('index.html',user=name)

    return render_template("login.html")

@app.route("/register",methods=['get','post'])
def registerPage():
    print(request.method)
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = dataBase.checkUser(username,password)
        print(user)
        if len(user)!=0:

            return render_template('index.html',user=user[0][1])

    return render_template("register.html")


if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app,host='localhost')
    # socketio.run(app,host='192.168.77.136')
