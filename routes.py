from flask import Flask,render_template
from datetime import datetime

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def login():
    return render_template('login.html')

if __name__ == '__main__':
	app.run(debug = True)