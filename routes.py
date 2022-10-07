from flask import Flask,render_template, redirect,url_for,request,session,flash
from datetime import datetime
from model import *
import sys

app=Flask(__name__)
app.config['SECRET_KEY']='1234'    




@app.before_request
def require_login():
    allowed_routes=['login','home','register','reward']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form['email']
        password=request.form['password']
        alert=Login_firebase(username,password) 
        print(alert)
        if alert=="Failed":
            return redirect(url_for('register'))
        else:
            session['username']=username
            session['name']=alert
            re =  add_rewards_firebase(username,1,"Login")
            print(re)
            return redirect(url_for('home'))
       
    return render_template('login.html')


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        username=request.form['email']
        name=request.form['name']
        password=request.form['password']
        interests=request.form['Interests']
        address=request.form['address']
        comfirm_password=request.form['confirm-password']
        if address=="":
            address="NA"
        if interests=="":
            interests="NA"
        if comfirm_password == password:
            alert=Register_firebase(username,password,name,interests,address) 
            if alert=="Failed":
                return redirect(url_for('register'))
            else:
                session['username']=username
                session['name']=name
                add_rewards_firebase(username,25,"Registration")
                return redirect(url_for('home'))
       
    return render_template('register.html')

@app.route('/',methods=['GET','POST'])
def home():
    active="active"
    if 'username' in session:
        name=session['name']
        reward = get_rewards_firebase(session['username'])
        
    else:
        name='default'
        reward="None"
    return render_template('home.html',name=name,reward=reward)

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('username')
    return redirect(url_for('home'))

@app.route('/quiz/<a>',methods=['GET','POST'])
def quiz(a):
    count=int(a)
    question=["","What is not operating system ","Mac OS is developed by?","Choose a programming language"]
    answers=[[],["DOS","Mac","C","Linux"],["Samsung","Apple","Microsoft","Google"],["C++","Figma","Canva","VS Code"]]  
   
    if request.method=="GET":
        answers1=["DOS","Mac","C","Linux"]
        return render_template('quiz.html',name=session['name'],Question="What is not operating system ",count=1,option0=answers1[0],option1=answers1[1],option2=answers1[2],option3=answers1[3])
    if request.method=="POST": 

        if count <=3:
            return render_template('quiz.html',name=session['name'],Question=question[count],count=count,option0=answers[count][0],option1=answers[count][1],option2=answers[count][2],option3=answers[count][3])
        else:
            return redirect(url_for('home'))

@app.route('/profile',methods=['GET'])
def profile():
    info = get_user_info(session['username'])
    name=session['name']
    email=session['username']
    interests=info['interests']
    address=info['address']
    react=info['re']
    reward = get_rewards_firebase(session['username'])
    return render_template('profile.html',name=name,reward=reward,email=email,address=address,interest=interests,react = react)


@app.route('/reward',methods=['GET'])
def reward():
    if 'username' in session: 
        name=session['name']
        email=session['username']
        reward = get_rewards_firebase(session['username'])
    else:
        name='default'
        reward="None"
    return render_template('reward.html',name=name,reward=reward,)


if __name__ == '__main__':
	app.run(debug = True)