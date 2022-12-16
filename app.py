from flask import Flask,request, redirect, url_for,render_template
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import datetime
import time


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

flag=0
def alarm(set_alarm_timer):
    
    while True:
        time.sleep(1)
        current_time = datetime.datetime.now()
        now = current_time.strftime("%H:%M")      #converts time
        if now == set_alarm_timer:
            flag=1
            break
    if flag==1:
        return True    

    

    
    
class Todoo(db.Model):
    id=db.Column(db.Integer,primary_key=True) #creation of the table db 
    title=db.Column(db.String(100))
    hourtime=db.Column(db.Integer)
    mintime=db.Column(db.Integer)
    complete=db.Column(db.Boolean)

    
@app.route('/')
def index():
    todo_list=Todoo.query.all()
    return render_template('index.html',todo_list=todo_list) #passing the object

@app.route('/add', methods=["POST"])
def add():
    title=request.form.get('title')
    hourtime=request.form.get('hourtime')
    mintime=request.form.get('mintime')
    new_todo=Todoo(title=title,hourtime=hourtime,mintime=mintime,complete=True)
    db.session.add(new_todo)
    db.session.commit()
    set_alarm_timer = f"{hourtime}:{mintime}"
    if alarm(set_alarm_timer):
        return '<h1 style="text-align:center;margin-top:20%;">ALARM</h1>'
    
    return redirect(url_for("index"))


@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo=Todoo.query.filter_by(id=todo_id).first()     #to update the reminder option
    todo.complete=not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo=Todoo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit() 
    return redirect(url_for("index")) #redirect to  index url
 


if __name__=="__main__":
    with app.app_context():
        db.create_all()
   
    app.run(debug=True,port=8800)    #open in port 8800
