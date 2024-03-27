from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send

import dataBase

app = Flask(__name__)
app.config['SECRET'] = 'hello-world'
socketio = SocketIO(app, cors_allowed_origins="*",)

def validate(n,u,p,p_c):
    errors = []
    if len(n)<4:
        errors.append({'name':'name xato'})
    if len(u)<6:
        errors.append({'username':'username xato'})
    if p!=p_c:
        errors.append({'password':'password mos emas'})
    return errors

@socketio.on("message")
def sendMessage(message):
    print(request.sid,message)
    send(message, broadcast=True)
    # users.append(request.sid)
    # print(users)
    # send() function will emit a message vent by default

@app.route("/")
def homePage():
    doctors = []
    for i in range(6):
        data = {}
        data['name'] = "Jamila Nosirovna"
        data['region'] = "Tashkent"
        data['kasb'] = "Bolalar shifokori"
        data['page'] = "/doctors/"+data['name']
        data['shior'] = "Kasal bo'lish siz uchun emas"
        data['bio'] = "Oliy malumotli bolalar shifokori"
        data['image'] = "static/images/doctor.jpg"
        data['description'] = "Sadipscing labore amet rebum est et justo gubergren. Et eirmod ipsum sit diam ut magna lorem. Nonumy vero labore lorem sanctus rebum et lorem magna kasd, stet amet magna accusam consetetur eirmod. Kasd accusam sit ipsum sadipscing et at at sanctus et. Ipsum sit gubergren dolores et, consetetur justo invidunt at et aliquyam ut et vero clita. Diam sea sea no sed dolores diam"
        doctors.append(data)

    return render_template("index.html",doctors=doctors)

@app.route("/chat/<doctorname>")
def chat(doctorname):
    doctor = doctorname
    return render_template("message.html",doctor=doctor)

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
        
        return render_template("login.html",errors=errors)

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

            return render_template('index.html',user=user)
    
        return render_template("register.html")

    return render_template("register.html")

@app.route('/doctors/<doctor>')
def doctorsPage(doctor):
    data = {}
    data['name'] = doctor
    data['shior'] = "Kasal bo'lish siz uchun emas"
    data['bio'] = "Oliy malumotli bolalar shifokori"
    data['image'] = "images/doctor.jpg"
    data['description'] = "Sadipscing labore amet rebum est et justo gubergren. Et eirmod ipsum sit diam ut magna lorem. Nonumy vero labore lorem sanctus rebum et lorem magna kasd, stet amet magna accusam consetetur eirmod. Kasd accusam sit ipsum sadipscing et at at sanctus et. Ipsum sit gubergren dolores et, consetetur justo invidunt at et aliquyam ut et vero clita. Diam sea sea no sed dolores diam"
    return render_template('doctor/index.html',doctor=data)

@app.route('/users/<user>')
def usersPage(user):
    return render_template('user/index.html',user=user)

@app.route('/categorys/<category>')
def categorysPage(category):
    doctors=""
    return category

@app.route('/regions/<region>')
def regionsPage(region):
    doctors=""
    return region


if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app,host='localhost')
    # socketio.run(app,host='192.168.77.136')
